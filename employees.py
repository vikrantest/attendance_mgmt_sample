import sys
import datetime
from attendence import *
from analytics import *


class Company:
	def __init__(self,name):
		self.name = name
		self.employees_count = 0
		self.employees = {}
		self.employees_name = set()


	def getAverageWorkingHour(self,day,num_days=False):
		total_hours = 0.00
		if not num_days:
			day = datetime.datetime.strptime(day,'%Y-%m-%d').date()
			for employee in self.employees_name:
				if self.employees[employee].working_hours.get(day):
					total_hours+=self.employees[employee].working_hours[day] 

			return float(total_hours)/float(self.employees_count)
		else:
			start , n = day,0
			date_range = set([start])
			while n <= num_days:
				new = start-datetime.timedelta(days=1)
				date_range.add(new)
				start = new
				n+=1
			for dates in date_range:
				for employee in self.employees_name:
					if self.employees[employee].working_hours.get(dates):
						total_hours+=self.employees[employee].working_hours[dates]

			return float(total_hours)/float(self.employees_count)








class Employees:
	def __init__(self,department = None,attendance_strategy = None,name = None,doj = None,company = None):
		self.department = department.lower()
		self.name = name.lower()
		self.attendance_strategy = attendance_strategy
		try:
			self.doj = datetime.datetime.strptime(doj,'%Y-%m-%d')
		except:
			return "Error - invalid date format , please enter in YYYY-MM-DD format"
		self.working_hours = {}
		self.islogin = False
		self.attendence_events = {'login':[],'logout':[]}
		self.last_event = self.doj
		self.company_name = None


	def setLoginLogout(self,values,event):
		try:
			event_date = datetime.datetime.strptime(values[2],'%Y-%m-%d %H:%M:%S')
		except:
			return "Error - invalid date , please enter in 'YYYY-MM-DD HH:MM:SS"
		if event_date < self.last_event:
			return "Error - Wrong date for event"

		if event.lower() == 'login':
			login_event = Login(name = self.name,login_mode = values[1],login_time = event_date)
			self.last_event = event_date
			self.islogin = True
			self.attendence_events['login'].append(login_event)
			return '%s loggedin successfully' % self.name

		elif event.lower() == 'logout':
			logout_event = Logout(name = self.name,logout_mode = values[1],logout_time = event_date)
			self.attendence_events['logout'].append(logout_event)
			self.islogin = False
			AttendanceAnalytics.calculateDailyWorkingHours((self.last_event ,event_date),self.working_hours)
			self.last_event = event_date
			return '%s loggedout successfully' % self.name

	def getattendance(self,num_days):
		num_days = int(num_days)
		start = datetime.datetime.now().date()
		n = 0
		date_range = [start]
		while n <= int(num_days):
			new = start-datetime.timedelta(days=1)
			date_range.append(new)
			start = new
			n+=1
		days_present = 0

		if self.attendance_strategy == '6_HOURS_A_DAY':
			for dates in date_range:
				if self.working_hours.get(dates):
					if self.working_hours.get(dates) >= 6:
						days_present+=1

			return '%d days present in last %d days ' % (days_present,num_days)
		else:
			for m in range(num_days,0,-7):
				hours = 0
				for n in range(m,m-7):

					dates = date_range[n]
					if self.working_hours.get(date_range[n]):
						hours+=self.working_hours.get(date_range[n])

				if hours>=40:
					days_present+=1
			return '%d days present in last %d days ' % (days_present,num_days)













