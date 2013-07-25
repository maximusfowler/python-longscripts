from longscripts.monitor_script import runScript
from time import sleep
from functools import partial
import random

print "longscripts example!"
# random function
class EnigmaException(Exception):
    pass
def arbitraryMachine(number, cool_numbers, shitty_numbers):
    if number in shitty_numbers:
        raise EnigmaException(str(number) + " sucks!")
    elif number in cool_numbers:
        print number
        sleep(60)

# create a function which takes in one argument using functools.partial
numbers = range(100)
cool_numbers = random.sample(numbers, random.randint(5,10))
shitty_numbers = random.sample(numbers, random.randint(5,10))
item_fun = partial(arbitraryMachine, cool_numbers=cool_numbers, shitty_numbers=shitty_numbers)

# items, is just a list of numbers in this case
items = numbers

# run the script using runScript from longscript.monitor_script
runScript(name="arbitraryMachine", items=items, item_fun=item_fun)

# open up another shell and run alert_script_progress.sh to monitor the progress of the script while its running
