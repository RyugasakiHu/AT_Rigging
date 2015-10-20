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
        self.spineFkRevBlendChain = None 
        self.spineFkGrp = None
        self.spineIkGrp = None
        
        #guide para
        self.trvPosList = None
        self.guideCc = None
        self.guideTrv = None
        self.guideGrp = None        
        self.fkGuides = None
        self.revFkGuides = None
        
        #ctrl
        self.ribbonJc = None
        self.spineCc = None
        self.config_node = None
        
        #stretch
        self.stretchLength = None
        self.stretchStartLoc = None
        self.stretchEndLoc = None
        self.stretchCube = None
        
        #nameList
        self.nameList = ['Hip','Mid','Chest']
        
        
    def buildGuides(self):
        
        #set hi
        self.hi = hierarchy.Hierarchy(characterName = 'test')
        self.hi.build()        
        
        #group
        self.fkGuides = []
        
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
        self.trvPosList = []

        for num in range(0,self.segment):
            trvDis = num * (1 / float(self.segment-1))
            pm.setAttr(moPathNode + '.uValue',trvDis)
            trvPos = self.guideTrv.getTranslation(space = 'world')
            self.trvPosList.append(trvPos)

        #set loc
        #set loc grp
        for i,p in enumerate(self.trvPosList):
            trvName = nameUtils.getUniqueName(self.side,self.baseName + 'Fk','gud')
            loc = pm.spaceLocator(n = trvName)
            loc.t.set(p)
            loc.r.set(0,0,90)
            self.fkGuides.append(loc)
            loc.setParent(self.guideGrp)
            
        tempGuides = list(self.fkGuides)
        tempGuides.reverse()
        
        #set loc grp
        for i in range(len(tempGuides)):
            if i != (len(tempGuides) - 1):
                pm.parent(tempGuides[i],tempGuides[i + 1])            
        
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')        
        self.guideGrp = pm.group(self.guideCc,self.fkGuides[0],self.guideTrv,n = name)   
        self.guideGrp.v.set(0)
        
        self.__bodyCtrl()
        self.__fkJj()
        self.__ikJj()
        self.__SquashStretch()
#         self.__enchanceFk()
        
    def __bodyCtrl(self):
         
        self.config_node = control.Control(self.side,self.baseName + 'Cc',size = self.length / 2) 
        self.config_node.bodyCtrl()
        
        midPos = pm.xform(self.fkGuides[(self.segment - 1) / 2],query=1,ws=1,rp=1)
        
        #move the target object
        pm.move(midPos[0],midPos[1],midPos[2] - self.length / 1.5,self.config_node.controlGrp,a=True)
        pm.setAttr(self.config_node.controlGrp + '.ry',90)
        self.config_node.controlGrp.setParent(self.hi.CC)
        
        #lock and hide
        control.lockAndHideAttr(self.config_node.control,['sx','sy','sz','v'])
        
        #add attr
        control.addFloatAttr(self.config_node.control,['volume'],0,1)
        pm.addAttr(self.config_node.control,ln = '______',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '.______',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['bend_up','bend_mid','bend_lo'],-3600,3600)

        pm.addAttr(self.config_node.control,ln = '_______',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '._______',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['bend_up_rev','bend_mid_rev','bend_lo_rev'],-3600,3600)        
        
        
    def __fkJj(self):
        
        #create fk jj
        self.spineFkRevBlendChain = []        
        self.guideSpineFkPos = [x.getTranslation(space = 'world') for x in self.fkGuides]
        self.guideSpineFkRot = [x.getRotation(space = 'world') for x in self.fkGuides]
        
        self.spineFkBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'fk')
        self.spineFkBlendChain.fromList(self.guideSpineFkPos,self.guideSpineFkRot,autoOrient = 1)
        
        #create revFk MDN node
        fkMultipleNodeList = []
        for num,fkJj in enumerate(self.spineFkBlendChain.chain):
            fkMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'Fk','MDN')
            fkMultipleNode = pm.createNode('multiplyDivide',n = fkMultipleNodeName)
            fkMultipleNodeList.append(fkMultipleNode)
            fkJj.rx.connect(fkMultipleNode.input1X)
            fkJj.ry.connect(fkMultipleNode.input1Y)
            fkJj.rz.connect(fkMultipleNode.input1Z)
            fkMultipleNode.input2X.set(-1)
            fkMultipleNode.input2Y.set(-1)
            fkMultipleNode.input2Z.set(-1)
            
        #clean up
        self.spineFkGrp = pm.group(self.spineFkBlendChain.chain[0],
                                   n = nameUtils.getUniqueName(self.side,self.baseName + 'Fk','grp'))
        
        self.spineFkGrp.setParent(self.config_node.control)
        
        #create revFk
        self.revFkGuides = []
        self.trvPosList
        for num,pos in enumerate(self.trvPosList):
            revFkName = nameUtils.getUniqueName(self.side,self.baseName + 'RevFk','gud')
            loc = pm.spaceLocator(n = revFkName)
            loc.t.set(pos)
            self.revFkGuides.append(loc)
            loc.setParent(self.guideGrp)
        
        for num,fk in enumerate(self.revFkGuides):
            if num != len(self.revFkGuides) - 1:
                pm.parent(self.revFkGuides[num],self.revFkGuides[num + 1])
                
        self.revFkGuides.reverse()    
        self.guideSpineRevFkPos = [x.getTranslation(space = 'world') for x in self.revFkGuides]
        self.guideSpineRevFkRot = [x.getRotation(space = 'world') for x in self.revFkGuides]
 
        self.spineRevFkBlendChain = boneChain.BoneChain(self.baseName + 'Rev',self.side,type = 'fk')
        self.spineRevFkBlendChain.fromList(self.guideSpineRevFkPos,self.guideSpineRevFkRot,autoOrient = 1)       
        self.spineRevFkBlendChain.chain[0].setParent(self.spineFkBlendChain.chain[-1])

        #set Rotate
        '''
        this part could be delete (z axis trash node)
        '''
        #nodename
        multiplefkBendNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkBend','MDN')
        multiplefkRevBendNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkRevBend','MDN')
         
        #nodecreate
        multiplefkBendNode = pm.createNode('multiplyDivide',n = multiplefkBendNodeName)
        multiplefkRevBendNode = pm.createNode('multiplyDivide',n = multiplefkRevBendNodeName)
        
        #connect
        self.config_node.control.bend_lo.connect(multiplefkBendNode.input1X)
        self.config_node.control.bend_mid.connect(multiplefkBendNode.input1Y)
        self.config_node.control.bend_up.connect(multiplefkBendNode.input1Z)
        self.config_node.control.bend_lo_rev.connect(multiplefkRevBendNode.input1X)
        self.config_node.control.bend_mid_rev.connect(multiplefkRevBendNode.input1Y)
        self.config_node.control.bend_up_rev.connect(multiplefkRevBendNode.input1Z)
        
        multiplefkBendNode.input2X.set(-1)
        multiplefkBendNode.input2Y.set(-1)
        multiplefkBendNode.input2Z.set(-1)
        multiplefkBendNode.operation.set(1)
        
        multiplefkRevBendNode.input2X.set(-1)
        multiplefkRevBendNode.input2Y.set(-1)
        multiplefkRevBendNode.input2Z.set(-1)
        multiplefkRevBendNode.operation.set(1)        
        
        #fk
        for num,chain in enumerate(self.spineFkBlendChain.chain):
            if 1 <= num <= (self.segment / 3):
                multiplefkBendNode.outputX.connect(chain.rz)
            elif (self.segment / 3) < num < ((self.segment / 3) * 2):
                multiplefkBendNode.outputY.connect(chain.rz)
            elif ((self.segment / 3) * 2) <= num < (self.segment - 1):
                multiplefkBendNode.outputZ.connect(chain.rz)
           
        #revFk        
        for num,chain in enumerate(self.spineRevFkBlendChain.chain):
            fkMultipleNodeList[num].outputX.connect(chain.rz)
#             if 1 <= num <= (self.segment / 3 - 1):
#                 multiplefkRevBendNode.outputX.connect(chain.rz)
#             elif (self.segment / 3 - 1) < num < ((self.segment / 3) * 2):
#                 multiplefkRevBendNode.outputY.connect(chain.rz)
#             elif ((self.segment / 3) * 2) <= num < (self.segment - 1):
#                 multiplefkRevBendNode.outputZ.connect(chain.rz)     
#                 

                 
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
        self.stretchCube = []
        for num,fol in enumerate(folList):
            pm.setAttr(fol + '.parameterU',(num * (1 / float(self.segment - 1))))
            jj = pm.joint(p = (0,0,0),n = nameUtils.getUniqueName(self.side,self.baseName,'jj'),
                          radius = self.length / 5)
            self.spineIkBlendJoint.append(jj)
            jj.setParent(fol)
            tempCube = pm.polyCube(ch = 1,o = 1,w = float(self.length / 5),h = float(self.length / 10),
                                   d = float(self.length / 5),cuv = 4,n = nameUtils.getUniqueName(self.side,self.baseName,'cube'))
            tempCube[0].setParent(jj)
#             tempCube[0].v.set(0)
            self.stretchCube.append(tempCube[0])
            jj.translateX.set(0)
            jj.translateY.set(0)
            jj.translateZ.set(0)
            
        #create spine grp
        self.spineIkGrp = pm.group(self.spineCc[0].getParent(),self.spineCc[1].getParent(),self.spineCc[2].getParent(),folGrp,ribbonSurf[0],
                                 n = nameUtils.getUniqueName(self.side,self.baseName + 'Ik','grp'))
        ribbonSurf[0].inheritsTransform.set(0)
        folGrp.inheritsTransform.set(0)
        
        #clean
        self.spineIkGrp.setParent(self.config_node.control)
        
        #temp
        self.spineIkGrp.v.set(0)
        
        '''put chest ctrl under chest cc'''
        '''put leg under hip cc'''
        
    def __SquashStretch(self):
        
        #perpare Name
        startLocName = nameUtils.getUniqueName(self.side,self.baseName + '_StretchStart','loc')
        endLocName = nameUtils.getUniqueName(self.side,self.baseName + '_StretchEnd','loc')
        distanceBetweenNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','dist')
        multipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','MDN')
        conditionNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','COND')
        colorRedRemapValueName = nameUtils.getUniqueName(self.side,self.baseName + 'Red','RV')        
        colorGreenRemapValueName = nameUtils.getUniqueName(self.side,self.baseName + 'Green','RV')
#         expressionNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','EXP')
        stretchSwitchNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','BCN')
        
        #remap Node for ikJj scale
        remapNodeRed = pm.createNode('remapValue',n = colorRedRemapValueName)
        remapNodeGreen = pm.createNode('remapValue',n = colorGreenRemapValueName)
        remapNodeNum = ((self.segment - 1) / 2) + 1
        remapList = []
        for num in range(0,remapNodeNum):
            remapNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_Stretch','RV')
            remapNode = pm.createNode('remapValue',n = remapNodeName)
            remapList.append(remapNode)
        
        #createNode
        distBetweenNode = pm.createNode('distanceBetween',n = distanceBetweenNodeName)
        multipleNode = pm.createNode('multiplyDivide',n = multipleNodeName)
        conditionNode = pm.createNode('condition',n = conditionNodeName)
        stretchSwitchNode = pm.createNode('blendColors',n = conditionNodeName)
        
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
        self.config_node.control.volume.connect(stretchSwitchNode.blender)
        stretchSwitchNode.color1R.set(1)
        multipleNode.outputX.connect(stretchSwitchNode.color2R)
        
        #multiple    
        distBetweenNode.distance.connect(multipleNode.input1X)
        multipleNode.input2X.set(self.stretchLength)
        multipleNode.operation.set(2)
        
        #remap    
        for num,remapNode in enumerate(remapList):
            stretchSwitchNode.outputR.connect(remapNode.inputValue)
            remapNode.inputMax.set(2)
            remapNode.outputMin.set(3)
            remapNode.outputMax.set(-1)
            if (self.segment - num - 1) != num:
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sx)
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sz)
                remapNode.outValue.connect(self.spineIkBlendJoint[self.segment - num - 1].sx)
                remapNode.outValue.connect(self.spineIkBlendJoint[self.segment - num - 1].sz)
                
            else:
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sx)
                remapNode.outValue.connect(self.spineIkBlendJoint[num].sz)
                
            remapNode.value[0].value_FloatValue.set(num * float(1 / float(self.segment - 1)))
            remapNode.value[0].value_Position.set(0)   
            remapNode.value[1].value_FloatValue.set(float(1 - (num * float(1 / float(self.segment - 1)))))
            remapNode.value[1].value_Position.set(1)                                                        
            remapNode.value[2].value_FloatValue.set(0.5)
            remapNode.value[2].value_Position.set(0.5)
            remapNode.value[2].value_Interp.set(1)
                                 
        #create shader
        materials = pm.shadingNode('blinn',asShader = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Stretch','MAT'))
        shadingGroup = pm.sets(renderable = 1,noSurfaceShader = 1,empty = 1,name = nameUtils.getUniqueName(self.side,self.baseName + 'Stretch','SG'))
        materials.outColor.connect(shadingGroup.surfaceShader)

        #condition node
        multipleNode.outputX.connect(conditionNode.firstTerm)
        conditionNode.secondTerm.set(1)
        conditionNode.operation.set(2)
        conditionNode.colorIfTrueR.set(0)
        conditionNode.colorIfFalseR.set(0)        
        conditionNode.colorIfTrueG.set(0)
        conditionNode.colorIfFalseG.set(0)
        conditionNode.colorIfTrueB.set(0)
        conditionNode.colorIfFalseB.set(0)
        
        #bug spotted!!!
        stretchSwitchNode.outputR.connect(remapNodeRed.inputValue)
        stretchSwitchNode.outputR.connect(remapNodeGreen.inputValue)
        remapNodeRed.inputMin.set(1)
        remapNodeRed.inputMax.set(2)
        remapNodeRed.outputMin.set(0)
        remapNodeRed.outputMax.set(1)
        remapNodeGreen.inputMin.set(0)
        remapNodeGreen.inputMax.set(1)
        remapNodeGreen.outputMin.set(1)
        remapNodeGreen.outputMax.set(0)   
        remapNodeRed.outValue.connect(conditionNode.colorIfTrueR)   
        remapNodeGreen.outValue.connect(conditionNode.colorIfFalseG)    
#         print materials +  '.incandescenceR = ' + conditionNode + '.outColorR'
#         print materials +  '.incandescenceG = ' + conditionNode + '.outColorG'
#         print materials +  '.incandescenceB = ' + conditionNode + '.outColorB'
        conditionNode.outColor.outColorR.connect(materials.incandescence.incandescenceR)
        conditionNode.outColor.outColorG.connect(materials.incandescence.incandescenceG)
        conditionNode.outColor.outColorB.connect(materials.incandescence.incandescenceB)
        
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
