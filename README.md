# po-fp-django-1


---

Swagger does not work for nested Serializers so here is the Serializer for the RegistrationView:

{							<br />
"user_firstname": <str>,<br />
"user_lastname": <str>,<br />
"user_login": <str>,<br />
"user_mail": <str>,<br />
"user_matrikel": <str>,<br />
"institutes":[<br />
		{<br />
		"name": <str>,<br />
		"graduation": <str>,<br />
		"semesterhalf": <int><br />
		},<br />
		{<br />
		"name": <str>,<br />
		"graduation": <str>,<br />
		"semesterhalf": <int><br />
		}<br />
		],<br />
"partner": {<br />
            "user_firstname": <str>,<br />
            "user_lastname": <str>,<br />
            "user_login": <str>,<br />
            "user_mail": <str>,<br />
            "user_matrikel": <str><br />
            }<br />
}<br />
