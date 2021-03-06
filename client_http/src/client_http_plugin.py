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

class ClientHttpPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Client plugin.
    """

    id = "pt.hive.colony.plugins.client.http"
    name = "Http Client"
    description = "The plugin that offers the http client"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "client.http"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.client.utils", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.url_parser", "1.x.x")
    ]
    main_modules = [
        "client_http.exceptions",
        "client_http.system"
    ]

    client_http = None
    """ The client http """

    client_utils_plugin = None
    """ The client plugin """

    url_parser_plugin = None
    """ The url parser plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import client_http.system
        self.client_http = client_http.system.ClientHttp(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def create_client(self, parameters):
        return self.client_http.create_client(parameters)

    def create_request(self, parameters):
        return self.client_http.create_request(parameters)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.client.utils")
    def set_client_utils_plugin(self, client_utils_plugin):
        self.client_utils_plugin = client_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.url_parser")
    def set_url_parser_plugin(self, url_parser_plugin):
        self.url_parser_plugin = url_parser_plugin
