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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Lu�s Martinho <lmartinho@hive.pt>"
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

class SearchInterpreterPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Search Interpreter plugin.
    """

    id = "pt.hive.colony.plugins.search.interpreter"
    name = "Search Interpreter Plugin"
    short_name = "Search Interpreter"
    description = "Search Interpreter Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/search_interpreter/interpreter/resources/baf.xml"}
    capabilities = ["search_interpreter", "build_automation_item"]
    capabilities_allowed = ["search_interpreter_adapter"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["search_interpreter.interpreter.search_interpreter_system"]

    search_intepreter = None

    search_interpreter_adapter_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global search_interpreter
        import search_interpreter.interpreter.search_interpreter_system
        self.search_intepreter = search_interpreter.interpreter.search_interpreter_system.SearchInterpreter(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.search.interpreter", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.search.interpreter", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def process_tokens_list(self, tokens_list, properties):
        return self.search_intepreter.process_tokens_list(tokens_list, properties)

    @colony.base.decorators.load_allowed_capability("search_interpreter_adapter")
    def search_interpreter_adapter_load_allowed(self, plugin, capability):
        self.search_interpreter_adapter_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("search_interpreter_adapter")
    def search_interpreter_adapter_unload_allowed(self, plugin, capability):
        self.search_interpreter_adapter_plugins.remove(plugin)
