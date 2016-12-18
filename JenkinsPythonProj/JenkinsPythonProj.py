import jenkins
import sys
import time
import sqlite3

jenkinsURL = raw_input("Please enter your Jenkins URL. Leave blank for localhost")
if jenkinsURL == "":
    jenkinsURL = 'http://localhost:8080'            
jenkinsUsername = raw_input("Please enter your Jenkins username. Leave blank for admin")
if jenkinsUsername == "":
    jenkinsUsername = "admin"
jenkinsPassword = raw_input("Please enter your Jenkins password:")


server = jenkins.Jenkins(jenkinsURL,jenkinsUsername, jenkinsPassword)
jobs = server.get_jobs()
currentTimeInEpoch = time.time()
conn = sqlite3.connect('project.db')
print "Opened database successfully";


for job in jobs:    
    jobName = job["fullname"]
    jobColor = job["color"].lower()    
    if(jobColor == "blue"):
        jobStatus = "Success"
    elif(jobColor == "red"):
        jobStatus = "Failed"
    elif(jobColor == "notbuilt"):
        jobStatus = "Not Built"   
    else:
        jobStatus = jobColor    

    print("Project: %s Project Status: %s Time checked: %f" %(jobName, jobStatus, currentTimeInEpoch))
   
    executionString = ("INSERT OR REPLACE INTO Project (project_name,project_status,time_last_updated) \
      VALUES ('%s','%s', %f)" % (jobName,jobStatus,currentTimeInEpoch))    
    conn.execute(executionString)

conn.commit()
print "Records created successfully";
conn.close()