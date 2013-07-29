from django.db import models
from datetime import datetime

# stores an exception thrown by a script
class ScriptException(models.Model):
    exception_type = models.CharField(max_length=50)
    message = models.TextField()
    when = models.DateTimeField(auto_now_add=True)
    item_id = models.IntegerField(null=True)

# represents a scripts and its progress: stores when it started, how many items it has processed, exceptions
class Script(models.Model):
    name = models.CharField(blank=True, max_length=50)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    running = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    num_total_items = models.IntegerField(default=0)
    num_processed_items = models.IntegerField(default=0)
    num_exceptions = models.IntegerField(default=0)
    num_successes = models.IntegerField(default=0)
    exceptions = models.ManyToManyField(ScriptException)
    def getUniqueID(self):
        return self.id
    def getName(self):
        return self.name
    def getStartTime(self):
        return self.start
    def getEndTime(self):
        return self.end
    def getNumProcessedItems(self):
        return self.num_processed_items
    def getNumExceptions(self):
        return self.num_exceptions
    def getNumTotalItems(self):
        return self.num_total_items
    def getSecondsPassed(self):
        if not self.finished:
            now = datetime.now()
            time_passed = now - self.getStartTime()
        else:
            time_passed = self.getEndTime() - self.getStartTime()
        return time_passed.total_seconds()
    def getSecondsRemaining(self):
        if self.finished:
            return 0
        total_items = float(self.getNumTotalItems())
        if not total_items:
            return 0
        else:
            percentage_complete = self.getNumProcessedItems() / float(self.getNumTotalItems())
            if percentage_complete:
                time_remaining = self.getSecondsPassed() / percentage_complete - self.getSecondsPassed()
            else:
                time_remaining = -1
            return time_remaining
    def startRunning(self):
        self.running = True
        self.start = datetime.now()
        self.save()
    def setFinished(self):
        self.running = False
        self.end = datetime.now()
        self.finished = True
        self.save()
    def getExceptionNumsDictionary(self):
        exception_types = {}
        for x in self.exceptions.all():
            e_type = x.exception_type
            if not e_type in exception_types:
                exception_types[e_type] = 0
            exception_types[e_type] += 1
        return exception_types

def clearSavedScripts():
    for x in Script.objects.all():
        x.delete()

def clearSavedExceptions():
    for x in ScriptException.objects.all():
        x.delete()

# stores the number of times a particular error or event has occurred special error
class ScriptSpecialError(models.Model):
    which_error = models.CharField(max_length=50)
    num_errors = models.IntegerField(default=0)

def saveSpecialError(which_error):
    already = ScriptSpecialError.objects.filter(which_error=which_error)
    if already:
        error = already[0]
    else:
        error = ScriptSpecialError(which_error=which_error)
        error.save()
    error.num_errors += 1
    error.save()

def clearSavedSpecialErrors():
    for x in ScriptSpecialError.objects.all():
        x.delete()
