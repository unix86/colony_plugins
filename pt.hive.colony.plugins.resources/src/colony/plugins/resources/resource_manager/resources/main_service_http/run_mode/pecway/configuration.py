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

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

configuration = {
                 "default_end_points" : [("normal", "", 8888, {}), ("ssl", "", 443, {})],
                 "default_handler" : "file",
                 "default_encoding" : None,
                 "default_content_type_charset" : "utf-8",
                 "default_client_connection_timeout" : 3,
                 "default_connection_timeout" : 30,
                 "default_request_timeout" : 30,
                 "default_response_timeout" : 30,
                 "default_number_threads" : 30,
                 "default_scheduling_algorithm" : 2,
                 "default_maximum_number_threads" : 60,
                 "default_maximum_number_work_threads" : 15,
                 "default_work_scheduling_algorithm" : 1,
                 "preferred_error_handlers" : ["template", "default"],
                 "allowed_hosts" : {"127.0.0.1" : True,
                                    "localhost" : True,
                                    "pecway.com" : True,
                                    "www.pecway.com" : True,
                                    "payments.plubee.com" : True},
                 "virtual_servers" : {
                     "resolution_order" : ["pecway.com", "www.pecway.com", "payments.plubee.com"],
                     "pecway.com" : {
                         "redirections" : {
                             "resolution_order" : ["/"],
                             "/" : {
                                 "target" : "/colony_mod_python/rest/mvc/pecway/",
                                 "recursive_redirection" : True
                             }
                         }
                     },
                     "www.pecway.com" : {
                         "redirections" : {
                             "resolution_order" : ["/"],
                             "/" : {
                                 "target" : "/colony_mod_python/rest/mvc/pecway/",
                                 "recursive_redirection" : True
                             }
                         }
                     },
                     "payments.plubee.com" : {
                         "redirections" : {
                             "resolution_order" : ["/"],
                             "/" : {
                                 "target" : "/colony_mod_python/rest/mvc/pecway/",
                                 "recursive_redirection" : True
                             }
                         }
                     }
                 },
                 "redirections" : {
                 },
                 "contexts" : {
                     "resolution_order" : ["/colony_mod_python"],
                     "/colony_mod_python" : {
                         "handler" : "colony",
                         "allow_redirection" : False,
                         "request_properties" : {}
                     }
                 }
             }