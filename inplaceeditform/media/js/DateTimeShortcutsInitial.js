function DateTimeShortcutsInitial() {
    var datetime_load = false;
    var calendar_load = false;
    var gettext_load = false;
    try{
        if(DateTimeShortcuts != null)
            datetime_load = true;
        if(gettext != null)
            gettext_load = true;
        if(CalendarNamespace)
            calendar_load = true;
    }
    catch(err) {
    }
    if (datetime_load && calendar_load && gettext_load){
        DateTimeShortcuts.init();
    }
    else {
        setTimeout(DateTimeShortcutsInitial, 500);
    }
}
DateTimeShortcutsInitial();
