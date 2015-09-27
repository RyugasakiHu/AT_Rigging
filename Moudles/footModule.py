import pymel.core as pm
from subModules import fkChain,ikChain,boneChain
from Utils import nameUtils
from Modules import control,hierarchy,legModule

class FootModule(object):

    posArray = [[6,2,0],[6,0,-1],[6,0,4],[4,0,2],[8,0,2],[6,0,2]]
    rotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self, baseName = 'foot',side = 'l',size = 1.5,
                 controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = side
        self.size = size
        
        '''
        self para
        '''
        
        #jj
        self.footChain = None
        self.sklGrp = None
        
        #cc 
        self.footCtrl = None
        
        #guides 
        self.guides = None
        
        #namelist
        self.locNameList = ['ankle','heel','toe','inside','outside','ball']
        self.footNameList = ['ankle','ball','toe','heel']
        
    def buildGuides(self):
        
        self.guides = []
        
        #set loc pos
        for i,p in enumerate(self.posArray):
            locName = nameUtils.getUniqueName(self.side,self.locNameList[i],'loc')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(p)
            self.guides.append(loc)        
         
        tempGuides = list(self.guides)
        tempGuides.reverse()
         
        for i in range(len(tempGuides)):
            if i != (len(tempGuides) - 1):
                pm.parent(tempGuides[i],tempGuides[i + 1])
         
    def build(self):
        
        print self.guides
        self.guidePos = [x.getTranslation(space = 'world') for x in self.guides[0],self.guides[-1],self.guides[2],self.guides[1]]
        self.guideRot = [x.getRotation(space = 'world') for x in self.guides[0],self.guides[-1],self.guides[2],self.guides[1]]

        #foot jj
        self.footChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.footChain.fromList(self.guidePos,self.guideRot)

        for num,joint in enumerate(self.footChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'jj')
            pm.rename(joint,name)
        
        self.footChain.chain[-1].setParent(self.footChain.chain[0])
        self.__addCtrl()
        self.__connectAttr()
#         self.__cleanUp()

    def __addCtrl(self):
        
#         ccName = nameUtils.getUniqueName(self.side,self.baseName,'CONFIG')
        self.footCtrl = control.Control(self.side,self.baseName,self.size) 
        self.footCtrl.circleCtrl()
        self.footCtrl.control.rotateZ.set(90)
        pm.makeIdentity(apply = 1,t = 0,r = 1,s = 0,pn = 1)
        pm.xform(self.footCtrl.controlGrp,ws = 1,matrix = self.guides[0].worldMatrix.get())
        pm.move(0,-self.guidePos[0][1],0,self.footCtrl.control + '.cv[0:7]',r = 1)
        self.footChain.chain[0].setParent(self.footCtrl.control)
        self.footCtrl.control.t.lock(1)
        self.footCtrl.control.s.lock(1)
        self.footCtrl.control.v.lock(1)
        control.lockAndHideAttr(self.footCtrl.control,["tx","ty","tz","sy","sz","v","sx"])

        self.footCtrl.control.addAttr('________',at = 'double',min = 0,max = 0,dv = 0)
        pm.setAttr(self.footCtrl.control + '.________',e = 0,channelBox = 1)
        self.footCtrl.control.________.lock(1)
        
        self.footCtrl.control.addAttr('IKFK',at = 'float',min = 0,max = 1,dv = 0,k = 1)
        self.footCtrl.control.addAttr('heel_roll',at = 'double',dv = 0,k = 1)
        self.footCtrl.control.addAttr('ball_roll',at = 'double',dv = 0,k = 1)
        self.footCtrl.control.addAttr('toe_roll',at = 'double',dv = 0,k = 1)
        self.footCtrl.control.addAttr('toe_bend',at = 'double',dv = 0,k = 1)
        self.footChain.chain[0].setParent(self.guides[-1])
        self.guides[0].setParent(self.footCtrl.control)
    
    def __connectAttr(self):
        
        #name Node
        counterMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName ,'MDN')
        toePlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,self.baseName ,'PMA')

        #create Node
        counterMultipleNode = pm.createNode('multiplyDivide',n = counterMultipleNodeName)
        toePlusMinusAverageNode = pm.createNode('plusMinusAverage',n = toePlusMinusAverageNodeName)
        
        #toe_roll
        self.footCtrl.control.ball_roll.connect(self.guides[-1].rx)
        self.footCtrl.control.ball_roll.connect(counterMultipleNode.input1X)
        counterMultipleNode.input2X.set(-1)
#         counterMultipleNode.outputX.connect(self.footChain.chain[1].rz)
        self.footCtrl.control.toe_roll.connect(self.guides[2].rx)       
        
        #heel_roll
        self.footCtrl.control.heel_roll.connect(self.guides[1].rx)
#         self.footCtrl.control.IKFK.connect(legModule.LegModule.config_node.IKFK)

        #ball_roll and toe_bend
        counterMultipleNode.outputX.connect(toePlusMinusAverageNode.input3D[1].input3Dx)     
        self.footCtrl.control.toe_bend.connect(toePlusMinusAverageNode.input3D[2].input3Dx)   
        toePlusMinusAverageNode.output3Dx.connect(self.footChain.chain[1].rz)
#         self.footCtrl.control.toe_bend.connect(self.guides[1].rx)
#         self.footCtrl.control.heel_roll.connect(self.guides[1].rx)
    
    def __cleanUp(self):
        
        #jj grp 
        self.footChain.chain[0].setParent(self.footCtrl.control)

        
        
        
        
# from Modules import legModule,footModule
# lg = legModule.LegModule()
# ft = footModule.FootModule()
# lg.buildGuides()
# ft.buildGuides()
# lg.build()
# ft.build()