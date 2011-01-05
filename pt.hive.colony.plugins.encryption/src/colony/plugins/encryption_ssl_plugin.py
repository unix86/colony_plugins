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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class EncryptionSslPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Ssl Encryption plugin.
    """

    id = "pt.hive.colony.plugins.encryption.ssl"
    name = "Ssl Encryption Plugin"
    short_name = "Ssl Encryption"
    description = "The plugin that offers the ssl encryption support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/encryption/ssl/resources/baf.xml"}
    capabilities = ["encryption.ssl", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.encryption.rsa", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.encryption.pkcs_1", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["encryption.ssl.encryption_ssl_system"]

    encryption_ssl = None

    encryption_rsa_plugin = None
    encryption_pkcs_1_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global encryption
        import encryption.ssl.encryption_ssl_system
        self.encryption_ssl = encryption.ssl.encryption_ssl_system.EncryptionSsl(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.encryption.ssl", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_structure(self, parameters):
        return self.encryption_ssl.create_structure(parameters)

    def get_encryption_rsa_plugin(self):
        return self.encryption_rsa_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.encryption.rsa")
    def set_encryption_rsa_plugin(self, encryption_rsa_plugin):
        self.encryption_rsa_plugin = encryption_rsa_plugin

    def get_encryption_pkcs_1_plugin(self):
        return self.encryption_pkcs_1_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.encryption.pkcs_1")
    def set_encryption_pkcs_1_plugin(self, encryption_pkcs_1_plugin):
        self.encryption_pkcs_1_plugin = encryption_pkcs_1_plugin