import os


class Config:
    SECRET_KEY = "dev-local-only-not-for-deployment"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_db_uri(instance_path):
        db_path = os.path.join(instance_path, "inventory.db")
        return "sqlite:///" + db_path
