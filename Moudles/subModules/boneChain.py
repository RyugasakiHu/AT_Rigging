import pymel.core as pm
from Utils import nameUtils

class BoneChain(object):
    
#     def __init__(self, baseName = 'chain',side = 'c'):
    def __init__(self,baseName,side,type):
        '''
        Constructor
        '''
        self.baseName = baseName
        self.side = side
        self.type = type
        
        self.chain = []
        
    def fromList(self,posList = [],orientList = [],autoOrient = 1):
        
        for i in range(len(posList)):
            
            tempName = nameUtils.getUniqueName(self.side,self.baseName,self.type)
            if i == len(posList) - 1:
                tempName = nameUtils.getUniqueName(self.side,self.baseName,self.type)
                
            pm.select(cl = 1)
            
            if autoOrient == 1:
                
                tempJnt = pm.joint(n = tempName,position = posList[i])
                
            else :
                tempJnt = pm.joint(n = tempName,position = posList[i],orientation = orientList[i])
            
            self.chain.append(tempJnt)
        self.__parentJoints()
         
        if autoOrient == 1:
            #pm.joint(self.chain[0].name(),e = 1,oj = 'yzx',secondaryAxisOrient = 'zup',ch = 1)
             
            pm.joint(self.chain[0].name(),e = 1,oj = 'xyz',secondaryAxisOrient = 'zdown',ch = 1)
            #xzy -secondaryAxisOrient ydown -ch -zso;
             
        self.__zeroOrientJoint(self.chain[-1])

    def chainLength(self):
        'return length'
         
        return len(self.chain)
    
    def __str__(self):
        
        result = 'BoneChain class , length : {l}, chain : '.format(l = self.chainLength()) 
        chainName = [obj.name() for obj in self.chain]        
        result += str(chainName)
        
        return result

    def __zeroOrientJoint(self,bone):
        'zero out the jointOrient'
        for a in ['jointOrientX','jointOrientY','jointOrientZ']:
            bone.attr(a).set(0)     
                    
    
    def __parentJoints(self):
        'parent a list of joints'
        reversedList = list(self.chain)
        reversedList.reverse()
         
        for i in range(len(reversedList)):
            if i != (len(reversedList)-1):
                pm.parent(reversedList[i],reversedList[i+1])
    
    @staticmethod           
    def blendTwoChains(chain1,chain2,resChain,attrHolder,attrName,baseName,side):
        
        blnTArray = []
        blnRArray = []
        blnSArray = []
        
        data = {'blendTranslate':blnTArray,
                'blendRotate':blnRArray,
                'blendScale':blnSArray
                }
        
        if attrHolder.hasAttr(attrName) == 0:
            attrHolder.addAttr(attrName,at = 'float',min = 0,max = 1,dv = 0,k = 1)
            
        for i,b in enumerate(resChain):
            
            blnT = nameUtils.getUniqueName(side,baseName + 'Tra','BCN')    
            blnR = nameUtils.getUniqueName(side,baseName + 'Rot','BCN') 
            blnS = nameUtils.getUniqueName(side,baseName + 'Sca','BCN') 
            
            if not blnT or not blnR or not blnS:
                return
            
            blnNodeT = pm.createNode('blendColors', n = blnT)
            blnNodeR = pm.createNode('blendColors', n = blnR)
            blnNodeS = pm.createNode('blendColors', n = blnS)
            
            chain1[i].t.connect(blnNodeT.color2)
            chain2[i].t.connect(blnNodeT.color1)
            
            chain1[i].r.connect(blnNodeR.color2)
            chain2[i].r.connect(blnNodeR.color1)
            
            chain1[i].s.connect(blnNodeS.color2)
            chain2[i].s.connect(blnNodeS.color1)
        
            blnNodeT.output.connect(b.t)
            blnNodeS.output.connect(b.s)
            blnNodeR.output.connect(b.r)
        
            blnTArray.append(blnNodeT)
            blnRArray.append(blnNodeR)
            blnSArray.append(blnNodeS)
            
            attrHolder.attr(attrName).connect(blnNodeT.blender)
            attrHolder.attr(attrName).connect(blnNodeR.blender)
            attrHolder.attr(attrName).connect(blnNodeS.blender)
        
        return data
        
# from Modules.subModule import boneChain
# bc = boneChain.BoneChain()
# bc.fromList([[x,x,0] for x in range(10)],autoOrient = 1)  
                
        
#from module import boneChain
#bc = boneChain.BoneChain()
#bc.fromList([[x,x,0] for x in range(10)],[[90,0,0] for x in range(10)],autoOrient = 1)              
                        
