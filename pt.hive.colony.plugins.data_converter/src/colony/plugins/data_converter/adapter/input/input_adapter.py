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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import copy
import time

import data_converter.adapter.input.configuration.input_configuration_parser

class InputAdapter:
    """
    Adapter used to convert data from the source medium and schema to the internal structure.
    """

    table_name_configuration_internal_entity_id_internal_id_map = {}
    """ Dictionary relating the unique identifier of an internal entity instance in a table's configuration file with the internal entity instance's real id. """
    
    internal_entity_name_primary_key_entity_id_map = {}
    """ Dictionary relating internal entity name, with primary key value, with internal entity id. """

    foreign_key_queue = None
    """ Queue of foreign keys that are waiting of the entity they point to, to be processed. """

    input_description = None
    """ Reference to the input configuration properties (extracted from the configuration file). """

    data_converter_plugin = None
    """ Reference to the plugin that owns this code. """

    logger = None
    """ Reference to the logging instance. """

    def __init__(self, data_converter_plugin):
        """
        Class constructor.
        
        @param data_converter_plugin: Reference to the plugin that owns this code.
        """

        self.data_converter_plugin = data_converter_plugin
        self.logger = self.data_converter_plugin.logger_plugin.get_logger("main").get_logger()

    def load_configuration(self):
        """
        Loads from the XML configuration file into the correspondent conversion configuration data structures.
        """
        
        parser = data_converter.adapter.input.configuration.input_configuration_parser.InputConfigurationParser()
        file_paths = self.configuration.get_configuration_file_paths()
        for file_path in file_paths:
            parser.file_path = file_path
            parser.parse()
        self.input_description = parser.input_configuration

    def convert(self, task, internal_structure, connection, configuration):
        """
        Processes an operation on the input database.
        
        @param task: Task monitoring object used to inform the status of the query.
        @param internal_structure: Internal structure where the data will be converted to.
        @param connection: Connection object for the input adapter to extract data from.
        @param configuration: Configuration object that indicates how to migrate data from the source to the internal structure.
        @return: The internal structure with the data migrated from the source medium and schema.
        """
        self.logger.warn("The input adapter has started the conversion process.\n")
                
        # reset the input adapter's data
        self.table_name_configuration_internal_entity_id_internal_id_map = {}
        self.internal_entity_name_primary_key_entity_id_map = {}
        self.foreign_key_queue = ForeignKeyQueue()
        self.internal_structure = internal_structure
        self.connection = connection
        self.configuration = configuration
        self.load_configuration()
        
        # convert the data to the internal structure
        self.process_work_units(task)
        
        # notify all data converter observers that the internal structure changed
        for data_converter_observer_plugin in self.data_converter_plugin.data_converter_observer_plugins:
            data_converter_observer_plugin.notify_data_conversion_status({"internal_structure" : internal_structure})
        return internal_structure       

    def process_work_units(self, task):
        """
        Performs the operations necessary to complete each of the specified work units.
        
        @param task: Task monitoring object used to inform the status of the query.
        @param work_units: List of work units to complete.
        """

        # where the counter should start at for this operation
        COUNTER_OFFSET = 0
        # what range does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)
        COUNTER_RANGE = 50

        counter = COUNTER_OFFSET
        work_units = self.configuration.get_work_units()
        counter_inc = COUNTER_RANGE / len(work_units)
        for work_unit in work_units:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_work_unit(task, counter, counter_inc, work_unit)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()

    def process_work_unit(self, task, counter_offset, counter_range, work_unit_name):
        """
        Processes the tables indicated by the specified work unit.
        
        @param task: Task monitoring object used to inform the status of the query.
        @param counter_offset: Where the progress counter should start at for this operation.
        @param counter_range: What range of the progress counter does this operation affect (ex: 50 would mean this total operation counts for 50% of the progress bar)
        @param work_unit_name: Name of the work unit whose work will be performed.
        """

        self.logger.warn("Input adapter: Processing work unit '%s'.\n" % work_unit_name)

        counter = counter_offset
        table_names = self.configuration.get_tables(work_unit_name)
        counter_inc = counter_range / len(table_names)
        for table_name in table_names:
            if not task.status == task.STATUS_TASK_STOPPED:
                self.process_table(table_name)
                if task.status == task.STATUS_TASK_PAUSED:
                    # confirms the pause
                    task.confirm_pause()
                    while task.status == task.STATUS_TASK_PAUSED:
                        time.sleep(1)
                    # confirms the resume
                    task.confirm_resume()

                counter += counter_inc
                #task.set_percentage_complete(counter)

    def process_handler(self, handler_name, arguments):
        """
        Invokes a given handler function with the provided name and supplying the provided arguments.
        
        @param handler_name: Name of the handler function to invoke.
        @param arguments: List of arguments that will be supplied to the handler function.
        @return: The value returned by the handler.
        """

        self.logger.debug("Input adapter: Processing handler function '%s'.\n" % handler_name)
        
        if self.configuration.has_handler(handler_name):
            handler = self.configuration.get_handler(handler_name)
            return handler(arguments)        
        
    def process_table(self, table_name):
        """
        Converts the table's contents to the internal structure.
        
        @param table_name: Name of the table one wants to process.
        """

        self.logger.warn("Input adapter: Processing table '%s'.\n" % table_name)

        # retrieve the table's rows
        table_configuration = self.input_description.get_table(table_name)
        column_names = [column_configuration.name for column_configuration in table_configuration.get_columns()]
        rows = self.connection.query(table_name, column_names)

        # run the handlers configured for this table
        self.process_table_handlers(TableConversionInfo(table_configuration, rows))
        
        # for every row in the table
        for row in rows:     
            # create the entity related with the table and a table conversion information object
            row_internal_entity = self.internal_structure.add_entity(table_configuration.internal_entity)
            row_conversion_info = RowConversionInfo(table_configuration, row_internal_entity, row)
            # bind the entity's id to the table's primary key
            self.process_primary_key(row_conversion_info)
            # process every foreign key that was waiting for this entity to be created
            self.process_foreign_key_queue(row_conversion_info)
            # process the table columns
            self.process_columns(row_conversion_info)

    def process_table_handlers(self, row_conversion_info):
        """
        Invokes the functions associated with the specified table.
        
        @param row_conversion_info: Object containing information about the table conversion process.
        """

        self.logger.debug("Input adapter: Processing table handlers for table '%s'.\n" % row_conversion_info.configuration.name)

        for handler in row_conversion_info.configuration.handlers:
            self.process_handler(handler.name, [row_conversion_info])

    def process_columns(self, row_conversion_info):
        """
        Copies data from the database columns to the internal structure entity attributes.
        
        @param row_conversion_info: Object containing information about this row conversion process.
        """
        
        table_configuration = row_conversion_info.configuration
        row_internal_entity = row_conversion_info.internal_entity
        row = row_conversion_info.row
       
        # for every plain column, convert the value and send it to the associated entity instances
        for plain_column in table_configuration.get_plain_columns():
            # if the plain column as an internal attribute target and it exists in the row set
            if not plain_column.internal_attribute is None and plain_column.name in row:
                self.logger.debug("Input adapter: Processing column '%s'.\n" % plain_column.name)
                field_value = row[plain_column.name]
                destination_internal_entity_name = row_internal_entity._name
                destination_internal_entity_id = row_internal_entity._id
                # if the column is pointing to a different internal entity than the table then use that one instead and create a link to the table entity
                if plain_column.internal_entity and plain_column.internal_entity_id:
                    destination_internal_entity_name = plain_column.internal_entity
                    destination_internal_entity_id = self.get_real_internal_entity_id(table_configuration.name, plain_column.internal_entity, plain_column.internal_entity_id)
                    self.internal_structure.set_field_value(destination_internal_entity_name, destination_internal_entity_id, row_internal_entity._name, row_internal_entity)
                # grab the row and process it through its handlers
                for handler in plain_column.handlers:
                    field_value = self.process_handler(handler.name, [field_value])
                # store the row in the associated entity
                self.internal_structure.set_field_value(destination_internal_entity_name, destination_internal_entity_id, plain_column.internal_attribute, field_value)
                           
        # for every foreign key
        for foreign_key in table_configuration.foreign_keys:
            # compute the string representation of the foreign key
            foreign_key_column_names = [foreign_key_column.name for foreign_key_column in foreign_key.columns]
            foreign_key_values = [row[foreign_key_column.name] for foreign_key_column in foreign_key.columns]
            
            # if one of the foreign key values is null then cancel the foreign key binding operation
            if None in foreign_key_values:
                break
            
            foreign_key_string = str(foreign_key_values)

            self.logger.debug("Input adapter: Processing foreign key '%s'.\n" % foreign_key_string)

            # if the foreign row the foreign key points to was already converted to an entity then create a relation to it
            foreign_table = self.input_description.get_table(foreign_key.foreign_table)
            foreign_internal_entity_id = self.get_primary_key_entity_id(foreign_table.internal_entity, foreign_key_string)
            if foreign_internal_entity_id:
               foreign_internal_entity_instance = self.internal_structure.get_entity(foreign_internal_entity_name, foreign_internal_entity_id)
               self.internal_structure.set_field_value(row_internal_entity_name, row_internal_entity_id, foreign_internal_entity_name, foreign_internal_entity_instance)
            else: # otherwise add the foreign key to the queue
               self.foreign_key_queue.enqueue_foreign_key(foreign_key_string, foreign_key, row_internal_entity._name, row_internal_entity._id)
                
    def process_primary_key(self, row_conversion_info):
        """
        Extracts the primary key value from the query row set and into the the internal structure. After this
        operation the row set will not contain the primary key column anymore.
        
        @param row_conversion_info: Object containing information about the row conversion process.
        """
        
        table_configuration = row_conversion_info.configuration
        row_internal_entity = row_conversion_info.internal_entity
        row = row_conversion_info.row
        
        # compute this row's primary key string representation
        primary_key_column_names = [column.name for column in table_configuration.primary_key_columns]
        primary_key_string = str([row[primary_key_column_name] for primary_key_column_name in primary_key_column_names])
         
        # associate the created internal entity with the row's primary key
        key = (row_internal_entity._name, primary_key_string)
        self.internal_entity_name_primary_key_entity_id_map[key] = row_internal_entity._id

    def process_foreign_key_queue(self, row_conversion_info):
        """
        Process the foreign key queue.
        
        @param row_conversion_info: Object containing information about the row conversion process.
        """
        
        table_configuration = row_conversion_info.configuration
        row_internal_entity = row_conversion_info.internal_entity
        row = row_conversion_info.row
        
        # compute this row's primary key string representation
        primary_key_column_names = [column.name for column in table_configuration.primary_key_columns]
        primary_key_string = str([row[primary_key_column_name] for primary_key_column_name in primary_key_column_names])

        # retrieve the foreign keys that were waiting for this primary key to have an entity associated with it
        foreign_key_informations = self.foreign_key_queue.get_pending_foreign_keys(table_configuration.name, primary_key_string)
        if foreign_key_informations:
                # for every foreign key create a connection from its entity to the entity that was processed
                for foreign_key_information in foreign_key_informations:
                    foreign_key_internal_entity_name = foreign_key_information["foreign_key_internal_entity_name"]
                    foreign_key_internal_entity_id = foreign_key_information["foreign_key_internal_entity_id"]
                    self.internal_structure.set_field_value(foreign_key_internal_entity_name, foreign_key_internal_entity_id, row_internal_entity_name, row_internal_entity) 

    def get_primary_key_entity_id(self, entity_name, primary_key_string):
        """
        Retrieves the internal entity unique identifier that corresponds to the provided primary key value.
        
        @param entity_name: Name of the internal entity from which one wants to get an identifier.
        @param primary_key_string: String representation of associated primary key.
        @return: Identification number of a internal entity instance.
        """
        key = (entity_name, primary_key_string)
        return self.internal_entity_name_primary_key_entity_id_map[key]
        
    def get_real_internal_entity_id(self, table_name, internal_entity_name, table_configuration_internal_entity_id):
        """
        Retrieves the equivalent internal entity id in the internal structure for the provided
        internal entity id in the configuration file.
        
        @param table_name: Name of the table where the internal entity reference is configured.
        @param internal_entity_name: Name of the internal entity.
        @param table_configuration_internal_entity_id: Identification number of the internal entity in the configuration file.
        @return: Returns the internal entity's unique identifier in the internal structure.
        """

        key = (table_name, internal_entity_name, table_configuration_internal_entity_id)
        if not key in self.table_name_configuration_internal_entity_id_internal_id_map:
            internal_entity = self.internal_structure.add_entity(internal_entity_name)
            self.table_name_configuration_internal_entity_id_internal_id_map[key] = internal_entity._id
        return self.table_name_configuration_internal_entity_id_internal_id_map[key]

class ForeignKeyQueue:
    """
    Holds information about the conversion of a certain database table. Useful for passing around different functions
    that share a requirement for these informations.
    """
    
    table_name_primary_key_foreign_key_queue_map = {}
    """ Multi-level map used to store pending foreign keys """
    
    def __init__(self):
        """
        Class constructor.
        """
        table_name_primary_key_foreign_key_queue_map = {}
    
    def enqueue_foreign_key(self, foreign_key_string, foreign_key_configuration, foreign_key_internal_entity_name, foreign_key_internal_entity_id):
        """
        Adds a foreign key to the queue.
        
        @param foreign_key: Foreign key that is waiting for its associated entity to be created.
        @param foreign_key_internal_entity_name: Name of the internal entity the pending foreign key belongs to.
        @param foreign_key_internal_entity_id: Unique identifier for the internal entity instance this foreign key belongs to.
        """
        key = (foreign_key_configuration.foreign_table, foreign_key_string)
        if not key in self.table_name_primary_key_foreign_key_queue_map:
            self.table_name_primary_key_foreign_key_queue_map[key] = []
        foreign_key_queue = self.table_name_primary_key_foreign_key_queue_map[key]
        foreign_key_queue.append({"foreign_key_internal_entity_name" : foreign_key_internal_entity_name, 
                                  "foreign_key_internal_entity_id" : foreign_key_internal_entity_id})
    
    def get_pending_foreign_keys(self, table_name, primary_key_string):
        """
        Retrieves a list with informations about the foreign keys that are waiting for the specified primary key to be processed.
        
        @param table_name: Name of the table the primary key belongs to.
        @param primary_key_string: String representation of the primary key whose associated pending foreign keys one wants to retrieve.
        @return: List with informations about the foreign keys that are waiting to be processed.
        """
        foreign_key_queue = []
        if table_name in self.table_name_primary_key_foreign_key_queue_map and primary_key in self.table_name_primary_key_foreign_key_queue_map[table_name]:
            foreign_key_queue = self.table_name_primary_key_foreign_key_queue_map[table_name][primary_key]
        return foreign_key_queue

class TableConversionInfo:
    """
    Holds information about the conversion of a certain database table.
    """

    configuration = None
    """ Table configuration object. """
    
    rows = []
    """ The rows this table has in the source medium. """

    def __init__(self, configuration, rows):
        """
        Class constructor.
        
        @param configuration: Object representing the conversion configuration for this table.
        @param rows: The rows this table has in the source medium.
        """
        
        self.configuration = configuration
        self.rows = rows

class RowConversionInfo:
    """
    Holds information about the conversion of a certain database table row.
    """

    configuration = None
    """ Table configuration object describing the table this row belongs to. """

    internal_entity = None
    """ The internal entity created for this row. """

    row = None
    """ Source medium table row. """

    def __init__(self, configuration, internal_entity, row):
        """
        Class constructor.
        
        @param configuration: Object representing the conversion configuration for this table.
        @param internal_entity: The internal entity created for this row.
        @param row: The row being converted.
        """
        
        self.configuration = configuration
        self.internal_entity = internal_entity
        self.row = row
