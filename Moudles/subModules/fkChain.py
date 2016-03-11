import pymel.core as pm
import boneChain
from maya import cmds , OpenMaya
from Modules import control

class FkChain(boneChain.BoneChain):

    def __init__(self, baseName = 'fk',side = 'm',size = 1.5,fkCcType = 'shape',type = 'fk',pointCnst = 1):
        '''
        Constructor
        '''
        self.baseName = baseName
        self.side = side
        self.size = size
        self.fkType = type
        self.fkCcType = fkCcType
        self.controlsArray = []
        self.pointCnst = pointCnst
#         self.fallOff = fallOff
        self.__acceptedCcTypes = ['shape','cc']
        self.__acceptedFkTypes = ['fk','jj']
                
        self.__checkFkType()
        
        if self.fkType == 'fk':
            boneChain.BoneChain.__init__(self, baseName, side,type = self.fkType)
        
        else :    
            boneChain.BoneChain.__init__(self, baseName, side,type = 'jj')
            
    def fromList(self,posList = [],orientList = [],autoOrient = 1,skipLast = 1,fallOff = 0):
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
        
        self.__addControls(skipLast,fallOff)        
        
        if self.fkCcType == self.__acceptedCcTypes[0]:        
            self.__finalizeFkChainShape()
            
        else:
            self.__finalizeFkChainOriCnst() 
        
    def __addControls(self,skipLast = 1,fallOff = 0):
        
        for num in range(self.chainLength()):
            
            #the last loop condition
            if skipLast == 1:
                if num ==(self.chainLength() - 1):
                    return
            
            #create control for each one    
            cntClass = control.Control(self.side,self.baseName,self.size) 
            cntClass.circleCtrl()            
            
            if fallOff == 1:
                cntClass.control.s.set(float(1 - float((num + 1.0) / 5)),float(1 - float((num + 1.0) / 5)),float(1 - float((num + 1.0) / 5)))
                pm.makeIdentity(cntClass.control,apply = True,t = 0,r = 0,s = 1,n = 0,pn = 1)
                   
            pm.delete(cntClass.control,ch=1)
            #snap to the control
            #que xform
            pm.xform(cntClass.controlGrp,ws = 1,matrix = self.chain[num].worldMatrix.get())
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
            if self.pointCnst == 1:
                pm.pointConstraint(c.control,self.chain[i],mo = 1)

    def __finalizeFkChainShape(self):
        
        reversedList = list(self.controlsArray)
        reversedList.reverse()
          
        #parent shape        
        for num,ctrl in enumerate(self.controlsArray):
            
#             for shape in ctrl.control.getShapes():
#                 pm.parent(shape,self.chain[num],r=1,s=1)
            pm.parent(ctrl.control.getShape(),self.chain[num],r=1,s=1)
            
            #lock and hide
            control.lockAndHideAttr(self.chain[num],["ty","tz","sy","sz",'sx'])
        
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
               
            
