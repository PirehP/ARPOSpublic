import os
import re
import pandas as pd

from Configurations import Configurations
from FileIO import FileIO
from SQLResults.SQLConfig import SQLConfig

"""
Main Class:
"""
class Main:
    # Store Region of Interest and Results
    ROIStore = {}

    # Global Objects
    objConfig = None
    objSQLConfig= None
    objFileIO = None
    ParticipantsProcessedHeartRateData = {}
    ParticipantsProcessedBloodOxygenData = {}
    HRNameFileName = "AvgHRdata_"
    SPONameFileName = "AvgSPOdata_"
    CaseList = []

    HeaderRow = 'WindowCount,bestSnrString,GroundTruth HeartRate Averaged,Computed HeartRate,HRDifference from averaged,' \
                'bestBpm Without ReliabilityCheck,OriginalObtianedAveragedifferenceHR, Hr from windows last second, ' \
                'LastSecondWindow differenceHR, OriginalObtianed LastSecondWindow differenceHR,' \
                'GroundTruth SPO Averaged,Computed SPO,SPO Difference from averaged,best SPO WithoutReliability Check,Original Obtianed Average differenceSPO,' \
                'SPOLastSecond,LastSecondWindowdifferenceSPO ,OriginalObtianedLastSecondWindowdifferenceSPO, Regiontype, channeltype,' \
                'FrequencySamplingError,heartRateError,TotalWindowCalculationTimeTaken,' \
                'PreProcessTimeTaken,AlgorithmTimeTaken,FFTTimeTaken,SmoothTimeTaken,' \
                'FilterTimeTaken,ComputingHRSNRTimeTaken,ComputingSPOTimeTaken,Algorithm_type,' \
                'FFT_type,Filter_type,Result_type,Preprocess_type,isSmoothen,ColorFPS,IRFPS,' \
                'SelectedColorFPSMethod,SelectedIRFPSMethod,' \
                'AttemptType,FPSNotes,UpSampled'
    HeaderRowSplit = []

    # Constructor
    def __init__(self, skinGroup='None'):
        self.objConfig = Configurations(skinGroup)
        self.objSQLConfig = SQLConfig()
        self.objFileIO = FileIO()
        self.HeaderRowSplit = self.HeaderRow.split(",")

    """
    Generate cases:
    """
    def GenerateCases(self):
        self.CaseList = []
        for preprocesstype in self.objConfig.preprocesses:
            for algoType in self.objConfig.AlgoList:
                for isSmooth in self.objConfig.Smoothen:
                    for fftype in self.objConfig.fftTypeList:
                        for filtertype in self.objConfig.filtertypeList:
                            for resulttype in self.objConfig.resulttypeList:
                                    fileName = algoType + "_PR-" + str(preprocesstype) + "_FFT-" + str(
                                        fftype) + "_FL-" + str(filtertype) \
                                               + "_RS-" + str(resulttype) + "_SM-" + str(isSmooth)
                                    if (fileName not in self.CaseList):
                                        self.CaseList.append(fileName)

    def CheckIfGenerated(self, fileName):
        pathExsists = objFile.FileExits(self.objConfig.SavePath + 'Result\\' + 'HRSPOwithLog_' + fileName + ".txt")
        # already generated
        if (pathExsists):
            return True
        return False

    """
     GenerateResultsfromParticipants:
     """
    def GenerateResultsfromParticipants(self, ParticipantsOriginalDATA,typeProcessing, UpSampleData,CaseListExists,NoHRCases,AttemptType,skintype):
        self.GenerateCases()
        TotalCasesCount = len(self.CaseList)
        for participant_number in self.objConfig.ParticipantNumbers:  # for each participant
            for position in self.objConfig.hearratestatus:  # for each heart rate status (resting or active)
                print(participant_number + ', ' + position)
                objWindowProcessedData = ParticipantsOriginalDATA.get(participant_number + '_' + position)
                self.objConfig.setSavePath(participant_number, position,typeProcessing)
                currentCasesDone = 0
                for case in self.CaseList:
                    casefullValue = case + '+' + participant_number+'+' +position + str(UpSampleData)
                    IsGenerated= True if CaseListExists.count(casefullValue) else False
                    if(not IsGenerated):
                        IsGenerated= True if NoHRCases.__contains__(case) else False
                    if(not IsGenerated):
                        currentCasesDone = currentCasesDone + 1
                        currentPercentage = ((currentCasesDone/TotalCasesCount)*100)
                        print(case + '  -> ' + str(currentPercentage) + ' out of 100%')
                        splitCase = case.split('_')
                        fileName = case
                        algoType = splitCase[0]
                        fftype = splitCase[2].replace('FFT-', '')
                        filtertype = int(splitCase[3].replace('FL-', ''))
                        resulttype = int(splitCase[4].replace('RS-', ''))
                        preprocesstype = int(splitCase[1].replace('PR-', ''))
                        isSmooth = splitCase[5].replace('SM-', '')
                        isSmooth=isSmooth.lower()
                        isSmooth=isSmooth.capitalize()
                        if (isSmooth == 'True'):
                            isSmooth = True
                        else:
                            isSmooth = False

                        # Generate Data for all Techniques
                        objParticipantsResultEntireSignalDataRow = Process_SingalData(
                            self.objConfig.RunAnalysisForEntireSignalData,
                            objWindowProcessedData.ROIStore, self.objConfig.SavePath,
                            algoType, fftype,
                            filtertype, resulttype, preprocesstype, isSmooth,
                            objWindowProcessedData.HrGroundTruthList, objWindowProcessedData.SPOGroundTruthList,
                            fileName, self.objConfig.DumpToDisk,participant_number,position,UpSampleData,AttemptType)
                        if(objParticipantsResultEntireSignalDataRow != 'NO HR'):
                            self.objSQLConfig.SaveRowParticipantsResultsEntireSignal(objParticipantsResultEntireSignalDataRow)
                        else:
                            if(not NoHRCases.__contains__(case)):
                                exists = self.objFileIO.FileExits(self.objConfig.SavePath+ "NOHRCases_" + skintype+ ".txt")
                                mode = "w+"
                                if(exists):
                                    mode = "a"
                                self.objFileIO.WritedatatoFile(self.objConfig.SavePath,"NOHRCases_" + skintype, objParticipantsResultEntireSignalDataRow + "\t" + case,mode)

                ParticipantsOriginalDATA.pop(participant_number + '_' + position)

    def LoadandGenerateFaceDatatoBianryFiles(self,SaveFileName, UpSampleData, SaveFolder):
        for participant_number in self.objConfig.ParticipantNumbers:  # for each participant
            for position in self.objConfig.hearratestatus:  # for each heart rate status (resting or active)
                self.objConfig.setSavePath(participant_number, position, SaveFolder)  # set path
                print('Loading and generating FaceData for ' + participant_number + ', ' + position + " and UpSampleData" + str(UpSampleData))
                print('Loading from path ' + self.objConfig.DiskPath + '; Storing data to path ' + self.objConfig.SavePath)
                # for each roi and put in Store Region
                for region in self.objConfig.roiregions:
                    # Init for each region
                    objFaceImage = LoadFaceData()
                    objFaceImage.Clear()

                    ##get loading path
                    LoadColordataPath, LoadIRdataPath, LoadDistancePath = self.objConfig.getLoadPath(
                        participant_number, position,
                        region)

                    # Load Roi data (ALL)
                    # print("Loading and processing color roi data")
                    objFaceImage.ProcessColorImagestoArray(LoadColordataPath,UpSampleData)

                    # print("Loading and processing ir roi data")
                    objFaceImage.ProcessIRImagestoArray(LoadIRdataPath, LoadDistancePath,UpSampleData)

                    # Create global data object and use dictionary (ROI Store) to uniquely store a regions data
                    self.ROIStore[region] = GlobalData(objFaceImage.time_list_color, objFaceImage.timecolorCount,
                                                       objFaceImage.time_list_ir, objFaceImage.timeirCount,
                                                       objFaceImage.Frametime_list_ir,
                                                       objFaceImage.Frametime_list_color,
                                                       objFaceImage.red, objFaceImage.green, objFaceImage.blue,
                                                       objFaceImage.grey,
                                                       objFaceImage.Irchannel, objFaceImage.distanceM,
                                                       objFaceImage.totalTimeinSeconds,
                                                       objFaceImage.ColorEstimatedFPS, objFaceImage.IREstimatedFPS,
                                                       objFaceImage.ColorfpswithTime, objFaceImage.IRfpswithTime)

                    # delete face image object
                    del objFaceImage

                HrGr, SpoGr = CommonMethods.GetGroundTruth(participant_number, position,
                                                           self.objConfig.DiskPath.replace("SerialisedRawServerData",""),
                                                           int(self.ROIStore.get(self.objConfig.roiregions[0]).totalTimeinSeconds))

                ##Original Data storage
                objWindowProcessedData = WindowProcessedData()
                objWindowProcessedData.HrGroundTruthList = HrGr
                objWindowProcessedData.SPOGroundTruthList = SpoGr
                objWindowProcessedData.ColorLengthofAllFrames = self.ROIStore.get(self.objConfig.roiregions[0]).getLengthColor()
                objWindowProcessedData.IRLengthofAllFrames = self.ROIStore.get(self.objConfig.roiregions[0]).getLengthIR()
                objWindowProcessedData.TimeinSeconds = int(self.ROIStore.get(self.objConfig.roiregions[0]).totalTimeinSeconds)
                objWindowProcessedData.ROIStore = self.ROIStore
                self.objFileIO.DumpObjecttoDisk(self.objConfig.SavePath.replace("SerialisedRawServerData",""), SaveFileName, objWindowProcessedData)

                del objWindowProcessedData

    '''
    LoadBinaryData: load data from disk ParticipantsOriginalDATA[ParticipantNumber + Position] -> ROISTORE data
    '''
    def LoadBinaryData(self, FileName,LoadFolder):
        ParticipantsOriginalDATA = {}
        for participant_number in self.objConfig.ParticipantNumbers:  # for each participant
            for position in self.objConfig.hearratestatus:  # for each heart rate status (resting or active)
                self.objConfig.setSavePath(participant_number, position, LoadFolder)  # set path

                ##binary Data read from disk
                objWindowProcessedData = self.objFileIO.ReadfromDisk(self.objConfig.SavePath, FileName)

                # Store for procesing locally
                ParticipantsOriginalDATA[participant_number + '_' + position] = objWindowProcessedData

        return ParticipantsOriginalDATA

    def GenerateFaceData(self):
        #For larger ROIS
        self.LoadandGenerateFaceDatatoBianryFiles("BinaryFaceROI", False,'BinaryFaceROIDataFiles')# Requries -> SaveFileName, UpSampleData, SaveFolder

        #For smaller ROIS
        # self.LoadandGenerateFaceDatatoBianryFiles("BinaryFaceROIsmall", False,'BinaryFaceROIsmallDataFiles')# Requries -> SaveFileName, UpSampleData, SaveFolder

    '''
     mainMethod: Execute program
     '''
    def mainMethod(self,skintype):
        self.GenerateFaceData()  # Run only once

        # Load data
        ParticipantsDATA = self.LoadBinaryData("BinaryFaceROI", 'BinaryFaceROIDataFiles')

        # if(self.objConfig.RunAnalysisForEntireSignalData):
        #     #For entire signal
        # else:
        #     #For Window FolderNameforSave = 'ProcessedDataWindows'
        #  Load Data from path and Process Data
        self.GenerateResultsfromParticipants(ParticipantsDATA, 'ProcessedData',skintype)  # FOR Window processing

objMain = Main()  # Main(skintype) Pass type none here to process all skin types
Skin_Group_Types = ['BrownSkin_Group','WhiteSkin_Group' ]
for skintype in Skin_Group_Types:
    objMain.mainMethod(skintype)  # Send true to generate binary object data holding images in arrays meaned
del objMain
print('Program Ended')
