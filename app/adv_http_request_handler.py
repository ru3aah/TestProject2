"""
AdvancedHTTPRequestHandler is a class that handles HTTP requests and
responses. It provides methods to send HTML and JSON responses and
is used to handle GET, POST, and DELETE requests.

"""
import json
from http.server import BaseHTTPRequestHandler

from loguru import logger

from Router import Router
from settings import STATIC_PATH, LOG_PATH, LOG_FILE

logger.add(LOG_PATH + LOG_FILE,
           format='[{time:YYYY-MM-DD HH:mm:ss}] {level}: {message}',
           level='INFO')


class AdvancedHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP requests and responses with advanced functionalities.

    Extends BaseHTTPRequestHandler to provide
    enhanced handling of requests and responses.

    :ivar default_response: A lambda function used to send a 404 HTML response
                            when no handler is found for a request.
    :type default_response: Callable[[], None]
    :ivar router: An instance of the Router class used to resolve request paths
                and determine appropriate handlers.
    :type router: Router
    """
    def __init__(self, request, client_address, server):
        self.default_response = lambda: self.send_html('404.html', 404)
        self.router = Router()
        super().__init__(request, client_address, server)

    def send_html(self, file, code=200, headers=None, file_path=STATIC_PATH):
        """
        Sends an HTML file as an HTTP response to the client.
        The response includes a status code, headers, and the contents
        of the specified HTML file.

        :param file: Name of the HTML file to be sent as the response body.
        :type file: str
        :param code: HTTP status code to be sent in the response.
                        Defaults to 200.
        :type code: int, optional
        :param headers: Additional headers to include in the response.
                        There Should be a dictionary where keys are header names
                        and values are header values. Defaults to None.
        :type headers: dict, optional
        :param file_path: Directory path where the specified HTML file
                            is located. Default to STATIC_PATH.
        :type file_path: str, optional
        :return: None
        """
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        with open(file_path + file, 'rb') as file:
            self.wfile.write(file.read())

    def send_json(self, response: dict, code=200, headers=None):
        """
        Send a JSON response to the client. This method sets the response code,
        adds the required headers, and writes the JSON-encoded response body
        to the output stream.

        :param response: The JSON-serializable dictionary object to
            send as the response body.
        :type response: dict
        :param code: The HTTP status code for the response (default is 200).
        :type code: int, optional
        :param headers: Additional headers to include in the response.
                Each key-value pair in the dictionary represents a header
                and its value.
        :type headers: dict, optional
        :return: None
        """
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_request(self, method):
        """
        Executes an HTTP request by resolving the method and path
        against the router.

        If a corresponding handler is found, it is invoked with the resolved
        parameters. If no handler is found, a default response is returned.

        :param method: The HTTP method for the incoming request.
        :type method: str
        :return: None
        """
        logger.info(f'{method} {self.path}')
        handler, params = self.router.resolve(method, self.path)
        if handler:
            handler(self, **params)
        else:
            self.default_response()

    def do_GET(self):
        """
        Handles HTTP GET requests by delegating the logic
        to a shared request handling function ``do_request`` function.

        :param self:

        :return: None
        """
        self.do_request('GET')

    def do_POST(self):
        """
        Handles HTTP POST requests by delegating the logic to the `do_request`
        function.

        :param self: Instance of the HTTP request handler.
        :return: None
        """
        self.do_request('POST')

    def do_DELETE(self):
        """
        Handles HTTP DELETE requests
        by invoking a generic HTTP request handler for the DELETE method.

        :raises Exception: If the underlying request handling process
                            encounters errors.

        :return: None
        """
        self.do_request('DELETE')