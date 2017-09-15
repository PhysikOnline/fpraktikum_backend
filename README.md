# po-fp-django-1


---

Swagger does not work for nested Serializers so here is the Serializer for the RegistrationView:

{
"user_firstname": <str>,
"user_lastname": <str>,
"user_login": <str>,
"user_mail": <str>,
"user_matrikel": <str>,
"institutes":[
		{
		"name": <str>,
		"graduation": <str>,
		"semesterhalf": <int>
		},
		{
		"name": <str>,
		"graduation": <str>,
		"semesterhalf": <int>
		}
		],
"partner": {
            "user_firstname": <str>,
            "user_lastname": <str>,
            "user_login": <str>,
            "user_mail": <str>,
            "user_matrikel": <str>
            }
}
