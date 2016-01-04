import boneChain
import pymel.core as pm
from maya import cmds , OpenMaya
from Modules import control
from Utils import nameUtils

class IkChain(boneChain.BoneChain):

    def __init__(self, baseName = 'arm',side = 'm',size = 1,solver = 'ikSCsolver',
                 controlOrient = [0,0,0]):    
        '''
        Constructor
        '''
        #init
        self.baseName = baseName
        self.side = side
        self.size = size
        self.solver = solver
        self.controlOrient = controlOrient
        self.__acceptedSolvers = ['ikSCsolver','ikRPsolver']
        
        #cc
        self.ikCtrl = None
        self.poleVectorCtrl = None
        self.ikHandle = None
        self.ikCnst = None
        self.poleVectorCnst = None
        self.ikEffector = None
        
        #stretch data
        self.stretchStartLoc = None
        self.stretchEndLoc = None
        self.stretchData = None
        self.stretchBlendcolorNode = None
        self.length = None
        
        #elbow data
        self.armLockData = ['armElbow','elbowWrist','EBlock']
        self.legLockData = ['thighKnee','kneeAnkle','KNlock']
        self.lockUpStartLoc = None
        self.lockUpEndLoc = None
        self.lockDownStartLoc = None
        self.lockDownEndLoc = None        
        
        if self.solver == 'ikSCsolver':
            self.type = 'ikSC'
        else:
            self.type = 'ikRP'
        
        boneChain.BoneChain.__init__(self,baseName,side,type = self.type)
        
    def fromList(self,posList = [],orientList = [],autoOrient = 1):
        '''
        posList position
        orientList orient
        autoOrient bool whether use autoOrient List or not
        skipLast =whether add the last jj cc
        '''
        res = self.__checkSolver()
        if not res :
            return

        boneChain.BoneChain.fromList(self, posList, orientList, autoOrient)
        
        #create ctrl:
        self.__addControls() 
        
        #create ikHandle:
        ikName = nameUtils.getUniqueName(self.side,self.baseName + self.type,'iks')
        self.ikHandle,self.ikEffector = pm.ikHandle(sj = self.chain[0],ee = self.chain[2],solver = self.solver,n = ikName)
        pm.pointConstraint(self.ikCtrl.control,self.ikHandle,w = 1)
        
        #create PV 
        if self.solver == 'ikRPsolver':
            self.poleVectorCnst = pm.poleVectorConstraint(self.poleVectorCtrl.control,ikName,w = 1)
                         
            #lock and hide
            control.lockAndHideAttr(self.poleVectorCtrl.control,["rx","ry","rz","sx","sy","sz","v"])
                
        #add stretch    
        self.__stretchIk()
        
        if self.solver == 'ikRPsolver':
            self.__elbowKneeLock()
        
    def __addControls(self):

        #create control  
        self.ikCtrl = control.Control(self.side,self.baseName + self.type,self.size) 
        self.ikCtrl.circleSplitCtrl()
        self.ikCtrl.controlGrp.rotate.set(self.controlOrient)
        
        #snap to the last joint matrix = self.chain[i].worldMatrix.get()
        pm.xform(self.ikCtrl.controlGrp,ws = 1,matrix = self.chain[2].worldMatrix.get())
        #lock and hide
        control.lockAndHideAttr(self.ikCtrl.control,["sx","sy","sz","v"])
        
        #add stretch attr
        control.addFloatAttr(self.ikCtrl.control,['stretch'],0,1)
        
        if self.type == 'ikRP':
            #create control      
            self.poleVectorCtrl = control.Control(self.side,self.baseName + 'pv',self.size) 
            self.poleVectorCtrl.cubeCtrl()
            self.poleVectorCtrl.controlGrp.rotate.set(self.controlOrient)
            self.poleVectorCtrl.control.s.set(self.size / 4,self.size / 4,self.size / 4)
            pm.makeIdentity(self.poleVectorCtrl.control,apply = True,t = 0,r = 0,s = 1,n = 0,pn = 1)
            control.addFloatAttr(self.poleVectorCtrl.control,['elbow_lock'],0,1)
            
            #get joint info 
            startJoint = self.chain[0]
            midJoint = self.chain[1]
            endJoint = self.chain[2]
            
            #create pole vector
            #get info
            startInfo = pm.xform(startJoint,q= 1 ,ws = 1,t =1 )
            midInfo = pm.xform(midJoint,q= 1 ,ws = 1,t =1 )
            endInfo = pm.xform(endJoint,q= 1 ,ws = 1,t =1 )
            
            #Coordinate the info 
            startV = OpenMaya.MVector(startInfo[0] ,startInfo[1],startInfo[2])
            midV = OpenMaya.MVector(midInfo[0] ,midInfo[1],midInfo[2])
            endV = OpenMaya.MVector(endInfo[0] ,endInfo[1],endInfo[2])
            
            #Vector the info
            startEnd = endV - startV
            startMid = midV - startV
            
            #get Normal vector
            dotP = startMid * startEnd
            
            #get projection
            proj = float(dotP) / float(startEnd.length())
            
            startEndN = startEnd.normal()
            projV = startEndN * proj
            arrowV = startMid - projV
            arrowV *= 5
            finalV = arrowV + midV
            
            #place pole vector
            pm.xform(self.poleVectorCtrl.controlGrp,ws = 1,t= (finalV.x , finalV.y ,finalV.z))
            
            #aim curve
            ikBeamCurve = pm.curve(d = 1,p = [self.poleVectorCtrl.control.getTranslation(space = 'world'),
                                              self.chain[1].getTranslation(space = 'world')],k = [0,1],
                                    n = nameUtils.getUniqueName(self.side,'beam','cc'))
            ikBeamCurve.overrideEnabled.set(1)
            ikBeamCurve.overrideDisplayType.set(1)
            
            #cls
            beamClusterStart = pm.cluster(ikBeamCurve.cv[0])
            pm.rename(beamClusterStart[1].name(),nameUtils.getUniqueName(self.side,'beam' + 'Start','cls'))
            beamClusterStart[1].setParent(self.poleVectorCtrl.control)
            beamClusterStart[1].v.set(0)
            
            beamClusterEnd = pm.cluster(ikBeamCurve.cv[1])
            pm.rename(beamClusterEnd[1].name(),nameUtils.getUniqueName(self.side,'beam' + 'End','cls'))
            beamClusterEnd[1].setParent(self.chain[1])
            beamClusterEnd[1].v.set(0)
        
    def __stretchIk(self):

        self.stretchData = {}
        #name setting
        startLocName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_StretchStart','loc')
        endLocName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_StretchEnd','loc')
        distanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','dist')
                
        ratioMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Ratio','MDN')
        multipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','MDN')
        conditionNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','COND')
        blendcolorNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','BCN')
        
        #create node        
        ratioMultipleNode = pm.createNode('multiplyDivide',n = ratioMultipleNodeName)
        multipleNode = pm.createNode('multiplyDivide',n = multipleNodeName)
        conditionNode = pm.createNode('condition',n = conditionNodeName)
        self.stretchBlendcolorNode = pm.createNode('blendColors',n = blendcolorNodeName)
        
        #create loc 
        startPos = self.chain[0].worldMatrix.get()[-1][0:3]
        endPos = self.chain[2].worldMatrix.get()[-1][0:3]

        distShapeNode = pm.distanceDimension( sp = startPos, ep = endPos)
        distTransNode = pm.ls(sl = 1)[1]
        pm.rename(distTransNode,distanceBetweenNodeName)
        
        startLocCon = distTransNode.getShapes()[0].startPoint
        endLocCon = distTransNode.getShapes()[0].endPoint
        
        #get start loc
        if pm.connectionInfo(startLocCon,id = 1):
            startLocInfo = pm.connectionInfo(startLocCon,sourceFromDestination=True)
            oriStartLocName = startLocInfo.split('.')[0]
            pm.select(oriStartLocName)
            startLocShape = pm.selected()[0]
            self.stretchStartLoc = startLocShape.getParent()
            pm.rename(self.stretchStartLoc,startLocName)
        
        #get end loc
        if pm.connectionInfo(endLocCon,id = 1):
            endLocInfo = pm.connectionInfo(endLocCon,sourceFromDestination=True)
            oriEndLocName = endLocInfo.split('.')[0]
            pm.select(oriEndLocName)
            endLocShape = pm.selected()[0]
            self.stretchEndLoc = endLocShape.getParent()
            pm.rename(self.stretchEndLoc,endLocName)
        
        #connect to the dist
        #base on trans
        self.length = distTransNode.distance.get()
        distTransNode.distance.connect(ratioMultipleNode.input1X)
        ratioMultipleNode.input2X.set(self.chain[1].tx.get() + self.chain[2].tx.get())
        ratioMultipleNode.operation.set(2)
        
        #set cond node
        ratioMultipleNode.outputX.connect(conditionNode.firstTerm)
        ratioMultipleNode.outputX.connect(conditionNode.colorIfFalseR)
        conditionNode.secondTerm.set(1)
        conditionNode.operation.set(5)
        conditionNode.colorIfTrueR.set(1)
        
        #set multiple node
        conditionNode.outColorR.connect(multipleNode.input1X)
        conditionNode.outColorR.connect(multipleNode.input1Y)
        multipleNode.input2X.set(self.chain[1].tx.get())
        multipleNode.input2Y.set(self.chain[2].tx.get())
                
        #set stretch BCN switch
        multipleNode.outputX.connect(self.stretchBlendcolorNode.color1R)
        multipleNode.outputY.connect(self.stretchBlendcolorNode.color1G)
        self.stretchBlendcolorNode.color2R.set(self.chain[1].tx.get())
        self.stretchBlendcolorNode.color2G.set(self.chain[2].tx.get())
        self.ikCtrl.control.stretch.connect(self.stretchBlendcolorNode.blender)
#         stretchBlendcolorNode.outputR.connect(self.chain[1].tx)
#         stretchBlendcolorNode.outputG.connect(self.chain[2].tx)
        
        #clean the scene
        distTransNode.v.set(0)
        self.stretchEndLoc.setParent(self.ikCtrl.control)
        self.stretchData["startLoc"] = self.stretchStartLoc
        self.stretchData["endLoc"] = self.stretchEndLoc
        self.stretchData["stretchMulti"] = multipleNode
        self.stretchData["stretchCondition"] = conditionNode
        self.stretchData["stretchDist"]  = distTransNode
        self.stretchData["stretchBlendcolorNode"]  = self.stretchBlendcolorNode
    
        if self.type != 'ikRP':
            self.stretchBlendcolorNode.outputR.connect(self.chain[1].tx)
            self.stretchBlendcolorNode.outputG.connect(self.chain[2].tx)
    
    def __elbowKneeLock(self):
    
        #name setting
        if self.baseName == 'arm':
            upStartLocName = nameUtils.getUniqueName(self.side,self.armLockData[0] + '_' + self.armLockData[2] + 'Start','loc')
            upEndLocName = nameUtils.getUniqueName(self.side,self.armLockData[0] + '_' + self.armLockData[2] + 'End','loc')
            downStartLocName = nameUtils.getUniqueName(self.side,self.armLockData[1] + '_' + self.armLockData[2] + 'Start','loc')
            downEndLocName = nameUtils.getUniqueName(self.side,self.armLockData[1] + '_' + self.armLockData[2] + 'End','loc')
            upDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.armLockData[0] + '_' + self.armLockData[2],'dist')
            lowertDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.armLockData[1] + '_' + self.armLockData[2],'dist')
                        
            lockBlendcolorNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_' + self.armLockData[2],'BCN')
            
        elif self.baseName == 'leg':
            upStartLocName = nameUtils.getUniqueName(self.side,self.legLockData[0] + '_' + self.legLockData[2] + 'Start','loc')
            upEndLocName = nameUtils.getUniqueName(self.side,self.legLockData[0] + '_' + self.legLockData[2] + 'End','loc')
            downStartLocName = nameUtils.getUniqueName(self.side,self.legLockData[1] + '_' + self.legLockData[2] + 'Start','loc')
            downEndLocName = nameUtils.getUniqueName(self.side,self.legLockData[1] + '_' + self.legLockData[2] + 'End','loc')
            upDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.legLockData[0] + '_' + self.legLockData[2],'dist')
            lowertDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.legLockData[1] + '_' + self.legLockData[2],'dist')
            
            lockBlendcolorNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.legLockData[2],'BCN')            
        
        #set command
        lockBlendcolorNode = pm.createNode('blendColors',n = lockBlendcolorNodeName)
        
        #create loc
        #get info
        upStartPos = self.chain[0].worldMatrix.get()[-1][0:3]
        midPos = self.poleVectorCtrl.control.worldMatrix.get()[-1][0:3]
        downEndPos = self.chain[2].worldMatrix.get()[-1][0:3]                
        
        #armEblow node create 
        upDistShapeNode = pm.distanceDimension( sp = upStartPos, ep = midPos)
        upDistTransNode = pm.ls(sl = 1)[1]
        pm.rename(upDistTransNode,upDistanceBetweenNodeName)
        
        upStartLocCon = upDistTransNode.getShapes()[0].startPoint
        upEndLocCon = upDistTransNode.getShapes()[0].endPoint        
        
        #get start loc
        if pm.connectionInfo(upStartLocCon,id = 1):
            upStartLocInfo = pm.connectionInfo(upStartLocCon,sourceFromDestination=True)
            oriUpStartLocName = upStartLocInfo.split('.')[0]
            pm.select(oriUpStartLocName)
            upStartLocShape = pm.selected()[0]
            self.lockUpStartLoc = upStartLocShape.getParent()
            pm.rename(self.lockUpStartLoc,upStartLocName)
        
        #get end loc
        if pm.connectionInfo(upEndLocCon,id = 1):
            upEndLocInfo = pm.connectionInfo(upEndLocCon,sourceFromDestination=True)
            oriUpEndLocName = upEndLocInfo.split('.')[0]
            pm.select(oriUpEndLocName)
            endUpLocShape = pm.selected()[0]
            self.lockUpEndLoc = endUpLocShape.getParent()
            pm.rename(self.lockUpEndLoc,upEndLocName)
            
        #elbowWrist node create 
        
        downDistShapeNode = pm.distanceDimension( sp = midPos, ep = downEndPos)
        downDistTransNode = pm.ls(sl = 1)[1]
        pm.rename(downDistTransNode,lowertDistanceBetweenNodeName)
         
        downStartLocCon = downDistTransNode.getShapes()[0].startPoint
        downEndLocCon = downDistTransNode.getShapes()[0].endPoint        
         
        #get start loc
        if pm.connectionInfo(downStartLocCon,id = 1):
            downStartLocInfo = pm.connectionInfo(downStartLocCon,sourceFromDestination=True)
            oriUpStartLocName = downStartLocInfo.split('.')[0]
            pm.select(oriUpStartLocName)
            downStartLocShape = pm.selected()[0]
            self.lockDownStartLoc = downStartLocShape.getParent()
            pm.rename(self.lockDownStartLoc ,downStartLocName)
         
        #get end loc
        if pm.connectionInfo(downEndLocCon,id = 1):
            downEndLocInfo = pm.connectionInfo(downEndLocCon,sourceFromDestination=True)
            oriDownEndLocName = downEndLocInfo.split('.')[0]
            pm.select(oriDownEndLocName)
            endDownLocShape = pm.selected()[0]
            self.lockDownEndLoc = endDownLocShape.getParent()
            pm.rename(self.lockDownEndLoc,downEndLocName)            
         
        ######
        pm.parent(self.lockUpEndLoc,self.poleVectorCtrl.control)
        pm.parent(self.lockDownStartLoc,self.poleVectorCtrl.control)
        self.lockDownEndLoc.setParent(self.ikCtrl.control)
         
#         #connect loc to the dist
#         #arm elbow dist
#         self.lockUpStartLoc.worldPosition[0].connect(upDistBetweenNode.point1) 
#         self.lockUpEndLoc.worldPosition[0].connect(upDistBetweenNode.point2) 
        upDistTransNode.distance.connect(lockBlendcolorNode.color1R)
#         
#         #elbow wrist dist
#         lockDownStartLoc.worldPosition[0].connect(lowerDistBetweenNode.point1) 
#         lockDownEndLoc.worldPosition[0].connect(lowerDistBetweenNode.point2) 
        downDistTransNode.distance.connect(lockBlendcolorNode.color1G)

        self.stretchData["stretchBlendcolorNode"].outputR.connect(lockBlendcolorNode.color2R)
        self.stretchData["stretchBlendcolorNode"].outputG.connect(lockBlendcolorNode.color2G)
         
        #set BCN switch
        self.poleVectorCtrl.control.elbow_lock.connect(lockBlendcolorNode.blender)
        lockBlendcolorNode.outputR.connect(self.chain[1].tx)
        lockBlendcolorNode.outputG.connect(self.chain[2].tx)
        
        #clean the scene
#         upDistTransNode.v.set(0)
#         downDistTransNode.v.set(0)
        self.lockUpStartLoc.v.set(0)
        self.lockUpEndLoc.v.set(0)
        self.stretchEndLoc.v.set(0)
        self.lockDownStartLoc.v.set(0)
        self.lockDownEndLoc.v.set(0)
        self.ikHandle.v.set(0)
        
    def __checkSolver(self):
        '''
        whether the solver is valid
        @return:bool
        '''                 
        
        if not self.solver in self.__acceptedSolvers :
            OpenMaya.MGlobal.displayError('plz provide a valid solver , accept value are :' + ','.join(self.__acceptedSolvers))
            return False
        return True

# from Modules.subModules import ikChain
# bc = ikChain.IkChain(solver = 'ikRPsolver')
# bc.fromList([[0,0,0],[4,2,2],[8,0,0]],autoOrient = 1) 
               
