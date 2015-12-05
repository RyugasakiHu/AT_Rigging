#import maya.cmds as mc
import pymel.core as pm
from Utils import nameUtils,xformUtils


class Control(object):

    def __init__(self, side,baseName,size,aimAxis = 'x',sub = 0):
    
        self.baseName = baseName
        self.side = side
        self.size = size
        self.aimAxis = aimAxis
        self.sub = sub
     
        self.control = None
        self.controlGrp = None
        self.controlName = None
    
    def microCtrl(self):
        
        self.__buildName()
        
        #set cc and cc limit
        self.control = pm.circle(name = self.controlName,ch = 0,o = 1 ,nr = [0,0,1],r = 0.2)[0]
        pm.transformLimits( tx=(-1, 1), ty=(-1, 1))
        pm.transformLimits( etx=(True, True), ety=(True, True))
        
        #set boundary
        boundaryName = nameUtils.getUniqueName(self.side,self.baseName,'bdr')
        boundary = pm.curve(name = boundaryName,d = 1,
                            p = [(-1,1,0),(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)],k = (0,1,2,3,4))
        boundary.getShape().overrideEnabled.set(1)
        boundary.getShape().overrideDisplayType.set(1)
        boundary.v.set(0)
        
        #group them all
        grpName = nameUtils.getUniqueName(self.side,self.baseName + '_cc','grp')
        self.controlGrp = pm.group(self.control,boundary,n = grpName)
        lockAndHideAttr(self.control,['tz','rx','ry','rz','sx','sy','sz','v'])
        self.__colorSet()   
        
    def circleCtrl(self):
         
        self.__buildName()
        
        if self.controlName :
            
            if self.aimAxis == 'x':
                dic = [1,0,0]
                
            elif self.aimAxis == 'y':
                dic = [0,1,0]
                
            elif self.aimAxis == 'z':
                dic = [0,0,1] 
                
            self.control = pm.circle(name = self.controlName,ch = 1,o = 1 ,nr = dic,r = self.size)[0]
#             self.control.s.set(self.size,self.size,self.size)
                 
        self.__finalizeCc()       
        self.__colorSet()     
        
    def circleSplitCtrl(self):
         
        self.__buildName()
        
        if self.controlName :
            
            if self.aimAxis == 'x':
                dic = [1,0,0]
                
            elif self.aimAxis == 'y':
                dic = [0,1,0]
                
            elif self.aimAxis == 'z':
                dic = [0,0,1] 
                
            self.control = pm.circle(name = self.controlName,ch = 1,o = 1 ,nr = dic,r = self.size)[0]
            line = pm.curve(d = 1,p = [(-dic[1],-dic[2],-dic[0]),(dic[1],dic[2],dic[0])], k = [0,1],n = nameUtils.getUniqueName(self.side,'circleV','cc'))
            pm.parent(line.getShape(),self.control,shape = 1,add = 1)
            self.control.s.set(self.size,self.size,self.size)
            pm.delete(line)
                 
        self.__finalizeCc()       
        self.__colorSet() 
        
    def cubeCtrl(self):
        
        self.__buildName()
        
        if self.controlName :
            self.control = pm.curve(name = self.controlName,d = 1,
                                    p = [(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,0.5,-0.5),(-0.5,0.5,-0.5),(-0.5,0.5,0.5),
                                         (-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),
                                         (0.5,-0.5,0.5),(0.5,0.5,0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,-0.5),
                                         (-0.5,0.5,-0.5)],k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
            
            self.control.s.set(self.size,self.size,self.size)
            pm.makeIdentity(self.control,apply = True,t = 0,r = 0,s = 1,n = 0,pn = 1)
            
        self.__finalizeCc()       
        self.__colorSet() 
        
    def sphereCtrl(self):
        
        self.__buildName()
        
        if self.controlName :
            self.control = pm.curve(name = self.controlName,d = 1,
                                    p = [(0,3,0),(0,2,-2),(0,0,-3),(0,-2,-2),(0,-3,0),
                                         (0,-2,2),(0,0,3),(0,2,2),(0,3,0),(2,2,0),
                                         (3,0,0),(2,-2,0),(0,-3,0),(-2,-2,0),(-3,0,0),
                                         (-2,2,0),(0,3,0)],k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
            
            self.control.s.set(self.size,self.size,self.size)
            pm.makeIdentity(self.control,apply = True,t = 0,r = 0,s = 1,n = 0,pn = 1)
            
        self.__finalizeCc()       
        self.__colorSet()         
        
    def plusCtrl(self):
        
        self.__buildName()
        
        if self.controlName :
            self.control = pm.curve(name = self.controlName,d = 1,
                                    p = [(0,1,0),(0,-1,0),(0,0,0),(-1,0,0),(1,0,0),
                                         (0,0,0),(0,0,1),(0,0,-1)],k = [0,1,2,3,4,5,6,7])
            
            self.control.s.set(self.size / 2,self.size / 2,self.size / 2)
            pm.makeIdentity(self.control,apply = True,t = 0,r = 0,s = 1,n = 0,pn = 1)
            
        self.__finalizeCc()       
        self.__colorSet()            
        
    def bodyCtrl(self):

        self.__buildName()
        
        if self.controlName :
            
            dic = None
            coords = []
            
            if self.aimAxis == 'x':
                dic = [1,0,0]
                for xyz in dic:
                    coord = xyz * float(self.size / 3) 
                    coords.append(coord)
                
            elif self.aimAxis == 'y':
                dic = [0,1,0]
                for xyz in dic:
                    coord = xyz * float(self.size / 3) 
                    coords.append(coord)
                
            elif self.aimAxis == 'z':
                dic = [0,0,1]
                for xyz in dic:
                    coord = xyz * float(self.size / 3) 
                    coords.append(coord)
            
            insideCircle = pm.circle(name = self.controlName,ch = 1,o = 1 ,nr = dic,r = self.size)
            arrow = pm.curve(n = self.controlName + 'Arrow',d = 1 ,p = [[0,4,0],[-2,0,0],[0,1,0],[2,0,0],[0,4,0]],k = [0,1,2,3,4])
            pm.move(0,2,0,arrow + '.rotatePivot')
            pm.move(0,2,0,arrow + '.scalePivot')
            pm.move(0,-2,0,arrow)
#             arrow.r.set(90 * dic[0],90 * dic[1],90 * dic[1])
            arrow.s.set(0.35,0.35,0.35)
            pm.makeIdentity(arrow,apply = True, t = 1,r = 1 ,s = 1,n = 0,pn = 1)
            arrowObj = pm.selected()
            pm.parent(arrowObj[0].getShape(),insideCircle,shape = 1,add = 1)
            pm.delete(arrowObj[0])
            
            
            outsideCircleF = pm.circle(name = self.controlName + 'Front',ch = 0,o = 1 ,nr = dic,r = self.size * 3 / 4)
            outsideCircleB = pm.circle(name = self.controlName + 'Back',ch = 0,o = 1 ,nr = dic,r = self.size * 3 / 4)
            
            pm.move(coords[0],coords[1],coords[2],outsideCircleF[0].getShape().cv,r = 1)
            pm.parent(outsideCircleF[0].getShape(),insideCircle,shape = 1,add = 1)
            pm.delete(outsideCircleF)
 
            pm.move(-coords[0],-coords[1],-coords[2],outsideCircleB[0].getShape().cv,r = 1)
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
        self.__finalizeCc()  
        self.__colorSet()     
    
    def ikfkBlender(self):
        
        self.__buildName()
        
        if self.controlName :
            
            self.textObj = [] 
            self.control = pm.curve(name = self.controlName , d = 1,p = [(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,0.5,-0.5),(-0.5,0.5,-0.5),
                                                          (-0.5,0.5,0.5),(-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),
                                                          (0.5,-0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),(0.5,-0.5,0.5),
                                                          (0.5,0.5,0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,-0.5),
                                                          (-0.5,0.5,-0.5)],k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
            
            #setName
            text = ['F','K','I']
            codeFName = nameUtils.getUniqueName(self.side,text[0],'cc')
            codeKName = nameUtils.getUniqueName(self.side,text[1],'cc')
            codeIName = nameUtils.getUniqueName(self.side,text[2],'cc')
            
            #create char
            fText = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'F')
            fObj = pm.selected()[0]
            fCc = fObj.getChildren()[0].getChildren()[0]
            fChar = pm.rename(fCc,codeFName)
            self.textObj.append(fChar)
            
            iText = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'I')
            iObj = pm.selected()[0]
            iCc = iObj.getChildren()[0].getChildren()[0]
            iChar = pm.rename(iCc,codeIName)
            self.textObj.append(iChar)
            
            kText = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'K')
            kObj = pm.selected()[0]
            kCc = kObj.getChildren()[0].getChildren()[0]
            kChar = pm.rename(kCc,codeKName)
            self.textObj.append(kChar)
            
            for char in self.textObj:
                pm.setAttr(char + '.overrideEnabled',1)
                pm.setAttr(char + '.overrideDisplayType',2)
                char.setParent(self.control)
                    
            pm.delete(fText,iText,kText)      
             
            pm.move(self.textObj[0],-1,0.6,0)
            pm.move(self.textObj[1],-0.6,0.6,0)
            pm.move(self.textObj[2],0,0.6,0)

            pm.makeIdentity(self.textObj[0],apply = 1,t = 1,r = 0,s = 0,n = 0,pn = 1)
            pm.makeIdentity(self.textObj[1],apply = 1,t = 1,r = 0,s = 0,n = 0,pn = 1)
            pm.makeIdentity(self.textObj[2],apply = 1,t = 1,r = 0,s = 0,n = 0,pn = 1)
            pm.parent(self.textObj[0],self.control)
            pm.parent(self.textObj[1],self.control)
            pm.parent(self.textObj[2],self.control)
 
        self.__finalizeCc()       
        self.__colorSet() 
    
    def visCtrl(self):
        self.__buildName()
        
        textList = []
            
        vText = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'V')
        vName = nameUtils.getHierachyName('visChar_V','cc')
        vObj = pm.selected()[0]
        vCc = vObj.getChildren()[0].getChildren()[0]
        pm.rename(vCc,vName)
        pm.move(vCc,-1.5,0.2,0)
        
        iText = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'I')
        iName = nameUtils.getHierachyName('visChar_I','cc')
        iObj = pm.selected()[0]
        iCc = iObj.getChildren()[0].getChildren()[0]
        pm.rename(iCc,iName)
        pm.move(iCc,-0.2,0.2,0)
        
        sText = pm.textCurves(ch = 0,f = 'Goudy Old Style|w700|h-6',t = 'S')
        sName = nameUtils.getHierachyName('visChar_S','cc')
        sObj = pm.selected()[0]
        sCc = sObj.getChildren()[0].getChildren()[0]
        pm.rename(sCc,sName)
        pm.move(sCc,0.4,0.2,0)

        textList.append(vCc)
        textList.append(iCc)
        textList.append(sCc)
        
        self.control = pm.curve(n = self.controlName,d = 1,p = [[1.5,0,0],[1.5,1.8,0],[-1.9,1.8,0],[-1.9,0,0],[1.5,0,0]],k = [0,1,2,3,4])
        
        for text in textList:
            pm.makeIdentity(text,apply = True,t = 1,r = 1,s = 1,n = 0,pn = 1)
            pm.parent(text.getShape(),self.control,shape = 1,add = 1)   
        
        pm.delete(vText,iText,sText)
        lockAndHideAttr(self.control,['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])
        
        
        self.__finalizeCc()       
        self.__colorSet() 
        
    def arrow(self):

        self.__buildName()
        if not self.controlName :
            return
        
        self.control = pm.curve(name = self.controlName,d = 1,p = [(-4,0,0),(-2,2,0),(-2,1,0),(2,1,0),(2,2,0),
                                                                   (4,0,0),(2,-2,0),(2,-1,0),(-2,-1,0),(-2,-2,0),(-4,0,0)],
                                k = [0,1,2,3,4,5,6,7,8,9,10])
        
        self.__finalizeCc()       
        self.__colorSet() 
        
    def solidSphereCtrl(self):
        '''
        'charlie01_l_elbow01_pole_cc' 
        '''
        self.__buildName()
        
        if self.controlName :
            #que
            self.control = pm.sphere(name = self.controlName,ch = 0,o = 1,po = 0 ,r = float(self.size) / 4,ax = [0,1,0],nsp = 8)[0]

        for dag in self.control.getShape().instObjGroups:
            if pm.connectionInfo(dag, isSource=True):
                source = dag
                destination = pm.connectionInfo(dag, destinationFromSource=True)[0]
                pm.disconnectAttr(source,destination)
            
        self.__finalizeCc()   
        self.__colorSet()        
        
    def pinCtrl(self):
        
        self.__buildName()
        
        if not self.controlName :
            return 
        
        if self.aimAxis == 'x':
            dic = [1,0,0]
            
        elif self.aimAxis == 'y':
            dic = [0,1,0]
            
        elif self.aimAxis == 'z':
            dic = [0,0,1] 
        
        line = pm.curve(d = 1,p = [(0,0,0),(dic[0],dic[1],dic[2])], k = [0,1],n = self.controlName)
        circleH = pm.circle(ch = 1,o = True,nr = (dic[1],dic[2],dic[0]),r = 0.2,n = nameUtils.getUniqueName(self.side,'circleH','cc'))[0]
        circleV = pm.circle(ch = 1,o = True,nr = (dic[2],dic[0],dic[1]),r = 0.2,n = nameUtils.getUniqueName(self.side,'circleV','cc'))[0]
        
        pm.move(dic[0] * 1.2,dic[1] * 1.2,dic[2] * 1.2,circleH.getShape().cv,r = 1)
        pm.parent(circleH.getShape(),line,shape = 1,add = 1)    
        
        pm.move(dic[0] * 1.2,dic[1] * 1.2,dic[2] * 1.2,circleV.getShape().cv,r = 1)
        pm.parent(circleV.getShape(),line,shape = 1,add = 1)   
        
        pm.delete(circleH)
        pm.delete(circleV)
        pm.setAttr(line + '.scale',self.size,self.size,self.size)
        self.control = line
        pm.delete(self.control,ch = 1)
        
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
        
        pass
#         y = 0
#         z = 0
#         
#         
#         if self.aimAxis == 'y':
#             z = 90
#           
#         if self.aimAxis == 'z':
#             y = -90   
#     
#         for s in self.control.getShapes():
#             pm.rotate(s.cv,0,y,z,r = 1)
            
    def __colorSet(self):
        '''
        this def set the color,c = yellow,l = blue,r = red
        '''
        for shape in self.control.getShapes():
            #open override
            shape.overrideEnabled.set(1)
            if self.sub == 0:
                if self.side == 'm':
                    shape.overrideColor.set(17) 
                elif self.side == 'l':
                    shape.overrideColor.set(6) 
                elif self.side == 'r':        
                    shape.overrideColor.set(13)        
            elif self.sub == 1:
                shape.overrideColor.set(14) 
            
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
