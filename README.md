# Django RestApi Project

Steps to test this API
## Install requirements.txt
```
pip install -r requirements.txt
```

### Incase you dont use the existing database
```
The database is populated with relevant data for testing purposes but If you want to use a 
different database you can use the 'sample-data.json' file for importing the information for 
the databse. Just use- 

python manage.py makemigrations
python manage.py loaddata sample-data.json

```

## Migrate the database
```
python manage.py migrate
```
## Runserver
```
python manage.py runserver
```
## API Endpoints

### To Register New User
```
URL: http://127.0.0.1:8000/api/register/
POST Request
Data: {
    "username":"Harley Quinn",
    "email":"Harley@example.com",
    "password":"qwertyui1234",
    "phone":"9282726252"
}
```

### To Login 
```
URl: http://127.0.0.1:8000/api/login/
POST Request
Data: {
    "username":"batman",
    "password":"qwertyui1234"
} 
```
### JWT AUTH TOKEN
After successful registeration and login
You will be provided with a JWT Authentication Token when you login
Add this token in the headers of requests that requires user authentication.
```
Authorization: token ff5dc48eeefc3d45b15ac13c6b42a360d34477bf
```

### To view all the contacts associated with the request user
```
URL: http://127.0.0.1:8000/api/contacts/
GET Request
Header: {
    Authorization: token ff5dc48eeefc3d45b15ac13c6b42a360d34477bf
}
```

### To save a contact for a request user'
```
URL: http://127.0.0.1:8000/api/contacts/
GET Request
Header: {
    Authorization: token ff5dc48eeefc3d45b15ac13c6b42a360d34477bf
}

Data: {
    "name": "Poison Ivy",
    "phone_number": 8446718050,
    "email": "ivy@example.com"
}
```

### To mark any contact as Spam Number
```
URL: http://127.0.0.1:8000/api/spams/
POST Request
Data: {
    "phone_number": 9181716151
}
```

### To search a contact by name
```
URL: http://localhost:8000/api/search_by_name/
GET Request
Header: {
    Authorization: token ff5dc48eeefc3d45b15ac13c6b42a360d34477bf
}
```

### To search a contact by phone
```
URL: http://localhost:8000/api/search_by_phone/
GET Request
Header: {
    Authorization: token ff5dc48eeefc3d45b15ac13c6b42a360d34477bf
}
```