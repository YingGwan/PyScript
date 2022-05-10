# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_13-18.49.31 163176
# Run by tiany on Thu May  5 05:41:49 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.11979, 1.1169), width=164.833, 
    height=110.796)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('MannPre-pro.py', __main__.__dict__)
#: Actuation 0 is 23.000000
#: Actuation 1 is 700.000000
#: Actuation 2 is 2109.375000
#: Actuation 3 is 1115.625000
#: The model database "H:\DropBoxNewFolder\2022-ML-based-Soft-Mannequin-Control\AbaqusScript-ML\client-original\abaqusFile\0\Manniquin_2.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
print 'RT script done'
#: RT script done
