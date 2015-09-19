import control,limbModule,hierarchy,legModule,footModule

def reloadIt():
    reload(control)
    reload(limbModule)
    reload(hierarchy)
    reload(legModule)
    reload(footModule)
    
    print '----->Modules Reload : OK'
