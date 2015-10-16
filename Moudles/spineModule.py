import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy

class MyClass(object):

    posSpineArray = [[],[],[]]

    def __init__(self,baseName = 'finger',size = 0.5,):
        
        self.baseName = baseName 
        self.size = size
        
        self.guide = None
        
        
    def buildGuides(self):
        
        #build curve
        self.guide = pm.curve()
        
        #

        
