from datetime import datetime
import pandas as pd
from os import path

# Log class contains information from designated csv file
class LogFile:

    def __init__(self, name, start='10:00 AM', dur = '70'):

        self.file_name = name
        self.raw_data = None
        self.data = None
        self.date = None
        self.file_type = None # 0 = roster, 1 = attendance, 2 = chat
        self.start_time = None
        self.duration = None

        # Check that file exists
        if path.exists(name):

            # Import the attendance data as a csv and the chat data as 
            # a table. Distinguish by file extension
            if '.txt' in name:
                self.raw_data = pd.read_table(name, encoding='latin1')
                self.file_type = 2

            elif '.csv' in name:
                self.raw_data = pd.read_csv(name) 

            else: 
                print('Error: '+ name+' is not of type .csv or .txt. '+
                    'Proceeding without this file.')
                return( None )

        else:
            print( "Error:" + name + " does not exist." )
            exit()

        self.formatData(start, dur)


    def formatData(self, start, dur):

        # If this log file is chat data, then get the date from the file name
        if self.file_type == 2:

            # Get the date from the filename. Zoom does not put the date into
            # the chat logs. 
            dateStr = (self.file_name.split("_"))[1].split('.')[0]
            dateFormatted = datetime.strptime(dateStr, "%m%d%Y").date()

            self.date = dateFormatted

        # Otherwise, figure out what kind of data file this object is. 
        # options are roster or attendance 
        else:
        
            try:

                # Search for these column names
                df = self.raw_data[['Meeting ID', 'Start Time', 'End Time', 'Duration (Minutes)']]

                # If the file contains these columns, then this is an attendance file
                # Check that this is the right type of Zoom file. (There are sequential
                # and cumulative data. )
                i = df[ (df['Meeting ID'] == 'Name (Original Name)')].index

                # print(df.iloc[i.values].values)

                if 'Join Time' in df.iloc[i.values].values:
                
                    self.file_type = 1

                    # The third row in the Zoom files is dropped. (Becuase it contains 
                    # non-numeric values it causes errors when processing later.)
                    self.data = df.drop(i)

                    # Set the date
                    self.date = pd.to_datetime(df.iloc[0]['Start Time']).date()

                    # Set the class start time and duration
                    self.start_time = start 
                    self.duration = int(dur)


            except KeyError:

                # If the file doesn't contain this key, then this is a roster file
                self.file_type = 0
