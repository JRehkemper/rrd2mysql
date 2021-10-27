import os
import mysql.connector
import subprocess
import time

####################################
### --- User Action Required --- ###
####################################

#rrd filename to read
filename = "/var/lib/smokeping/rrd/Ping/FedoraprojektOrg.rrd"

#Smokeping steps - Interval between each Ping
step = 10

#MySQL Credentials
dbhost = "localhost"
dbuser = ""
dbpassword = ""
dbdatabase = ""

##################################
### --- End of User Action --- ###
##################################


#globale variables
lastChange = 0

#Check if rrd File was updated
def checkFileUpdate(filename):
    mtime = os.stat(filename).st_mtime
    global lastChange
    if mtime != lastChange:
        lastChange = mtime
        return True
    else:
        return False

#Read the new Values form the rrd File and save them to the values array
def readNewValue(filename):
    output = subprocess.check_output(['rrdtool', 'lastupdate', filename]).decode('utf-8')
    output = output.strip()
    output = output.splitlines()[2]
    print(output)
    words = output.split()
    values = list()
    for index, word in enumerate(words):
    	if index >= 3:
    	    values.append(float(words[index]))
    	else:
   			pass
    for index, value in enumerate(values):
    	values[index] = value*1000
    return values

#Open Database Connection
def openDBConnection():
	mydb = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
	return mydb

#Generate SQL depending on the amount of Pings per Step and insert them to Database
def processNewValue(values):
	mydb = openDBConnection()
	mycursor = mydb.cursor()
	i = 1
	pingstr = ""
	while i < len(values):
		pingstr = pingstr+", ping"+str(i)
		i += 1
	sql = "INSERT INTO jrehkemper(median"+pingstr+") VALUES (%s"+",%s "*(len(values)-1)+")"
	values = tuple(values)
	mycursor.execute(sql, values)
	mydb.commit()
	mycursor.close()
	mydb.close()
	return

def mainRoutine(filename):
    if checkFileUpdate(filename):
        values = readNewValue(filename)
        processNewValue(values)
        return

#Keep Programm running until Terminated with Ctrl+C
try:
	print("#########################")
	print("# RRD2MySQL             #")
	print("# Programm started      #")
	print("# Terminate with Ctrl+C #")
	print("#########################")
	while True:
		mainRoutine(filename)
		time.sleep(step)
except KeyboardInterrupt:
	print("Programm stopped")