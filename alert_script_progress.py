from longscripts.models import *
from longscripts.settings import EMAIL_ALERT_RECIPIENTS
from django.core.mail import EmailMessage
import datetime
import sys

def probeScript(script_id):
    script = Script.objects.get(id=script_id)
    msg = ""
    msg += "name: " + script.getName() + "\n"
    msg += "running: " + str(script.running) + "\n"
    msg += "started: " + script.getStartTime().strftime("%m/%d %H:%M") + "\n"
    msg += "num processed: " + str(script.getNumProcessedItems()) + "\n"
    msg += "total exceptions: " + str(script.getNumExceptions()) + "\n"
    msg += "total items: " + str(script.getNumTotalItems()) + "\n"
    msg += "time passed: " + secondsToReadable(script.getSecondsPassed()) + "\n"
    msg += "time remaining: " + secondsToReadable(script.getSecondsRemaining()) + "\n"
    msg += "------ exceptions ------" + "\n"
    for k,v in script.getExceptionNumsDictionary().items():
        msg += k + ": " + str(v) + "\n"
    msg += "------------------------" + "\n"
    return msg

def secondsToReadable(seconds):
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

def displayScriptProgress(special_errors=False):
    msg = ''
    scripts = Script.objects.all().order_by("-start")
    for script in scripts:
        msg += probeScript(script.getUniqueID())
    if special_errors:
        msg += "------ special ------ \n"
        for special_error in ScriptSpecialError.objects.all().order_by("which_error"):
            msg += str(special_error.which_error) + ": " + str(special_error.num_errors) + "\n"
        msg += "--------------------- \n"
    return msg

if __name__=="__main__":
    print str(datetime.datetime.now())
    args = sys.argv
    if len(args) > 1:
        script_id = args[1]
        msg = probeScript(script_id)
    else:
        msg = displayScriptProgress()
    if "-email" in args:
        email_alert = True
        index = args.index("-email")
        if len(args) > index:
            email = args[index+1]
            email_recipients = [email]
        else:
            email_recipients = EMAIL_ALERT_RECIPIENTS
    else:
        email_alert = False
    if email_alert:
        email = EmailMessage(subject='Longscripts Update', body=msg, to=email_recipients)
        email.send()
    else:
        print msg