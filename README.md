

# Python LongScripts : the future of scripts

LongScripts is a simple tool to track how quickly a python script is running and what exceptions it's throwing.

#### Step 1. Start your script
```python
from longscripts import runLongScript
runLongScript(my_iterable, my_function, "My script that takes a long time")
```
**my_function** is a function that takes in one argument and will get called on every element of **my_iterable**.


#### Step 2. Monitor your script 
by running longscripts.py from the command line.

Example Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
name: My Script that takes a long time
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~











