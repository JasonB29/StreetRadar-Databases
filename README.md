# StreetRadar-Databases

These are python files I wrote when I was learning about the python language and how to create a database on a server. Most of the files are used to create a Postgres database and to populate it with data.

sr_endpoints.py contains the bulk of the server set up and the use of routes for the endpoints that can be consumed. This is designed as a restful service, and the endpoints are intended to be called by an ios app that uses your gps location to update the database on a member's location.
The user is also able to query the database inorder to get real-time data about a particular place, such as the number of people currently located at that location and their associated member details ie. Age-group, gender, interests...etc

This project was part of a personal project aimed at exploring server-side development coupled with IOS app development. 
