from longscripts.models import *
from traceback import format_exception
import sys

def runScript(name, items, item_fun, resolution=5):
    """
    runs inputted function on every item in inputted iterable,
    storing how much progress the script has made and all the exceptions that are thrown
    Parameters
    ----------
    name : str
        Description or name of script being logged.
    items : iterable
        Every item of item_fun will be used in a separate call of item_fun
    item_fun: function
        A function which takes in one mandatory argument
    resolution: int
        Every <resolution> number of items processed, the script will save all exceptions throw
        and script progress to a persistent database and clear this data from memory.
    """
    script = Script(name=name, num_total_items=len(items))
    script.save()
    print "Running and Logging " + name + " (ID is " + str(script.getUniqueID()) + ")"
    script.startRunning()
    found_exceptions = []
    for count,item in enumerate(items):
        try:
            item_fun(item)
            script.num_successes += 1
        except:
            e_type, the_exception, traceback = sys.exc_info()
            e_strings = format_exception(e_type, the_exception, traceback)
            e_message = ""
            for i,x in enumerate(e_strings):
                e_message += x + "\n"
            script_exception = ScriptException(exception_type=str(e_type), message=e_message, item_id=count)
            found_exceptions.append(script_exception)
            script.num_exceptions += 1
        finally:
            script.num_processed_items += 1
        if not count % resolution:
            script.save()
            for x in found_exceptions:
                x.save()
                script.exceptions.add(x)
            found_exceptions = []
    script.setFinished()
