"""
Image Hosting HTTP Request Handler Module

This module implements the `ImageHostingHttpRequestHandler` class, which facilitates handling HTTP requests for an
image hosting server. It provides methods for managing image files, including retrieving, uploading, and deleting images,
as well as maintaining specific request routes.

Key Features:
- HTTP route management for GET, POST, and DELETE requests.
- Image retrieval by individual image or count.
- Support for file uploads.
- Image deletion functionality.

Classes:
----------
- ImageHostingHttpRequestHandler:
"""
import os
from uuid import uuid4

from loguru import logger

from DB_Manager import DBManager
from adv_http_request_handler import AdvancedHttpRequestHandler
from settings import IMAGES_PATH, MAX_FILE_SIZE, \
    ALLOWED_EXTENSIONS, PAGE_LIMIT, ERROR_FILE


class ImageHostingHttpRequestHandler(AdvancedHttpRequestHandler):

    server_version = 'Image Hosting Server v1.0'

    def __init__(self, request, client_address, server):
        """
        Initialize the HTTP request handler with required configurations.
        Parameters:
        request (bytes): The raw HTTP request.
        client_address (tuple): The client address.
        server (HTTPServer): The HTTP server instance.
        """
        self.get_routes = {
            '/api/images/': self.get_images,
            '/api/images_count/': self.get_images_count
        }
        self.post_routes = {
            '/upload/': self.post_upload
        }
        self.delete_routes = {
            '/api/delete/': self.delete_image
        }
        super().__init__(request, client_address, server)


    def get_images(self):
        """
        Retrieves a paginated list of image records from the database,
        formats them into a JSON-compatible response structure,
        and sends it as a JSON response.
        If no images are available, an empty list is returned

        :param self: The instance of the class that calls this method.
        :return: List of images in JSON format.
            Each image contains the following:
            - filename: The name of the file stored in the system.
            - original_name: The original name of the file when uploaded.
            - size: Size of the file.
            - upload_time: The upload timestamp.
            - file_type: The MIME type or type of the file.
        """
        page = self.headers.get('Page')
        logger.info(f'Page: {page}')
        query = (f"SELECT * FROM images ORDER BY upload_time DESC"
                 f" LIMIT {PAGE_LIMIT} OFFSET {(int(page) - 1) * PAGE_LIMIT};")
        logger.info(f'Query: {query}')
        images = DBManager().execute_fetch_query(query)
        if not images:
            return self.send_json({'images': []})

        to_json_images = []
        for image in images:
            to_json_images.append({
                'filename': image[1],
                'original_name': image[2],
                'size': image[3],
                'upload_time': image[4].strftime('%Y-%m-%d %H:%M:%s'),
                'file_type': image[5]
            })
        self.send_json({
            'images': to_json_images
        })


    def get_images_count(self):
        """
        Fetches and logs the total number of images from the database, then sends the count
        as a JSON response.

        :raises Exception: If querying the database or sending the JSON response fails.
        :return: None
        """
        count = DBManager().execute_fetch_query('SELECT COUNT(*) FROM '
                                                'images;')[0][0]
        logger.info('Count: ' + str(count))
        self.send_json({'count': count})


    def post_upload(self):
        """
        Handle POST requests for uploading images.
        Validates the file size and type before saving it to the server.
        """

        length = int(self.headers.get('Content-Length'))
        if length > MAX_FILE_SIZE:
            logger.warning('File too large')
            self.send_html(ERROR_FILE, 413)
            return

        data = self.rfile.read(length)
        orig_filename = self.headers.get('Filename')
        _, ext = os.path.splitext(orig_filename)
        image_id = uuid4()
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning('File type not allowed')
            self.send_html(ERROR_FILE, 400)
            return
        DBManager().execute_query(
            f"INSERT INTO images (filename, original_name, size, file_type) "
            f"VALUES ('{image_id}', '{orig_filename}', {length}, '{ext}');"
        )
        with open(IMAGES_PATH + f'{image_id}{ext}', 'wb') as file:
            file.write(data)
        self.send_html('upload_success.html', headers={
                'Location': f'http://localhost/{IMAGES_PATH}{image_id}{ext}'})

    def delete_image(self):
        """
        Deletes an image file from the server and its corresponding database record.

        This function handles the deletion of a specified image based on the filename
        provided in the HTTP headers. If the filename is missing, the file doesn't
        exist, or the deletion fails for any reason, appropriate logging and error
        responses are generated. Successful operations also update the database to
        remove the associated entry.

        :raises ValueError: If no filename is provided in the headers.
        :raises FileNotFoundError: If the file does not exist in the specified directory.

        :return: A JSON response confirming successful deletion if operation is
            completed without issues.
        """
        full_filename = self.headers.get('Filename')
        if not full_filename:
            logger.warning('No filename provided')
            self.send_html(ERROR_FILE, 404)
            return

        filename, _ = os.path.splitext(full_filename)
        image_path = IMAGES_PATH + full_filename
        if not os.path.exists(image_path):
            logger.warning('Image not found')
            self.send_html(ERROR_FILE, 404)
            return

        os.remove(image_path)
        DBManager().execute_query(
            f"DELETE FROM images WHERE filename = '{filename}';")
        self.send_json({'Success': 'Image deleted'})



