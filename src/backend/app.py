import logging
import os
from contextlib import suppress

import connexion

def set_cors_headers_on_response(response):
    """Sets CORS headers on response.

    Args:
        response (flask.Response): Response object.

    Returns:
        response (flask.Response): Response object with CORS headers.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS'
    response.headers['Access-Control-Expose-Headers'] = 'X-Compression-Time, X-Compression-Rate'
    return response

def create_app(test_config=None):
    """Creates the application.
        
    Returns:
        app (connexion.App): Application object.
    """
    logging.getLogger().setLevel(logging.INFO)
    con_app = connexion.App(
        __name__,
        specification_dir='./',
        options={
            'swagger_url': '/doc/',
        },
        debug=True,
    )
    con_app.add_api('swagger.yml')
    app = con_app.app
    app.config.from_mapping(
        SECRET_KEY=os.getenv('APP_SECRET', 'dev'),
        JSON_SORT_KEYS=False,
    )
    app.after_request(set_cors_headers_on_response)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    with suppress(OSError):
        os.makedirs(app.instance_path)

    return app