import pymel.core as pm
from subModules import fkChain,ikChain,boneChain
from Utils import nameUtils
from Modules import control,hierarchy,legModule

class HeadModule(object):

    neckPosArray = [[0,14.25,-0.1],[0,14.77,0],[0,15,0.07],[0,15.355,0.236]]
    neckRotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self, baseName = 'foot',size = 1.5,
                 controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = ['r','m','l']
        self.size = size
        
        #jj
        self.neckChain = None
        self.sklGrp = None
        
        #cc 
#         self.footCtrl = None
        
        #guides 
        self.neckGuides = None
        
        #namelist
        self.nameList = ['neck','head']
        
    def buildGuides(self):
        
        self.neckGuides = []
        
        #build neck guides
        #set loc pos
        for num,pos in enumerate(self.neckPosArray):
            if num != len(self.neckPosArray) - 1:
                locName = nameUtils.getUniqueName(self.side[1],self.nameList[0],'gud')
            else :
                locName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.neckGuides.append(loc)        
         
        tempNeckGuides = list(self.neckGuides)
        tempNeckGuides.reverse()
         
        for i in range(len(tempNeckGuides)):
            if i != (len(tempNeckGuides) - 1):
                pm.parent(tempNeckGuides[i],tempNeckGuides[i + 1])
         
    def build(self):
        
        self.neckGuidePos = [x.getTranslation(space = 'world') for x in self.neckGuides]
        self.neckGuideRot = [x.getRotation(space = 'world') for x in self.neckGuides]

        #foot jj
#         self.footChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
#         self.footChain.fromList(self.guidePos,self.guideRot)
# 
#         for num,joint in enumerate(self.footChain.chain):
#             name = nameUtils.getUniqueName(self.side,self.footNameList[num],'jj')
#             pm.rename(joint,name)
#         
#         self.footChain.chain[-1].setParent(self.footChain.chain[0])
#         self.__addCtrl()
#         self.__connectAttr()
#         self.__cleanUp()

    def __addCtrl(self):
        pass
    
    def __connectAttr(self):
        
        pass
    
    def __cleanUp(self):
        
        pass

        
        
        
        
# from Modules import legModule,footModule
# hg = headModule.HeadModule()
# hg.buildGuides()
# hg.build()
