from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sr_db_setup import Member, Locations, Base

engine = create_engine('sqlite:///streetradar.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# "Under 18", "18 - 24", "25 - 30", "31 - 40", "40+"
# "Male", "Female", "Prefer Not To Say"
# "Single", "Dating", "Married"


# Add members to the database

member1 = Member(username = "Kane" ,age = "Under 18",gender = "Male",relationship_status = "Single")
session.add(member1)
session.commit()

member2 = Member(username = "Sterling" ,age = "Under 18",gender = "Male",relationship_status = "Single")
session.add(member2)
session.commit()

member3 = Member(username = "Trippier" ,age = "18 - 24",gender = "Male",relationship_status = "Single")
session.add(member3)
session.commit()

member4 = Member(username = "Young" ,age = "18 - 24",gender = "Male",relationship_status = "Single")
session.add(member4)
session.commit()

member5 = Member(username = "Henderson" ,age = "Under 18",gender = "Male",relationship_status = "Single")
session.add(member5)
session.commit()

member6 = Member(username = "Dele" ,age = "Under 18",gender = "Male",relationship_status = "Single")
session.add(member6)
session.commit()

member7 = Member(username = "Lingard" ,age = "18 - 24",gender = "Male",relationship_status = "Single")
session.add(member7)
session.commit()

member8 = Member(username = "Stones" ,age = "25 - 30",gender = "Male",relationship_status = "Single")
session.add(member8)
session.commit()

member9 = Member(username = "Maguire" ,age = "25 - 30",gender = "Male",relationship_status = "Single")
session.add(member9)
session.commit()

member10 = Member(username = "Walker" ,age = "25 - 30",gender = "Male",relationship_status = "Single")
session.add(member10)
session.commit()

member11 = Member(username = "Pickford" ,age = "25 - 30",gender = "Female",relationship_status = "Dating")
session.add(member11)
session.commit()

member12 = Member(username = "Southgate" ,age = "25 - 30",gender = "Female",relationship_status = "Dating")
session.add(member12)
session.commit()

member13 = Member(username = "Rashford" ,age = "25 - 30",gender = "Female",relationship_status = "Dating")
session.add(member13)
session.commit()

member14 = Member(username = "Dier" ,age = "31 - 40",gender = "Female",relationship_status = "Dating")
session.add(member14)
session.commit()

member15 = Member(username = "Rose" ,age = "31 - 40",gender = "Female",relationship_status = "Dating")
session.add(member15)
session.commit()

member16 = Member(username = "Butland" ,age = "31 - 40",gender = "Female",relationship_status = "Dating")
session.add(member16)
session.commit()

member17 = Member(username = "Mbappe" ,age = "18 - 24",gender = "Prefer Not To Say",relationship_status = "Dating")
session.add(member17)
session.commit()

member18 = Member(username = "Giroud" ,age = "31 - 40",gender = "Prefer Not To Say",relationship_status = "Married")
session.add(member18)
session.commit()

member19 = Member(username = "Pele" ,age = "40+",gender = "Prefer Not To Say",relationship_status = "Married") 
session.add(member19)
session.commit()

member20 = Member(username = "Lineker" ,age = "40+",gender = "Prefer Not To Say",relationship_status = "Married")
session.add(member20)
session.commit()


# Add Member Locations 
# ChIJ7XpC434LdkgReSvNuiQdzf0, ChIJYbo31oELdkgRGK0eIWXakFQ, ChIJr2RySocLdkgRUV2E_xLJGx4
# The Teddington Arms,The King's Head, The Anglers

location1 = Locations(member_id = "5", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location1)
session.commit()

location2 = Locations(member_id = "6", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location2)
session.commit()

location3 = Locations(member_id = "7", location_id = "ChIJYbo31oELdkgRGK0eIWXakFQ", location_name = "The King's Head")
session.add(location3)
session.commit()

location4 = Locations(member_id = "8", location_id = "ChIJr2RySocLdkgRUV2E_xLJGx4", location_name = "The Anglers")
session.add(location4)
session.commit()

location5 = Locations(member_id = "9", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location5)
session.commit()

location6 = Locations(member_id = "10", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location6)
session.commit()

location7 = Locations(member_id = "11", location_id = "ChIJr2RySocLdkgRUV2E_xLJGx4", location_name = "The Anglers")
session.add(location7)
session.commit()

location8 = Locations(member_id = "12", location_id = "ChIJr2RySocLdkgRUV2E_xLJGx4", location_name = "The Anglers")
session.add(location8)
session.commit()

location9 = Locations(member_id = "13", location_id = "ChIJYbo31oELdkgRGK0eIWXakFQ", location_name = "The King's Head")
session.add(location9)
session.commit()

location10 = Locations(member_id = "14", location_id = "ChIJYbo31oELdkgRGK0eIWXakFQ", location_name = "The King's Head")
session.add(location10)
session.commit()

location11 = Locations(member_id = "15", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location11)
session.commit()

location12 = Locations(member_id = "16", location_id = "ChIJr2RySocLdkgRUV2E_xLJGx4", location_name = "The Anglers")
session.add(location12)
session.commit()

location13 = Locations(member_id = "17", location_id = "ChIJr2RySocLdkgRUV2E_xLJGx4", location_name = "The Anglers")
session.add(location13)
session.commit()

location14 = Locations(member_id = "18", location_id = "ChIJYbo31oELdkgRGK0eIWXakFQ", location_name = "The King's Head")
session.add(location14)
session.commit()

location15 = Locations(member_id = "19", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location15)
session.commit()

location16 = Locations(member_id = "20", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location16)
session.commit()

location17 = Locations(member_id = "21", location_id = "ChIJr2RySocLdkgRUV2E_xLJGx4", location_name = "The Anglers")
session.add(location17)
session.commit()

location18 = Locations(member_id = "22", location_id = "ChIJ7XpC434LdkgReSvNuiQdzf0", location_name = "The Teddington Arms")
session.add(location18)
session.commit()

location19 = Locations(member_id = "23", location_id = "ChIJYbo31oELdkgRGK0eIWXakFQ", location_name = "The King's Head")
session.add(location19)
session.commit()

location20 = Locations(member_id = "24", location_id = "ChIJr2RySocLdkgRUV2E_xLJGx4", location_name = "The Anglers")
session.add(location20)
session.commit()