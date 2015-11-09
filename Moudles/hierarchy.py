import pymel.core as pm
from Utils import nameUtils,metaUtils
from Modules import control,limbModule

class Hierarchy(object):
    '''
    classdocs
    '''

    def __init__(self, baseName = 'main',side = 'm',size = 1,characterName = None):
        '''
        Constructor
        '''
        self.baseName = baseName
        self.side = side
        self.size = size
        self.characterName = characterName
        
        #get papare for class
        self.ALL = None
        self.TRS_cc = None
        self.TRS = None
        self.PP = None
        self.SKL = None
        self.CC = None
        self.IK = None
        self.LOC = None
        self.GEO = None
        self.XTR = None
        self.CSG = None
        self.GUD = None

        #set ctrl
        self.cogCtrl = None
        self.bodyCtrl = None
        
        #create Meta
        self.meta = metaUtils.createMeta(self.side,self.baseName,1)
        
    def buildGuides(self):
        
        pass    
        
    def build(self):
        
        #build grp
        self.ALL = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'ALL')) 
        self.TRS = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'TRS')) 
        self.PP = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'PP')) 
        self.SKL = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'SKL')) 
        self.CC = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'CC')) 
        self.IK = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'IK')) 
        self.LOC = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'LOC')) 
        self.GEO = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'GEO')) 
        self.XTR = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'XTR')) 
        self.CSG = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'CSG'))
        self.GUD = pm.group(empty = 1,n = nameUtils.getHierachyName(self.characterName,'GUD'))
        
        #set ctrl
        #set cog
        self.cogCtrl = control.Control(side = 'm',baseName = self.characterName ,size = self.size,aimAxis = 'y')
#         self.cogCtrl.cogCtrlTest()
        self.cogCtrl.circleCtrl()
        self.cogCtrl.controlGrp.setParent(self.ALL)        
        
        #set grp 
        self.TRS.setParent(self.cogCtrl.control)
        self.PP.setParent(self.TRS)
        self.CSG.setParent(self.TRS)
        self.SKL.setParent(self.PP)
        self.CC.setParent(self.PP)
        self.IK.setParent(self.PP)
        self.LOC.setParent(self.PP)
        self.GEO.setParent(self.ALL)
        self.XTR.setParent(self.ALL)
        self.GUD.setParent(self.ALL)
        
        #clean up
        self.__cleanUp()
        
    def buildConnections(self):
                
        pass
                         
    def __cleanUp(self):
        
#         metaUtils.addToMeta(self.meta,, objs)
        print 'perpare meta is : ' + self.meta
        metaUtils.addToMeta(self.meta,'moduleGrp', [self.ALL,self.TRS,self.PP,self.SKL,self.CC,self.IK,self.LOC,self.GEO,self.GUD])  
        metaUtils.addToMeta(self.meta,'controls', [self.cogCtrl.control])    
        
#         metaUtils.addToMeta(self.meta,, objs)
#         metaUtils.addToMeta(self.meta,, objs)
#         metaUtils.addToMeta(self.meta,, objs)
#         metaUtils.addToMeta(self.meta,, objs)
#         metaUtils.addToMeta(self.meta,, objs)
#         metaUtils.addToMeta(self.meta,, objs)
#         metaUtils.addToMeta(self.meta,, objs)

def getUi(parent,mainUi):
    
    return MainModuleUi(parent,mainUi)

class MainModuleUi(object):
    
    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
        
        
        #(self, baseName = 'main',side = 'm',size = 1,characterName = None):
        self.name = pm.text(l = '**** Main Module ****')
        self.cNameT = pm.textFieldGrp(l = 'characterName : ',ad2 = 1)        
        self.baseNameT = pm.textFieldGrp(l = 'baseName : ',ad2 = 1)
        self.sideT = pm.textFieldGrp(l = 'side :',ad2 = 1)
        self.cntSize = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],
                                        ad2 = 1,numberOfFields = 1,value1 = 1)
        
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance)
        pm.separator(h = 10)
        
        self.__pointerClass = None
        
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
        
    def getModuleInstance(self):
        
        baseName = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)
        cName = pm.textFieldGrp(self.cNameT,q = 1,text = 1)
        side = pm.textFieldGrp(self.sideT,q = 1,text = 1)
        cntSizeV = pm.floatFieldGrp(self.cntSize,q = 1,value1 = 1)
        
        self.__pointerClass = Hierarchy(baseName,side,size = cntSizeV,characterName = cName)
        return self.__pointerClass

    
    
        
