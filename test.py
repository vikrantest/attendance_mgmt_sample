from main import *
import datetime

class AttendanceUnitTest:

	def __init__(self):
		self.companyData = AttendanceMain()
		self.input_data = [('Onboard',('manager','6_HOURS_A_DAY','Ankit','2018-04-13')),('Onboard',('developer','40_HOURS_A_WEEK','Sumit','2018-05-10')),('Login',('Ankit','VPN','2018-04-15 13:00:00')),
						('Logout',('Ankit','VPN','2018-04-15 22:00:00')),('Login',('Ankit','VPN','2018-04-16 09:00:00')),('Logout',('Ankit','VPN','2018-04-16 16:00:00')),('Logout',('Ankit','VPN','2018-04-15 13:00:00')),
						('GetAverageWorkingHourOfAllEmployeesOnADay',('2018-04-15',)),('GetAverageWorkingHourOfAllEmployeesForLastnDays',('60',)),('getAttendance',('Ankit','60')),('end logout',('1'))]


	def inputs(self):
		for data in self.input_data:
			if len(data) == 1:
				param = []
			else:
				param = data[1]
			response = self.companyData.inputMain(data[0],param)
			print(response)




AttendanceUnitTest().inputs()