import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy,limbModule

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
        
        fingerSDK = []
        
        for num,indexJoint in enumerate(self.indexBlendChain.chain):
            
            if num < self.indexBlendChain.chainLength() - 1:
                #correct jj name
                pm.rename(indexJoint,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'jj'))
                
                #create circle
                cc = pm.circle(n = nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'cc'),
                               ch = 1,nr = (1,0,0),r =  indexJoint.getRadius() / 5)[0]
                               
                #align and parent               
                pm.xform(cc,ws = 1,matrix = indexJoint.worldMatrix.get())
                cc.setParent(self.indexBlendChain.chain[num])
                self.indexBlendChain.chain[num+1].setParent(cc)
                    
                #create sdk grp
                sdkGrp = pm.group(cc,n = nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'SDK'),
                         parent = self.indexBlendChain.chain[num])
                fingerSDK.append(sdkGrp)
                
    def __nodeConnect(self):
        
        #create node name
        imrMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + '_index','MDN')
        
        #create node
        imrMultipleNode = pm.createNode('multiplyDivide',n = imrMultipleNodeName)
        
        #set default value
        imrMultipleNode.input2X.set(10)
        imrMultipleNode.input2Y.set(10)
        imrMultipleNode.input2Z.set(10)
        
        #connect curl
        self.lm.config_node.control.index_curl.connect(imrMultipleNode.input1X)
        self.lm.config_node.control.middle_curl.connect(imrMultipleNode.input1Y)
        self.lm.config_node.control.ring_curl.connect(imrMultipleNode.input1Z)        
        
        #output
        #index_curl
        imrMultipleNode.outputX.connect(self.fkIndexChain.chain[0].ry)
        imrMultipleNode.outputX.connect(self.fkIndexChain.chain[1].ry)
        imrMultipleNode.outputX.connect(self.fkIndexChain.chain[2].ry)

#         #middle_curl
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[0].ry)
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[1].ry)
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[2].ry)
#         
#         #index_curl
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[0].ry)
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[1].ry)
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[2].ry)
#         
#         #index_curl
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[0].ry)
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[1].ry)
#         imrMultipleNode.outputX.connect(self.fkIndexChain.chain[2].ry)                        
                 
        
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

        

        
        
        
