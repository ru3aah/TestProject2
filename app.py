from http.server import HTTPServer, BaseHTTPRequestHandler

SERVER_ADDRESS = ('localhost', 8000)


class ImageHostingHTTPRequestHandler(BaseHTTPRequestHandler):
    #handls all GET requests
    server_version = 'Image Hosting Server v0.1'

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Hello, world!</h1>")


# noinspection PyTypeChecker
def run(server_class=HTTPServer, handler_class=ImageHostingHTTPRequestHandler):
    httpd = server_class(SERVER_ADDRESS, handler_class)
    print(f'Server is running at {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt received, exiting.')
        httpd.server_close()
    finally:
        print('Server has been shut down.')



if __name__ == '__main__':
        run()
