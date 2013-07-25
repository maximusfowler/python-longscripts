from traceback import format_exception
import sys
import smtplib
from ls.models import *
import ls_settings

#### Importable Functions ##############################################################################################

def runLongScript(items, item_fun, name="My LongScript", resolution=5):
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


def displaySingleLongScriptProgress(script_id):
    """
    Returns string describing the status and progress of Longscripts script with inputted script_id.
    ----------
    script_id : int
        Description or name of script being logged.
    """
    script = dbGetLongScriptByID(script_id)
    msg = ""
    msg += "name: " + script.getName() + "\n"
    msg += "running: " + str(script.running) + "\n"
    msg += "started: " + script.getStartTime().strftime("%m/%d %H:%M") + "\n"
    msg += "num processed: " + str(script.getNumProcessedItems()) + "\n"
    msg += "total exceptions: " + str(script.getNumExceptions()) + "\n"
    msg += "total items: " + str(script.getNumTotalItems()) + "\n"
    msg += "time passed: " + helperSecondsToReadable(script.getSecondsPassed()) + "\n"
    msg += "time remaining: " + helperSecondsToReadable(script.getSecondsRemaining()) + "\n"
    msg += "------ exceptions ------" + "\n"
    exceptions_dict_items = script.getExceptionNumsDictionary().items()
    for k,v in exceptions_dict_items:
        msg += k + ": " + str(v) + "\n"
    if not exceptions_dict_items:
        msg += "None\n"
    msg += "================================================ \n"
    return msg

def displayLongScriptProgress(special_errors=False):
    """
    Returns string describing the status and progress of all current Longscript scripts.
    ----------
    special_errors : boolean
        Flag which controls whether or not to include section reporting special errors.
    """
    msg = "How are your scripts?\n"
    msg += "================================================ \n"
    scripts = dbGetAllLongScript()
    scripts.sort(key=lambda x: x.start)
    for script in scripts:
        msg += displaySingleLongScriptProgress(script.getUniqueID())
    if special_errors:
        msg += "------ special ------ \n"
        special_errors = dbGetAllLongScriptEvents()
        special_errors.sort(key=lambda x: x.which_error)
        for special_error in special_errors:
            msg += str(special_error.which_error) + ": " + str(special_error.num_errors) + "\n"
        msg += "--------------------- \n"
    return msg

def clearData():
    """
    Clears all saved ls data.
    """
    clearSavedScripts()
    clearSavedExceptions()
    clearSavedSpecialErrors()

#### Helper Functions ###################################################################################################

def helperSecondsToReadable(seconds):
    minutes = int(seconds / 60)
    hours = minutes / 60
    minutes = minutes - 60*hours
    days = hours / 24
    hours = hours - 24*days
    to_return = ""
    if days:
        to_return += str(days) + " days, "
    if hours:
        to_return += str(hours) + " hours, "
    to_return += str(int(minutes)) + " minutes"
    return to_return

def helperSendEmail(subject, message,to):
    from_addr = ls_settings.LONGSCRIPTS_FROM_EMAIL
    user = ls_settings.LONGSCRIPTS_EMAIL_USER
    password = ls_settings.LONGSCRIPTS_EMAIL_PASSWORD
    smtp_server = ls_settings.LONGSCRIPTS_EMAIL_SERVER
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(user,password)
    problems = server.sendmail(from_addr, to, message)
    server.quit()

#### DB Interactions ###################################################################################################

def dbGetAllLongScript():
    return list(Script.objects.all())

def dbGetLongScriptByID(id):
    return Script.objects.get(id=id)

def dbGetAllLongScriptEvents():
    return list(ScriptSpecialError.objects.all())

#### CLI Interface #####################################################################################################

def cliInterface(args):
    if "-clear" in args:
        print "---- Are you sure you want to clear all python-longscript data? [y/n]"
        while True:
            yes = {'yes','y', 'ye'}
            no = {'no','n'}
            choice = raw_input().lower()
            if choice in yes:
               print "---- :$ clearing all data $:"
               return True
            elif choice in no:
               print "---- :$ see ya later alligator $:"
               return False
            else:
               sys.stdout.write("Please respond with 'yes' or 'no'")
        clearData()
    if "-id" in args:
        index = args.index("-id")
        script_id = args[index + 1]
        msg = displaySingleLongScriptProgress(script_id)
    else:
        msg = displayLongScriptProgress()
    if "-email" in args:
        email_alert = True
        index = args.index("-email")
        if len(args)-1 > index:
            email = args[index+1]
            email_recipients = [email]
        else:
            email_recipients = ls_settings.LONGSCRIPTS_EMAIL_RECIPIENTS
    else:
        email_alert = False
    if email_alert:
        helperSendEmail(subject='python-longscripts update', message=msg, to=email_recipients)
    else:
        print msg

if __name__=="__main__":
    args = sys.argv
    cliInterface(args)
