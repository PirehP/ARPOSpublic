class ProcessedParticipantsData:
    WindowRegionList = {} # ROI Window Result list

    def __init__(self,minFPSIRvalue, maxFPSIRvalue, minFPSColorvalue, maxFPSColorvalue,  FPSNotes,
                 LengthofAllFramesColor,LengthofAllFramesIR,  totalTimeinSeconds,TimeinSeconds,  timeinSeconds,
                 TotalWindows, HrAvgList, SPOAvgList , Algorithm_type, FFT_type,  Filter_type ,  Result_type , Preprocess_type ,
                 isSmoothen):
        self.minFPSIRvalue = minFPSIRvalue
        self.maxFPSIRvalue =maxFPSIRvalue
        self.minFPSColorvalue = minFPSColorvalue
        self.maxFPSColorvalue = maxFPSColorvalue
        self.FPSNotes =FPSNotes
        self.LengthofAllFramesColor =LengthofAllFramesColor
        self.LengthofAllFramesIR = LengthofAllFramesIR

        self.totalTimeinSeconds = totalTimeinSeconds
        self.TimeinSeconds = TimeinSeconds
        self.timeinSeconds = timeinSeconds
        self.TotalWindows =TotalWindows

        self.HrAvgList = HrAvgList
        self.SPOAvgList = SPOAvgList

        self.Algorithm_type = Algorithm_type
        self.FFT_type = FFT_type
        self.Filter_type =Filter_type
        self.Result_type =Result_type
        self.Preprocess_type =Preprocess_type
        self.isSmoothen = isSmoothen

    minFPSIRvalue = 0
    maxFPSIRvalue = 0
    minFPSColorvalue = 0
    maxFPSColorvalue = 0
    FPSNotes = ''
    LengthofAllFramesColor = 0
    LengthofAllFramesIR = 0

    totalTimeinSeconds =0
    TimeinSeconds = 0
    timeinSeconds = 0
    TotalWindows = 0

    # Split ground truth data
    HrAvgList = []
    SPOAvgList = []

    Algorithm_type=''
    FFT_type=''
    Filter_type=0
    Result_type=0
    Preprocess_type=0
    isSmoothen =None
