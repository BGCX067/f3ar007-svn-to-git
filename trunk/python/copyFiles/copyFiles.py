import shutil, os
from datetime import datetime, date, time
import winsound, pygame

source = 'd:\\'
destin = os.path.join('e:\\','rips')

source = os.path.realpath(source)
destin = os.path.realpath(destin)

print 'Source: %s' % source
print 'Destination: %s' % destin

def copyFiles(src,dst):
    names = os.listdir(src)
    i = 1
    for name in names:
        print '%s.) %s' % (i, name)
        i = i + 1
    if os.path.isdir(destin):
        pass
    else:
        os.mkdir(destin)
    c = 0
    for name in names:
        srcname = os.path.join(src,name)
        dstname = os.path.join(dst,name)
        print srcname
        print dstname
        if os.path.isdir(srcname):
            shutil.copytree(srcname,dstname)
        elif os.path.isfile(srcname):
            shutil.copy(srcname,dstname)
        else:
            print 'Check DVD-Rom Drive!'
        c = c + 1

copyFiles(source,destin)

print '\nCopy Complete!'

winsound.PlaySound('SystemExit',winsound.SND_ALIAS)

pygame.cdrom.init()
dvd = pygame.cdrom.CD(0)
dvd.init()
dvd.eject()
dvd.quit()
