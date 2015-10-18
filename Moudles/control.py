#import maya.cmds as mc
import pymel.core as pm
from Utils import nameUtils,xformUtils


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
    
    def microCtrl(self):
        
        #set cc and cc limit
        self.control = pm.circle(name = self.baseName + '_cc',ch = 0,o = 1 ,nr = [0,0,1],r = 0.2)[0]
        pm.transformLimits( tx=(-1, 1), ty=(-1, 1))
        pm.transformLimits( etx=(True, True), ety=(True, True))
        lockAndHideAttr(self.control,['tz','rx','ry','rz','sx','sy','sz','v'])
        
        #set boundary
        boundary = pm.curve(name = self.baseName + '_bdr',d = 1,
                            p = [(-1,1,0),(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)],k = (0,1,2,3,4))
        boundary.getShape().overrideEnabled.set(1)
        boundary.getShape().overrideDisplayType.set(1)
        
        #group them all
        pm.group(self.control,boundary,n = self.baseName + '_cc_grp')
        
        self.__colorSet()   
        
    def circleCtrl(self):
         
        self.__buildName()
        
        if self.controlName :
            #que
            self.control = pm.circle(name = self.controlName,ch = 0,o = 1 ,nr = [1,0,0],r = self.size)[0]
            #self.control = mc.circle(n = self.controlName,ch = 0,o = 1,nr = (1,0,0))

        self.__finalizeCc()       
        self.__colorSet() 
        
    def bodyCtrl(self):

        self.__buildName()
        
        if self.controlName :
            #que
            insideCircle = pm.circle(name = self.controlName,ch = 0,o = 1 ,nr = [1,0,0],r = self.size)
            outsideCircleF = pm.circle(name = self.controlName,ch = 0,o = 1 ,nr = [1,0,0],r = self.size * 3 / 4)
            outsideCircleB = pm.circle(name = self.controlName,ch = 0,o = 1 ,nr = [1,0,0],r = self.size * 3 / 4)
            
            pm.move(0.5,0,0,outsideCircleF[0].getShape().cv,r = 1)
            pm.parent(outsideCircleF[0].getShape(),insideCircle,shape = 1,add = 1)
            pm.delete(outsideCircleF)

            pm.move(-0.5,0,0,outsideCircleB[0].getShape().cv,r = 1)
            pm.parent(outsideCircleB[0].getShape(),insideCircle,shape = 1,add = 1)   
            pm.delete(outsideCircleB)   

        self.control = insideCircle[0]
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
    
    def ikfkBlender(self):
        
        self.__buildName()
        
        if self.controlName :
            
            self.control = pm.curve(name = self.controlName , d = 1,p = [(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,0.5,-0.5),(-0.5,0.5,-0.5),
                                                          (-0.5,0.5,0.5),(-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),
                                                          (0.5,-0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),(0.5,-0.5,0.5),
                                                          (0.5,0.5,0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,-0.5),
                                                          (-0.5,0.5,-0.5)],k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
            
            F = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'FK')
            I = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'I')
            text = ['F','K','I']
            selectionList = pm.ls("curve*")
            self.textObj = [] 
            for num,sl in enumerate(selectionList):
                if num <= 2:
                    pm.parent(sl,w = 1)   
                    name = pm.rename(sl,text[num])
                    pm.setAttr(text[num] + '.overrideEnabled',1)
                    pm.setAttr(text[num] + '.overrideDisplayType',2)
                    self.textObj.append(name)
            pm.delete('Text*')      
            pm.move(self.textObj[0],-1,0.6,0)
            pm.move(self.textObj[1],0,0.6,0)
            pm.move(self.textObj[2],-0.6,0.6,0)
            pm.makeIdentity(self.textObj[0],apply = 1,t = 1,r = 0,s = 0,n = 0,pn = 1)
            pm.makeIdentity(self.textObj[1],apply = 1,t = 1,r = 0,s = 0,n = 0,pn = 1)
            pm.makeIdentity(self.textObj[2],apply = 1,t = 1,r = 0,s = 0,n = 0,pn = 1)
            pm.parent(self.textObj[0],self.control)
            pm.parent(self.textObj[1],self.control)
            pm.parent(self.textObj[2],self.control)

        self.__finalizeCc()       
        self.__colorSet() 
        
    def ifkSwitch(self):

        self.__buildName()
        if not self.controlName :
            return
        
        self.control = pm.curve(name = self.controlName,d = 1,p = [(-4,0,0),(-2,2,0),(-2,1,0),(2,1,0),(2,2,0),
                                                                   (4,0,0),(2,-2,0),(2,-1,0),(-2,-1,0),(-2,-2,0),(-4,0,0)],
                                k = [0,1,2,3,4,5,6,7,8,9,10])
        
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
            pm.disconnectAttr(self.control.getShape().instObjGroups[0],'initialShadingGroup.dagSetMembers[0]')
            
        self.__finalizeCc()   
        self.__colorSet()        
        
    def pinCtrl(self):
        
        self.__buildName()
        
        if not self.controlName :
            return 
        line = pm.curve(d = 1,p = [(0,0,0),(0.8,0,0)], k = [0,1],n = self.controlName)
        circle = pm.circle(ch = 1,o = True,nr = (0,1,0),r=0.1)[0]
        
        pm.move(0.9,0,0,circle.getShape().cv,r = 1)
        pm.parent(circle.getShape(),line,shape = 1,add = 1)    
         
        pm.delete(circle)
        pm.select(cl = 1)    
        
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
        for shape in self.control.getShapes():
            #open override
            shape.overrideEnabled.set(1)
            if self.side == 'm':
                shape.overrideColor.set(17) 
            elif self.side == 'l':
                shape.overrideColor.set(6) 
            elif self.side == 'r':        
                shape.overrideColor.set(13)        
            
def lockAndHideAttr(objName,attrs):
    '''
    this function lock and Hide attrs
    @para attrs: list
    '''
    
    if not objName:
        return
    
    for attr in attrs:
        pm.setAttr(objName + "." + attr,l=True,k=False,cb=False)
                        
def addFloatAttr(objName,attrs,minV,maxV):
    
    '''
    this function add single/multiple attr
    @para attrs: list 
    '''
    
    if not objName:
        return 
    for attr in attrs:
        pm.addAttr(objName, ln = attr, at ="double",min = minV,max = maxV,dv = 0,h = False,k = True )
        
# from Modules import control
# cnt = control.Control(side = 'r',baseName = 'aaa',size = 1.5)
# cnt.circleCtrl()        
