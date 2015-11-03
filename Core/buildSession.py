import os
import pymel.core as pm
import autorig_settings

class BuildSession(object):
    
    def __init__(self):
        
        self.modules = []
        self.__foldersToExclude = ['subModules']
        self.__filesToExclude = ['__init__.py']
        self.__modulesDict = {}
        self.availableModules = []
        self.getAvailableModules()
        
    def getAvailableModules(self):
        
        path = autorig_settings.rootPath + '/Modules/'
        self.__checkPath(path) 
        
    def __checkPath(self,path):
        

        res = os.listdir(path)
        toReturn = []
        
        for obj in res:
             
            if obj not in self.__foldersToExclude and os.path.isdir(path + obj) == 1:
                self.__checkPath(path + '/' + obj)
                 
            if obj.find('.py') != -1 and obj.find('.pyc') == -1 and obj not in self.__filesToExclude:
                if obj.find('reload') == -1:
                    toReturn.append(obj)
                    self.__modulesDict[obj] = path + obj
                    
        self.availableModules += toReturn
                
    def buildGuides(self):
        
        for m in self.modules:
            m.buildGuides()
            
    def build(self):
        
        for m in self.modules:
            m.build()
            
    def buildConnections(self):
        for m in self.modules:
            m.buildConnections()
        
            
            

import maya.cmds as mc
from see import see
mc.file(new = 1,f = 1)        
import sys
myPath = 'C:/eclipse/test/OOP/AutoRig'
if not myPath in sys.path:
    sys.path.append(myPath)        
import reloadMain
reload(reloadMain)
from Core import buildSession
from Modules import hierarchy,headModule,spineModule,fingerModule

bs = buildSession.BuildSession()
hi = hierarchy.Hierarchy(characterName = 'pro')
hd = headModule.HeadModule()
sp = spineModule.SpineModule()
fg = fingerModule.FingerModule()

bs.modules = [hi,hd,sp,fg]
bs.buildGuides()
bs.build()


#from Modules import fingerModule
#fg = fingerModule.FingerModule()
#fg.buildGuides()
#fg.build()

#from Modules import headModule
#hg = headModule.HeadModule()
#hg.buildGuides()
#hg.build()

#from Modules import spineModule
#rp = spineModule.SpineModule()
#rp.buildGuides()
#rp.build()         
        
