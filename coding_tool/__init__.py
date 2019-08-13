from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from coding_tool.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from coding_tool.metadata.routes import metadata
    from coding_tool.guideline.routes import guideline
    from coding_tool.sampling.routes import sampling
    from coding_tool.design.routes import exp_design
    from coding_tool.main.routes import main
    from coding_tool.measurements.routes import measurements
    from coding_tool.errors.handlers import errors
    app.register_blueprint(metadata)
    app.register_blueprint(guideline)
    app.register_blueprint(sampling)
    app.register_blueprint(exp_design)
    app.register_blueprint(main)
    app.register_blueprint(measurements)
    app.register_blueprint(errors)

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app
