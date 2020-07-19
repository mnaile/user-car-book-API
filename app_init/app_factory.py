from flask import Flask
from extensions.extensions import db,ma,migrate
import os

settings = {
    "dev" : "settings.devsettings.DevelopSettings",
    "prod" : "settings.prodsettings.ProdSettings"
}

def get_settings(settings_name):
    if settings.get(settings_name):
        return settings.get(settings_name)
    return Exception("Setting name you select %s isn't supported" % settings_name)

def create_app(settings_name):
    app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"]="postgres:///caruserdb"
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app,db)
    settings_obj = get_settings(settings_name)
    app.config.from_object(settings_obj)

    ctx = app.app_context()
    ctx.push()

    

    return app