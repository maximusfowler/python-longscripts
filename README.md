# Python LongScripts : the future of scripts

LongScripts is a simple tool to track how quickly a python script is running and what exceptions it's throwing in real time.

#### Step 1. Start your script
```python
from longscripts import runLongScript
runLongScript(my_iterable, my_function, "My script that takes a long time")
```
**my_function** is a function that takes in one argument and will get called on every element of **my_iterable**.


#### Step 2. Monitor your script 
You can check on your script's progress by running ```python longscripts.py``` from the command line.

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

#### :$ Advanced Features $:

##### Email alerts

Configure your smtp email settings in ls_settings.py or by setting environmental variables.
- LONGSCRIPTS_EMAIL_RECIPIENT
- LONGSCRIPTS_EMAIL_SERVER
- LONGSCRIPTS_EMAIL_USER
- LONGSCRIPTS_EMAIL_PASSWORD

Use the -email flag to have longscripts send its output to the default email recipients configured in your settings or to the optionally supplied email address.
```python longscripts.py -email [email_address]``` 

##### Clear data

```python longscripts.py -clear``` will clear all saved longscripts data.











