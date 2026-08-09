class Config:
    SECRET_KEY = "digiteacher-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:123456@localhost/digiteacher"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False