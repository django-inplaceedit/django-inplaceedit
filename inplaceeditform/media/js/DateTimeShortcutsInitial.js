function DateTimeShortcutsInitial() {
    try{
        DateTimeShortcuts.init();
        var calendar_load = CalendarNamespace;
    }
    catch(err) {
        setTimeout(DateTimeShortcutsInitial, 500);
    }
}
DateTimeShortcutsInitial();
