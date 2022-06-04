"""
Common Methods:
These can be used in any class or file.
"""
import numpy as np

"""
GetGroundTruth:
get ground truth data of a participant by heart rate status (resting or active)
"""
def GetGroundTruth(participant_number, position,diskpath,totalTimeinSeconds=0):
    filepath = diskpath + "\\GroundTruthData" + "\\" + participant_number + "\\" + position + "\\"
    HrFile =  filepath + "HR.txt"
    SPOFile =  filepath + "SPO.txt"

    #read data from files
    HrFiledata = open(HrFile, "r")
    SPOFiledata = open(SPOFile, "r")

    HrGr =HrFiledata.read().split("\n")
    SpoGr =SPOFiledata.read().split("\n")

    if (totalTimeinSeconds > 0):
        HrGr= HrGr[:totalTimeinSeconds]
        SpoGr=SpoGr[:totalTimeinSeconds]

    HrFiledata.close()
    SPOFiledata.close()

    HrGr = [float(value) for value in HrGr]
    SpoGr = [float(value) for value in SpoGr]

    return HrGr, SpoGr
