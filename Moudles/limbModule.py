import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy

class LimbModule(object):
    
#     posArray = [[2,14,-0.2],[4,14,-0.3],[6.15,14,-0.2],[6.4,14,-0.2]]
    
    posArray = [[2,14,-0.2],[4,14,-0.3],[6.15,14,-0.2]]
    rotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'arm',side = 'l',size = 1.5,
                 solver = 'ikRPsolver',controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = side
#         self.cntColor = cntColor
        self.size = size
        self.solver = solver
        self.controlOrient = controlOrient
        
        '''
        self para
        '''
        
        #jj
        self.fkChain = None
        self.ikChain = None
        self.blendChain = None
        self.blendData = None
        self.sklGrp = None
            
        #cc    
        self.config_node = None
        self.ccDefGrp = None
        self.cntsGrp = None
        
        #guides 
        self.guides = None
        self.guideGrp = None
        
        self.ribon = None
        self.ribon45hp = None
        
        self.subMidCtrlShoulderElbow = None
        self.subMidCtrlElbowWrist = None
        self.subMidCtrlElbow = None
         
        self.ribbonData = ['ShoulderElbow','EblowWrist','Elbow']
        
        self.hi = None
        
         
    def buildGuides(self):
        
        self.hi = hierarchy.Hierarchy(characterName = 'test')
        self.hi.build()
        
        self.guides = []
            
        for i,p in enumerate(self.posArray):
            name = nameUtils.getUniqueName(self.side,self.baseName,'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(p)
            loc.r.set(self.rotArray[i])
            self.guides.append(loc)
            
        tempGuides = list(self.guides)
        tempGuides.reverse()
        for i in range(len(tempGuides)):
            if i != (len(tempGuides) - 1):
                pm.parent(tempGuides[i],tempGuides[i + 1])
        
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(self.guides[0],n = name)
                     
               
    def build(self):
        
        self.guidePos = [x.getTranslation(space = 'world') for x in self.guides]
        self.guideRot = [x.getRotation(space = 'world') for x in self.guides]
        
        #addBlendCtrl 
        self.config_node = control.Control(self.side,self.baseName + 'Settings',self.size) 
        self.config_node.ikfkBlender()        
        
        #fk first 
        self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkChain.fromList(self.guidePos,self.guideRot,skipLast = 0)
        
        #then ik
        self.ikChain = ikChain.IkChain(self.baseName,self.side,self.size,self.solver,type = 'ikRP')
        self.ikChain.fromList(self.guidePos,self.guideRot)
        
        #ik cc connect ori
        self.ikChain.ikCtrl.control.rx.connect(self.ikChain.chain[-1].rx)
        self.ikChain.ikCtrl.control.ry.connect(self.ikChain.chain[-1].ry)
        self.ikChain.ikCtrl.control.rz.connect(self.ikChain.chain[-1].rz)
        
        #set cc
        pm.addAttr(self.config_node.control,ln = '__',at = 'enum',en = 'ArmCtrl:')
        pm.setAttr(self.config_node.control + '.__',k = 1,l = 1)
        
        #ori                
        self.blendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.blendChain.fromList(self.guidePos,self.guideRot)
        
        self.blendData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikChain.chain,self.blendChain.chain,
                                                            self.config_node.control,'IKFK',self.baseName,self.side)
        
        self.__ikfkBlender()
        self.__setRibbonUpper()
        self.__setRibbonLower()
        self.__setRibbonSubMidCc()
         
        self.__cleanUp()
        
    def __ikfkBlender(self):
        
        #connect visable function 
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'IKFK','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
        
        #connect node
        self.config_node.control.IKFK.connect(self.ikChain.ikCtrl.controlGrp.v)
        self.config_node.control.IKFK.connect(self.ikChain.poleVectorCtrl.controlGrp.v)
        self.config_node.control.IKFK.connect(self.config_node.textObj[2].v)
        self.config_node.control.IKFK.connect(reverseNode.inputX)
        reverseNode.outputX.connect(self.fkChain.chain[0].v)
        reverseNode.outputX.connect(self.config_node.textObj[0].v)             
        
        #set pos
        scaleValue = 1 * self.ikChain.length/16
        size = 1.5 * self.ikChain.length / 16
        pm.xform(self.config_node.controlGrp,ws = 1,matrix = self.blendChain.chain[2].worldMatrix.get())
        self.config_node.controlGrp.rx.set(0)
        self.config_node.controlGrp.ry.set(0)
        self.config_node.controlGrp.rz.set(0)
        self.config_node.controlGrp.sx.set(scaleValue)
        self.config_node.controlGrp.sy.set(scaleValue)
        self.config_node.controlGrp.sz.set(scaleValue)
        pm.move(self.guidePos[2][0],self.guidePos[2][1] + 2 * size,self.guidePos[2][2],self.config_node.controlGrp)
        wrist_pos = pm.xform(self.blendChain.chain[2],query=1,ws=1,rp=1)
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.config_node.controlGrp + '.rotatePivot')
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.config_node.controlGrp + '.scalePivot')
        pm.pointConstraint(self.blendChain.chain[2],self.config_node.controlGrp,mo = 1)
#         pm.orientConstraint(self.blendChain.chain[2],self.config_node.controlGrp,mo = 1)   
        control.lockAndHideAttr(self.config_node.control,['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])     
    
    def __setRibbonUpper(self):
        '''
        this function set ribbon for the Upper 
        '''
        self.ribon = ribbon.Ribbon(RibbonName = self.ribbonData[0],Width = 1.0,Length = 5.0,UVal = 1,VVal = 5,subMid = 1,side = self.side,baseName=self.baseName + self.ribbonData[0])
        self.ribon.construction()

        pm.xform(self.ribon.startLoc,ws = 1,matrix = self.blendChain.chain[0].worldMatrix.get())
        pm.xform(self.ribon.endLoc,ws = 1,matrix = self.blendChain.chain[1].worldMatrix.get())
        
        pm.parentConstraint(self.blendChain.chain[0],self.ribon.startLoc,mo = 1)
        pm.parentConstraint(self.blendChain.chain[0],self.blendChain.chain[1],self.ribon.epUploc,mo = 1)
        
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

        pm.xform(self.ribon45hp.startLoc,ws = 1,matrix = self.blendChain.chain[1].worldMatrix.get())
        pm.xform(self.ribon45hp.endLoc,ws = 1,matrix = self.blendChain.chain[2].worldMatrix.get())
        
        pm.parentConstraint(self.blendChain.chain[2],self.ribon45hp.endLoc,mo = 1)
        
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
        elbolPos = pm.xform(self.blendChain.chain[1],query=1,ws=1,rp=1)
        pm.move(self.subMidCtrlElbow.controlGrp,elbolPos[0],elbolPos[1],elbolPos[2],a=True)
        
        pm.parentConstraint(self.subMidCtrlElbow.control,self.ribon45hp.startLoc,mo = 1)
        pm.parentConstraint(self.subMidCtrlElbow.control,self.ribon.endLoc,mo = 1)
        pm.parentConstraint(self.blendChain.chain[1],self.subMidCtrlElbow.controlGrp,mo = 1)
        
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
        self.blendChain.chain[1].scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlShoulderElbow.control.scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.blendChain.chain[1].scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlShoulderElbow.control.scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.blendChain.chain[1].scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
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
        self.blendChain.chain[0].scaleX.connect(self.ribon.jj[4].scaleX)
        self.blendChain.chain[0].scaleY.connect(self.ribon.jj[4].scaleY)
        self.blendChain.chain[0].scaleZ.connect(self.ribon.jj[4].scaleZ)
        
        
        
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
        self.blendChain.chain[2].scaleX.connect(self.ribon45hp.jj[0].scaleX)
        self.blendChain.chain[2].scaleY.connect(self.ribon45hp.jj[0].scaleY)
        self.blendChain.chain[2].scaleZ.connect(self.ribon45hp.jj[0].scaleZ)
            
    def __cleanUp(self):
        
        #add cc ctrl
        control.addFloatAttr(self.config_node.control,['CC'],0,1) 
        
        #ccDef grp and v
        self.ccDefGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Def','grp')) 
        self.subMidCtrlShoulderElbow.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlElbowWrist.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlElbow.controlGrp.setParent(self.ccDefGrp)
        self.config_node.control.CC.set(0)
        self.config_node.control.CC.connect(self.ccDefGrp.v)
        
        #cc hierarchy        
        self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
                                n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))
        

        self.ccDefGrp.setParent(self.cntsGrp)
        self.cntsGrp.setParent(self.hi.CC) 
        self.config_node.controlGrp.setParent(self.cntsGrp)    
                
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
        self.sklGrp = pm.group(self.ikChain.lockUpStartLoc,self.ikChain.stretchStartLoc,
                               n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))
        
        armInitial =  self.blendChain.chain[0].getTranslation(space = 'world')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.sklGrp + '.rotatePivot')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.sklGrp + '.scalePivot')
        
        for b in (self.ikChain,self.fkChain,self.blendChain):
            b.chain[0].setParent(self.sklGrp)
            
        self.sklGrp.setParent(self.hi.SKL)
                    
            
#         for b in (self.ikChain,self.fkChain,self.blendChain):
#             b.chain[0].setParent(self.bonesGrp)
#          
#         self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))
#              
#         self.mainGrp = pm.group(self.bonesGrp,self.cntsGrp,self.config_node,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))   
         


# from Modules import limbModule
# lm = limbModule.LimbModule()
# lm.buildGuides()
# lm.build()
