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
        self.indexSdks = []
        
        #attrs
#         self.attrs = ['fist_a','firs_b','relax_a','relax_b','relax_c',
#                       'relax_d','relax_e','grab_a','grab_b','spread_a',
#                       'spread_b','hand','plam_a','plam_b','thumb_a',
#                       'thumb_b','index_curl','middle_curl','ring_curl',
#                       'pinky_curl','point']
        
        self.attrs = ['fist_a']
            
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
        control.addFloatAttr(self.lm.config_node.control,self.attrs,-3,10)

    def __fingerCC(self):
        
        #create index cc ctrl
        self.indexSdks = []
        
        for num,indexJoint in enumerate(self.indexBlendChain.chain):
            if num < self.indexBlendChain.chainLength() - 1:
                #correct jj name
                pm.rename(indexJoint,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'jj'))
                
                #create sdk and correct cc name
                cc = control.Control(self.side,self.baseName,size = indexJoint.getRadius() / 5) 
                cc.circleCtrl()
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'SDK'))
                self.indexSdks.append(cc.controlGrp)
                
                #align cc grp
                pm.xform(cc.controlGrp,ws = 1,matrix = indexJoint.worldMatrix.get())
                
                #parent jj
                cc.controlGrp.setParent(indexJoint)
                self.indexBlendChain.chain[num + 1].setParent(cc.control)   
           
    def __setSDK(self):

        #prepare chr:
        chr = ['x','y','z']
        
        #set val:
        indexMainMaxRotList = []
        indexMainMinRotList = []
        
        #fist max(10) val:
        indexFistaMaxRotList = [[0.0, 1.1667451, 0.0],[7.7256914, 98.47196, -6.9225698],[-5.0864835, 109.12878, -14.33877],[0.0, 121.35306, 0.0]]
        midFistaMaxRotList = [[0.0, 0.0, 0.0],[1.343452, 94.24476, -0.17447495],[-1.2531719, 111.28286, -3.2134328],[0.0, 111.31801, 0.0]]
        ringFistaMaxRotList = [[-2.2915976, 0.99224884, 0.3515861],[-1.654204, 94.229347, 8.2182298],[1.4022289, 107.094, 4.5496722],[0.0, 118.21848, 0.0]]
        pinkyFistaMaxRotList = [[-3.4711895, 4.0933869, 1.0393476],[-3.908681, 104.27619, 16.853265],[3.2222396, 102.18746, 14.587789],[0.0, 96.374496, 0.0]]
        
        indexMainMaxRotList.append(indexFistaMaxRotList)
                
        #fist min(-3) val:        
        indexFistaMinRotList = [[0.0, 0.0, 0.0], [2.3656792422, -23.6599771482, 1.9016638177], [1.52594527386, -22.6379875224, 4.30163088994], [0.0, -26.3052739235, 0.0]]
        midFistaMinRotList = [[0.0, 0.0, 0.0], [0.0, -13.0502537762, 0.0], [0.0, -23.0761814451, 0.964029917432], [0.0, -23.0867256252, 0.0]]
        ringFistaMinRotList = [[0.0, 0.0, 0.0], [-8.0276, -10.3753295339, -0.732478856346], [0.0, -17.8428903421, -1.36490170652], [0.0, -21.1802374187, 0.0]]
        pinkyFistaMinRotList = [[1.04135682811, -1.22801612104, 0.0], [-8.96452963728, -10.9554773142, -2.95571135541], [-0.966671923269, -14.4907648544, -4.37633648762], [0.0, -12.7468772018, 0.0]]
        
        indexMainMinRotList.append(indexFistaMinRotList)
        
        #set dic
        indexRotAttrs = []
        indexFistMaxRotVals = [] 
        indexFistMinRotVals = []
        
        indexMainMaxRotVals = [indexFistMaxRotVals]
        indexMainMinRotVals= [indexFistMinRotVals]
        
        
#         midRotAttrs = []
#         midFistMaxRotVals = [] 
#         midFistMinRotVals = []
#         
#         ringRotAttrs = []
#         ringFistMaxRotVals = [] 
#         ringFistMinRotVals = []
#         
#         pinkyRotAttrs = []
#         pinkyFistMaxRotVals = [] 
#         pinkyFistMinRotVals = []

        #get attr data
        for indexSdk in self.indexSdks:
            for ch in chr:
                attr = indexSdk + '.r' + ch
                indexRotAttrs.append(attr)
                                
        #set defaut(0) sdk
        for indexSdk in self.indexSdks:
            for ch in chr:            
                pm.setDrivenKeyframe(indexSdk + '.r' + ch,v = 0, 
                                     cd = self.lm.config_node.control + '.fist_a',dv = 0)
#             for vec in ['t','r']:                
#                 pm.setDrivenKeyframe(indexSdk + '.' + vec + ch,v = 0, 
#                                      cd = self.lm.config_node.control + '.fist_a',dv = 0)            
    
        for selfAttr in self.attrs:
            #get rotate Max val
            for valueList in indexMainMaxRotList:
                for value in valueList:
                    for num in [0,1,2]:
                        val = value[num]
                        indexFistMaxRotVals.append(val)
            
            #set dic max(10) val
            for indexMaxRotVals in indexMainMaxRotVals:
                for num,attr in enumerate(indexRotAttrs):
                    pm.setDrivenKeyframe(attr,v = indexMaxRotVals[num],
                                        cd = self.lm.config_node.control + '.' + selfAttr,dv = 10)
     
            #get rotate Min val
            for index in indexFistaMinRotList:
                for num in [0,1,2]:
                    val = index[num]
                    indexFistMinRotVals.append(val)
     
            #set dic min(-3) val
            for num,attr in enumerate(indexRotAttrs):
                pm.setDrivenKeyframe(attr,v = indexFistMinRotVals[num],
                                    cd = self.lm.config_node.control + '.' + selfAttr,dv = -3)
 
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

        

        
        
        
