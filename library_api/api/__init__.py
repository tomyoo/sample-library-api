from ..extensions import schemas, migrate, db
from .commands import register_commands
from .handlers import setup_handlers
from .app_factory import create_app as factory_create_app


def create_app(settings_override=None):
    """Returns an api application instance"""
    extensions = frozenset([schemas, migrate, db])

    app = factory_create_app(__name__, __path__, settings_override, extensions)
    setup_handlers(app)
    register_commands(app)

    return app
