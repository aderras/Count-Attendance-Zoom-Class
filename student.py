# Student class 

from datetime import datetime
import pandas as pd

class Student:

	def __init__(self, first, last):

		self.first_name = first
		self.last_name = last

		self.participation_grade = {}
		self.attendance_grade_sequential = {}
		self.attendance_grade_cumulative = {}

		self.attendance_total = {}
	
	def computeGrades(self, logList, computeParticipation = False):

		
		for log in logList:

			# Check the type of log file that this is
			if log.file_type == 1:

				self.computeAttendance(log)

			elif log.file_type == 2 and computeParticipation:

				self.computeParticipation(log)

		# Total the sequential and cumulative participation 
		# grades. Result is dictionary with date1: total_grade1...
		for date in self.attendance_grade_sequential:

			tot = self.attendance_grade_sequential[date][0] + self.attendance_grade_cumulative[date][0]

			self.attendance_total[ date ] = [tot]


	def computeAttendance(self, attLog):

		fullName = self.first_name + " " + self.last_name

		dfAtt = attLog.data

		# Store all the instances in an array
		studentAppearances = dfAtt[ dfAtt['Meeting ID'].str.contains( fullName.lower(), case=False) ].values

		if len(studentAppearances) > 0 :

			# Convert the data to dateTime objects so that we can calulate time difference
			# Sum all the time differences to get total time stayed. Probably can vectorize this.
			totalTime = 0
			for i in range(len(studentAppearances)):

				# Zoom contains a column that lists duration, but for some reason those values 
				# become Nan when imported to python with pandas. A work around is to calculate 
				# the difference based on Join/Leave times. This is probably inefficient.
				enterTime = pd.to_datetime( studentAppearances[i][1] )
				exitTime = pd.to_datetime( studentAppearances[i][2] )

				totalTime = totalTime + pd.Timedelta( exitTime - enterTime ).seconds / 60.0

			# If they stayed for the specified time, give them credit
			if totalTime > attLog.duration:
				self.attendance_grade_cumulative[ attLog.date ] = [1]
			else: 
				self.attendance_grade_cumulative[ attLog.date ] = [0]

			# First row, second column contains the  time that the student entered the session
			enterTime = pd.to_datetime( studentAppearances[0][1] ).time()

			# If they entered on time, give them credit
			if enterTime < attLog.start_time :
				self.attendance_grade_sequential[ attLog.date ] = [1]
			else:
				self.attendance_grade_sequential[ attLog.date ] = [0]

			# Drop the name from the attendance log when you
			# have found the student. This is done so that left over names
			# will be logged. 
			attInstances = dfAtt.loc[ dfAtt['Meeting ID'].str.contains(fullName, case=False) ]
			attLog.data = dfAtt.drop( attInstances.index )

		else:

			self.attendance_grade_sequential[ attLog.date ] = [0]
			self.attendance_grade_cumulative[ attLog.date ] = [0]

	# Compute participation grade by counting how many times a student participated in the 
	# chat. Could be more sophisticated. E.g. if students ask or answer a question with the
	# preface A: or Q:, that could count differently. 
	def computeParticipation(self, chatLog):

		fullName = self.first_name + " " + self.last_name

		numMessages = 0

		chatData = chatLog.raw_data
		chatOccurances = chatData[ chatData.columns[1] ].str.contains(fullName, case=False)
		numMessages = sum( chatOccurances )

		self.participation_grade[ chatLog.date ] = [numMessages]