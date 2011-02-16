function DateTimeShortcutsInitial() {
    var datetime_load = null;
    var calendar_load = null;
    var gettext_load = null;
    try{
        datetime_load = DateTimeShortcuts;
        gettext_load = gettext;
        calendar_load = CalendarNamespace;
    }
    catch(err) {
        setTimeout(DateTimeShortcutsInitial, 3000);
    }
    if (datetime_load != null && calendar_load != null && gettext_load !=null){
        DateTimeShortcuts.init();
    }
}
DateTimeShortcutsInitial();
