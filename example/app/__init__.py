from deez import Deez
from deez.urls import path

from .resources import IndexResource


def get_application() -> Deez:
    """
    Setup and return the application
    """
    app = Deez()
    app.register_routes(
        [
            path("/", IndexResource),
        ]
    )
    return app
