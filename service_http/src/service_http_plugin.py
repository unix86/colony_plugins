#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class ServiceHttpPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Service plugin.
    """

    id = "pt.hive.colony.plugins.service.http"
    name = "Http Service"
    description = "The plugin that offers the http service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "service.http"
    ]
    capabilities_allowed = [
        "http_service_handler",
        "http_service_encoding",
        "http_service_authentication_handler",
        "http_service_error_handler"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.service.utils", "1.x.x")
    ]
    main_modules = [
        "service_http.http.exceptions",
        "service_http.http.system"
    ]

    service_http = None
    """ The service http """

    http_service_handler_plugins = []
    """ The http service handler plugins """

    http_service_encoding_plugins = []
    """ The http service encoding plugins """

    http_service_authentication_handler_plugins = []
    """ The http service authentication handler plugins """

    http_service_error_handler_plugins = []
    """ The http service error handler plugins """

    service_utils_plugin = None
    """ The service utils plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import service_http.http.system
        self.service_http = service_http.http.system.ServiceHttp(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.system.Plugin.unset_configuration_property(self, property_name)

    def start_service(self, parameters):
        return self.service_http.start_service(parameters)

    def stop_service(self, parameters):
        return self.service_http.stop_service(parameters)

    @colony.base.decorators.load_allowed_capability("http_service_handler")
    def http_service_handler_load_allowed(self, plugin, capability):
        self.http_service_handler_plugins.append(plugin)
        self.service_http.http_service_handler_load(plugin)

    @colony.base.decorators.load_allowed_capability("http_service_encoding")
    def http_service_encoding_load_allowed(self, plugin, capability):
        self.http_service_encoding_plugins.append(plugin)
        self.service_http.http_service_encoding_load(plugin)

    @colony.base.decorators.load_allowed_capability("http_service_authentication_handler")
    def http_service_authentication_handler_load_allowed(self, plugin, capability):
        self.http_service_authentication_handler_plugins.append(plugin)
        self.service_http.http_service_authentication_handler_load(plugin)

    @colony.base.decorators.load_allowed_capability("http_service_error_handler")
    def http_service_error_handler_load_allowed(self, plugin, capability):
        self.http_service_error_handler_plugins.append(plugin)
        self.service_http.http_service_error_handler_load(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_handler")
    def http_service_handler_unload_allowed(self, plugin, capability):
        self.http_service_handler_plugins.remove(plugin)
        self.service_http.http_service_handler_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_encoding")
    def http_service_encoding_unload_allowed(self, plugin, capability):
        self.http_service_encoding_plugins.remove(plugin)
        self.service_http.http_service_encoding_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_authentication_handler")
    def http_service_authentication_handler_unload_allowed(self, plugin, capability):
        self.http_service_authentication_handler_plugins.remove(plugin)
        self.service_http.http_service_authentication_handler_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_error_handler")
    def http_service_error_handler_unload_allowed(self, plugin, capability):
        self.http_service_error_handler_plugins.remove(plugin)
        self.service_http.http_service_error_handler_unload(plugin)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.service.utils")
    def set_service_utils_plugin(self, service_utils_plugin):
        self.service_utils_plugin = service_utils_plugin

    @colony.base.decorators.set_configuration_property_method("service_configuration")
    def service_configuration_set_configuration_property(self, property_name, property):
        self.service_http.set_service_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("service_configuration")
    def service_configuration_unset_configuration_property(self, property_name):
        self.service_http.unset_service_configuration_property()
