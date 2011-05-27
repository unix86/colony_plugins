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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

class MinimalBaseScaffolderPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Minimal Base Scaffolder Plugin.
    """

    id = "pt.hive.colony.plugins.main.scaffolding.minimal_base"
    name = "Minimal Base Scaffolder Plugin"
    short_name = "Minimal Base Scaffolder"
    description = "The minimal base scaffolder plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/minimal_base_scaffolder/scaffolder/resources/baf.xml"
    }
    capabilities = [
        "scaffolder",
        "build_automation_item"
    ]
    main_modules = [
        "minimal_base_scaffolder.scaffolder.minimal_base_scaffolder_system"
    ]

    minimal_base_scaffolder = None
    """ The minimal base scaffolder """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import minimal_base_scaffolder.scaffolder.minimal_base_scaffolder_system
        self.minimal_base_scaffolder = minimal_base_scaffolder.scaffolder.minimal_base_scaffolder_system.MinimalBaseScaffolder(self)

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

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_scaffolder_type(self):
        return self.minimal_base_scaffolder.get_scaffolder_type()

    def get_templates(self, scaffold_attributes_map):
        return self.minimal_base_scaffolder.get_templates(scaffold_attributes_map)

    def process_scaffold_attributes(self, scaffold_attributes_map):
        return self.minimal_base_scaffolder.process_scaffold_attributes(scaffold_attributes_map)

    def process_template(self, template_file_name, template, scaffold_attributes_map):
        return self.minimal_base_scaffolder.process_template(template_file_name, template, scaffold_attributes_map)

    def generate_scaffold(self, scaffold_path, scaffold_attributes_map):
        self.minimal_base_scaffolder.generate_scaffold(scaffold_path, scaffold_attributes_map)