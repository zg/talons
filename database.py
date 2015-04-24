# database.py - creates the database session, declares Base object, defines init_db()
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite:///jobstore.db',
                       poolclass=StaticPool,
                       connect_args={'check_same_thread':False},
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
db_session.execute("PRAGMA journal_mode = DELETE")
db_session.execute("PRAGMA synchronous = OFF")
db_session.execute("PRAGMA temp_store = MEMORY")
db_session.execute("PRAGMA cache_size = 500000")
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
