from flask import Flask, request, redirect, url_for, flash, jsonify, abort, g, render_template

from datetime import datetime, timedelta
import time, random, string
from sqlalchemy import create_engine, func, distinct, DateTime, and_, asc
from sqlalchemy.sql import select, extract
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.util import OrderedDict
from sr_db_setup import Base, Member, Locations, LocationHistory


#OAuth Imports
from flask_httpauth import HTTPBasicAuth
from itsdangerous import URLSafeTimedSerializer
import json, random, string, requests
# Goolge and FB Imports
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequest
from datetime import datetime
# EMail Imports
from flask_mail import Mail, Message


auth = HTTPBasicAuth()
engine = create_engine('sqlite:///streetradar.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind = engine))
session = DBSession()
app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)

# Client IDs for OAuth
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['iosClientID']
FB_CLIENT_ID = json.loads(open('client_secretsFB.json', 'r').read())['facebook']['fb_clientID']
FB_CLIENT_SECRET = json.loads(open('client_secretsFB.json', 'r').read())['facebook']['fb_client_secret']

# Log in Helper Functions

@auth.verify_password
def verify_password(email_or_token, password):
    user_id = Member.verify_auth_token(email_or_token)
    if user_id:
        print("Token Used")
        user = session.query(Member).filter_by(id=user_id).one()
    else:
        user = session.query(Member).filter_by(email = email_or_token).first()
        print("Email Used")
        if not user or not user.verify_password(password):
            print("Access Denied")
            return False
        
    g.user = user
    print("Access Granted")
    return True

def query_DB_Token(userEmail):
    user = session.query(Member).filter_by(email = userEmail).first()
    if not user:
        user = Member(email = userEmail, email_confirmed = True, email_confirmed_on = datetime.now())
        session.add(user)
        session.commit()
    
    token = user.generate_auth_token()
    print(token)
    return jsonify({'token': token.decode('ascii')})
        
    


# Log In Endpoints
# 1. Token

@app.route('/streetradar/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


# 2. Google OAuth2.0
@app.route('/streetradar/google', methods=['POST'])
def googleLogin():
    print("google")
    client_data = request.get_json()
    idToken = client_data['idtoken']
    # Send idToken to Google for verification, signed and ClientID
    try:
        idinfo = id_token.verify_oauth2_token(idToken, googleRequest.Request(), CLIENT_ID)
        print(idinfo)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong Issuer')
        userEmail = idinfo['email']
        print(userEmail)
    except ValueError:
        pass
    
    # Check DB if member exists, register if new and/or generate new session token
    return query_DB_Token(userEmail)
    

# 3. FaceBook Login
@app.route('/streetradar/facebook', methods= ['POST'])
def facebookLogin():
    print("facebooking")
    client_data = request.get_json()
    idToken = client_data['idtoken']
    
    appLink = 'https://graph.facebook.com/oauth/access_token?client_id='+ FB_CLIENT_ID + '&client_secret=' + FB_CLIENT_SECRET + '&grant_type=client_credentials'
    # From appLink, retrieve second AccessToken ie app access_token 
    appToken = requests.get(appLink).json()['access_token']    
    
    link = 'https://graph.facebook.com/debug_token?input_token=' + idToken + '&access_token=' + appToken
    
    try:
        userID = requests.get(link).json()['data']['user_id']
        authLink = 'https://graph.facebook.com/me?fields=id,name,email&access_token=' + idToken
        
        if userID is not None:
            try:
                userEmail = requests.get(authLink).json()['email']
                userName = requests.get(authLink).json()['name']
            
            except (ValueError, KeyError, TypeError) as error:
                print("IdToken not valid")
                return error
        
    return query_DB_Token(userEmail)

#4. Login for access to DB
@app.route('/streetradar/login')
@auth.login_required
def get_memberID():
    return jsonify({'memberID': g.user.id, 'emailConfirmed': g.user.email_confirmed})

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
        print (eachVenue.location_name)
        print (venueCount)
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
    print (resultsDictSorted)
    return jsonify(resultsDictSorted)


# Test LocationStats Query with Member Details for location = ChIJ7XpC434LdkgReSvNuiQdzf0
@app.route('/streetradar/locationstats/JSON')
def locationStats():
    resultsDict = {}
    
    locationID = request.args.get('location', type = str)
    timeFrame = request.args.get('timeframe', type = str)
    startPeriod = request.args.get('start', type = float)
    endPeriod = request.args.get('end', type = float)    
    
    locationAndTimeResults = session.query(LocationHistory, Member).join(Member).filter(and_(
        LocationHistory.location_id == locationID), LocationHistory.datetime.between(datetime.fromtimestamp(startPeriod),datetime.fromtimestamp(endPeriod))).all()
    
    
    
    for timestamp, details in locationAndTimeResults:
        dict = {'VenueCount': 0}
        
        
        resultsDict[startPeriod] = dict
        resultsDict[endPeriod] = dict
        
        timeKey = time.mktime(datetime.strptime(timestamp.datetime.strftime ('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S").utctimetuple())
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
@app.route('/streetradar/registration', methods= ['POST'])
def new_member():
    request_data = request.get_json()
    password = request_data['password']
    email = request_data['email']  
    
    if email is None or password is None:
        print("Missing Fields")
        abort(400)
    
    if session.query(Member).filter_by(email = email).first() is not None:
        print("User Already Exists")
        abort(400)

    createNewMember(email, password)
    #send_confirmation_email(email)
    
    return query_DB_Token(email)    

@app.route('/streetradar/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        print("Confirmation Failed")
        return
    
    member = session.query(Member).filter_by(email=email).first()
    
    if member.email_confirmed:
        print("Member has already verified email")
    else:
        member.email_confirmed = True
        member.email_confirmed_on = datetime.now()
        session.add(member)
        session.commit()
        print("Email address has been confirmed")
        
    # Need to add code to close browser on client device or redirect to webpage.
    return redirect(url_for('get_memberID'))
    

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

def createNewMember(email, password):
    newMember = Member(email = email)
    newMember.hash_password(password)
    session.add(newMember)
    session.commit()
    return jsonify({'username': newMember.username, 'email': newMember.email, 'age': newMember.age}), 201

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
    
   
def send_confirmation_email(member_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
    confirm_url = url_for('confirm_email', token=confirm_serializer.dumps(member_email, salt='email-confirmation-salt'), _external=True)
    html = render_template('email_confirmation.html', confirm_url=confirm_url)
    send_email('Please Verify Email Address', [member_email], html)
    
def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    mail.send(msg)
   
   
   
@app.route('/streetradar/locationstats/TEST')
def testLocationStats():
    resultsDict = {}
    
    locationID = request.args.get('location', type = str)
    timeFrame = request.args.get('timeframe', type = str)
    startPeriod = request.args.get('start', type = float)
    endPeriod = request.args.get('end', type = float)
    
    locationAndTimeResults = session.query(LocationHistory, Member).join(Member).filter(and_(
        LocationHistory.location_id == locationID), LocationHistory.datetime.between(datetime.fromtimestamp(startPeriod),datetime.fromtimestamp(endPeriod))).all()
    
    
    
    for timestamp, details in locationAndTimeResults:
        dict = {'VenueCount': 0}
        #dayStart = timestamp.datetime.replace(hour= 00, minute = 00, second=00)
        #dayEnd = dayStart + timedelta(hours=24)
        #dayStartTuple = time.mktime(dayStart.utctimetuple())
        #dayEndTuple = time.mktime(dayEnd.utctimetuple())
        
        resultsDict[startPeriod] = dict
        resultsDict[endPeriod] = dict
        
        timeKey = time.mktime(datetime.strptime(timestamp.datetime.strftime ('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S").utctimetuple())
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
    
    


# Configuration

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'MasonB'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)