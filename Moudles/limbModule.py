import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy

class LimbModule(object):
    
#     posLimbArray = [[2,14,-0.2],[4,14,-0.3],[6.15,14,-0.2],[6.4,14,-0.2]]
    
    posLimbArray = [[2,14,-0.2],[4,14,-0.3],[6.15,14,-0.2]]
    rotLimbArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    posShoulderArray = [[0.2,13.95,-0.25],[1.45,14.25,-0.17]]
    rotShoulderArray = [[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'arm',side = 'l',size = 1.5,
                 solver = 'ikRPsolver',controlOrient = [0,0,0]):
        #init
        self.baseName = baseName
        self.side = side
        self.size = size
        self.solver = solver
        self.controlOrient = controlOrient
        
        #jj
        self.fkChain = None
        self.ikChain = None
        self.limbBlendChain = None
        self.shoulderChain = None
        self.shoulderAtChain = None
        self.blendData = None
        self.limbGrp = None
        self.chestGrp = None
            
        #cc
        self.shoulderCtrl = None
        self.handSetting = None
        self.ccDefGrp = None
        self.cntsGrp = None
        self.shoulderBriGrp = None
        
        #guides 
        self.limbGuides = None
        self.shoulderGuides = None
        self.guideGrp = None
        
        #ribbon
        self.ribon = None
        self.ribon45hp = None
        self.subMidCtrlShoulderElbow = None
        self.subMidCtrlElbowWrist = None
        self.subMidCtrlElbow = None
        self.ribbonData = ['ShoulderElbow','EblowWrist','Elbow']
        
        #AT
        self.ikAtHandle = None
        self.ikAtEffector  = None
        
        self.hi = None
         
    def buildGuides(self):
        
        self.hi = hierarchy.Hierarchy(characterName = 'test')
        self.hi.build()
        
        self.limbGuides = []
        self.shoulderGuides = []
        
        #limb Guides
        for num,pos in enumerate(self.posLimbArray):
            name = nameUtils.getUniqueName(self.side,self.baseName,'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(pos)
            loc.r.set(self.rotLimbArray[num])
            self.limbGuides.append(loc)
            
        tempLimbGuides = list(self.limbGuides)
        tempLimbGuides.reverse()
        for i in range(len(tempLimbGuides)):
            if i != (len(tempLimbGuides) - 1):
                pm.parent(tempLimbGuides[i],tempLimbGuides[i + 1])
                
        #shoulder Guides:        
        for num,pos in enumerate(self.posShoulderArray):
            name = nameUtils.getUniqueName(self.side,self.baseName + 'Shoulder','gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(pos)
            loc.r.set(self.rotShoulderArray[num])
            self.shoulderGuides.append(loc)
            
        tempShoulderGuides = list(self.shoulderGuides)
        tempShoulderGuides.reverse()
        for i in range(len(tempShoulderGuides)):
            if i != (len(tempShoulderGuides) - 1):
                pm.parent(tempShoulderGuides[i],tempShoulderGuides[i + 1])  
        
        #clean up
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(self.limbGuides[0],self.shoulderGuides[0],n = name)
                     
               
    def build(self):
        
        #shoulder set
        #shoulder pos get
        self.shoulderGuidePos = [x.getTranslation(space = 'world') for x in self.shoulderGuides]
        self.shoulderGuideRot = [x.getRotation(space = 'world') for x in self.shoulderGuides]
        
        #shoulder jj set
        self.shoulderChain = boneChain.BoneChain(self.baseName + 'Shoulder',self.side,type = 'jj')
        self.shoulderChain.fromList(self.shoulderGuidePos,self.shoulderGuideRot)  
        
        ###########################
        
        #limb set
        #limb pos get
        self.limbGuidePos = [x.getTranslation(space = 'world') for x in self.limbGuides]
        self.limbGuideRot = [x.getRotation(space = 'world') for x in self.limbGuides]      
        
        #addBlendCtrl 
        self.handSetting = control.Control(self.side,self.baseName + 'Settings',self.size) 
        self.handSetting.ikfkBlender()        
        
        #fk first 
        self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkChain.fromList(self.limbGuidePos,self.limbGuideRot,skipLast = 0)
        for chain in self.fkChain.chain:
            pm.setAttr(chain + ".visibility",k = False,cb=False)
            pm.setAttr(chain + ".radi",k = False,cb=False)
        
        #then ik
        self.ikChain = ikChain.IkChain(self.baseName,self.side,self.size,self.solver,type = 'ikRP')
        self.ikChain.fromList(self.limbGuidePos,self.limbGuideRot)
        
        #ik cc connect ori
        self.ikChain.ikCtrl.control.rx.connect(self.ikChain.chain[-1].rx)
        self.ikChain.ikCtrl.control.ry.connect(self.ikChain.chain[-1].ry)
        self.ikChain.ikCtrl.control.rz.connect(self.ikChain.chain[-1].rz)
        
        #set cc
        pm.addAttr(self.handSetting.control,ln = '__',at = 'enum',en = 'ArmCtrl:')
        pm.setAttr(self.handSetting.control + '.__',k = 1,l = 1)
        
        #ori                
        self.limbBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.limbBlendChain.fromList(self.limbGuidePos,self.limbGuideRot)
        
        self.blendData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikChain.chain,self.limbBlendChain.chain,
                                                            self.handSetting.control,'IKFK',self.baseName,self.side)
        
        self.__ikfkBlender()
        self.__setRibbonUpper()
        self.__setRibbonLower()
        self.__setRibbonSubMidCc()
        self.__shoulderCtrl()
        self.__cleanUp()
        
    def __ikfkBlender(self):
        
        #connect visable function 
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'IKFK','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
        
        #connect node
        self.handSetting.control.IKFK.connect(self.ikChain.ikCtrl.controlGrp.v)
        self.handSetting.control.IKFK.connect(self.ikChain.poleVectorCtrl.controlGrp.v)
        self.handSetting.control.IKFK.connect(self.handSetting.textObj[2].v)
        self.handSetting.control.IKFK.connect(reverseNode.inputX)
        reverseNode.outputX.connect(self.fkChain.chain[0].v)
        reverseNode.outputX.connect(self.handSetting.textObj[0].v)             
        
        #set pos
        scaleValue = 1 * self.ikChain.length/16
        size = 1.5 * self.ikChain.length / 16
        pm.xform(self.handSetting.controlGrp,ws = 1,matrix = self.limbBlendChain.chain[2].worldMatrix.get())
        self.handSetting.controlGrp.rx.set(0)
        self.handSetting.controlGrp.ry.set(0)
        self.handSetting.controlGrp.rz.set(0)
        self.handSetting.controlGrp.sx.set(scaleValue)
        self.handSetting.controlGrp.sy.set(scaleValue)
        self.handSetting.controlGrp.sz.set(scaleValue)
        pm.move(self.limbGuidePos[2][0],self.limbGuidePos[2][1] + 2 * size,self.limbGuidePos[2][2],self.handSetting.controlGrp)
        wrist_pos = pm.xform(self.limbBlendChain.chain[2],query=1,ws=1,rp=1)
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.handSetting.controlGrp + '.rotatePivot')
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.handSetting.controlGrp + '.scalePivot')
        pm.pointConstraint(self.limbBlendChain.chain[2],self.handSetting.controlGrp,mo = 1)
#         pm.orientConstraint(self.limbBlendChain.chain[2],self.handSetting.controlGrp,mo = 1)   
        control.lockAndHideAttr(self.handSetting.control,['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])     
    
    def __setRibbonUpper(self):
        '''
        this function set ribbon for the Upper 
        '''
        self.ribon = ribbon.Ribbon(RibbonName = self.ribbonData[0],Width = 1.0,Length = 5.0,UVal = 1,VVal = 5,subMid = 1,side = self.side,baseName=self.baseName + self.ribbonData[0])
        self.ribon.construction()

        pm.xform(self.ribon.startLoc,ws = 1,matrix = self.limbBlendChain.chain[0].worldMatrix.get())
        pm.xform(self.ribon.endLoc,ws = 1,matrix = self.limbBlendChain.chain[1].worldMatrix.get())
        
        pm.parentConstraint(self.limbBlendChain.chain[0],self.ribon.startLoc,mo = 1)
        pm.parentConstraint(self.limbBlendChain.chain[0],self.limbBlendChain.chain[1],self.ribon.epUploc,mo = 1)
        
        self.__subCtrlUpper()
        
    def __subCtrlUpper(self):

        #connect scale for ShoulderElbow jj2
        self.subMidCtrlShoulderElbow = self.ribon.subMidCtrl
        self.subMidCtrlShoulderElbow.control.scaleX.connect(self.ribon.jj[2].scaleX)
        self.subMidCtrlShoulderElbow.control.scaleY.connect(self.ribon.jj[2].scaleY)
        self.subMidCtrlShoulderElbow.control.scaleZ.connect(self.ribon.jj[2].scaleZ)

    def __setRibbonLower(self):
        '''
        this function set ribbon for the ShoulderElbow 
        '''
        
        self.ribon45hp = ribbon.Ribbon(RibbonName = self.ribbonData[1],Width = 1.0,Length = 5.0,UVal = 1,VVal = 5,subMid = 1,side = self.side,baseName=self.baseName + self.ribbonData[1])
        self.ribon45hp.construction()

        pm.xform(self.ribon45hp.startLoc,ws = 1,matrix = self.limbBlendChain.chain[1].worldMatrix.get())
        pm.xform(self.ribon45hp.endLoc,ws = 1,matrix = self.limbBlendChain.chain[2].worldMatrix.get())
        
        pm.parentConstraint(self.limbBlendChain.chain[2],self.ribon45hp.endLoc,mo = 1)
        
        self.__subCtrlLower()
          
    def __subCtrlLower(self):

        #connect scale for mid jj
        self.subMidCtrlElbowWrist = self.ribon45hp.subMidCtrl
        self.subMidCtrlElbowWrist.control.scaleX.connect(self.ribon45hp.jj[2].scaleX)
        self.subMidCtrlElbowWrist.control.scaleY.connect(self.ribon45hp.jj[2].scaleY)
        self.subMidCtrlElbowWrist.control.scaleZ.connect(self.ribon45hp.jj[2].scaleZ)
        
    def __setRibbonSubMidCc(self):
        
        self.subMidCtrlElbow = control.Control(size = 1,baseName = self.ribbonData[2] + '_CC',side = self.side) 
        self.subMidCtrlElbow.circleCtrl()
        elbolPos = pm.xform(self.limbBlendChain.chain[1],query=1,ws=1,rp=1)
        pm.move(self.subMidCtrlElbow.controlGrp,elbolPos[0],elbolPos[1],elbolPos[2],a=True)
        
        pm.parentConstraint(self.subMidCtrlElbow.control,self.ribon45hp.startLoc,mo = 1)
        pm.parentConstraint(self.subMidCtrlElbow.control,self.ribon.endLoc,mo = 1)
        pm.parentConstraint(self.limbBlendChain.chain[1],self.subMidCtrlElbow.controlGrp,mo = 1)
        
        #name setting for the scale node for shoulderElbow Jj1
        shoulderElbowScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'shoulderElbowScaleJj1','PMA')
        
        #create Node for  shoulderElbow Jj1
        #ribbon name for robin
        shoulderElbowScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = shoulderElbowScaleNodeNameJj1)
        
        #connect shoulderElbow scale for  shoulderElbow Jj1
        self.subMidCtrlShoulderElbow.control.scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlElbow.control.scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlShoulderElbow.control.scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlElbow.control.scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlShoulderElbow.control.scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlElbow.control.scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        shoulderElbowScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to shoulderElbow Jj1
        shoulderElbowScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon.jj[1].scaleX)
        shoulderElbowScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon.jj[1].scaleY)
        shoulderElbowScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon.jj[1].scaleZ)
        
        #name setting for the scale node for shoulderElbow Jj3
        shoulderElbowScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'shoulderElbowScaleJj3','PMA')
        
        #create Node for  shoulderElbow Jj3
        shoulderElbowScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = shoulderElbowScaleNodeNameJj3)
           
        #connect shoulderElbow scale for  shoulderElbow Jj3
        
        self.subMidCtrlShoulderElbow.control.scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.limbBlendChain.chain[1].scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlShoulderElbow.control.scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.limbBlendChain.chain[1].scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlShoulderElbow.control.scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.limbBlendChain.chain[1].scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        shoulderElbowScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to shoulderElbow Jj3
        shoulderElbowScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon.jj[3].scaleX)
        shoulderElbowScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon.jj[3].scaleY)
        shoulderElbowScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon.jj[3].scaleZ)
        
        #connect scale to shoulderElbow jj0
        self.subMidCtrlElbow.control.scaleX.connect(self.ribon.jj[0].scaleX)
        self.subMidCtrlElbow.control.scaleY.connect(self.ribon.jj[0].scaleY)
        self.subMidCtrlElbow.control.scaleZ.connect(self.ribon.jj[0].scaleZ)
        
        #connect scale to shoulderElbow jj4
        self.limbBlendChain.chain[0].scaleX.connect(self.ribon.jj[4].scaleX)
        self.limbBlendChain.chain[0].scaleY.connect(self.ribon.jj[4].scaleY)
        self.limbBlendChain.chain[0].scaleZ.connect(self.ribon.jj[4].scaleZ)
        
        
        
        #name setting for the scale node for elbowWrist Jj1
        elbowWristScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'elbowWristScaleJj1','PMA')
        
        #create Node for  elbowWrist jj1
        elbowWristScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = elbowWristScaleNodeNameJj1)
               
        #connect elbowWrist scale for elbowWrist jj1
        self.subMidCtrlElbowWrist.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlElbow.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlElbowWrist.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlElbow.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlElbowWrist.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlElbow.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        elbowWristScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to elbowWrist jj1
        elbowWristScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon45hp.jj[1].scaleX)
        elbowWristScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon45hp.jj[1].scaleY)
        elbowWristScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon45hp.jj[1].scaleZ)
        
        #name setting for the scale node for elbowWrist Jj3
        elbowWristScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'elbowWristScaleJj3','PMA')
        
        #create Node for  elbowWrist jj3
        elbowWristScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = elbowWristScaleNodeNameJj3)
               
        #connect elbowWrist scale for elbowWrist jj3
        self.subMidCtrlElbowWrist.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.subMidCtrlElbow.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlElbowWrist.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.subMidCtrlElbow.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlElbowWrist.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.subMidCtrlElbow.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        elbowWristScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to elbowWrist jj3
        elbowWristScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon45hp.jj[3].scaleX)
        elbowWristScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon45hp.jj[3].scaleY)
        elbowWristScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon45hp.jj[3].scaleZ)
        
        #connect scale to elbowWrist jj4
        self.subMidCtrlElbow.control.scaleX.connect(self.ribon45hp.jj[4].scaleX)
        self.subMidCtrlElbow.control.scaleY.connect(self.ribon45hp.jj[4].scaleY)
        self.subMidCtrlElbow.control.scaleZ.connect(self.ribon45hp.jj[4].scaleZ)
        
        #connect scale to elbowWrist jj0
        self.limbBlendChain.chain[2].scaleX.connect(self.ribon45hp.jj[0].scaleX)
        self.limbBlendChain.chain[2].scaleY.connect(self.ribon45hp.jj[0].scaleY)
        self.limbBlendChain.chain[2].scaleZ.connect(self.ribon45hp.jj[0].scaleZ)
            
    def __shoulderCtrl(self):
        
        #add Ctrl 
        self.shoulderCtrl = control.Control(self.side,self.baseName + 'Shoulder',self.size) 
        self.shoulderCtrl.shoulderCtrl(axis = 'y') 
        
        #align
        posArray = self.shoulderChain.chain[0]
        pm.xform(self.shoulderCtrl.controlGrp,ws = 1,matrix = posArray.worldMatrix.get())
        pm.setAttr(self.shoulderCtrl.controlGrp + '.tz',-self.shoulderChain.chain[1].tx.get())
        control.lockAndHideAttr(self.shoulderCtrl.control,['sx','sy','sz','rx','v'])
        
        #clean
        self.shoulderChain.chain[0].setParent(self.shoulderCtrl.control)
        
        #AT shoulder
        #add attr
        control.addFloatAttr(self.shoulderCtrl.control,['follow_ik'],0,1)
        
        #create AT joint 
        self.shoulderAtChain = boneChain.BoneChain(self.baseName + 'AtSd',self.side,type = 'jc')
        self.shoulderAtChain.fromList(self.limbGuidePos,self.limbGuideRot)
        
        #create ikHandle:
        atIkName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','iks')
        self.ikAtHandle,self.ikAtEffector = pm.ikHandle(sj = self.shoulderAtChain.chain[0],
                                                    ee = self.shoulderAtChain.chain[2],solver = self.solver,n = atIkName)
        self.ikAtHandle.setParent(self.ikChain.ikCtrl.control)
        pm.poleVectorConstraint(self.ikChain.poleVectorCtrl.control,atIkName,w = 1)
        self.ikAtHandle.v.set(0)
        
        #connect to the shoulder
        #node name
        remapColorNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','RC')
        multipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','MDN')
        
        #create node
        remapColorNode = pm.createNode('remapColor',n = remapColorNodeName)
        multipleNode = pm.createNode('multiplyDivide',n = multipleNodeName)
        
        #parpare to connect
        self.shoulderBriGrp = pm.group(self.shoulderCtrl.control,
                                       n = nameUtils.getUniqueName(self.side,self.baseName + 'BriAtSd','grp'))
        briPos = self.shoulderChain.chain[0].getTranslation(space = 'world')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBriGrp + '.rotatePivot')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBriGrp + '.scalePivot')
        self.shoulderBriGrp.setParent(self.shoulderCtrl.controlGrp)        
        
        #connect
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2X)
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2Y)
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2Z)
        
        self.shoulderAtChain.chain[0].rx.connect(multipleNode.input1X)
        multipleNode.outputX.connect(remapColorNode.colorR)
        self.shoulderAtChain.chain[0].ry.connect(multipleNode.input1Y)
        multipleNode.outputY.connect(remapColorNode.colorG)
        self.shoulderAtChain.chain[0].rz.connect(multipleNode.input1Z)
        multipleNode.outputZ.connect(remapColorNode.colorB)
        
        remapColorNode.outColor.outColorG.connect(self.shoulderBriGrp.ry)
        remapColorNode.outColor.outColorB.connect(self.shoulderBriGrp.rz)
        
        remapColorNode.inputMin.set(-90)
        remapColorNode.inputMax.set(90)
        remapColorNode.outputMin.set(-45)
        remapColorNode.outputMax.set(45)
        
        remapColorNode.green[0].green_FloatValue.set(0.25)
        remapColorNode.green[0].green_Position.set(0)
        remapColorNode.green[1].green_FloatValue.set(0.6)
        remapColorNode.green[1].green_Position.set(1)        
        remapColorNode.green[2].green_FloatValue.set(0.5)
        remapColorNode.green[2].green_Position.set(0.5)
        remapColorNode.green[2].green_Interp.set(1)
        
        remapColorNode.blue[0].blue_FloatValue.set(0.15)
        remapColorNode.blue[0].blue_Position.set(0)
        remapColorNode.blue[1].blue_FloatValue.set(0.6)
        remapColorNode.blue[1].blue_Position.set(1)        
        remapColorNode.blue[2].blue_FloatValue.set(0.5)
        remapColorNode.blue[2].blue_Position.set(0.5)
        remapColorNode.blue[2].blue_Interp.set(1)  
        remapColorNode.blue[3].blue_FloatValue.set(0.3)
        remapColorNode.blue[3].blue_Position.set(0.25)      
        remapColorNode.blue[3].blue_Interp.set(1)   
      
    def __cleanUp(self):
        
        #add cc ctrl
        control.addFloatAttr(self.handSetting.control,['CC'],0,1) 
        
        #ccDef grp and v
        self.ccDefGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Def','grp')) 
        self.subMidCtrlShoulderElbow.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlElbowWrist.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlElbow.controlGrp.setParent(self.ccDefGrp)
        self.handSetting.control.CC.set(0)
        self.handSetting.control.CC.connect(self.ccDefGrp.v)
        
        #cc hierarchy        
        self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
                                n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))
        

        self.ccDefGrp.setParent(self.cntsGrp)
        self.cntsGrp.setParent(self.hi.CC) 
        self.handSetting.controlGrp.setParent(self.cntsGrp)    
                
        if self.solver == 'ikRPsolver':
            pm.parent(self.ikChain.poleVectorCtrl.controlGrp,self.cntsGrp)        
        
        #ribbon hierarchy   
        self.ribon.main.setParent(self.hi.XTR)
        self.ribon45hp.main.setParent(self.hi.XTR)
        self.ribon.main.v.set(0)
        self.ribon45hp.main.v.set(0)
        
        #ik stretch loc vis
        self.ikChain.stretchStartLoc.setParent(self.hi.SKL)
        self.ikChain.stretchStartLoc.v.set(0)
        self.ikChain.lockUpStartLoc.setParent(self.hi.SKL)
        self.ikChain.lockUpStartLoc.v.set(0)
        self.ikChain.ikHandle.setParent(self.hi.IK)
        
        #guide grp
        self.guideGrp.setParent(self.hi.GUD)
        self.hi.GUD.v.set(0)

        #jj grp
        self.limbGrp = pm.group(self.ikChain.lockUpStartLoc,self.ikChain.stretchStartLoc,
                               n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))
        
        armInitial =  self.limbBlendChain.chain[0].getTranslation(space = 'world')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.limbGrp + '.rotatePivot')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.limbGrp + '.scalePivot')
        
        for b in (self.ikChain,self.fkChain,self.limbBlendChain):
            b.chain[0].setParent(self.limbGrp)
            
        self.limbGrp.setParent(self.shoulderCtrl.control)
        
        #chest clean 
        self.chestGrp = pm.group(self.shoulderCtrl.controlGrp,n = nameUtils.getUniqueName('m','chest','grp'))
        self.chestGrp.setParent(self.hi.SKL)
        self.shoulderAtChain.chain[0].setParent(self.chestGrp)
        
#         for b in (self.ikChain,self.fkChain,self.limbBlendChain):
#             b.chain[0].setParent(self.bonesGrp)
#          
#         self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))
#              
#         self.mainGrp = pm.group(self.bonesGrp,self.cntsGrp,self.handSetting,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))   
         


# from Modules import limbModule
# lm = limbModule.LimbModule()
# lm.buildGuides()
# lm.build()
