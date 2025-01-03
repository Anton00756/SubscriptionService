from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from settings import settings
from dotenv import load_dotenv
import os
# Настройте строку подключения к базе данных
load_dotenv()
DATABASE_URL = str(os.getenv("DB_URL",""))  

# Создаём движок базы данных
engine = create_engine(DATABASE_URL)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()