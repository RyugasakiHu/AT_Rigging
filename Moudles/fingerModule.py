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
        self.indexSdks = []
        
        #attrs
#         self.attrs = ['fist_a','firs_b','relax_a','relax_b','relax_c',
#                       'relax_d','relax_e','grab_a','grab_b','spread_a',
#                       'spread_b','hand','plam_a','plam_b','thumb_a',
#                       'thumb_b','index_curl','middle_curl','ring_curl',
#                       'pinky_curl','point']
        
        self.attrs = ['fist_a','firs_b','relax_a','relax_b','relax_c','relax_d','relax_e']
            
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
        
        #set Mian val List:
        indexAppendMaxRotList = []
        indexAppendMinRotList = []
        indexMainMaxRotList = []
        indexMainMinRotList = []
        
        #fist_a
        #fist_a max(10) val:
        indexFistaMaxRotList = [[0.0, 1.1667451, 0.0],[7.7256914, 98.47196, -6.9225698],[-5.0864835, 109.12878, -14.33877],[0.0, 121.35306, 0.0]]
        midFistaMaxRotList = [[0.0, 0.0, 0.0],[1.343452, 94.24476, -0.17447495],[-1.2531719, 111.28286, -3.2134328],[0.0, 111.31801, 0.0]]
        ringFistaMaxRotList = [[-2.2915976, 0.99224884, 0.3515861],[-1.654204, 94.229347, 8.2182298],[1.4022289, 107.094, 4.5496722],[0.0, 118.21848, 0.0]]
        pinkyFistaMaxRotList = [[-3.4711895, 4.0933869, 1.0393476],[-3.908681, 104.27619, 16.853265],[3.2222396, 102.18746, 14.587789],[0.0, 96.374496, 0.0]]
        
        indexAppendMaxRotList.append(indexFistaMaxRotList)
        
        #fist_a min(-3) val:        
        indexFistaMinRotList = [[0.0, 0.0, 0.0], [2.3656792422, -23.6599771482, 1.9016638177], [1.52594527386, -22.6379875224, 4.30163088994], [0.0, -26.3052739235, 0.0]]
        midFistaMinRotList = [[0.0, 0.0, 0.0], [0.0, -13.0502537762, 0.0], [0.0, -23.0761814451, 0.964029917432], [0.0, -23.0867256252, 0.0]]
        ringFistaMinRotList = [[0.0, 0.0, 0.0], [-8.0276, -10.3753295339, -0.732478856346], [0.0, -17.8428903421, -1.36490170652], [0.0, -21.1802374187, 0.0]]
        pinkyFistaMinRotList = [[1.04135682811, -1.22801612104, 0.0], [-8.96452963728, -10.9554773142, -2.95571135541], [-0.966671923269, -14.4907648544, -4.37633648762], [0.0, -12.7468772018, 0.0]]
         
        indexAppendMinRotList.append(indexFistaMinRotList)        
        
        #fist_b
        #fist_b max(10) val:
        indexFistbMaxRotList = [[0.0, 0.0, 0.0],[4.4223436, 66.184789, 1.8546305],[0.0, 101.20612, 0.0],[0.0, 75.878746, 0.0]]
        midFistbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 81.00373, 0.0],[0.0, 97.623089, 0.0],[0.0, 98.548929, 0.0]]
        ringFistbMaxRotList = [[0.0, 0.0, 0.0],[-4.8254718, 85.586453, 2.4808469],[0.0, 93.487201, 0.0],[0.0, 97.57188, 0.0]]
        pinkyFistbMaxRotList = [[0.0, 0.0, 0.0],[-11.238872, 91.357247, 3.8876141],[0.0, 90.796196, 0.0],[0.0, 94.880874, 0.0]]
 
        indexAppendMaxRotList.append(indexFistbMaxRotList)

        #fist_b min(-3)val:
        indexFistbMinRotList = [[0.0, 0.0, 0.0],[-1.32670302602, -19.8554351973, 0.0],[0.0, -30.3618382339, 0.0],[0.0, -22.7636215909, 0.0]]
        midFistbMinRotList = [[0.0, 0.0, 0.0],[0.0, -24.3011201928, 0.0],[0.0, -29.2869273013, 0.0],[0.0, -29.5646757999, 0.0]]
        ringFistbMinRotList = [[0.0, 0.0, 0.0],[1.44764159413, -25.6759372289, 0.0],[0.0, -28.0461595706, 0.0],[0.0, -29.2715641599, 0.0]]
        pinkyFistbMinRotList = [[0.0, 0.0, 0.0],[3.37166184668, -27.4071741155, -1.16628417085],[0.0, -27.2388580576, 0.0],[0.0, -28.4642617121, 0.0]]

        indexAppendMinRotList.append(indexFistbMinRotList)
        
        #relax_a        
        #relax_a max(10) val:        
        indexRelaxaMaxRotList = [[0.0, 0.0, 0.0],[-0.89780606, -8.5116474, -9.925511],[0.0, 15.239331, 0.0],[0.0, 15.239331, 0.0]]
        midRelaxaMaxRotList = [[0.0, 0.0, 0.0],[-0.14373821, 4.6882137, -0.50410896],[0.0, 32.523238, 0.0],[0.0, 32.523238, 0.0]]
        ringRelaxaMaxRotList = [[-2.9928762, 0.0, 0.0],[4.1312803, 15.615173, 7.78713],[0.0, 30.371118, 0.0],[0.0, 30.371118, 0.0]]
        pinkyRelaxaMaxRotList = [[-1.8613005, 0.056215787, 1.7302502],[12.382909, 26.61312, 15.826518],[0.0, 45.728939, 0.0],[0.0, 45.728939, 0.0]]
                
        indexAppendMaxRotList.append(indexRelaxaMaxRotList)
        
        #relax_a  min(-3)val:          
        indexRelaxaMinRotList = [[0.0, 0.0, 0.0],[0.0, 2.55349438396, 2.97765346574],[0.0, -4.57179902403, 0.0],[0.0, -4.57179902403, 0.0]]
        midRelaxaMinRotList = [[0.0, 0.0, 0.0],[0.0, -1.40646424112, 0.0],[0.0, -9.75697114332, 0.0],[0.0, -9.75697114332, 0.0]]
        ringRelaxaMinRotList = [[0.897862892745, 0.0, 0.0],[-1.23938408908, -4.68455226138, -2.33613911906],[0.0, -9.11133613376, 0.0],[0.0, -9.11133613376, 0.0]]
        pinkyRelaxaMinRotList = [[0.0, 0.0, 0.0],[-3.7148726673, -7.98393590273, -4.74795583361],[0.0, -13.7186819746, 0.0],[0.0, -13.7186819746, 0.0]]
         
        indexAppendMinRotList.append(indexRelaxaMinRotList) 
        
        #relax_b        
        #relax_b max(10) val:        
        indexRelaxbMaxRotList = [[0.0, 0.0, 0.0],[4.6833866, 5.8816114, -0.1751071],[0.0, 10.100644, 0.0],[0.0, 10.100644, 0.0]]
        midRelaxbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 15.223175, 0.0],[0.0, 10.308678, 0.0],[0.0, 10.308678, 0.0]]
        ringRelaxbMaxRotList = [[0.0, 0.0, 0.0],[-8.0276, 17.893472, 1.7329901],[0.0, 14.285307, 0.0],[0.0, 14.285307, 0.0]]
        pinkyRelaxbMaxRotList = [[0.0, 0.0, 0.0],[-10.137134, 20.327381, 2.100268],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
         
        indexAppendMaxRotList.append(indexRelaxbMaxRotList)
        
        #relax_b min(-3) val: 
        indexRelaxbMinRotList = [[0.0, 0.0, 0.0],[-1.40501603744, -1.76448329217, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
        midRelaxbMinRotList = [[0.0, 0.0, 0.0],[0.0, -4.56695278412, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
        ringRelaxbMinRotList = [[0.0, 0.0, 0.0],[2.40827997571, -5.36804128933, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
        pinkyRelaxbMinRotList = [[0.0, 0.0, 0.0],[3.04113989245, -6.09821425613, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
                 
        indexAppendMinRotList.append(indexRelaxbMinRotList)
            
        #relax_c        
        #relax_c max(10) val:        
        indexRelaxcMaxRotList = [[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[0.0, 22.91704, 0.0],[0.0, 22.91704, 0.0]]
        midRelaxcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 46.799998, 0.0],[0.0, 38.519999, 0.0],[0.0, 38.519999, 0.0]]
        ringRelaxcMaxRotList = [[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 43.664156, 0.0],[0.0, 43.664156, 0.0]]
        pinkyRelaxcMaxRotList = [[-2.8230663, 0.0, 0.0],[-3.8132578, 54.511244, 5.3288443],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
                         
        indexAppendMaxRotList.append(indexRelaxcMaxRotList)        
        
        #relax_c min(-3) val:
        indexRelaxcMinRotList = [[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -6.87511250747, 0.0],[0.0, -6.87511250747, 0.0]]
        midRelaxcMinRotList = [[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
        ringRelaxcMinRotList = [[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -13.099245447, 0.0],[0.0, -13.099245447, 0.0]]
        pinkyRelaxcMinRotList = [[0.0, 0.0, 0.0],[1.14397733976, -16.3533737924, -1.59865341533],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
                 
        indexAppendMinRotList.append(indexRelaxcMinRotList)
        
        #relax_d        
        #relax_d max(10) val:              
        indexRelaxdMaxRotList = [[0.0, 0.0, 0.0],[5.4160948, 12.535184, 1.2137211],[0.0, 10.100644, -1.7270777e-08],[6.8093491e-09, 10.100644, -1.6329651e-08]]
        midRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-1.7709299, 22.999166, -1.5032809],[6.9404626e-09, 10.308678, -1.6351366e-08],[9.7545475e-09, 10.308678, -1.4845411e-08]]
        ringRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-9.0447572, 27.937911, -2.3253179],[8.2228049e-09, 14.285307, -1.5505428e-08],[1.1794547e-08, 14.285307, -1.2996997e-08]]
        pinkyRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-15.723218, 33.076844, -1.6909839],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
        
        indexAppendMaxRotList.append(indexRelaxdMaxRotList)  

        #relax_d min(-3) val:
        indexRelaxdMinRotList = [[0.0, 0.0, 0.0],[-1.62482857459, -3.76055524696, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
        midRelaxdMinRotList = [[0.0, 0.0, 0.0],[0.0, -6.89974964616, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
        ringRelaxdMinRotList = [[0.0, 0.0, 0.0],[2.71342718955, -8.38137266181, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
        pinkyRelaxdMinRotList = [[0.0, 0.0, 0.0],[4.71696534913, -9.92305375801, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
                         
        indexAppendMinRotList.append(indexRelaxdMinRotList)
        
        #relax_e         
        #relax_e max(10) val:                     
        indexRelaxeMaxRotList = [[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[9.2055523e-09, 5.0979753, -1.5113549e-08],[1.0512118e-08, 12.199657, -1.4235765e-08]]
        midRelaxeMaxRotList = [[0.0, 0.0, 0.0],[0.0, 46.799998, 1.7771855e-08],[0.0, 38.519999, 2.5966873e-08],[0.0, 38.519999, 2.1833783e-07]]
        ringRelaxeMaxRotList = [[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 47.306373, 0.0],[0.0, 47.306373, 0.0]]
        pinkyRelaxeMaxRotList = [[-2.8230663, 0.0, 0.0],[-11.348742, 55.622932, 9.5249724],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
                 
        indexAppendMaxRotList.append(indexRelaxeMaxRotList)          
                
        #relax_e min(-3) val:
        indexRelaxeMinRotList = [[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -1.52939260387, 0.0],[0.0, -3.65989711932, 0.0]]
        midRelaxdMinRotList = [[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
        ringRelaxdMinRotList = [[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -14.1919116307, 0.0],[0.0, -14.1919116307, 0.0]]
        pinkyRelaxdMinRotList = [[0.0, 0.0, 0.0],[3.4046228407, -16.6868815882, -2.85749193878],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
                 
        indexAppendMinRotList.append(indexRelaxeMinRotList)        
                
                
                
                
                
                
                
                
                
                
                

        

        
        #set attr list:
        indexRotAttrs = []
        
        for selfAttr in self.attrs:
            #set attr
            for indexSdk in self.indexSdks:
                for ch in chr:
                    attr = indexSdk + '.r' + ch
                    indexRotAttrs.append(attr)            

            #set default(0) sdk
            #set index default:
            for indexSdk in self.indexSdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(indexSdk + '.r' + ch,v = 0, 
                                         cd = self.lm.config_node.control + '.' + selfAttr,dv = 0)            
                      
        #get/set rotate Max val to main rot list:
        #get index list
        for number,valueList in enumerate(indexAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    indexMainMaxRotList.append(val)
        print indexMainMaxRotList
        
        #set dic max(10) val
        for number,attrList in enumerate(indexRotAttrs):
            pm.setDrivenKeyframe(attrList,v = indexMainMaxRotList[number],
                                 cd = self.lm.config_node.control + '.' + self.attrs[number/12],dv = 10)    
            
        #get/set rotate Min val to main rot list:
        #get index list
        for number,valueList in enumerate(indexAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    indexMainMinRotList.append(val)
        print indexMainMinRotList
        
        #set dic max(-3) val
        for number,attrList in enumerate(indexRotAttrs):
            pm.setDrivenKeyframe(attrList,v = indexMainMinRotList[number],
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

        

        
        
        
