from flask import Flask, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from datetime import datetime
import time
from sqlalchemy import create_engine, func, distinct, DateTime, and_
from sqlalchemy.sql import select, extract
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.util import OrderedDict
from sr_db_setup import Base, Member, Locations, LocationHistory

engine = create_engine('sqlite:///streetradar.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# GET Request Endpoints
@app.route('/streetradar/memberlist/JSON')
def memberList():
    members = session.query(Member).all()
    return jsonify(memberList = [i.serialize for i in members])


@app.route('/streetradar/<int:member_id>/account/JSON')
def memberDetails(member_id):
    member = session.query(Member).filter_by(id = member_id).one()
    return jsonify(memberDetails =  member.serialize)

@app.route('/streetradar/locationlist/JSON')
def locationList():
    locations = session.query(Locations).all()
    return jsonify(locationList = [i.serialize for i in locations])

@app.route('/streetradar/locationquery/JSON')
def locationQuery():
    
    resultsDict = {}
    venueCount = select([Locations.location_id,Locations.location_name, func.count(Locations.location_name.distinct())])
    uniqueVenues = venueCount.group_by(Locations.location_name)
    venues = engine.execute(uniqueVenues).fetchall()
    for eachVenue in venues:
        resultsDict[eachVenue.location_id] = {}
        locationMembers = session.query(Locations).filter(Locations.location_name == eachVenue.location_name).subquery()
        queryResult = session.query(Member).join(locationMembers, Member.location)
        venueCount = queryResult.count()
        print eachVenue.location_name
        print venueCount
        dict = {'VenueCount': venueCount}
        for memberObjects in queryResult:
            for attr, value in memberObjects.__dict__.items():
                if attr == 'age':
                    if attr in dict:
                        if value in dict[attr]:
                            dict[attr][value] += 1
                        else:
                            dict[attr][value] = 1
                    else: 
                        dict[attr] = {value : 1}
                elif attr == 'gender':
                    if attr in dict:
                        if value in dict[attr]:
                            dict[attr][value] += 1
                        else:
                            dict[attr][value] = 1
                    else: 
                        dict[attr] = {value : 1}
                elif attr == 'relationship_status':
                    if attr in dict:
                        if value in dict[attr]:
                            dict[attr][value] += 1
                        else:
                            dict[attr][value] = 1
                    else: 
                        dict[attr] = {value : 1} 
                        
        
        resultsDict[eachVenue.location_id] = dict
    
    resultsDictSorted = OrderedDict(sorted(resultsDict.items(), key=lambda kv: kv[1]['VenueCount'], reverse=True))
    print resultsDictSorted
    return jsonify(resultsDictSorted)
    
@app.route('/streetradar/locationstats/JSON')
def queryLocationStats():
   # statsQuery = session.query(LocationHistory).all()
    timeCounter = {}
    timeIntervals = {}
    timeFrame = request.args.get('timeFrame', type = str)
    if timeFrame == 'day':
        statsQuery = session.query(LocationHistory).filter(extract('day', LocationHistory.datetime) == 12).all()
        for i in statsQuery:
            if i.datetime.strftime ('%Y-%m-%d %H:%M:%S') not in timeCounter:
                timeCounter[i.datetime.strftime ('%Y-%m-%d %H:%M:%S')] = 1
                timeCounter[i.datetime.strftime ('%Y-%m-%d 00:00:00')] = 0
                timeCounter[i.datetime.strftime ('%Y-%m-%d 23:59:59')] = 0
            else: 
                timeCounter[i.datetime.strftime ('%Y-%m-%d %H:%M:%S')] += 1
    print timeCounter
    for key, value in timeCounter.items():
        timeIntervals[time.mktime(datetime.strptime(key, "%Y-%m-%d %H:%M:%S").utctimetuple())] = value
        
    return jsonify(timeIntervals)


# Test LocationStats Query with Member Details for location = ChIJ7XpC434LdkgReSvNuiQdzf0
@app.route('/streetradar/locationstats/TEST')
def testLocationStats():
    resultsDict = {}
    
    locationID = "ChIJ7XpC434LdkgReSvNuiQdzf0"
    
    locationAndTimeResults = session.query(LocationHistory, Member).join(Member).filter(and_(
        LocationHistory.location_id == locationID), extract('day', LocationHistory.datetime) == 12).all()
    
    for timestamp, details in locationAndTimeResults:
        dict = {'VenueCount': 0}
        timeKey = timestamp.datetime.strftime ('%Y-%m-%d %H:%M:%S')
        if timeKey not in resultsDict:
            dict['VenueCount'] = 1         
            resultsDict[timeKey] = dict
        else:
            resultsDict[timeKey]['VenueCount'] += 1  
            
        for attr, value in details.__dict__.items():
                if attr == 'age':
                    if attr in resultsDict[timeKey]:
                        if value in resultsDict[timeKey][attr]:
                            resultsDict[timeKey][attr][value] += 1
                        else:
                            resultsDict[timeKey][attr][value] = 1
                    else: 
                        resultsDict[timeKey][attr] = {value : 1}
                elif attr == 'gender':
                    if attr in resultsDict[timeKey]:
                        if value in resultsDict[timeKey][attr]:
                            resultsDict[timeKey][attr][value] += 1
                        else:
                            resultsDict[timeKey][attr][value] = 1
                    else: 
                        resultsDict[timeKey][attr] = {value : 1}
                elif attr == 'relationship_status':
                    if attr in resultsDict[timeKey]:
                        if value in resultsDict[timeKey][attr]:
                            resultsDict[timeKey][attr][value] += 1
                        else:
                            resultsDict[timeKey][attr][value] = 1
                    else: 
                        resultsDict[timeKey][attr] = {value : 1}     
    return jsonify(resultsDict)


# POST Request Endpoints
@app.route('/streetradar/newmember/POST', methods = ['POST'])
def addMember():
    request_data = request.get_json()
    username = request_data['username']
    age = request_data['age']
    gender = request_data['gender']
    relationship = request_data['relationship_status']
    createNewMember(username, age, gender, relationship)
    updatedList = session.query(Member).all()
    return jsonify(memberList = [i.serialize for i in updatedList])

@app.route('/streetradar/<int:member_id>/editmember/POST', methods = ['POST'])
def editMember(member_id):
    request_data = request.get_json()
    itemToEdit = request_data['item_to_edit']
    itemValue = request_data['item_value']
    updateMember = session.query(Member).filter_by(id = member_id).one()
    setattr(updateMember, itemToEdit, itemValue)
    session.add(updateMember)
    session.commit()
    updatedList = session.query(Member).all()
    return jsonify(memberList = [i.serialize for i in updatedList])    


@app.route('/streetradar/<int:member_id>/location/POST', methods = ['POST'])
def addMemberLocation(member_id):
    request_data = request.get_json()
    location_id = request_data['id']
    location_name = request_data['name']
    postLocation(member_id, location_id, location_name)
    updatedLocations = session.query(Locations).all()
    return jsonify(locationsTable = [i.serialize for i in updatedLocations])




# Helper Functions

def createNewMember(username, age, gender, relationship):
    newMember = Member(username = username, age = age, gender = gender, relationship_status = relationship)
    session.add(newMember)
    session.commit()

def postLocation(member_id, location_id, location_name):
    if session.query(Locations).filter_by(member_id = member_id).first() == None:
        logLocation(member_id, location_id, location_name)
    else:
        memberNewLocation = session.query(Locations).filter_by(id = member_id).one()
        memberNewLocation.location_id = location_id
        memberNewLocation.location_name = location_name
        session.add(memberNewLocation)
        session.commit()

def logLocation(member_id, location_id, location_name):
    membersLocation = Locations(member_id = member_id, location_id = location_id, location_name = location_name)
    session.add(membersLocation)
    session.commit()
    
   

    
    


# Configuration

if __name__ == '__main__':
    app.secret_key = 'SuperSecretKey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
