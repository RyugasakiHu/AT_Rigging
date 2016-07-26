import pymel.core as pm
from Utils import nameUtils,metaUtils
from Modules import control 

class Hierarchy(object):
    '''
    classdocs
    '''

    def __init__(self,side = 'm',size = 1,characterName = None):
        '''
        Constructor
        '''
#         self.baseName = baseName
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
        
        #setGuides
        self.visGuides = None
        
        #set ctrl
        self.visCtrl = None
        self.cogCtrl = None
        self.bodyCtrl = None
        
        #create Meta
        self.meta = metaUtils.createMeta(self.side,self.characterName,1)
        
    def buildGuides(self):
        
        self.visGuides = []
        name = nameUtils.getHierachyName('visibility','gud')
        loc = pm.spaceLocator(n = name)
        self.visGuides.append(loc)

    def build(self):
        
        self.visGuides[0].v.set(0)
        
        #vis cc
        self.visGuidePos = [x.getTranslation(space = 'world') for x in self.visGuides]
        self.visCtrl = control.Control(self.side,'visibility',self.size) 
        self.visCtrl.visCtrl()
        pm.move(self.visCtrl.controlGrp,self.visGuidePos[0])
        control.addFloatAttr(self.visCtrl.control,
                             ['spine_fk_vis','finger_ctrl_vis','facial_mouth_sec_vis','facial_panel'],0,1)
        pm.setAttr(self.visCtrl.control.spine_fk_vis,e = 1,cb = True)
        pm.setAttr(self.visCtrl.control.finger_ctrl_vis,e = 1,cb = True)
        pm.setAttr(self.visCtrl.control.facial_mouth_sec_vis,e = 1,cb = True)
        pm.setAttr(self.visCtrl.control.facial_panel,e = 1,cb = True)
        
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
                
        self.visCtrl.controlGrp.setParent(self.CC)
        self.visGuides[0].setParent(self.GUD)
        
                         
    def __cleanUp(self):
        
#         metaUtils.addToMeta(self.meta,, objs)
        metaUtils.addToMeta(self.meta,'moduleGrp', [self.SKL,self.CC,self.IK,self.LOC,self.XTR,self.GUD,self.GEO,self.ALL,self.TRS,self.PP])  
        metaUtils.addToMeta(self.meta,'controls', [self.cogCtrl.control])
        print ''
        print 'Info : ' + self.meta + ' has been integrate, ready for next module'
        
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
        self.cNameT = pm.textFieldGrp(l = 'characterName : ',ad2 = 1,text = 'test')        
        self.sideT = pm.textFieldGrp(l = 'side :',ad2 = 1,text = 'm')
        self.cntSize = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],
                                        ad2 = 1,numberOfFields = 1,value1 = 3)
        self.tempButton = pm.button(l = 'measure',c = self.__measure)
        
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance)
        pm.separator(h = 10)
        
        self.__pointerClass = None
        
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
    
    def __measure(self,*arg):
        
        sizeOneCtrl = control.Control('m','measureSizeOne',1,'y')
        sizeOneCtrl.circleCtrl()
        sizeFiveCtrl = control.Control('m','measureSizeFive',5,'y')
        sizeFiveCtrl.circleCtrl()
        sizeTenCtrl = control.Control('m','measureSizeTen',10,'y')
        sizeTenCtrl.circleCtrl()
        sizeTwentyCtrl = control.Control('m','measureSizeTwenty',20,'y')
        sizeTwentyCtrl.circleCtrl()
        
        tempGrp = pm.group(empty = 1,n = nameUtils.getUniqueName('m','measure','grp'))
        sizeOneCtrl.controlGrp.setParent(tempGrp)
        sizeFiveCtrl.controlGrp.setParent(tempGrp)
        sizeTenCtrl.controlGrp.setParent(tempGrp)
        sizeTwentyCtrl.controlGrp.setParent(tempGrp)              
        
    def getModuleInstance(self):
        
        cName = pm.textFieldGrp(self.cNameT,q = 1,text = 1)
        side = pm.textFieldGrp(self.sideT,q = 1,text = 1)
        cntSizeV = pm.floatFieldGrp(self.cntSize,q = 1,value1 = 1)
        
        self.__pointerClass = Hierarchy(side,size = cntSizeV,characterName = cName)
        return self.__pointerClass

    
    
        
