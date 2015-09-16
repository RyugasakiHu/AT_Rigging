import boneChain
import pymel.core as pm
from maya import cmds , OpenMaya
from Modules import control
from Utils import nameUtils

#ik pc

class IkChain(boneChain.BoneChain):

    def __init__(self, baseName = 'arm',side = 'c',size = 1,solver = 'ikSCsolver',
                 controlOrient = [0,0,0],type = 'ikSC'):    
        '''
        Constructor
        '''
        
        self.baseName = baseName
        self.side = side
        self.size = size
        self.solver = solver
        self.controlOrient = controlOrient
        self.type = type
        
        self.__acceptedSolvers = ['ikSCsolver','ikRPsolver']
        self.__accpetedskipLast = [0,1]
        
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
        
        #elbow data
        self.armLockData = ['armElbow','elbowWrist','EBlock']
        self.legLockData = ['thighKnee','kneeAnkle','KNlock']
        self.lockUpStartLoc = None
        self.lockUpEndLoc = None
  
        
        boneChain.BoneChain.__init__(self, baseName, side,type = self.type)
        
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
        if self.type == 'ikRP':
            self.poleVectorCnst = pm.poleVectorConstraint(self.poleVectorCtrl.control,ikName,w = 1)
                         
            #lock and hide
            control.lockAndHideAttr(self.poleVectorCtrl.control,["rx","ry","rz","sx","sy","sz","v"])
                
        #add stretch    
        self.__stretchIk()
        
        if self.type == 'ikRP':
            self.__elbowKneeLock()
        
    def __addControls(self):

        #create control  
        self.ikCtrl = control.Control(self.side,self.baseName + self.type,self.size) 
        self.ikCtrl.circleCtrl()
        self.ikCtrl.controlGrp.rotate.set(self.controlOrient)
        
        #snap to the last joint matrix = self.chain[i].worldMatrix.get()
        pm.xform(self.ikCtrl.controlGrp,ws = 1,matrix = self.chain[2].worldMatrix.get())
        #lock and hide
        control.lockAndHideAttr(self.ikCtrl.control,["sx","sy","sz","v"])
        
        #add stretch attr
        control.addSwitchAttr(self.ikCtrl.control,['stretch'])
        
        if self.type == 'ikRP':
            #create control      
            self.poleVectorCtrl = control.Control(self.side,self.baseName + 'pv',self.size) 
            self.poleVectorCtrl.poleCtrl()
            self.poleVectorCtrl.controlGrp.rotate.set(self.controlOrient)
            control.addSwitchAttr(self.poleVectorCtrl.control,['elbow_lock'])
            
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
            arrowV *= 1 
            finalV = arrowV + midV
            
            #place pole vector
            pm.xform(self.poleVectorCtrl.controlGrp,ws = 1,t= (finalV.x , finalV.y ,finalV.z))
        
    def __stretchIk(self):

        self.stretchData = {}
        #name setting
        startLocName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_StretchStart','loc')
        endLocName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_StretchEnd','loc')
        ratioMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Ratio','MDN')
        multipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','MDN')
        conditionNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','COND')
        blendcolorNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','BCN')
        distanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.type + '_Stretch','dist')
        
        #set command
        self.stretchStartLoc = pm.spaceLocator(n = startLocName)
        self.stretchEndLoc = pm.spaceLocator(n = endLocName)
        ratioMultipleNode = pm.createNode('multiplyDivide',n = ratioMultipleNodeName)
        multipleNode = pm.createNode('multiplyDivide',n = multipleNodeName)
        conditionNode = pm.createNode('condition',n = conditionNodeName)
        self.stretchBlendcolorNode = pm.createNode('blendColors',n = blendcolorNodeName)
        distBetweenNode = pm.createNode('distanceBetween',n = distanceBetweenNodeName)
        
        #align loc
        startPos = self.chain[0].worldMatrix.get()
        endPos = self.chain[2].worldMatrix.get()
        pm.xform(self.stretchStartLoc,matrix = startPos)
        pm.xform(self.stretchEndLoc,matrix = endPos)
        
        #connect to the dist
        #base on trans
        self.stretchStartLoc.worldPosition[0].connect(distBetweenNode.point1) 
        self.stretchEndLoc.worldPosition[0].connect(distBetweenNode.point2) 
        distBetweenNode.distance.connect(ratioMultipleNode.input1X)
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
        self.stretchEndLoc.setParent(self.ikCtrl.control)
        self.stretchData["startLoc"] = self.stretchStartLoc
        self.stretchData["endLoc"] = self.stretchEndLoc
        self.stretchData["stretchMulti"] = multipleNode
        self.stretchData["stretchCondition"] = conditionNode
        self.stretchData["stretchDist"]  = distBetweenNode
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
            lockBlendcolorNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_' + self.armLockData[2],'BCN')
            upperDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.armLockData[0] + '_' + self.armLockData[2],'dist')
            lowertDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.armLockData[1] + '_' + self.armLockData[2],'dist')
        elif self.baseName == 'leg':
            upStartLocName = nameUtils.getUniqueName(self.side,self.legLockData[0] + '_' + self.legLockData[2] + 'Start','loc')
            upEndLocName = nameUtils.getUniqueName(self.side,self.legLockData[0] + '_' + self.legLockData[2] + 'End','loc')
            downStartLocName = nameUtils.getUniqueName(self.side,self.legLockData[1] + '_' + self.legLockData[2] + 'Start','loc')
            downEndLocName = nameUtils.getUniqueName(self.side,self.legLockData[1] + '_' + self.legLockData[2] + 'End','loc')
            lockBlendcolorNodeName = nameUtils.getUniqueName(self.side,self.baseName + self.legLockData[2],'BCN')
            upperDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.legLockData[0] + '_' + self.legLockData[2],'dist')
            lowertDistanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.legLockData[1] + '_' + self.legLockData[2],'dist')
                
        
        #set command
        self.lockUpStartLoc = pm.spaceLocator(n = upStartLocName)
        self.lockUpEndLoc = pm.spaceLocator(n = upEndLocName)
        lockDownStartLoc = pm.spaceLocator(n = downStartLocName)
        lockDownEndLoc = pm.spaceLocator(n = downEndLocName)
        lockBlendcolorNode = pm.createNode('blendColors',n = lockBlendcolorNodeName)
        upperDistBetweenNode = pm.createNode('distanceBetween',n = upperDistanceBetweenNodeName)
        lowerDistBetweenNode = pm.createNode('distanceBetween',n = lowertDistanceBetweenNodeName)    
        
        #align loc and parent
        startPos = self.chain[0].worldMatrix.get()
        midPos = self.poleVectorCtrl.control.worldMatrix.get()
        endPos = self.chain[2].worldMatrix.get()
        
        pm.xform(self.lockUpStartLoc,matrix = startPos)
        pm.xform(self.lockUpEndLoc,matrix = midPos)
        pm.xform(lockDownStartLoc,matrix = midPos)
        pm.xform(lockDownEndLoc,matrix = endPos)
        
        pm.parent(self.lockUpEndLoc,self.poleVectorCtrl.control)
        pm.parent(lockDownStartLoc,self.poleVectorCtrl.control)
        lockDownEndLoc.setParent(self.ikCtrl.control)
        
        #connect loc to the dist
        #arm elbow dist
        self.lockUpStartLoc.worldPosition[0].connect(upperDistBetweenNode.point1) 
        self.lockUpEndLoc.worldPosition[0].connect(upperDistBetweenNode.point2) 
        upperDistBetweenNode.distance.connect(lockBlendcolorNode.color1R)
        
        #elbow wrist dist
        lockDownStartLoc.worldPosition[0].connect(lowerDistBetweenNode.point1) 
        lockDownEndLoc.worldPosition[0].connect(lowerDistBetweenNode.point2) 
        lowerDistBetweenNode.distance.connect(lockBlendcolorNode.color1G)
        
        self.stretchData["stretchBlendcolorNode"].outputR.connect(lockBlendcolorNode.color2R)
        self.stretchData["stretchBlendcolorNode"].outputG.connect(lockBlendcolorNode.color2G)
        
        #set BCN switch
        self.poleVectorCtrl.control.elbow_lock.connect(lockBlendcolorNode.blender)
        lockBlendcolorNode.outputR.connect(self.chain[1].tx)
        lockBlendcolorNode.outputG.connect(self.chain[2].tx)
        
        #clean the scene
        self.lockUpStartLoc.v.set(0)
        self.lockUpEndLoc.v.set(0)
        self.stretchEndLoc.v.set(0)
        lockDownStartLoc.v.set(0)
        lockDownEndLoc.v.set(0)
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
# bc = ikChain.IkChain(solver = 'ikRPsolver',skipLast = 0)
# bc.fromList([[0,0,0],[4,2,2],[8,0,0]],autoOrient = 1) 
               
            
