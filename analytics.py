from collections import *

class AttendanceAnalytics:
	def calculateDailyWorkingHours(data,working_hours):
		if data[0].day == data[1].day:
			difference =  data[1].hour - data[0].hour + (data[1].minute - data[0].minute)/100
			key = data[0].date()
			if working_hours.get(key):
				working_hours[key] += difference
			else:
				working_hours[key] = difference
		elif data[0].day != data[1].day:
			key = data[0].date()
			key_difference = ((24.00*60.00)-(float(data[0].hour)*60+float(data[0].minute)))/60.00
			if working_hours.get(key):
				working_hours[key] += key_difference
			else:
				working_hours[key] = key_difference

			next_key = data[1].date()
			key_difference = (float(data[1].hour)*60+float(data[1].minute))/60.00
			if working_hours.get(next_key):
				working_hours[next_key] += key_difference
			else:
				working_hours[next_key] = key_difference




class ConcurrentLockoutHandler:

	def __init__(self):
		self.lockout_eligible_events = set(['login','logout','onboard'])
		self.event_queue = []
		self.locking_event = None

	def setLockingEvent(self,event):
		self.locking_event = event


class Event:
	def __init__(self,event_name = None,params = None):
		self.event_name = event_name
		self.params = params
