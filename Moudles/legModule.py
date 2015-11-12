import pymel.core as pm
from Modules.subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils,metaUtils
from Modules import control,hierarchy
from maya import OpenMaya

class LegModule(object):
    
    posArray = [[0.772,9.008,0],[0.772,4.8,0.258],[0.772,1,-0.411],[0.772,0,-1.1],[0.772,0,1.8],[0.443,0,0.584],[1.665,0,0.584],[0.772,0,0.584]]
    rotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'leg',side = 'l',size = 1.5,
                 controlOrient = [0,0,0],metaMain = None):
        
        self.baseName = baseName
        self.side = side
        self.size = size
        self.controlOrient = controlOrient
        
        '''
        self para
        '''

        #jj 
        self.ikRpPvChain = None
        self.ikRpChain = None
        self.ikBlendChain = None
        self.fkChain = None
        self.legBlendChain = None
        self.blendData = None   
        self.sklGrp = None
        self.upperJointLentgh = None
        self.lowerJointLentgh = None        
        
        #cc
        self.config_node = None       
        self.ccDefGrp = None
        self.cntsGrp = None
        
        #guide
        self.guides = None
        self.guideGrp = None
        
        #ribon
        self.ribon = None
        self.ribon45hp = None 
        self.subMidCtrlThighKnee = None
        self.subMidCtrlKneeAnkle = None
        self.subMidCtrlKnee = None
        
        #name list 
        self.ribbonData = ['ThighKnee','KneeAnkle','Knee']
        self.legNameList = ['Thigh','Knee','Ankle','Heel','Toe','Inside','Outside','Ball']
        self.footNameList = ['Thigh','Knee','Ankle','Ball','Toe','Heel']       
        
        #metanode
        self.meta = metaUtils.createMeta(self.side,self.baseName,0)
        self.metaMain = metaMain 
        
    def buildGuides(self):
        
        self.guides = []
        #set pos loc    
        for i,p in enumerate(self.posArray):
            name = nameUtils.getUniqueName(self.side,self.legNameList[i],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(p)
            loc.r.set(self.rotArray[i])
            self.guides.append(loc)
            
        tempGuides = list(self.guides)
        tempGuides.reverse()
        
        #set loc grp
        for i in range(len(tempGuides)):
            if i != (len(tempGuides) - 1):
                pm.parent(tempGuides[i],tempGuides[i + 1])
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(self.guides[0],n = name)
            
    def build(self):
        
        self.guidePos = [x.getTranslation(space = 'world') for x in self.guides]
        self.guideRot = [x.getRotation(space = 'world') for x in self.guides]
        
        footPos = []
        footPos.append(self.guidePos[-1])        
        footPos.append(self.guidePos[4])
        footPos.append(self.guidePos[3])
        
        #addBlendCtrl 
        self.config_node = control.Control(self.side,self.baseName + 'IKFK_blender',self.size) 
        self.config_node.ikfkBlender()
        
        #ikRpPvChain
        self.ikRpPvChain = ikChain.IkChain(self.baseName,self.side,self.size,solver = 'ikRPsolver',type = 'ikRP')
        self.ikRpPvChain.fromList(self.guidePos[0:3],self.guideRot)
        for num,joint in enumerate(self.ikRpPvChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'ikRP')
            pm.rename(joint,name)
  
        #ikRpChain
        self.ikRpChain = ikChain.IkChain(self.baseName,self.side,self.size,solver = 'ikRPsolver',type = 'ikNF')
        self.ikRpChain.fromList(self.guidePos[0:3],self.guideRot)
        for num,joint in enumerate(self.ikRpChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'ikNF')
            pm.rename(joint,name)
          
        #ik blend 
        self.ikBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'ik')
        self.ikBlendChain.fromList(self.guidePos[0:3] + footPos,self.guideRot)
        self.ikBlendChainData = boneChain.BoneChain.blendTwoChains(self.ikRpChain.chain,self.ikRpPvChain.chain,self.ikBlendChain.chain[0:3],
                                                                   self.ikRpPvChain.ikCtrl.control,'enable_PV',self.baseName,self.side)
        for num,joint in enumerate(self.ikBlendChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'ik')
            pm.rename(joint,name)
          
        #ikset
        self.__ikSet()
            
        #fk 
        self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkChain.fromList(self.guidePos[0:3] + footPos,self.guideRot)
        for num,joint in enumerate(self.fkChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'fk')
            pm.rename(joint,name)
        pm.delete(self.fkChain.chain[4].getShape())
        
        #ori chain
        self.legBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.legBlendChain.fromList(self.guidePos[0:3] + footPos,self.guideRot)
        self.ikBlendChainData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikBlendChain.chain,self.legBlendChain.chain,
                                                                   self.config_node.control,'IKFK',self.baseName,self.side)
        for num,joint in enumerate(self.legBlendChain.chain,):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'jj')
            pm.rename(joint,name)
         
        self.ikBlendChain.chain[-1].setParent(self.ikBlendChain.chain[-4])
        self.fkChain.chain[-1].setParent(self.fkChain.chain[-4])
        self.legBlendChain.chain[-1].setParent(self.legBlendChain.chain[-4])
        
        #ikfkset
        self.__ikfkBlendSet()
         
        #leg set
        self.__setRibbonUpper()
        self.__setRibbonLower()
        self.__setRibbonSubMidCc()
          
        #foot set
        self.__editCtrl()
        self.__ikFootSet()        
        self.__cleanUp()

    def __ikSet(self):
        
        #stretch loc reset
        self.ikRpChain.stretchEndLoc.setParent(self.ikRpPvChain.ikCtrl.control)
        
        #reset ik cc
        pm.delete(self.ikRpChain.ikCtrl.controlGrp)
        
        #connect joint stretch
        self.ikRpPvChain.ikCtrl.control.stretch.connect(self.ikRpChain.stretchBlendcolorNode.blender)
        
        #connect ik handle point cnst
#         pm.pointConstraint(self.ikRpPvChain.ikCtrl.control,self.ikRpChain.ikHandle,w = 1)
        
        #rename ikRPcc
        pm.rename(self.ikRpPvChain.ikCtrl.control,nameUtils.getUniqueName(self.side,self.baseName + 'ik','cc'))
        pm.rename(self.ikRpPvChain.ikCtrl.controlGrp,nameUtils.getUniqueName(self.side,self.baseName + 'ik','grp'))        
        
        #set ik flip
        self.ikRpChain.ikHandle.poleVectorX.set(-0.1)
        self.ikRpChain.ikHandle.poleVectorY.set(0)
        self.ikRpChain.ikHandle.poleVectorZ.set(0)
        PMAName = nameUtils.getUniqueName(self.side,self.baseName + '_noFlip','PMA')
        pm.addAttr(self.ikRpPvChain.ikCtrl.control, ln = 'knee_twist', at ="float",dv = 0,h = False,k = True )
        pm.addAttr(self.ikRpPvChain.ikCtrl.control, ln = 'knee_offset', at ="float",dv = 0,h = False,k = True )
        plusMinusAverageNode = pm.createNode('plusMinusAverage',n = PMAName)
        self.ikRpPvChain.ikCtrl.control.knee_offset.connect(plusMinusAverageNode.input1D[0])
        self.ikRpPvChain.ikCtrl.control.knee_twist.connect(plusMinusAverageNode.input1D[1])                
        plusMinusAverageNode.output1D.connect(self.ikRpChain.ikHandle.twist)
        self.ikRpPvChain.ikCtrl.control.knee_offset.set(-90)
        self.ikRpPvChain.ikCtrl.control.knee_offset.lock(1)
        
        #add ik pv vis
        self.ikRpPvChain.ikCtrl.control.enable_PV.connect(self.ikRpPvChain.poleVectorCtrl.controlGrp.v)
        self.ikRpChain.ikHandle.v.set(0)
        self.ikRpChain.stretchStartLoc.v.set(0)
        self.ikRpPvChain.stretchStartLoc.v.set(0)  
    
    def __ikfkBlendSet(self):
    
        #connect visable function
        #create node 
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'IKFK','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
        
        #connecct node 
        self.config_node.control.IKFK.connect(self.ikRpPvChain.ikCtrl.controlGrp.v)
        self.config_node.control.IKFK.connect(self.config_node.textObj[2].v)
        self.config_node.control.IKFK.connect(reverseNode.inputX)
        reverseNode.outputX.connect(self.fkChain.chain[0].v)
        reverseNode.outputX.connect(self.config_node.textObj[0].v)
        
        #set pos
        pm.xform(self.config_node.controlGrp,ws = 1,matrix = self.legBlendChain.chain[2].worldMatrix.get())
        self.config_node.controlGrp.rx.set(0)
        self.config_node.controlGrp.ry.set(0)
        self.config_node.controlGrp.rz.set(0)
        pm.move(self.guidePos[2][0],self.guidePos[2][1],self.guidePos[4][2],self.config_node.controlGrp)
        ankle_pos = pm.xform(self.legBlendChain.chain[2],query=1,ws=1,rp=1)
        pm.move(ankle_pos[0],ankle_pos[1],ankle_pos[2],self.config_node.controlGrp + '.rotatePivot')
        pm.move(ankle_pos[0],ankle_pos[1],ankle_pos[2],self.config_node.controlGrp + '.scalePivot')
        pm.pointConstraint(self.legBlendChain.chain[2],self.config_node.controlGrp,mo = 1)
#         pm.orientConstraint(self.legBlendChain.chain[2],self.config_node.controlGrp,mo = 1)   
        control.lockAndHideAttr(self.config_node.control,['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])     

    #set ribbon
      
    def __setRibbonUpper(self):
        '''
        this function set ribbon for the Upper 
        '''
        self.upperJointLentgh = self.legBlendChain.chain[1].tx.get()
        self.ribon = ribbon.Ribbon(RibbonName = self.ribbonData[0],Length = self.upperJointLentgh,
                                   size = self.size * 0.75,subMid = 1,side = self.side,
                                   midCcName = self.baseName + self.ribbonData[0])   
             
        self.ribon.construction()
        
        pm.xform(self.ribon.startLoc,ws = 1,matrix = self.legBlendChain.chain[0].worldMatrix.get())
        pm.xform(self.ribon.endLoc,ws = 1,matrix = self.legBlendChain.chain[1].worldMatrix.get())
        
        pm.parentConstraint(self.legBlendChain.chain[0],self.ribon.startLoc,mo = 1)
#         pm.parentConstraint(self.legBlendChain.chain[0],self.legBlendChain.chain[1],self.ribon.epUploc,mo = 1)
        
        self.__subCtrlUpper()
        
    #set ribbon ctrl
    
    def __subCtrlUpper(self):
        
        #connect scale for thighKnee jj2
        self.subMidCtrlThighKnee = self.ribon.subMidCtrl
        self.subMidCtrlThighKnee.control.scaleX.connect(self.ribon.jj[2].scaleX)
        self.subMidCtrlThighKnee.control.scaleY.connect(self.ribon.jj[2].scaleY)
        self.subMidCtrlThighKnee.control.scaleZ.connect(self.ribon.jj[2].scaleZ)
            
    def __setRibbonLower(self):

        '''
        this function set ribbon for the thighKnee 
        '''
        self.lowerJointLentgh = self.legBlendChain.chain[2].tx.get()
        self.ribon45hp = ribbon.Ribbon(RibbonName = self.ribbonData[1],Length = self.lowerJointLentgh,
                                   size = self.size * 0.75,subMid = 1,side = self.side,
                                   midCcName = self.baseName + self.ribbonData[1])   
                
        self.ribon45hp.construction()
        
        pm.xform(self.ribon45hp.startLoc,ws = 1,matrix = self.legBlendChain.chain[1].worldMatrix.get())
        pm.xform(self.ribon45hp.endLoc,ws = 1,matrix = self.legBlendChain.chain[2].worldMatrix.get())
        
        pm.parentConstraint(self.legBlendChain.chain[2],self.ribon45hp.endLoc,mo = 1)
                
        self.__subCtrlLower()
    
    def __subCtrlLower(self):
        
        #connect scale for mid jj
        self.subMidCtrlKneeAnkle = self.ribon45hp.subMidCtrl
        self.subMidCtrlKneeAnkle.control.scaleX.connect(self.ribon45hp.jj[2].scaleX)
        self.subMidCtrlKneeAnkle.control.scaleY.connect(self.ribon45hp.jj[2].scaleY)
        self.subMidCtrlKneeAnkle.control.scaleZ.connect(self.ribon45hp.jj[2].scaleZ)

    def __setRibbonSubMidCc(self):
                
                
        self.subMidCtrlKnee = control.Control(size = self.size * 0.75,baseName = self.ribbonData[2] + '_CC',side = self.side,aimAxis = 'y') 
        self.subMidCtrlKnee.circleCtrl()
        kneePos = pm.xform(self.legBlendChain.chain[1],query=1,ws=1,rp=1)
        pm.move(self.subMidCtrlKnee.controlGrp,kneePos[0],kneePos[1],kneePos[2],a=True)
        
        pm.parentConstraint(self.subMidCtrlKnee.control,self.ribon45hp.startLoc,mo = 1)
        pm.parentConstraint(self.subMidCtrlKnee.control,self.ribon.endLoc,mo = 1)
        pm.parentConstraint(self.legBlendChain.chain[1],self.subMidCtrlKnee.controlGrp,mo = 1)
        
        #name setting for the scale node for thighKnee Jj1
        thighKneeScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'thighKneeScaleJj1','PMA')
        
        #create Node for  thighKnee Jj1
        #ribbon name for robin
        thighKneeScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = thighKneeScaleNodeNameJj1)
        
        #connect thighKnee scale for  thighKnee Jj1
        self.subMidCtrlThighKnee.control.scaleX.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlKnee.control.scaleX.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlThighKnee.control.scaleY.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlKnee.control.scaleY.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlThighKnee.control.scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlKnee.control.scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        thighKneeScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to thighKnee Jj1
        thighKneeScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon.jj[1].scaleX)
        thighKneeScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon.jj[1].scaleY)
        thighKneeScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon.jj[1].scaleZ)
        
        #name setting for the scale node for thighKnee Jj3
        thighKneeScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'thighKneeScaleJj3','PMA')
        
        #create Node for  thighKnee Jj3
        thighKneeScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = thighKneeScaleNodeNameJj3)
           
        #connect thighKnee scale for  thighKnee Jj3
        
        self.subMidCtrlThighKnee.control.scaleX.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.legBlendChain.chain[1].scaleX.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlThighKnee.control.scaleY.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.legBlendChain.chain[1].scaleY.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlThighKnee.control.scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.legBlendChain.chain[1].scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        thighKneeScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to thighKnee Jj3
        thighKneeScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon.jj[3].scaleX)
        thighKneeScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon.jj[3].scaleY)
        thighKneeScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon.jj[3].scaleZ)
        
        #connect scale to thighKnee jj0
        self.subMidCtrlKnee.control.scaleX.connect(self.ribon.jj[0].scaleX)
        self.subMidCtrlKnee.control.scaleY.connect(self.ribon.jj[0].scaleY)
        self.subMidCtrlKnee.control.scaleZ.connect(self.ribon.jj[0].scaleZ)
        
        #connect scale to thighKnee jj4
        self.legBlendChain.chain[0].scaleX.connect(self.ribon.jj[4].scaleX)
        self.legBlendChain.chain[0].scaleY.connect(self.ribon.jj[4].scaleY)
        self.legBlendChain.chain[0].scaleZ.connect(self.ribon.jj[4].scaleZ)
        
        
        
        #name setting for the scale node for kneeAnkle Jj1
        kneeAnkleScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'kneeAnkleScaleJj1','PMA')
        
        #create Node for  kneeAnkle jj1
        kneeAnkleScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = kneeAnkleScaleNodeNameJj1)
               
        #connect kneeAnkle scale for kneeAnkle jj1
        self.subMidCtrlKneeAnkle.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlKnee.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlKneeAnkle.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlKnee.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlKneeAnkle.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlKnee.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        kneeAnkleScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to kneeAnkle jj1
        kneeAnkleScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon45hp.jj[1].scaleX)
        kneeAnkleScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon45hp.jj[1].scaleY)
        kneeAnkleScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon45hp.jj[1].scaleZ)
        
        #name setting for the scale node for kneeAnkle Jj3
        kneeAnkleScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'kneeAnkleScaleJj3','PMA')
        
        #create Node for  kneeAnkle jj3
        kneeAnkleScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = kneeAnkleScaleNodeNameJj3)
               
        #connect kneeAnkle scale for kneeAnkle jj3
        self.subMidCtrlKneeAnkle.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.subMidCtrlKnee.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlKneeAnkle.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.subMidCtrlKnee.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlKneeAnkle.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.subMidCtrlKnee.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        kneeAnkleScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to kneeAnkle jj3
        kneeAnkleScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon45hp.jj[3].scaleX)
        kneeAnkleScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon45hp.jj[3].scaleY)
        kneeAnkleScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon45hp.jj[3].scaleZ)
        
        #connect scale to kneeAnkle jj4
        self.subMidCtrlKnee.control.scaleX.connect(self.ribon45hp.jj[4].scaleX)
        self.subMidCtrlKnee.control.scaleY.connect(self.ribon45hp.jj[4].scaleY)
        self.subMidCtrlKnee.control.scaleZ.connect(self.ribon45hp.jj[4].scaleZ)
        
        #connect scale to kneeAnkle jj0
        self.legBlendChain.chain[2].scaleX.connect(self.ribon45hp.jj[0].scaleX)
        self.legBlendChain.chain[2].scaleY.connect(self.ribon45hp.jj[0].scaleY)
        self.legBlendChain.chain[2].scaleZ.connect(self.ribon45hp.jj[0].scaleZ)

    def __editCtrl(self):
        
        control.addFloatAttr(self.config_node.control,['CC'],0,1)         
        self.ikRpPvChain.ikCtrl.control.addAttr('foot_roll',at = 'double',min = 0,max = 0,dv = 0)
        pm.setAttr(self.ikRpPvChain.ikCtrl.control + '.foot_roll',e = 0,channelBox = 1)
        self.ikRpPvChain.ikCtrl.control.foot_roll.lock(1)

        self.ikRpPvChain.ikCtrl.control.addAttr('ball',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_lift',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_straight',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_wiggle',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_spin',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('side',at = 'double',dv = 0,k = 1)
        
        self.ikRpPvChain.ikCtrl.control.addAttr('single_roll',at = 'double',min = 0,max = 0,dv = 0)
        pm.setAttr(self.ikRpPvChain.ikCtrl.control + '.single_roll',e = 0,channelBox = 1)
        self.ikRpPvChain.ikCtrl.control.single_roll.lock(1)     
        
        self.ikRpPvChain.ikCtrl.control.addAttr('ball_roll',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_roll',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('heel_roll',at = 'double',dv = 0,k = 1)        

    def __ikFootSet(self):
        
        #add toe wiggle loc
        toeWiggleLoc = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'toeWiggle','gud'))
        pm.xform(toeWiggleLoc,ws = 1,matrix = self.guides[-1].worldMatrix.get())
        pm.parent(toeWiggleLoc,self.guides[-2])
        
        #ik
        ballIkName = nameUtils.getUniqueName(self.side,'ballSc','iks')
        toeWiggleIKName = nameUtils.getUniqueName(self.side,'toeWiggleSc','iks')
        ballIkHandle,ballIkEffector = pm.ikHandle(sj = self.ikBlendChain.chain[-4],ee = self.ikBlendChain.chain[-3],solver = 'ikSCsolver',n = ballIkName)
        toeIkHandle,toeIkEffector = pm.ikHandle(sj = self.ikBlendChain.chain[-3],ee = self.ikBlendChain.chain[-2],solver = 'ikSCsolver',n = toeWiggleIKName)
        pm.parent(ballIkHandle,self.guides[-1])
        self.ikRpChain.ikHandle.setParent(self.guides[-1])
        self.ikRpPvChain.ikHandle.setParent(self.guides[-1])
        pm.delete(self.ikRpPvChain.ikHandle + '_pointConstraint1')
        pm.parentConstraint(self.ikRpPvChain.ikCtrl.control,self.guides[2],mo = 1)
        
        #node Name
        heelConditionNodeName = nameUtils.getUniqueName(self.side,'Heel','COND')
        ballConditionNodeName = nameUtils.getUniqueName(self.side,'Ball','COND')
        ballRangeNodeName = nameUtils.getUniqueName(self.side,'Ball','RANG')
        ballRangeMultipleNodeName = nameUtils.getUniqueName(self.side,'Ball','MDN')
        ballPlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'Ball','PMA')
        tipRangeNodeName = nameUtils.getUniqueName(self.side,'Tip','RANG')
        tipRangeMultipleNodeName = nameUtils.getUniqueName(self.side,'tipRange','MDN')
        insideConditionNodeName = nameUtils.getUniqueName(self.side,'Inside','COND')
        outsideConditionNodeName = nameUtils.getUniqueName(self.side,'Outside','COND')
        singleBallPlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'singleBall','PMA')
        singleToePlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'singleToe','PMA')
        singleHeelPlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'singleHeel','PMA')        
        
        #create Node
        heelConditionNode = pm.createNode('condition',n = heelConditionNodeName)
        ballConditionNode = pm.createNode('condition',n = ballConditionNodeName)
        ballMultipleNode = pm.createNode('multiplyDivide',n = ballRangeMultipleNodeName)
        ballRangeNode = pm.createNode('setRange',n = ballRangeNodeName)
        ballPlusMinusAverageNode = pm.createNode('plusMinusAverage',n = ballPlusMinusAverageNodeName)
        tipRangeNode = pm.createNode('setRange',n = tipRangeNodeName)
        tipRangeMultipleNode = pm.createNode('multiplyDivide',n = tipRangeMultipleNodeName)
        insideConditionNode = pm.createNode('condition',n = insideConditionNodeName)
        outsideConditionNode = pm.createNode('condition',n = outsideConditionNodeName)
        singleBallPlusMinusAverageNode = pm.createNode('plusMinusAverage',n = singleBallPlusMinusAverageNodeName)        
        singleToePlusMinusAverageNode = pm.createNode('plusMinusAverage',n = singleToePlusMinusAverageNodeName)        
        singleHeelPlusMinusAverageNode = pm.createNode('plusMinusAverage',n = singleHeelPlusMinusAverageNodeName)                
        
        #connecting
        #ball negetive
        self.ikRpPvChain.ikCtrl.control.ball.connect(heelConditionNode.firstTerm)
        self.ikRpPvChain.ikCtrl.control.ball.connect(heelConditionNode.colorIfTrueR)
        self.ikRpPvChain.ikCtrl.control.heel_roll.connect(singleHeelPlusMinusAverageNode.input1D[0])
        heelConditionNode.outColorR.connect(singleHeelPlusMinusAverageNode.input1D[1])
        heelConditionNode.secondTerm.set(0)
        heelConditionNode.operation.set(5)
        heelConditionNode.colorIfFalseR.set(0)
        singleHeelPlusMinusAverageNode.output1D.connect(self.guides[3].rx)
        
        #ball value
        self.ikRpPvChain.ikCtrl.control.ball.connect(ballConditionNode.firstTerm)
        self.ikRpPvChain.ikCtrl.control.ball.connect(ballConditionNode.colorIfTrueR)
        ballConditionNode.secondTerm.set(0)
        ballConditionNode.operation.set(3)
        ballConditionNode.colorIfFalseR.set(0)
        
        #ball lift/straight
        tipRangeNode.minX.set(0)
        tipRangeNode.maxX.set(1)
        ballRangeNode.minX.set(0)
        ballRangeNode.maxX.set(1)
        self.ikRpPvChain.ikCtrl.control.ball.connect(ballRangeNode.valueX)
        self.ikRpPvChain.ikCtrl.control.ball_roll.connect(singleBallPlusMinusAverageNode.input1D[0])
        self.ikRpPvChain.ikCtrl.control.toe_lift.connect(ballRangeNode.oldMinX)
        self.ikRpPvChain.ikCtrl.control.toe_straight.connect(ballRangeNode.oldMaxX)        
        ballRangeNode.outValueX.connect(ballPlusMinusAverageNode.input1D[1])
        ballConditionNode.outColorR.connect(ballMultipleNode.input1X)
        ballMultipleNode.operation.set(1)
        ballPlusMinusAverageNode.operation.set(2)
        ballPlusMinusAverageNode.input1D[0].set(1)
        ballPlusMinusAverageNode.output1D.connect(ballMultipleNode.input2X)
        ballMultipleNode.outputX.connect(singleBallPlusMinusAverageNode.input1D[1])
        singleBallPlusMinusAverageNode.output1D.connect(self.guides[-1].rx)
        
        #toe lift/ straight
        tipRangeNode.minX.set(0)
        tipRangeNode.maxX.set(1)
        self.ikRpPvChain.ikCtrl.control.ball.connect(tipRangeNode.valueX)
        self.ikRpPvChain.ikCtrl.control.toe_lift.connect(tipRangeNode.oldMinX)
        self.ikRpPvChain.ikCtrl.control.toe_straight.connect(tipRangeNode.oldMaxX)
        self.ikRpPvChain.ikCtrl.control.toe_roll.connect(singleToePlusMinusAverageNode.input1D[0])        
        ballConditionNode.outColorR.connect(tipRangeMultipleNode.input1X)
        tipRangeNode.outValueX.connect(tipRangeMultipleNode.input2X)
        tipRangeMultipleNode.outputX.connect(singleToePlusMinusAverageNode.input1D[1])
        singleToePlusMinusAverageNode.output1D.connect(self.guides[-4].rx)
        self.ikRpPvChain.ikCtrl.control.toe_spin.connect(self.guides[-4].ry)
        self.guides.append(toeWiggleLoc)
        pm.parent(toeIkHandle,self.guides[-1])
        self.ikRpPvChain.ikCtrl.control.toe_wiggle.connect(self.guides[-1].rx)
        
        #inside
        self.ikRpPvChain.ikCtrl.control.side.connect(insideConditionNode.firstTerm)
        self.ikRpPvChain.ikCtrl.control.side.connect(insideConditionNode.colorIfTrueR)
        insideConditionNode.operation.set(3)
        insideConditionNode.outColorR.connect(self.guides[-4].rz)
        
        #outside
        self.ikRpPvChain.ikCtrl.control.side.connect(outsideConditionNode.firstTerm)
        self.ikRpPvChain.ikCtrl.control.side.connect(outsideConditionNode.colorIfTrueR)
        outsideConditionNode.operation.set(5)
        outsideConditionNode.outColorR.connect(self.guides[-3].rz)
        
        #default set
        self.ikRpPvChain.ikCtrl.control.toe_lift.set(35)
        self.ikRpPvChain.ikCtrl.control.toe_straight.set(70)
            
    def __cleanUp(self):
        
        #cc grp and v 
        self.cntsGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp')) 
        self.config_node.controlGrp.setParent(self.cntsGrp)
        self.ikRpPvChain.ikCtrl.controlGrp.setParent(self.cntsGrp)
        self.ikRpPvChain.poleVectorCtrl.controlGrp.setParent(self.cntsGrp)
        
        #ccDef grp and v
        self.ccDefGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Def','grp')) 
        self.subMidCtrlKneeAnkle.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlThighKnee.controlGrp.setParent(self.ccDefGrp)
        self.subMidCtrlKnee.controlGrp.setParent(self.ccDefGrp)
#         self.config_node.CC.set(1)
        self.config_node.control.CC.connect(self.ccDefGrp.v)        
        
        #cc hierarchy        
        self.ccDefGrp.setParent(self.cntsGrp)

        self.config_node.control.IKFK.set(1)    
        
        #ribbon hierarchy   
        self.ribon.main.v.set(0)
        self.ribon45hp.main.v.set(0) 
        
        #jj grp
        self.sklGrp = pm.group(self.ikRpChain.stretchStartLoc,self.ikRpPvChain.stretchStartLoc,self.ikRpPvChain.lockUpStartLoc,
                               n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))

        for b in (self.ikRpChain,self.ikRpPvChain,self.ikBlendChain,self.fkChain,self.legBlendChain):
            b.chain[0].setParent(self.sklGrp)
        
        #guide grp
        self.ikRpChain.stretchEndLoc.v.set(0)
        self.guideGrp.v.set(0)

        self.guides[2].v.set(0)       
        
    def buildConnections(self):
        
        #reveice info from incoming package
        if pm.objExists(self.metaMain) == 1:
            
            print ''
            print 'Package from ' + self.metaMain + ' has been received'
            
            pm.select(self.metaMain) 
            headQuarter = pm.selected()[0]
            destinations = []
            moduleGrp = pm.connectionInfo(headQuarter.moduleGrp, destinationFromSource=True)
            
            for tempDestination in moduleGrp:
                destination = tempDestination.split('.')
                destinations.append(destination[0])
                
# [u'asd_CC', u'asd_SKL', u'asd_IK', u'asd_LOC', u'asd_XTR', u'asd_GUD', u'asd_GEO', u'asd_ALL', u'asd_TRS', u'asd_PP']

    #         self.sklGrp.setParent(self.hi.SKL)
    #         self.cntsGrp.setParent(self.hi.CC) 
    #         self.ribon.main.setParent(self.hi.XTR)
    #         self.ribon45hp.main.setParent(self.hi.XTR)
    #         self.guideGrp.setParent(self.hi.GUD)
    #         self.guides[2].setParent(self.hi.IK)
            self.sklGrp.setParent(destinations[1])
            self.cntsGrp.setParent(destinations[0]) 
            self.ribon.main.setParent(destinations[4])
            self.ribon45hp.main.setParent(destinations[4])
            self.guideGrp.setParent(destinations[5])
            self.guides[2].setParent(destinations[2])
            
            print ''
            print 'Info from (' + self.meta + ') has been integrate, ready for next Module'
            print ''
            
        else:
            OpenMaya.MGlobal.displayError('Target :' + self.metaMain + ' is NOT exist')
            
        
        #create package send for next part
        #template:
        #metaUtils.addToMeta(self.meta,'attr', objs)
        metaUtils.addToMeta(self.meta,'controls',[self.config_node.control] + [self.ikChain.ikCtrl.control,self.ikChain.poleVectorCtrl.control]
                             + [fk for fk in self.fkChain.chain])
        metaUtils.addToMeta(self.meta,'moduleGrp',[self.limbGrp])
        metaUtils.addToMeta(self.meta,'chain', [ik for ik in self.ikChain.chain] + [ori for ori in self.limbBlendChain.chain])
        

def getUi(parent,mainUi):
    
    return LegModuleUi(parent,mainUi)

class LegModuleUi(object):
#     baseName = 'leg',side = 'l',size = 1.5,
    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        self.__popuItems = []
        
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
        
        #(self,baseName = 'arm',side = 'l',size = 1.5,
        self.name = pm.text(l = '**** Leg Module ****')       
        self.baseNameT = pm.textFieldGrp(l = 'baseName : ',ad2 = 1,text = 'leg')
        self.sideT = pm.textFieldGrp(l = 'side :',ad2 = 1,text = 'l')
        self.cntSizeBody = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],
                                        ad2 = 1,numberOfFields = 1,value1 = 1)
        
        self.mainMetaNodeN = pm.textFieldGrp(l = 'mainMeta :',ad2 = 1)
        
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance)
        pm.separator(h = 10)
        
        self.__pointerClass = None
        
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
        
    def getModuleInstance(self):
        
        baseNameT = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)
        sideT = pm.textFieldGrp(self.sideT,q = 1,text = 1)
        mainMetaNode = pm.textFieldGrp(self.mainMetaNodeN,q = 1,text = 1)
        
        self.__pointerClass = LegModule(baseName = baseNameT,side = sideT,
                                        metaMain = mainMetaNode)
        return self.__pointerClass             

# import sys
# myPath = 'C:/eclipse/test/OOP/AutoRig'
# 
# if not myPath in sys.path:
#     sys.path.append(myPath)
#     
# import reloadMain
# reload(reloadMain)
# 
# from Modules import legModule
# lg = legModule.LegModule()
# lg.buildGuides()
# lg.build()        
        
                        
