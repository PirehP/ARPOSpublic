import os
import glob

import cv2
import numpy as np
from cv2 import IMREAD_UNCHANGED
import datetime
import collections

"""
LoadFaceData Class:
Paramters and functions to Load, Sort, getMean, and other pre processing loading data implemented
"""
class LoadFaceData:
    # Image r,g,b,ir,grey data arrays
    red = []
    blue = []
    green = []
    grey = []
    Irchannel = []

    Tempred = []
    Tempblue = []
    Tempgreen = []
    Tempgrey = []
    TempIrchannel=[]
    TempFrametime_list_ir = []
    TempFrametime_list_color = []
    TemptimecolorCount = []
    TemptimeirCount = []
    TempdistanceM = []

    #Time stamp arrays for rgb grey and ir channels
    time_list_color = []
    time_list_ir = []
    Frametime_list_ir =[]
    Frametime_list_color =[]
    timecolorCount = []
    timeirCount = []
    totalTimeinSeconds = 0

    #Depth
    distanceM = []

    #start and end time for data
    HasStartTime = 0
    StartTime = datetime.datetime.now()
    EndTime = datetime.datetime.now()

    # Ohter constatns#
    ColorEstimatedFPS = 0
    IREstimatedFPS = 0
    ColorfpswithTime = {}
    IRfpswithTime= {}

    def Clear(self):
        self.red = []
        self.blue = []
        self.green = []
        self.grey = []
        self.Irchannel = []

        self.Tempred = []
        self.Tempblue = []
        self.Tempgreen = []
        self.Tempgrey = []
        self.TempIrchannel = []
        self.TempdistanceM = []
        self.TempFrametime_list_ir = []
        self.TempFrametime_list_color = []
        self.TemptimecolorCount = []
        self.TemptimeirCount = []

        self.time_list_color = []
        self.time_list_ir = []
        self.Frametime_list_ir = []
        self.Frametime_list_color = []
        self.timecolorCount = []
        self.timeirCount = []
        self.totalTimeinSeconds = 0
        self.distanceM = []
        self.HasStartTime = 0
        self.StartTime = datetime.datetime.now()
        self.EndTime = datetime.datetime.now()


    def getDuplicateValue(self,ini_dict):
        # finding duplicate values
        flipped = {}
        for key, value in ini_dict.items():
            if value not in flipped:
                flipped[value] = 1
            else:
                val = flipped.get(value)
                flipped[value] = val + 1
        key = [fps for fps, count in flipped.items() if count == max(flipped.values())]
        return key[0]


    """
    SortLoadedFiles:
    sorts file in time stamp order
    """
    def SortTime(self, dstimeList):
        UnsortedFiles = {}
        for k,v in dstimeList.items():
            # GET Time from filename
            # Skip first and last second
            FrameTimeStamp = k
            distance =v
            UnsortedFiles[FrameTimeStamp] = distance

        SortedFiles = collections.OrderedDict(sorted(UnsortedFiles.items()))
        return SortedFiles

    """
    LoadFiles:
    Load file from path
    """
    def LoadFiles(self, filepath):
        data_path = os.path.join(filepath, '*g')
        Image_Files = glob.glob(data_path)
        return Image_Files

    """
    SortLoadedFiles:
    sorts file in time stamp order
    """
    def SortLoadedFiles(self, Image_Files):
        UnsortedFiles = {}
        for f1 in Image_Files:
            # GET Time from filename
            # Skip first and last second
            filenamearr = f1.split('\\')
            filename = filenamearr[len(filenamearr)-1]
            filename = filename.replace('.png', '')
            filenameList = filename.split('-')
            hr = filenameList[1]
            min = filenameList[2]
            sec = filenameList[3]
            mili = filenameList[4]
            FrameTimeStamp = self.GetFrameTime(hr, min, sec, mili)

            img = cv2.imread(f1, IMREAD_UNCHANGED)

            UnsortedFiles[FrameTimeStamp] = img

        SortedFiles = collections.OrderedDict(sorted(UnsortedFiles.items()))
        return SortedFiles

    """
    GetFrameTime:
    returns Frame Time Stamp in date time format
    """
    def GetFrameTime(self, hr, min, sec, mili):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        FrameTimeStamp = datetime.datetime(year, month, day, int(hr), int(min), int(sec), int(mili))
        return FrameTimeStamp

    def getColorMeans(self,img,count, FrameTimeStamp):
        # split channels
        b, g, r, a = cv2.split(img)

        # mean data
        BmeanValues = cv2.mean(b)
        GmeanValues = cv2.mean(g)
        RmeanValues = cv2.mean(r)
        greymeanValues = (BmeanValues[0] + GmeanValues[0] + RmeanValues[0]) / 3  # r+g+b/pixel count = grey

        # add to list
        self.blue.append(BmeanValues[0])
        self.green.append(GmeanValues[0])
        self.red.append(RmeanValues[0])
        self.grey.append(greymeanValues)

        # Temp fps wise
        self.Tempblue.append(BmeanValues[0])
        self.Tempgreen.append(GmeanValues[0])
        self.Tempred.append(RmeanValues[0])
        self.Tempgrey.append(greymeanValues)
        self.TemptimecolorCount.append(count)
        self.TempFrametime_list_color.append(FrameTimeStamp)

        # Add Time Stamp with miliseconds
        self.Frametime_list_color.append(FrameTimeStamp)

    """
    ProcessColorImagestoArray:
    Load color region of interests, get average of b,g,r and time.
    skip first and last seconds 
    """
    def ProcessColorImagestoArray(self, filepath,UpSampleData):

        Image_Files = self.LoadFiles(filepath)
        Image_Files = self.SortLoadedFiles(Image_Files)
        LastFileTimeStamp = list(Image_Files.keys())[-1]
        self.EndTime = self.GetFrameTime(LastFileTimeStamp.hour, LastFileTimeStamp.minute, LastFileTimeStamp.second, 0)

        ColorfpswithTime = {}
        prevFrameTimeStamp = None
        fpscountcolor=1
        count=0
        endRecodrded= False
        # Go through each image
        for key, value in Image_Files.items():
            FrameTimeStamp = key
            FrameTimeStampWOMili = datetime.datetime(FrameTimeStamp.year, FrameTimeStamp.month, FrameTimeStamp.day,
                                                     FrameTimeStamp.hour, FrameTimeStamp.minute, FrameTimeStamp.second,
                                                     0)

            # Get start time
            if (self.HasStartTime == 0):
                self.StartTime = FrameTimeStampWOMili
                self.HasStartTime = 1

            if (FrameTimeStampWOMili <= self.StartTime):  # SKIP FIRST SECOND
                continue
                # Do nothing or add steps here if required
            elif (FrameTimeStampWOMili >= self.EndTime):  # SKIP LAST SECOND
                #only do once
                if(not endRecodrded):
                    # Record fps
                    ColorfpswithTime[prevFrameTimeStamp] = fpscountcolor
                    fpscountcolor = 1

                    # totalNewLeng = totalNewLeng + len(self.Tempgrey)
                    self.Tempred = []
                    self.Tempblue = []
                    self.Tempgreen = []
                    self.Tempgrey = []
                    self.TempFrametime_list_color = []
                    self.TemptimecolorCount = []
                    endRecodrded= True

                continue
                # Do nothing or add steps here if required
            else:
                count = count + 1
                # Color fps
                TrimmedTime = datetime.time(FrameTimeStamp.hour, FrameTimeStamp.minute, FrameTimeStamp.second)
                if(TrimmedTime != prevFrameTimeStamp and prevFrameTimeStamp !=None):#fpscountcolor == 30):

                    #Record fps
                    ColorfpswithTime[prevFrameTimeStamp] = fpscountcolor
                    fpscountcolor= 1

                    self.Tempred = []
                    self.Tempblue = []
                    self.Tempgreen = []
                    self.Tempgrey = []
                    self.TempFrametime_list_color = []
                    self.TemptimecolorCount = []

                if(TrimmedTime == prevFrameTimeStamp):
                    fpscountcolor = fpscountcolor + 1

                prevFrameTimeStamp = TrimmedTime

                img = value
                b, g, r, a = cv2.split(img)

                # mean data
                BmeanValues = cv2.mean(b)
                GmeanValues = cv2.mean(g)
                RmeanValues = cv2.mean(r)
                greymeanValues = (BmeanValues[0] + GmeanValues[0] + RmeanValues[0]) / 3  # r+g+b/pixel , grey

                # add to list
                self.blue.append(BmeanValues[0])
                self.green.append(GmeanValues[0])
                self.red.append(RmeanValues[0])
                self.grey.append(greymeanValues)

                # Temp fps wise
                self.Tempblue.append(BmeanValues[0])
                self.Tempgreen.append(GmeanValues[0])
                self.Tempred.append(RmeanValues[0])
                self.Tempgrey.append(greymeanValues)
                self.TemptimecolorCount.append(count)
                self.TempFrametime_list_color.append(FrameTimeStamp)

                # Add Time Stamp with miliseconds
                self.Frametime_list_color.append(FrameTimeStamp)

        self.ColorEstimatedFPS = self.getDuplicateValue(ColorfpswithTime) #Only one time
        self.ColorfpswithTime = ColorfpswithTime

    def getDistance(self,distnacepath):
        fdistancem = open(distnacepath, "r")
        dstimeList = {}
        ##Sort first
        for x in fdistancem:
            fullline = x
            if (fullline.__contains__("Distance datetime")):
                fulllineSplited = fullline.split(" , with distance : ")
                dm = float(fulllineSplited[1])
                dt = fulllineSplited[0].replace("Distance datetime : ", "")  # 27/05/2021 06:39:10
                dttimesplit = dt.split(" ")

                converteddtime = dttimesplit[1].split(":")  # datetime.datetime.strptime(dt, '%y/%m/%d %H:%M:%S')
                hour = int(converteddtime[0])
                min = int(converteddtime[1])
                second = int(converteddtime[2])
                disFrameTime = datetime.time(hour, min, second, 0)
                dstimeList[disFrameTime] = dm

        distanceData = self.SortTime(dstimeList)
        return distanceData


    def getIRMeans(self,countIR,img,FrameTimeStamp,TrimmedTime,distanceData):
        # dimensions = img.shape
        ImgmeanValues = cv2.mean(img)  # single channel  RmeanValue = cv2.mean(r)

        self.Irchannel.append(ImgmeanValues[0])
        # Temp fps wise
        self.TempIrchannel.append(ImgmeanValues[0])
        self.TemptimeirCount.append(countIR)
        self.TempFrametime_list_ir.append(FrameTimeStamp)

        self.Frametime_list_ir.append(FrameTimeStamp)
        self.timeirCount.append(countIR)
        # Distance
        distanceinM = distanceData.get(TrimmedTime)
        self.distanceM.append(float(np.abs(distanceinM)))
        self.TempdistanceM.append(float(np.abs(distanceinM)))

    """
    ProcessIRImagestoArray:
    Load IR region of interests, get average of b,g,r and time and distance
    also make sure color and ir data has same x and y values for processing and plotting
    skip first and last seconds 
    """
    def ProcessIRImagestoArray(self, filepath,LoadDistancePath,UpSampleData):

        Image_Files = self.LoadFiles(filepath)
        Image_Files = self.SortLoadedFiles(Image_Files)
        IRfpswithTime = {}
        fpscountir = 1
        prevFrameTimeStamp=None
        count = 0
        endRecodrded= False
        distanceData = self.getDistance(LoadDistancePath)
        # Go through each image
        for key, value in Image_Files.items():


            FrameTimeStamp = key
            FrameTimeStampWOMili = datetime.datetime(FrameTimeStamp.year, FrameTimeStamp.month, FrameTimeStamp.day,
                                                     FrameTimeStamp.hour, FrameTimeStamp.minute, FrameTimeStamp.second,
                                                     0)

            if (FrameTimeStampWOMili <= self.StartTime):  # SKIP FIRST SECOND
                # Do nothing or add steps here if required
                continue
            elif (FrameTimeStampWOMili >= self.EndTime):  # SKIP LAST SECOND
                # only do once
                if (not endRecodrded):
                    ##FPS record
                    IRfpswithTime[prevFrameTimeStamp] = fpscountir
                    fpscountir = 1

                    self.TempIrchannel = []
                    self.TempFrametime_list_ir = []
                    self.TemptimeirCount = []
                    self.TempdistanceM = []
                    endRecodrded= True
                    #record for previous last second

                # Do nothing or add steps here if required
                continue
            else:
                count = count+1

                TrimmedTime = datetime.time(FrameTimeStamp.hour, FrameTimeStamp.minute, FrameTimeStamp.second)
                # IR fps
                if (TrimmedTime != prevFrameTimeStamp and prevFrameTimeStamp != None):
                    ##FPS record
                    IRfpswithTime[prevFrameTimeStamp] = fpscountir
                    fpscountir = 1

                    self.TempIrchannel = []
                    self.TempFrametime_list_ir = []
                    self.TemptimeirCount = []
                    self.TempdistanceM = []

                if (TrimmedTime == prevFrameTimeStamp):
                    fpscountir = fpscountir + 1

                prevFrameTimeStamp = TrimmedTime

                img = value

                # dimensions = img.shape
                ImgmeanValues = cv2.mean(img)  # single channel

                self.Irchannel.append(ImgmeanValues[0])
                # Temp fps wise
                self.TempIrchannel.append(ImgmeanValues[0])
                self.TempFrametime_list_ir.append(FrameTimeStamp)
                self.Frametime_list_ir.append(FrameTimeStamp)

                # Distance
                distanceinM = distanceData.get(TrimmedTime)
                self.distanceM.append(float(np.abs(distanceinM)))
                self.TempdistanceM.append(float(np.abs(distanceinM)))

        self.IREstimatedFPS = self.getDuplicateValue(IRfpswithTime)
        self.IRfpswithTime = IRfpswithTime
        self.totalTimeinSeconds = len(self.IRfpswithTime)