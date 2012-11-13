import gtk

from datetime import datetime
import gobject
from threading import Thread

class uiSignalHelpers(object):
    def __init__(self, *args, **kwargs):
        super(uiSignalHelpers, self).__init__(*args, **kwargs)
        #print 'signal helpers __init__'

    def callback(self, *args, **kwargs):
        super(uiSignalHelpers, self).callback(*args, **kwargs)
        #print 'signal helpers callback'

    def gtk_widget_show(self, w, e = None):
        w.show()
        return True
        
    def gtk_widget_hide(self, w, e = None):
        w.hide()
        return True

    def information_message(self, widget, message, cb = None):
        self.attention = "INFO: %s" % message
        messagedialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, message)
        messagedialog.connect("delete-event", lambda w, e: w.hide() or True)
        if cb:
            messagedialog.connect("response", cb)

        messagedialog.set_default_response(gtk.RESPONSE_OK)
        messagedialog.show()
        messagedialog.present()
        return messagedialog


    def error_message(self, widget, message):
        self.attention = "ERROR: %s" % message
        messagedialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CANCEL, message)
        messagedialog.run()
        messagedialog.destroy()

    def warning_message(self, widget, message):
        self.attention = "WARNING: %s" % message
        messagedialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL, message)
        messagedialog.show()
        messagedialog.present()
        messagedialog.run()
        messagedialog.destroy()

    def question_message(self, widget, message, cb = None):
        self.attention = "QUESTION: %s" % message
        messagedialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
        messagedialog.connect("delete-event", lambda w, e: w.hide() or True)
        if cb:
            messagedialog.connect("response", cb)

        messagedialog.set_default_response(gtk.RESPONSE_YES)
        messagedialog.show()
        messagedialog.present()
        return messagedialog

    def interval_dialog(self, message):
        if not self.interval_dialog_showing:
            if not self.timetracker_window.is_active():
                self.timetracker_window.show()
                self.timetracker_window.present()

            self.interval_dialog_showing = True
            self.message_dialog_instance = self.question_message(self.timetracker_window, message, self.on_interval_dialog)

    def stop_interval_dialog(self, message):
        if not self.stop_interval_dialog_showing:
            if not self.timetracker_window.is_active():
                self.timetracker_window.show()
                self.timetracker_window.present()

            self.stop_interval_dialog_showing = True
            self.stop_interval_dialog_instance = self.information_message(self.timetracker_window, message, self.on_stopped)

    def set_custom_label(self, widget, text):
        #set custom label on stock button
        Label = widget.get_children()[0]
        Label = Label.get_children()[0].get_children()[1]
        Label = Label.set_label(text)

    def window_state(self, widget, state):
        self.timetracker_window_state = state.new_window_state

class uiSignals(uiSignalHelpers):
    def __init__(self, *args, **kwargs):
        super(uiSignals, self).__init__(*args, **kwargs)
        #these are components defined inside the ui file
        #print 'signals __init__'
        self.preferences_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.timetracker_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.timetracker_window.connect('destroy', lambda w, e: w.hide() or True)
        self.timetracker_window.connect("window-state-event", self.window_state)
        self.about_dialog.connect("delete-event", lambda w, e: w.hide() or True)
        self.about_dialog.connect("response", lambda w, e: w.hide() or True)


    def callback(self, *args, **kwargs): #stub
        super(uiSignals, self).callback(*args, **kwargs) #executed after init, hopefully this will let me inject interrupts
        #print 'signals callback'
        self.icon.connect('activate', self.left_click)
        self.icon.connect("popup-menu", self.right_click)

    def before_init(self): #stub for later
        #print 'signals before init'
        pass

    def after_init(self): #init any other callback we can't setup in the actual init phase
        #print 'signals after init'
        self.project_combobox_handler = self.project_combobox.connect('changed', self.on_project_combobox_changed)
        self.task_combobox_handler = self.task_combobox.connect('changed', self.on_task_combobox_changed)

    def on_show_about_dialog(self, widget):
        self.about_dialog.show()

    def on_interval_dialog(self, dialog, a): #interval_dialog callback
        if a == gtk.RESPONSE_NO and self.running: #id will be set if running
            self.set_entries()
            if not self.timetracker_window.is_active():#show timetracker window if not shown
                self.timetracker_window.show()
                self.timetracker_window.present()
        else:
            self.timetracker_window.hide() #hide timetracker and continue task
            notes = self.get_notes(self.last_notes)
            hours = "%0.02f" % round(float(self.last_hours) + float(self.interval), 2)
            entry = self.harvest.update(self.last_entry_id, {#append to existing timer
                  'notes': notes,
                  'hours': hours,
                  'project_id': self.last_project_id,
                  'task_id': self.last_task_id
            })

        dialog.destroy()

        self.attention = None

        self.interval_dialog_showing = False

    def on_stopped(self, dialog):
        if not self.timetracker_window.is_active():
            self.timetracker_window.show()
            self.timetracker_window.present()

        dialog.destroy()

        self.attention = None

        self.stop_interval_dialog_showing = False

    def on_save_preferences_button_clicked(self, widget):
        if self.running: #if running it will turn off, lets empty the comboboxes
            #stop the timer
            #self.toggle_current_timer(self.current_entry_id) #maybe add pref option to kill timer on pref change?
            if self.message_dialog_instance:
                self.message_dialog_instance.hide() #hide the dialog

        self.get_prefs()
        if self.connect_to_harvest():
            self.preferences_window.hide()
            self.timetracker_window.show()
            self.timetracker_window.present()


    def on_task_combobox_changed(self, widget):
        new_idx = widget.get_active()
        if new_idx != -1:
            if new_idx != self.current_selected_task_idx: #-1 is sent from pygtk loop or something
                self.current_selected_task_id = self.get_combobox_selection(widget)
                self.current_selected_task_idx = new_idx
                self.refresh_comboboxes()

    def on_project_combobox_changed(self, widget):
        self.current_selected_project_id = self.get_combobox_selection(widget)
        new_idx = widget.get_active()
        if new_idx != -1:
            #reset task when new project is selected
            self.current_selected_project_idx = new_idx
            self.current_selected_task_id = None
            self.current_selected_task_idx = 0
            self.refresh_comboboxes()

    def on_show_preferences(self, widget):
        self.preferences_window.show()
        self.preferences_window.present()

    def on_away_from_desk(self, widget):
        #toggle away state
        if self.running:
            self.away_from_desk = True if not self.away_from_desk else False

    def on_check_for_updates(self, widget):
        pass

    def on_top(self, widget):
        self.always_on_top = False if self.always_on_top else True
        self.timetracker_window.set_keep_above(self.always_on_top)


    def on_submit_button_clicked(self, widget):
        self.away_from_desk = False
        self.attention = None
        self.append_add_entry()

        self.set_entries()



    def on_stop_timer(self, widget):
        self.toggle_current_timer(self.current_entry_id)


    def on_quit(self, widget):
        if self.running and self.harvest:
            self.harvest.toggle_timer(self.current_entry_id)

        gtk.main_quit()

    def _do_refresh(self):
        self.set_entries()
        self.timetracker_window.show()
        self.timetracker_window.present()

    def on_refresh(self, widget):
        self._do_refresh()

    def left_click(self, widget):
        self._do_refresh()

    def right_click(self, widget, button, time):
        #create popup menu
        menu = gtk.Menu()

        refresh = gtk.ImageMenuItem(gtk.STOCK_REFRESH)
        refresh.connect("activate", self.on_refresh)
        menu.append(refresh)

        if self.running:
            stop_timer = gtk.MenuItem("Stop Timer")
            stop_timer.connect("activate", self.on_stop_timer)
            menu.append(stop_timer)

        if not self.away_from_desk:
            away = gtk.ImageMenuItem(gtk.STOCK_NO)
            away.set_label("Away from desk")
        else:
            away = gtk.ImageMenuItem(gtk.STOCK_YES)
            away.set_label("Back at desk")

        if not self.always_on_top:
            top = gtk.ImageMenuItem(gtk.STOCK_NO)
        else:
            top = gtk.ImageMenuItem(gtk.STOCK_YES)
        top.set_label("Always on top")

        updates = gtk.MenuItem("Check for updates")
        prefs = gtk.MenuItem("Preferences")
        about = gtk.MenuItem("About")
        quit = gtk.MenuItem("Quit")

        away.connect("activate", self.on_away_from_desk)
        updates.connect("activate", self.on_check_for_updates)
        top.connect("activate", self.on_top)
        prefs.connect("activate", self.on_show_preferences)
        about.connect("activate", self.on_show_about_dialog)
        quit.connect("activate", self.on_quit)

        menu.append(away)
        menu.append(updates)
        menu.append(top)
        menu.append(prefs)
        menu.append(about)
        menu.append(quit)

        menu.show_all()

        menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.icon)
