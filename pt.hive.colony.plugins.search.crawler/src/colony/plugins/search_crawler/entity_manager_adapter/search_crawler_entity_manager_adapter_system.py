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

__author__ = "Lu�s Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

import types

import search_crawler_entity_manager_adapter_exceptions

SEARCH_CRAWLER_ADAPTER_TYPE = "entity_manager"
""" The search crawler adapter type """

ENTITY_MANAGER_ARGUMENTS_VALUE = "entity_manager_arguments"
""" The value for arguments for the entity manager """

ENTITY_CLASSES_MODULE_VALUE = "entity_classes_module"
""" The value for the entity classes module """

ENTITY_CLASSES_LIST_VALUE = "entity_classes_list"
""" The entity classes list value """

DIRECTORY_PATH_VALUE = "directory_path"
""" The directory path value """

TOKEN_LIST_VALUE = "token_list"
""" The key for the token list in the properties map """

ENGINE_VALUE = "engine"
""" The engine value """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

DEFAULT_ENGINE = "sqlite"
""" The default engine """

DEFAULT_CONNECTION_PARAMETERS = {"file_path" : "/remote_home/lmartinho/tobias.db", "autocommit" : False}
""" The default connection parameters """

EXCLUSION_MAP = {"__class__" : True, "__delattr__" : True, "__dict__" : True, "__doc__" : True, "__getattribute__" : True, "__hash__" : True,
                 "__init__" : True, "__module__" : True, "__new__" : True, "__reduce__" : True, "__reduce_ex__" : True, "__repr__" : True,
                 "__setattr__" : True, "__str__" : True, "__weakref__" : True, "__format__" : True, "__sizeof__" : True, "__subclasshook__" : True}

EXCLUSION_TYPES = {types.MethodType : True, types.FunctionType : True}

WORD_REGEX_VALUE = "(?u)\w+"
""" The regular expression value for scanning a word """

WORD_REGEX = re.compile(WORD_REGEX_VALUE)
""" The compiled regex object for scanning a word """

class SearchCrawlerEntityManagerAdapter:
    """
    The search crawler file system adapter class.
    """

    search_crawler_entity_manager_adapter_plugin = None
    """ The search crawler file system adapter plugin """

    def __init__(self, search_crawler_entity_manager_adapter_plugin):
        """
        Constructor of the class.

        @type search_crawler_entity_manager_adapter_plugin: SearchCrawlerEntityManagerAdapterPlugin
        @param search_crawler_entity_manager_adapter_plugin: The search crawler file system adapter plugin.
        """

        self.search_crawler_entity_manager_adapter_plugin = search_crawler_entity_manager_adapter_plugin

    def get_type(self):
        return SEARCH_CRAWLER_ADAPTER_TYPE

    def get_tokens(self, properties):
        if not ENTITY_MANAGER_ARGUMENTS_VALUE in properties:
            raise search_crawler_entity_manager_adapter_exceptions.MissingProperty(ENTITY_MANAGER_ARGUMENTS_VALUE)

        # retrieves the entity manager plugin
        entity_manager_plugin = self.search_crawler_entity_manager_adapter_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.search_crawler_entity_manager_adapter_plugin.business_helper_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = properties[ENTITY_MANAGER_ARGUMENTS_VALUE]

        # tries to retrieve the list of entity classes from the properties
        if ENTITY_CLASSES_LIST_VALUE in properties:
            entity_classes_list = properties[ENTITY_CLASSES_LIST_VALUE]
        # otherwise tries to retrieve all the classes in the provided module
        elif ENTITY_CLASSES_MODULE_VALUE in properties and DIRECTORY_PATH_VALUE in properties:
            # retrieves the relevant entity classes
            entity_classes_module_name = properties[ENTITY_CLASSES_MODULE_VALUE]

            # retrieves the directory path
            directory_path = properties[DIRECTORY_PATH_VALUE]

            # imports the base entity models module
            base_entity_models_module = business_helper_plugin.import_class_module_target(entity_classes_module_name, globals(), locals(), [], directory_path, entity_classes_module_name)

            # retrieves the entity class
            entity_class = business_helper_plugin.get_entity_class()

            # retrieves all the entity classes from the base entity models module
            entity_classes_list = self._get_entity_classes(base_entity_models_module, entity_class)
        # in case no entity specification is provided
        else:
            raise search_crawler_entity_manager_adapter_exceptions.MissingProperty(ENTITY_CLASSES_LIST_VALUE)

        # generates the entity models map from the base entity models list
        # creating the map associating the class names with the classes
        entity_classes_map = business_helper_plugin.generate_bundle_map(entity_classes_list)

        # retrieves the engine from the entity manager arguments or uses
        # the default engine
        engine = entity_manager_arguments.get(ENGINE_VALUE, DEFAULT_ENGINE)

        # retrieves the connection parameters from the entity manager arguments or uses
        # the default connection parameters
        connection_parameters = entity_manager_arguments.get(CONNECTION_PARAMETERS_VALUE, DEFAULT_CONNECTION_PARAMETERS)

        # creates a new entity manager for the remote models
        entity_manager = entity_manager_plugin.load_entity_manager(engine)

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters(connection_parameters)

        # sets the entity manager classes list
        entity_manager.entity_classes_list = entity_classes_list

        # sets the entity manager classes map
        entity_manager.entity_classes_map = entity_classes_map

        # loads the entity manager
        entity_manager.load_entity_manager()

        # creates the token list
        token_list = []

        # retrieves the list of entities
        options = {}
        for entity_class in entity_classes_list:
            entities = entity_manager._find_all_options(entity_class, options)

            for entity in entities:
                entity_tokens = self.get_entity_tokens(entity, entity_class)
                token_list.append(entity_tokens)

        # crawls across the entities for tokens

        # returns the token list
        return token_list

    def get_handler_plugin(self, properties):
        search_provider_entity_manager_plugins = self.search_crawler_entity_manager_adapter_plugin.search_provider_entity_manager_plugins

        for search_provider_entity_manager_plugin in search_provider_entity_manager_plugins:
            if search_provider_entity_manager_plugin.is_file_provider(properties):
                return search_provider_entity_manager_plugin

    def get_entity_tokens(self, entity, entity_class):
        # retrieves the name of the entity class
        entity_class_name = entity_class.__name__

        # the list of words in the entity
        entity_word_list = []

        # the corresponding attributes for each word in the
        entity_word_attribute_list = []

        # retrieves the entitie's attributes
        entity_attributes = [value for value in dir(entity) if not value in EXCLUSION_MAP and not type(getattr(entity, value)) in EXCLUSION_TYPES]

        # for all the entity attributes
        for entity_attribute in entity_attributes:
            # retrieves the attribute value
            entity_attribute_value = unicode(getattr(entity, entity_attribute))

            # retrieves the list of words in the attribute
            attribute_word_list = WORD_REGEX.findall(entity_attribute_value)

            # appends the list of words in the attribute to the entity word list
            entity_word_list.extend(attribute_word_list)

            attribute_word_list_length = len(attribute_word_list)

            entity_word_attribute_list.extend([entity_attribute for _i in range(attribute_word_list_length)])

        # computes the number of word hits
        entity_word_list_length = len(entity_word_list)

        # creates a list with the corresponding positions for each word
        entity_word_positions_list = range(entity_word_list_length)

        # generates the words metadata list
        entity_word_metadata_list = [{"position" : value, "attribute" : attribute} for value, attribute in zip(entity_word_positions_list, entity_word_attribute_list)]

        # creates the document information map
        # @todo: determine the entity's primary key
        document_information_map = {"document_id": entity.object_id, "entity_class_name" : entity_class_name}

        return [entity_word_list, entity_word_metadata_list, document_information_map]

    def _get_entity_classes(self, module, entity_class):
        """
        Retrieves all the entity classes from the given module
        using the given entity class as the reference to get the entity classes.

        @type module: Module
        @param module: The module to be used to retrieve the entity classes.
        @type entity_class: Class
        @param entity_class: The entity class to be used as reference
        to retrieve the entity classes.
        @rtype: List
        @return: The list of entity classes in the module.
        """

        # creates the entity classes list
        entity_classes = []

        # retrieves the base entity models module map
        module_map = module.__dict__

        # iterates over all the module item names
        for module_item_name in module_map:
            # retrieves the module item from  module
            module_item = getattr(module, module_item_name)

            # retrieves the module item type
            module_item_type = type(module_item)

            # in case the module item type is type and
            # the module item is subclass of the entity class
            if module_item_type == types.TypeType and issubclass(module_item, entity_class):
                # adds the module item to the entity classes
                entity_classes.append(module_item)

        # returns the entity classes
        return entity_classes
