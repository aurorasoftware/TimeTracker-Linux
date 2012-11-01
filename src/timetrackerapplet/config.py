# Copyright (C) 2008 Jimmy Do <jimmydo@users.sourceforge.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os.path as path

try:
    from defs import *
except ImportError:
    PACKAGE = 'timetracker-applet'
    VERSION = '0'
    GETTEXT_PACKAGE = ''
    LOCALE_DIR = ''
    RESOURCES_DIR = path.join(path.dirname(__file__), '../../data')
    IMAGES_DIR = path.join(path.dirname(__file__), '../../images')

print 'Using these definitions:'
print 'GETTEXT_PACKAGE: %s' % GETTEXT_PACKAGE
print 'LOCALE_DIR: %s' % LOCALE_DIR
print 'RESOURCES_DIR: %s' % RESOURCES_DIR
print 'IMAGES_DIR: %s' % IMAGES_DIR

GLADE_PATH = path.join(RESOURCES_DIR, 'timetracker-applet.glade')
POPUP_MENU_FILE_PATH = path.join(RESOURCES_DIR, 'TimeTrackerApplet.xml')
ICON_PATH = path.join(IMAGES_DIR, 'timetracker-applet.png')
PRESETS_PATH = path.expanduser('~/.gnome2/timetracker-applet/presets.xml')
DEFAULT_SOUND_PATH = '/usr/share/sounds/gtk-events/clicked.wav'
