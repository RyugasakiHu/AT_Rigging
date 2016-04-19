'''
Created on 2016/4/18

@author: Ryugasaki Hu
'''
import pymel.core as pm
import maya.mel as mel
from Modules.subModules import fkChain,ikChain,boneChain
from Utils import nameUtils,metaUtils
from Modules import control,hierarchy,legModule
from maya import OpenMaya
 
# class ToolModule(object):
#     '''
#     this module include:
#     1.sel skin joint for each meta
#     2.fk chain
#     3.dynamic ik 
#     '''
#  
#     def __init__(self,meta = None):
#         '''
#         Constructor
#         '''
#         
#         self.meta = meta


def getUi(parent,mainUi):
    
    return ToolModuleUi(parent,mainUi)

class ToolModuleUi(object):
    
    '''
    this module include three part:
    1.sel skin joint for each meta
    2.fk chain
    3.dynamic ik 
    '''
    
    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        self.__popuItems = []
        
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
 
        self.name = pm.text(l = '**** Tool Module ****')  
        
        #meta
        self.metaMenu = pm.optionMenu(l = 'meta : ')
        self.__metaSel()  
        self.skinJointB = pm.button(l = 'select Skin Joint',c = self.__selSkinJoint,p = self.mainL)
        pm.separator(h = 10)
        
        #remove this panel
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance,p = self.mainL)
        pm.separator(h = 10)
        
        self.__pointerClass = None
 
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
        
#     ###part start
#     def getModuleInstance(self):
#         
#         metaT = pm.optionMenu(self.metaMenu, q = 1,v = 1)
#         
#         self.__pointerClass = ToolModule(meta = metaT)             
#         
#         return self.__pointerClass
#     ###part end
    
    def __metaSel(self): 
        selStr = pm.ls('*META*',type = 'lightInfo' ) 
        for sel in selStr:
            pm.menuItem(l = sel)          
            
    def __selSkinJoint(self,*args):
        
        metaT = pm.optionMenu(self.metaMenu, q = 1,v = 1)  
        meta = pm.ls(metaT)[0]
        jointStrs = pm.connectionInfo(meta.skinJoint, destinationFromSource=True) 
        pm.select(cl = 1) 
         
        for jointStr in jointStrs : 
            joint = jointStr.split('.') 
            pm.select(joint[0],add = 1)
                
        print 'Skin joint from ' + metaT + ' are ' + str(jointStr.split('.')[0])
        print 'Number of ' + metaT + ' is ' + str(len(jointStr))    
            
            
