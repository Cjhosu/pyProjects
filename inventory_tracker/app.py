import os

from flask import Flask
from sqlalchemy import inspect, text

from config import Config
from extensions import db
from routes import register_blueprints


def _add_missing_columns(app):
    """Adds columns that a model gained after the table already existed,
    without dropping/recreating the table (so existing data survives).
    create_all() only creates missing tables, not missing columns on
    existing ones, so this fills that gap for a solo local app where a
    full migration tool (Flask-Migrate/Alembic) would be overkill."""
    import models  # noqa: F401  (ensures models are registered on the metadata)

    inspector = inspect(db.engine)
    for table in db.metadata.tables.values():
        if table.name not in inspector.get_table_names():
            continue
        existing_columns = {col["name"] for col in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing_columns:
                continue
            column_type = column.type.compile(db.engine.dialect)
            with db.engine.begin() as conn:
                conn.execute(
                    text(
                        "ALTER TABLE {} ADD COLUMN {} {}".format(
                            table.name, column.name, column_type
                        )
                    )
                )
                # SQLite's ADD COLUMN always creates a nullable column
                # regardless of the model's nullable=False, so existing
                # rows get NULL here. Backfill with the model's scalar
                # default so they match what a fresh row would get.
                has_scalar_default = (
                    column.default is not None and not column.default.is_callable
                )
                if not column.nullable and has_scalar_default:
                    conn.execute(
                        text(
                            "UPDATE {} SET {} = :default WHERE {} IS NULL".format(
                                table.name, column.name, column.name
                            )
                        ),
                        {"default": column.default.arg},
                    )


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.init_db_uri(app.instance_path)

    db.init_app(app)
    register_blueprints(app)

    with app.app_context():
        import models  # noqa: F401  (ensures models are registered before create_all)

        db.create_all()
        _add_missing_columns(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
