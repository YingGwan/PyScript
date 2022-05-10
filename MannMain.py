#from odbAccess import *
#from textRepr import *
#from abaqusConstants import *
import numpy as np
import time
import re
import inputPython
import subprocess
import open3d as o3d 
import trimesh as tm
import time
import os
import threading
import multiprocess
from multiprocess import Process, Queue
from multiprocess import Condition
#from pathlib import Path

# my_file = Path("/path/to/file")
# if my_file.is_file():
    # # file exists


#return value:  False -> simulation failed
#               True  -> simulation successful
'''
Global variable used in multi-threading functionality
'''
#threadNum = 4
npprocessNum = 4
processNum = multiprocess.Value('i', npprocessNum)

'''
threadsAvailableVec[i]==0 means it is available
                        1 means it is now occupied
'''
#create a numpy array first
npArray_sharedArray = np.zeros([npprocessNum],dtype = np.intc)
#assign to multiprocess shared array
processesAvailableVec = multiprocess.Array('i', npArray_sharedArray)
# processesAvailableVec = [multiprocess.Value(i) for i in processesAvailableVec_ori]


'''
number of threads in operation
'''
#activeThreadNum = 0
npactiveProcessNum = 0
activeProcessNum = multiprocess.Value('i', npactiveProcessNum)

'''
Lock of multi-process data
'''
# lock_of_data = threading.Condition()                #in order to access same data structure
# lock_of_write_record_file = threading.Condition()

lock_of_data = multiprocess.RLock()               #in order to access same data structure
lock_of_write_record_file = multiprocess.RLock()




'''
Function to call abaqus and store simulated file
'''
def MannequinSimulation(threadIdx,Cp,saveFileName):
    #pressure of chamber
    Pc1 = Cp[0]; Pc2 = Cp[1]; Pc3 = Cp[2]; Pc4 = Cp[3]
  
    
    currentPath = os.getcwd()
    print(f"[SIMULATION {threadIdx}] old directory is {currentPath}")
    currentPath = currentPath + f"/abaqusFile/{threadIdx}"
    print(f"[SIMULATION {threadIdx}] now directory is {currentPath}")
    os.chdir(currentPath)
   
    #Check and remove the previous LCK file
    if os.path.exists(currentPath + '\\Job-Man.lck'):   
        print(f"[SIMULATION {threadIdx}] lck exist, will remove this...\n")
        os.remove(currentPath + '\\Job-Man.lck')# Work dir
    else:
        print(f"[SIMULATION {threadIdx}] lck dosen't exist, just start the simulation..\n")
    
    #return True
    

    
    #########
    print(f"[SIMULATION {threadIdx}] Working directory changed...\n")
    
    
    # Check and remove the previous inp file
    if os.path.exists(currentPath + '\\Job-Man.inp'): 
        print(f"[SIMULATION {threadIdx}] inp exist, will remove this...\n")
        os.remove(currentPath + '\\Job-Man.inp')# delete inp file
        time.sleep(1)
    else:
        print(f"[SIMULATION {threadIdx}] inp dosen't exist, just start the simulation..\n")
    
    if os.path.exists(currentPath + '\\Job-Man.sta'): 
        print(f"[SIMULATION {threadIdx}] .sta exist, will remove this...\n")
        os.remove(currentPath + '\\Job-Man.sta')# delete inp file
        time.sleep(1)
    else:
        print(f"[SIMULATION {threadIdx}] .sta dosen't exist, just start the simulation..\n")
    
    time.sleep(3)
    print(f"[SIMULATION {threadIdx}] wait for inp file to be deleted..\n")
    
    commandStr = f"abaqus cae noGUI=MannPre-pro.py --"
    
    for i in range(4):
        commandStr = commandStr +" "+str(Cp[i])
    print(f"{commandStr}")   
        
    os.system(commandStr)# Pre-processing and create the inp file
    
    print(f"[SIMULATION {threadIdx}] wait 5s for inp file to be created..\n")
    time.sleep(5)    
    while os.path.exists(currentPath+'\\Job-Man.inp') ==False:
        time.sleep(1)
        print(f"[SIMULATION {threadIdx}] Waiting for inp file to be generated")
        
    print(f"[SIMULATION {threadIdx}] Inp file generated...\n")
    
    ##create inp file and submite the job
    
    
    # delete inp file first

    os.system('abaqus cpus=5 job=Job-Man ask_delete=OFF')# Solve the job with ???? cores(about 70%~80% of maximum cores)
            

    print (f'[SIMULATION {threadIdx}]>>> Chamber Pressure = [%.5f, %.5f, %.5f, %.5f] kPa'%(Cp[0]/1000,Cp[1]/1000,Cp[2]/1000,Cp[3]/1000))
    
    print (f'[SIMULATION {threadIdx}]------------------------------------------------------------')
    
    # Read and process the result
    print(f"[SIMULATION {threadIdx}] wait 6s for lck file to be generated...\n")
    time.sleep(6)
    CountOfTimer = 0
    outputnumber = 0
    
    lastPercent =0.0  #0->1
    nowPercent  =0.0  #0->1
    while os.path.exists('Job-Man.odb') == False or os.path.exists('Job-Man.lck') == True:
        time.sleep(2)
        #print("")
        CountOfTimer = CountOfTimer +1
        
      
        if CountOfTimer%4 == 0:
            #outputnumber = outputnumber +1
            #print("Simulation running, counter number: ",outputnumber)
            percent = inputPython.GetPercentage()    
            nowPercent = percent#get the percentage of work
            shouldOutPutInfo = inputPython.ShouldOutPut(nowPercent,lastPercent,5)            #judge whether we could output information according to information of this iteration and last iteration
            if shouldOutPutInfo == True:
                print(f"[SIMULATION {threadIdx}] Simulation percentage: %lf"%(nowPercent))
 
            lastPercent = nowPercent
    
    
    #we need to record save obj file action
    outputfileName = saveFileName
    commandStr = "abaqus cae noGUI=MannsaveOBJ.py -- "+ outputfileName
    
    os.system(commandStr)
    #print(f"[SIMULATION] file saved...\n")
    #time.sleep(6)
    print(f"[SIMULATION {threadIdx}] Simulation ends...\n")
    data=inputPython.GetPercentage()
    if np.fabs(data-5.0)<0.001:
        print(f"[SIMULATION {threadIdx}] Simulation finished...\n")
        return True
    else:
        print(f"[SIMULATION {threadIdx}] Simulation failed...\n")
        return False
  
'''
multi-threading function
Idx: from 0                 -> actuation sequence index
threadIdx: from 0
'''
def handle_client(Idx, ActParameters,processIdx,processNum,activeProcessNum,processesAvailableVec):

    lock_of_data.acquire()
    print(f"[CLIENT {processIdx}] simulates {Idx} (from 0):\n{ActParameters[0]}\t{ActParameters[1]}\t{ActParameters[2]}\t{ActParameters[3]}\n")
    lock_of_data.release()
    
    #do the simulation
    #save the obj file to the right place
    cPath = os.getcwd()
    result = MannequinSimulation(processIdx,[ActParameters[0],ActParameters[1],ActParameters[2],ActParameters[3]],cPath+f"/data/mesh/{Idx}.obj")
    
    #update record file
    os.chdir("../../")
    lock_of_write_record_file.acquire()
    recordData = np.loadtxt("./data/record.txt",delimiter=',')
    if result == True:
        recordData[Idx,1] = 1                           #this actuation sequence is finished now
    if result == False:
        recordData[Idx,1] = 0                           #this actuation sequence is finished now
    np.savetxt(f"./data/record.txt",recordData,delimiter=',')
    lock_of_write_record_file.release()
    time.sleep(1)          #simulate the abaqus sub-process
    
    #before exiting thread, clear this thread flag
    print(f"[CLIENT {processIdx}] finished simulation..")
    lock_of_data.acquire()
    activeProcessNum.value = activeProcessNum.value-1
    processesAvailableVec[processIdx] = 0
    print(f"[CLIENT {processIdx}] Finished, thread number will become {activeProcessNum.value}\n\n")
    lock_of_data.release()
                
'''
Server thread will handle simulation tasks ranging from [startIdx, endIdx];
Here, endIdx is included in batch;
startIdx is from 0

if simulation is not successful, we skip them
The last three arguments are shared value or array
'''              

def SERVER_MAIN_LOOP(startIdx,endIdx,processNum,activeProcessNum,processesAvailableVec):   
  
    record = np.loadtxt("./data/record.txt",delimiter=',')
    actuation = np.loadtxt("./data/actuationDataSet.txt",delimiter=',')
    
    
    #print("actuation:",actuation.shape)
    #print(actuation)
    
    start = startIdx
    end = endIdx
    
    actuationIdx = startIdx
    # os.chdir(".\\abaqusFile\\0")
    # print("SubProcess Directory is:",os.getcwd())
    # commandStr = f"abaqus cae noGUI=MannPre-pro.py --"
    # Cp = [1,2,3,4]
    # for i in range(4):
        # commandStr = commandStr +" "+str(Cp[i])
    # print(f"{commandStr}")   
        
    # os.system(commandStr)# Pre-processing and create the inp file
    
  
    while True:
        lock_of_data.acquire()
        #print(f"activeProcessNum.value is {activeProcessNum.value}")
        if activeProcessNum.value < processNum.value:
            '''
            Get actuation parameters for the execution thread
            '''
            start = actuationIdx
            exitFlag = False
            for i in range(start,end+1):
                if(np.fabs(record[i,1])<0.05):
                    #not finished yet
                    print(f"[Server Thread] Actuation Index {i+1} is not finished...")
                    actuationIdx = i
                    break;
                else:
                    #has been finished
                    
                    #if last simulation job is already finished, end the server
                    if i == end:
                        exitFlag = True;
                        
                        break;
            if start == end+1:
                print("[Server Thread] Last task finished 2.. Server will exit...\n")
                lock_of_data.release()
                break
                        
            if exitFlag == True:
                print("[Server Thread] Last task finished.. Server will exit...\n")
                lock_of_data.release()
                break
            
            if actuationIdx == end+1:
                print("[Server Thread] Tasks finished.. Server will exit...\n")
                lock_of_data.release()
                break;
        
            processIdx = -1
            for i in range(processNum.value):
                if processesAvailableVec[i] == 0:
                    processIdx = i
                    break
                
                   
            processesAvailableVec[processIdx] = 1  #it will be occupied soon
            
            actParameters = actuation[actuationIdx]
            
            #multi-threading part
            # thread = threading.Thread(target = handle_client, args=(actuationIdx, actParameters,threadIdx))        #start thread to handle response
            # thread.start()
            # activeThreadNum=activeThreadNum+1
            
            #multi-process
            activeProcessNum.value = activeProcessNum.value+1
            processWorker = Process(target=handle_client, args=(actuationIdx,actParameters,processIdx,processNum,activeProcessNum,processesAvailableVec))
            processWorker.start() 
            
            
            actuationIdx = actuationIdx+1
            print(f"[Server Thread] [Open Thread] num: {activeProcessNum.value}")
            lock_of_data.release()
            time.sleep(0.5)
        else:
            lock_of_data.release()
            time.sleep(2)
    
    #after assigning all data, we should wait for all worker threads to be finished
    
    while True:
        lock_of_data.acquire()
        if activeProcessNum.value == 0:
            print("All active threads finished their jobs...\nEND OF CODE\n\n")
            break
        lock_of_data.release()
        time.sleep(30)
        print("Waiting for all threads ending...")
    
    
####thread to handle listening
def server_start(startIdx, endIdx):
    #multi-threading
    # serverMainthread = threading.Thread(target = SERVER_MAIN_LOOP, args=(startIdx,endIdx))        #start thread to handle response
    # serverMainthread.start()            
    
    #multi-process
    serverMainProcess = Process(target=SERVER_MAIN_LOOP, args=(startIdx,endIdx,processNum,activeProcessNum,processesAvailableVec))
    serverMainProcess.start() 
    

if __name__ == "__main__":
    
    server_start(0,100)
    
    #result = MannequinSimulation([0.1,1500.0,0.1,0.1],"0505.obj")
    
    # outputfileName = "test.obj"
    # commandStr = "abaqus cae noGUI=MannsaveOBJ.py -- "+ outputfileName
    
    # os.system(commandStr)
    # print(f"[SIMULATION] file saved...\n")
    
    
    # data=inputPython.GetPercentage()
    # print(f"progress is {data}")