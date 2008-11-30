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

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class MainXmlrpcClientPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Xmlrpc Client Main plugin
    """

    id = "pt.hive.colony.plugins.main.remote.client.xmlrpc"
    name = "Xmlrpc Client Main Plugin"
    short_name = "Xmlrpc Client Main"
    description = "Xmlrpc Client Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["xmlrpc_client", "remote_client_adapter"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    main_xmlrpc_client = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_remote_client_xmlrpc
        import main_remote_client_xmlrpc.client.main_xmlrpc_client_system
        self.main_xmlrpc_client = main_remote_client_xmlrpc.client.main_xmlrpc_client_system.MainXmlrpcClient(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_service_name(self):
        return self.main_xmlrpc_client.get_service_name()

    def create_remote_client(self, service_attributes):
        return self.main_xmlrpc_client.create_remote_client(service_attributes)
