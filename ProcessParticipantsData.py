import sys
from datetime import datetime
import numpy as np
import CommonMethods
from CheckReliability import CheckReliability
from Configurations import Configurations
from FileIO import FileIO
from ProcessData import ProcessFaceData

# Global Objects
objConfig = Configurations()
objFile = FileIO()

'''
Process participants data 
'''


def Process_SingalData(RunAnalysisForEntireSignalData, ROIStore, SavePath, Algorithm_type, FFT_type,
                       Filter_type, Result_type, Preprocess_type, isSmoothen, HrGr, SpoGr, fileName, DumpToDisk,ParticipantId,position,UpSampleData,AttemptType):
    if (not RunAnalysisForEntireSignalData):
        Process_Participants_Data_Windows(ROIStore, SavePath,
                                          Algorithm_type, FFT_type,
                                          HrGr, SpoGr,
                                          Filter_type, Result_type, Preprocess_type, isSmoothen, fileName, DumpToDisk)
    else:
        objParticipantsResultEntireSignalDataRow = Process_Participants_Data_WindowEntireSignal(ROIStore, SavePath,
                                          Algorithm_type, FFT_type,
                                          HrGr, SpoGr,
                                          Filter_type, Result_type, Preprocess_type, isSmoothen, fileName, DumpToDisk,ParticipantId,position,UpSampleData,AttemptType)

    return  objParticipantsResultEntireSignalDataRow


'''
Process participants data in window size over the signal
'''
def Process_Participants_Data_Windows(ROIStore, SavePath,
                                      Algorithm_type, FFT_type, HrGr, SpoGr,
                                      Filter_type, Result_type, Preprocess_type, isSmoothen, fileName, DumpToDisk):
    objReliability = CheckReliability()
    # Lists to hold heart rate and blood oxygen data
    Listdata = []
    # ListSPOdata = []
    bestHeartRateSnr = 0.0
    bestBpm = 0.0
    channeltype = ''
    regiontype = ''
    freqencySamplingError = 0.0
    previousComputedHeartRate = 0.0
    smallestOxygenError = sys.float_info.max
    timeinSeconds = 10
    finaloxy = 0.0
    FullTimeLog = None

    # ROI Window Result list
    WindowRegionList = {}

    # Windows for regions (should be same for all)
    LengthofAllFramesColor = ROIStore.get(objConfig.roiregions[0]).getLengthColor()  # len()  # all have same lenghts
    LengthofAllFramesIR = ROIStore.get(objConfig.roiregions[0]).getLengthIR()
    TimeinSeconds = ROIStore.get(
        "lips").totalTimeinSeconds  # LengthofAllFrames / objProcessData.ColorEstimatedFPS  # take color as color and ir would run for same window
    # step = 30  # slide window for 1 second or 30 frames.
    # this step will aslo be variable as per that seconds frame rate
    # WindowSlider = step * timeinSeconds  # step * 5 second,  window can hold  150 frames or 5 second data #THIS WORKS ONLY IF FPS IS 30 FOR EVERY SECOND so
    # window slider is calculated in variable frames within the window as it changes
    # TODO: CHECK FOR 5 AND 6 SECOND WINDOW COMPARED TO 10 with results
    # TotalWindows in this sample
    TotalWindows = (TimeinSeconds - timeinSeconds) + 1  # second window gorup
    TotalWindows = round(TotalWindows)
    # Split ground truth data
    HrAvgList = CommonMethods.splitGroundTruth(HrGr, TotalWindows, timeinSeconds)
    SPOAvgList = CommonMethods.splitGroundTruth(SpoGr, TotalWindows, timeinSeconds)

    # Initialise object to process face regions signal data
    objProcessDataLips = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                         SavePath,
                                         objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                         DumpToDisk, fileName)
    # Initialise object to process face regions signal data
    objProcessDataForehead = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                             SavePath,
                                             objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                             DumpToDisk, fileName)

    # Initialise object to process face regions signal data
    objProcessDataRcheek = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                           SavePath,
                                           objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                           DumpToDisk, fileName)

    # Initialise object to process face regions signal data
    objProcessDataLcheek = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                           SavePath,
                                           objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                           DumpToDisk, fileName)
    # Loop through signal data
    for WindowCount in range(0, int(TotalWindows)):  # RUNNING FOR WINDOW TIMES # TimeinSeconds
        # print('Window: '+ str(WindowCount))
        # Lips
        objProcessDataLips.getSingalDataWindow(ROIStore, objConfig.roiregions[0], WindowCount, TotalWindows,
                                               timeinSeconds)
        lipsResult = objProcessDataLips.Process_EntireSignalData(False)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'lipsResult_Window_' + str(WindowCount), lipsResult)

        # Forehead
        objProcessDataForehead.getSingalDataWindow(ROIStore, objConfig.roiregions[1],
                                                   WindowCount, TotalWindows, timeinSeconds)  # Lips
        foreheadResult = objProcessDataForehead.Process_EntireSignalData(False)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'foreheadResult_Window_' + str(WindowCount), foreheadResult)

        # LeftCheek
        objProcessDataLcheek.getSingalDataWindow(ROIStore, objConfig.roiregions[2],
                                                 WindowCount, TotalWindows, timeinSeconds)
        leftcheekResult = objProcessDataLcheek.Process_EntireSignalData(False)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'leftcheekResult_Window_' + str(WindowCount), leftcheekResult)

        # RightCheek
        objProcessDataRcheek.getSingalDataWindow(ROIStore, objConfig.roiregions[3],
                                                 WindowCount, TotalWindows, timeinSeconds)
        rightcheekResult = objProcessDataRcheek.Process_EntireSignalData(False)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'rightcheekResult_Window_' + str(WindowCount), rightcheekResult)

        # Store Data in Window List
        WindowRegionList['lips'] = lipsResult
        WindowRegionList['forehead'] = foreheadResult
        WindowRegionList['rightcheek'] = rightcheekResult
        WindowRegionList['leftcheek'] = leftcheekResult

        # Get best region data
        for k, v in WindowRegionList.items():
            if (v.BestSnR > bestHeartRateSnr):
                bestHeartRateSnr = v.BestSnR
                bestBpm = v.BestBPM
                channeltype = v.channeltype
                regiontype = k
                freqencySamplingError = v.IrFreqencySamplingError
                diffNow = v.diffTime
                diffTimeLog = v.diffTimeLog
                FullTimeLog = v.gettimeDifferencesToString()

            if (v.oxygenSaturationValueError < smallestOxygenError):
                smallestOxygenError = v.oxygenSaturationValueError
                finaloxy = v.oxygenSaturationValueValue

        if (bestBpm > 0):
            # Check reliability and record best readings
            heartRateValue, heartRateError = objReliability.AcceptorRejectHR(bestHeartRateSnr, bestBpm,
                                                                             freqencySamplingError)
            oxygenSaturationValue, oxygenSaturationValueError = objReliability.AcceptorRejectSPO(smallestOxygenError,
                                                                                                 finaloxy)

            # Get difference and append data (heart rate)
            differenceHR = round(float(HrAvgList[WindowCount]) - float(heartRateValue))

            # Get difference and append data (blood oxygen)
            differenceSPO = round(float(SPOAvgList[WindowCount]) - float(oxygenSaturationValue))

            Listdata.append('WindowCount: ' + str(WindowCount) + " ,\t" + 'GroundTruthHeartRate: ' + str(
                round(HrAvgList[WindowCount])) + " ,\t" +
                            'ComputedHeartRate: ' + str(round(heartRateValue)) + " ,\t" + 'HRDifference: ' + str(
                differenceHR) + " ,\t" +
                            'GroundTruthSPO: ' + str(round(SPOAvgList[WindowCount])) + " ,\t" +
                            'ComputedSPO: ' + str(round(oxygenSaturationValue)) + " ,\t" + 'SPODifference: ' + str(
                differenceSPO) + " ,\t" +
                            'Regiontype: ' + " ,\t" + str(regiontype) + " ,\t" + FullTimeLog)

    # filename
    fileNameResult = "HRSPOwithLog_" + fileName
    #          regiontype + "_" + Algorithm_type + "_FFT-" + str(FFT_type) + "_FL-" + str(
    # Filter_type) + "_RS-" + str(Result_type) + "_PR-" + str(Preprocess_type) + "_SM-" + str(
    # isSmoothen)
    # Write data to file
    objFile.WriteListDatatoFile(SavePath + 'Result\\', fileNameResult, Listdata)

    # filename
    # fileNameSpo = "SPO_" + fileName
    # # Algorithm_type + "_FFT-" + str(FFT_type) + "_FL-" + str(
    # #     Filter_type) + "_RS-" + str(Result_type)  + "_PR-" + str(Preprocess_type) + "_SM-" + str(
    # #     isSmoothen)
    # # Write data to file
    # objFile.WriteListDatatoFile(SavePath+ 'Result\\', fileNameSpo, ListSPOdata)

    del objReliability
    del objProcessDataLips
    del objProcessDataRcheek
    del objProcessDataForehead
    del objProcessDataLcheek


def LogTime(self):
    logTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                       datetime.now().time().hour, datetime.now().time().minute,
                       datetime.now().time().second, datetime.now().time().microsecond)
    return logTime


'''
Process participants data over the entire signal data
'''


def Process_Participants_Data_WindowEntireSignal(ROIStore, SavePath,
                                      Algorithm_type, FFT_type, HrGr, SpoGr,
                                      Filter_type, Result_type, Preprocess_type, isSmoothen, fileName, DumpToDisk,ParticipantId,position,UpSampleData,AttemptType ):
    objReliability = CheckReliability()
    # Lists to hold heart rate and blood oxygen data
    Listdata = []
    # ListSPOdata = []
    bestHeartRateSnr = 0.0
    bestBpm = 0.0
    channeltype = ''
    regiontype = ''
    freqencySamplingError = 0.0
    previousComputedHeartRate = 0.0
    smallestOxygenError = sys.float_info.max
    finaloxy = 0.0
    FullTimeLog = None
    TotalWindowCalculationTime=None
    PreProcessTime=None
    AlgorithmTime=None
    FFTTime=None
    SmoothTime=None
    FilterTime=None
    ComputerHRSNRTime=None
    ComputerSPOTime=None
    SelectedColorFPS =0
    SelectedIRFPS=0
    SelectedColorFPSMethod =''
    SelectedIRFPSMethod =''
    ListobjParticipantsResultEntireSignalDataRow = []
    # ROI Window Result list
    WindowRegionList = {}
    minFPSIRvalue = min(ROIStore.get(objConfig.roiregions[0]).IRfpswithTime.values())
    maxFPSIRvalue = max(ROIStore.get(objConfig.roiregions[0]).IRfpswithTime.values())
    minFPSColorvalue = min(ROIStore.get(objConfig.roiregions[0]).ColorfpswithTime.values())
    maxFPSColorvalue = max(ROIStore.get(objConfig.roiregions[0]).ColorfpswithTime.values())
    FPSNotes = 'min IRvalue: '+ str(minFPSIRvalue) + ', max IRvalue: '+ str(maxFPSIRvalue) +', min Colorvalue: '+ str(minFPSColorvalue) + ', max Colorvalue: '+ str(maxFPSColorvalue)

    # Windows for regions (should be same for all)
    LengthofAllFramesColor = ROIStore.get(objConfig.roiregions[0]).getLengthColor()  # len()  # all have same lenghts
    LengthofAllFramesIR = ROIStore.get(objConfig.roiregions[0]).getLengthIR()
    TimeinSeconds = ROIStore.get(
        "lips").totalTimeinSeconds  # LengthofAllFrames / objProcessData.ColorEstimatedFPS  # take color as color and ir would run for same window
    timeinSeconds = round(TimeinSeconds)
    # step = 30  # slide window for 1 second or 30 frames.
    # this step will aslo be variable as per that seconds frame rate
    # WindowSlider = step * timeinSeconds  # step * 5 second,  window can hold  150 frames or 5 second data #THIS WORKS ONLY IF FPS IS 30 FOR EVERY SECOND so
    # window slider is calculated in variable frames within the window as it changes
    # TODO: CHECK FOR 5 AND 6 SECOND WINDOW COMPARED TO 10 with results
    # TotalWindows in this sample
    TotalWindows = 1
    # Split ground truth data
    HrAvg = CommonMethods.AvegrageGroundTruth(HrGr)#TODO: FIX FOR NEW more processed PARTICITPANTS
    SPOAvg = CommonMethods.AvegrageGroundTruth(SpoGr)

    # Initialise object to process face regions signal data
    objProcessDataLips = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                         SavePath,
                                         objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                         DumpToDisk, fileName)
    # Initialise object to process face regions signal data
    objProcessDataForehead = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                             SavePath,
                                             objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                             DumpToDisk, fileName)

    # Initialise object to process face regions signal data
    objProcessDataRcheek = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                           SavePath,
                                           objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                           DumpToDisk, fileName)

    # Initialise object to process face regions signal data
    objProcessDataLcheek = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                           SavePath,
                                           objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                           DumpToDisk, fileName)
    # Loop through signal data#a
    for WindowCount in range(0, int(TotalWindows)):  # RUNNING FOR WINDOW TIMES # TimeinSeconds
        # print('Window: '+ str(WindowCount))
        # Lips
        objProcessDataLips.getSingalData(ROIStore, objConfig.roiregions[0], WindowCount, TotalWindows,
                                               timeinSeconds)
        lipsResult = objProcessDataLips.Process_EntireSignalData(objConfig.RunAnalysisForEntireSignalData,DumpToDisk)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'lipsResult_Window_' + str(WindowCount), lipsResult)

        # Forehead
        objProcessDataForehead.getSingalData(ROIStore, objConfig.roiregions[1],
                                                   WindowCount, TotalWindows, timeinSeconds)  # Lips
        foreheadResult = objProcessDataForehead.Process_EntireSignalData(objConfig.RunAnalysisForEntireSignalData,DumpToDisk)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'foreheadResult_Window_' + str(WindowCount), foreheadResult)

        # LeftCheek
        objProcessDataLcheek.getSingalData(ROIStore, objConfig.roiregions[2],
                                                 WindowCount, TotalWindows, timeinSeconds)
        leftcheekResult = objProcessDataLcheek.Process_EntireSignalData(objConfig.RunAnalysisForEntireSignalData,DumpToDisk)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'leftcheekResult_Window_' + str(WindowCount), leftcheekResult)

        # RightCheek
        objProcessDataRcheek.getSingalData(ROIStore, objConfig.roiregions[3],
                                                 WindowCount, TotalWindows, timeinSeconds)
        rightcheekResult = objProcessDataRcheek.Process_EntireSignalData(objConfig.RunAnalysisForEntireSignalData,DumpToDisk)
        if (DumpToDisk):
            objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
                                     'rightcheekResult_Window_' + str(WindowCount), rightcheekResult)

        # Store Data in Window List
        WindowRegionList['lips'] = lipsResult
        WindowRegionList['forehead'] = foreheadResult
        WindowRegionList['rightcheek'] = rightcheekResult
        WindowRegionList['leftcheek'] = leftcheekResult

        # Get best region data
        for k, v in WindowRegionList.items():
            if (v.BestSnR > bestHeartRateSnr):
                bestHeartRateSnr = v.BestSnR
                bestBpm = v.BestBPM
                channeltype = v.channeltype
                regiontype = k
                freqencySamplingError = v.FrequencySamplieErrorForChannel
                # diffNow = v.diffTime#TODO: UPDATE
                # diffTimeLog = v.diffTimeLog#TODO: UPDATE
                # FullTimeLog = v.gettimeDifferencesToString()#TODO: UPDATE
                SelectedColorFPS = v.SelectedColorFPS
                SelectedIRFPS = v.SelectedIRFPS
                SelectedColorFPSMethod = v.SelectedColorFPSMethod
                SelectedIRFPSMethod = v.SelectedIRFPSMethod

                TotalWindowCalculationTime,PreProcessTime,AlgorithmTime,\
                FFTTime,SmoothTime,FilterTime,\
                ComputerHRSNRTime,ComputerSPOTime = v.gettimeDifferencesToStringIndividual()

            if (v.oxygenSaturationValueError < smallestOxygenError):
                smallestOxygenError = v.oxygenSaturationValueError
                finaloxy = v.oxygenSaturationValueValue

        if (bestBpm > 30 and bestBpm <300):
            # Check reliability and record best readings
            heartRateValue, heartRateError = objReliability.AcceptorRejectHR(bestHeartRateSnr, bestBpm,
                                                                             freqencySamplingError)
            oxygenSaturationValue, oxygenSaturationValueError = objReliability.AcceptorRejectSPO(smallestOxygenError,
                                                                                                 finaloxy)

            # Get difference and append data (heart rate)
            differenceHR = (float(HrAvg) - float(heartRateValue))

            # Get difference and append data (blood oxygen)
            differenceSPO = round(float(SPOAvg) - float(oxygenSaturationValue))

            # ###Store in list or Datatbase#TODO: UPDATE
            # Listdata.append('WindowCount: ' + str(WindowCount) + " ,\t" + 'GroundTruthHeartRate: ' + str(
            #     round(HrAvg)) + " ,\t" +
            #                 'ComputedHeartRate: ' + str(round(heartRateValue)) + " ,\t" + 'HRDifference: ' + str(
            #     differenceHR) + " ,\t" +
            #                 'GroundTruthSPO: ' + str(round(SPOAvg)) + " ,\t" +
            #                 'ComputedSPO: ' + str(round(oxygenSaturationValue)) + " ,\t" + 'SPODifference: ' + str(
            #     differenceSPO) + " ,\t" +
            #                 'Regiontype: ' + " ,\t" + str(regiontype) + " ,\t" + FullTimeLog)
            bestSnrString= str(float(bestHeartRateSnr))
            if(bestSnrString == "inf"):
                bestSnrString = '-1'
            objParticipantsResultEntireSignalDataRow = ParticipantsResultEntireSignalDataRow()
            objParticipantsResultEntireSignalDataRow.ParticipantId = ParticipantId
            objParticipantsResultEntireSignalDataRow.HeartRateStatus = position
            objParticipantsResultEntireSignalDataRow.bestHeartRateSnr =bestSnrString
            objParticipantsResultEntireSignalDataRow.bestBPM = str(float(bestBpm))
            objParticipantsResultEntireSignalDataRow.channelType = channeltype
            objParticipantsResultEntireSignalDataRow.regionType = regiontype
            objParticipantsResultEntireSignalDataRow.FrequencySamplingError = str(float(freqencySamplingError))
            objParticipantsResultEntireSignalDataRow.oxygenSaturationValueError = str(float(oxygenSaturationValueError))
            objParticipantsResultEntireSignalDataRow.heartRateError = str(float(heartRateError))
            objParticipantsResultEntireSignalDataRow.bestSPO = str(float(finaloxy))
            objParticipantsResultEntireSignalDataRow.HeartRateValue = str(float(heartRateValue))
            objParticipantsResultEntireSignalDataRow.SPOValue = str(float(oxygenSaturationValue))
            objParticipantsResultEntireSignalDataRow.differenceHR = str(float(differenceHR))
            objParticipantsResultEntireSignalDataRow.differenceSPO = str(float(differenceSPO))
            objParticipantsResultEntireSignalDataRow.TotalWindowCalculationTimeTaken = str(TotalWindowCalculationTime)
            objParticipantsResultEntireSignalDataRow.PreProcessTimeTaken = str(PreProcessTime)
            objParticipantsResultEntireSignalDataRow.AlgorithmTimeTaken = str(AlgorithmTime)
            objParticipantsResultEntireSignalDataRow.FFTTimeTaken = str(FFTTime)
            objParticipantsResultEntireSignalDataRow.SmoothTimeTaken = str(SmoothTime)
            objParticipantsResultEntireSignalDataRow.FilterTimeTaken = str(FilterTime)
            objParticipantsResultEntireSignalDataRow.ComputingHRSNRTimeTaken = str(ComputerHRSNRTime)
            objParticipantsResultEntireSignalDataRow.ComputingSPOTimeTaken = str(ComputerSPOTime)
            # objParticipantsResultEntireSignalDataRow.TechniqueId = None
            objParticipantsResultEntireSignalDataRow.Algorithm_type = str(Algorithm_type)
            objParticipantsResultEntireSignalDataRow.FFT_type = str(FFT_type)
            objParticipantsResultEntireSignalDataRow.Filter_type = str(Filter_type)
            objParticipantsResultEntireSignalDataRow.Result_type = str(Result_type)
            objParticipantsResultEntireSignalDataRow.Preprocess_type = str(Preprocess_type)
            objParticipantsResultEntireSignalDataRow.isSmoothen = str(isSmoothen)
            objParticipantsResultEntireSignalDataRow.UpSampled = '1' if UpSampleData == True else '0'
            objParticipantsResultEntireSignalDataRow.ColorFPS = str(SelectedColorFPS)
            objParticipantsResultEntireSignalDataRow.IRFPS = str(SelectedIRFPS)
            objParticipantsResultEntireSignalDataRow.SelectedColorFPSMethod = str(SelectedColorFPSMethod)
            objParticipantsResultEntireSignalDataRow.SelectedIRFPSMethod = str(SelectedIRFPSMethod)
            objParticipantsResultEntireSignalDataRow.GroundTruthHeartRate = str(float(HrAvg))
            objParticipantsResultEntireSignalDataRow.GroundTruthSPO = str(float(SPOAvg))
            objParticipantsResultEntireSignalDataRow.AttemptType = str(AttemptType)
            objParticipantsResultEntireSignalDataRow.FPSNotes = FPSNotes
            ListobjParticipantsResultEntireSignalDataRow.append(objParticipantsResultEntireSignalDataRow)
            # objSQLConfig.SaveRowParticipantsResultsEntireSignal(objParticipantsResultEntireSignalDataRow)

    # filename

    # fileNameResult = "HRSPOwithLog_" + fileName #+ '_UpSampleData-'+ str(UpSampleData)#ParticipantId+ "_" +position+
    #          regiontype + "_" + Algorithm_type + "_FFT-" + str(FFT_type) + "_FL-" + str(
    # Filter_type) + "_RS-" + str(Result_type) + "_PR-" + str(Preprocess_type) + "_SM-" + str(
    # isSmoothen)
    # Write data to file
    # objFile.WriteListDatatoFile(SavePath + 'Result\\', fileNameResult, Listdata)
    # objFile.WriteListDatatoFile('E:\\ARPOS_Server_Data\\Server_Study_Data\\Europe_WhiteSkin_Group\\BoxPlotCSV\\FinalBestCases\\', fileNameResult, Listdata)

    # filename
    # fileNameSpo = "SPO_" + fileName
    # # Algorithm_type + "_FFT-" + str(FFT_type) + "_FL-" + str(
    # #     Filter_type) + "_RS-" + str(Result_type)  + "_PR-" + str(Preprocess_type) + "_SM-" + str(
    # #     isSmoothen)
    # # Write data to file
    # objFile.WriteListDatatoFile(SavePath+ 'Result\\', fileNameSpo, ListSPOdata)

    del objReliability
    del objProcessDataLips
    del objProcessDataRcheek
    del objProcessDataForehead
    del objProcessDataLcheek


    if(len(ListobjParticipantsResultEntireSignalDataRow)>0):
        return ListobjParticipantsResultEntireSignalDataRow[0] # TODO: FIX FOR WINDOW LATER
    else:
        return 'NO HR'

def Process_Participants_Data_EntireSignalINChunks(ROIStore, SavePath, HrGr, SpoGr, fileName, DumpToDisk, ProcessingStep,
                                           ProcessingType):
    objReliability = CheckReliability()
    # Lists to hold heart rate and blood oxygen data
    Listdata = []
    # ListSPOdata = []
    bestHeartRateSnr = 0.0
    bestBpm = 0.0
    channeltype = ''
    regiontype = ''
    freqencySamplingError = 0.0
    previousComputedHeartRate = 0.0
    smallestOxygenError = sys.float_info.max
    finaloxy = 0.0
    FullTimeLog = None

    # ROI Window Result list
    WindowRegionList = {}

    # Windows for regions (should be same for all)
    TimeinSeconds = ROIStore.get(
        "lips").totalTimeinSeconds  # LengthofAllFrames / objProcessData.ColorEstimatedFPS  # take color as color and ir would run for same window
    timeinSeconds = TimeinSeconds
    TotalWindows = 1
    # Split ground truth data
    HrAvgList = CommonMethods.AvegrageGroundTruth(HrGr)
    SPOAvgList = CommonMethods.AvegrageGroundTruth(SpoGr)

    # Loop through signal data
    WindowCount = 0
    # Initialise object to process face regions signal data
    Algorithm_type = 0
    FFT_type = 0
    Filter_type = 0
    Result_type = 0
    Preprocess_type = 0
    isSmoothen = 0
    if (ProcessingStep == 'PreProcess'):
        Preprocess_type = ProcessingType

    for k, v in ROIStore.items():

        objProcessData = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type,
                                         SavePath,
                                         objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds,
                                         DumpToDisk, fileName)
        objProcessData.getSingalDataWindow(ROIStore, objConfig.roiregions[0], WindowCount, TotalWindows, timeinSeconds)

        if (ProcessingStep == 'PreProcessing'):
            # Log Start Time  signal data
            startLogTime = LogTime()  # foreach region
            # PreProcess Signal
            processedBlue, processedGreen, processedRed, processedGrey, processedIR = objProcessData.preprocessSignalData(
                objProcessData.regionBlueData, objProcessData.regionGreenData,
                objProcessData.regionRedData, objProcessData.regionGreyData,
                objProcessData.regionIRData)

            endlogTime = LogTime()
            diffTime = endlogTime - startLogTime
            objProcessData.regionWindowBlueData = processedBlue
            objProcessData.regionWindowGreenData = processedGreen
            objProcessData.regionWindowRedData = processedRed
            objProcessData.regionWindowGreyData = processedGrey
            objProcessData.regionWindowIRData = processedIR
            objProcessData.WindowProcessStartTime = startLogTime
            objProcessData.WindowProcessEndTime = endlogTime
            objProcessData.WindowProcessDifferenceTime = diffTime

            WindowRegionList[k] = objProcessData

        elif (ProcessingStep == 'Algorithm'):
            startLogTime = LogTime()  # foreach region
            # Apply Algorithm
            processedBlue, processedGreen, processedRed, processedGrey, processedIR = objProcessData.ApplyAlgorithm(
                objProcessData.regionBlueData, objProcessData.regionGreenData,
                objProcessData.regionRedData, objProcessData.regionGreyData,
                objProcessData.regionIRData)
            endlogTime = LogTime()
            diffTime = endlogTime - startLogTime

            objProcessData.regionWindowBlueData = processedBlue
            objProcessData.regionWindowGreenData = processedGreen
            objProcessData.regionWindowRedData = processedRed
            objProcessData.regionWindowGreyData = processedGrey
            objProcessData.regionWindowIRData = processedIR
            objProcessData.WindowProcessStartTime = startLogTime
            objProcessData.WindowProcessEndTime = endlogTime
            objProcessData.WindowProcessDifferenceTime = diffTime

            WindowRegionList[k] = objProcessData

        elif (ProcessingStep == 'Smoothen'):
            startLogTime = LogTime()  # foreach region
            # Smooth Signal
            processedBlue = objProcessData.SmoothenData(objProcessData.regionBlueData)
            processedGreen = objProcessData.SmoothenData(objProcessData.regionGreenData)
            processedRed = objProcessData.SmoothenData(objProcessData.regionRedData)
            processedGrey = objProcessData.SmoothenData(objProcessData.regionGreyData)
            processedIR = objProcessData.SmoothenData(objProcessData.regionIRData)
            endlogTime = LogTime()
            diffTime = endlogTime - startLogTime

            objProcessData.regionWindowBlueData = processedBlue
            objProcessData.regionWindowGreenData = processedGreen
            objProcessData.regionWindowRedData = processedRed
            objProcessData.regionWindowGreyData = processedGrey
            objProcessData.regionWindowIRData = processedIR
            objProcessData.WindowProcessStartTime = startLogTime
            objProcessData.WindowProcessEndTime = endlogTime
            objProcessData.WindowProcessDifferenceTime = diffTime

            WindowRegionList[k] = objProcessData

        elif (ProcessingStep == 'FFT'):
            startLogTime = LogTime()  # foreach region
            # Apply FFT
            processedBlue, processedGreen, processedRed, processedGrey, processedIR = objProcessData.ApplyFFT(
                objProcessData.regionBlueData, objProcessData.regionGreenData,
                objProcessData.regionRedData, objProcessData.regionGreyData,
                objProcessData.regionIRData)
            endlogTime = LogTime()
            diffTime = endlogTime - startLogTime

            objProcessData.regionWindowBlueData = processedBlue
            objProcessData.regionWindowGreenData = processedGreen
            objProcessData.regionWindowRedData = processedRed
            objProcessData.regionWindowGreyData = processedGrey
            objProcessData.regionWindowIRData = processedIR
            objProcessData.WindowProcessStartTime = startLogTime
            objProcessData.WindowProcessEndTime = endlogTime
            objProcessData.WindowProcessDifferenceTime = diffTime

            WindowRegionList[k] = objProcessData

        elif (ProcessingStep == 'Filter'):
            startLogTime = LogTime()  # foreach region
            # Apply FFT
            processedBlue, processedGreen, processedRed, processedGrey, processedIR = objProcessData.FilterTechniques(
                objProcessData.regionBlueData, objProcessData.regionGreenData,
                objProcessData.regionRedData, objProcessData.regionGreyData,
                objProcessData.regionIRData)
            endlogTime = LogTime()
            diffTime = endlogTime - startLogTime

            objProcessData.regionWindowBlueData = processedBlue
            objProcessData.regionWindowGreenData = processedGreen
            objProcessData.regionWindowRedData = processedRed
            objProcessData.regionWindowGreyData = processedGrey
            objProcessData.regionWindowIRData = processedIR
            objProcessData.WindowProcessStartTime = startLogTime
            objProcessData.WindowProcessEndTime = endlogTime
            objProcessData.WindowProcessDifferenceTime = diffTime

            WindowRegionList[k] = objProcessData
        # elif(ProcessingStep == 'CalculateHRSNR'):
            # windowList = Window_Data()
            # windowList.WindowNo = self.Window_count
            # windowList.LogTime(LogItems.Start_Total)
            # windowList.isSmooth = self.isSmoothen
            # windowList.fileName = self.fileName
            # startLogTime = LogTime()  # foreach region
            # objProcessData.generateHeartRateandSNR(objProcessData.regionBlueData, objProcessData.regionGreenData,
            #     objProcessData.regionRedData, objProcessData.regionGreyData,
            #     objProcessData.regionIRData, objProcessData.Result_type)
            # endlogTime = LogTime()
            # diffTime = endlogTime - startLogTime
            #
            # # get best bpm and heart rate period in one region
            # objProcessData.bestHeartRateSnr = 0.0
            # objProcessData.bestBpm = 0.0
            # objProcessData.GetBestBpm()
            #
            # # calculate SPO
            # startLogTime = LogTime()  # foreach region
            # windowList.LogTime(LogItems.Start_SPO)
            # std, err, oxylevl = objProcessData.getSpo(grey, Gy_filtered, objProcessData.regionWindowIRData, red,
            #                                 objProcessData.distanceM)  # Irchannel and distanceM as IR channel lengh can be smaller so passing full array
            # endlogTime = LogTime()
            # diffTime = endlogTime - startLogTime
            #
            # # SPO
            # windowList.SignalWindowSPOgrey = grey
            # windowList.SignalWindowSPOIrchannel = Irchannel
            # windowList.SignalWindowSPOred = red
            # windowList.SignalWindowSPOdistance = distanceM
            # windowList.SignalWindowSPOGy_filtered = Gy_filtered
            #
            # # HR
            # windowList.SNRSummary = self.SNRSummary
            # windowList.channeltype = self.channeltype
            # windowList.WindowNo = self.Window_count
            # windowList.BestBPM = self.bestBpm
            # windowList.BestSnR = self.bestHeartRateSnr
            # windowList.IrSnr = self.IrSnr
            # windowList.GreySnr = self.GreySnr
            # windowList.RedSnr = self.RedSnr
            # windowList.GreenSnr = self.GreenSnr
            # windowList.BlueSnr = self.BlueSnr
            # windowList.BlueBpm = self.BlueBpm
            # windowList.IrBpm = self.IrBpm
            # windowList.GreyBpm = self.GreyBpm
            # windowList.RedBpm = self.RedBpm
            # windowList.GreenBpm = self.GreenBpm
            # windowList.regiontype = self.region
            # windowList.IrFreqencySamplingError = self.IrFreqencySamplingError
            # windowList.GreyFreqencySamplingError = self.GreyFreqencySamplingError
            # windowList.RedFreqencySamplingError = self.RedFreqencySamplingError
            # windowList.GreenFreqencySamplingError = self.GreenFreqencySamplingError
            # windowList.BlueFreqencySamplingError = self.BlueFreqencySamplingError
            # windowList.oxygenSaturationSTD = std  # std
            # windowList.oxygenSaturationValueError = err  # err
            # windowList.oxygenSaturationValueValue = oxylevl  # oxylevl
            # windowList.timeDifferences()
    # if (DumpToDisk):
    #     objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
    #                              'lipsResult_Window_' + str(WindowCount), objProcessDataLips)
    #     objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
    #                              'foreheadResult_Window_' + str(WindowCount), objProcessDataForehead)
    #     objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
    #                              'leftcheekResult_Window_' + str(WindowCount), objProcessDataLcheek)
    #     objFile.DumpObjecttoDisk(SavePath + fileName + '_WindowsBinaryFiles' + '\\',
    #                              'rightcheekResult_Window_' + str(WindowCount), objProcessDataRcheek)

    # # Store Data in Window List ###OLD
    # WindowRegionList['lips'] = lipsResult
    # WindowRegionList['forehead'] = foreheadResult
    # WindowRegionList['rightcheek'] = rightcheekResult
    # WindowRegionList['leftcheek'] = leftcheekResult

    # Get best region data
    # for k, v in WindowRegionList.items():
    #     if (v.BestSnR > bestHeartRateSnr):
    #         bestHeartRateSnr = v.BestSnR
    #         bestBpm = v.BestBPM
    #         channeltype = v.channeltype
    #         regiontype = k
    #         freqencySamplingError = v.IrFreqencySamplingError
    #         diffNow = v.diffTime
    #         diffTimeLog = v.diffTimeLog
    #         FullTimeLog = v.gettimeDifferencesToString()
    #
    #     if (v.oxygenSaturationValueError < smallestOxygenError):
    #         smallestOxygenError = v.oxygenSaturationValueError
    #         finaloxy = v.oxygenSaturationValueValue

    # if(bestBpm>0):
    #     # Check reliability and record best readings
    #     heartRateValue, heartRateError = objReliability.AcceptorRejectHR(bestHeartRateSnr, bestBpm,
    #                                                                      freqencySamplingError)
    #     oxygenSaturationValue, oxygenSaturationValueError = objReliability.AcceptorRejectSPO(smallestOxygenError,
    #                                                                                          finaloxy)
    #
    #     # Get difference and append data (heart rate)
    #     differenceHR = round(float(HrAvgList[WindowCount]) - float(heartRateValue))
    #
    #     # Get difference and append data (blood oxygen)
    #     differenceSPO = round(float(SPOAvgList[WindowCount]) - float(oxygenSaturationValue))
    #
    #     Listdata.append('WindowCount: ' + str(WindowCount) + " ,\t" + 'GroundTruthHeartRate: ' +  str(round(HrAvgList[WindowCount])) + " ,\t" +
    #                       'ComputedHeartRate: ' + str(round(heartRateValue)) + " ,\t" + 'HRDifference: ' +str(differenceHR)+ " ,\t" +
    #                       'GroundTruthSPO: ' + str(round(SPOAvgList[WindowCount])) + " ,\t" +
    #                       'ComputedSPO: '  + str(round(oxygenSaturationValue)) + " ,\t" + 'SPODifference: ' + str(differenceSPO) + " ,\t" +
    #                       'Regiontype: ' + " ,\t" + str(regiontype) + " ,\t"  + FullTimeLog)

    # filename
    # fileNameResult = "HRSPOwithLog_" + fileName
    # # Write data to file
    # objFile.WriteListDatatoFile(SavePath + 'Result\\', fileNameResult, Listdata)

    del objReliability
    # del objProcessDataLips
    # del objProcessDataRcheek
    # del objProcessDataForehead
    # del objProcessDataLcheek

    # # Lists to hold heart rate and blood oxygen data
    # ListHrdata = []
    # ListSPOdata = []
    #
    # objReliability = CheckReliability()
    #
    # diffNow = 0.0
    # bestHeartRateSnr = 0.0
    # bestBpm = 0.0
    # channeltype = ''
    # regiontype = ''
    # IsSuccess = ''
    # finaloxy = 0.0
    # freqencySamplingError = 0.0
    # smallestOxygenError = sys.float_info.max
    # timeinSeconds = ROIStore.get("lips").totalTimeinSeconds  # this is same for all regions as no of frames are same recorded for that time peroid so we can use any region to get time
    # # leng = len(ROIStore.get("lips").Irchannel)
    #
    # # Initialise object to process face regions signal data
    # objProcessData = ProcessFaceData(Algorithm_type, FFT_type, Filter_type, Result_type, Preprocess_type, SavePath,
    #                                  objConfig.ignoregray, isSmoothen, objConfig.GenerateGraphs, timeinSeconds
    #                                  )
    #
    # # ROI Window Result list
    # WindowRegionList = {}
    #
    # # Average ground truth data
    # HrAvegrage = (np.average(CommonMethods.AvegrageGroundTruth(HrGr)))
    # SPOAvegrage = (np.average(CommonMethods.AvegrageGroundTruth(SpoGr)))
    #
    # # Lips
    # objProcessData.getSingalData(ROIStore, objConfig.roiregions[0])
    # lipsResult = objProcessData.Process_EntireSignalData()
    #
    # # Forehead
    # objProcessData.getSingalData(ROIStore, objConfig.roiregions[1])
    # foreheadResult = objProcessData.Process_EntireSignalData()
    #
    # # LeftCheek
    # objProcessData.getSingalData(ROIStore, objConfig.roiregions[2])
    # leftcheekResult = objProcessData.Process_EntireSignalData()
    #
    # # RightCheek
    # objProcessData.getSingalData(ROIStore, objConfig.roiregions[3])
    # rightcheekResult = objProcessData.Process_EntireSignalData()
    #
    # # Store Data in Window List
    # WindowRegionList['lips'] = lipsResult
    # WindowRegionList['forehead'] = foreheadResult
    # WindowRegionList['rightcheek'] = rightcheekResult
    # WindowRegionList['leftcheek'] = leftcheekResult
    # diffTimeTotal = {}
    #
    # # Get best region data
    # for k, v in WindowRegionList.items():
    #     if(v.BestSnR > bestHeartRateSnr):
    #         bestHeartRateSnr = v.BestSnR
    #         bestBpm = v.BestBPM
    #         # channeltype = v.
    #         regiontype = k
    #         # freqencySamplingError = v.IrFreqencySamplingError
    #         diffNow = v.diffTime
    #         diffTimeTotal = v.diffTimeLog
    #     # if (v.IrSnr > bestHeartRateSnr):
    #     #     bestHeartRateSnr = v.IrSnr
    #     #     bestBpm = v.IrBpm
    #     #     channeltype = 'IR'
    #     #     regiontype = k
    #     #     freqencySamplingError = v.IrFreqencySamplingError
    #     #     diffNow = v.diffTime
    #     #     diffTimeTotal = v.diffTimeLog
    #     #
    #     # if (v.GreySnr > bestHeartRateSnr):
    #     #     bestHeartRateSnr = v.GreySnr
    #     #     bestBpm = v.GreyBpm
    #     #     channeltype = 'Grey'
    #     #     regiontype = k
    #     #     freqencySamplingError = v.GreyFreqencySamplingError
    #     #     diffNow = v.diffTime
    #     #     diffTimeTotal = v.diffTimeLog
    #     #
    #     # if (v.RedSnr > bestHeartRateSnr):
    #     #     bestHeartRateSnr = v.RedSnr
    #     #     bestBpm = v.RedBpm
    #     #     channeltype = 'Red'
    #     #     regiontype = k
    #     #     freqencySamplingError = v.RedFreqencySamplingError
    #     #     diffNow = v.diffTime
    #     #     diffTimeTotal = v.diffTimeLog
    #     #
    #     # if (v.GreenSnr > bestHeartRateSnr):
    #     #     bestHeartRateSnr = v.GreenSnr
    #     #     bestBpm = v.GreenBpm
    #     #     channeltype = 'Green'
    #     #     regiontype = k
    #     #     freqencySamplingError = v.GreenFreqencySamplingError
    #     #     diffNow = v.diffTime
    #     #     diffTimeTotal = v.diffTimeLog
    #     #
    #     # if (v.BlueSnr > bestHeartRateSnr):
    #     #     bestHeartRateSnr = v.BlueSnr
    #     #     bestBpm = v.BlueBpm
    #     #     channeltype = 'Blue'
    #     #     regiontype = k
    #     #     freqencySamplingError = v.BlueFreqencySamplingError
    #     #     diffNow = v.diffTime
    #     #     diffTimeTotal = v.diffTimeLog
    #
    #     if (v.oxygenSaturationValueError < smallestOxygenError):
    #         smallestOxygenError = v.oxygenSaturationValueError
    #         finaloxy = v.oxygenSaturationValueValue
    #
    # if (regiontype != ''):
    #     IsSuccess = True
    #     # Check reliability and record best readings
    #     heartRateValue, heartRateError = objReliability.AcceptorRejectHR(bestHeartRateSnr, bestBpm, freqencySamplingError)
    #     oxygenSaturationValue, oxygenSaturationValueError = objReliability.AcceptorRejectSPO(smallestOxygenError, finaloxy)
    #
    #     # Get difference and append data (heart rate)
    #     difference = round(float(HrAvegrage) - float(round(heartRateValue)))
    #     ListHrdata.append(str(round(HrAvegrage)) + " ,\t" + str(round(heartRateValue)) + " ,\t" + str(difference)+ " ,\t" + str(diffNow)+ " ,\t" + str(regiontype))
    #
    #     # Get difference and append data (blood oxygen)
    #     difference = round(float(SPOAvegrage) - float(oxygenSaturationValue))
    #     ListSPOdata.append(str(round(SPOAvegrage)) + " ,\t" + str(round(oxygenSaturationValue)) + " ,\t" + str(difference) + str(diffNow)+ " ,\t" + str(regiontype))
    #
    #     printTime = ''
    #     for k, v in diffTimeTotal.items():
    #         printTime = printTime + str(k) + ': ' + str(v) + '\n'
    #
    #     objFile = FileIO()
    #     objFile.WritedatatoFile(SavePath,'timeLogFile',printTime)
    #     del objFile
    #
    # # # Write data to file
    # # objFile.WriteListDatatoFile(SavePath, fileNameHr, ListHrdata)
    # # objFile.WriteListDatatoFile(SavePath, fileNameSpo, ListSPOdata)
    # else:
    #     IsSuccess = False
    #
    # del objReliability
    # del objProcessData
    #
    # return ListHrdata, ListSPOdata, IsSuccess


'''
Process participants data over the entire signal data
'''
def Process_Participants_Data_GetBestHR(objresultProcessedDataLips, objresultProcessedDataForehead,
                                        objresultProcessedDataRcheek, objresultProcessedDataLCheek, SavePath, HrGr,
                                        filename):
    ##Copy obj compute HR data to local class
    # objresultProcessedData.IrSnr = objComputerHeartRate.IrSnr
    # objresultProcessedData.GreySnr = objComputerHeartRate.GreySnr
    # objresultProcessedData.RedSnr = objComputerHeartRate.RedSnr
    # objresultProcessedData.GreenSnr = objComputerHeartRate.GreenSnr
    # objresultProcessedData.BlueSnr = objComputerHeartRate.BlueSnr
    # objresultProcessedData.IrBpm = objComputerHeartRate.IrBpm
    # objresultProcessedData.GreyBpm = objComputerHeartRate.GreyBpm
    # objresultProcessedData.RedBpm = objComputerHeartRate.RedBpm
    # objresultProcessedData.GreenBpm = objComputerHeartRate.GreenBpm
    # objresultProcessedData.BlueBpm = objComputerHeartRate.BlueBpm
    # objresultProcessedData.IrFreqencySamplingError = objComputerHeartRate.IrFreqencySamplingError
    # objresultProcessedData.GreyFreqencySamplingError = objComputerHeartRate.GreyFreqencySamplingError
    # objresultProcessedData.RedFreqencySamplingError = objComputerHeartRate.RedFreqencySamplingError
    # objresultProcessedData.GreenFreqencySamplingError = objComputerHeartRate.GreenFreqencySamplingError
    # objresultProcessedData.BlueFreqencySamplingError = objComputerHeartRate.BlueFreqencySamplingError
    # objresultProcessedData.startTime = startTime
    # objresultProcessedData.endTime = endTime
    # objresultProcessedData.diffTime = diffTime
    # objresultProcessedData.blue_fft_realabs = blue_fft_realabs
    # objresultProcessedData.green_fft_realabs = green_fft_realabs
    # objresultProcessedData.red_fft_realabs = red_fft_realabs
    # objresultProcessedData.grey_fft_realabs = grey_fft_realabs
    # objresultProcessedData.ir_fft_realabs = ir_fft_realabs
    # Lists to hold heart rate and blood oxygen data
    ListHrdata = []

    objReliability = CheckReliability()

    diffNow = 0.0
    regiontype = ''
    freqencySamplingError = 0.0

    # ROI Window Result list
    WindowRegionList = {}

    # Average ground truth data
    HrAvegrage = (np.average(CommonMethods.AvegrageGroundTruth(HrGr)))

    # Store Data in Window List
    WindowRegionList['lips'] = objresultProcessedDataLips
    WindowRegionList['forehead'] = objresultProcessedDataForehead
    WindowRegionList['rightcheek'] = objresultProcessedDataRcheek
    WindowRegionList['leftcheek'] = objresultProcessedDataLCheek

    # get best bpm and heart rate period in one region
    bestHeartRateSnr = 0.0
    bestBpm = 0.0

    # Get best region data
    for k, v in WindowRegionList.items():
        if (v.IrSnr > bestHeartRateSnr):
            bestHeartRateSnr = v.IrSnr
            bestBpm = v.IrBpm
            freqencySamplingError = v.IrFreqencySamplingError

        if (v.GreySnr > bestHeartRateSnr):
            bestHeartRateSnr = v.GreySnr
            bestBpm = v.GreyBpm
            freqencySamplingError = v.GreyFreqencySamplingError

        if (v.RedSnr > bestHeartRateSnr):
            bestHeartRateSnr = v.RedSnr
            bestBpm = v.RedBpm
            freqencySamplingError = v.RedFreqencySamplingError

        if (v.GreenSnr > bestHeartRateSnr):
            bestHeartRateSnr = v.GreenSnr
            bestBpm = v.GreenBpm
            freqencySamplingError = v.GreenFreqencySamplingError

        if (v.BlueSnr > bestHeartRateSnr):
            bestHeartRateSnr = v.BlueSnr
            bestBpm = v.BlueBpm
            freqencySamplingError = v.BlueFreqencySamplingError

    # Check reliability and record best readings
    heartRateValue, heartRateError = objReliability.AcceptorRejectHR(bestHeartRateSnr, bestBpm, freqencySamplingError)

    # Get difference and append data (heart rate)
    difference = round(float(HrAvegrage) - float(heartRateValue))
    ListHrdata.append(
        str(round(HrAvegrage)) + " ,\t" + str(round(heartRateValue)) + " ,\t" + str(difference) + " ,\t" + str(
            diffNow) + " ,\t" + str(regiontype))

    # printTime = str(start) + ': ' + str(v) + '\n'

    objFile = FileIO()
    # objFile.WritedatatoFile(SavePath,'timeLogFile',printTime)
    objFile.WriteListDatatoFile(SavePath, filename, ListHrdata)
    del objFile

    del objReliability

    # return ListHrdata

class ParticipantsResultEntireSignalDataRow:
    ParticipantId = None
    HeartRateStatus = None
    bestHeartRateSnr = None
    bestBPM = None
    channelType = None
    regionType = None
    FrequencySamplingError = None
    oxygenSaturationValueError = None
    heartRateError = None
    bestSPO = None
    HeartRateValue = None
    SPOValue = None
    differenceHR = None
    differenceSPO = None
    TotalWindowCalculationTimeTaken = None
    PreProcessTimeTaken = None
    AlgorithmTimeTaken = None
    FFTTimeTaken = None
    SmoothTimeTaken = None
    FilterTimeTaken = None
    ComputingHRSNRTimeTaken = None
    ComputingSPOTimeTaken = None
    TechniqueId = 0
    Algorithm_type = ''
    FFT_type = ''
    Filter_type = ''
    Result_type = ''
    Preprocess_type = ''
    isSmoothen = ''
    UpSampled = None
    ColorFPS = None
    IRFPS = None
    SelectedColorFPSMethod = ''
    SelectedIRFPSMethod = ''
    GroundTruthHeartRate = None
    GroundTruthSPO = None
    AttemptType = '1'
    FPSNotes = ''