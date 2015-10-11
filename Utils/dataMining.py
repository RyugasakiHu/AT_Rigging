import pymel.core as pm
from see import see
cc = pm.selected(flatten = 1)[0]

indexSdks = ['L_fingerB0_HandDrv_sdk','L_fingerB1_HandDrv_sdk',
            'L_fingerB2_HandDrv_sdk','L_fingerB3_HandDrv_sdk']
            
midSdks = ['L_fingerC0_HandDrv_sdk','L_fingerC1_HandDrv_sdk',
          'L_fingerC2_HandDrv_sdk','L_fingerC3_HandDrv_sdk']
          
ringSdks = ['L_fingerD0_HandDrv_sdk','L_fingerD1_HandDrv_sdk',
            'L_fingerD2_HandDrv_sdk','L_fingerD3_HandDrv_sdk']

pinkySdks = ['L_fingerE0_HandDrv_sdk','L_fingerE1_HandDrv_sdk',
             'L_fingerE2_HandDrv_sdk','L_fingerE3_HandDrv_sdk']         
         
attrs = ['fist']      
         
#attrs = ['fist','relaxA','relaxB','relaxC','grab','hand',
#         'palm1','palm2','fa1','fa2','fb','fc','fd','fe',
#         'fistB','close_relax','relaxD','relaxE','Grab2',
#         'spread2','point','Fa3','Fa4',]            
         
for num,attr in enumerate(attrs):
    
    indexMaxAttrs = []
    midMaxAttrs = []
    ringMaxAttrs = []
    pinkyMaxAttrs = []
    
    indexMinAttrs = []
    midMinAttrs = []
    ringMinAttrs = []
    pinkyMinAttrs = []
    
    #max val 10
    pm.setAttr(cc + ' . ' +attr,10)
    
    #index data
    for indexSdk in indexSdks:
        indexData = pm.getAttr(indexSdk + '.r')
        indexMaxAttrs.append(indexData)
    print 'indexMaxAttrs: ' + str(attr) + ' 10:' + str(list(indexMaxAttrs))        
    
    #mid data
    for midSdk in midSdks:    
        midData = pm.getAttr(midSdk + '.r')
        midMaxAttrs.append(midData)
    print 'midMaxAttrs: ' + str(attr) + ' 10:' + str(list(midMaxAttrs))    
    
    #ring data
    for ringSdk in ringSdks:    
        ringData = pm.getAttr(ringSdk + '.r')
        ringMaxAttrs.append(ringData)
    print 'ringMaxAttrs: ' + str(attr) + ' 10:' + str(list(ringMaxAttrs))     
    
    #pinky ring data
    for pinkySdk in pinkySdks:    
        pinkyData = pm.getAttr(pinkySdk + '.r')
        pinkyMaxAttrs.append(pinkyData)
    print 'pinkyMaxAttrs: ' + str(attr) + ' 10:' + str(list(pinkyMaxAttrs))       
    print ''
    
    #min val -3
    pm.setAttr(cc + ' . ' +attr,-3)
    #index data
    for indexSdk in indexSdks:
        indexData = pm.getAttr(indexSdk + '.r')
        indexMinAttrs.append(indexData)
    print 'indexMinAttrs: ' + str(attr) + ' -3:' + str(list(indexMinAttrs))        
    
    #mid data
    for midSdk in midSdks:    
        midData = pm.getAttr(midSdk + '.r')
        midMinAttrs.append(midData)
    print 'midMinAttrs: ' + str(attr) + ' -3:' + str(list(midMinAttrs))    
    
    #ring data
    for ringSdk in ringSdks:    
        ringData = pm.getAttr(ringSdk + '.r')
        ringMinAttrs.append(ringData)
    print 'ringMinAttrs: ' + str(attr) + ' -3:' + str(list(ringMinAttrs))     
    
    #pinky ring data
    for pinkySdk in pinkySdks:    
        pinkyData = pm.getAttr(pinkySdk + '.r')
        pinkyMinAttrs.append(pinkyData)
    print 'pinkyMinAttr: ' + str(attr) + ' -3:' + str(list(pinkyMinAttrs))       
    print ''
    pm.setAttr(cc + ' . ' +attr,0)
    
# indexMaxAttrs: fist 10:[[0.0, 1.1667451, 0.0], [12.409078, 104.3535714, -7.0976769], [-5.0864835, 119.229424, -14.33877], [0.0, 131.453704, 0.0]]
# midMaxAttrs: fist 10:[[0.0, 0.0, 0.0], [1.343452, 109.467935, -0.17447495], [-1.2531719, 121.591538, -3.2134328], [0.0, 121.626688, 0.0]]
# ringMaxAttrs: fist 10:[[-2.2915976, 0.99224884, 0.3515861], [-9.681804, 112.122819, 9.9512199], [1.4022289, 121.379307, 4.5496722], [0.0, 132.503787, 0.0]]
# pinkyMaxAttrs: fist 10:[[-3.4711895, 4.0933869, 1.0393476], [-14.045815, 124.603571, 18.953533], [3.2222396, 118.352933, 14.587789], [0.0, 112.539969, 0.0]]
# 
# indexMinAttrs: fist -3:[[0.0, 0.0, 0.0], [2.3656792422, -23.6599771482, 1.9016638177], [1.52594527386, -22.6379875224, 4.30163088994], [0.0, -26.3052739235, 0.0]]
# midMinAttrs: fist -3:[[0.0, 0.0, 0.0], [0.0, -13.0502537762, 0.0], [0.0, -23.0761814451, 0.964029917432], [0.0, -23.0867256252, 0.0]]
# ringMinAttrs: fist -3:[[0.0, 0.0, 0.0], [-8.0276, -10.3753295339, -0.732478856346], [0.0, -17.8428903421, -1.36490170652], [0.0, -21.1802374187, 0.0]]
# pinkyMinAttr: fist -3:[[1.04135682811, -1.22801612104, 0.0], [-8.96452963728, -10.9554773142, -2.95571135541], [-0.966671923269, -14.4907648544, -4.37633648762], [0.0, -12.7468772018, 0.0]]
    
