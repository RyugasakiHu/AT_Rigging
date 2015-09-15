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
        
        

#         self.ribon = None
#         self.ribon45hp = None
#         
#         self.subMidCtrlThighKnee = None
#         self.subMidCtrlKneeAnkle = None
#         self.subMidCtrlKnee = None
         
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
#         self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
#         self.fkChain.fromList(guidePos,guideRot)
                        
        self.__cleanUp()
    
    def __ikSet(self):
        
        #stretch loc reset
        self.ikRpChain.endLoc.setParent(self.ikRpPvChain.ikCtrl.control)
        
        #reset ik cc
        pm.delete(self.ikRpChain.ikCtrl.controlGrp)
        
        #connect joint stretch
        self.ikRpPvChain.ikCtrl.control.stretch.connect(self.ikRpChain.stretchBlendcolorNode.blender)
        
        #connect ik handle point cnst
        pm.pointConstraint(self.ikRpPvChain.ikCtrl.control,self.ikRpChain.ikHandle,w = 1)
        
        #rename ikRPcc
        pm.rename(self.ikRpPvChain.ikCtrl.control,nameUtils.getUniqueName(self.side,self.baseName + 'ik','cc'))
        pm.rename(self.ikRpPvChain.ikCtrl.controlGrp,nameUtils.getUniqueName(self.side,self.baseName + 'ik','grp'))
        
        #set ikflip
        
        #add ik pv vis
        self.ikRpPvChain.ikCtrl.control.enable_PV.connect(self.ikRpPvChain.poleVectorCtrl.controlGrp.v)
        
    def __cleanUp(self):
        
        #jj grp
        self.sklGrp = pm.group(self.ikRpChain.startLoc,self.ikRpPvChain.startLoc,self.ikRpPvChain.lockUpStartLoc,
                               n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))

        for b in (self.ikRpChain,self.ikRpPvChain,self.ikBlendChain):
            b.chain[0].setParent(self.sklGrp)
            
        #cc grp
        self.ccGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp')) 
        self.config_node.setParent(self.ccGrp)
        self.ikRpPvChain.ikCtrl.controlGrp.setParent(self.ccGrp)
        self.ikRpPvChain.poleVectorCtrl.controlGrp.setParent(self.ccGrp)
        
        
        
        
        
        
                        
