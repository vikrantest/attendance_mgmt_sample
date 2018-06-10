from employees import *
from analytics import *
import datetime

class AttendanceMain:

	def __init__(self):
		self.company = Company('Vtest Pvt Ltd.')
		self.input_ops_mapping = {'onboard':self.onboard,'login':self.loginLogout,'logout':self.loginLogout,
							'getaverageworkinghourofallemployeesonaday':self.getAverageWorkingHourOfAllEmployeesOndays,'getaverageworkinghourofallemployeesforlastndays':self.getAverageWorkingHourOfAllEmployeesOndays,
							'getattendance':self.getAttendance}
		self.concurrency_control = ConcurrentLockoutHandler()



	def inputMain(self,input_ops,values):
		if input_ops.lower() == 'end logout':
			self.handleConcurrency(input_ops)
		elif self.checkConcurrency(input_ops,values):
			response = self.input_ops_mapping[input_ops.lower()](input_ops,values)
			return response
		else:
			return "Will show some cache value with waiting or refresh message."



	def onboard(self,input_ops,values):
		if str(values[2]).lower() in self.company.employees_name:
			response = "Error - Employee with this name already exists"
		else:
			employee = Employees(department = values[0],attendance_strategy = values[1],name = values[2],doj = values[3])
			self.company.employees_count+=1
			self.company.employees[employee.name] = employee
			self.company.employees_name.add(employee.name)
			employee.company_name = self.company.name
			response = '%s onboarded' % employee.name
		self.handleConcurrency(input_ops)
		return response

	def loginLogout(self,input_ops,values):
		event = input_ops
		if self.company.employees.get(values[0].lower()):
			employee = self.company.employees[values[0].lower()]
			if event.lower() == 'login' and employee.islogin == True:
				response = 'Error - %s already logged in ' % (employee.name)

			elif event.lower() == 'logout' and employee.islogin == False:
				# response = 'Error - %s already loggedout in ' % (employee.name)
				return 'Error - %s already loggedout in ' % (employee.name)
			else:
				response = employee.setLoginLogout(values,event)

		else:
			response = 'Error - This employee Doesnot exists'

		self.handleConcurrency(input_ops)

		return response

	def getAverageWorkingHourOfAllEmployeesOndays(self,input_ops,values):
		if '-' not in values[0]:
			num_days = int(values[0])
			hours = self.company.getAverageWorkingHour(datetime.datetime.now().date(),num_days)
			return 'Average working hours of all employess on in last %d day is %s ' % (num_days,str(hours))
		else:
			if len(values)<1:
				date = datetime.datetime.now().strftime('%Y-%m-%d')
			else:
				date = values[0]
			hours =  self.company.getAverageWorkingHour(date)
			return 'Average working hours of all employess on that day is %s ' % str(hours)

	def getAttendance(self,input_ops,values):
		employee = self.company.employees[values[0].lower()]
		return employee.getattendance(values[1])


	def checkConcurrency(self,input_ops,values):
		if input_ops.lower() in self.concurrency_control.lockout_eligible_events:
			self.concurrency_control.setLockingEvent(input_ops)
			return True
		else:
			if self.concurrency_control.locking_event:
				event = Event(event_name = input_ops,params=values)
				self.concurrency_control.event_queue.append(event)
				return False
			else:
				return True


	def handleConcurrency(self,input_ops):
		self.concurrency_control.locking_event = None
		if len(self.concurrency_control.event_queue) > 0:
			while len(self.concurrency_control.event_queue)>0:
				event = self.concurrency_control.event_queue.pop()
				print(self.input_ops_mapping[event.event_name.lower()](event.event_name.lower(),event.params))









