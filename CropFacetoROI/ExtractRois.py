import os

from Configurations import Configurations
from FileIO import FileIO
from LoadWriteImageData import LoadWriteROI
from LoadWriteImageDataIR import LoadWriteIRROI

"""
ExtractROIdata Class:
Uses LoadWriteImageData and LoadWriteImageDataIR classes to extract ROI's and store them ROI_dataPath.
This class extracts region of interests (ROIS) from face image and creates lips, right and left cheek and forehead images.
"""
class ExtractROIdata:
    #Global Objects
    objFile = FileIO()
    objConfig = Configurations()
    positions = ["Resting1", "Resting2", "AfterExcersize"]

    '''
    CropandLoadData: ONLY RUN First Time for loading and cropping data
    Parameters: Heart rate status (resting1,resting2 or after excersize_), Participant number
    '''
    def CropandLoadData(self,position,ParticipantNumber):

        SaveROIPath, ROI_dataPath = self.objFile.getROIPath(ParticipantNumber,position,self.objConfig.UnCompressed_dataPath)

        #Check if process has been completed previously
        if not (self.objFile.FileExits(SaveROIPath + 'ColorCompleted.txt')):
            print("Process started for, Loading and Cropping all Color files...")
            # Run for cropping Color
            objLoadCrop = LoadWriteROI()
            objLoadCrop.LoadFiles(ROI_dataPath + 'Color',SaveROIPath+ 'Color')
            # objLoadCrop.ONLYLoadandCropFilesMannually(ROI_dataPath + 'Color',SaveROIPath+ 'Color')
            self.objFile.WritedatatoFile(SaveROIPath,'ColorCompleted','Completed')

        if not (self.objFile.FileExits(SaveROIPath + 'IRCompleted.txt')):
            print("Process started for, Loading and Cropping all IR files...")
            # Run for cropping IR
            objLoadIRCrop = LoadWriteIRROI()
            objLoadIRCrop.LoadandCropFiles(ROI_dataPath + 'IR',SaveROIPath+ 'IR')
            # objLoadIRCrop.ONLYLoadandCropFilesMannually(ROI_dataPath + 'IR',SaveROIPath+ 'IR')
            self.objFile.WritedatatoFile(SaveROIPath,'IRCompleted','Completed')

    '''
    InitiateProcess: Either initiate process (crop and load) for one participant or for all data
    Parameters: Type is either Single or All, Heart rate status (resting1,resting2 or after excersize_), Participant number
    Example: CropandLoadData("Resting1", "PIS-6729")
             CropandLoadData("Resting1", "PIS-3186")
             CropandLoadData("Resting2", "PIS-3186")
             CropandLoadData("AfterExcersize", "PIS-3186")
    '''
    def InitiateProcess(self,type, position,ParticipantNumber):
        #Process as per type
        if(type == 'Single'):
            #set group type
            self.objConfig.setDiskPath()
            self.CropandLoadData(position, ParticipantNumber)
        elif(type == 'All'):
            # for skinPigementation in self.objConfig.Skin_Group_Types:
            self.objConfig.setDiskPath()
            #Get all participant numbers (each folders data)
            folder = self.objConfig.UnCompressed_dataPath
            subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

            #for each participant
            for folder in subfolders:
                foldername = str(folder)
                foldernameparams = foldername.split("\\")
                ParticipantNumber = foldernameparams[len(foldernameparams)-1]

                # for each position
                for pos in self.positions:
                    print("Processing for : " + ParticipantNumber + " for " + pos)
                    self.CropandLoadData(pos, ParticipantNumber)
        else:
            print('PLEASE ENTER CORRECT TYPE Croping data type ("Single", "All")')

objExtractData = ExtractROIdata()
objExtractData.InitiateProcess('All', '', '')
# objExtractData.InitiateProcess('Single','Resting1','PIS-00')
# objExtractData.InitiateProcess('Single','Resting2','PIS-00')
# objExtractData.InitiateProcess('Single','AfterExcersize','PIS-00')