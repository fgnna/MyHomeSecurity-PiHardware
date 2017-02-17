import RPi.GPIO as GPIO
import time
import datetime
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)


fileObj = file("./log",'w+')

#0.034 0.011 0.034 0.011
#0=00  1=11 f=01  null=10

M335_CODE_0 = "0"
M335_CODE_1 = "1"
M335_CODE_f = "f"
M335_CODE_null = "N" 

def checkHighLow():
	d1 = GPIO.input(23)
	d2 = GPIO.input(24)
	if d1&d2:
		return M335_CODE_1
	elif d1|d2 is not True:
		return M335_CODE_0
	elif d1 is True and d2 is not True:
		return M335_CODE_null
	else:
		return M335_CODE_f
	
def loadCode():
	#for i in range(12):
	while True:
		if M335_CODE_1 == checkHighLow():
			break
	while True:
		temp_code = checkHighLow()
		if M335_CODE_1 == temp_code:
			break
		if M335_CODE_1 == temp_code and M335_CODE_0 == temp_code:
			print "error code" 
			return
	count = 0
	while count < 12:
		temp_code = get4in1Code()
		if "" is temp_code:
			return
		print get4in1Code(),
		count +=1
	
def get4in1Code():
	count = 0
	data_code_now = M335_CODE_1
	data_time_now = datetime.datetime.now()
	print data_code_now,

	time_list = []

	while count < 4:		
		data_code_last = checkHighLow()
		if M335_CODE_1 == data_code_last and M335_CODE_0 == data_code_last:
			print "error code" 
			return
		data_time_last = datetime.datetime.now()
		if data_code_now != data_code_last:
			temp_us = int((data_time_last - data_time_now).microseconds)
			time_list.append(temp_us)
			data_code_now = data_code_last
			data_time_now = data_time_last
			count += 1 
	return checkTimeLsit(time_list)

def checkTimeLsit(timeList):
	one_code = ""
	for i in timeList:
		if i >= 100 and i < 500:
			one_code += "0"
		elif i >= 700 and i < 1150:
			one_code += "1"
		else:
			print "error Time["+str(i)+"]" 
			return ""
	
	if "1010" == one_code:
		return M335_CODE_1
	elif "0101" == one_code:
		return M335_CODE_0
	elif "0110" == one_code:
		return M335_CODE_f
	else:
		return M335_CODE_null

curret_code = M335_CODE_0
while True:
	if checkHighLow() == M335_CODE_0:
		print "break"
		break
date_now = datetime.datetime.now()	
while True:
	end_code = checkHighLow() 
	if end_code != curret_code:
		date_end = datetime.datetime.now()
		#fileObj.write(end_code)
		#fileObj.write( ":")
		t1 = int((date_end - date_now).microseconds)
		if t1 >= 10000 and t1 < 11500:
			print "new head:",
			print t1
			loadCode()
		curret_code = M335_CODE_0
		#fileObj.write(str((date_end - date_now).microseconds))
		#fileObj.write("us")
		date_now = date_end
		#curret_code = end_code



