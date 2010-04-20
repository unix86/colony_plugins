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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys
import socket
import select

import colony.libs.string_buffer_util

import main_client_http_exceptions

HTTP_PREFIX_VALUE = "http://"
""" The http prefix value """

HTTPS_PREFIX_VALUE = "https://"
""" The https prefix value """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post mehtod value """

HTTP_1_1_VERSION = "HTTP/1.1"
""" The http 1.1 protocol version """

WWW_FORM_URLENCODED_VALUE = "application/x-www-form-urlencoded"
""" The www form urlencoded value """

RESPONSE_TIMEOUT = 3
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

USER_AGENT_NAME = "Hive-Colony-Web-Client"
""" The user agent name """

USER_AGENT_VERSION = "1.0.0"
""" The user agent version """

ENVIRONMENT_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
""" The environment version """

USER_AGENT_IDENTIFIER = USER_AGENT_NAME + "/" + USER_AGENT_VERSION + " (Python/" + sys.platform + "/" + ENVIRONMENT_VERSION + ")"
""" The user agent identifier """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

STATUS_CODE_VALUES = {100 : "Continue", 101 : "Switching Protocols",
                      200 : "OK", 207 : "Multi-Status",
                      301 : "Moved permanently", 302 : "Found", 303 : "See Other", 304 : "Not Modified",
                      305 : "Use Proxy", 306 : "(Unused)", 307 : "Temporary Redirect",
                      403 : "Forbidden", 404 : "Not Found",
                      500 : "Internal Server Error"}
""" The status code values map """

HOST_VALUE = "Host"
""" The host value """

USER_AGENT_VALUE = "User-Agent"
""" The user agent value """

CONTENT_LENGTH_VALUE = "Content-Length"
""" The content length value """

CONTENT_TYPE_VALUE = "Content-Type"
""" The content type value """

LOCATION_VALUE = "Location"
""" The location value """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

QUOTE_SAFE_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' '_.-"
""" The string containing all the safe characters to be quoted """

QUOTE_SAFE_MAPS = {}
""" The map of cached (buffered) safe lists to be quoted """

PROTOCOL_SOCKET_NAME_MAP = {HTTP_PREFIX_VALUE : "normal", HTTPS_PREFIX_VALUE : "ssl"}
""" The map associating the http protocol prefixed with the name of the socket """

PROTOCOL_DEFAULT_PORT_MAP = {HTTP_PREFIX_VALUE : 80, HTTPS_PREFIX_VALUE : 443}
""" The map associating the http protocol prefixed with the port number """

class MainClientHttp:
    """
    The main client http class.
    """

    main_client_http_plugin = None
    """ The main client http plugin """

    def __init__(self, main_client_http_plugin):
        """
        Constructor of the class.

        @type main_client_http_plugin: MainClientHttp
        @param main_client_http_plugin: The main client http plugin.
        """

        self.main_client_http_plugin = main_client_http_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given paramaters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: HttpClient
        @return: The created client object.
        """

        # retrieves the version
        version = parameters.get("version", None)

        # creates the http client
        http_client = HttpClient(self, version)

        # returns the http client
        return http_client

    def create_request(self, parameters):
        pass

class HttpClient:
    """
    The http client class, representing
    a client connection in the http protocol.
    """

    main_client_http = None
    """ The main client http object """

    protocol_version = "none"
    """ The version of the http protocol """

    content_type_charset = None
    """ The content type charset """

    def __init__(self, main_client_http, protocol_version, content_type_charset = DEFAULT_CHARSET):
        """
        Constructor of the class.

        @type main_client_http: MainClientHttp
        @param main_client_http: The main client http object.
        @type protocol_version: String
        @param protocol_version: The version of the http protocol to
        be used.
        @type content_type_charset: String
        @param content_type_charset: The charset to be used by the content.
        """

        self.main_client_http = main_client_http
        self.protocol_version = protocol_version
        self.content_type_charset = content_type_charset

    def fetch_url(self, url, method, parameters):
        # parses the url retrieving the protocol the host the port and the path
        protocol, host, port, path = self._parse_url(url)

        # creates the http request with the host the port, the path
        # and the parameters
        request = HttpRequest(host, port, path, parameters)

        # retrieves the result value from the request
        result_value = request.get_result()

        # retrieves the socket name from the protocol socket map
        socket_name = PROTOCOL_SOCKET_NAME_MAP.get(protocol, None)

        self.http_connection = self._get_socket(socket_name)
        self.http_connection.connect((host, port))
        self.http_connection.send(result_value)

        # retrieves the response
        response = self.retrieve_response(request)

        # returns the response
        return response

    def _get_socket(self, socket_name = "normal"):
        # retrieves the socket provider plugins
        socket_provider_plugins = self.main_client_http.main_client_http_plugin.socket_provider_plugins

        # iterates over all the socket provider plugins
        for socket_provider_plugin in socket_provider_plugins:
            # retrieves the provider name from the socket provider plugin
            socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

            # in case the names are the same
            if socket_provider_plugin_provider_name == socket_name:
                # creates a new socket with the socket provider plugin
                socket = socket_provider_plugin.provide_socket()

                return socket

    def build_url(self, base_url, method, parameters):
        """
        Builds the url for the given base url, method
        and parameters.

        @type base_url: String
        @param base_url: The base url to build the final
        url.
        @type method: String
        @param method: The method to be used in the url retrieval.
        @type parameters: Dicionary
        @param parameters: The parameters to be used in the url
        retrieval.
        @rtype: String
        @return: The final url value.
        """

        # in case the request method is not get
        if not method == GET_METHOD_VALUE:
            # returns the base url
            return base_url

        # creates the http request to build the url
        request = HttpRequest(attributes_map = parameters)

        # encodes the request attributes
        encoded_attributes = request._encode_attributes()

        # in case the encoded attributes string
        # is not valid or is empty the url remain
        # the base one
        if not encoded_attributes:
            # returns the base url
            return base_url

        # in case no exclamation mark exists in
        # the url
        if base_url.find("?") == -1:
            # creates the url by adding the encoded attributes
            # as the first parameters
            url = base_url + "?" + encoded_attributes
        # in case an exclamation mark already exists in the
        # url (parameters exist)
        else:
            # creates the url by adding the encoded attributes
            # to the existing parameters
            url = base_url + "&" + encoded_attributes

        # return the built url
        return url

    def retrieve_response(self, request, response_timeout = RESPONSE_TIMEOUT):
        """
        Retrieves the response from the received message.

        @rtype: HttpRequest
        @return: The request that originated the response.
        @type response_timeout: int
        @param response_timeout: The timeout for the response retrieval.
        @rtype: HttpResponse
        @return: The response from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a response object
        response = HttpResponse(request)

        # creates the start line loaded flag
        start_line_loaded = False

        # creates the header loaded flag
        header_loaded = False

        # creates the message loaded flag
        message_loaded = False

        # creates the message offset index, representing the
        # offset byte to the initialization of the message
        message_offset_index = 0

        # creates the message size value
        message_size = 0

        # creates the received data size (counter)
        received_data_size = 0

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(response_timeout)

            # retrieves the data length
            data_length = len(data)

            # in case no valid data was received
            if data_length == 0:
                # raises the http invalid data exception
                raise main_client_http_exceptions.HttpInvalidDataException("empty data received")

            # increments the received data size (counter)
            received_data_size += data_length

            # writes the data to the string buffer
            message.write(data)

            # in case the header is loaded or the message contents are completely loaded
            if not header_loaded or received_data_size - message_offset_index == message_size:
                # retrieves the message value from the string buffer
                message_value = message.get_value()
            # in case there's no need to inspect the message contents
            else:
                # continues with the loop
                continue

            # in case the start line is not loaded
            if not start_line_loaded:
                # finds the first new line value
                start_line_index = message_value.find("\r\n")

                # in case there is a new line value found
                if not start_line_index == -1:
                    # retrieves the start line
                    start_line = message_value[:start_line_index]

                    # splits the start line in spaces
                    start_line_splitted = start_line.split(" ")

                    # retrieves the start line splitted length
                    start_line_splitted_length = len(start_line_splitted)

                    # in case the length of the splitted line is not three
                    if not start_line_splitted_length == 3:
                        # raises the http invalid data exception
                        raise main_client_http_exceptions.HttpInvalidDataException("invalid data received: " + start_line)

                    # retrieve the protocol version the status code and the satus message
                    # from the start line splitted
                    protocol_version, status_code, status_message = start_line_splitted

                    # converts the status code to integer
                    status_code_integer = int(status_code)

                    # sets the response protocol version
                    response.set_protocol_version(protocol_version)

                    # sets the response status code
                    response.set_status_code(status_code_integer)

                    # sets the response status message
                    response.set_status_message(status_message)

                    # sets the start line loaded flag
                    start_line_loaded = True

            # in case the header is not loaded
            if not header_loaded:
                # retrieves the end header index (two new lines)
                end_header_index = message_value.find("\r\n\r\n")

                # in case the end header index is found
                if not end_header_index == -1:
                    # sets the message offset index as the end header index
                    # plus the two sequences of newlines (four characters)
                    message_offset_index = end_header_index + 4

                    # sets the header loaded flag
                    header_loaded = True

                    # retrieves the start header index
                    start_header_index = start_line_index + 2

                    # retrieves the headers part of the message
                    headers = message_value[start_header_index:end_header_index]

                    # splits the headers by line
                    headers_splitted = headers.split("\r\n")

                    # iterates over the headers lines
                    for header_splitted in headers_splitted:
                        # finds the header separator
                        division_index = header_splitted.find(":")

                        # retrieves the header name
                        header_name = header_splitted[:division_index].strip()

                        # retrieves the header value
                        header_value = header_splitted[division_index + 1:].strip()

                        # sets the header in the headers map
                        response.headers_map[header_name] = header_value

                    # in case the location value is set in the response header
                    if LOCATION_VALUE in response.headers_map:
                        # retrieves the location
                        location = response.headers_map[LOCATION_VALUE]

                        # returns the "new" fetched url
                        return self.fetch_url(location, request.operation_type, request.attributes_map)

                    # retrieves the message size
                    message_size = int(response.headers_map.get(CONTENT_LENGTH_VALUE, 0))

            # in case the message is not loaded and the header is loaded
            if not message_loaded and header_loaded:
                # retrieves the start message size
                start_message_index = end_header_index + 4

                # retrieves the message part of the message value
                message_value_message = message_value[start_message_index:]

                # in case the length of the message value message is the same
                # or greater as the message size
                if len(message_value_message) >= message_size:
                    # sets the message loaded flag
                    message_loaded = True

                    # sets the received message
                    response.received_message = message_value_message

                    # decodes the response if necessary
                    self.decode_response(response)

                    # returns the response
                    return response

    def decode_response(self, response):
        """
        Decodes the response message for the encoding
        specified in the response.

        @type response: HttpResponse
        @param response: The response to be decoded.
        """

        # start the valid charset flag
        valid_charset = False

        # in case there is no valid charset defined
        if not valid_charset:
            # sets the default content type charset
            content_type_charset = DEFAULT_CHARSET

        # retrieves the received message value
        received_message_value = response.received_message

        # decodes the message value into unicode using the given charset
        response.received_message = received_message_value.decode(content_type_charset)

    def retrieve_data(self, response_timeout = RESPONSE_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.http_connection.setblocking(0)

            # runs the select in the http connection, with timeout
            selected_values = select.select([self.http_connection], [], [], response_timeout)

            # sets the connection to blocking mode
            self.http_connection.setblocking(1)
        except:
            raise main_client_http_exceptions.ResponseClosed("invalid socket")

        if selected_values == ([], [], []):
            self.http_connection.close()
            raise main_client_http_exceptions.ClientResponseTimeout("%is timeout" % response_timeout)
        try:
            # receives the data in chunks
            data = self.http_connection.recv(chunk_size)
        except:
            raise main_client_http_exceptions.ServerResponseTimeout("timeout")

        # returns the data
        return data

    def _parse_url(self, url):
        """
        Parses the url, retrieving a tuple structure containing
        the protocol, the host, the port an the path for the given url.

        @type url: String
        @param url: The url to be parsed.
        @rtype: Tuple
        @return: A tuple containing the protocol, the host, the port
        and the path.
        """

        # retrieves the url parser plugin
        url_parser_plugin = self.main_client_http.main_client_http_plugin.url_parser_plugin

        # parses the url retrieving the structure
        url_structure = url_parser_plugin.parse_url(url)

        if url_structure.protocol:
            protocol = url_structure.protocol.lower()
        else:
            # raises the http invalid url data exception
            raise main_client_http_exceptions.HttpInvalidUrlData("missing protocol information: " + url)

        if url_structure.base_name:
            host = url_structure.base_name
        else:
            # raises the http invalid url data exception
            raise main_client_http_exceptions.HttpInvalidUrlData("missing host information: " + url)

        if url_structure.port:
            port = url_structure.port
        else:
            port = PROTOCOL_DEFAULT_PORT_MAP.get(protocol, None)

        if url_structure.resource_reference:
            path = url_structure.resource_reference
        else:
            path = "/"

        # returns the tuple containing the protocol, the host, the port
        # and the path of the url
        return (protocol, host, port, path)

class HttpRequest:
    """
    The http request class.
    """

    host = "none"
    """ The host value """

    port = None
    """ The port value """

    operation_type = "none"
    """ The operation type """

    path = "none"
    """ The path """

    arguments = "none"
    """ The arguments """

    protocol_version = "none"
    """ The protocol version """

    attributes_map = {}
    """ The attributes map """

    headers_map = {}
    """ The headers map """

    content_type = None
    """ The content type """

    message_stream = None
    """ The message stream """

    content_type_charset = None
    """ The content type charset """

    def __init__(self, host = "none", port = None, path = "none", attributes_map = {}, operation_type = GET_METHOD_VALUE, protocol_version = HTTP_1_1_VERSION, content_type_charset = DEFAULT_CHARSET):
        self.host = host
        self.port = port
        self.path = path
        self.attributes_map = attributes_map
        self.operation_type = operation_type
        self.protocol_version = protocol_version
        self.content_type_charset = content_type_charset

        self.headers_map = {}
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()

    def get_result(self):
        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # encodes the attributes
        encoded_attributes = self._encode_attributes()

        # sets the initial path
        path = self.path

        # in case the encoded attributes string
        # is valid and not empty
        if encoded_attributes:
            # in case the operation is of type get
            if self.operation_type == GET_METHOD_VALUE:
                # in case no exclamation mark exists in
                # the path
                if self.path.find("?") == -1:
                    path = self.path + "?" + encoded_attributes
                else:
                    path = self.path + "&" + encoded_attributes
            # in case the operation is of type post
            elif self.operation_type == POST_METHOD_VALUE:
                # writes the encoded attributes into the message stream
                self.message_stream.write(encoded_attributes)

                # sets the response content type
                self.content_type = "application/x-www-form-urlencoded"

        # retrieves the real host value
        real_host = self._get_real_host()

        # retrieves the result string value
        message = self.message_stream.get_value()

        # retrieves the content length from the
        # message content itself
        content_length = len(message)

        # writes the http command in the string buffer (version, status code and status value)
        result.write(self.operation_type + " " + path + " " + self.protocol_version + "\r\n")

        # in case there is a content type defined
        if self.content_type:
            result.write(CONTENT_TYPE_VALUE + ": " + self.content_type + "\r\n")

        # in case the content length is valid
        if content_length > 0:
            result.write(CONTENT_LENGTH_VALUE + ": " + str(content_length) + "\r\n")

        result.write(HOST_VALUE + ": " + real_host + "\r\n")
        result.write(USER_AGENT_VALUE + ": " + USER_AGENT_IDENTIFIER + "\r\n")

        # iterates over all the header values to be sent
        for header_name, header_value in self.headers_map.items():
            # writes the extra header value in the result
            result.write(header_name + ": " + header_value + "\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write("\r\n")
        result.write(message)

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def _get_real_host(self):
        """
        Retrieves the "real" host value to be sent
        in http header of the request.

        @rtype: String
        @return: The "real" host value.
        """

        # in case the port is defined
        if self.port:
            # returns the host appended with the port value
            return self.host + ":" + str(self.port)
        # in case the port is not defined
        else:
            # returns only the host
            return self.host

    def _quote(self, string_value, safe = "/"):
        """
        Quotes the given string value according to
        the url encoding specification.
        The implementation is based on the python base library.

        @type string_value: String
        @param string_value: The string value to be quoted.
        @rtype: String
        @return: The quoted string value.
        """

        # creates the cache key tuple
        cache_key = (safe, QUOTE_SAFE_CHAR)

        try:
            # in case the cache key is not defined
            # in the quote sage maps creates a new entry
            safe_map = QUOTE_SAFE_MAPS[cache_key]
        except KeyError:
            # adds the "base" quote safe characters to the
            # "safe list"
            safe += QUOTE_SAFE_CHAR

            # starts the safe map
            safe_map = {}

            # iterates over all the ascii values
            for index in range(256):
                # retrieves the character for the
                # given index
                character = chr(index)

                # adds the "valid" character ot the safe mao entry
                safe_map[character] = (character in safe) and character or ("%%%02X" % index)

            # sets the safe map in the cache quote safe maps
            QUOTE_SAFE_MAPS[cache_key] = safe_map

        # maps the getitem method of the map to all the string
        # value to retrieve the valid items
        resolution_list = map(safe_map.__getitem__, string_value)

        # joins the resolution list to retrieve the quoted value
        return "".join(resolution_list)

    def _quote_plus(self, string_value, safe = ""):
        """
        Quotes the given string value according to
        the url encoding specification. This kind of quote
        takes into account the plus and the space relation.
        The implementation is based on the python base library.

        @type string_value: String
        @param string_value: The string value to be quoted.
        @rtype: String
        @return: The quoted string value.
        """

        # in case there is at least one white
        # space in the string value
        if " " in string_value:
            # quotes the string value adding the white space
            # to the "safe list"
            string_value = self._quote(string_value, safe + " ")

            # replaces the white spaces with plus signs and
            # returns the result
            return string_value.replace(" ", "+")

        # returns the quoted string value
        return self._quote(string_value, safe)

    def _encode_attributes(self):
        """
        Encodes the current attributes into url encoding.

        @rtype: String
        @return: The encoded parameters.
        """

        # creates a string buffer to hold the encoded attribute values
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # sets the is first flag
        is_first = True

        # iterates over all the attribute keys and values
        for attribute_key, attribute_value in self.attributes_map.items():
            # encodes both the attribute key and value
            attribte_key_encoded = self._encode(attribute_key)
            attribte_value_encoded = self._encode(attribute_value)

            # quotes both the attribute key and value
            attribute_key_quoted = self._quote_plus(attribte_key_encoded)
            attribute_value_quoted = self._quote_plus(attribte_value_encoded)

            # in case it's is the first iteration
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # writes the and continuation in the string buffer
                string_buffer.write("&")

            # adds the quoted key and value strings to the
            # string buffer
            string_buffer.write(attribute_key_quoted)
            string_buffer.write("=")
            string_buffer.write(attribute_value_quoted)

        # retrieves the encoded attributes from the string buffer
        encoded_attributes = string_buffer.get_value()

        # returns the encoded attributes
        return encoded_attributes

    def _encode(self, string_value):
        """
        Encodes the given string value to the current encoding.

        @type string_value: String
        @param string_value: The string value to be encoded.
        @rtype: String
        @return: The given string value encoded in the current encoding.
        """

        return unicode(string_value).encode(self.content_type_charset)

class HttpResponse:
    """
    The http response class.
    """

    request = None
    """ The request that originated the response """

    status_code = "none"
    """ The status code """

    protocol_version = "none"
    """ The protocol version """

    headers_map = {}
    """ The headers map """

    received_message = "none"
    """ The received message """

    status_code = None
    """ The status code """

    status_message = None
    """ The status message """

    content_type_charset = None
    """ The content type charset """

    def __init__(self, request):
        """
        Constructor of the class.
        """

        self.request = request

        self.attributes_map = {}
        self.headers_map = {}
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()

    def set_protocol_version(self, protocol_version):
        """
        Sets the protocol version.

        @type protocol_version: String
        @param protocol_version: The protocol version.
        """

        self.protocol_version = protocol_version

    def set_status_code(self, status_code):
        """
        Sets the status code.

        @type status_code: int
        @param status_code: The status code.
        """

        self.status_code = status_code

    def set_status_message(self, status_message):
        """
        Sets the status message.

        @type status_message: String
        @param status_message: The status message.
        """

        self.status_message = status_message
