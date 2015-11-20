import pymel.core as pm


from core.utils import nameUtils 

class Template(object):
    
    posArray = [[0,0,0],
                [3,0,0],
                [6,0,0]]
    
    rotArray = [[0,0,0],
                [0,0,0],
                [0,0,0]]
    
    
    baseNames = ["upr_arm","lwr_arm","hand"]
    
    def __init__(self,baseName="limb" ,side="L" ,ctrlColor=6 ,ctrlSize=1,solver = "ikRPsolver",
                 controlOrient = [0,0,0]):
        """
        @param baseName : string, This is the name to be used as a base for all the names
        @param side : string, This is the side that will be used for our controls
        @param ctrlSize : string,the control size
        @param ctrlColor :string , color to apply to the controls
        @param solver: string , the solver to be used,current support:
                             - ikSCsolver : simple chain
                             - ikRPsolver : rotation plane
        
        @param controlOrient : float[3] , what orient to apply to control
        """
        
        self.baseName = baseName
        self.side = side 
        #the size of the handGuides
        self.ctrlSize = ctrlSize
        #the objColor of the handGuides
        self.ctrlColor = ctrlColor
        self.solver = solver
        self.controlOrient = controlOrient
        
        
        self.fkChain = None
        self.ikChain = None
        self.blendChain = None

        self.blendData = None
        
        #grps for parenting
        self.ctrlsParGrp = None
        self.bonesGrp = None
        self.mainGrp = None
        
        #our node for ikfk settings(temp)
        self.configName = nameUtils.getUniqueName(self.baseName, self.side, "CONFIG")
        self.configNode = pm.spaceLocator(n=self.configName)
        
        self.guides = None
        self.guidesGrp = None
        
        #attachments hooks
        self.inHooks = []
        self.outHooks = []
        
        self.__tempSpaceSwitch = None
        self.switchGrp = None
        
    def buildGuides(self):
        """
        This function setups our guide system
        
        WILL PROBABLY BE ANOTHER CLASS WHEN WE EXPAND AS IT'S GOING TO BE COMPLEX
        """
        
        self.guides = []
        
        for i,p in enumerate(self.posArray):
            
            name = nameUtils.getUniqueName(self.baseNames[i],self.side,"GUIDE")
            loc = pm.spaceLocator(n=name)
            loc.t.set(p)
            loc.r.set(self.rotArray[i])
            self.guides.append(loc)
            
        tempGuides = list(self.guides)
        tempGuides.reverse()

        for i in range(len(tempGuides)):
            if i != (len(tempGuides)-1):
                pm.parent(tempGuides[i],tempGuides[i+1])
        
        name = nameUtils.getUniqueName(self.baseName+"_guides",self.side,"grp")
        self.guidesGrp = pm.createNode("transform",n=name)
        
        self.guides[0].setParent(self.guidesGrp)
    
    def build(self,stretch=True):
        """
        This function build's the limbModule (ik,fk,blendchains,squash&stretch)
        """
        guidePos = [x.getTranslation(space="world") for x in self.guides]
        guideRot = [x.getRotation(space = "world") for x in self.guides]
        
        
        self.color()
        self.__cleanUp()

    
    def delete(self):
        pm.delete(self.mainGrp)
        del(self)    
    def deleteGuides(self):
        """
        THis function deletes the guides from the scene
        
        WILL BE CHANGED LATER WHEN WE EXPAND
        """
        pm.delete(self.guidesGrp)
    def __cleanUp(self):
        """
        This function cleans up the created limb by creating grps and parenting the created node to it 
        grps created: bones_grp,ctrls_grp,main_grp
        
        """
        pass
    

# import sys
# myPath = 'C:/eclipse/test/OOP/AutoRig'
# maya.cmds.file(new = 1,f = 1)
# if not myPath in sys.path:    
#     sys.path.append(myPath)  
# 
#      
# import reloadMain
# reload(reloadMain)
# 
# from Ui import buildSessionUi
# bs = buildSessionUi.BuildSessionUi()
# bs.openUi()
#  
# #from Modules import fingerModule
# #fg = fingerModule.FingerModule()
# #fg.buildGuides()
# #fg.build()
#  
# #from Modules import legModule
# #lg = legModule.LegModule()
# #lg.buildGuides()
# #lg.build()        
# 
# #from Modules import headModule
# #hg = headModule.HeadModule()
# #hg.buildGuides()
# #hg.build()
# # [self.SKL,self.CC,self.IK,self.LOC,self.XTR,self.GUD,self.GEO,self.ALL,self.TRS,self.PP])  
# #change select joints radius
# import maya.cmds as mc
# selection = mc.ls(type='joint')
# for x in range (0, len(selection)):
#     selection[x] = mc.setAttr(selection[x]+'.radius',0.3)
#     #selection[x] = mc.setAttr(selection[x]+'.drawStyle',1)
