import os
import numpy as np
from matplotlib import pyplot as plt

from FileIO import FileIO

"""
Configuration:
Global and configuration parameters defined in this class
"""
class Configurations:
    # change path here for uncompressed dataset
    def __init__(self, skinGroup='None'):
        # Get participant Ids
        self.setDiskPath(skinGroup)
        self.getParticipantNumbersFromPath()
        # self.getParticipantNumbers(skinGroup) # use this to get pi from list

    #Global parameters
    DiskPath = ""
    SavePath = ""
    UnCompressed_dataPath = ""
    # Skin_Group_Types = ["WhiteSkin_Group", "BrownSkin_Group"]
    current_Skin_Group = ""

    #Algorithm List
    AlgoList = [
        "None",
        "PCA",
        "FastICA",
        "PCAICA",
        "Jade",
        "Spectralembedding"

    ]

    #FFT method types
    fftTypeList = ["M1","M2","M3"]

    filtertypeList = [1,2,3,4]

    windowSize = 15#10,4,15,20

    #Pre processing techniques
    preprocesses = [1,2,6,7] # 3,4,5--> bad graphs

    #Generating result methods (peak identification and frequency value identification) and getting bpm
    resulttypeList = [1,2]

    #Smoothen Curve after filtering frequency
    Smoothen = [True,False]

    #region of interests, add or reduce here.. (make sure it matches foldername is same as roi region name holding the data)
    roiregions = ["lips", "forehead", "leftcheek", "rightcheek", "cheeksCombined"]

    """
    Participants numbers list
    """
    ParticipantNumbers = []
    Participantnumbers_SkinGroupTypes = {}
    Skin_Group_Types = ['OtherAsian_OtherSkin_Group', 'SouthAsian_BrownSkin_Group', 'Europe_WhiteSkin_Group']

    # heart rate status example resting state and after small workout "Resting1","Resting2","AfterExcersize"
    hearratestatus = ["Resting1","Resting2","AfterExcersize"]

    #Processing Steps
    ProcessingSteps = [ "PreProcess", "Algorithm", "FFT", "Filter","ComputerHRandSPO", "CheckReliability" ,"SaveResultstoDisk"] # SaveResultoDatabase

    #Generate HTML Summary
    GenerateSummary = False

    #Ignore gray when processing signals (only process r,g,b and ir)
    ignoregray = False

    #Generate graphs when processing signals (only process r,g,b and ir)
    GenerateGraphs = False

    #StoreValuesinDisk
    DumpToDisk = True

    #Run for window or for entire signal
    RunAnalysisForEntireSignalData = False

    def setDiskPath(self, current_Skin_Group="None"):
        self.DiskPath = 'E:\\ARPOS_Server_Data\\Server_Study_Data\\' + current_Skin_Group + "\\"
        self.UnCompressed_dataPath = self.DiskPath + 'SerialisedRawServerData\\UnCompressed\\'


    """
    GetSavePath:
    Store all the generated graphs and files to this path
    """
    def setSavePath(self,participantNumber,position,pathname='ProcessedData'):
        self.setDiskPath(self.Participantnumbers_SkinGroupTypes.get(participantNumber))
        self.SavePath = self.DiskPath + '\\' + pathname + '\\' + participantNumber + '\\' + position + '\\'
        #Create save path if it does not exists
        if not os.path.exists(self.SavePath):
            os.makedirs(self.SavePath)

        # if(self.GenerateGraphs):
        #     graphPath = self.SavePath + "Graphs\\"
        #     if not os.path.exists(graphPath):
        #         os.makedirs(graphPath)

    """
    getLoadPath:
    Get all paths where color, ir, and distance of participants is stored 
    Only uncompressed data path,Change path accordingly
    Requires participant number, position (heart rate status), and the region (lips, forehead etc)
    """
    def getLoadPath(self,participantNumber,position,region):
        LoadColordataPath = self.DiskPath + 'SerialisedRawServerData\\UnCompressed\\' + participantNumber + '\\' + position + 'Cropped\\' + 'Color\\' + region + '\\'  ## Loading path for color data
        LoadIRdataPath = self.DiskPath + 'SerialisedRawServerData\\UnCompressed\\' + participantNumber + '\\' + position + 'Cropped\\' + 'IR\\' + region + '\\'  ## Loading path for IR data
        LoadDistancePath = self.DiskPath + 'SerialisedRawServerData\\UnCompressed\\' + participantNumber + '\\' + position + '\\ParticipantInformation.txt'  ## Loading path for depth and other information
        # ProcessedDataPath = self.SavePath + datatype + '\\'  ## Loading path for storing processed data
        # # Create save path if it does not exists
        # if not os.path.exists(ProcessedDataPath):
        #     os.makedirs(ProcessedDataPath)
        return LoadColordataPath,LoadIRdataPath,LoadDistancePath #,ProcessedDataPath

    """
    getParticipantNumbers:
    Store all the participant ids to variable [ParticipantNumbers]
    """
    def getParticipantNumbers(self,skinGroup):
        #Read participantid file to get list of participants
        ROOT_DIR = os.path.dirname(os.path.abspath(os.curdir)) # This is your Project Root
        AppDataPath=''
        if(ROOT_DIR.__contains__('ARPOSProject')):
            AppDataPath = ROOT_DIR + '\\' + 'AppData' + '\\'
        else:
            AppDataPath = ROOT_DIR + '\\ARPOSProject\\' + 'AppData' + '\\'
        objFile = FileIO()
        participantIds = objFile.ReaddatafromFile(AppDataPath,'ParticipantIds')

        self.ParticipantNumbers = []
        for Line in participantIds:
            Lineid = Line.split(', ')
            if(Lineid[len(Lineid)-1].__contains__('Yes')): #Is participating
                if(Lineid[len(Lineid)-2] != 'UNOCCUPIED'): #Is occupied
                    if(skinGroup == 'None'):
                        piId = Lineid[1] #participantId
                        self.ParticipantNumbers.append(piId)
                        self.Participantnumbers_SkinGroupTypes[piId] = Lineid[len(Lineid)-2]
                    else:
                        if (Lineid[len(Lineid)-2] == skinGroup):
                            piId = Lineid[1]  # participantId
                            self.ParticipantNumbers.append(piId)
                            self.Participantnumbers_SkinGroupTypes[piId] = Lineid[len(Lineid) - 2]
                        else:
                            skip=True


    def getParticipantNumbersFromPath(self):
        folder = self.UnCompressed_dataPath
        subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

        # for each participant
        for folder in subfolders:
            foldername = str(folder)
            foldernameparams = foldername.split("\\")
            ParticipantNumber = foldernameparams[len(foldernameparams) - 1]
            if(not self.ParticipantNumbers.__contains__(ParticipantNumber) ):
                self.ParticipantNumbers.append(ParticipantNumber)
            # self.Participantnumbers_SkinGroupTypes[piId] = Lineid[len(Lineid)-2]
