from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional
import os
from dotenv import load_dotenv
Base = declarative_base()
load_dotenv()
engine: Optional[object] = None
SessionLocal: Optional[sessionmaker[Session]] = None

def init_db():
    global engine, SessionLocal

    try:
        url = os.getenv("DATABASE_URL")
        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=40,
            pool_recycle=3600,
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with engine.connect() as connection:
            db_name = connection.execute(text("SELECT DATABASE()")).scalar()
            print(f"✓ Connected to MySQL successfully! Database: {db_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to connect to MySQL: {e}")
        print("Check DATABASE_URL and MySQL availability.")
        return False
        
init_db()    
        
        
# Dependency for routes
def get_db():
    """Get database session - only works if database is configured"""
    if SessionLocal is None:
        # Try to initialize if not done yet
        if not init_db():
            raise Exception("Database not configured. Check DATABASE_URL and MySQL availability.")
    
    if SessionLocal is None:
        raise Exception("Database session could not be initialized. Check DATABASE_URL.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
