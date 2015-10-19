import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy

class SpineModule(object):

    posSpineArray = [[],[],[]]

    def __init__(self,side = 'm',baseName = 'spine',segment = 9):
        
        #self para
        self.side = side
        self.baseName = baseName 
        self.segment = segment
        self.length  = None
        self.size = None
        self.spineFkBlendChain = None
        self.spineIkBlendJoint = None
        
        #guide para
        self.guideCc = None
        self.guideTrv = None
        self.guides = None
        self.guideGrp = None
        
        #ctrl
        self.ribbonJc = None
        self.spineCc = None
        self.spineGrp = None
        self.config_node = None
        
        #stretch
        self.stretchLength = None
        self.stretchStartLoc = None
        self.stretchEndLoc = None
        
        #nameList
        self.nameList = ['Hip','Mid','Chest']
        
        
    def buildGuides(self):
        
        #set hi
        self.hi = hierarchy.Hierarchy(characterName = 'test')
        self.hi.build()        
        
        #group
        self.guides = []
        
        #build curve
        self.guideCc = pm.curve(d = 3,p = [[0,9.040668,0.0623416],[0,10.507795,0.181759],[0,11.991982,0.164699],
                                         [0,13.322632,-0.108255],[0,14.397388,-0.0570757]],k = [0,0,0,1,2,2,2],
                              n = nameUtils.getUniqueName(self.side,self.baseName + '_cc','gud'))      
        curveInfo = pm.createNode('curveInfo',n = nameUtils.getUniqueName(self.side,self.baseName + '_cc','cvINFO'))
        self.guideCc.getShape().worldSpace.connect(curveInfo.inputCurve)
        self.length = curveInfo.arcLength.get()
        
    def build(self):
        
        #build Trv
        self.guideTrv = pm.joint(p = [0,0,0],n = nameUtils.getUniqueName(self.side,self.baseName,'trv'))
        moPathName = nameUtils.getUniqueName(self.side,self.baseName,'MOP')
        moPathNode = pm.pathAnimation(self.guideCc,self.guideTrv,fractionMode = 1,follow = 1,followAxis = 'x',upAxis = 'y',worldUpType = 'vector',
                                      worldUpVector = [0,1,0],inverseUp = 0,inverseFront = 0,bank = 0,startTimeU = 1,endTimeU = 24,n = moPathName)        
        pm.disconnectAttr(moPathNode + '_uValue.output',moPathNode + '.uValue')
        
        #set Trv Loc:
        trvPosList = []

        for num in range(0,self.segment):
            trvDis = num * (1 / float(self.segment-1))
            pm.setAttr(moPathNode + '.uValue',trvDis)
            trvPos = self.guideTrv.getTranslation(space = 'world')
            trvPosList.append(trvPos)

        #set loc
        #set loc grp
        for i,p in enumerate(trvPosList):
            trvName = nameUtils.getUniqueName(self.side,self.baseName,'gud')
            loc = pm.spaceLocator(n = trvName)
            loc.t.set(p)
            self.guides.append(loc)
            loc.setParent(self.guideGrp)
            
        tempGuides = list(self.guides)
        tempGuides.reverse()
        
        #set loc grp
        for i in range(len(tempGuides)):
            if i != (len(tempGuides) - 1):
                pm.parent(tempGuides[i],tempGuides[i + 1])            
        
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')        
        self.guideGrp = pm.group(self.guideCc,self.guides[0],self.guideTrv,n = name)   
        self.guideGrp.v.set(0)
        
        self.__bodyCtrl()
        self.__fkJj()
        self.__ikJj()
        self.__SquashStretch()
        
    def __bodyCtrl(self):
         
        self.config_node = control.Control(self.side,self.baseName + 'Cc',size = self.length / 2) 
        self.config_node.bodyCtrl()
        
        midPos = pm.xform(self.guides[(self.segment - 1) / 2],query=1,ws=1,rp=1)
        
        #move the target object
        pm.move(midPos[0],midPos[1],midPos[2] - self.length / 1.5,self.config_node.controlGrp,a=True)
        pm.setAttr(self.config_node.controlGrp + '.ry',90)
        self.config_node.controlGrp.setParent(self.hi.CC)
        
    def __fkJj(self):
        
        #create fk jj
        self.guideSpinePos = [x.getTranslation(space = 'world') for x in self.guides]
        self.guideSpineRot = [x.getRotation(space = 'world') for x in self.guides]
        
        self.spineFkBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'fk')
        self.spineFkBlendChain.fromList(self.guideSpinePos,self.guideSpineRot)
    
    def __ikJj(self):    
        
        #create IKRibbonSpine
        #ribbon spine info:
        curveInfo = [0,(self.segment - 1) / 4,(self.segment - 1) / 2,
                     ((self.segment - 1) / 2 + (self.segment - 1)) / 2,
                     (self.segment - 1)]
        ribbonCurve = []
        
        #create curve
        for jjInfo in curveInfo:
            ribonJjPos = self.spineFkBlendChain.chain[jjInfo].getTranslation(space = 'world') 
            ribbonCurve.append(ribonJjPos)
        
        #set ribbon offset
        offset = 0.0
        if self.length / self.segment <= 1:
            offset = 0.5
        else :
            offset = self.length / ((self.segment - 1) / 2)
        
        #set ribbon cur
        ribbonCurveL = pm.curve(d = 3,p = [ribbonCurve[0],ribbonCurve[1],ribbonCurve[2],ribbonCurve[3],ribbonCurve[4]],
                                k = [0,0,0,1,2,2,2],n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbonL','gud'))

        pm.move(offset,0,0,ribbonCurveL)         

        ribbonCurveR = pm.curve(d = 3,p = [ribbonCurve[0],ribbonCurve[1],ribbonCurve[2],ribbonCurve[3],ribbonCurve[4]],
                                k = [0,0,0,1,2,2,2],n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbonR','gud')) 
         
        pm.move(-offset,0,0,ribbonCurveR)     
        
        ribbonCurveR.setParent(self.guideGrp)
        ribbonCurveL.setParent(self.guideGrp)
        
        #create ribbon surf
        ribbonSurf = pm.loft(ribbonCurveR,ribbonCurveL,ch = 0,u = 1,c = 0,ar = 1,d = 3,ss = 1, rn = 0,po = 0,rsn = 1,
                             n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbon','surf'))
        
        ribbonClusList = []
        self.ribbonJc = []
        self.spineCc = []
        
        #get Jc pos
        for num in [0,2,4]:
            pos = pm.select(ribbonSurf[0] + '.cv[' + str(num) + '][0:3]',r = 1)
            clus = pm.cluster()
            pm.rename(clus[1],nameUtils.getUniqueName(self.side,self.baseName + '_ribbon','cls'))
            ribbonClusList.append(clus)
            pm.select(cl = 1)
            
        #set Jc and Jc ctrl    
        for num,x in enumerate(ribbonClusList):
            jc = pm.joint(p = x[1].getRotatePivot(),
                          n = nameUtils.getUniqueName(self.side,self.baseName + self.nameList[num],'jc'),
                          radius = self.length / 3)
            self.ribbonJc.append(jc)
            pm.select(cl = 1)
            pm.delete(ribbonClusList[num])
            pm.select(cl = 1)
            cc = control.Control(self.side,self.baseName + self.nameList[num],size = self.length / 2) 
            cc.circleCtrl()
            self.spineCc.append(cc.control)
            pm.xform(cc.controlGrp,ws = 1,matrix = jc.worldMatrix.get())
            pm.setAttr(cc.controlGrp + '.rz',90)
        
        #skin Jc
        for num,jc in enumerate(self.ribbonJc):
            jc.setParent(self.spineCc[num])

        pm.skinCluster(self.ribbonJc[0],self.ribbonJc[1],self.ribbonJc[2],ribbonSurf[0],
                       tsb = 1,ih = 1,mi = 3,dr = 4,rui = 1)
        
        #set fol
        #create / rename fol
        pm.select(ribbonSurf[0],r = 1)
        pm.runtime.CreateHair(9,1,2,0,0,0,0,5,0,1,2,1)
        pm.select('*surfFollicle*',r = 1)
        folSel = pm.select('*surfFollicleShape*',tgl = 1)
        fol = pm.ls(sl = 1)
        folList = []
               
        for i in range(len(fol)):
            j = i + 1
            pm.rename(fol[i],nameUtils.getUniqueName(self.side,self.baseName,'fol'))
            folList.append(fol[i])
             
        #clean scene    
        pm.parent(w = 1)
        pm.delete('hairSystem*')
        pm.delete('curve*')
        pm.delete('nucleus*')   
        pm.delete('pfxHair1')        
        folGrp = pm.group(n = nameUtils.getUniqueName(self.side,self.baseName + 'Fol','grp')  )
        
        #rebuild fol pos
        self.spineIkBlendJoint = []
        for num,fol in enumerate(folList):
            pm.setAttr(fol + '.parameterU',(num * (1 / float(self.segment - 1))))
            jj = pm.joint(p = (0,0,0),n = nameUtils.getUniqueName(self.side,self.baseName,'jj'),
                          radius = self.length / 5)
            self.spineIkBlendJoint.append(jj)
            jj.setParent(fol)
            tempCube = pm.polyCube(ch = 1,o = 1,w = 1,h = 1,d = 1,cuv = 4,
                                   n = nameUtils.getUniqueName(self.side,self.baseName,'cube'))
            tempCube[0].setParent(jj)
            jj.translateX.set(0)
            jj.translateY.set(0)
            jj.translateZ.set(0)

            
            
        #create spine grp
        self.spineGrp = pm.group(self.spineCc[0].getParent(),self.spineCc[1].getParent(),self.spineCc[2].getParent(),folGrp,ribbonSurf[0],
                 n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))
        ribbonSurf[0].inheritsTransform.set(0)
        folGrp.inheritsTransform.set(0)
        
        #clean
        self.spineGrp.setParent(self.config_node.control)
        
        '''put chest ctrl under chest cc'''
        '''put leg under hip cc'''
        
   
    def __SquashStretch(self):
        
        #create Name
        startLocName = nameUtils.getUniqueName(self.side,self.baseName + '_StretchStart','loc')
        endLocName = nameUtils.getUniqueName(self.side,self.baseName + '_StretchEnd','loc')
        distanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','dist')
        multipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','MDN')
        
        #remap Node
        remapNodeNum = ((self.segment - 1) / 2) + 1
        remapList = []
        for num in range(0,remapNodeNum):
            remapNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','RV')
            remapNode = pm.createNode('remapValue',n = remapNodeName)
            remapList.append(remapNode)
        
        #createNode
        distBetweenNode = pm.createNode('distanceBetween',n = distanceBetweenNodeName)
        multipleNode = pm.createNode('multiplyDivide',n = multipleNodeName)
        
        #set command
        self.stretchStartLoc = pm.spaceLocator(n = startLocName)
        self.stretchEndLoc = pm.spaceLocator(n = endLocName)
        
        #align loc
        startPos = self.ribbonJc[0].worldMatrix.get()
        endPos = self.ribbonJc[-1].worldMatrix.get()
        pm.xform(self.stretchStartLoc,matrix = startPos)
        pm.xform(self.stretchEndLoc,matrix = endPos)
        self.stretchStartLoc.setParent(self.spineCc[0])
        self.stretchEndLoc.setParent(self.spineCc[-1])
        
        #connect
        #stretch
        self.stretchStartLoc.worldPosition[0].connect(distBetweenNode.point1) 
        self.stretchEndLoc.worldPosition[0].connect(distBetweenNode.point2) 
        self.stretchLength = distBetweenNode.distance.get()
        
        #multiple    
        distBetweenNode.distance.connect(multipleNode.input1X)
        multipleNode.input2X.set(self.stretchLength)
        multipleNode.operation.set(2)
        
        #remap    
        for num,remapNode in enumerate(remapList):
            multipleNode.outputX.connect(remapNode.inputValue)
            remapNode.inputMax.set(2)
            remapNode.outputMin.set(2)
            remapNode.outputMax.set(0)
            if self.segment - num - 1 != num:
                print remapNode
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sx)
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sz)
                remapNode.outValue.connect(self.spineIkBlendJoint[self.segment - num - 1].sx)
                remapNode.outValue.connect(self.spineIkBlendJoint[self.segment - num - 1].sz)
                remapNode.value[2].value_FloatValue.set(0.5)
                remapNode.value[2].value_Position.set(0.5)
                remapNode.value[2].value_Interp.set(1)             
                
            else:
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sx)
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sz)
                remapNode.value[2].value_FloatValue.set(0.5)
                remapNode.value[2].value_Position.set(0.5)
                remapNode.value[2].value_Interp.set(1)                 
            
# import maya.cmds as mc
# from see import see
# pathOfFiles = 'C:\Users\UV\Desktop\Rigging workshop/'
# fileType = 'obj'
# files = mc.getFileList(folder = pathOfFiles,fs = '*.%s' % fileType)
# mc.file(new = 1,f = 1)
#  
# if len(files) == 0:
#     mc.warning('no files found')
# else:
#     for fi in files:
#         print pathOfFiles + fi
#         mc.file(pathOfFiles + fi,i = True)
#          
# import sys
# myPath = 'C:/eclipse/test/OOP/AutoRig'
#  
# if not myPath in sys.path:
#     sys.path.append(myPath)    
#      
# import reloadMain
# reload(reloadMain)   
#  
# from Modules import spineModule
# rp = spineModule.SpineModule()
# rp.buildGuides()
# rp.build()              
