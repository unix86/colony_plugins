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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class MainRemoteManager:
    """
    The main remote manager class.
    """

    main_remote_manager_plugin = None
    """ The main remote manager plugin """

    def __init__(self, main_remote_manager_plugin):
        """
        Constructor of the class.

        @type main_remote_manager_plugin: MainRemoteManagerPlugin
        @param main_remote_manager_plugin: The main remote manager plugin.
        """

        self.main_remote_manager_plugin = main_remote_manager_plugin

    def get_available_rpc_handlers(self):
        """
        Retrieves the available rpc handler.

        @rtype: List
        @return: The list of available rpc handlers.
        """

        # creates the available rpc handlers list
        available_rpc_handlers = []

        # retrieves the rpc handler plugins
        rpc_handler_plugins = self.main_remote_manager_plugin.rpc_handler_plugins

        # iterates over all the rpc handler plugins
        for rpc_handler_plugin in rpc_handler_plugins:
            if rpc_handler_plugin.is_active():
                available_rpc_handlers.append(rpc_handler_plugin)

        return available_rpc_handlers
