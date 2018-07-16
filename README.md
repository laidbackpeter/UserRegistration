# django-farmer-api

REST API for registration of farmers and their bags of seed


## Instructions

Using Django, build and document a REST API for a system that will be used in multiple countries and different languages in each country to  register farmers & farmers' bags of seed. 

Farmers registration requires the following details:
 - Phone number
 - District
 - Village 
 - Crop grown by the farmer 
 - bank account number 

Bags of seed registration requires:
 - Unique Bag number 
 - The farmer who's bought the bag 
 
 Be sure to add proof that the system is working through automated testing.  


### Due
Tuesday 17th July, 2018 22:00HRS EAT

### Brief and Assumptions
This is an a RESTful API that will be utilized in the registration of farmers and the seed bags they purchase.

There are two views
1. Farmer registration view
2. Seed Bag registration view

Below are some of the assumptions that were used in the implementation of the API:
1. Input validation will be done by the consumer of the API e.g. Ensuring country input is a valid input etc
2. A farmer cannot buy a seed bag if they are not registered

For one to use the API they need to make sure they have the correct http headers for authentication

`{APIKEY: 'api-key-123'}`

#### Usage
1. First clone the repository.
2. Ensure you have virtualenv installed
3. Go to the project root
4. Activate the virtual env i.e. `source venv/bin/activate`
5. Run `python manage.py runserver` to start server
6. Send POST requests using a client e.g. POSTMAN
7. Ensure you have the correct headers especially for authentication
8. To run test run `python manage.py test`

### Farmer Registration Request
`
{
    "first_name" : "Peter",
    "last_name" : "Muchina",
    "other_name" : "Ndegwa",
    "phone_number" : "254725817350",
    "country" : "Kenya",
    "district" : "Nairobi",
    "village" : "Tipis",
    "crop" : "Potatoes"
}
`

### Farmer Registration Response
202 [Accepted]  Request accepted processing underway

`
{
    "Details": "Ok"
}
`

400 [Bad Request] Malformed request

403 [Forbidden] API authentication failed

### Seed Bag Registration Request
`
{
    "phone_number" : "254725817350",
    "bag_unique_number" : "12345ygft"
}
`

### Seed Bag Registration Response
202 [Accepted]  Request accepted processing underway

`
{
    "Details": "Ok"
}
`

Or

`
{
    "Details": "Farmer doesn't exists"
}
`

400 [Bad Request] Malformed request

403 [Forbidden] API authentication failed


### Log events to look out for

`register_farmer_response` - Contains response after a farmer registration attempt

`register_farmer_request` - Contains request payload for a farmer registration attempt

`register_seed_bag_response` - Contains response after a seed bag registration attempt

`register_seed_bag_request` - Contains request payload for a seed bag registration attempt
