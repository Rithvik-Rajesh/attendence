import subprocess

# Create and start the processes
proc1 = subprocess.Popen(['python', 'attendence/main.py'])
proc2 = subprocess.Popen(['python', 'attendence/Scanner.py'])
# Wait for the processes to finish
proc1.wait() 
proc2.wait()