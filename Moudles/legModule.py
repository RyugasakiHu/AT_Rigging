import pymel.core as pm
from subModules import fkChain,ikChain,boneChain
from Utils import nameUtils
from Modules import control,hierarchy

class FootModule(object):

    posArray = [[6,2,0],[6,0,-1],[6,0,4],[4,0,2],[8,0,2],[6,0,2]]
    rotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self, baseName = 'foot',side = 'l',size = 1.5,
                 controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = side
        self.size = size
        
        '''
        self para
        '''
        
        #jj
        self.footChain = None
        self.sklGrp = None
        
        #cc 
        self.footCtrl = None
        
        #guides 
        self.guides = None
        
        #namelist
        self.footNameList = ['ankle','heel','toe','inside','outside','ball']
        
    def buildGuides(self):
        
        self.guides = []
        
        #set loc pos
        for i,p in enumerate(self.posArray):
            locName = nameUtils.getUniqueName(self.side,self.footNameList[i],'loc')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(p)
            self.guides.append(loc)        
         
        tempGuides = list(self.guides)
        tempGuides.reverse()
         
        for i in range(len(tempGuides)):
            if i != (len(tempGuides) - 1):
                pm.parent(tempGuides[i],tempGuides[i + 1])
         
    def build(self):
        
        guidePos = [x.getTranslation(space = 'world') for x in self.guides[0],self.guides[-1],self.guides[2],self.guides[1]]
        guideRot = [x.getRotation(space = 'world') for x in self.guides[0],self.guides[-1],self.guides[2],self.guides[1]]

        #foot jj
        self.footChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.footChain.fromList(guidePos,guideRot)

        for num,joint in enumerate(self.footChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footGudNameList[num],'jj')
            pm.rename(joint,name)
        
        self.footChain.chain[-1].setParent(self.footChain.chain[0])
        self.__addCtrl()
#         self.__cleanUp()

    def __addCtrl(self):
        
#         ccName = nameUtils.getUniqueName(self.side,self.baseName,'CONFIG')
        self.footCtrl = control.Control(self.side,self.baseName,self.size) 
        self.footCtrl.circleCtrl()
        self.footCtrl.control.rotateZ.set(90)
        pm.makeIdentity(apply = 1,t = 0,r = 1,s = 0,pn = 1)
        pm.xform(self.footCtrl.controlGrp,ws = 1,matrix = self.guides[0].worldMatrix.get())
    

        
    def __cleanUp(self):
        
        #jj grp 
        self.footChain.chain[0].setParent(self.footCtrl.control)
        
        #gud grp
        self.guideGrp.v.set(0)

        
        
        
        
# from Modules import legModule,footModule
# lg = legModule.LegModule()
# ft = footModule.FootModule()
# lg.buildGuides()
# ft.buildGuides()
# lg.build()
# ft.build()
