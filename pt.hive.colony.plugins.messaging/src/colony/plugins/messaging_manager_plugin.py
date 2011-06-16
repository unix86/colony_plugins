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

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MessagingManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Messaging Manager plugin.
    """

    id = "pt.hive.colony.plugins.messaging.manager"
    name = "Messaging Manager Plugin"
    short_name = "Messaging Manager"
    description = "A plugin to manage the messaging service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/messaging/manager/resources/baf.xml"
    }
    capabilities = [
        "messaging_manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "messaging_extension"
    ]
    main_modules = [
        "messaging.manager.messaging_manager_exceptions",
        "messaging.manager.messaging_manager_system"
    ]

    messaging_manager = None
    """ The messaging manager """

    messaging_extension_plugins = []
    """ The messaging extension plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import messaging.manager.messaging_manager_system
        self.messaging_manager = messaging.manager.messaging_manager_system.MessagingManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def send_message(self, messaging_service_id, message_attributes):
        return self.messaging_manager.send_message(messaging_service_id, message_attributes)

    @colony.base.decorators.load_allowed_capability("messaging_extension")
    def messaging_extension_load_allowed(self, plugin, capability):
        self.messaging_extension_plugins.append(plugin)
        self.messaging_manager.load_messaging_extension_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("messaging_extension")
    def messaging_extension_unload_allowed(self, plugin, capability):
        self.messaging_extension_plugins.remove(plugin)
        self.messaging_manager.unload_messaging_extension_plugin(plugin)
