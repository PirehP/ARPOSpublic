import numpy as np


class GlobalData:
    # Image r,g,b,ir,grey data arrays
    red = []
    blue = []
    green = []
    grey = []
    Irchannel = []

    # Time stamp arrays for rgb grey and ir channels
    time_list_color = []
    time_list_ir = []
    Frametime_list_ir = []
    Frametime_list_color = []
    timecolorCount = []
    timeirCount = []
    totalTimeinSeconds =0
    # Depth
    distanceM = []

    #fps info
    ColorfpswithTime=[]
    IRfpswithTime=[]

    ColorEstimatedFPS=0
    IREstimatedFPS=0

    def __init__(self, timecolor, timecolorcount,timeir,timeircount,Frametime_list_ir,Frametime_list_color,
                 red,green,blue,grey,ir,distanceM,totalTimeinSeconds,ColorEstimatedFPS, IREstimatedFPS,ColorfpswithTime=None, IRfpswithTime=None):
        self.time_list_color = timecolor
        self.timecolorCount = timecolorcount
        self.time_list_ir = timeir
        self.timeirCount = timeircount
        self.red = red
        self.green = green
        self.blue = blue
        self.grey = grey
        self.Irchannel = ir
        self.distanceM = distanceM
        self.ColorfpswithTime=ColorfpswithTime
        self.IRfpswithTime=IRfpswithTime
        self.Frametime_list_ir = Frametime_list_ir
        self.Frametime_list_color = Frametime_list_color
        self.totalTimeinSeconds = totalTimeinSeconds
        self.ColorEstimatedFPS=ColorEstimatedFPS
        self.IREstimatedFPS=IREstimatedFPS

    def getLengthColor(self):
        return len(self.grey)

    def getLengthIR(self):
        return len(self.Irchannel)


'''
WindowProcessedData:
'''
class WindowProcessedData:
    HrGroundTruthList = None
    SPOGroundTruthList = None
    ColorLengthofAllFrames= None
    IRLengthofAllFrames= None
    TimeinSeconds= None
    ROIStore= None