# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_13-18.49.31 163176
# Run by tiany on Thu May  5 19:06:17 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=142.885406494141, 
    height=134.474533081055)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb('Manniquin_2.cae')
#: The model database "H:\DropBoxNewFolder\2022-ML-based-Soft-Mannequin-Control\AbaqusScript-ML\client-original\Manniquin_2.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Job-Man'].parts['CHEST-LEFT']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Job-Man'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2.11841, 
    farPlane=3.6036, width=1.45959, height=0.75213, viewOffsetX=0.0348091, 
    viewOffsetY=0.057055)
i1 = mdb.models['Job-Man'].rootAssembly.allInstances['MEMBRANE-1']
leaf = dgm.LeafFromInstance(instances=(i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2.30463, 
    farPlane=3.44867, width=0.554621, height=0.285797, viewOffsetX=0.0312703, 
    viewOffsetY=0.169521)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2.36088, 
    farPlane=3.3047, width=0.568158, height=0.292772, cameraPosition=(2.31076, 
    1.76533, 1.24544), cameraUpVector=(-0.466981, 0.715644, -0.519406), 
    cameraTarget=(-0.0363062, 0.678712, 0.0223808), viewOffsetX=0.0320335, 
    viewOffsetY=0.173659)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2.36923, 
    farPlane=3.29635, width=0.473573, height=0.244032, viewOffsetX=0.0314327, 
    viewOffsetY=0.185716)
session.viewports['Viewport: 1'].view.setValues(nearPlane=2.33474, 
    farPlane=3.48236, width=0.466679, height=0.24048, cameraPosition=(2.16537, 
    2.40133, 0.863541), cameraUpVector=(-0.608934, 0.504874, -0.611801), 
    cameraTarget=(0.00402094, 0.708302, 0.0588425), viewOffsetX=0.0309751, 
    viewOffsetY=0.183012)
