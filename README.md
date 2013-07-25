python-longscripts is a simple tool to track how quickly a python script is running and what exceptions it's throwing.

# Python LongScripts : the future of scripts

If you have an iterable, and want to a call a function on every piece of data in the iterable, longscripts is for you.

### Step 1. Start your script
'''python
from longscripts import runLongScript

runLongScript(my_iterable, my_function)
'''

### Step 2. Monitor your script
'''python longscripts.py'''

Example Output
================================================ 
name: arbitraryMachine
running: True
started: 07/25 16:30
num processed: 61
total exceptions: 10
total items: 100
time passed: 0 minutes
time remaining: 0 minutes
------ exceptions ------
<type 'exceptions.KeyboardInterrupt'>: 5
<class '__main__.EnigmaException'>: 5
================================================ 












