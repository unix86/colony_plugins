#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainServiceXmppPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Xmpp Service Main plugin.
    """

    id = "pt.hive.colony.plugins.main.service.xmpp"
    name = "Xmpp Service Main Plugin"
    short_name = "Xmpp Service Main"
    description = "The plugin that offers the xmpp service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_service_xmpp/xmpp/resources/baf.xml"
    }
    capabilities = [
        "service.xmpp",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "xmpp_service_handler"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.service.utils", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.service.xmpp_helper", "1.0.0")
    ]
    main_modules = [
        "main_service_xmpp.xmpp.main_service_xmpp_exceptions",
        "main_service_xmpp.xmpp.main_service_xmpp_system"
    ]

    main_service_xmpp = None
    """ The main service xmpp """

    xmpp_service_handler_plugins = []
    """ The xmpp service handler plugins """

    main_service_utils_plugin = None
    """ The main service utils plugin """

    main_service_xmpp_helper_plugin = None
    """ The main service xmpp helper plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_service_xmpp.xmpp.main_service_xmpp_system
        self.main_service_xmpp = main_service_xmpp.xmpp.main_service_xmpp_system.MainServiceXmpp(self)

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def start_service(self, parameters):
        return self.main_service_xmpp.start_service(parameters)

    def stop_service(self, parameters):
        return self.main_service_xmpp.stop_service(parameters)

    @colony.base.decorators.load_allowed_capability("xmpp_service_handler")
    def xmpp_service_handler_load_allowed(self, plugin, capability):
        self.xmpp_service_handler_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("xmpp_service_handler")
    def xmpp_service_handler_unload_allowed(self, plugin, capability):
        self.xmpp_service_handler_plugins.remove(plugin)

    def get_main_service_utils_plugin(self):
        return self.main_service_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.service.utils")
    def set_main_service_utils_plugin(self, main_service_utils_plugin):
        self.main_service_utils_plugin = main_service_utils_plugin

    def get_main_service_xmpp_helper_plugin(self):
        return self.main_service_xmpp_helper_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.service.xmpp_helper")
    def set_main_service_xmpp_helper_plugin(self, main_service_xmpp_helper_plugin):
        self.main_service_xmpp_helper_plugin = main_service_xmpp_helper_plugin

    @colony.base.decorators.set_configuration_property_method("service_configuration")
    def service_configuration_set_configuration_property(self, property_name, property):
        self.main_service_xmpp.set_service_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("service_configuration")
    def service_configuration_unset_configuration_property(self, property_name):
        self.main_service_xmpp.unset_service_configuration_property()
