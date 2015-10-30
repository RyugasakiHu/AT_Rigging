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
        self.folGrp = None
        
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
        self.__squashStretch()
        self.__combine()
        
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
        #bend
        pm.addAttr(self.config_node.control,ln = '______',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '.______',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['bend_up','bend_mid','bend_lo'],-3600,3600)

        pm.addAttr(self.config_node.control,ln = '_______',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '._______',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['bend_up_rev','bend_mid_rev','bend_lo_rev'],-3600,3600)
        
        #side
        pm.addAttr(self.config_node.control,ln = '__________',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '.__________',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['side_up','side_mid','side_lo'],-3600,3600)

        pm.addAttr(self.config_node.control,ln = '___________',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '.___________',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['side_up_rev','side_mid_rev','side_lo_rev'],-3600,3600)               
        
        #twist
        pm.addAttr(self.config_node.control,ln = '________',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '.________',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['twist_up','twist_mid','twist_lo'],-3600,3600)

        pm.addAttr(self.config_node.control,ln = '_________',at = 'enum',en = '0')
        pm.setAttr(self.config_node.control + '._________',e = 1,channelBox = 1)
        control.addFloatAttr(self.config_node.control,
                             ['twist_up_rev','twist_mid_rev','twist_lo_rev'],-3600,3600)                 
        
    def __fkJj(self):
        
        #create fk jj
        self.spineFkRevBlendChain = []        
        self.guideSpineFkPos = [x.getTranslation(space = 'world') for x in self.fkGuides]
        self.guideSpineFkRot = [x.getRotation(space = 'world') for x in self.fkGuides]
        
        self.spineFkBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'fk')
        self.spineFkBlendChain.fromList(self.guideSpineFkPos,self.guideSpineFkRot,autoOrient = 1)
        
        #create revFk MDN node
        fkMultipleNodeList = []
        fkPlusMinusAverageList = []
        for num,fkJj in enumerate(self.spineFkBlendChain.chain):
            fkMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'Fk','MDN')
            fkMultipleNode = pm.createNode('multiplyDivide',n = fkMultipleNodeName)
            fkMultipleNodeList.append(fkMultipleNode)
            
            fkPlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'Fk','PMA')
            fkPlusMinusAverageNode = pm.createNode('plusMinusAverage',n = fkPlusMinusAverageNodeName)
            fkPlusMinusAverageNode.operation.set(1)
            fkPlusMinusAverageList.append(fkPlusMinusAverageNode)         

            fkJj.rx.connect(fkMultipleNode.input1X)
            fkJj.ry.connect(fkMultipleNode.input1Y)
            fkJj.rz.connect(fkMultipleNode.input1Z)
            
            fkMultipleNode.input2X.set(-1)
            fkMultipleNode.input2Y.set(-1)
            fkMultipleNode.input2Z.set(-1)
            
            fkMultipleNode.outputX.connect(fkPlusMinusAverageNode.input3D[0].input3Dx)
            fkMultipleNode.outputY.connect(fkPlusMinusAverageNode.input3D[0].input3Dy)
            fkMultipleNode.outputZ.connect(fkPlusMinusAverageNode.input3D[0].input3Dz)
                
        #clean up
        self.spineFkGrp = pm.group(self.spineFkBlendChain.chain[0],
                                   n = nameUtils.getUniqueName(self.side,self.baseName + 'Fk','grp'))
        
        self.spineFkGrp.setParent(self.config_node.control)
        
        #create revFk
        self.guideSpineRevFkPos = [x.getTranslation(space = 'world') for x in self.fkGuides]
        self.guideSpineRevFkRot = [x.getRotation(space = 'world') for x in self.fkGuides]
 
        self.spineFkRevBlendChain = boneChain.BoneChain(self.baseName + 'Rev',self.side,type = 'fk')
        self.spineFkRevBlendChain.fromList(self.guideSpineRevFkPos,self.guideSpineRevFkRot,autoOrient = 1)  
        
        #reroot skl
        pm.select(self.spineFkRevBlendChain.chain[-1])
        pm.runtime.RerootSkeleton()     
        self.spineFkRevBlendChain.chain[-1].setParent(self.spineFkBlendChain.chain[-1])

        #set Rotate
        #nodename
        multiplefkBendNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkBend','MDN')
        multiplefkRevBendNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkRevBend','MDN')
        multiplefkTwistNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkTwist','MDN')
        multiplefkRevTwistNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkRevTwist','MDN')
        multiplefkSideNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkSide','MDN')
        multiplefkRevSideNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'FkRevSide','MDN')                
          
        #nodecreate
        multiplefkBendNode = pm.createNode('multiplyDivide',n = multiplefkBendNodeName)
        multiplefkRevBendNode = pm.createNode('multiplyDivide',n = multiplefkRevBendNodeName)
        multiplefkTwistNode = pm.createNode('multiplyDivide',n = multiplefkTwistNodeName)
        multiplefkRevTwistNode = pm.createNode('multiplyDivide',n = multiplefkRevTwistNodeName)
        multiplefkSideNode = pm.createNode('multiplyDivide',n = multiplefkSideNodeName)
        multiplefkRevSideNode = pm.createNode('multiplyDivide',n = multiplefkRevSideNodeName)        
         
        #connect
        #bend
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
         
        #twist
        self.config_node.control.twist_lo.connect(multiplefkTwistNode.input1X)
        self.config_node.control.twist_mid.connect(multiplefkTwistNode.input1Y)
        self.config_node.control.twist_up.connect(multiplefkTwistNode.input1Z)
        self.config_node.control.twist_lo_rev.connect(multiplefkRevTwistNode.input1X)
        self.config_node.control.twist_mid_rev.connect(multiplefkRevTwistNode.input1Y)
        self.config_node.control.twist_up_rev.connect(multiplefkRevTwistNode.input1Z)
         
        multiplefkTwistNode.input2X.set(-1)
        multiplefkTwistNode.input2Y.set(-1)
        multiplefkTwistNode.input2Z.set(-1)
        multiplefkTwistNode.operation.set(1)
         
        multiplefkRevTwistNode.input2X.set(-1)
        multiplefkRevTwistNode.input2Y.set(-1)
        multiplefkRevTwistNode.input2Z.set(-1)
        multiplefkRevTwistNode.operation.set(1)        
         
        #side
        self.config_node.control.side_lo.connect(multiplefkSideNode.input1X)
        self.config_node.control.side_mid.connect(multiplefkSideNode.input1Y)
        self.config_node.control.side_up.connect(multiplefkSideNode.input1Z)
        self.config_node.control.side_lo_rev.connect(multiplefkRevSideNode.input1X)
        self.config_node.control.side_mid_rev.connect(multiplefkRevSideNode.input1Y)
        self.config_node.control.side_up_rev.connect(multiplefkRevSideNode.input1Z)
         
        multiplefkSideNode.input2X.set(-1)
        multiplefkSideNode.input2Y.set(-1)
        multiplefkSideNode.input2Z.set(-1)
        multiplefkSideNode.operation.set(1)
         
        multiplefkRevSideNode.input2X.set(-1)
        multiplefkRevSideNode.input2Y.set(-1)
        multiplefkRevSideNode.input2Z.set(-1)
        multiplefkRevSideNode.operation.set(1)                     
         
        #fk
        for num,chain in enumerate(self.spineFkBlendChain.chain):
            #lo
            if 1 <= num <= (self.segment / 3):
                multiplefkBendNode.outputX.connect(chain.rz)
                multiplefkSideNode.outputX.connect(chain.ry)
                multiplefkTwistNode.outputX.connect(chain.rx)
            #mid    
            elif (self.segment / 3) < num < ((self.segment / 3) * 2):
                multiplefkBendNode.outputY.connect(chain.rz)
                multiplefkSideNode.outputY.connect(chain.ry)
                multiplefkTwistNode.outputY.connect(chain.rx)
            #up    
            elif ((self.segment / 3) * 2) <= num < (self.segment - 1):
                multiplefkBendNode.outputZ.connect(chain.rz)
                multiplefkSideNode.outputZ.connect(chain.ry)
                multiplefkTwistNode.outputZ.connect(chain.rx)
            
        #revFk        
#         self.spineFkRevBlendChain.chain.reverse()
        for num,chain in enumerate(self.spineFkRevBlendChain.chain):
            #lo
            if 1 <= num <= (self.segment / 3 - 1):
                multiplefkRevBendNode.outputX.connect(fkPlusMinusAverageList[num].input3D[1].input3Dz)
                multiplefkRevSideNode.outputX.connect(fkPlusMinusAverageList[num].input3D[1].input3Dy)
                multiplefkRevTwistNode.outputX.connect(fkPlusMinusAverageList[num].input3D[1].input3Dx)
                 
                fkPlusMinusAverageList[num].output3D.output3Dz.connect(chain.rz)
                fkPlusMinusAverageList[num].output3D.output3Dy.connect(chain.ry)
                fkPlusMinusAverageList[num].output3D.output3Dx.connect(chain.rx)
                 
            #mid              
            elif (self.segment / 3 - 1) < num < ((self.segment / 3) * 2):
                multiplefkRevBendNode.outputY.connect(fkPlusMinusAverageList[num].input3D[1].input3Dz)
                multiplefkRevSideNode.outputY.connect(fkPlusMinusAverageList[num].input3D[1].input3Dy)
                multiplefkRevTwistNode.outputY.connect(fkPlusMinusAverageList[num].input3D[1].input3Dx)
                 
                fkPlusMinusAverageList[num].output3D.output3Dz.connect(chain.rz)
                fkPlusMinusAverageList[num].output3D.output3Dy.connect(chain.ry)
                fkPlusMinusAverageList[num].output3D.output3Dx.connect(chain.rx)
                 
            #up    
            elif ((self.segment / 3) * 2) <= num < (self.segment - 1):
                multiplefkRevBendNode.outputZ.connect(fkPlusMinusAverageList[num].input3D[1].input3Dz)
                multiplefkRevSideNode.outputZ.connect(fkPlusMinusAverageList[num].input3D[1].input3Dy)
                multiplefkRevTwistNode.outputZ.connect(fkPlusMinusAverageList[num].input3D[1].input3Dx)
                 
                fkPlusMinusAverageList[num].output3D.output3Dz.connect(chain.rz)     
                fkPlusMinusAverageList[num].output3D.output3Dy.connect(chain.ry)
                fkPlusMinusAverageList[num].output3D.output3Dx.connect(chain.rx)
                 
    def __ikJj(self):    
        
        #create IKRibbonSpine
        #ribbon spine info:
        curveInfo = [0,(self.segment - 1) / 4,(self.segment - 1) / 2,
                     ((self.segment - 1) / 2 + (self.segment - 1)) / 2,
                     (self.segment - 1)]
        ribbonCurve = []
        self.folList = []
        
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
        ribbonGeo = pm.loft(ribbonCurveR,ribbonCurveL,ch = 0,u = 1,c = 0,ar = 1,d = 3,ss = 1, rn = 0,po = 0,rsn = 1,
                             n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbon','surf'))
        
        ribbonClusList = []
        self.ribbonJc = []
        self.spineCc = []
        
        #get Jc pos
        for num in [0,2,4]:
            pos = pm.select(ribbonGeo[0] + '.cv[' + str(num) + '][0:3]',r = 1)
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
            cc = control.Control(self.side,self.baseName + self.nameList[num],size = self.length / 3)
            print self.length / 2 
            cc.circleCtrl()
            self.spineCc.append(cc.control)
            pm.xform(cc.controlGrp,ws = 1,matrix = jc.worldMatrix.get())
            pm.setAttr(cc.controlGrp + '.rz',90)
        
        #skin Jc
        for num,jc in enumerate(self.ribbonJc):
            jc.setParent(self.spineCc[num])

        pm.skinCluster(self.ribbonJc[0],self.ribbonJc[1],self.ribbonJc[2],ribbonGeo[0],
                       tsb = 1,ih = 1,mi = 3,dr = 4,rui = 1)
        
        #set fol
        #create / rename fol
        
        self.folGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Fol','grp')) 
        
        for fol in range(self.segment):
            
            #createNodeName
            follicleTransName = nameUtils.getUniqueName(self.side,self.baseName,'fol')
            follicleShapeName = nameUtils.getUniqueName(self.side,self.baseName,'folShape')
            
            #createNode
            follicleShape = pm.createNode('follicle',n = follicleShapeName)
            follicleTrans = pm.listRelatives(follicleShape, parent=True)[0]
            follicleTrans = pm.rename(follicleTrans, follicleTransName)
            
            # connect the surface to the follicle
            
            if ribbonGeo[0].getShape().nodeType() == 'nurbsSurface':
                pm.connectAttr((ribbonGeo[0] + '.local'), (follicleShape + '.inputSurface'))
                
            #Connect the worldMatrix of the surface into the follicleShape
            pm.connectAttr((ribbonGeo[0] + '.worldMatrix[0]'), (follicleShape + '.inputWorldMatrix'))
            
            #Connect the follicleShape to it's transform
            pm.connectAttr((follicleShape + '.outRotate'), (follicleTrans + '.rotate'))
            pm.connectAttr((follicleShape + '.outTranslate'), (follicleTrans + '.translate'))
            
            #Set the uValue and vValue for the current follicle
            pm.setAttr((follicleShape + '.parameterV'), 0.5)
            pm.setAttr((follicleShape + '.parameterU'), float(1.0 / self.segment) * fol + (1.0 / (self.segment * 2)))
            
            #Lock the translate/rotate of the follicle
            pm.setAttr((follicleTrans + '.translate'), lock=True)
            pm.setAttr((follicleTrans + '.rotate'), lock=True)
            
            #parent
            self.folList.append(follicleTrans)
            follicleTrans.setParent(self.folGrp)
        
        #rebuild fol pos
        self.spineIkBlendJoint = []
        self.stretchCube = []
        for num,fol in enumerate(self.folList):
            jj = pm.joint(p = (0,0,0),n = nameUtils.getUniqueName(self.side,self.baseName,'jj'),
                          radius = self.length / 5)
            self.spineIkBlendJoint.append(jj)
            jj.setParent(fol)
            tempCube = pm.polyCube(ch = 1,o = 1,w = float(self.length / 5),h = float(self.length / 10),
                                   d = float(self.length / 5),cuv = 4,n = nameUtils.getUniqueName(self.side,self.baseName,'cube'))
            tempCube[0].setParent(jj)
            tempCube[0].v.set(0)
            self.stretchCube.append(tempCube[0])
            jj.translateX.set(0)
            jj.translateY.set(0)
            jj.translateZ.set(0)
            
        #create spine grp
        self.spineIkGrp = pm.group(self.spineCc[0].getParent(),self.spineCc[1].getParent(),self.spineCc[2].getParent(),self.folGrp,ribbonGeo[0],
                                   n = nameUtils.getUniqueName(self.side,self.baseName + 'Ik','grp'))
        ribbonGeo[0].inheritsTransform.set(0)
        self.folGrp.inheritsTransform.set(0)
        
        #clean
        self.spineIkGrp.setParent(self.config_node.control)
        
        #temp
        self.spineIkGrp.v.set(1)
        
        '''put chest ctrl under chest cc'''
        '''put leg under hip cc'''
        
    def __squashStretch(self):
        
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
        '''
        color cannot change interactively
        '''
        
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

    def __combine(self):
        
        hip = self.spineCc[0].getParent()
        mid = self.spineCc[1].getParent()
        chest = self.spineCc[2].getParent()
        
        hip.setParent(self.spineFkRevBlendChain.chain[-1])
        chest.setParent(self.spineFkRevBlendChain.chain[0])
        mid.setParent(self.spineFkRevBlendChain.chain[(self.segment - 1) / 2])
        
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

