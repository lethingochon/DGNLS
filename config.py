import os

class Config:
    SECRET_KEY = "digiteacher-secret-key"
    
    # Khôi phục nguyên bản kết nối MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost/dgnls'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False