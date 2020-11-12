from ...extensions import migrate, db

def initialize_extensions(app, extensions):
    for extension in extensions:
        extension.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
