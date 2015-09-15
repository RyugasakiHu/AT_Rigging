import pymel.core as pm
from Utils import nameUtils
from Modules import control

class Hierarchy(object):
    '''
    classdocs
    '''

    def __init__(self, characterName):
        '''
        Constructor
        '''
        self.characterName = characterName
        
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
        self.GEO = None
        self.GUD = None

        self.cogCtrl = None
        
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
        
        #set cog
        self.cogCtrl = control.Control(side = 'c',baseName = self.characterName ,size = 1)
        self.cogCtrl.cogCtrlTest()
        self.cogCtrl.control.setParent(self.ALL)
        
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
