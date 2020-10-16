# Count-Attendance-Zoom-Class
Take attendance for online Zoom class

Author: Amel Derras-Chouk

Take attendance for online Zoom classes, and optionally count student participation. (See participation section for special instructions.) Written in Python 3.7.4

Required libraries:
  - Pandas to read and build .csv or .xlsx files

# Usage #

To use this script, need:
  1. CSV file containing student roster. Sample roster was [downloaded from Blackboard](https://help.blackboard.com/Learn/Instructor/Grade/Grading_Tasks/Work_Offline_With_Grade_Data#download-grades-from-the-grade-center_OTP-1) course. Code assumes that roster contains the columns 'First Name' and 'Last Name.'
  2. Usage information from each Zoom class. After class, [download usage data](https://support.zoom.us/hc/en-us/articles/201363213-Getting-started-with-reports). 
  
Compute attendance by running 'python compute_grades.py' in the project directory. User will be prompted to enter
  - Location of log files (default: project-dir/log-files/)
  - Roster filename (default: roster.csv)
  - Time at which to take attendance (Required input. Enter a later time to include a grace period.)
  - Duration of class, or minimum time spent in class to be marked present (default: 0)
  - Compute participation y/n? (default: n)
  - Output filename (default: computed_grades.xlsx)

Output file is saved in project directory. 

**Note:** Nicknames/partial names/mispelled names are not counted. These are output to a different sheet in the output file titled 'Error Log.' This sheet contains all the uncounted names separated by date. 

# Participation #

This code also counts student participation by totaling the number of contributions to the Zoom chat. To use, [download chat files](https://support.zoom.us/hc/en-us/articles/115004792763-Saving-in-meeting-chat) to the same location as the usage report files. 

The chat file does not contain the date of the class, so the date must be included in the filename in the format MMDDYYYY, separated by an underscore. E.g. 'any-name_09152020.txt.'

## How to download attendance reports from Zoom ##

	1. Select reports from Zoom home page. 
	[!step1](img/step1edit.png)
	2. Select usage
	[!step2](img/step2edit.png)
	2. Select class for which you'd like to report
	[!step3](img/step3edit.png)
	2. Check "Export with meeting data" before clicking export
	[!step4](img/step4edit.png)



