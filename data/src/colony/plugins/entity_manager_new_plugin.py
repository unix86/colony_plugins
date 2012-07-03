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

__revision__ = "$LastChangedRevision: 7650 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 12:16:51 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class EntityManagerNewPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Entity Manager New plugin.
    """

    id = "pt.hive.colony.plugins.data.entity_manager.new"
    name = "Entity Manager New Plugin"
    short_name = "Data Entity Manager New"
    description = "The plugin that manages the entity manager orm system new"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/data/entity_manager_new/resources/baf.xml"
    }
    capabilities = [
        "plugin_test_case_bundle",
        "build_automation_item"
    ]
    capabilities_allowed = [
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.x.x")
    ]
    main_modules = [
        "data.entity_manager_new.entity_manager_decorators",
        "data.entity_manager_new.entity_manager_exceptions",
        "data.entity_manager_new.entity_manager_new_system",
        "data.entity_manager_new.entity_manager_structures",
        "data.entity_manager_new.entity_manager_test",
        "data.entity_manager_new.entity_manager_test_mocks",
        "data.entity_manager_new.mysql_system",
        "data.entity_manager_new.pgsql_system",
        "data.entity_manager_new.sqlite_system"
    ]

    entity_manager = None
    """ The entity manager """

    entity_manager_test = None
    """ The entity manager test """

    entity_manager_decorators_module = None
    """ The entity manager decorators module """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import data.entity_manager_new.entity_manager_new_system
        import data.entity_manager_new.entity_manager_test
        import data.entity_manager_new.entity_manager_decorators
        self.entity_manager = data.entity_manager_new.entity_manager_new_system.DataEntityManager(self)
        self.entity_manager_test = data.entity_manager_new.entity_manager_test.EntityManagerTest(self)
        self.entity_manager_decorators_module = data.entity_manager_new.entity_manager_decorators

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

    def load_entity_manager(self, engine_name):
        """
        Loads an entity manager for the given engine name.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        return self.entity_manager.load_entity_manager(engine_name)

    def load_entity_manager_properties(self, engine_name, properties):
        """
        Loads an entity manager for the given engine name.

        @type engine_name: String
        @param engine_name: The name of the engine to be used.
        @type properties: Dictionary
        @param properties: The properties to be used in the
        loading of the entity manager
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        return self.entity_manager.load_entity_manager(engine_name, properties)

    def get_entity_manager(self, id):
        """
        Retrieves the appropriate entity manager instance for the
        given (entity manager) identifier.
        In case no entity manager instance is found none is retrieved.

        @type id: String
        @param id: The identifier of the entity manager to be retrieved.
        @rtype: EntityManager
        @return: The retrieved entity manager.
        """

        return self.entity_manager.get_entity_manager(id)

    def get_entity_class(self):
        """
        Retrieves the top level entity class, responsible for the base
        methods to be used along all the entity classes.

        All the entities to be used in the context of the entity manager
        should inherit from this class in order to provide the appropriate
        interface for entity manager handling.

        @rtype: EntityClass
        @return: The top level entity class, responsible for the base
        methods to be used along all the entity classes.
        """

        return self.entity_manager.get_entity_class()

    def get_transaction_decorator(self):
        """
        Retrieves the transaction decorator used to decorate
        a method in order to force transaction existence.

        @rtype: Function
        @return: The transaction decorator function.
        """

        return self.entity_manager_decorators_module.transaction

    def get_lock_table_decorator(self):
        """
        Retrieves the lock table decorator used to decorate
        a method in order to force locking in table.

        @rtype: Function
        @return: The lock table decorator function.
        """

        return self.entity_manager_decorators_module.lock_table

    def get_plugin_test_case_bundle(self):
        return self.entity_manager_test.get_plugin_test_case_bundle()

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
