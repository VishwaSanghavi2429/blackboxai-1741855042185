import os
from datetime import timedelta

class Config:
    # Application Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Excel File Paths
    EXCEL_DIR = 'data'
    USERS_EXCEL = os.path.join(EXCEL_DIR, 'users.xlsx')
    APPOINTMENTS_EXCEL = os.path.join(EXCEL_DIR, 'appointments.xlsx')
    
    # OTP Configuration
    OTP_EXPIRY = timedelta(minutes=5)
    
    # Company Information
    COMPANY_NAME = "WebbyTouch Infotech"
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Ensure Excel directory exists
    @staticmethod
    def init_app(app):
        os.makedirs(Config.EXCEL_DIR, exist_ok=True)
