import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy,limbModule
from see import see

class FingerModule(object):
    
    posIndexArray = [[6.58,14.03,-0.04],[6.94,14.03,-0.04],[7.3,14.03,-0.04],[7.515,14.03,-0.04],[7.74,14.03,-0.04]]
    posMiddleArray = [[6.539,14.05,-0.22],[6.9,14.05,-0.22],[7.361,14.05,-0.22],[7.58,14.05,-0.22],[7.88,14.05,-0.22]]
    posRingArray = [[6.58,14.055,-0.413],[6.94,14.055,-0.413],[7.3,14.055,-0.413],[7.515,14.055,-0.413],[7.74,14.055,-0.413]]
    posPinkyArray = [[6.746,14.03,-0.585],[6.94,14.03,-0.585],[7.134,14.03,-0.585],[7.276,14.03,-0.585],[7.5,14.03,-0.585]]
    
    rotIndexArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotMiddleArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotRingArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotPinkyArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'finger',side = 'l',size = 0.5,controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = side
        self.size = size
        self.controlOrient = controlOrient
        
        #guides 
        self.guides = None
        self.guideGrp = None        
        
        #cc
        self.config_node = None
        self.indexSDK = []
            
        #nameList
        self.fingerName = ['thumb','index','middle','ring','pinky']
        self.fingerJoint = ['Base','Root','Tip','Mid','End','Partial']
        
    def buildGuides(self):
        
        self.guides = []
        self.guideGrp = []
        
        self.indexGuides = []
        self.middleGuides = []
        self.ringGuides = []
        self.pinkyGuides = []
            
        #index    
        for num,obj in enumerate(self.posIndexArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotIndexArray[num])
            self.indexGuides.append(loc)
            
        self.tempIndexGuides = list(self.indexGuides)
        self.tempIndexGuides.reverse()
        for i in range(len(self.tempIndexGuides)):
            if i != (len(self.tempIndexGuides) - 1):
                pm.parent(self.tempIndexGuides[i],self.tempIndexGuides[i + 1])
        self.tempIndexGuides.reverse()
        self.guides.append(self.tempIndexGuides[0])
        
        #middle
        for num,obj in enumerate(self.posMiddleArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotMiddleArray[num])
            self.middleGuides.append(loc)
             
        self.tempMiddleGuides = list(self.middleGuides)
        self.tempMiddleGuides.reverse()
        for i in range(len(self.tempMiddleGuides)):
            if i != (len(self.tempMiddleGuides) - 1):
                pm.parent(self.tempMiddleGuides[i],self.tempMiddleGuides[i + 1])
        self.tempMiddleGuides.reverse()   
        self.guides.append(self.tempMiddleGuides[0])        
         
        #ring 
        for num,obj in enumerate(self.posRingArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotRingArray[num])
            self.ringGuides.append(loc)
             
        self.tempRingGuides = list(self.ringGuides)
        self.tempRingGuides.reverse()
        for i in range(len(self.tempRingGuides)):
            if i != (len(self.tempRingGuides) - 1):
                pm.parent(self.tempRingGuides[i],self.tempRingGuides[i + 1])
        self.tempRingGuides.reverse()   
        self.guides.append(self.tempRingGuides[0])            
         
        #pinky 
        for num,obj in enumerate(self.posPinkyArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotPinkyArray[num])
            self.pinkyGuides.append(loc)
             
        self.tempPinkyGuides = list(self.pinkyGuides)
        self.tempPinkyGuides.reverse()
        for i in range(len(self.tempPinkyGuides)):
            if i != (len(self.tempPinkyGuides) - 1):
                pm.parent(self.tempPinkyGuides[i],self.tempPinkyGuides[i + 1])
        self.tempPinkyGuides.reverse()   
        self.guides.append(self.tempPinkyGuides[0])            
        
        #guide grp       
        guideName = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
#         self.guideGrp = pm.group(self.tempIndexGuides[0],n = guideName) 
        self.guideGrp = pm.group(self.tempIndexGuides[0],self.tempMiddleGuides[0],
                                 self.tempRingGuides[0],self.tempPinkyGuides[0],n = guideName)

        self.guideGrp.v.set(0)
        
        #connect to the limb
        self.lm = limbModule.LimbModule()
        self.lm.buildGuides()
        
    def build(self):
        
        self.lm.build()  
        #build index
        #index info
        self.guideIndexPos = [x.getTranslation(space = 'world') for x in self.indexGuides]
        self.guideIndexRot = [x.getRotation(space = 'world') for x in self.indexGuides]
        
        #fk test
        self.indexBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.indexBlendChain.fromList(self.guideIndexPos,self.guideIndexPos)
                                   
        self.__handAttr()
        self.__fingerCC()
        self.__setSDK()
#         self.__nodeConnect()
        
    def __handAttr(self):
           
        #set cc
        pm.addAttr(self.lm.config_node.control,ln = '___',at = 'enum',en = 'HandDrives:')
        pm.setAttr(self.lm.config_node.control + '.___',e = 1,channelBox = 1)
        
        #add attr
        control.addFloatAttr(self.lm.config_node.control,['fist_a','firs_b','relax_a','relax_b','relax_c',
                                                          'relax_d','relax_e','grab_a','grab_b','spread_a',
                                                          'spread_b','hand','plam_a','plam_b','thumb_a',
                                                          'thumb_b','index_curl','middle_curl','ring_curl',
                                                          'pinky_curl','point'],-3,10)

    def __fingerCC(self):
        
        self.indexSDK = []
        
        for num,indexJoint in enumerate(self.indexBlendChain.chain):
            if num < self.indexBlendChain.chainLength() - 1:
                #correct jj name
                pm.rename(indexJoint,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'jj'))
                
                #create sdk and correct cc name
                cc = control.Control(self.side,self.baseName,size = indexJoint.getRadius() / 5) 
                cc.circleCtrl()
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'SDK'))
                self.indexSDK.append(cc.controlGrp)
                
                #align cc grp
                pm.xform(cc.controlGrp,ws = 1,matrix = indexJoint.worldMatrix.get())
                
                #parent jj
                cc.controlGrp.setParent(indexJoint)
                self.indexBlendChain.chain[num + 1].setParent(cc.control)   
                             
        print self.indexSDK
           
    def __setSDK(self):
        
        #set defaut sdk
        for SDK in self.indexSDK:
            for vec in ['t','r']:
                for ch in ['x','y','z']:            
                    pm.setDrivenKeyframe(SDK + '.' + vec + ch, cd = self.lm.config_node.control + '.fist_a' )
        
        #set max value
        pm.setAttr('CN_l_indexRoot_0_SDK' + '.translateZ',1)
#         self.indexSDK[1].rx.set(7.726)
#         self.indexSDK[1].ry.set(98.472)
#         self.indexSDK[1].rz.set(-6.923)
        self.lm.config_node.control.fist_a.set(10)
        
        print self.indexSDK[1].rx.get()
#         print see(self.indexSDK[1].rx)
        print self.lm.config_node.control.fist_a.get()
        
#         #set max sdk
#         for SDK in self.indexSDK:
#             for vec in ['t','r']:
#                 for ch in ['x','y','z']:            
#                     pm.setDrivenKeyframe(SDK + '.' + vec + ch, cd = self.lm.config_node.control + '.fist_a' )
         
#         #reset value   
#         for SDK in self.indexSDK:
#             pm.setDrivenKeyframe(SDK + '.ry', cd=self.lm.config_node.control + '.fist_a' )
#             for vec in ['t','r']:
#                 for ch in ['x','y','z']:
#                     SDK.attr('%s%s'%vec,ch.set(0))
                                   
        def __cleanUp():
            pass                        
                 
        
# import maya.cmds as mc
# 
# pathOfFiles = 'C:\Users\UV\Desktop\Rigging workshop/'
# fileType = 'obj'
# files = cmds.getFileList(folder = pathOfFiles,fs = '*.%s' % fileType)
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
# #from Modules import legModule
# #lg = legModule.LegModule()
# #lg.buildGuides()
# #lg.build()        
# 
# from Modules import fingerModule
# fg = fingerModule.FingerModule()
# fg.buildGuides()
# #fg.build()

        

        
        
        
