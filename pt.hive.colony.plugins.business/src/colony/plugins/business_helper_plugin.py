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

import colony.base.plugin_system

class BusinessHelperPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Business Helper plugin.
    """

    id = "pt.hive.colony.plugins.business.helper"
    name = "Business Helper Plugin"
    short_name = "Business Helper"
    description = "Business Helper Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/business/helper/resources/baf.xml"}
    capabilities = ["business_helper", "build_automation_item"]
    capabilities_allowed = ["entity", "entity_bundle", "business_logic", "business_logic_bundle"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["business.helper.business_helper_system"]

    business_helper = None

    entity_plugins = []
    entity_bundle_plugins = []
    business_logic_plugins = []
    business_logic_bundle_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global business
        import business.helper.business_helper_system
        self.business_helper = business.helper.business_helper_system.BusinessHelper(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.business.helper", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.business.helper", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def import_class_module(self, class_module_name, globals, locals, global_values, base_directory_path):
        return self.business_helper.import_class_module(class_module_name, globals, locals, global_values, base_directory_path)

    def import_class_module_target(self, class_module_name, globals, locals, global_values, base_directory_path, target_module_name):
        return self.business_helper.import_class_module(class_module_name, globals, locals, global_values, base_directory_path, target_module_name)

    def generate_bundle_map(self, bundle_classes):
        return self.business_helper.generate_bundle_map(bundle_classes)

    def generate_module_bundle(self, bundle_module_name, bundle_map):
        return self.business_helper.generate_module_bundle(bundle_module_name, bundle_map)

    def get_entity_class(self):
        return self.business_helper.get_entity_class()

    def get_entity_classes_namespace(self, namespace):
        return self.business_helper.get_entity_classes_namespace(namespace)

    def get_business_logic_classes_namespace(self, namespace):
        return self.business_helper.get_business_logic_classes_namespace(namespace)

    @colony.base.decorators.load_allowed_capability("entity")
    def entity_load_allowed(self, plugin, capability):
        self.entity_plugins.append(plugin)
        self.business_helper.entity_load(plugin)

    @colony.base.decorators.load_allowed_capability("entity_bundle")
    def entity_bundle_load_allowed(self, plugin, capability):
        self.entity_bundle_plugins.append(plugin)
        self.business_helper.entity_bundle_load(plugin)

    @colony.base.decorators.load_allowed_capability("business_logic")
    def business_logic_load_allowed(self, plugin, capability):
        self.business_logic_plugins.append(plugin)
        self.business_helper.business_logic_load(plugin)

    @colony.base.decorators.load_allowed_capability("business_logic_bundle")
    def business_logic_bundle_load_allowed(self, plugin, capability):
        self.business_logic_bundle_plugins.append(plugin)
        self.business_helper.business_logic_bundle_load(plugin)

    @colony.base.decorators.unload_allowed_capability("entity")
    def entity_unload_allowed(self, plugin, capability):
        self.entity_plugins.remove(plugin)
        self.business_helper.entity_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("entity_bundle")
    def entity_bundle_unload_allowed(self, plugin, capability):
        self.entity_bundle_plugins.remove(plugin)
        self.business_helper.entity_bundle_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("business_logic")
    def business_logic_unload_allowed(self, plugin, capability):
        self.business_logic_plugins.remove(plugin)
        self.business_helper.business_logic_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("business_logic_bundle")
    def business_logic_bundle_unload_allowed(self, plugin, capability):
        self.business_logic_bundle_plugins.remove(plugin)
        self.business_helper.business_logic_bundle_unload(plugin)
