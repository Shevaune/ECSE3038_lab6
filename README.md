# ECSE3038_lab6
# Aim of Lab
This lab is meant to get students more accustomed to the technologies used in designing and implementing an embedded module as part of an IoT system and RESTful API server.
# Requirements
# Client
For the final part of the system you're meant to build, status updates should be sent from each tank's location.
The goal is to continuously send POST requests to the server from the embedded circuit. 

The POST request should send a JSON object as payload.
# Server
A new route handler should be added to your API. The route handler function should accept a POST request on the path "/tank": `POST /tank`.

The function should also take the `water_level` value from the request body and calculate the `percentage_full` by converting the `water_level` value to a percentage. 

The response of this API call should be a JSON with a suitable success message, the status of the process and the time of the response.
# Database 
A new schema should be added to your application. This would mean that a new table or collection should be added to the database that you're application communicates with.  
# Joke
A man tells his doctor, “Doc, help me. I’m addicted to Twitter!”
The doctor replies, “Sorry, I don’t follow you …” :)
