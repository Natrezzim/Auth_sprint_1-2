import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.datastore.token_datastore import TokenDataStore
from data.db.db_models import Users

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTk1MmE2M2QtMDEwNy00Y2NmLTg4N2QtZTc3NzUxOGVjZDcwIiwidXNlcm5hbWUiOiJ0ZXN0IiwicGFzc3dvcmQiOiJ0ZXN0MTIzIiwiZXhwaXJlcyI6IjIwMjItMDUtMDdUMTc6MzE6NTIiLCJ0eXBlIjoiYWNjZXNzIiwiaXNfYWRtaW5pc3RyYXRvciI6ZmFsc2V9.CvakkJX3ZMqLl7AXNx98pnGZF00ZahoEu4IWAdQpl20'
SECRET_KEY='t1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'

@contextmanager
def session_db():
    engine = create_engine("postgresql://app:123qwe@localhost:5432/auth_database")
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


token_data = TokenDataStore.get_user_data_from_token(token=token, secret_key=SECRET_KEY)

with session_db() as s:
    check_user = s.query(Users).filter_by(id=token_data['user_id']).one_or_none()
