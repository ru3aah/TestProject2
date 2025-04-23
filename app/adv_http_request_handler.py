import json
from http.server import BaseHTTPRequestHandler

from loguru import logger

from settings import LOG_FILE, LOG_PATH, STATIC_PATH

logger.add(LOG_PATH + LOG_FILE,
           format='[{time:YY-MM-DD HH:mm:ss}] {level}: {message}',
           level='INFO')

class AdvancedHttpRequestHandler(BaseHTTPRequestHandler):
    """
    A custom HTTP request handler
    """

    def __init__(self, request, client_address, server):
        """
        Initializes  HTTP request handler with required configurations.
        Parameters:
        request (bytes): raw HTTP request.
        client_address (tuple): client address.
        server (HTTPServer): HTTP server instance.
        """
        self.default_response = lambda: self.send_html('404.html', 404)
        super().__init__(request, client_address, server)


    def send_html(self, file_name, code=200, headers=None,
                  file_path = STATIC_PATH):
        """
        Sends an HTML response using a static file.
        Parameters:
            file_name (str): HTML file name to be sent.
            code (int): HTTP status code for the response. Defaults to 200.
            headers (dict): Additional HTTP headers to include in the response.
            file_path (str): Path to the HTML files.
        """
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        with open(file_path + file_name, 'rb') as file:
            self.wfile.write(file.read())


    def send_json(self, response: dict, code=200, headers=None):
        """
        Send a JSON response to the client.
        Parameters:
        :param response: The dictionary containing the JSON.
        :param code: The HTTP status code for the response. Defaults to 200.
        :param headers: Optional headers to be included in the response.
                Should be a dictionary where the key is the header name
                and the value is the corresponding value.
        :return: None
        """
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))


    def do_GET(self):
        """
        Handle incoming GET requests by routing them to the appropriate handler.
        """
        logger.info(f'GET {self.path}')
        self.get_routes.get(self.path, self.default_response)()


    def do_POST(self):
        """
        Handle incoming POST requests by routing them to the appropriate handler.
        """
        logger.info(f'POST {self.path}')
        self.post_routes.get(self.path, self.default_response)()


    def do_DELETE(self):
        """
        Handles incoming DELETE requests
        """
        logger.info(f'DELETE {self.path}')
        self.delete_routes.get(self.path, self.default_response)()