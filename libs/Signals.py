import gtk

import pytz

class uiSignalHelpers(object):
    def __init__(self, *args, **kwargs):
        super(uiSignalHelpers, self).__init__(*args, **kwargs)
        
    def gtk_widget_show(self, w, e = None):
        w.show()
        return True
        
    def gtk_widget_hide(self, w, e = None):
        w.hide()
        return True

    def information_message(self, widget, message):
        messagedialog = gtk.MessageDialog(widget, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, message)
        messagedialog.run()
        messagedialog.destroy()

    def error_message(self, widget, message):
        messagedialog = gtk.MessageDialog(widget, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CANCEL, message)
        messagedialog.run()
        messagedialog.destroy()

    def warning_message(self, widget, message):
        messagedialog = gtk.MessageDialog(widget, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL, message)
        messagedialog.run()
        messagedialog.destroy()

    def question_message(self, widget, message):
        messagedialog = gtk.MessageDialog(widget, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
        messagedialog.run()
        messagedialog.destroy()

    def set_custom_label(self, widget, text):
        #set custom label on stock button
        Label = widget.get_children()[0]
        Label = Label.get_children()[0].get_children()[1]
        Label = Label.set_label(text)

    def is_entry_active(self, entry):
        return entry.timer_started_at.replace(tzinfo=pytz.utc) >= entry.updated_at.replace(tzinfo=pytz.utc)

    def set_comboboxes(self, widget, id):
        model = widget.get_model()
        i = 0

        for m in model:
            iter = model.get_iter(i)
            if "%s"%model.get_value(iter, 1) == "%s"%id:
                widget.set_active(i)
                break
            i += 1

class uiSignals(uiSignalHelpers):
    def __init__(self, *args, **kwargs):
        super(uiSignals, self).__init__(*args, **kwargs)
        self.preferences_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.timetracker_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.about_dialog.connect("delete-event", lambda w, e: w.hide() or True)
        self.about_dialog.connect("response", lambda w, e: w.hide() or True)
        self.icon.connect('activate', self.left_click)
        self.icon.connect("popup-menu", self.right_click)

    def on_show_about_dialog(self, widget):
        self.about_dialog.show()

    def on_save_preferences_button_clicked(self, widget):
        uri = self.harvest_url_entry.get_text()
        username = self.harvest_email_entry.get_text()
        password = self.harvest_password_entry.get_text()
        if self.auth(uri, username, password):
            self.preferences_window.hide()
            self.timetracker_window.show()
            self.timetracker_window.present()
        else:
            self.preferences_window.show()
            self.preferences_window.present()

    def on_task_combobox_changed(self, widget):
        pass #print widget

    def on_project_combobox_changed(self, widget):
        pass #print widget

    def on_client_combobox_changed(self, widget):
        pass #print widget

    def on_show_preferences(self, widget):
        self.preferences_window.show()
        self.preferences_window.present()

    def on_away_from_desk(self, widget):
        #toggle away state
        self.away_from_desk = True if not self.away_from_desk else False

    def on_check_for_updates(self, widget):
        pass

    def on_timer_toggle_clicked(self, widget, id):
        self.away_from_desk = False
        for entry in self.harvest.toggle_entry(id):
            self.set_entries()


    def get_combobox_selection(self, widget):
            model = widget.get_model()
            active = widget.get_active()
            if active < 0:
                return None
            return model[active][1] #0 is name, 1 is id
    def on_entries_expander_activate(self, widget):
        self.set_entries()

    def on_submit_button_clicked(self, widget):
        self.away_from_desk = False
        self.daily.add({
            "request": {
                'notes': self.get_textview_text(self.notes_textview),
                'hours': self.hours_entry.get_text(),
                'project_id': self.get_combobox_selection(self.project_combobox),
                'task_id': self.get_combobox_selection(self.task_combobox)
            }
        })
        self.set_entries()

    def on_timer_entry_removed(self, widget, entry_id):
        self.away_from_desk = False
        self.daily.delete(entry_id)
        self.set_entries()

    def on_edit_timer_entry(self, widget, entry_id):
        self.away_from_desk = False
        self.daily.update( entry_id, {
            "request": {
                'notes': self.get_textview_text(self.notes_textview),
                'hours': self.hours_entry.get_text(),
                'project_id': self.get_combobox_selection(self.project_combobox),
                'task_id': self.get_combobox_selection(self.task_combobox)
            }
        })

        self.set_entries()
