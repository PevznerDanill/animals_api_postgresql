# Animals API with Postgresql

## API with Postgresql to store and manage an animal database

### Installation

* Execute ``pip install -r requirements.txt`` 

This application uses the sending of emails. 

The configuration for the sending of emails is set in the end of the
settings.py file:

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-host-smtp.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'your-host-email@email.com'
EMAIL_HOST_PASSWORD = 'your_account_application_password'
DEFAULT_FROM_EMAIL = 'your-host-email@email.com'
```

To activate this mechanism, it is necessary to set these variables.

Also, the application uses this configuration for the database:

````
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'animals',
        'PASSWORD': 'animals_password_0',
        'USER': 'user_animals'
    }
}
````

Currently, all users in the database (including the superuser (admin)) have a password ```robot1234```.
The saved instances are stored in the ```app_animals/fixtures``` and ``app_users/fixtures`` folders in json format.

The further installation requires the execution of the following commands:

* ``cd animals``
* ``python manage.py migrate``
* ``python manage.py createsuperuser``
* ``python manage.py runserver``

### Creation of new users and authorization

The application uses djoser for the creation of a new user and token authentication.

Almost all endpoints, except ``api/v1/animals/shelters/``, require authentication.

To create a new user, one should make the following post request:

* Endpoint: ```auth/users/```
* Example of JSON content: 

```
{
	"username": "new-uzz-1000", 
	"password": "robot1234",
	"shelter": 2
}
```

The example response will be:

```
{
	"username": "new-uzz-1000",
	"shelter": 2,
	"id": 9
}
```

To get a token for the activation, one should make the following post request:

* Endpoint: ```auth/token/login/```
* Example of JSON-content:

```
{
	"username": "new-uzz-1000", 
	"password": "robot1234"
}
```

The example response will be:

```
{
	"auth_token": "77bad56b1f9ace3b3769f2565446a6dcc0cb4817"
}
```

The other requests must contain an Authorization header with the value
```Token 77bad56b1f9ace3b3769f2565446a6dcc0cb4817```


To set the email of the user, he can make the following put request:

* Endpoint: ```auth/users/me/```
* Example of JSON-content:

```
{

	"email": "somemail@mail.com"
}
```

The example response will be:

```
{
	"email": "somemail@mail.com",
	"id": 9,
	"username": "new-uzz-1000"
}
```

Once created, a new user has a status ```is_guest```, set to True. With this guest status
he can access the list of the animals in his shelter and the detail information of every animal in 
his shelter. 

To upgrade this status and be able to add new animal records to the database and edit/delete them, 
the user needs to make the following post request:

* Endpoint: ```users/upgrade/```

If the user has not provided his email, he needs to pass it in the request:

* Example of JSON content:

```
{
	"email": "somemail@mail.com"
}
```

The example response will be:

```
{
	"details": "You request was submitted"
}
```

After this the superuser receives an email message with the request to update the user:

```
The user new-uzz-1000 with id 9 asks to upgrade him to be able to create new Animal objects and set the is_guest 
flag to False. If you decide to accept the request and then in the future to set the flag back to True, do not 
forget to alsoset the flag asked_for_upgrade so the user could send a new request.
```

If the superuser decides to change the status of the user in the admin panel, the user will receive a
notification email like this one:

```
Your status was upgraded. You can now create and add new animal objects in your shelter.
```

If the status is downgraded, the user will also receive a notification message about it.

To logout, the user can make the following post request without any content:

* Endpoint: ```auth/token/logout/```

As the result, the issued token won't be active anymore.

### Animals database.

Once authenticated, the user can access the list of the animals in his shelter with 
the following get request:

* Endpoint: ```api/v1/animals/```

The example response will be:

```
{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 3,
			"name": "Murzik",
			"shelter": {
				"id": 2,
				"title": "Cat's shelter"
			}
		},
		{
			"id": 4,
			"name": "Pushok",
			"shelter": {
				"id": 2,
				"title": "Cat's shelter"
			}
		}
	]
}
```

To see the details of every animal in the user's shelter, he can make
the following get request:

* Endpoint: ```api/v1/animals/3/``` - here "3" is an id of the retrieved animal record.

The example response will be:

```
{
	"id": 3,
	"joined_shelter": "2023-05-13",
	"name": "Murzik",
	"age": "2022-08-08",
	"height": 20.0,
	"weight": 20.0,
	"owner": 2,
	"shelter": 2,
	"distinctive_features": "grey little cat"
}
```

The user can't access the data about the animals of the other shelters.

If the user has an upgraded status (not guest), he can create a new record with the
following post request:

* Endpoint: ```api/v1/animals/new/```
* Example of JSON-content:

```
{
	"joined_shelter": "2023-04-13",
	"age": "2023-05-10",
	"height": 10.0,
	"weight": 30.0,
	"name": "some name",
	"distinctive_features": "some distinctive_features"
	
}
```

The successful example response will be:

```
{
	"id": 21,
	"joined_shelter": "2023-04-13",
	"name": "some name",
	"age": "2023-02-10",
	"height": 10.0,
	"weight": 30.0,
	"owner": 9,
	"shelter": 2,
	"distinctive_features": "some distinctive_features"
}
```

Note that the date of birth (age) can not be later than the date of joining the shelter (joined_shelter).
Also, both of these fields can not be later than the current date.

To update the record or delete it, the user can perform put, patch and delete requests to the 
```api/v1/animals/21/``` ("21" here is an id of the record) endpoint.

Note that the user can edit or delete only those records that he created himself.


It is important to mention that the delete request doesn't actually delete the record from the database. 
It sets its attribute ```is_archived``` to True and this records won't be available anymore. 
However, the superuser can delete it from the database using the admin panel.



### Testing

The application can be tested with the ```python manage.py test``` command executed from the animals/ root folder.
To run multiple tests, the multiple_tests.sh bash script can be executed. Currently, it performs 100 iterations. 
This number can be changed.

It is important to have a look at the setUp method in the AskForUpgradeAPITestCase in the app_users.tests.py file:

```
def setUp(self) -> None:
        self.user.email = 'someemail@email.com'
        self.user.save(force_update=['email'])
        # admin_user = User.objects.get(is_superuser=True)
        # admin_user.email = 'somenewemail@mail.com'
        # admin_user.save()
        self.url = reverse('app_users:user_upgrade')
```

Here the user's email and the admin's email are set to some non-existing emails. To test if the message is sent, it is 
important to set the real values.