import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

raw_password = "jayant@@sharma"

encoded_password = urllib.parse.quote_plus(raw_password)

db_url = f"mysql+pymysql://root:{encoded_password}@localhost:3306/taskflow"


engine = create_engine(db_url, pool_pre_ping=True)

session = sessionmaker(bind = engine,autocommit=False, autoflush=False)

