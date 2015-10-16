import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy

class SpineModule(object):

    posSpineArray = [[],[],[]]

    def __init__(self,baseName = 'spine',size = 0.5,):
        
        self.side = 'c'
        self.baseName = baseName 
        self.size = size
        
        self.guideCc = None
        self.guideTrv = None
        self.guideGrp = None
        
        
    def buildGuides(self):
        
        #set hi
        self.hi = hierarchy.Hierarchy(characterName = 'test')
        self.hi.build()        
        
        #build curve
        self.guideCc = pm.curve(d = 3,p = [[0,9.040668,0.0623416],[0,10.507795,0.181759],[0,11.991982,0.164699],
                                         [0,13.322632,-0.108255],[0,14.397388,-0.0570757]],k = [0,0,0,1,2,2,2],
                              n = nameUtils.getUniqueName(self.side,self.baseName,'gud'))
        
        #build Trv
        self.guideTrv = pm.joint(p = [0,0,0])
        moPathName = nameUtils.getUniqueName(self.side,self.baseName,'MOP')
        pm.pathAnimation(self.guideCc,self.guideTrv,fractionMode = 1,follow = 1,followAxis = 'x',upAxis = 'y',worldUpType = 'vector',
                         worldUpVector = [0,1,0],inverseUp = 0,inverseFront = 0,bank = 0,startTimeU = 1,endTimeU = 24,n = moPathName)
        
#         CN_c_spine_0_MOP_uValue.output CN_c_spine_0_MOP.uValue
        moPathNode = pm.select(moPathName)
        moPathNode.output.Disconnect(moPathNode.uValue)
        
        
        
        
        
        
        
        
        #group
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(self.guideCc,n = name)        

    def build(self):
        
        pass
        
            
            
# import maya.cmds as mc
# from see import see
# pathOfFiles = 'C:\Users\UV\Desktop\Rigging workshop/'
# fileType = 'obj'
# files = mc.getFileList(folder = pathOfFiles,fs = '*.%s' % fileType)
# mc.file(new = 1,f = 1)
#  
# if len(files) == 0:
#     mc.warning('no files found')
# else:
#     for fi in files:
#         print pathOfFiles + fi
#         mc.file(pathOfFiles + fi,i = True)
#          
# import sys
# myPath = 'C:/eclipse/test/OOP/AutoRig'
#  
# if not myPath in sys.path:
#     sys.path.append(myPath)    
#      
# import reloadMain
# reload(reloadMain)   
#  
# from Modules import spineModule
# rp = spineModule.SpineModule()
# rp.buildGuides()
# rp.build()         
