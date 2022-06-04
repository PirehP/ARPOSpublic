import pandas as pd
import pyodbc


class SQLConfig:
    #dbconnection
    conn = None
    cursor = None
    # Constructor
    def __init__(self):
        # Defining the connection string
        self.conn = pyodbc.connect('''DRIVER={SQL Server}; Server=ADD SERVER NAME HERE; 
                                UID=USERNAME; PWD=PASSWORD; DataBase=DBNAME''')
        self.cursor = self.conn.cursor()

    def GetBestAmongAll(self,HeartRateStatus,UpSampled,AttemptType, TechniqueId):
        ##Parameters
        FullQuery = "exec GetBestAmongAll " + UpSampled + ",'" + HeartRateStatus + "'," + AttemptType + "," + TechniqueId
        dataTable = pd.read_sql_query(FullQuery, self.conn)
        dataTable.head()
        return dataTable

    def getTechniqueId(self,AlgorithmType,PreProcess,FFT,Filter,Result,Smoothen):
        TechniqueIdQuery = "select Id as TechniqueId from Techniques where AlgorithmType = '"+ AlgorithmType + "' and PreProcess="+\
                      PreProcess + " and " + "FFT='"+FFT+"' and Filter="+Filter+" and Result="+Result+" and Smoothen='"+Smoothen+"'"
        self.cursor.execute(TechniqueIdQuery)
        TechniqueId = self.cursor.fetchone()[0]
        return TechniqueId

    def ExistsInDb(self,AlgorithmType,PreProcess,FFT,Filter,Result,Smoothen,HeartRateStatus, ParticipantId):
        TechniqueId = self.getTechniqueId(AlgorithmType,str(PreProcess),FFT,str(Filter),str(Result),str(Smoothen))
        queryExists = "select count(ParticipantResultId) as CountRows from ParticipantsResultsEntireSignal " \
                      "where ParticipantId= '"  + ParticipantId + "' and HeartRateStatus = '"  + HeartRateStatus + "' and TechniqueId="+str(TechniqueId)

        self.cursor.execute(queryExists)
        CountValue = self.cursor.fetchone()[0]
        if(CountValue>0):
            return True
        else:
            return False

    def SaveRowParticipantsResultsEntireSignal(self, objParticipantsResultEntireSignalDataRow):
        try:

            self.cursor.execute("exec AddParticipantsResultEntireSignal '"+ objParticipantsResultEntireSignalDataRow.ParticipantId+ "', '" +
                                objParticipantsResultEntireSignalDataRow.HeartRateStatus + "', " +
                                objParticipantsResultEntireSignalDataRow.bestHeartRateSnr+ ", " +
                                objParticipantsResultEntireSignalDataRow.bestBPM + ",'"+
                                objParticipantsResultEntireSignalDataRow.channelType + "','"+
                                objParticipantsResultEntireSignalDataRow.regionType + "'," +
                                objParticipantsResultEntireSignalDataRow.FrequencySamplingError + ","+
                                objParticipantsResultEntireSignalDataRow.oxygenSaturationValueError + ","+
                                objParticipantsResultEntireSignalDataRow.heartRateError + "," +
                                objParticipantsResultEntireSignalDataRow.bestSPO + "," +
                                objParticipantsResultEntireSignalDataRow.HeartRateValue + "," +
                                objParticipantsResultEntireSignalDataRow.SPOValue + "," +
                                objParticipantsResultEntireSignalDataRow.differenceHR + "," +
                                objParticipantsResultEntireSignalDataRow.differenceSPO + ",'" +
                                objParticipantsResultEntireSignalDataRow.TotalWindowCalculationTimeTaken + "','" +
                                objParticipantsResultEntireSignalDataRow.PreProcessTimeTaken + "','"+
                                objParticipantsResultEntireSignalDataRow.AlgorithmTimeTaken + "','"+
                                objParticipantsResultEntireSignalDataRow.FFTTimeTaken + "','"+
                                objParticipantsResultEntireSignalDataRow.SmoothTimeTaken + "','"+
                                objParticipantsResultEntireSignalDataRow.FilterTimeTaken + "','"+
                                objParticipantsResultEntireSignalDataRow.ComputingHRSNRTimeTaken + "','"+
                                objParticipantsResultEntireSignalDataRow.ComputingSPOTimeTaken + "','"+
                                # objParticipantsResultEntireSignalDataRow.TechniqueId + ","+
                                objParticipantsResultEntireSignalDataRow.Algorithm_type  + "',"+
                                objParticipantsResultEntireSignalDataRow.Preprocess_type   + ",'"+
                                objParticipantsResultEntireSignalDataRow.FFT_type   + "',"+
                                objParticipantsResultEntireSignalDataRow.Filter_type   + ","+
                                objParticipantsResultEntireSignalDataRow.Result_type   + ",'"+
                                objParticipantsResultEntireSignalDataRow.isSmoothen    + "',"+
                                objParticipantsResultEntireSignalDataRow.UpSampled + ","+
                                objParticipantsResultEntireSignalDataRow.ColorFPS + ","+
                                objParticipantsResultEntireSignalDataRow.IRFPS + ",'"+
                                objParticipantsResultEntireSignalDataRow.SelectedColorFPSMethod + "','"+
                                objParticipantsResultEntireSignalDataRow.SelectedIRFPSMethod + "', " +
                                objParticipantsResultEntireSignalDataRow.GroundTruthHeartRate + ","+
                                objParticipantsResultEntireSignalDataRow.GroundTruthSPO + ","+
                                objParticipantsResultEntireSignalDataRow.AttemptType + ",'"+
                                objParticipantsResultEntireSignalDataRow.FPSNotes + "' "
                                )

            self.conn.commit()
        except Exception:
            print('ERROR adding ' + objParticipantsResultEntireSignalDataRow.Algorithm_type + ', preprocess: ' +objParticipantsResultEntireSignalDataRow.Preprocess_type
                  + ', FFT: ' + objParticipantsResultEntireSignalDataRow.FFT_type
                  + ', Filter: ' + objParticipantsResultEntireSignalDataRow.Filter_type  + ', Result: ' + objParticipantsResultEntireSignalDataRow.Result_type
                  + ', Smoothen' + objParticipantsResultEntireSignalDataRow.SmoothTimeTaken
                  )
