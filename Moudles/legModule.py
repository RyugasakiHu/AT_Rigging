import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy

class LegModule(object):
    
#     posArray = [[6,14,0],[6,8,2],[6,2,0],[6,1,4],[6,1,2],[6,1,-1]]
#     rotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

    posArray = [[6,14,0],[6,8,2],[6,2,0]]
    rotArray = [[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'leg',side = 'l',size = 1.5,
                 controlOrient = [0,0,0], module = 'Leg'):
        
        self.baseName = baseName
        self.side = side
#         self.cntColor = cntColor
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
        self.blendChain = None
        self.blendData = None   
        self.sklGrp = None
        
        #cc
        configName = nameUtils.getUniqueName(self.side,self.baseName,'CONFIG')
        self.config_node = pm.spaceLocator(n = configName)
        self.ccDefGrp = None
        self.ccGrp = None
        
        self.guides = None
        self.guideGrp = None
        
        #ribon
        self.ribon = None
        self.ribon45hp = None
         
        self.subMidCtrlThighKnee = None
        self.subMidCtrlKneeAnkle = None
        self.subMidCtrlKnee = None
         
        self.ribbonData = ['ThighKnee','KneeAnkle','Knee']
        self.legnamelist = ['Thigh','Knee','Ankle']
        
#         self.legnamelist = ['Thigh','Knee','Ankle','Ball','Toe','Heel']
        
        self.hi = None
        
    def buildGuides(self):
        
        self.hi = hierarchy.Hierarchy(characterName = 'test')
        self.hi.build()
        
        self.guides = []
        
        #set pos loc    
        for i,p in enumerate(self.posArray):
            name = nameUtils.getUniqueName(self.side,self.baseName + self.legnamelist[i],'gud')
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
#         pm.parent(self.guides[-1],self.guides[-4]) 
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(self.guides[0],n = name)
        self.guideGrp.v.set(0)
        self.guideGrp.setParent(self.hi.GUD)
            
    def build(self):
        
        guidePos = [x.getTranslation(space = 'world') for x in self.guides]
        guideRot = [x.getRotation(space = 'world') for x in self.guides]
        
        #ikRpPvChain
        self.ikRpPvChain = ikChain.IkChain(self.baseName,self.side,self.size,solver = 'ikRPsolver',type = 'ikRP')
        self.ikRpPvChain.fromList(guidePos,guideRot)

        #ikRpChain
        self.ikRpChain = ikChain.IkChain(self.baseName,self.side,self.size,solver = 'ikRPsolver',type = 'ikNF')
        self.ikRpChain.fromList(guidePos,guideRot)
        
        #ik blend 
        self.ikBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'ik')
        self.ikBlendChain.fromList(guidePos,guideRot)
        self.ikBlendChainData = boneChain.BoneChain.blendTwoChains(self.ikRpChain.chain,self.ikRpPvChain.chain,self.ikBlendChain.chain,
                                                                   self.ikRpPvChain.ikCtrl.control,'enable_PV',self.baseName,self.side)
        
        #ikset
        self.__ikSet()
        
         
        #fk 
        self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkChain.fromList(guidePos,guideRot)
        
        #ori chain
        self.blendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.blendChain.fromList(guidePos,guideRot)
        self.ikBlendChainData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikBlendChain.chain,self.blendChain.chain,
                                                                   self.config_node,'IKFK',self.baseName,self.side)
        
        self.__setRibbonUpper()
        self.__setRibbonLower()
        self.__setRibbonSubMidCc()        
        
        self.__cleanUp()
    
    def __ikSet(self):
        
        #stretch loc reset
        self.ikRpChain.stretchEndLoc.setParent(self.ikRpPvChain.ikCtrl.control)
        
        #reset ik cc
        pm.delete(self.ikRpChain.ikCtrl.controlGrp)
        
        #connect joint stretch
        self.ikRpPvChain.ikCtrl.control.stretch.connect(self.ikRpChain.stretchBlendcolorNode.blender)
        
        #connect ik handle point cnst
        pm.pointConstraint(self.ikRpPvChain.ikCtrl.control,self.ikRpChain.ikHandle,w = 1)
        
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
    
    #set ribbon    
    def __setRibbonUpper(self):
        '''
        this function set ribbon for the Upper 
        '''
        self.ribon = ribbon.Ribbon(RibbonName = self.ribbonData[0],Width = 1.0,Length = 5.0,UVal = 1,VVal = 5,subMid = 1)
        self.ribon.construction()
        
        pm.xform(self.ribon.startloc,ws = 1,matrix = self.blendChain.chain[0].worldMatrix.get())
        pm.xform(self.ribon.endloc,ws = 1,matrix = self.blendChain.chain[1].worldMatrix.get())
        
        pm.parentConstraint(self.blendChain.chain[0],self.ribon.startloc,mo = 1)
        
        self.__subCtrlUpper()
        
    #set ribbon ctrl
    def __subCtrlUpper(self):
        
        #connect scale for ShoulderElbow jj2
        self.subMidCtrlThighKnee = self.ribon.subMidCtrl
        self.subMidCtrlThighKnee.control.scaleX.connect(self.ribon.jj[2].scaleX)
        self.subMidCtrlThighKnee.control.scaleY.connect(self.ribon.jj[2].scaleY)
        self.subMidCtrlThighKnee.control.scaleZ.connect(self.ribon.jj[2].scaleZ)
            
    def __setRibbonLower(self):

        '''
        this function set ribbon for the ShoulderElbow 
        '''
        
        self.ribon45hp = ribbon.Ribbon(RibbonName = self.ribbonData[1],Width = 1.0,Length = 5.0,UVal = 1,VVal = 5,subMid = 1)
        self.ribon45hp.construction()
        
        pm.xform(self.ribon45hp.startloc,ws = 1,matrix = self.blendChain.chain[1].worldMatrix.get())
        pm.xform(self.ribon45hp.endloc,ws = 1,matrix = self.blendChain.chain[2].worldMatrix.get())
        
        pm.parentConstraint(self.blendChain.chain[2],self.ribon45hp.endloc,mo = 1)
                
        self.__subCtrlLower()
    
    def __subCtrlLower(self):
        
        #connect scale for mid jj
        self.subMidKneeAnkle = self.ribon45hp.subMidCtrl
        self.subMidKneeAnkle.control.scaleX.connect(self.ribon45hp.jj[2].scaleX)
        self.subMidKneeAnkle.control.scaleY.connect(self.ribon45hp.jj[2].scaleY)
        self.subMidKneeAnkle.control.scaleZ.connect(self.ribon45hp.jj[2].scaleZ)

    def __setRibbonSubMidCc(self):
        pass
    
    def __cleanUp(self):
        
        #jj grp
        self.sklGrp = pm.group(self.ikRpChain.stretchStartLoc,self.ikRpPvChain.stretchStartLoc,self.ikRpPvChain.lockUpStartLoc,
                               n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))

        for b in (self.ikRpChain,self.ikRpPvChain,self.ikBlendChain,self.fkChain,self.blendChain):
            b.chain[0].setParent(self.sklGrp)
        
        self.sklGrp.setParent(self.hi.SKL)
            
        #cc grp
        self.ccGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp')) 
        self.config_node.setParent(self.ccGrp)
        self.ikRpPvChain.ikCtrl.controlGrp.setParent(self.ccGrp)
        self.ikRpPvChain.poleVectorCtrl.controlGrp.setParent(self.ccGrp)
        self.ccGrp.setParent(self.hi.CC)
        
        #ik grp
        self.ikRpChain.ikHandle.setParent(self.hi.IK)
        self.ikRpPvChain.ikHandle.setParent(self.hi.IK)
        
        
        
        
                        
