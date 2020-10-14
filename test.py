from log import LogFile
from student import Student
import glob
import pandas as pd

# Create a log object from data file called roster.csv.
# File must contain 'First Name' and 'Last Name' columns. (Blackboard
# grade center file was used to demonstrate.)
roster = LogFile('log-files/roster.csv')

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

# Import all the log files. These 3 different types of log file come from
# Zoom. Note that chat files must contain date in their name in the format
# ddmmyyyy (e.g. Jan 1, 2020 would 01012020)
filenames = glob.glob('log-files/*')
logFiles = []

for file in filenames:

    logObject = LogFile( file , '10:00 AM', '70')
    logFiles.append( logObject )

c = 89
print(studentList[c].first_name)
studentList[c].computeGrades( logFiles )
print(studentList[c].attendance_total)

# # Use the log files to compute each student's grade
# for student in studentList:

#   student.computeGrades( logFiles )
