from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from django.conf import settings

def Session():
    # from aldjemy.core import get_engine
    # engine = get_engine()
    engine = create_engine(settings.DATABASE_ENGINE)
    _Session = scoped_session(sessionmaker(bind=engine))
    return _Session()