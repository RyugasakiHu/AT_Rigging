#import maya.cmds as mc
import pymel.core as pm
from Utils import nameUtils,xformUtils
#que getparent()

class Control(object):

    def __init__(self, side,baseName,size,aimAxis = 'X'):
    
        self.baseName = baseName
        self.side = side
#         self.objColor = objColor
        self.size = size
#         self.cntSize = cntSize
        self.aimAxis = aimAxis
     
        self.control = None
        self.controlGrp = None
        self.controlName = None
     
    def circleCtrl(self):
         
        self.__buildName()
        
        if self.controlName :
            #que
            self.control = pm.circle(name = self.controlName,ch = 0,o = 1 ,nr = [1,0,0],r = self.size)[0]
            #self.control = mc.circle(n = self.controlName,ch = 0,o = 1,nr = (1,0,0))

        self.__finalizeCc()       
        self.__colorSet() 
        
    def cogCtrlTest(self):
        self.__buildHierachyName()
        if not self.controlName :
            return
         
        self.control = pm.curve(name = self.controlName,d = 3,
                                p = [(-10,0,0),(-10,0,0),(-10,0,0),(-6,0,-4),(-6,0,-4),(-6,0,-2),(-6,0,-2),(-4,0,-2),
                                     (-4,0,-2),(-4,0,-4),(-2,0,-4),(-2,0,-4),(-2,0,-6),(-2,0,-6),(-4,0,-6),(-4,0,-6),
                                     (0,0,-10),(0,0,-10),(0,0,-10),(4,0,-6),(4,0,-6),(4,0,-6),(2,0,-6),(2,0,-6),(2,0,-4),
                                     (2,0,-4),(4,0,-4),(4,0,-2),(4,0,-2),(6,0,-2),(6,0,-2),(6,0,-4),(6,0,-4),(10,0,0),
                                     (10,0,0),(10,0,0),(6,0,4),(6,0,4),(6,0,4),(6,0,2),(6,0,2),(4,0,2),(4,0,2),(4,0,4),
                                     (2,0,4),(2,0,4),(2,0,6),(2,0,6),(4,0,6),(4,0,6),(0,0,10),(0,0,10),(0,0,10),(-4,0,6),
                                     (-4,0,6),(-4,0,6),(-2,0,6),(-2,0,6),(-2,0,4),(-2,0,4),(-4,0,4),(-4,0,2),(-4,0,2),
                                     (-6,0,2),(-6,0,2),(-6,0,4),(-6,0,4),(-10,0,0),(-10,0,0),(-10,0,0)],
                                k = [0,0,0,1,2,3,4,5,6,7,8,9,10,
                                     11,12,13,14,15,16,17,18,19,20,
                                     21,22,23,24,25,26,27,28,29,30,
                                     31,32,33,34,35,36,37,38,39,40,
                                     41,42,43,44,45,46,47,48,49,50,
                                     51,52,53,54,55,56,57,58,59,60,
                                     61,62,63,64,65,66,67,67,67]) 
#         self.__finalizeCc()  
        self.__colorSet()     
        
    def ifkSwitch(self):
        '''
        curve -d 1 -p -4 0 0 -p -2 2 0 -p -2 1 0 -p 2 1 0 -p 2 2 0 -p 4 0 0 
        -p 2 -2 0 -p 2 -1 0 -p -2 -1 0 -p -2 -2 0 
        -p -4 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 ;
        '''
        self.__buildName()
        if not self.controlName :
            return
        
        self.control = pm.curve(name = self.controlName,d = 1,p = [(-4,0,0),(-2,2,0),(-2,1,0),(2,1,0),(2,2,0),
                                                                   (4,0,0),(2,-2,0),(2,-1,0),(-2,-1,0),(-2,-2,0),(-4,0,0)],
                                k = [0,1,2,3,4,5,6,7,8,9,10])
        
    def ikCtrl(self):
         
        self.__buildName()
        
        if self.controlName :
            #que
            self.control = pm.circle(name = self.controlName,ch = 0,o = 1 ,nr = [0,1,0])[0]
            #self.control = mc.circle(n = self.controlName,ch = 0,o = 1,nr = (1,0,0))
            for i in range(4):
                i = 2 * i  + 1
                pm.select(self.control + '.cv[' + str(i) +']',add = 1)
            pm.move(0,0.5,0,r = 1)
            pm.scale(0.5,0.5,0.5,p = (0,0.5,0),r = 1)
            pm.select(cl = 1)

            for t in range(4):
                t = 2 * t 
                pm.select(self.control + '.cv[' + str(t) +']',add = 1)
            pm.move(0,-1,0,r = 1)                
            pm.scale(2.5,2.5,2.5,p = (0,-0.5,0),r = 1)
            pm.move(self.control+'.scalePivot',self.control+'.rotatePivot',r = (0,0,0))

        self.__finalizeCc()  
        self.__colorSet()     
        
    def poleCtrl(self):
        '''
        'charlie01_l_elbow01_pole_cc' 
        '''
        self.__buildName()
        
        if self.controlName :
            #que
            self.control = pm.sphere(name = self.controlName,ch = 0,o = 1,po = 0 ,r = 1,ax = [0,1,0],nsp = 8)[0]
            #self.control = mc.circle(n = self.controlName,ch = 0,o = 1,nr = (1,0,0))
            pm.disconnectAttr(self.control.getShape().instObjGroups[0],'initialShadingGroup.dagSetMembers[0]')
            
        self.__finalizeCc()   
        self.__colorSet()        
        
    def pinCtrl(self):
        
        self.__buildName()
        
        if not self.controlName :
            return 
        line = pm.curve(d = 1,p = [(0,0,0),(0.8,0,0)], k = [0,1],n = self.controlName)
        circle = pm.circle(ch = 1,o = True,nr = (0,1,0),r=0.1)[0]
        #line = mc.curve(n = self.controlName,d = 1,p = [(0,0,0),(0.8,0,0)],k = [0,1])
        #circle = mc.circle(n = 'temp',ch = 1,o = 1,nr = (0,1,0),r = 0.1)
        #cmds.getAttr('curve1.controlPoints',size=True)
        #cmds.getAttr('curve1.cv[*]')
        
        
        pm.move(0.9,0,0,circle.getShape().cv,r = 1)
        pm.parent(circle.getShape(),line,shape = 1,add = 1)    
        #mc.move(0.9,0,0,circle[0] + '.cv[0:7]',r = 1) 
        #mc.parent(circle[0] + 'Shape',line,shape = 1,add = 1)
         
        pm.delete(circle)
        pm.select(cl = 1)    
        #mc.delete(circle)
        #mc.select(cl = 1)
        
        self.control = line
        
        self.__finalizeCc()
        self.__colorSet()    
          
    def pinNewCtrl(self):
        
        self.__buildName()
        
        if not self.controlName :
            return
        
        self.control = pm.curve(name = self.controlName,d = 3,p = [(0,0,0),(0,0,0),(3,0,-0.5),(3,0,-0.5),(5,0,-3),(7.5,0,0),(5,0,3),(3,0,0.5),(3,0,0.5),(0,0,0)],
                 k = [0,0,0,1,2,3,4,5,6,7,7,7])
        pm.setAttr(self.controlName + '.rz',180)
        pm.makeIdentity(self.controlName,a = 1,t = 1, r = 1,s = 1,n = 0,pn = 1)
        self.__finalizeCc()
        self.__colorSet()    
                  
    def __buildName(self):
        
        self.controlName = nameUtils.getUniqueName(self.side,self.baseName,'cc')
        
    def __buildHierachyName(self):
        
        self.controlName = nameUtils.getHierachyName(self.baseName + '_TRS','cc')    
        
    def __finalizeCc(self):
        
        self.__aimCc()
        
#         if self.size != 1:
#             
#             for s in self.control.getShapes():
#                 
#                 pm.scale(s.cv,self.size,self.size,self.size,r = 1)
#                 pm.delete(self.control,ch = 1)
        
        self.controlGrp = xformUtils.zero(self.control)
    
    def __aimCc(self):
        
        y = 0
        z = 0
        
        
        if self.aimAxis == 'y':
            z = 90
          
        if self.aimAxis == 'z':
            y = -90   
    
        for s in self.control.getShapes():
            pm.rotate(s.cv,0,y,z,r = 1)
            
    def __colorSet(self):
        '''
        this def set the color,c = yellow,l = blue,r = red
        '''
        self.control.getShape().overrideEnabled.set(1)
        if self.side == 'c':
            self.control.getShape().overrideColor.set(17) 
        elif self.side == 'l':
            self.control.getShape().overrideColor.set(6) 
        elif self.side == 'r':        
            self.control.getShape().overrideColor.set(13)        
            
def lockAndHideAttr(objName,attrs):
    '''
    this function lock and Hide attrs
    @para attrs: list
    '''
    
    if not objName:
        return
    
    for attr in attrs:
        pm.setAttr(objName + "." + attr,l=True,k=False,cb=False)
        
def addSwitchAttr(objName,attrs):
    
    '''
    this function lock and Hide attr
    @para attrs: list 
    '''
    
    if not objName:
        return 
    for attr in attrs:
        pm.addAttr(objName, ln = attr, at ="float",min = 0,max = 1,dv = 0,h = False,k = True )
                        
        
# from Modules import control
# cnt = control.Control()
# cnt.circleCtrl()        
