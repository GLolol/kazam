# -*- coding: utf-8 -*-
#
#       grabber.py
#
#       Copyright 2012 David Klasinc <bigwhale@lubica.net>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import os
import shutil
import logging
logger = logging.getLogger("Grabber")

from gi.repository import GObject, Gtk, Gdk, GdkPixbuf

from kazam.backend.prefs import *
from kazam.backend.constants import *
from kazam.frontend.save_dialog import SaveDialog
from gettext import gettext as _

class Grabber(GObject.GObject):
    __gsignals__ = {
        "save-done"       : (GObject.SIGNAL_RUN_LAST,
                             None,
                             [GObject.TYPE_PYOBJECT],),
        "flush-done"      : (GObject.SIGNAL_RUN_LAST,
                             None,
                             (),),
        }

    def __init__(self):
        GObject.GObject.__init__(self)
        logger.debug("Starting Grabber.")


    def setup_sources(self, video_source, area):
        self.video_source = video_source
        print "ARRR", video_source
        self.area = area
        logger.debug("Grabber source: {0}, {1}, {2}, {3}".format(self.video_source['x'],
                                                                 self.video_source['y'],
                                                                 self.video_source['width'],
                                                                 self.video_source['height']))

    def grab(self):
        root_w = Gdk.get_default_root_window()
        self.pixbuf = None
        self.pixbuf = Gdk.pixbuf_get_from_window(root_w, self.video_source['x'],
                                                         self.video_source['y'],
                                                         self.video_source['width'],
                                                         self.video_source['height'])

        if prefs.capture_cursor_pic:
            cursor = Gdk.Cursor.new_for_display(Gdk.Display.get_default(), Gdk.CursorType.LEFT_PTR)
            c_picbuf = Gdk.Cursor.get_image(cursor)
            pointer = root_w.get_pointer()
            c_picbuf.composite(self.pixbuf, self.video_source['x'],
                                            self.video_source['y'],
                                            self.video_source['width'],
                                            self.video_source['height'],
                                            pointer[1],
                                            pointer[2],
                                            1.0,
                                            1.0,
                                            GdkPixbuf.InterpType.BILINEAR,
                                            255)

        if self.area is not None:
            self.area_buf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, self.area[4], self.area[5])
            self.pixbuf.copy_area(self.area[0], self.area[1], self.area[4], self.area[5], self.area_buf, 0, 0)
            self.pixbuf = None
            self.pixbuf = self.area_buf

        self.emit("flush-done")

    def save(self, filename):
        if self.pixbuf is not None:
            self.pixbuf.savev(filename, "png", "", "")

    def save_capture(self, old_path):
        logger.debug("Saving screenshot.")
        self.old_path = old_path
        (dialog, result, self.old_path) = SaveDialog(_("Save capture"),
                                                     self.old_path, None, main_mode=MODE_SCREENSHOT)

        if result == Gtk.ResponseType.OK:
            uri = os.path.join(dialog.get_current_folder(), dialog.get_filename())

            self.save(uri)

        dialog.destroy()
        self.emit("save-done", self.old_path)