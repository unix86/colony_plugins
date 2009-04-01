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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class BusinessMysqlEnginePlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Business Mysql Engine plugin
    """

    id = "pt.hive.colony.plugins.business.mysql_engine"
    name = "Business Mysql Engine Plugin"
    short_name = "Business Mysql Engine"
    description = "Business Mysql Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["entity_manager_engine"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "MySQL-Python", "MySQLdb", "1.2.2.x", "http://mysql-python.sourceforge.net/")]
    events_handled = []
    events_registrable = []

    business_mysql_engine = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global business
        import business.mysql_engine.business_mysql_engine_system
        self.business_mysql_engine = business.mysql_engine.business_mysql_engine_system.BusinessMysqlEngine(self)

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

    def get_engine_name(self):
        return self.business_mysql_engine.get_engine_name()

    def create_connection(self, connection_parameters):
        return self.business_mysql_engine.create_connection(connection_parameters)

    def commit_connection(self, connection):
        return self.business_mysql_engine.commit_connection(connection)

    def rollback_connection(self, connection):
        return self.business_mysql_engine.rollback_connection(connection)

    def create_transaction(self, connection, transaction_name):
        return self.business_mysql_engine.create_transaction(connection, transaction_name)

    def commit_transaction(self, connection, transaction_name):
        return self.business_mysql_engine.commit_transaction(connection, transaction_name)

    def rollback_transaction(self, connection, transaction_name):
        return self.business_mysql_engine.rollback_transaction(connection, transaction_name)

    def save_entity(self, entity):
        pass

    def remove_entity(self, entity):
        pass
