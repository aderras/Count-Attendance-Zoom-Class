from log import LogFile
from student import Student
import glob
import pandas as pd
from datetime import datetime

# add comments, amel.

def getUserInput(prompt, required=False, defaultInput=''):

    res = input(prompt)

    if res == '' and required:
        print( 'Your answer is required' )
        return getUserInput( prompt, required, defaultInput )
    elif res == '' and not required:
        print( 'Setting default value: ' + defaultInput)
        return defaultInput
    else:
        return res

def getStartTime():

    startTime = getUserInput('\nEnter the time attendance is taken in the format HH:MM AM (or PM): ', True)

    try: 

        return datetime.strptime(startTime, "%I:%M %p").time()


    except ValueError:

        print('Incorrect time format. Try again. ')
        
        return getStartTime()



# First, ask for a few inputs
logPath = getUserInput('\nEnter directory where log files are stored in the fomat "path-to-files/". Press enter to use default directory, "log-files/"', False, 'log-files/' )

# Check that the directory is formatted correctly
if logPath[-1] != '/':
    logPath = logPath + '/'


rosterName = getUserInput('\nEnter file name of class roster, located in path previously specified. Press enter to use default name, "roster.csv". ' , False, 'roster.csv')

startTime = getStartTime()


duration = getUserInput('\nEnter the minimum duration considered present (minutes): ', False, '0')

computeParticipation = 'y' == getUserInput('\nCompute participation using chat files? y/n ', False, 'n')

outputName = getUserInput('\nEnter output filename: ', False, 'computed_grades.xlsx')

if '.xlsx' not in outputName:
    outputName = outputName + '.xlsx'


###########################################################################
########################################## Grade calculations start here ##

# Create a log object from data file called roster.csv.
# File must contain 'First Name' and 'Last Name' columns. (Blackboard
# grade center file was used to demonstrate.)
roster = LogFile(logPath + rosterName)

# Get all names
firstNames = roster.raw_data['First Name'].array
lastNames = roster.raw_data['Last Name'].array

# Make a student object for every row in the roster. Store students
# in studentList
studentList = []

# For every row in roster, create a student with the first and last 
# name of that row. 
for first, last in zip(firstNames, lastNames):

    studentList.append( Student( first, last ) )

# Import all the log files. These 2 different types of log file come from
# Zoom. Note that chat files must contain date in their name in the format
# ddmmyyyy (e.g. Jan 1, 2020 would 01012020)
filenames = glob.glob(logPath+ '*')
logFiles = []

for file in filenames:

    logObject = LogFile( file, startTime, duration )
    logFiles.append( logObject )

# Use the log files to compute each student's grade
for student in studentList:

  student.computeGrades( logFiles, computeParticipation)


############################################################################
############################################# Export process starts here ###

# Get all the dates of the log files. This will label the columns of the 
# final excel sheet. Sort dates in the last step.
dateList = []
for logFile in logFiles:
  if logFile.date != None and logFile.date not in dateList:
      dateList.append( logFile.date )
dateList = sorted( dateList )

# Define columns of the export file. First column is student name, and the
# rest of the columns are the dates.
columns = {}
columns['Name'] = ''
for date in dateList:
    columns[ date ] = []

# Create an attendance dataframe and a participation dataframe
attDf = pd.DataFrame( columns )
parDf = pd.DataFrame( columns )

for student in studentList:

  # Create a row containing student name. The row contains all grades
  # for dates in the colums specified
  newRow = {'Name': student.first_name + ' '+ student.last_name}
  newRow.update( student.attendance_total  )

  # Add a new row to the dataframe 
  attDf = pd.concat( [ attDf, pd.DataFrame(newRow) ] )


  # Same steps for participation grade, if calculated
  if computeParticipation:
      newRow = {'Name': student.first_name + ' '+ student.last_name}
      newRow.update( student.participation_grade )
      parDf = pd.concat( [ parDf, pd.DataFrame(newRow)  ] )

attDf = attDf[ columns ]

if computeParticipation:
    parDf = parDf[ columns ]
  
# Final file contains
#   1. Sheet 1 has all students and their attendance grades for all dates
#   2. Sheet 2 has all students and their participation grades for all dates
#   3  Sheet 3 is an error log. Contains all names that were not catagorized.
#      This typically happens when names are mispelled. 
writer = pd.ExcelWriter(outputName, engine = 'xlsxwriter')
attDf.to_excel(writer, sheet_name = 'Attendance')

if computeParticipation:
    parDf.to_excel(writer, sheet_name = 'Participation')

# Create a dataframe of all the names that were not counted. 
errDf = pd.DataFrame()
for log in logFiles:

    if log.file_type == 1 or log.file_type == 2:

        # Add a row with the date
        errDf = pd.concat( [ pd.DataFrame( {'',log.date.strftime('%m-%d-%Y')} ) , errDf] )

        # Add row of whatever was in log file
        errDf = pd.concat( [log.data, errDf] )

        # Add empty row
        errDf.append( pd.Series(' '), ignore_index=True )

errDf.to_excel(writer, sheet_name = 'Error Log')

writer.save()
writer.close()

