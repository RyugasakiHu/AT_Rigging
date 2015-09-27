import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy,limbModule

class FingerModule(object):
    
    posIndexArray = [[20,12,1],[23,12,1],[25,12,1],[27,12,1]]
    posMiddleArray = [[20,12,0],[23,12,0],[25,12,0],[28,12,0]]
    posRingArray = [[20,12,-1],[23,12,-1],[25,12,-1],[27,12,-1]]
    posPinkyArray = [[20,12,-2],[23,12,-2],[25,12,-2],[26,12,-2]]
    
    rotIndexArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotMiddleArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotRingArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotPinkyArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'finger',side = 'l',size = 0.5,controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = side
        self.size = size
        self.controlOrient = controlOrient
        
        #guides 
        self.guides = None
        self.guideGrp = None        
        
        #cc
        self.config_node = None
            
        #nameList
        self.fingerName = ['thumb','index','middle','ring','pinky']
        self.fingerJoint = ['Root','Tip','Mid','End','Partial']
        
    def buildGuides(self):
        
        self.guides = []
        self.guideGrp = []
        
        self.indexGuides = []
        self.middleGuides = []
        self.ringGuides = []
        self.pinkyGuides = []
            
        #index    
        for num,obj in enumerate(self.posIndexArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotIndexArray[num])
            self.indexGuides.append(loc)
            
        self.tempIndexGuides = list(self.indexGuides)
        self.tempIndexGuides.reverse()
        for i in range(len(self.tempIndexGuides)):
            if i != (len(self.tempIndexGuides) - 1):
                pm.parent(self.tempIndexGuides[i],self.tempIndexGuides[i + 1])
        self.tempIndexGuides.reverse()
        self.guides.append(self.tempIndexGuides[0])
        
        #middle
        for num,obj in enumerate(self.posMiddleArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotMiddleArray[num])
            self.middleGuides.append(loc)
            
        self.tempMiddleGuides = list(self.middleGuides)
        self.tempMiddleGuides.reverse()
        for i in range(len(self.tempMiddleGuides)):
            if i != (len(self.tempMiddleGuides) - 1):
                pm.parent(self.tempMiddleGuides[i],self.tempMiddleGuides[i + 1])
        self.tempMiddleGuides.reverse()   
        self.guides.append(self.tempMiddleGuides[0])        
        
        #ring 
        for num,obj in enumerate(self.posRingArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotRingArray[num])
            self.ringGuides.append(loc)
            
        self.tempRingGuides = list(self.ringGuides)
        self.tempRingGuides.reverse()
        for i in range(len(self.tempRingGuides)):
            if i != (len(self.tempRingGuides) - 1):
                pm.parent(self.tempRingGuides[i],self.tempRingGuides[i + 1])
        self.tempRingGuides.reverse()   
        self.guides.append(self.tempRingGuides[0])            
        
        #pinky 
        for num,obj in enumerate(self.posPinkyArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotPinkyArray[num])
            self.pinkyGuides.append(loc)
            
        self.tempPinkyGuides = list(self.pinkyGuides)
        self.tempPinkyGuides.reverse()
        for i in range(len(self.tempPinkyGuides)):
            if i != (len(self.tempPinkyGuides) - 1):
                pm.parent(self.tempPinkyGuides[i],self.tempPinkyGuides[i + 1])
        self.tempPinkyGuides.reverse()   
        self.guides.append(self.tempPinkyGuides[0])            
        
        #guide grp       
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp') 
        self.guideGrp = pm.group(self.tempIndexGuides[0],self.tempMiddleGuides[0],
                                 self.tempRingGuides[0],self.tempPinkyGuides[0],n = name)
        
        #connect to the 
        self.lm = limbModule.LimbModule()
        self.lm.buildGuides()
        
    def build(self):
        
        self.lm.build()  
        
        #index info
        self.guideIndexPos = [x.getTranslation(space = 'world') for x in self.indexGuides]
        self.guideIndexRot = [x.getRotation(space = 'world') for x in self.indexGuides]
        
        #fk test
        self.fkIndexChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkIndexChain.fromList(self.guideIndexPos,self.guideIndexRot)        
        
        self.__handAttr()
        
    def __handAttr(self):
           
        #set cc
        pm.addAttr(self.lm.config_node.control,ln = '___',at = 'enum',en = 'HandDrives:')
        pm.setAttr(self.lm.config_node.control + '.___',e = 1,channelBox = 1)
        
        #add attr
        control.addFloatAttr(self.lm.config_node.control,['fist_a','firs_b','relax_a','relax_b','relax_c',
                                                          'relax_d','relax_e','grab_a','grab_b''spread_a',
                                                          'spread_b','hand','plam_a','plam_b','thumb_a',
                                                          'thumb_b','index','middle','ring','pinky','point'],-3,10)

        
          
        
# maya.cmds.file(new = 1,f = 1)
# import sys
# myPath = 'C:/eclipse/test/OOP/AutoRig'
# 
# if not myPath in sys.path:
#     sys.path.append(myPath)
#     
# import reloadMain
# reload(reloadMain)
# 
# from Modules import fingerModule
# fg = fingerModule.FingerModule()
# fg.buildGuides()
# fg.build()

        
        
        
