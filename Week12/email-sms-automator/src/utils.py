import logging
import os
from dotenv import load_dotenv

# โหลดข้อมูลจากไฟล์ .env
load_dotenv()

# ตั้งค่า Logging พื้นฐาน
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_logging(name, level=logging.INFO):
    """สร้าง Logger สำหรับแต่ละโมดูล"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def get_env_variable(var_name):
    """ดึงค่า Environment variable หากไม่มีจะแจ้ง Error"""
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not set. Please check your .env file.")
    return value

def ensure_directory_exists(path):
    """ตรวจสอบและสร้างโฟลเดอร์หากยังไม่มี"""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory ensured: {path}")
    except OSError as e:
        logging.error(f"Error creating directory {path}: {e}")
        raise