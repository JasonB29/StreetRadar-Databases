from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from sr_db_setup import Member, Locations, LocationHistory, Base

engine = create_engine('sqlite:///streetradar.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# entries

    #id = Column(Integer, primary_key=True)
    #member_id = Column(Integer, ForeignKey('member_table.id'))
    #location_id = Column(String(80), nullable = False)
    #datetime = Column(DateTime(timezone = True), server_default=func.now())
    #ChIJ7XpC434LdkgReSvNuiQdzf0, ChIJYbo31oELdkgRGK0eIWXakFQ, ChIJr2RySocLdkgRUV2E_xLJGx, "Tue, 12 Jun 2018 21:02:00 GMT")



history2 = LocationHistory(member_id = 2, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 21, 30, 10))
session.add(history2)
session.commit()

history3 = LocationHistory(member_id = 3, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 21, 30, 10))
session.add(history3)
session.commit()

history4 = LocationHistory(member_id = 4, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 21, 30, 10))
session.add(history4)
session.commit()

history5 = LocationHistory(member_id = 5, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 20, 30, 10))
session.add(history5)
session.commit()

history6 = LocationHistory(member_id = 6, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 20, 30, 10))
session.add(history6)
session.commit()

history7 = LocationHistory(member_id = 7, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 19, 30, 10))
session.add(history7)
session.commit()

history8 = LocationHistory(member_id = 8, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 19, 30, 10))
session.add(history8)
session.commit()

history9 = LocationHistory(member_id = 9, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 18, 30, 10))
session.add(history9)
session.commit()

history10 = LocationHistory(member_id = 10, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 18, 30, 10))
session.add(history10)
session.commit()

#

history11 = LocationHistory(member_id = 1, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 18, 30, 10))
session.add(history11)
session.commit()

history12 = LocationHistory(member_id = 2, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 18, 30, 10))
session.add(history12)
session.commit()

history13 = LocationHistory(member_id = 3, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 12, 18, 30, 10))
session.add(history13)
session.commit()

history14 = LocationHistory(member_id = 4, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 13, 19, 00, 10))
session.add(history14)
session.commit()

history15 = LocationHistory(member_id = 5, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 13, 19, 00, 10))
session.add(history15)
session.commit()

history16 = LocationHistory(member_id = 6, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 13, 19, 00, 10))
session.add(history16)
session.commit()

history17 = LocationHistory(member_id = 7, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 13, 19, 00, 10))
session.add(history17)
session.commit()

history18 = LocationHistory(member_id = 8, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 14, 21, 30, 10))
session.add(history18)
session.commit()

history19 = LocationHistory(member_id = 9, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 14, 21, 30, 10))
session.add(history19)
session.commit()

history20 = LocationHistory(member_id = 10, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 14, 21, 30, 10))
session.add(history20)
session.commit()


history21 = LocationHistory(member_id = 8, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 14, 21, 30, 10))
session.add(history21)
session.commit()

history22 = LocationHistory(member_id = 9, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 14, 21, 30, 10))
session.add(history22)
session.commit()

history23 = LocationHistory(member_id = 10, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 14, 21, 30, 10))
session.add(history23)
session.commit()
history24 = LocationHistory(member_id = 8, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 14, 21, 30, 10))
session.add(history24)
session.commit()

history25 = LocationHistory(member_id = 9, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 15, 21, 30, 10))
session.add(history25)
session.commit()

history26 = LocationHistory(member_id = 10, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 15, 21, 30, 10))
session.add(history26)
session.commit()

history27 = LocationHistory(member_id = 8, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 15, 21, 30, 10))
session.add(history27)
session.commit()

history28 = LocationHistory(member_id = 9, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 16, 21, 30, 10))
session.add(history28)
session.commit()

history29 = LocationHistory(member_id = 10, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 16, 21, 30, 10))
session.add(history29)
session.commit()

history30 = LocationHistory(member_id = 10, location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", datetime = datetime(2018, 6, 16, 21, 30, 10))
session.add(history30)
session.commit()