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

class AuthenticationLdapPlugin(colony.base.system.Plugin):
    """
    The main class for the Authentication Ldap plugin.
    """

    id = "pt.hive.colony.plugins.authentication.ldap"
    name = "Authentication Ldap"
    description = "Authentication Ldap Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "authentication_handler"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.main.client.ldap", "1.x.x")
    ]
    main_modules = [
        "authentication.ldap.exceptions",
        "authentication.ldap.system"
    ]

    authentication_ldap = None
    """ The authentication ldap """

    client_ldap_plugin = None
    """ The client ldap plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import authentication.ldap.system
        self.authentication_ldap = authentication.ldap.system.AuthenticationLdap(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        return self.authentication_ldap.get_handler_name()

    def handle_request(self, request):
        return self.authentication_ldap.handle_request(request)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.ldap")
    def set_client_ldap_plugin(self, client_ldap_plugin):
        self.client_ldap_plugin = client_ldap_plugin
