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

import imp

GLOBALS_REFERENCE_VALUE = "_globals"
""" The globals reference value """

class BusinessHelper:
    """
    The business helper class.
    """

    business_helper_plugin = None
    """ The business helper plugin """

    def __init__(self, business_helper_plugin):
        """
        Constructor of the class.

        @type business_helper_plugin: BusinessHelperPlugin
        @param business_helper_plugin: The business helper plugin.
        """

        self.business_helper_plugin = business_helper_plugin

    def import_class_module(self, class_module_name, globals, locals, global_values, base_directory_path, target_module_name = None):
        """
        Imports the class module using the globals and locals from the current target,
        it imports the symbols in the module to the current globals environment.

        @type class_module_name: String
        @param class_module_name: The name of the module containing the classes to be imported.
        @type globals: Dictionary
        @param globals: The global variables map.
        @type locals: Dictionary
        @param locals: The local variables map.
        @type global_values: List
        @param global_values: A list containing the global values to be converted from locals.
        @type base_directory_path: String
        @param base_directory_path: The base directory path to be used.
        @type target_module_name: String
        @param target_module_name: The name of the module to import the classes.
        @rtype: Module
        @return: The created target module.
        """

        # creates a copy of locals
        locals_copy = locals.copy()

        # iterates over the keys of the copy of locals
        for local_key_value in locals_copy:
            # retrieves the current local value
            local_value = locals_copy[local_key_value]

            # in case the local value exists in the list of global values
            if local_value in global_values:
                # adds the value to globals
                globals[local_key_value] = local_value

        if target_module_name:
            # tries to retrieve the target module
            target_module = self._get_target_module(target_module_name, globals)

            # sets the target module dictionary as the target map
            target_map = target_module.__dict__

            # sets the target module in the globals
            globals[target_module_name] = target_module
        else:
            # sets the target module as none
            target_module = None

            # sets the globals map as the target map
            target_map = globals

        base_data_module = self._get_target_module("base_data", globals)

        globals["base_data"] = base_data_module

        base_data_module.__dict__[EntityClass.__name__] = EntityClass

        globals[EntityClass.__name__] = EntityClass

        # sets the globals reference attribute
        target_map[GLOBALS_REFERENCE_VALUE] = globals

        # executes the file in the given environment
        # to import the symbols
        execfile(base_directory_path + "/" + class_module_name + ".py", target_map, target_map)

        # returns the target module
        return target_module

    def get_entity_class(self):
        return EntityClass

    def _get_target_module(self, target_module_name, globals):
        # tries to retrieve the target module
        target_module = globals.get(target_module_name, None)

        # in case the target module is not defined
        if not target_module:
            # creates the target module
            target_module = imp.new_module(target_module_name)

            # adds the target module to the globals map
            globals[target_module_name] = target_module

        # returns the target model
        return target_module

    def _get_base_data_module(self, target_module_name, globals):
        # tries to retrieve the base data module
        base_data_module = globals.get("base_data", None)

        # in case the base data module is not defined
        if not base_data_module:
            # creates the base data module
            base_data_module = imp.new_module(base_data_module)

            # adds the target module to the globals map
            globals[target_module_name] = target_module

        # returns the target model
        return target_module

class EntityClass(object):
    """
    The entity class.
    """

    def __init__(self):
        pass
