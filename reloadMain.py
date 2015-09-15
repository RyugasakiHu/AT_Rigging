from Modules import reloadModules    
from Modules.subModules import reloadSubmodules

from Ui import reloadUi
from Utils import reloadUtils

import autorig_settings

def reloadIt():
    
    reload(reloadModules)
    reload(reloadUi)
    reload(reloadUtils)
    reload(reloadSubmodules)
    
    reload(autorig_settings)

    reloadModules.reloadIt()
    reloadUtils.reloadIt()
    reloadUi.reloadIt()
    reloadSubmodules.reloadIt()
    
    print  '------ Main load:OK'
    print  '------ System : Initialize'

reloadIt()        
