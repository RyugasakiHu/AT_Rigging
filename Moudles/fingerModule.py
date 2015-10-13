import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy,limbModule

class FingerModule(object):
    
    posThumbArray = [(6.4540,13.8587,0.0015),(6.6541,13.7464,0.1988),(6.8466,13.6588,0.3228),(7.0855,13.5695,0.453)]
    posIndexArray = [[6.58,14.03,-0.04],[6.94,14.03,-0.04],[7.3,14.03,-0.04],[7.515,14.03,-0.04],[7.74,14.03,-0.04]]
    posMiddleArray = [[6.539,14.05,-0.22],[6.9,14.05,-0.22],[7.361,14.05,-0.22],[7.58,14.05,-0.22],[7.88,14.05,-0.22]]
    posRingArray = [[6.58,14.055,-0.413],[6.94,14.055,-0.413],[7.3,14.055,-0.413],[7.515,14.055,-0.413],[7.74,14.055,-0.413]]
    posPinkyArray = [[6.746,14.03,-0.585],[6.94,14.03,-0.585],[7.134,14.03,-0.585],[7.276,14.03,-0.585],[7.5,14.03,-0.585]]
    
    rotThumbArrary = [[45.007,38.874,17.922],[57.442,33.9,47.31],[58.095,33.758,47.498],[57.894,36.279,48.717]]
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
        self.attrs = ['fist_a','firs_b','relax_a','relax_b','relax_c',
                      'relax_d','relax_e','grab_a','grab_b','spread_a',
                      'spread_b','hand','palm_a','palm_b','thumb_a',
                      'thumb_b','thumb_c','thumb_d','index_curl',
                      'middle_curl','ring_curl','pinky_curl','point']
            
        #nameList
        self.fingerName = ['thumb','index','middle','ring','pinky']
        self.fingerJoint = ['Base','Root','Tip','Mid','End','Partial']
        self.thumbJoint = ['Base','Root','Tip','Mid','End','Partial']
        
    def buildGuides(self):
        
        self.guides = []
        self.guideGrp = []
        
        self.thumbGuides = []
        self.indexGuides = []
        self.middleGuides = []
        self.ringGuides = []
        self.pinkyGuides = []

        #thumb
        for num,obj in enumerate(self.posThumbArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[1] + self.thumbJoint[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotThumbArrary[num])
            self.thumbGuides.append(loc)
            
        self.tempThumbGuides = list(self.thumbGuides)
        self.tempThumbGuides.reverse()
        for i in range(len(self.tempThumbGuides)):
            if i != (len(self.tempThumbGuides) - 1):
                pm.parent(self.tempThumbGuides[i],self.tempThumbGuides[i + 1])
        self.tempThumbGuides.reverse()
        self.guides.append(self.tempThumbGuides[0])        
            
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
        self.guideGrp = pm.group(self.tempIndexGuides[0],self.tempMiddleGuides[0],
                                 self.tempRingGuides[0],self.tempPinkyGuides[0],
                                 self.tempThumbGuides[0],n = guideName)

        self.guideGrp.v.set(1)
        
        #connect to the limb
        self.lm = limbModule.LimbModule()
        self.lm.buildGuides()
        
    def build(self):
        
        self.lm.build()  
        #build index
        #thumb info
        self.guideThumbPos = [x.getTranslation(space = 'world') for x in self.thumbGuides]
        self.guideThumbRot = [x.getRotation(space = 'world') for x in self.thumbGuides]
                
        #thumb jj
        self.thumbBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.thumbBlendChain.fromList(self.guideThumbPos,self.guideThumbRot)               
        
        #index info
        self.guideIndexPos = [x.getTranslation(space = 'world') for x in self.indexGuides]
        self.guideIndexRot = [x.getRotation(space = 'world') for x in self.indexGuides]

        #index jj
        self.indexBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.indexBlendChain.fromList(self.guideIndexPos,self.guideIndexRot)        
        
        #mid info
        self.guideMidPos = [x.getTranslation(space = 'world') for x in self.middleGuides]
        self.guideMidRot = [x.getRotation(space = 'world') for x in self.middleGuides] 
        
        #mid jj
        self.midBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.midBlendChain.fromList(self.guideMidPos,self.guideMidRot)        
        
        #ring info
        self.guideRingPos = [x.getTranslation(space = 'world') for x in self.ringGuides]
        self.guideRingRot = [x.getRotation(space = 'world') for x in self.ringGuides] 
        
        #ring jj
        self.ringBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.ringBlendChain.fromList(self.guideRingPos,self.guideRingRot) 
        
        #pinky info
        self.guidePinkyPos = [x.getTranslation(space = 'world') for x in self.pinkyGuides]
        self.guidePinkyRot = [x.getRotation(space = 'world') for x in self.pinkyGuides] 
        
        #pinky jj
        self.pinkyBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.pinkyBlendChain.fromList(self.guidePinkyPos,self.guidePinkyRot) 
                                   
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
        
        #create thumb cc ctrl
        self.thumbSdks = []
        for num,thumbJoint in enumerate(self.thumbBlendChain.chain):
            #correct jj name
            pm.rename(thumbJoint,nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJoint[num],'jj'))
            if num < self.thumbBlendChain.chainLength() - 1:
                #create sdk and correct cc name
                cc = control.Control(self.side,self.baseName,size = thumbJoint.getRadius() / 5) 
                cc.circleCtrl()
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJoint[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJoint[num],'SDK'))
                self.indexSdks.append(cc.controlGrp)
                #align cc grp
                pm.xform(cc.controlGrp,ws = 1,matrix = thumbJoint.worldMatrix.get())
                #parent jj
                cc.controlGrp.setParent(thumbJoint)
                self.thumbBlendChain.chain[num + 1].setParent(cc.control)           
        
        #create index cc ctrl
        self.indexSdks = []
        for num,indexJoint in enumerate(self.indexBlendChain.chain):
            #correct jj name
            pm.rename(indexJoint,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJoint[num],'jj'))
            if num < self.indexBlendChain.chainLength() - 1:
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
           
        #create mid cc ctrl
        self.midSdks = []
        for num,midJoint in enumerate(self.midBlendChain.chain):
            #correct jj name
            pm.rename(midJoint,nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJoint[num],'jj'))                        
            if num < self.midBlendChain.chainLength() - 1:                
                #create sdk and correct cc name
                cc = control.Control(self.side,self.baseName,size = midJoint.getRadius() / 5) 
                cc.circleCtrl()
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJoint[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJoint[num],'SDK'))
                self.midSdks.append(cc.controlGrp)                
                #align cc grp
                pm.xform(cc.controlGrp,ws = 1,matrix = midJoint.worldMatrix.get())                
                #parent jj
                cc.controlGrp.setParent(midJoint)
                self.midBlendChain.chain[num + 1].setParent(cc.control)              

        #create ring cc ctrl
        self.ringSdks = []
        for num,ringJoint in enumerate(self.ringBlendChain.chain):
            #correct jj name
            pm.rename(ringJoint,nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJoint[num],'jj'))                        
            if num < self.ringBlendChain.chainLength() - 1:                
                #create sdk and correct cc name
                cc = control.Control(self.side,self.baseName,size = ringJoint.getRadius() / 5) 
                cc.circleCtrl()
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJoint[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJoint[num],'SDK'))
                self.ringSdks.append(cc.controlGrp)                
                #align cc grp
                pm.xform(cc.controlGrp,ws = 1,matrix = ringJoint.worldMatrix.get())                
                #parent jj
                cc.controlGrp.setParent(ringJoint)
                self.ringBlendChain.chain[num + 1].setParent(cc.control)    
           
        #create pinky cc ctrl
        self.pinkySdks = []
        for num,pinkyJoint in enumerate(self.pinkyBlendChain.chain):
            #correct jj name
            pm.rename(pinkyJoint,nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJoint[num],'jj'))                        
            if num < self.pinkyBlendChain.chainLength() - 1:                
                #create sdk and correct cc name
                cc = control.Control(self.side,self.baseName,size = pinkyJoint.getRadius() / 5) 
                cc.circleCtrl()
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJoint[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJoint[num],'SDK'))
                self.pinkySdks.append(cc.controlGrp)                
                #align cc grp
                pm.xform(cc.controlGrp,ws = 1,matrix = pinkyJoint.worldMatrix.get())                
                #parent jj
                cc.controlGrp.setParent(pinkyJoint)
                self.pinkyBlendChain.chain[num + 1].setParent(cc.control)             
           
    def __setSDK(self):

        #prepare chr:
        chr = ['x','y','z']
        
        #index min ring pinky list:
        #set Append val List:
        indexAppendMaxRotList = []
        indexAppendMinRotList = []
        midAppendMaxRotList = []
        midAppendMinRotList = []
        ringAppendMaxRotList = []
        ringAppendMinRotList = []                
        pinkyAppendMaxRotList = []
        pinkyAppendMinRotList = []                
        
        #set Main extreme list
        indexMainMaxRotList = []
        indexMainMinRotList = []
        midMainMaxRotList = []
        midMainMinRotList = []
        ringMainMaxRotList = []
        ringMainMinRotList = []
        pinkyMainMaxRotList = []
        pinkyMainMinRotList = []                        
        
        #fist_a
        #fist_a max(10) val:
        indexFistaMaxRotList = [[0.0, 1.1667451, 0.0],[7.7256914, 98.47196, -6.9225698],[-5.0864835, 109.12878, -14.33877],[0.0, 121.35306, 0.0]]
        midFistaMaxRotList = [[0.0, 0.0, 0.0],[1.343452, 94.24476, -0.17447495],[-1.2531719, 111.28286, -3.2134328],[0.0, 111.31801, 0.0]]
        ringFistaMaxRotList = [[-2.2915976, 0.99224884, 0.3515861],[-1.654204, 94.229347, 8.2182298],[1.4022289, 107.094, 4.5496722],[0.0, 118.21848, 0.0]]
        pinkyFistaMaxRotList = [[-3.4711895, 4.0933869, 1.0393476],[-3.908681, 104.27619, 16.853265],[3.2222396, 102.18746, 14.587789],[0.0, 96.374496, 0.0]]
        
        indexAppendMaxRotList.append(indexFistaMaxRotList)
        midAppendMaxRotList.append(midFistaMaxRotList)
        ringAppendMaxRotList.append(ringFistaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyFistaMaxRotList)
        
        #fist_a min(-3) val:        
        indexFistaMinRotList = [[0.0, 0.0, 0.0], [2.3656792422, -23.6599771482, 1.9016638177], [1.52594527386, -22.6379875224, 4.30163088994], [0.0, -26.3052739235, 0.0]]
        midFistaMinRotList = [[0.0, 0.0, 0.0], [0.0, -13.0502537762, 0.0], [0.0, -23.0761814451, 0.964029917432], [0.0, -23.0867256252, 0.0]]
        ringFistaMinRotList = [[0.0, 0.0, 0.0], [-8.0276, -10.3753295339, -0.732478856346], [0.0, -17.8428903421, -1.36490170652], [0.0, -21.1802374187, 0.0]]
        pinkyFistaMinRotList = [[1.04135682811, -1.22801612104, 0.0], [-8.96452963728, -10.9554773142, -2.95571135541], [-0.966671923269, -14.4907648544, -4.37633648762], [0.0, -12.7468772018, 0.0]]
         
        indexAppendMinRotList.append(indexFistaMinRotList)    
        midAppendMinRotList.append(midFistaMinRotList)        
        ringAppendMinRotList.append(ringFistaMinRotList)    
        pinkyAppendMinRotList.append(pinkyFistaMinRotList)    
        
        #fist_b
        #fist_b max(10) val:
        indexFistbMaxRotList = [[0.0, 0.0, 0.0],[4.4223436, 66.184789, 1.8546305],[0.0, 101.20612, 0.0],[0.0, 75.878746, 0.0]]
        midFistbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 81.00373, 0.0],[0.0, 97.623089, 0.0],[0.0, 98.548929, 0.0]]
        ringFistbMaxRotList = [[0.0, 0.0, 0.0],[-4.8254718, 85.586453, 2.4808469],[0.0, 93.487201, 0.0],[0.0, 97.57188, 0.0]]
        pinkyFistbMaxRotList = [[0.0, 0.0, 0.0],[-11.238872, 91.357247, 3.8876141],[0.0, 90.796196, 0.0],[0.0, 94.880874, 0.0]]
 
        indexAppendMaxRotList.append(indexFistbMaxRotList)
        midAppendMaxRotList.append(midFistbMaxRotList)
        ringAppendMaxRotList.append(ringFistbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyFistbMaxRotList)        

        #fist_b min(-3)val:
        indexFistbMinRotList = [[0.0, 0.0, 0.0],[-1.32670302602, -19.8554351973, 0.0],[0.0, -30.3618382339, 0.0],[0.0, -22.7636215909, 0.0]]
        midFistbMinRotList = [[0.0, 0.0, 0.0],[0.0, -24.3011201928, 0.0],[0.0, -29.2869273013, 0.0],[0.0, -29.5646757999, 0.0]]
        ringFistbMinRotList = [[0.0, 0.0, 0.0],[1.44764159413, -25.6759372289, 0.0],[0.0, -28.0461595706, 0.0],[0.0, -29.2715641599, 0.0]]
        pinkyFistbMinRotList = [[0.0, 0.0, 0.0],[3.37166184668, -27.4071741155, -1.16628417085],[0.0, -27.2388580576, 0.0],[0.0, -28.4642617121, 0.0]]

        indexAppendMinRotList.append(indexFistbMinRotList)
        midAppendMinRotList.append(midFistbMinRotList)        
        ringAppendMinRotList.append(ringFistbMinRotList)    
        pinkyAppendMinRotList.append(pinkyFistbMinRotList)            
        
        #relax_a        
        #relax_a max(10) val:        
        indexRelaxaMaxRotList = [[0.0, 0.0, 0.0],[-0.89780606, -8.5116474, -9.925511],[0.0, 15.239331, 0.0],[0.0, 15.239331, 0.0]]
        midRelaxaMaxRotList = [[0.0, 0.0, 0.0],[-0.14373821, 4.6882137, -0.50410896],[0.0, 32.523238, 0.0],[0.0, 32.523238, 0.0]]
        ringRelaxaMaxRotList = [[-2.9928762, 0.0, 0.0],[4.1312803, 15.615173, 7.78713],[0.0, 30.371118, 0.0],[0.0, 30.371118, 0.0]]
        pinkyRelaxaMaxRotList = [[-1.8613005, 0.056215787, 1.7302502],[12.382909, 26.61312, 15.826518],[0.0, 45.728939, 0.0],[0.0, 45.728939, 0.0]]
                
        indexAppendMaxRotList.append(indexRelaxaMaxRotList)
        midAppendMaxRotList.append(midRelaxaMaxRotList)
        ringAppendMaxRotList.append(ringRelaxaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxaMaxRotList)        
        
        #relax_a  min(-3)val:          
        indexRelaxaMinRotList = [[0.0, 0.0, 0.0],[0.0, 2.55349438396, 2.97765346574],[0.0, -4.57179902403, 0.0],[0.0, -4.57179902403, 0.0]]
        midRelaxaMinRotList = [[0.0, 0.0, 0.0],[0.0, -1.40646424112, 0.0],[0.0, -9.75697114332, 0.0],[0.0, -9.75697114332, 0.0]]
        ringRelaxaMinRotList = [[0.897862892745, 0.0, 0.0],[-1.23938408908, -4.68455226138, -2.33613911906],[0.0, -9.11133613376, 0.0],[0.0, -9.11133613376, 0.0]]
        pinkyRelaxaMinRotList = [[0.0, 0.0, 0.0],[-3.7148726673, -7.98393590273, -4.74795583361],[0.0, -13.7186819746, 0.0],[0.0, -13.7186819746, 0.0]]
         
        indexAppendMinRotList.append(indexRelaxaMinRotList) 
        midAppendMinRotList.append(midRelaxaMinRotList)        
        ringAppendMinRotList.append(ringRelaxaMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxaMinRotList)            
        
        #relax_b        
        #relax_b max(10) val:        
        indexRelaxbMaxRotList = [[0.0, 0.0, 0.0],[4.6833866, 5.8816114, -0.1751071],[0.0, 10.100644, 0.0],[0.0, 10.100644, 0.0]]
        midRelaxbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 15.223175, 0.0],[0.0, 10.308678, 0.0],[0.0, 10.308678, 0.0]]
        ringRelaxbMaxRotList = [[0.0, 0.0, 0.0],[-8.0276, 17.893472, 1.7329901],[0.0, 14.285307, 0.0],[0.0, 14.285307, 0.0]]
        pinkyRelaxbMaxRotList = [[0.0, 0.0, 0.0],[-10.137134, 20.327381, 2.100268],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
         
        indexAppendMaxRotList.append(indexRelaxbMaxRotList)
        midAppendMaxRotList.append(midRelaxbMaxRotList)
        ringAppendMaxRotList.append(ringRelaxbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxbMaxRotList)        
        
        #relax_b min(-3) val: 
        indexRelaxbMinRotList = [[0.0, 0.0, 0.0],[-1.40501603744, -1.76448329217, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
        midRelaxbMinRotList = [[0.0, 0.0, 0.0],[0.0, -4.56695278412, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
        ringRelaxbMinRotList = [[0.0, 0.0, 0.0],[2.40827997571, -5.36804128933, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
        pinkyRelaxbMinRotList = [[0.0, 0.0, 0.0],[3.04113989245, -6.09821425613, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
                 
        indexAppendMinRotList.append(indexRelaxbMinRotList)
        midAppendMinRotList.append(midRelaxbMinRotList)        
        ringAppendMinRotList.append(ringRelaxbMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxbMinRotList)            
            
        #relax_c        
        #relax_c max(10) val:        
        indexRelaxcMaxRotList = [[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[0.0, 22.91704, 0.0],[0.0, 22.91704, 0.0]]
        midRelaxcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 46.799998, 0.0],[0.0, 38.519999, 0.0],[0.0, 38.519999, 0.0]]
        ringRelaxcMaxRotList = [[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 43.664156, 0.0],[0.0, 43.664156, 0.0]]
        pinkyRelaxcMaxRotList = [[-2.8230663, 0.0, 0.0],[-3.8132578, 54.511244, 5.3288443],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
                         
        indexAppendMaxRotList.append(indexRelaxcMaxRotList)      
        midAppendMaxRotList.append(midRelaxcMaxRotList)
        ringAppendMaxRotList.append(ringRelaxcMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxcMaxRotList)              
        
        #relax_c min(-3) val:
        indexRelaxcMinRotList = [[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -6.87511250747, 0.0],[0.0, -6.87511250747, 0.0]]
        midRelaxcMinRotList = [[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
        ringRelaxcMinRotList = [[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -13.099245447, 0.0],[0.0, -13.099245447, 0.0]]
        pinkyRelaxcMinRotList = [[0.0, 0.0, 0.0],[1.14397733976, -16.3533737924, -1.59865341533],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
                 
        indexAppendMinRotList.append(indexRelaxcMinRotList)
        midAppendMinRotList.append(midRelaxcMinRotList)        
        ringAppendMinRotList.append(ringRelaxcMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxcMinRotList)            
        
        #relax_d        
        #relax_d max(10) val:              
        indexRelaxdMaxRotList = [[0.0, 0.0, 0.0],[5.4160948, 12.535184, 1.2137211],[0.0, 10.100644, -1.7270777e-08],[6.8093491e-09, 10.100644, -1.6329651e-08]]
        midRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-1.7709299, 22.999166, -1.5032809],[6.9404626e-09, 10.308678, -1.6351366e-08],[9.7545475e-09, 10.308678, -1.4845411e-08]]
        ringRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-9.0447572, 27.937911, -2.3253179],[8.2228049e-09, 14.285307, -1.5505428e-08],[1.1794547e-08, 14.285307, -1.2996997e-08]]
        pinkyRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-15.723218, 33.076844, -1.6909839],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
        
        indexAppendMaxRotList.append(indexRelaxdMaxRotList)  
        midAppendMaxRotList.append(midRelaxdMaxRotList)
        ringAppendMaxRotList.append(ringRelaxdMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxdMaxRotList)            

        #relax_d min(-3) val:
        indexRelaxdMinRotList = [[0.0, 0.0, 0.0],[-1.62482857459, -3.76055524696, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
        midRelaxdMinRotList = [[0.0, 0.0, 0.0],[0.0, -6.89974964616, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
        ringRelaxdMinRotList = [[0.0, 0.0, 0.0],[2.71342718955, -8.38137266181, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
        pinkyRelaxdMinRotList = [[0.0, 0.0, 0.0],[4.71696534913, -9.92305375801, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
                         
        indexAppendMinRotList.append(indexRelaxdMinRotList)
        midAppendMinRotList.append(midRelaxdMinRotList)        
        ringAppendMinRotList.append(ringRelaxdMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxdMinRotList)         
        
        #relax_e         
        #relax_e max(10) val:                     
        indexRelaxeMaxRotList = [[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[9.2055523e-09, 5.0979753, -1.5113549e-08],[1.0512118e-08, 12.199657, -1.4235765e-08]]
        midRelaxeMaxRotList = [[0.0, 0.0, 0.0],[0.0, 46.799998, 1.7771855e-08],[0.0, 38.519999, 2.5966873e-08],[0.0, 38.519999, 2.1833783e-07]]
        ringRelaxeMaxRotList = [[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 47.306373, 0.0],[0.0, 47.306373, 0.0]]
        pinkyRelaxeMaxRotList = [[-2.8230663, 0.0, 0.0],[-11.348742, 55.622932, 9.5249724],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
                 
        indexAppendMaxRotList.append(indexRelaxeMaxRotList)         
        midAppendMaxRotList.append(midRelaxeMaxRotList)
        ringAppendMaxRotList.append(ringRelaxeMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxeMaxRotList)             
                
        #relax_e min(-3) val:
        indexRelaxeMinRotList = [[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -1.52939260387, 0.0],[0.0, -3.65989711932, 0.0]]
        midRelaxeMinRotList = [[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
        ringRelaxeMinRotList = [[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -14.1919116307, 0.0],[0.0, -14.1919116307, 0.0]]
        pinkyRelaxeMinRotList = [[0.0, 0.0, 0.0],[3.4046228407, -16.6868815882, -2.85749193878],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
                 
        indexAppendMinRotList.append(indexRelaxeMinRotList)   
        midAppendMinRotList.append(midRelaxeMinRotList)        
        ringAppendMinRotList.append(ringRelaxeMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxeMinRotList)                 
         
        #grab_a 
        #grab_a max(10) val:        
        indexGrabaMaxRotList = [[0.0, 0.0, 0.0],[-1.7635041, -8.5214628, -16.147383],[0.0, 41.94425, 0.0],[0.0, 44.280939, 0.0]]
        midGrabaMaxRotList = [[0.0, 0.0, 0.0],[-0.030713774, -5.1010537, -3.0009306],[0.0, 40.029996, 0.0],[0.0, 41.086042, 0.0]]
        ringGrabaMaxRotList = [[-2.9928762, 0.0, 0.0],[3.6224929, -2.4102271, 4.7080181],[0.0, 40.898433, 0.0],[0.0, 41.482517, 0.0]]
        pinkyGrabaMaxRotList = [[-1.8613005, 0.056215787, 1.7302502],[1.4394069, 0.14493989, 16.418532],[0.0, 43.58425, 0.0],[0.0, 52.072421, 0.0]]
        
        indexAppendMaxRotList.append(indexGrabaMaxRotList)
        midAppendMaxRotList.append(midGrabaMaxRotList)
        ringAppendMaxRotList.append(ringGrabaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyGrabaMaxRotList)            
        
        #grab_a min(-3) val: 
        indexGrabaMinRotList = [[0.0, 0.0, 0.0],[0.0, 2.55643895266, 4.84421472464],[0.0, -12.5832744564, 0.0],[0.0, -13.284281742, 0.0]]
        midGrabaMinRotList = [[0.0, 0.0, 0.0],[0.0, 1.53031619331, 0.900279164949],[0.0, -12.0089988007, 0.0],[0.0, -12.3258143315, 0.0]]
        ringGrabaMinRotList = [[0.897862892745, 0.0, 0.0],[-1.08674781614, 0.0, -1.4124054644],[0.0, -12.2695308218, 0.0],[0.0, -12.4447552972, 0.0]]
        pinkyGrabaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -4.92555972899],[0.0, -13.0752754812, 0.0],[0.0, -15.6217261951, 0.0]]
                         
        indexAppendMinRotList.append(indexGrabaMinRotList)   
        midAppendMinRotList.append(midGrabaMinRotList)        
        ringAppendMinRotList.append(ringGrabaMinRotList)    
        pinkyAppendMinRotList.append(pinkyGrabaMinRotList)                 
                
        #grab_b 
        #grab_b max(10) val:                 
        indexGrabbMaxRotList = [[0.0, 0.0, 0.0],[-1.7635041, -8.5214628, -16.147383],[0.0, 20.931244, -1.7567324e-08],[0.0, 23.267933, -1.7348401e-08]]
        midGrabbMaxRotList = [[0.0, 0.0, 0.0],[-0.030713774, -2.9912371, -3.0009306],[0.0, 31.691439, -1.7747642e-08],[8.5345485e-09, 32.747485, -1.5588491e-08]]
        ringGrabbMaxRotList = [[-2.9928762, 0.0, 0.0],[-1.9605419, 10.418159, 11.084858],[0.0, 39.844309, 0.0],[0.0, 40.428393, 0.0]]
        pinkyGrabbMaxRotList = [[-1.8613005, 0.056215787, 1.7302502],[-1.9825828, 29.626945, 18.362295],[0.0, 35.245693, 0.0],[0.0, 34.28776, 0.0]]
                         
        indexAppendMaxRotList.append(indexGrabbMaxRotList)
        midAppendMaxRotList.append(midGrabbMaxRotList)
        ringAppendMaxRotList.append(ringGrabbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyGrabbMaxRotList)            
        
        #grab_b min(-3) val:                 
        indexGrabbMinRotList = [[0.0, 0.0, 0.0],[0.0, 2.55643895266, 4.84421472464],[0.0, -6.27937348304, 0.0],[0.0, -6.98037935086, 0.0]]
        midGrabbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.897371185757, 0.900279164949],[0.0, -9.5074318884, 0.0],[0.0, -9.82424536423, 0.0]]
        ringGrabbMinRotList = [[0.897862892745, 0.0, 0.0],[0.0, -3.12544759854, -3.32545729794],[0.0, -11.9532935107, 0.0],[0.0, -12.1285162186, 0.0]]
        pinkyGrabbMinRotList = [[0.0, 0.0, 0.0],[0.0, -8.8880835737, -5.50868833157],[0.0, -10.5737077603, 0.0],[0.0, -10.2863291471, 0.0]]
                            
        indexAppendMinRotList.append(indexGrabbMinRotList)       
        midAppendMinRotList.append(midGrabbMinRotList)        
        ringAppendMinRotList.append(ringGrabbMinRotList)    
        pinkyAppendMinRotList.append(pinkyGrabbMinRotList)                        
                
        #Spreada 
        #Spreada max(10) val:                 
        indexSpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -25.582658],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midSpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringSpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 8.8561972],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkySpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 22.877102],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        indexAppendMaxRotList.append(indexSpreadaMaxRotList)
        midAppendMaxRotList.append(midSpreadaMaxRotList)
        ringAppendMaxRotList.append(ringSpreadaMaxRotList)
        pinkyAppendMaxRotList.append(pinkySpreadaMaxRotList)             
        
        #Spreada min(-3) val:                 
        indexSpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 7.67479746336],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midSpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringSpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -2.65685910148],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkySpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -6.86313075324],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
              
        indexAppendMinRotList.append(indexSpreadaMinRotList)  
        midAppendMinRotList.append(midSpreadaMinRotList)        
        ringAppendMinRotList.append(ringSpreadaMinRotList)    
        pinkyAppendMinRotList.append(pinkySpreadaMinRotList)            


        #Spreadb 
        #Spreadb max(10) val:                 
        indexSpreadbMaxRotList = [[0.0, 0.0, 0.0],[8.7247019, -10.394853, -18.082124],[0.0, -8.2723094, -1.7277899e-08],[0.0, -8.2723094, -1.6642118e-08]]
        midSpreadbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, -8.2723094, 3.5543707e-08],[0.0, -8.2723094, 1.7958196e-08]]
        ringSpreadbMaxRotList = [[0.0, 0.0, 0.0],[-10.955866, 7.5271701, 2.1637058],[0.0, -8.2723094, -1.7297596e-08],[0.0, -8.2723094, -1.7446468e-08]]
        pinkySpreadbMaxRotList = [[0.0, 0.0, 0.0],[-3.4375475, 29.857157, 26.640187],[0.0, -8.2723094, 0.0],[0.0, -8.2723094, 0.0]]
                         
        indexAppendMaxRotList.append(indexSpreadbMaxRotList)
        midAppendMaxRotList.append(midSpreadbMaxRotList)
        ringAppendMaxRotList.append(ringSpreadbMaxRotList)
        pinkyAppendMaxRotList.append(pinkySpreadbMaxRotList)            
        
        #Spreadb min(-3) val:                 
        indexSpreadbMinRotList = [[0.0, 0.0, 0.0],[-2.61741043801, 3.11845608838, 5.42463689589],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
        midSpreadbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
        ringSpreadbMinRotList = [[0.0, 0.0, 0.0],[3.28675999708, -2.25815105805, 0.0],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
        pinkySpreadbMinRotList = [[0.0, 0.0, 0.0],[1.03126421643, -8.95714757769, -7.99205549907],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
                         
        indexAppendMinRotList.append(indexSpreadbMinRotList) 
        midAppendMinRotList.append(midSpreadbMinRotList)        
        ringAppendMinRotList.append(ringSpreadbMinRotList)    
        pinkyAppendMinRotList.append(pinkySpreadbMinRotList)             

        #hand 
        #hand max(10) val:                 
        indexHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 5.9506481],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.96022806],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -3.8924184],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -8.3619136],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
                         
        indexAppendMaxRotList.append(indexHandMaxRotList)
        midAppendMaxRotList.append(midHandMaxRotList)
        ringAppendMaxRotList.append(ringHandMaxRotList)
        pinkyAppendMaxRotList.append(pinkyHandMaxRotList)            
        
        #hand min(-3) val:                 
        indexHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -1.78519442026],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 1.16772562065],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 2.5085741245],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]       
                
        indexAppendMinRotList.append(indexHandMinRotList) 
        midAppendMinRotList.append(midHandMinRotList)        
        ringAppendMinRotList.append(ringHandMinRotList)    
        pinkyAppendMinRotList.append(pinkyHandMinRotList)             

        #palm_a 
        #palm_a max(10) val:                 
        indexPalmaMaxRotList = [[9.5015777, 0.0, 0.0],[12.129516, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmaMaxRotList = [[-24.239371, -0.30426803, -0.74108914],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmaMaxRotList = [[-17.534821, 1.0340395, -2.1197015],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]        
        
        indexAppendMaxRotList.append(indexPalmaMaxRotList)
        midAppendMaxRotList.append(midPalmaMaxRotList)
        ringAppendMaxRotList.append(ringPalmaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPalmaMaxRotList)            
        
        #palm_a min(-3) val:                 
        indexPalmaMinRotList = [[-2.85047358591, 0.0, 0.0],[-3.6388550315, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmaMinRotList = [[7.27181158401, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmaMinRotList = [[5.2604463016, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]] 
                
        indexAppendMinRotList.append(indexPalmaMinRotList)  
        midAppendMinRotList.append(midPalmaMinRotList)        
        ringAppendMinRotList.append(ringPalmaMinRotList)    
        pinkyAppendMinRotList.append(pinkyPalmaMinRotList)            
        
        #palm_b 
        #palm_b max(10) val:                 
        indexPalmbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmbMaxRotList = [[-6.8414008, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmbMaxRotList = [[-13.947657, 1.9094432, -0.4750786],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        indexAppendMaxRotList.append(indexPalmbMaxRotList)
        midAppendMaxRotList.append(midPalmbMaxRotList)
        ringAppendMaxRotList.append(ringPalmbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPalmbMaxRotList)            
        
        #palm_b min(-3) val:                 
        indexPalmbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmbMinRotList = [[2.05242044873, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmbMinRotList = [[4.18429703895, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        indexAppendMinRotList.append(indexPalmbMinRotList)
        midAppendMinRotList.append(midPalmbMinRotList)        
        ringAppendMinRotList.append(ringPalmbMinRotList)    
        pinkyAppendMinRotList.append(pinkyPalmbMinRotList)            
          
        #thumba 
        #thumba max(10) val:                 
        indexThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        indexAppendMaxRotList.append(indexThumbaMaxRotList)
        midAppendMaxRotList.append(midThumbaMaxRotList)
        ringAppendMaxRotList.append(ringThumbaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbaMaxRotList)            
        
        #thumba min(-3) val:                 
        indexThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                 
                
        indexAppendMinRotList.append(indexThumbaMinRotList)         
        midAppendMinRotList.append(midThumbaMinRotList)        
        ringAppendMinRotList.append(ringThumbaMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbaMinRotList)                     
        
        #thumbb 
        #thumbb max(10) val:                 
        indexThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                
        
        indexAppendMaxRotList.append(indexThumbbMaxRotList)
        midAppendMaxRotList.append(midThumbbMaxRotList)
        ringAppendMaxRotList.append(ringThumbbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbbMaxRotList)            
        
        #thumbb min(-3) val:                 
        indexThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                
                
        indexAppendMinRotList.append(indexThumbbMinRotList)  
        midAppendMinRotList.append(midThumbbMinRotList)        
        ringAppendMinRotList.append(ringThumbbMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbbMinRotList)            

        #thumbc 
        #thumbc max(10) val:   
        indexThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        midThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08]]
        ringThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        pinkyThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
         
        indexAppendMaxRotList.append(indexThumbcMaxRotList)    
        midAppendMaxRotList.append(midThumbcMaxRotList)
        ringAppendMaxRotList.append(ringThumbcMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbcMaxRotList)    
        
        #thumbc min(-3) val: 
        indexThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
         
        indexAppendMinRotList.append(indexThumbcMinRotList)
        midAppendMinRotList.append(midThumbcMinRotList)        
        ringAppendMinRotList.append(ringThumbcMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbcMinRotList)            
        
        #thumbd 
        #thumbd max(10) val:   
        indexThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        midThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08]]
        ringThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        pinkyThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
         
        indexAppendMaxRotList.append(indexThumbdMaxRotList)
        midAppendMaxRotList.append(midThumbdMaxRotList)
        ringAppendMaxRotList.append(ringThumbdMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbdMaxRotList)            
        
        #thumbd min(-3) val: 
        indexThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]

        indexAppendMinRotList.append(indexThumbdMinRotList)
        midAppendMinRotList.append(midThumbdMinRotList)        
        ringAppendMinRotList.append(ringThumbdMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbdMinRotList)            
        
        #index_curl 
        #index_curl max(10) val:                 
        indexIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
        midIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
                                 
        indexAppendMaxRotList.append(indexIndexCurlMaxRotList)
        midAppendMaxRotList.append(midIndexCurlMaxRotList)
        ringAppendMaxRotList.append(ringIndexCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyIndexCurlMaxRotList)            
        
        #index_curl min(-3) val:                 
        indexIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
        midIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
                                         
        indexAppendMinRotList.append(indexIndexCurlMinRotList)  
        midAppendMinRotList.append(midIndexCurlMinRotList)        
        ringAppendMinRotList.append(ringIndexCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkyIndexCurlMinRotList)            

        #middle_curl 
        #middle_curl max(10) val:                 
        indexMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
        ringMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        indexAppendMaxRotList.append(indexMiddleCurlMaxRotList)
        midAppendMaxRotList.append(midMiddleCurlMaxRotList)
        ringAppendMaxRotList.append(ringMiddleCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyMiddleCurlMaxRotList)            
        
        #middle_curl min(-3) val:                 
        indexMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
        ringMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]               
                
        indexAppendMinRotList.append(indexMiddleCurlMinRotList)  
        midAppendMinRotList.append(midMiddleCurlMinRotList)        
        ringAppendMinRotList.append(ringMiddleCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkyMiddleCurlMinRotList)            

        #ring_curl 
        #ring_curl max(10) val:                 
        indexRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
        pinkyRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                
        
        indexAppendMaxRotList.append(indexRingCurlMaxRotList)
        midAppendMaxRotList.append(midRingCurlMaxRotList)
        ringAppendMaxRotList.append(ringRingCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRingCurlMaxRotList)            
        
        #ring_curl min(-3) val:                 
        indexRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
        pinkyRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
                 
        indexAppendMinRotList.append(indexRingCurlMinRotList)
        midAppendMinRotList.append(midRingCurlMinRotList)        
        ringAppendMinRotList.append(ringRingCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkyRingCurlMinRotList)            
        
        #pinky_curl 
        #pinky_curl max(10) val:                 
        indexPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
                         
        indexAppendMaxRotList.append(indexPinkyCurlMaxRotList)
        midAppendMaxRotList.append(midPinkyCurlMaxRotList)
        ringAppendMaxRotList.append(ringPinkyCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPinkyCurlMaxRotList)            
        
        #pinky_curl min(-3) val:                 
        indexPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
                           
        indexAppendMinRotList.append(indexPinkyCurlMinRotList)       
        midAppendMinRotList.append(midPinkyCurlMinRotList)        
        ringAppendMinRotList.append(ringPinkyCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkPinkyCurlMinRotList)                                 

        #point 
        #point max(10) val:                 
        indexPointMaxRotList = [[0.0, 0.0, 0.0],[-0.48240779, 0.29722213, -0.10914528],[0.0, -7.8036046, 0.0],[0.0, -7.8036046, 0.0]]
        midPointMaxRotList = [[0.0, 0.0, 0.0],[1.6502186, 52.116256, -4.3852106],[0.0, 99.9835, 0.0],[0.0, 76.63128, 0.0]]
        ringPointMaxRotList = [[0.0, 0.0, 0.0],[-5.1919839, 62.997629, -1.741267],[0.0, 97.862165, 0.0],[0.0, 78.57743, 0.0]]
        pinkyPointMaxRotList = [[0.0, 0.0, 0.0],[-11.35146, 70.628056, 0.91715981],[0.0, 83.653515, 0.0],[0.0, 83.653515, 0.0]]
                                
        indexAppendMaxRotList.append(indexPointMaxRotList)
        midAppendMaxRotList.append(midPointMaxRotList)
        ringAppendMaxRotList.append(ringPointMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPointMaxRotList)    
        
        #point min(-3) val:                 
        indexPointMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 2.34108130208, 0.0],[0.0, 2.34108130208, 0.0]]
        midPointMinRotList = [[0.0, 0.0, 0.0],[0.0, -15.6348762585, 1.3155631832],[0.0, -29.9950512267, 0.0],[0.0, -22.9893817888, 0.0]]
        ringPointMinRotList = [[0.0, 0.0, 0.0],[1.55759534157, -18.8992888563, 0.0],[0.0, -29.358649066, 0.0],[0.0, -23.5732288764, 0.0]]
        pinkyPointMinRotList = [[0.0, 0.0, 0.0],[3.40543798067, -21.1884157715, 0.0],[0.0, -25.0960539922, 0.0],[0.0, -25.0960539922, 0.0]]
                             
        indexAppendMinRotList.append(indexPointMinRotList)       
        midAppendMinRotList.append(midPointMinRotList)        
        ringAppendMinRotList.append(ringPointMinRotList)    
        pinkyAppendMinRotList.append(pinkyPointMinRotList)               
        
        
        #set attr list:
        indexRotAttrs = []
        midRotAttrs = []
        ringRotAttrs = []
        pinkyRotAttrs = []                        
        
        #set attr for each rot attr
        for selfAttr in self.attrs:
            
            #index
            for indexSdk in self.indexSdks:
                for ch in chr:
                    attr = indexSdk + '.r' + ch
                    indexRotAttrs.append(attr)

            #mid
            for midSdk in self.midSdks:
                for ch in chr:
                    attr = midSdk + '.r' + ch
                    midRotAttrs.append(attr)                    

            #ring
            for ringSdk in self.ringSdks:
                for ch in chr:
                    attr = ringSdk + '.r' + ch
                    ringRotAttrs.append(attr)                    
                    
            #pinky
            for pinkySdk in self.pinkySdks:
                for ch in chr:
                    attr = pinkySdk + '.r' + ch
                    pinkyRotAttrs.append(attr)                    

            #set default(0) sdk
            #set index default:
            for indexSdk in self.indexSdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(indexSdk + '.r' + ch,v = 0, 
                                         cd = self.lm.config_node.control + '.' + selfAttr,dv = 0)
                    
            #set mid default:
            for midSdk in self.midSdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(midSdk + '.r' + ch,v = 0, 
                                         cd = self.lm.config_node.control + '.' + selfAttr,dv = 0)   
                    
            #set ring default:
            for ringSdk in self.ringSdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(ringSdk + '.r' + ch,v = 0, 
                                         cd = self.lm.config_node.control + '.' + selfAttr,dv = 0)   
                    
            #set index default:
            for pinkySdk in self.pinkySdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(pinkySdk + '.r' + ch,v = 0, 
                                         cd = self.lm.config_node.control + '.' + selfAttr,dv = 0)                                                                           
                      
        #get/set rotate Max val to main rot list:
        #get index list
        for number,valueList in enumerate(indexAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    indexMainMaxRotList.append(val)
        
        #get mid list
        for number,valueList in enumerate(midAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    midMainMaxRotList.append(val)
                    
        #get ring list
        for number,valueList in enumerate(ringAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    ringMainMaxRotList.append(val)                            

        #get pinky list
        for number,valueList in enumerate(pinkyAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    pinkyMainMaxRotList.append(val)        
        
        #set dic max(10) val
        #set index
        for number,attrList in enumerate(indexRotAttrs):
            pm.setDrivenKeyframe(attrList,v = indexMainMaxRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = 10)
            
        #set dic max(10) val
        #set mid
        for number,attrList in enumerate(midRotAttrs):
            pm.setDrivenKeyframe(attrList,v = midMainMaxRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = 10)  
            
        #set dic max(10) val
        #set ring
        for number,attrList in enumerate(ringRotAttrs):
            pm.setDrivenKeyframe(attrList,v = ringMainMaxRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = 10)  
            
        #set dic max(10) val
        #set pinky
        for number,attrList in enumerate(pinkyRotAttrs):
            pm.setDrivenKeyframe(attrList,v = pinkyMainMaxRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = 10)                                          
            
        #get/set rotate Min val to main rot list:
        #get index list
        for number,valueList in enumerate(indexAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    indexMainMinRotList.append(val)
                    
        #get mid list
        for number,valueList in enumerate(midAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    midMainMinRotList.append(val)
                    
        #get ring list
        for number,valueList in enumerate(ringAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    ringMainMinRotList.append(val)
                    
        #get pinky list
        for number,valueList in enumerate(pinkyAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    pinkyMainMinRotList.append(val)                                                            
        
        #set dic min(-3) val
        #index min(-3) val
        for number,attrList in enumerate(indexRotAttrs):
            pm.setDrivenKeyframe(attrList,v = indexMainMinRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = -3)

        #mid min(-3) val
        for number,attrList in enumerate(midRotAttrs):
            pm.setDrivenKeyframe(attrList,v = midMainMinRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = -3)      
            
        #ring min(-3) val
        for number,attrList in enumerate(ringRotAttrs):
            pm.setDrivenKeyframe(attrList,v = ringMainMinRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = -3)      
            
        #pinky min(-3) val
        for number,attrList in enumerate(pinkyRotAttrs):
            pm.setDrivenKeyframe(attrList,v = pinkyMainMinRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = -3)                                                       
        
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

        

        
        
        
