from flask.cli import with_appcontext
from back_apps.setting_web import db, flask_app
import click


@click.command(name='create_db')
@with_appcontext
def create_db():
    #db.drop_all()
    db.init_app(flask_app)
    db.create_all()
    #db.session.commit()