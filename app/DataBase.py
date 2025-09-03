from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


sql_url = 'postgresql://username:password@localhost:5432/ECOMDB'
engine  = create_engine(sql_url,echo = True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  