import sys
import os

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
# Imports for OAuth2.0 and custom OAuth
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

class Member(Base):
    __tablename__ = "member_table"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=False, index=True)
    password_hash = Column(String(64))
    username = Column(String(80), nullable = True)
    age = Column(String(50), nullable = True)
    gender = Column(String(50), nullable = True)
    relationship_status = Column(String(80), nullable = True)
    email_confirmed = Column(Boolean, nullable=True, default=False)
    email_confirmed_on = Column(DateTime, nullable=True)
    location = relationship("Locations", uselist=False, back_populates = "member")
    location_history = relationship("LocationHistory")
    #interest_one = Column(String(50), nullable = True, ForeignKey('interest_table.id'))
    #interest_two = Column(String(50), nullable = True, ForeignKey('interest_table.id'))
    #interest_three = Column(String(50), nullable = True, ForeignKey('interest_table.id'))
    #interests = relationship(Interests)
    
    # Helper Functions for Password
    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
    #604800
    def generate_auth_token(self, expiration=300):  
        s = Serializer(secret_key, expires_in=expiration)
        print("Generating Token")
        return s.dumps({'id': self.id})
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            print("Expired Token")
            return None
        except BadSignature:
            print("Invalid Token")
            return None
        user_id = data['id']
        return user_id
    
    @property
    def serialize(self):
        if self.location == None:
            locationName = "No Location Logged"
        else:
            locationName = self.location.location_name
            
        return {
            'MemberID' : self.id,
            'Username' : self.username,
            'Age' : self.age,
            'Gender' : self.gender,
            'RelationshipStatus' : self.relationship_status,
            #'Location' : locationName,
            #'Interest1' : self.interest_one,
            #'Interest2' : self.interest_two,
            #'Interest3' : self.interest_three,
            }
    
    
    
class Locations(Base):
    __tablename__ = "locations_table"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member_table.id'))
    member = relationship("Member", back_populates = "location")
    location_id = Column(String(100), nullable = False)
    location_name = Column(String(100), nullable = True)
    datetime = Column(DateTime(timezone = True), server_default=func.now())
    
    @property
    def serialize(self):
        return {
            'Member' : self.member.username,
            'MemberID' : self.member_id,
            'PlaceID' : self.location_id,
            'PlaceName' : self.location_name,
            'DateTime' : self.datetime,
            }
    

class Interests(Base):
    __tablename__ = "interest_table"
    id = Column(Integer, primary_key = True)
    category = Column(String(80), nullable = False)
    title = Column(String(80), nullable = False)
    
    
    @property
    def serialize(self):
        return {
            'InterestID' : self.id,
            'Category' : self.category,
            'Title' : self.title,
            }
   


class LocationHistory(Base):
    __tablename__ = "location_history"
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member_table.id'))
    location_id = Column(String(80), nullable = False)
    datetime = Column(DateTime(timezone = True), server_default=func.now())
    
    @property
    def serialize(self):
        return {
            'HistoryID' : self.id,
            'MemberID' : self.member_id,
            'PlaceID' : self.location_id,
            'Year' : self.datetime.year,
            'Month' : self.datetime.month,
            'Day' : self.datetime.day,
            'Time' : self.datetime.strftime ('%H:%M:%S'),
            }
    
    

engine = create_engine('sqlite:///streetradar.db')
Base.metadata.create_all(engine)