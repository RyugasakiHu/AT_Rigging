import pymel.core as pm
import boneChain
from maya import cmds , OpenMaya
from Modules import control

class FkChain(boneChain.BoneChain):

    def __init__(self, baseName = 'fk',side = 'm',size = 1.5,fkCcType = 'shape',type = 'fk'):
        '''
        Constructor
        '''
        self.baseName = baseName
        self.side = side
        self.size = size
        self.fkCcType = fkCcType
        self.controlsArray = []
        self.fkType = type
        self.__acceptedCcTypes = ['shape','cc']
        self.__acceptedFkTypes = ['fk','jj']
                
        self.__checkFkType()
        
        if self.fkType == 'fk':
            boneChain.BoneChain.__init__(self, baseName, side,type = self.fkType)
        
        else :    
            boneChain.BoneChain.__init__(self, baseName, side,type = 'jj')
            
    def fromList(self,posList = [],orientList = [],autoOrient = 1,skipLast = 1):
        '''
        posList position
        orientList orient
        autoOrient bool whether use autoOrient List or not
        skipLast =whether add the last jj cc
        '''
        
        res = self.__checkCcType()
        if not res :
            return
        
        boneChain.BoneChain.fromList(self, posList, orientList, autoOrient)
        
        self.__addControls(skipLast)        
        
        if self.fkCcType == self.__acceptedCcTypes[0]:        
            self.__finalizeFkChainShape()
            
        else:
            self.__finalizeFkChainOriCnst() 
        
    def __addControls(self,skipLast = 1):
        
        for i in range(self.chainLength()):
            #the last loop condition
            if skipLast == 1:
                if i ==(self.chainLength() - 1):
                    return
            #create control for each one    
            cntClass = control.Control(self.side,self.baseName,self.size) 
            cntClass.circleCtrl()
            
            #snap to the control
            #que xform
            pm.xform(cntClass.controlGrp,ws = 1,matrix = self.chain[i].worldMatrix.get())
            
            self.controlsArray.append(cntClass)                                
            
    def __finalizeFkChainOriCnst(self):        
           
        reversedList = list(self.controlsArray)
        reversedList.reverse()
           
        for i in range(len(reversedList)):
            if i != (len(reversedList)-1):
                pm.parent(reversedList[i].controlGrp,reversedList[i+1].control)    
        #orient cnst        
        for i,c in enumerate(self.controlsArray):
            pm.orientConstraint(c.control,self.chain[i],mo = 1)

    def __finalizeFkChainShape(self):
        
        reversedList = list(self.controlsArray)
        reversedList.reverse()
          
        #parent shape        
        for i,c in enumerate(self.controlsArray):
            pm.parent(c.control.getShape(),self.chain[i],r=1,s=1)
            
            #lock and hide
            control.lockAndHideAttr(self.chain[i],["tx","ty","tz","sy","sz"])
        
        #delete grp   
        for i in range(len(reversedList)):
            pm.delete(reversedList[i].controlGrp)         
            
    def __checkCcType(self):
        '''
        whether the Cc is valid
        @return:bool
        '''                 
        
        if not self.fkCcType in self.__acceptedCcTypes :
            OpenMaya.MGlobal.displayError('plz provide a valid type , accept value are :' + ','.join(self.__acceptedCcTypes))
            return False
        return True            
    
    def __checkFkType(self):
        '''
        whether the fkJj is valid
        @return:bool
        '''                 
        
        if not self.fkType in self.__acceptedFkTypes :
            OpenMaya.MGlobal.displayError('plz provide a valid type , accept value are :' + ','.join(self.__acceptedFkTypes))
            return False
        return True          
        
         
# from Modules.subModules import fkChain
# bc = fkChain.FkChain()
# bc.fromList([[0,0,0],[4,0,2],[8,0,0]],autoOrient = 1) 
               
            
