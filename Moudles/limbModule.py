import pymel.core as pm
import math 
from Modules.subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils,hookUtils,metaUtils
from Modules import control
from maya import OpenMaya

class LimbModule(object):
    
#     posLimbArray = [[2,14,-0.2],[4,14,-0.3],[6.15,14,-0.2],[6.4,14,-0.2]]
    
    posLimbArray = [[2,14,-0.2],[4,14,-0.3],[6.15,14,-0.2]]
    rotLimbArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    posShoulderArray = [[0.2,13.95,-0.25],[1.45,14.25,-0.17]]
    rotShoulderArray = [[0,0,0],[0,0,0]]
    posShoulderBladeArray = [[0.65,14,-0.6],[0.65,12.5,-0.6]]
    rotShoulderBladeArray = [[0,0,0],[0,0,0]]    
    
    def __init__(self,baseName = 'arm',side = 'l',size = 1.5,
                 solver = 'ikRPsolver',controlOrient = [0,0,0],
                 metaSpine = None,metaMain = None,mirror = None):
        #init
        self.baseName = baseName
        self.side = side
        self.size = size
        self.solver = solver
        self.controlOrient = controlOrient
        self.mirror = mirror
        
        #jj
        self.fkChain = None
        self.ikChain = None
        self.limbBlendChain = None
        self.shoulderChain = None
        self.shoulderAtChain = None
        self.shoulderBladeChain = None
        self.blendData = None
        self.limbGrp = None
        self.chestGrp = None
        self.shoulderBladeGrp = None
        self.upperJointLentgh = None
        self.lowerJointLentgh = None
            
        #cc
        self.distance = None
        self.shoulderCtrl = None
        self.handSettingCtrl = None
        self.ccDefGrp = None
        self.cntsGrp = None
        self.shoulderBriGrp = None
        
        #guides 
        self.limbGuides = None
        self.shoulderGuides = None
        self.shoulderBladeGuides = None
        self.totalGuides = None
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
        self.poseReadorGrp = None
        
        #Hook
        self.__tempSpaceSwitch = None
        self.locLocal = None
        self.locWorld = None
        self.hookData = {}

        #metanode
        self.meta = metaUtils.createMeta(self.side,self.baseName,0)
        self.metaMain = metaMain
        self.metaSpine = metaSpine
         
    def buildGuides(self):
        
        self.limbGuides = []
        self.shoulderGuides = []
        self.shoulderBladeGuides = []
        self.totalGuides = []
        
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
                
        #shoulder Blade
        for num,pos in enumerate(self.posShoulderBladeArray):
            name = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade','gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(pos)
            loc.r.set(self.rotShoulderBladeArray[num])
            self.shoulderBladeGuides.append(loc)
             
        tempShoulderBladeGuides = list(self.shoulderBladeGuides)
        tempShoulderBladeGuides.reverse()
        for i in range(len(tempShoulderBladeGuides)):
            if i != (len(tempShoulderBladeGuides) - 1):
                pm.parent(tempShoulderBladeGuides[i],tempShoulderBladeGuides[i + 1])
                
        #perpare for the mirror
        
        for guides in self.limbGuides + self.shoulderGuides + self.shoulderBladeGuides:
            self.totalGuides.append(guides)
        
        #clean up
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(em = 1,n = name)
        self.limbGuides[0].setParent(self.guideGrp)
        self.shoulderGuides[0].setParent(self.guideGrp)
        self.shoulderBladeGuides[0].setParent(self.guideGrp)
                     
    def build(self):
        
        self.guideGrp.v.set(0)
        #shoulder set
        #shoulder pos get
        self.shoulderGuidePos = [x.getTranslation(space = 'world') for x in self.shoulderGuides]
        self.shoulderGuideRot = [x.getRotation(space = 'world') for x in self.shoulderGuides]
        
        #shoulder jj set
        self.shoulderChain = boneChain.BoneChain(self.baseName + 'Shoulder',self.side,type = 'jj')
        self.shoulderChain.fromList(self.shoulderGuidePos,self.shoulderGuideRot)
        pm.rename(self.shoulderChain.chain[-1],nameUtils.getUniqueName(self.side,self.baseName + 'Shoulder','je'))
        
        ###########################
        #shoulder Blade set
        #shoulder Blade pos get
        self.shoulderBladeGuidePos = [x.getTranslation(space = 'world') for x in self.shoulderBladeGuides]
        self.shoulderBladeGuideRot = [x.getRotation(space = 'world') for x in self.shoulderBladeGuides]
        
        #shoulder jj set
        self.shoulderBladeChain = boneChain.BoneChain(self.baseName + 'ShoulderBlade',self.side,type = 'jj')
        self.shoulderBladeChain.fromList(self.shoulderBladeGuidePos,self.shoulderBladeGuideRot)
        pm.rename(self.shoulderBladeChain.chain[-1],nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade','je'))
        
        
        ###########################
        
        #limb set
        #limb pos get
        self.limbGuidePos = [x.getTranslation(space = 'world') for x in self.limbGuides]
        self.limbGuideRot = [x.getRotation(space = 'world') for x in self.limbGuides]      
        
        #addBlendCtrl 
        self.handSettingCtrl = control.Control(self.side,self.baseName + 'Settings',self.size) 
        self.handSettingCtrl.ikfkBlender()        
        
        #fk first 
        self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkChain.fromList(self.limbGuidePos,self.limbGuideRot,skipLast = 0)
        for chain in self.fkChain.chain:
            pm.setAttr(chain + ".visibility",k = False,cb=False)
            pm.setAttr(chain + ".radi",k = False,cb=False,l=False)
            pm.setAttr(chain + '.rotateOrder',cb = True)
        
        #then ik
        self.ikChain = ikChain.IkChain(self.baseName,self.side,self.size,self.solver,type = 'ikRP')
        self.ikChain.fromList(self.limbGuidePos,self.limbGuideRot)
        
        #ik cc connect ori
        self.ikChain.ikCtrl.control.rx.connect(self.ikChain.chain[-1].rx)
        self.ikChain.ikCtrl.control.ry.connect(self.ikChain.chain[-1].ry)
        self.ikChain.ikCtrl.control.rz.connect(self.ikChain.chain[-1].rz)
        
        #set cc
        pm.addAttr(self.handSettingCtrl.control,ln = '__',at = 'enum',en = 'ArmCtrl:')
        pm.setAttr(self.handSettingCtrl.control + '.__',k = 1,l = 1)
        
        #ori                
        self.limbBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jc')
        self.limbBlendChain.fromList(self.limbGuidePos,self.limbGuideRot)
        
        self.blendData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikChain.chain,self.limbBlendChain.chain,
                                                            self.handSettingCtrl.control,'IKFK',self.baseName,self.side)
        
        self.__ikfkBlender()
        self.__setRibbonUpper()
        self.__setRibbonLower()
        self.__setRibbonSubMidCc()
        self.__shoulderCtrl()
        self.__cleanUp()
        self.__buildHooks()
        
    def __ikfkBlender(self):
        
        #connect visable function 
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'IKFK','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
        
        #connect node
        self.handSettingCtrl.control.IKFK.connect(self.ikChain.ikCtrl.controlGrp.v)
        self.handSettingCtrl.control.IKFK.connect(self.ikChain.poleVectorCtrl.controlGrp.v)
        self.handSettingCtrl.control.IKFK.connect(self.handSettingCtrl.textObj[1].v)
        self.handSettingCtrl.control.IKFK.connect(reverseNode.inputX)
        reverseNode.outputX.connect(self.fkChain.chain[0].v)
        reverseNode.outputX.connect(self.handSettingCtrl.textObj[0].v)             
        
        #set pos
#         scaleValue = 1 * self.ikChain.length/16
#         size = 1.5 * self.ikChain.length / 16
        pm.xform(self.handSettingCtrl.controlGrp,ws = 1,matrix = self.limbBlendChain.chain[2].worldMatrix.get())
        self.handSettingCtrl.controlGrp.rx.set(0)
        self.handSettingCtrl.controlGrp.ry.set(0)
        self.handSettingCtrl.controlGrp.rz.set(0)
        self.handSettingCtrl.controlGrp.sx.set(self.size / 2)
        self.handSettingCtrl.controlGrp.sy.set(self.size / 2)
        self.handSettingCtrl.controlGrp.sz.set(self.size / 2)
        pm.move(self.limbGuidePos[2][0],self.limbGuidePos[2][1] + 2 * self.size,
                self.limbGuidePos[2][2],self.handSettingCtrl.controlGrp)
        wrist_pos = pm.xform(self.limbBlendChain.chain[2],query=1,ws=1,rp=1)
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.handSettingCtrl.controlGrp + '.rotatePivot')
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.handSettingCtrl.controlGrp + '.scalePivot')
        pm.pointConstraint(self.limbBlendChain.chain[2],self.handSettingCtrl.controlGrp,mo = 1)
#         pm.orientConstraint(self.limbBlendChain.chain[2],self.handSettingCtrl.controlGrp,mo = 1)   
        control.lockAndHideAttr(self.handSettingCtrl.control,['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])
        self.handSettingCtrl.control.IKFK.set(0) 
    
    def __setRibbonUpper(self):
        '''
        this function set ribbon for the Upper 
        '''
        #get length
        self.upperJointLentgh = self.limbBlendChain.chain[1].tx.get()
        self.ribon = ribbon.Ribbon(RibbonName = self.ribbonData[0],Length = self.upperJointLentgh,
                                   size = self.size * 0.75,subMid = 1,side = self.side,
                                   midCcName = self.baseName + self.ribbonData[0])
        self.ribon.construction()

        pm.xform(self.ribon.startLoc,ws = 1,matrix = self.limbBlendChain.chain[0].worldMatrix.get())
        pm.xform(self.ribon.endLoc,ws = 1,matrix = self.limbBlendChain.chain[1].worldMatrix.get())
        
        pm.parentConstraint(self.limbBlendChain.chain[0],self.ribon.startLoc,mo = 1)
        #flip que fix
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
        self.lowerJointLentgh = self.limbBlendChain.chain[2].tx.get()
        self.ribon45hp = ribbon.Ribbon(RibbonName = self.ribbonData[1],Length = self.lowerJointLentgh,
                                       size = self.size * 0.75,subMid = 1,side = self.side,
                                       midCcName=self.baseName + self.ribbonData[1])
        self.ribon45hp.construction()

        pm.xform(self.ribon45hp.startLoc,ws = 1,matrix = self.limbBlendChain.chain[1].worldMatrix.get())
        pm.xform(self.ribon45hp.endLoc,ws = 1,matrix = self.limbBlendChain.chain[2].worldMatrix.get())
        
        pm.parentConstraint(self.limbBlendChain.chain[2],self.ribon45hp.endLoc,mo = 1)
        #flip que fix
        pm.parentConstraint(self.limbBlendChain.chain[1],self.limbBlendChain.chain[2],self.ribon45hp.epUploc,mo = 1)
        
        self.__subCtrlLower()
          
    def __subCtrlLower(self):

        #connect scale for mid jj
        self.subMidCtrlElbowWrist = self.ribon45hp.subMidCtrl
        self.subMidCtrlElbowWrist.control.scaleX.connect(self.ribon45hp.jj[2].scaleX)
        self.subMidCtrlElbowWrist.control.scaleY.connect(self.ribon45hp.jj[2].scaleY)
        self.subMidCtrlElbowWrist.control.scaleZ.connect(self.ribon45hp.jj[2].scaleZ)
        
    def __setRibbonSubMidCc(self):
        
        self.subMidCtrlElbow = control.Control(size = self.size * 0.75,baseName = self.ribbonData[2] + '_CC',side = self.side) 
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
        self.shoulderCtrl = control.Control(self.side,self.baseName + 'Shoulder',self.size,aimAxis = 'y') 
        self.shoulderCtrl.pinCtrl() 
        
        #align
        posArraySpJj = self.shoulderChain.chain[0]
        posArrayEpJj = self.shoulderChain.chain[1]
        
        posArraySp = posArraySpJj.worldMatrix.get()
        posArrayEp = posArrayEpJj.worldMatrix.get()
        
        pm.xform(self.shoulderCtrl.controlGrp,ws = 1,matrix = posArraySp)
        self.shoulderCtrl.control.sy.set(-1)
        
        sdCvOffset = posArraySp[-1][0] - posArrayEp[-1][0]
        
        for shape in self.shoulderCtrl.control.getShapes():
            pm.move(-sdCvOffset,posArraySp[-1][1],posArraySp[-1][2],shape)
        
        pm.makeIdentity(self.shoulderCtrl.control,apply = True,t = 1,r = 0,s = 1,n = 0,pn = 1)    
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
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.control + '.rotatePivot')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.control + '.scalePivot')        
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.controlGrp + '.rotatePivot')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.controlGrp + '.scalePivot')          
          
        self.shoulderBriGrp.setParent(self.shoulderCtrl.controlGrp)        
          
        #connect
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2X)
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2Y)
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2Z)
#         ori connect
#         self.shoulderAtChain.chain[0].rx.connect(multipleNode.input1X)
#         self.shoulderAtChain.chain[0].ry.connect(multipleNode.input1Y)
#         self.shoulderAtChain.chain[0].rz.connect(multipleNode.input1Z)
        multipleNode.outputX.connect(remapColorNode.colorR)
        multipleNode.outputY.connect(remapColorNode.colorG)
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
          
        #shoulderBlade
        #initial
        pm.select(cl = 1)
        self.shoulderBladeGrp = pm.group(n = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade','grp'))
        pm.xform(self.shoulderBladeGrp,ws = 1,matrix = posArraySp)
        pm.select(cl = 1)
        self.shoulderBladeBriGrp = pm.group(n = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade_Bri','grp'))
        pm.xform(self.shoulderBladeBriGrp,ws = 1,matrix = posArraySp)
        self.shoulderBladeBriGrp.setParent(self.shoulderBladeGrp)
        self.shoulderBladeChain.chain[0].setParent(self.shoulderBladeBriGrp)
#         pm.select(self.shoulderBladeChain.chain[0])
#         pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBladeChain.chain[0] + '.rotatePivot')
#         pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBladeChain.chain[0] + '.scalePivot')
          
        #node name
        remapValueShoulderFBNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderFwBk','RV')
        remapValueShoulderUDNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderUpDn','RV')
          
        #create Node
        remapValueShoulderFBNode = pm.createNode('remapValue',n = remapValueShoulderFBNodeName)
        remapValueShoulderUDNode = pm.createNode('remapValue',n = remapValueShoulderUDNodeName)
          
        #connect
        #FB
#         self.shoulderCtrl.control.rz.connect(remapValueShoulderFBNode.inputValue)
        remapValueShoulderFBNode.inputMin.set(-90)
        remapValueShoulderFBNode.inputMax.set(90)
        remapValueShoulderFBNode.outputMin.set(-90)
        remapValueShoulderFBNode.outputMax.set(90)
        remapValueShoulderFBNode.outValue.connect(self.shoulderBladeBriGrp.rz)
  
        remapValueShoulderFBNode.value[1].value_FloatValue.set(0.75)
        remapValueShoulderFBNode.value[1].value_Position.set(1)                                                        
        remapValueShoulderFBNode.value[2].value_FloatValue.set(0.5)
        remapValueShoulderFBNode.value[2].value_Position.set(0.5)
        remapValueShoulderFBNode.value[2].value_Interp.set(1)        
          
        #UD
#         self.shoulderCtrl.control.ry.connect(remapValueShoulderUDNode.inputValue)
        remapValueShoulderUDNode.inputMin.set(-90)
        remapValueShoulderUDNode.inputMax.set(90)
        remapValueShoulderUDNode.outputMin.set(float(self.shoulderChain.chain[-1].tx.get() / 4))
        remapValueShoulderUDNode.outputMax.set(-float(self.shoulderChain.chain[-1].tx.get() / 4))
        remapValueShoulderUDNode.outValue.connect(self.shoulderBladeBriGrp.tz)
  
        remapValueShoulderUDNode.value[1].value_FloatValue.set(0.75)
        remapValueShoulderUDNode.value[1].value_Position.set(1)                                                        
        remapValueShoulderUDNode.value[2].value_FloatValue.set(0.5)
        remapValueShoulderUDNode.value[2].value_Position.set(0.5)
        remapValueShoulderUDNode.value[2].value_Interp.set(1)     
          
        #connect to the AT
        #create PMA node
        plusMinusAverageAtSdNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','PMA')
          
        #create Node 
        plusMinusAverageAtSdNode = pm.createNode('plusMinusAverage',n = plusMinusAverageAtSdNodeName)
          
        #connect
        self.shoulderCtrl.control.rx.connect(plusMinusAverageAtSdNode.input3D[0].input3Dx)
        self.shoulderCtrl.control.ry.connect(plusMinusAverageAtSdNode.input3D[0].input3Dy)
        self.shoulderCtrl.control.rz.connect(plusMinusAverageAtSdNode.input3D[0].input3Dz)
        self.shoulderBriGrp.ry.connect(plusMinusAverageAtSdNode.input3D[1].input3Dy)
        self.shoulderBriGrp.rz.connect(plusMinusAverageAtSdNode.input3D[1].input3Dz)
          
        plusMinusAverageAtSdNode.output3D.output3Dy.connect(remapValueShoulderUDNode.inputValue)
        plusMinusAverageAtSdNode.output3D.output3Dz.connect(remapValueShoulderFBNode.inputValue)
          
        ##############
        #chest clean 
#         self.chestGrp = pm.group(em = 1,n = nameUtils.getUniqueName('m','chest','grp'))
#         self.chestGrp.setParent(self.hi.SKL)
#         self.shoulderCtrl.controlGrp.setParent(self.chestGrp)
#         self.shoulderAtChain.chain[0].setParent(self.chestGrp)
          
        ############
        #pose Reador
          
        #set main Loc
        poseMain = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorMain','loc'))
        poseMain.overrideEnabled.set(1)
        poseMain.overrideColor.set(16)
          
        poseUp = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorUp','loc'))
        poseUp.localScale.set(0.5,0.5,0.5)
        poseUp.overrideEnabled.set(1)
        poseUp.overrideColor.set(16)
          
        poseTar = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTar','loc'))
        poseTar.localScale.set(0.25,0.25,0.25)
        poseTar.overrideEnabled.set(1)
        poseTar.overrideColor.set(16)
         
        #set twist loc
        poseTwistMain = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwistMain','loc'))
        poseTwistMain.overrideEnabled.set(1)
        poseTwistMain.overrideColor.set(4)
         
        poseTwistUp = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwistUp','loc'))
        poseTwistUp.localScale.set(0.5,0.5,0.5)
        poseTwistUp.overrideEnabled.set(1)
        poseTwistUp.overrideColor.set(4)
         
        poseTwistTar = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwistTar','loc'))
        poseTwistTar.localScale.set(0.25,0.25,0.25)
        poseTwistTar.overrideEnabled.set(1)
        poseTwistTar.overrideColor.set(4) 
         
        pm.setAttr(poseMain + '.tx',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseTar + '.tx',float(self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseUp + '.tx',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseUp + '.ty',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
         
        #create grp
        #main
        self.poseReadorGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorMain','grp'))
         
        poseMain.setParent(self.poseReadorGrp)
        poseTar.setParent(self.poseReadorGrp)
        poseUp.setParent(self.poseReadorGrp)
         
        poseTwistUp.setParent(self.poseReadorGrp)
        poseTwistMain.setParent(self.poseReadorGrp)        
        poseTwistTar.setParent(self.poseReadorGrp)
                   
        pm.xform(self.poseReadorGrp,ws = 1,matrix = self.limbBlendChain.chain[0].worldMatrix.get())
        self.poseReadorGrp.setParent(self.shoulderAtChain.chain[0])
        self.poseReadorGrp.t.set(0,0,0)
        self.poseReadorGrp.r.set(0,0,0)
         
        pm.aimConstraint(poseTar,poseMain,offset = [0,0,0],w = 1,aimVector = [1,0,0],upVector = [0,-1,0],
                         worldUpType = 'object',worldUpObject = poseUp)        
 
        #twist
        pm.setAttr(poseTwistTar + '.ty',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseTwistUp + '.tx',float(-self.shoulderAtChain.chain[1].tx.get() / 8))
           
        pm.aimConstraint(poseTwistTar,poseTwistMain,offset = [0,0,0],w = 1,aimVector = [0,-1,0],upVector = [-1,0,0],
                        worldUpType = 'object',worldUpObject = poseTwistUp)
           
        #connect 
#         self.poseReadorGrp.setParent(self.chestGrp)
        postTarGrp = pm.group(poseTar,n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTar','grp'))
           
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),postTarGrp + '.rotatePivot')
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),postTarGrp + '.scalePivot')
           
        postTarGrp.setParent(self.shoulderAtChain.chain[0])
        poseTwistTar.setParent(postTarGrp)
        poseTwistGrp = pm.group(poseTwistUp,poseTwistMain,n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwist','grp'))
           
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),poseTwistGrp + '.rotatePivot')
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),poseTwistGrp + '.scalePivot')        
           
        #multiple node name
        prMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorBri','MDN')
           
        #create Node
        prMultipleNode = pm.createNode('multiplyDivide',n = prMultipleNodeName)
           
        poseMain.ry.connect(prMultipleNode.input1Y)
        poseMain.rz.connect(prMultipleNode.input1Z)
        prMultipleNode.input2Y.set(-2)
        prMultipleNode.input2Z.set(-2)
        prMultipleNode.outputY.connect(poseTwistGrp.ry)
        prMultipleNode.outputZ.connect(poseTwistGrp.rz)
           
        control.addFloatAttr(self.shoulderAtChain.chain[0],
                             ['pose_bend','pose_side','pose_twist'],-3600,3600) 
           
        #get correct value
        prMultipleNode.outputY.connect(self.shoulderAtChain.chain[0].pose_bend)
        prMultipleNode.outputZ.connect(self.shoulderAtChain.chain[0].pose_side)
        poseTwistMain.rx.connect(self.shoulderAtChain.chain[0].pose_twist)
           
        #reconnect
        self.shoulderAtChain.chain[0].pose_bend.connect(multipleNode.input1Y)
        self.shoulderAtChain.chain[0].pose_side.connect(multipleNode.input1Z)
#         self.shoulderAtChain.chain[0].pose_twist.connect(multipleNode.input1X)
           
        #clean
        self.poseReadorGrp.v.set(0)
        postTarGrp.v.set(0)  
           
    def __cleanUp(self):
          
        #add cc ctrl
        control.addFloatAttr(self.handSettingCtrl.control,['CC'],0,1) 
          
        #ccDef grp and v
        self.ccDefGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Def','grp')) 
        self.subMidCtrlShoulderElbow.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlElbowWrist.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlElbow.controlGrp.setParent(self.ccDefGrp)
        self.handSettingCtrl.control.CC.set(0)
        self.handSettingCtrl.control.CC.connect(self.ccDefGrp.v)
          
        #cc hierarchy        
        self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
                                n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))
          
  
        self.ccDefGrp.setParent(self.cntsGrp)
#         self.cntsGrp.setParent(self.hi.CC) 
        self.handSettingCtrl.controlGrp.setParent(self.cntsGrp)    
                  
        if self.solver == 'ikRPsolver':
            pm.parent(self.ikChain.poleVectorCtrl.controlGrp,self.cntsGrp)        
          
        #ribbon hierarchy   
        self.ribon.main.v.set(0)
        self.ribon45hp.main.v.set(0)
          
        #ik stretch loc vis
        self.ikChain.stretchStartLoc.v.set(0)
        self.ikChain.lockUpStartLoc.v.set(0)
  
        #jj grp
        self.limbGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))
         
        self.ikChain.lockUpStartLoc.setParent(self.limbGrp)
        self.ikChain.stretchStartLoc.setParent(self.limbGrp)
         
        armInitial =  self.limbBlendChain.chain[0].getTranslation(space = 'world')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.limbGrp + '.rotatePivot')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.limbGrp + '.scalePivot')
          
        for b in (self.ikChain,self.fkChain,self.limbBlendChain):
            b.chain[0].setParent(self.limbGrp)
         
        self.limbGrp.setParent(self.shoulderCtrl.control)
         
#         for b in (self.ikChain,self.fkChain,self.limbBlendChain):
#             b.chain[0].setParent(self.bonesGrp)
#          
#         self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))
#              
#         self.mainGrp = pm.group(self.bonesGrp,self.cntsGrp,self.handSettingCtrl,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))   
 
    def __buildHooks(self):
 
        #create and align
        worldName = nameUtils.getUniqueName(self.side,self.baseName + 'World','loc')
        self.locWorld = pm.spaceLocator(n = worldName)
        self.locWorld.v.set(0)
           
        localName = nameUtils.getUniqueName(self.side,self.baseName + 'Local','loc')
        self.locLocal = pm.spaceLocator(n = localName)
        self.locLocal.v.set(0)
           
        pm.xform(self.locWorld,ws = 1,matrix = self.limbBlendChain.chain[0].wm.get())
        pm.xform(self.locLocal,ws = 1,matrix = self.limbBlendChain.chain[0].wm.get())
         
        self.locWorld.r.set(0,0,0)
        self.locLocal.r.set(0,0,0)
          
        self.locLocal.setParent(self.shoulderChain.chain[-1])
        pm.parentConstraint(self.shoulderCtrl.control,self.locWorld,skipRotate = ['x','y','z'],mo = 1)
           
        self.fkChain.chain[0].addAttr('space',at = 'enum',en = 'world:local:',k = 1)
           
        #add target tester
        targetName = nameUtils.getUniqueName(self.side,self.baseName + 'Tar','loc')
        self.__tempSpaceSwitch = pm.spaceLocator(n = targetName)
        pm.xform(self.__tempSpaceSwitch,ws = 1,matrix = self.limbBlendChain.chain[0].wm.get())
#         self.__tempSpaceSwitch.setParent(self.hi.XTR)
        self.__tempSpaceSwitch.v.set(0)
    
        #final cnst
        finalCnst = pm.parentConstraint(self.locLocal,self.locWorld,self.__tempSpaceSwitch,mo = 1)
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'Hook','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
            
        #fk cnst
        pm.parentConstraint(self.__tempSpaceSwitch,self.limbGrp,mo = 1)
        self.fkChain.chain[0].attr('space').connect(finalCnst.attr(self.locLocal.name() + 'W0'))
        self.fkChain.chain[0].attr('space').connect(reverseNode.inputX)
        reverseNode.outputX.connect(finalCnst.attr(self.locWorld.name() + 'W1'))

    def buildConnections(self):

        #reveice info from incoming package
        if pm.objExists(self.metaMain) and pm.objExists(self.metaSpine) == 1:
            
            print ''
            print 'Package from (' + self.metaMain + ') has been received'
            
            pm.select(self.metaMain) 
            main = pm.selected()[0]
            
            pm.select(self.metaSpine)
            spine = pm.selected()[0]
            
            #meta main
            mainDestinations = []
            moduleGrp = pm.connectionInfo(main.moduleGrp, destinationFromSource=True)
            
            #meta spine
            spineDestinations = []
            transGrp = pm.connectionInfo(spine.transGrp, destinationFromSource=True)
            
            #get linked
            for tempMainDestination in moduleGrp:
                splitTempMainDestination = tempMainDestination.split('.')
                mainDestinations.append(splitTempMainDestination[0])
                
            for tempSpineDestination in transGrp:
                splitTempSpineDestination = tempSpineDestination.split('.')
                spineDestinations.append(splitTempSpineDestination[0])
#             print spineDestinations
#             [u'asd_CC', u'asd_SKL', u'asd_IK', u'asd_LOC', u'asd_XTR', u'asd_GUD', u'asd_GEO', u'asd_ALL', u'asd_TRS', u'asd_PP']

#             self.chestGrp = pm.group(em = 1,n = nameUtils.getUniqueName('m','chest','grp'))
#             self.chestGrp.setParent(self.hi.SKL)
            
            #to the chest
            self.shoulderBladeGrp.setParent(spineDestinations[0])
            self.shoulderAtChain.chain[0].setParent(spineDestinations[0])
            self.shoulderCtrl.controlGrp.setParent(spineDestinations[0])
            self.poseReadorGrp.setParent(spineDestinations[0])
            
            #to the main hierachy
            self.cntsGrp.setParent(mainDestinations[0]) 
            self.ribon.main.setParent(mainDestinations[4])
            self.ribon45hp.main.setParent(mainDestinations[4])
#             self.ikChain.lockUpStartLoc.setParent(mainDestinations[1])
#             self.ikChain.stretchStartLoc.setParent(mainDestinations[1])
            self.ikChain.ikHandle.setParent(mainDestinations[2])
            self.guideGrp.setParent(mainDestinations[5])
            self.locWorld.setParent(mainDestinations[2])
            self.__tempSpaceSwitch.setParent(mainDestinations[4])
            
            print ''
            print 'Info from (' + self.meta + ') has been integrate, ready for next Module'
            print ''
            
        else:
            OpenMaya.MGlobal.displayError('Target :' + self.metaMain + ' is NOT exist')
            
        #create package send for next part
        #template:
        #metaUtils.addToMeta(self.meta,'attr', objs)
        metaUtils.addToMeta(self.meta,'controls',[self.handSettingCtrl.control])
#          ([self.ikChain.ikCtrl.control,self.ikChain.poleVectorCtrl.control] + [fk for fk in self.fkChain.chain])
        metaUtils.addToMeta(self.meta,'moduleGrp',[self.limbGrp])
        metaUtils.addToMeta(self.meta,'chain', [ik for ik in self.ikChain.chain] + [ori for ori in self.limbBlendChain.chain])
        
        
#         #mirror part:
#         if self.mirror == 1:
#             print ''
#             print 'mirror selection is active'
#              
#             #perpare 
#             mirrorSide = None
#             self.mirror = 2
#             
#             if self.side == 'l':
#                 mirrorSide = 'r'
#              
#             mirrorLimb = LimbModule(self.baseName,mirrorSide,self.size,self.solver,
#                                     self.metaSpine,self.metaMain,self.mirror)
#              
#             mirrorLimb.buildGuides()
#             oriGuideList = []
#             
#             #mirror guide
#             for gud in mirrorLimb.totalGuides:
#                 
#                 #perpare
#                 oriName = gud.split('_')
#                 
#                 #sl list
#                 pm.select(self.side + str(gud[1:]))
#                 oriGuide = pm.selected()[0]
#                 oriGuideList.append(oriGuide)
#                  
#                 #create Node Name
#                 linearNodeName = nameUtils.getUniqueName(self.side,oriName[1],'MDL')
#                 
#                 #create Node
#                 linearNode = pm.createNode('multDoubleLinear',n = linearNodeName)
#                 
#                 #connect Node
#                 oriGuide.tx.connect(linearNode.input1)
#                 linearNode.input2.set(-1)
#                 linearNode.output.connect(gud.tx)
#                 
# #             print oriGuideList
# #             print mirrorLimb.totalGuides
#             mirrorLimb.build()
#             mirrorLimb.buildConnections()
#             
#         else :
#             print 'mirror selection is in_active'        
        
def getUi(parent,mainUi):
    
    return LimbModuleUi(parent,mainUi)

class LimbModuleUi(object):
    
    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        self.__popuItems = []
        
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
        
        #(self,baseName = 'arm',side = 'l',size = 1.5,
        self.name = pm.text(l = '**** Limb Module ****')       
        self.baseNameT = pm.textFieldGrp(l = 'baseName : ',ad2 = 1,text = 'arm')
        self.sideT = pm.textFieldGrp(l = 'side :',ad2 = 1,text = 'l')
        self.cntSize = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],
                                        ad2 = 1,numberOfFields = 1,value1 = 1)
        self.solverMenu = pm.optionMenu(l = 'color')
        pm.menuItem(l = 'ikRPsolver')
        pm.menuItem(l = 'ikSCsolver')
#         self.mirror = pm.radioButtonGrp('mirror',nrb = 2,label = 'Mirror:',la2 = ['yes','no'],sl = 1)    
        
        self.metaSpineNodeN = pm.textFieldGrp(l = 'spineMeta :',ad2 = 1,text = 'spineMeta')        
        self.mainMetaNodeN = pm.textFieldGrp(l = 'mainMeta :',ad2 = 1,text = 'mainMeta')
        self.ver2Loc = pm.button(l = 'ver2Loc',c = self.__clusLoc)
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance)
        pm.separator(h = 10)
        
        self.__pointerClass = None
        
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
        
    def getModuleInstance(self):
        
        baseNameT = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)
        sideT = pm.textFieldGrp(self.sideT,q = 1,text = 1)
        cntSizeV = pm.floatFieldGrp(self.cntSize,q = 1,value1 = 1)
        solverV = pm.optionMenu(self.solverMenu, q = 1,v = 1)
#         mirrorC = pm.radioButtonGrp(self.mirror,q = 1,sl = 1)
        mainMetaNode = pm.textFieldGrp(self.mainMetaNodeN,q = 1,text = 1)
        spineMetaNode = pm.textFieldGrp(self.metaSpineNodeN,q = 1,text = 1)
        
        self.__pointerClass = LimbModule(baseNameT,sideT,size = cntSizeV,solver = solverV,
                                         metaSpine = spineMetaNode,metaMain = mainMetaNode)        
#         self.__pointerClass = LimbModule(baseNameT,sideT,size = cntSizeV,solver = solverV,
#                                          metaSpine = spineMetaNode,metaMain = mainMetaNode,mirror = mirrorC)                
        
        return self.__pointerClass
    
    def __clusLoc(self,*arg):
        
        '''create a clus base on edges'''        
        sideT = pm.textFieldGrp(self.sideT,q = 1,text = 1)
        cntSizeV = pm.floatFieldGrp(self.cntSize,q = 1,value1 = 1)
        baseNameT = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)

        #sl edges
        edges = pm.selected(flatten = True)
        #convert to edges
        verts = list(set(sum([list(e.connectedVertices()) for e in edges],[])))

        #create clus
        clusShp,clusTras = pm.cluster(verts)
          
        helpCtrl = control.Control(side = sideT,baseName = baseNameT + 'Pos',size = cntSizeV)
        helpCtrl.solidSphereCtrl()
        pcn = pm.pointConstraint(clusTras,helpCtrl.controlGrp, mo = False)
        pm.delete(pcn)
        pm.delete(clusTras)    
