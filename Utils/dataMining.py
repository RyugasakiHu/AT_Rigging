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
         
attrs = ['fist','relaxA','relaxB','relaxC','grab','spread','hand',
         'palm1','palm2','fa1','fa2','fb','fc','fd','fe',
         'fistB','close_relax','relaxD','relaxE','Grab2',
         'spread2','point','Fa3','Fa4',]            
         
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
    
# indexMaxAttrs: fist 10:[[0.0, 1.1667451, 0.0],[7.7256914, 98.47196, -6.9225698],[-5.0864835, 109.12878, -14.33877],[0.0, 121.35306, 0.0]]
# midMaxAttrs: fist 10:[[0.0, 0.0, 0.0],[1.343452, 94.24476, -0.17447495],[-1.2531719, 111.28286, -3.2134328],[0.0, 111.31801, 0.0]]
# ringMaxAttrs: fist 10:[[-2.2915976, 0.99224884, 0.3515861],[-1.654204, 94.229347, 8.2182298],[1.4022289, 107.094, 4.5496722],[0.0, 118.21848, 0.0]]
# pinkyMaxAttrs: fist 10:[[-3.4711895, 4.0933869, 1.0393476],[-3.908681, 104.27619, 16.853265],[3.2222396, 102.18746, 14.587789],[0.0, 96.374496, 0.0]]
# 
# indexMinAttrs: fist -3:[[0.0, 0.0, 0.0],[-2.3177073578, -29.5415885482, 2.0767709177],[1.52594527386, -32.7386315224, 4.30163088994],[0.0, -36.4059179235, 0.0]]
# midMinAttrs: fist -3:[[0.0, 0.0, 0.0],[0.0, -28.2734287762, 0.0],[0.0, -33.3848594451, 0.964029917432],[0.0, -33.3954036252, 0.0]]
# ringMinAttrs: fist -3:[[0.0, 0.0, 0.0],[0.0, -28.2688015339, -2.46546895635],[0.0, -32.1281973421, -1.36490170652],[0.0, -35.4655444187, 0.0]]
# pinkyMinAttr: fist -3:[[1.04135682811, -1.22801612104, 0.0],[1.17260436272, -31.2828583142, -5.05597935541],[-0.966671923269, -30.6562378544, -4.37633648762],[0.0, -28.9123502018, 0.0]]
# 
# indexMaxAttrs: relaxA 10:[[0.0, 0.0, 0.0],[-0.89780606, -8.5116474, -9.925511],[0.0, 15.239331, 0.0],[0.0, 15.239331, 0.0]]
# midMaxAttrs: relaxA 10:[[0.0, 0.0, 0.0],[-0.14373821, 4.6882137, -0.50410896],[0.0, 32.523238, 0.0],[0.0, 32.523238, 0.0]]
# ringMaxAttrs: relaxA 10:[[-2.9928762, 0.0, 0.0],[4.1312803, 15.615173, 7.78713],[0.0, 30.371118, 0.0],[0.0, 30.371118, 0.0]]
# pinkyMaxAttrs: relaxA 10:[[-1.8613005, 0.056215787, 1.7302502],[12.382909, 26.61312, 15.826518],[0.0, 45.728939, 0.0],[0.0, 45.728939, 0.0]]
# 
# indexMinAttrs: relaxA -3:[[0.0, 0.0, 0.0],[0.0, 2.55349438396, 2.97765346574],[0.0, -4.57179902403, 0.0],[0.0, -4.57179902403, 0.0]]
# midMinAttrs: relaxA -3:[[0.0, 0.0, 0.0],[0.0, -1.40646424112, 0.0],[0.0, -9.75697114332, 0.0],[0.0, -9.75697114332, 0.0]]
# ringMinAttrs: relaxA -3:[[0.897862892745, 0.0, 0.0],[-1.23938408908, -4.68455226138, -2.33613911906],[0.0, -9.11133613376, 0.0],[0.0, -9.11133613376, 0.0]]
# pinkyMinAttr: relaxA -3:[[0.0, 0.0, 0.0],[-3.7148726673, -7.98393590273, -4.74795583361],[0.0, -13.7186819746, 0.0],[0.0, -13.7186819746, 0.0]]
# 
# indexMaxAttrs: relaxB 10:[[0.0, 0.0, 0.0],[4.6833866, 5.8816114, -0.1751071],[0.0, 10.100644, 0.0],[0.0, 10.100644, 0.0]]
# midMaxAttrs: relaxB 10:[[0.0, 0.0, 0.0],[0.0, 15.223175, 0.0],[0.0, 10.308678, 0.0],[0.0, 10.308678, 0.0]]
# ringMaxAttrs: relaxB 10:[[0.0, 0.0, 0.0],[-8.0276, 17.893472, 1.7329901],[0.0, 14.285307, 0.0],[0.0, 14.285307, 0.0]]
# pinkyMaxAttrs: relaxB 10:[[0.0, 0.0, 0.0],[-10.137134, 20.327381, 2.100268],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
# 
# indexMinAttrs: relaxB -3:[[0.0, 0.0, 0.0],[-1.40501603744, -1.76448329217, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
# midMinAttrs: relaxB -3:[[0.0, 0.0, 0.0],[0.0, -4.56695278412, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
# ringMinAttrs: relaxB -3:[[0.0, 0.0, 0.0],[2.40827997571, -5.36804128933, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
# pinkyMinAttr: relaxB -3:[[0.0, 0.0, 0.0],[3.04113989245, -6.09821425613, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
# 
# indexMaxAttrs: relaxC 10:[[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[0.0, 22.91704, 0.0],[0.0, 22.91704, 0.0]]
# midMaxAttrs: relaxC 10:[[0.0, 0.0, 0.0],[0.0, 46.799998, 0.0],[0.0, 38.519999, 0.0],[0.0, 38.519999, 0.0]]
# ringMaxAttrs: relaxC 10:[[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 43.664156, 0.0],[0.0, 43.664156, 0.0]]
# pinkyMaxAttrs: relaxC 10:[[-2.8230663, 0.0, 0.0],[-3.8132578, 54.511244, 5.3288443],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
# 
# indexMinAttrs: relaxC -3:[[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -6.87511250747, 0.0],[0.0, -6.87511250747, 0.0]]
# midMinAttrs: relaxC -3:[[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
# ringMinAttrs: relaxC -3:[[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -13.099245447, 0.0],[0.0, -13.099245447, 0.0]]
# pinkyMinAttr: relaxC -3:[[0.0, 0.0, 0.0],[1.14397733976, -16.3533737924, -1.59865341533],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
# 
# indexMaxAttrs: grab 10:[[0.0, 0.0, 0.0],[-1.7635041, -8.5214628, -16.147383],[0.0, 41.94425, 0.0],[0.0, 44.280939, 0.0]]
# midMaxAttrs: grab 10:[[0.0, 0.0, 0.0],[-0.030713774, -5.1010537, -3.0009306],[0.0, 40.029996, 0.0],[0.0, 41.086042, 0.0]]
# ringMaxAttrs: grab 10:[[-2.9928762, 0.0, 0.0],[3.6224929, -2.4102271, 4.7080181],[0.0, 40.898433, 0.0],[0.0, 41.482517, 0.0]]
# pinkyMaxAttrs: grab 10:[[-1.8613005, 0.056215787, 1.7302502],[1.4394069, 0.14493989, 16.418532],[0.0, 43.58425, 0.0],[0.0, 52.072421, 0.0]]
# 
# indexMinAttrs: grab -3:[[0.0, 0.0, 0.0],[0.0, 2.55643895266, 4.84421472464],[0.0, -12.5832744564, 0.0],[0.0, -13.284281742, 0.0]]
# midMinAttrs: grab -3:[[0.0, 0.0, 0.0],[0.0, 1.53031619331, 0.900279164949],[0.0, -12.0089988007, 0.0],[0.0, -12.3258143315, 0.0]]
# ringMinAttrs: grab -3:[[0.897862892745, 0.0, 0.0],[-1.08674781614, 0.0, -1.4124054644],[0.0, -12.2695308218, 0.0],[0.0, -12.4447552972, 0.0]]
# pinkyMinAttr: grab -3:[[0.0, 0.0, 0.0],[0.0, 0.0, -4.92555972899],[0.0, -13.0752754812, 0.0],[0.0, -15.6217261951, 0.0]]
# 
# indexMaxAttrs: spread 10:[[0.0, 0.0, 0.0],[0.0, 0.0, -25.582658],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: spread 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: spread 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 8.8561972],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: spread 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 22.877102],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: spread -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 7.67479746336],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: spread -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: spread -3:[[0.0, 0.0, 0.0],[0.0, 0.0, -2.65685910148],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: spread -3:[[0.0, 0.0, 0.0],[0.0, 0.0, -6.86313075324],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: hand 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 5.9506481],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: hand 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.96022806],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: hand 10:[[0.0, 0.0, 0.0],[0.0, 0.0, -3.8924184],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: hand 10:[[0.0, 0.0, 0.0],[0.0, 0.0, -8.3619136],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: hand -3:[[0.0, 0.0, 0.0],[0.0, 0.0, -1.78519442026],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: hand -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: hand -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 1.16772562065],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: hand -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 2.5085741245],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: palm1 10:[[9.5015777, 0.0, 0.0],[12.129516, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: palm1 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: palm1 10:[[-24.239371, -0.30426803, -0.74108914],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: palm1 10:[[-17.534821, 1.0340395, -2.1197015],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: palm1 -3:[[-2.85047358591, 0.0, 0.0],[-3.6388550315, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: palm1 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: palm1 -3:[[7.27181158401, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: palm1 -3:[[5.2604463016, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: palm2 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: palm2 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: palm2 10:[[-6.8414008, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: palm2 10:[[-13.947657, 1.9094432, -0.4750786],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: palm2 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: palm2 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: palm2 -3:[[2.05242044873, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: palm2 -3:[[4.18429703895, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: fa1 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: fa1 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: fa1 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: fa1 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: fa1 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: fa1 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: fa1 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: fa1 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: fa2 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: fa2 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: fa2 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: fa2 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: fa2 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: fa2 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: fa2 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: fa2 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: fb 10:[[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
# midMaxAttrs: fb 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: fb 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: fb 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: fb -3:[[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
# midMinAttrs: fb -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: fb -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: fb -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: fc 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: fc 10:[[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
# ringMaxAttrs: fc 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: fc 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: fc -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: fc -3:[[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
# ringMinAttrs: fc -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: fc -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: fd 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: fd 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: fd 10:[[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
# pinkyMaxAttrs: fd 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: fd -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: fd -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: fd -3:[[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
# pinkyMinAttr: fd -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: fe 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMaxAttrs: fe 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMaxAttrs: fe 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMaxAttrs: fe 10:[[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
# 
# indexMinAttrs: fe -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: fe -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: fe -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: fe -3:[[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
# 
# indexMaxAttrs: fistB 10:[[0.0, 0.0, 0.0],[4.4223436, 66.184789, 1.8546305],[0.0, 101.20612, 0.0],[0.0, 75.878746, 0.0]]
# midMaxAttrs: fistB 10:[[0.0, 0.0, 0.0],[0.0, 81.00373, 0.0],[0.0, 97.623089, 0.0],[0.0, 98.548929, 0.0]]
# ringMaxAttrs: fistB 10:[[0.0, 0.0, 0.0],[-4.8254718, 85.586453, 2.4808469],[0.0, 93.487201, 0.0],[0.0, 97.57188, 0.0]]
# pinkyMaxAttrs: fistB 10:[[0.0, 0.0, 0.0],[-11.238872, 91.357247, 3.8876141],[0.0, 90.796196, 0.0],[0.0, 94.880874, 0.0]]
# 
# indexMinAttrs: fistB -3:[[0.0, 0.0, 0.0],[-1.32670302602, -19.8554351973, 0.0],[0.0, -30.3618382339, 0.0],[0.0, -22.7636215909, 0.0]]
# midMinAttrs: fistB -3:[[0.0, 0.0, 0.0],[0.0, -24.3011201928, 0.0],[0.0, -29.2869273013, 0.0],[0.0, -29.5646757999, 0.0]]
# ringMinAttrs: fistB -3:[[0.0, 0.0, 0.0],[1.44764159413, -25.6759372289, 0.0],[0.0, -28.0461595706, 0.0],[0.0, -29.2715641599, 0.0]]
# pinkyMinAttr: fistB -3:[[0.0, 0.0, 0.0],[3.37166184668, -27.4071741155, -1.16628417085],[0.0, -27.2388580576, 0.0],[0.0, -28.4642617121, 0.0]]
# 
# indexMaxAttrs: close_relax 10:[[0.0, 0.0, 0.0],[5.9633763, 15.700059, 0.54465106],[0.0, 81.977047, -1.7016228e-08],[1.7517221e-08, 55.126766, 0.0]]
# midMaxAttrs: close_relax 10:[[0.0, 0.0, 0.0],[-5.8901638, 62.713939, 6.4230467],[1.5710974e-08, 89.073468, -8.1041822e-09],[8.3571925e-09, 89.073468, 1.5577875e-08]]
# ringMaxAttrs: close_relax 10:[[-2.9928762, 0.0, 0.0],[-7.5992846, 76.569896, 9.6618835],[0.0, 94.254135, 0.0],[0.0, 94.254135, 0.0]]
# pinkyMaxAttrs: close_relax 10:[[-1.8613005, 0.056215787, 1.7302502],[-16.070961, 98.08572, 16.060939],[0.0, 85.170248, 0.0],[0.0, 85.170248, 0.0]]
# 
# indexMinAttrs: close_relax -3:[[0.0, 0.0, 0.0],[-1.78901296209, -4.71001766824, 0.0],[0.0, -24.5931117458, 0.0],[0.0, -16.5380308993, 0.0]]
# midMinAttrs: close_relax -3:[[0.0, 0.0, 0.0],[1.767049046, -18.8141809128, -1.92691395053],[0.0, -26.722042326, 0.0],[0.0, -26.722042326, 0.0]]
# ringMinAttrs: close_relax -3:[[0.897862892745, 0.0, 0.0],[2.27978534257, -22.9709678296, -2.89856494708],[0.0, -28.276243548, 0.0],[0.0, -28.276243548, 0.0]]
# pinkyMinAttr: close_relax -3:[[0.0, 0.0, 0.0],[4.82128816103, -29.4257143434, -4.81828168971],[0.0, -25.5510728862, 0.0],[0.0, -25.5510728862, 0.0]]
# 
# indexMaxAttrs: relaxD 10:[[0.0, 0.0, 0.0],[5.4160948, 12.535184, 1.2137211],[0.0, 10.100644, -1.7270777e-08],[6.8093491e-09, 10.100644, -1.6329651e-08]]
# midMaxAttrs: relaxD 10:[[0.0, 0.0, 0.0],[-1.7709299, 22.999166, -1.5032809],[6.9404626e-09, 10.308678, -1.6351366e-08],[9.7545475e-09, 10.308678, -1.4845411e-08]]
# ringMaxAttrs: relaxD 10:[[0.0, 0.0, 0.0],[-9.0447572, 27.937911, -2.3253179],[8.2228049e-09, 14.285307, -1.5505428e-08],[1.1794547e-08, 14.285307, -1.2996997e-08]]
# pinkyMaxAttrs: relaxD 10:[[0.0, 0.0, 0.0],[-15.723218, 33.076844, -1.6909839],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
# 
# indexMinAttrs: relaxD -3:[[0.0, 0.0, 0.0],[-1.62482857459, -3.76055524696, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
# midMinAttrs: relaxD -3:[[0.0, 0.0, 0.0],[0.0, -6.89974964616, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
# ringMinAttrs: relaxD -3:[[0.0, 0.0, 0.0],[2.71342718955, -8.38137266181, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
# pinkyMinAttr: relaxD -3:[[0.0, 0.0, 0.0],[4.71696534913, -9.92305375801, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
# 
# indexMaxAttrs: relaxE 10:[[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[9.2055523e-09, 5.0979753, -1.5113549e-08],[1.0512118e-08, 12.199657, -1.4235765e-08]]
# midMaxAttrs: relaxE 10:[[0.0, 0.0, 0.0],[0.0, 46.799998, 1.7771855e-08],[0.0, 38.519999, 2.5966873e-08],[0.0, 38.519999, 2.1833783e-07]]
# ringMaxAttrs: relaxE 10:[[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 47.306373, 0.0],[0.0, 47.306373, 0.0]]
# pinkyMaxAttrs: relaxE 10:[[-2.8230663, 0.0, 0.0],[-11.348742, 55.622932, 9.5249724],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
# 
# indexMinAttrs: relaxE -3:[[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -1.52939260387, 0.0],[0.0, -3.65989711932, 0.0]]
# midMinAttrs: relaxE -3:[[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
# ringMinAttrs: relaxE -3:[[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -14.1919116307, 0.0],[0.0, -14.1919116307, 0.0]]
# pinkyMinAttr: relaxE -3:[[0.0, 0.0, 0.0],[3.4046228407, -16.6868815882, -2.85749193878],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
# 
# indexMaxAttrs: Grab2 10:[[0.0, 0.0, 0.0],[-1.7635041, -8.5214628, -16.147383],[0.0, 20.931244, -1.7567324e-08],[0.0, 23.267933, -1.7348401e-08]]
# midMaxAttrs: Grab2 10:[[0.0, 0.0, 0.0],[-0.030713774, -2.9912371, -3.0009306],[0.0, 31.691439, -1.7747642e-08],[8.5345485e-09, 32.747485, -1.5588491e-08]]
# ringMaxAttrs: Grab2 10:[[-2.9928762, 0.0, 0.0],[-1.9605419, 10.418159, 11.084858],[0.0, 39.844309, 0.0],[0.0, 40.428393, 0.0]]
# pinkyMaxAttrs: Grab2 10:[[-1.8613005, 0.056215787, 1.7302502],[-1.9825828, 29.626945, 18.362295],[0.0, 35.245693, 0.0],[0.0, 34.28776, 0.0]]
# 
# indexMinAttrs: Grab2 -3:[[0.0, 0.0, 0.0],[0.0, 2.55643895266, 4.84421472464],[0.0, -6.27937348304, 0.0],[0.0, -6.98037935086, 0.0]]
# midMinAttrs: Grab2 -3:[[0.0, 0.0, 0.0],[0.0, 0.897371185757, 0.900279164949],[0.0, -9.5074318884, 0.0],[0.0, -9.82424536423, 0.0]]
# ringMinAttrs: Grab2 -3:[[0.897862892745, 0.0, 0.0],[0.0, -3.12544759854, -3.32545729794],[0.0, -11.9532935107, 0.0],[0.0, -12.1285162186, 0.0]]
# pinkyMinAttr: Grab2 -3:[[0.0, 0.0, 0.0],[0.0, -8.8880835737, -5.50868833157],[0.0, -10.5737077603, 0.0],[0.0, -10.2863291471, 0.0]]
# 
# indexMaxAttrs: spread2 10:[[0.0, 0.0, 0.0],[8.7247019, -10.394853, -18.082124],[0.0, -8.2723094, -1.7277899e-08],[0.0, -8.2723094, -1.6642118e-08]]
# midMaxAttrs: spread2 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, -8.2723094, 3.5543707e-08],[0.0, -8.2723094, 1.7958196e-08]]
# ringMaxAttrs: spread2 10:[[0.0, 0.0, 0.0],[-10.955866, 7.5271701, 2.1637058],[0.0, -8.2723094, -1.7297596e-08],[0.0, -8.2723094, -1.7446468e-08]]
# pinkyMaxAttrs: spread2 10:[[0.0, 0.0, 0.0],[-3.4375475, 29.857157, 26.640187],[0.0, -8.2723094, 0.0],[0.0, -8.2723094, 0.0]]
# 
# indexMinAttrs: spread2 -3:[[0.0, 0.0, 0.0],[-2.61741043801, 3.11845608838, 5.42463689589],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
# midMinAttrs: spread2 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
# ringMinAttrs: spread2 -3:[[0.0, 0.0, 0.0],[3.28675999708, -2.25815105805, 0.0],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
# pinkyMinAttr: spread2 -3:[[0.0, 0.0, 0.0],[1.03126421643, -8.95714757769, -7.99205549907],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
# 
# indexMaxAttrs: point 10:[[0.0, 0.0, 0.0],[-0.48240779, 0.29722213, -0.10914528],[0.0, -7.8036046, 0.0],[0.0, -7.8036046, 0.0]]
# midMaxAttrs: point 10:[[0.0, 0.0, 0.0],[1.6502186, 52.116256, -4.3852106],[0.0, 99.9835, 0.0],[0.0, 76.63128, 0.0]]
# ringMaxAttrs: point 10:[[0.0, 0.0, 0.0],[-5.1919839, 62.997629, -1.741267],[0.0, 97.862165, 0.0],[0.0, 78.57743, 0.0]]
# pinkyMaxAttrs: point 10:[[0.0, 0.0, 0.0],[-11.35146, 70.628056, 0.91715981],[0.0, 83.653515, 0.0],[0.0, 83.653515, 0.0]]
# 
# indexMinAttrs: point -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 2.34108130208, 0.0],[0.0, 2.34108130208, 0.0]]
# midMinAttrs: point -3:[[0.0, 0.0, 0.0],[0.0, -15.6348762585, 1.3155631832],[0.0, -29.9950512267, 0.0],[0.0, -22.9893817888, 0.0]]
# ringMinAttrs: point -3:[[0.0, 0.0, 0.0],[1.55759534157, -18.8992888563, 0.0],[0.0, -29.358649066, 0.0],[0.0, -23.5732288764, 0.0]]
# pinkyMinAttr: point -3:[[0.0, 0.0, 0.0],[3.40543798067, -21.1884157715, 0.0],[0.0, -25.0960539922, 0.0],[0.0, -25.0960539922, 0.0]]
# 
# indexMaxAttrs: Fa3 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
# midMaxAttrs: Fa3 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08]]
# ringMaxAttrs: Fa3 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
# pinkyMaxAttrs: Fa3 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: Fa3 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: Fa3 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: Fa3 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: Fa3 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMaxAttrs: Fa4 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
# midMaxAttrs: Fa4 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08]]
# ringMaxAttrs: Fa4 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
# pinkyMaxAttrs: Fa4 10:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# 
# indexMinAttrs: Fa4 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# midMinAttrs: Fa4 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# ringMinAttrs: Fa4 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
# pinkyMinAttr: Fa4 -3:[[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]


 

