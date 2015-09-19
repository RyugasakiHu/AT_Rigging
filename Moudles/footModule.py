import pymel.core as pm
from subModules import fkChain,ikChain,boneChain
from Utils import nameUtils
from Modules import control,hierarchy

class FootModule(object):

    posArray = [[6,2,0],[6,0,2],[6,0,4],[6,0,-1]]
    rotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

    def __init__(self, baseName = 'foot',side = 'l',size = 1.5,
                 controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = side
        
        '''
        self para
        '''
        
        #jj
        self.footChain = None
        
        #cc 
        configName = nameUtils.getUniqueName(self.side,self.baseName,'CONFIG')
        self.config_node = pm.spaceLocator(n = configName)
        
        #guides 
        self.guides = None
        
        #namelist
        self.footNameList = ['ankle','ball','toe','heel']
        
    def buildGuides(self):
        
        self.guides = []
            
        #set pos loc    
        for i,p in enumerate(self.posArray):
            name = nameUtils.getUniqueName(self.side,self.baseName + self.footNameList[i],'gud')
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

    def build(self):
        
        guidePos = [x.getTranslation(space = 'world') for x in self.guides]
        guideRot = [x.getRotation(space = 'world') for x in self.guides]

        #foot jj
        self.footChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.footChain.fromList(guidePos,guideRot)

        for num,joint in enumerate(self.footChain.chain):
            name = nameUtils.getUniqueName(self.side,self.baseName + self.footNameList[num],'jj')
            pm.rename(joint,name)
            
        
        
        
        
        
        
from Modules import legModule,footModule
lg = legModule.LegModule()
ft = footModule.FootModule()
lg.buildGuides()
ft.buildGuides()
lg.build()
ft.build()
