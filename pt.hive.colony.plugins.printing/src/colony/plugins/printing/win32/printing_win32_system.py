#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1089 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-22 23:19:39 +0000 (qui, 22 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import win32print
import win32ui
import win32con

import PIL.Image
import PIL.ImageWin

import printing_win32_constants

PRINTING_SCALE = 4
""" The printing scale """

TEST_TITLE = "colony_test_document"
""" The test title """

TEST_TEXT = "Hello world from Hive Colony"
""" The test text """

class PrintingWin32:
    """
    The printing win32 class.
    """

    printing_win32_plugin = None
    """ The printing win32 plugin """

    def __init__(self, printing_win32_plugin):
        """
        Constructor of the class.

        @type printing_win32_plugin: PrintingWin32Plugin
        @param printing_win32_plugin: The printing win32 plugin.
        """

        self.printing_win32_plugin = printing_win32_plugin

    def print_test(self):
        # retrieves the printer handler
        handler_device_context, printable_area, printer_size, printer_margins = self.get_printer_handler()

        # starts the document
        handler_device_context.StartDoc(TEST_TITLE)

        # starts the first page
        handler_device_context.StartPage()

        # sets the map mode
        handler_device_context.SetMapMode(win32con.MM_TWIPS)

        # draws the test text in the handler device context
        handler_device_context.DrawText(TEST_TEXT, (0, printing_win32_constants.INCH * -1, printing_win32_constants.INCH * 8, printing_win32_constants.INCH * -2), win32con.DT_CENTER)

        # ends the current page
        handler_device_context.EndPage()

        # ends the document
        handler_device_context.EndDoc()

        # closes the printer handler
        self.close_printer_handler(handler_device_context)

    def print_test_configuration(self, configuration):
        pass

    def print_test_image(self, image_path):
        # retrieves the printer handler
        handler_device_context, printable_area, printer_size, printer_margins = self.get_printer_handler()

        # opens the bitmap image
        bitmap_image = PIL.Image.open(image_path)

        # retrieves the bitmap image width and height
        bitmap_image_width, bitmap_image_height = bitmap_image.size

        # starts the document
        handler_device_context.StartDoc(TEST_TITLE)

        # starts the first page
        handler_device_context.StartPage()

        # creates the dib image from the original
        # bitmap image, created with PIL
        dib_image = PIL.ImageWin.Dib(bitmap_image)

        real_bitmap_image_width = bitmap_image_width * PRINTING_SCALE
        real_bitmap_image_height = bitmap_image_height * PRINTING_SCALE

        real_bitmap_x1 = int((printer_size[0] - printer_margins[0] - real_bitmap_image_width) / 2)
        real_bitmap_y1 = int((printer_size[1] - printer_margins[1] - real_bitmap_image_height) / 2)
        real_bitmap_x2 = real_bitmap_x1 + real_bitmap_image_width
        real_bitmap_y2 = real_bitmap_y1 + real_bitmap_image_height

        # retrieves the output for the handler device context
        handler_device_context_output = handler_device_context.GetHandleOutput()

        # draws the image in the output for the handler device context
        dib_image.draw(handler_device_context_output, (real_bitmap_x1, real_bitmap_y1, real_bitmap_x2, real_bitmap_y2))

        # ends the current page
        handler_device_context.EndPage()

        # ends the document
        handler_device_context.EndDoc()

        # closes the printer handler
        self.close_printer_handler(handler_device_context)

    def print_test_image_configuration(self, image_path, configuration):
        pass

    def print_text(self, text):
        pass

    def print_test_configuration(self, text, configuration):
        pass

    def load_printer(self, configuration):
        pass

    def get_printer_handler(self, printer_name = None):
        # in case the printer name is not defined
        if not printer_name:
            # retrieves the default printer name
            printer_name = win32print.GetDefaultPrinter()

        # creates a new win32 device context and retrieves the handler
        handler_device_context = win32ui.CreateDC()

        # creates a printer device context using the handler
        handler_device_context.CreatePrinterDC(printer_name)

        # retrieves the printable area
        printable_area = handler_device_context.GetDeviceCaps(printing_win32_constants.HORIZONTAL_RESOLUTION), handler_device_context.GetDeviceCaps(printing_win32_constants.VERTICAL_RESOLUTION)

        # retrieves the printer size
        printer_size = handler_device_context.GetDeviceCaps(printing_win32_constants.PHYSICAL_WIDTH), handler_device_context.GetDeviceCaps(printing_win32_constants.PHYSICAL_HEIGHT)

        # retrieves the printer margins
        printer_margins = handler_device_context.GetDeviceCaps(printing_win32_constants.PHYSICAL_OFFSET_X), handler_device_context.GetDeviceCaps(printing_win32_constants.PHYSICAL_OFFSET_Y)

        return (handler_device_context, printable_area, printer_size, printer_margins)

    def close_printer_handler(self, printer_handler_context):
        # releases the resource
        printer_handler_context.DeleteDC()
