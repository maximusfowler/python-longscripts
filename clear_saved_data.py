from longscripts.models import clearSavedScripts, clearSavedSpecialErrors, clearSavedExceptions
# utility script to clear all saved data
if __name__=="__main__":
    clearSavedScripts()
    clearSavedExceptions()
    clearSavedSpecialErrors()