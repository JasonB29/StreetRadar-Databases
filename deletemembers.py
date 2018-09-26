from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sr_db_setup import Member, Locations, Base

engine = create_engine('sqlite:///streetradar.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

memberdelete = session.query(Member).all()
for member in memberdelete:
    if member.id > 4:
        session.delete(member)
        session.commit()
    else:
        print member.username
        


locationdelete = session.query(Locations).all()
for location in locationdelete:
    if location.id > 4:
        session.delete(location)
        session.commit()
    else:
        print location.id