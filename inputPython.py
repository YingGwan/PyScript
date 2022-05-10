import sys
import numpy as np
import os


#get percentage of simulation
def GetPercentage():
    try:
        f = open("Job-Man.sta", "r")
    except:
        print("Wait for sta file estalishment...\n")
        return 0;
    lineSet = f.readlines()
    counter = 0
    lineSetSize = len(lineSet)
    invalidLineSet = []
    validLineSet = []
    debugIdx = 0
    for i in lineSet:
        if True:
            LIST = i.split(" ")
            NEW_LIST = [elem for elem in LIST if elem.strip()]
            #print("NEW LIST:\n",NEW_LIST)
            FLAG = True #when FLAG is True, which means the 
            try:
                float(NEW_LIST[6])
                # for k in NEW_LIST:
                    # float(k)
            except: # catch *all* exceptions
                FLAG = False
            if(FLAG == False or len(NEW_LIST)==0):
                #print("LINE %d contains no figure...\n"%(counter))
                invalidLineSet.append(counter)
                #print(f"{debugIdx} is invlid\n")
            else:
                validLineSet.append(counter)
                #print(f"{debugIdx} is valid\n")
                #print("Total time step:\n",NEW_LIST[6])
            debugIdx = debugIdx +1
            counter = counter + 1

    #print("lineset:\n",validLineSet)
    ##parse percentage of finish
    
    Ptr = -1
    validLastIdx = validLineSet[len(validLineSet)-1]
    invalidLastIdx = invalidLineSet[len(invalidLineSet)-1]
    ####situation 1: when last validLineSet element is bigger than invalid: then is doing iteration
    if validLastIdx> invalidLastIdx:
        LIST = lineSet[validLastIdx].split(" ")
        NEW_LIST = [elem for elem in LIST if elem.strip()]
        #print(NEW_LIST)
        Percentage = float(NEW_LIST[6])
        return(Percentage)

    
    
    ####situation 2: when last validLineSet element is smaller than invalid: finish iteration.
    else:
        for i in range(lineSetSize):
            index = lineSetSize -i-1
            if index in invalidLineSet:
                #print("index %d in invalidlineset\n"%(index))
                pass
            else:
                #print("index %d in validlineset\n"%(index))
                Ptr = index
                break


        LIST = lineSet[Ptr].split(" ")
        NEW_LIST = [elem for elem in LIST if elem.strip()]
        #print(NEW_LIST)
        percentage = float(NEW_LIST[6])

        #print("percentage: %lf"%(percentage))
        return(percentage)
    # for i in NEW_LIST:
        # print("number is %lf\n"%(float(i)))

#percent is [0,2], lastPercent is [0,2]
#
def ShouldOutPut(percent,lastPercent, percentageThershold):


    stageNow = int(percent*100 / percentageThershold)
    lastPercent = int(lastPercent*100/percentageThershold)
    
    if stageNow - lastPercent > 0.95:
        return True
    else:
        return False

if __name__ == "__main__":
    percent = GetPercentage()
    print(f"percent is {percent}")