from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = "postgresql://postgresUser:postgresPW@localhost/TodoApplicationDatabase"
SQLALCHEMY_DATABASE_URL = "postgresql://cuulicqp:y5ggwhZWuCQM32zb3ZhooLP-Gc65pevh@mahmud.db.elephantsql.com/cuulicqp"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

