# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import numpy as np

'''

'''
actuationStr = sys.argv
actuation = np.zeros((4,1))
f = open('readme.txt', 'a')
for i in range(4):
    actuation[i][0] =float(actuationStr[-4+i])
    print("Actuation %d is %lf\n"%(i,actuation[i][0]))
    info =str(i) +" "+ str(actuation[i][0])+"\n"
    #f.write(info)

#find out prefix
# start = '--'
# end = 'bbb'
# cpath = actuationStr[actuationStr.find(start)+len(start):actuationStr.rfind(end)]

import re
found = actuationStr[-5]
#re.search('-- (.+?)bbb', actuationStr).group(1)
# try:
    # found = re.search('AAA(.+?)ZZZ', text).group(1)
# except AttributeError:
    # # AAA, ZZZ not found in the original string
    # found = '' # apply your error handling

caeFile = os.path.join(found,"Manniquin_2.cae")

openMdb(pathName=caeFile)

session.viewports['Viewport: 1'].setValues(displayedObject=None)
a = mdb.models['Job-Man'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, optimizationTasks=OFF, 
    geometricRestrictions=OFF, stopConditions=OFF)

mdb.models['Job-Man'].loads['PRS-W-DOWN'].setValues(magnitude=actuation[0][0])
mdb.models['Job-Man'].loads['PRS-W-UP'].setValues(magnitude=actuation[2][0])
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-2')
mdb.models['Job-Man'].loads['PRS-W-MID'].setValues(magnitude=actuation[1][0])
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-5')
mdb.models['Job-Man'].loads['PRS-C-LEFT'].setValues(magnitude=actuation[3][0])
mdb.models['Job-Man'].loads['PRS-C-RIGHT'].setValues(magnitude=actuation[3][0])


mdb.Job(name='Job-Man', model='Job-Man', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=2, 
    numDomains=4, numGPUs=0)


mdb.jobs['Job-Man'].writeInput(consistencyChecking=OFF)