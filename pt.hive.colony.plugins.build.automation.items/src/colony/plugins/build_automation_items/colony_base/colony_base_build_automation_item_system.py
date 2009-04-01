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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class ColonyBaseBuildAutomationItem:
    """
    The colony base build automation item class.
    """

    colony_base_build_automation_item_plugin = None
    """ The colony base build automation item plugin """

    def __init__(self, colony_base_build_automation_item_plugin):
        """
        Constructor of the class.

        @type colony_base_build_automation_item_plugin: ColonyBaseBuildAutomationItemPlugin
        @param colony_base_build_automation_item_plugin: The colony base build automation item plugin.
        """

        self.colony_base_build_automation_item_plugin = colony_base_build_automation_item_plugin

    def get_build_automation_file_path(self):
        """
        Retrieves the build automation file path.

        @rtype: String
        @return: The build automation file path.
        """

        # retrieves the plugin manager
        manager = self.colony_base_build_automation_item_plugin.manager

        # retrieves the colony base build automation item plugin id
        colony_base_build_automation_item_plugin_id = self.colony_base_build_automation_item_plugin.id

        # retrieves the colony base build automation item plugin path
        colony_base_build_automation_item_plugin_path = manager.get_plugin_path_by_id(colony_base_build_automation_item_plugin_id)

        # retrieves the colony base build automation item baf xml path
        colony_base_build_automation_item_plugin_baf_path = colony_base_build_automation_item_plugin_path + "/build_automation_items/colony_base/resources/baf.xml"

        return colony_base_build_automation_item_plugin_baf_path

    def get_build_automation_execution_path(self):
        """
        Retrieves the build automation execution path.

        @rtype: String
        @return: The build automation execution path.
        """

        # retrieves the plugin manager
        manager = self.colony_base_build_automation_item_plugin.manager

        # retrieves the colony base build automation item plugin id
        colony_base_build_automation_item_plugin_id = self.colony_base_build_automation_item_plugin.id

        # retrieves the colony base build automation item plugin path
        colony_base_build_automation_item_plugin_path = manager.get_plugin_path_by_id(colony_base_build_automation_item_plugin_id)

        return colony_base_build_automation_item_plugin_path
