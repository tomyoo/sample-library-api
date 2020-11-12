from flask import Flask

from .initialize_extensions import initialize_extensions
from .register_blueprints import register_blueprints
from library_api.extensions import schemas, db


def create_app(package_name, package_path, settings_override=None,
               extensions=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for this application.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary or path to file of settings to
        override
    :param extensions: an array of instances of additional extensions to
        initialize on the app
    """
    app = Flask(package_name)
    # Load environment specific configuration
    app.config.from_pyfile('settings.py')

    if isinstance(settings_override, str):  # pragma: no cover
        app.config.from_pyfile(settings_override, silent=True)
    elif isinstance(settings_override, dict):
        app.config.update(settings_override)

    register_blueprints(app, package_name, package_path)

    initialize_extensions(app, [db, schemas])
    initialize_extensions(app, extensions)

    return app
