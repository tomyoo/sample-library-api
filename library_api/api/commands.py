import click
from flask.cli import with_appcontext

from ..extensions import db


@click.command()
@with_appcontext
def create_tables():  # pragma: no cover
    db.create_all()


def register_commands(app):
    app.cli.add_command(create_tables)
