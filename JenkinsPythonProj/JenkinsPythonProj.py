import jenkins
import sys
import time
import sqlite3


server = jenkins.Jenkins('http://localhost:8080', username='admin', password='essai')
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
    print(executionString)
    conn.execute(executionString)

conn.commit()
print "Records created successfully";
conn.close()