tabs_data = [
    {
        "tabTitle": "Personal Information",
        "inputFields": [
            {"key": "firstName", "label": "First Name", "type": "text", "mandatory": True},
            {"key": "lastName", "label": "Last Name", "type": "text", "mandatory": True},
            {"key": "email", "label": "Email Address", "type": "email", "mandatory": False},
            {"key": "phoneNumber", "label": "Phone Number", "type": "tel", "mandatory": False},
            {"key": "dob", "label": "Date of Birth", "type": "date", "mandatory": True},
        ],
    },
    {
        "tabTitle": "Account Settings",
        "inputFields": [
            {"key": "username", "label": "Username", "type": "text", "mandatory": True},
            {"key": "password", "label": "Password", "type": "password", "mandatory": True},
            {"key": "confirmPassword", "label": "Confirm Password", "type": "password", "mandatory": True},
            {"key": "notifications", "label": "Receive Notifications", "type": "checkbox", "mandatory": False},
        ],
    },
    {
        "tabTitle": "Account Settings 2",
        "inputFields": [
            {"key": "username2", "label": "Username", "type": "text", "mandatory": True},
            {"key": "password2", "label": "Password", "type": "password", "mandatory": True},
            {"key": "confirmPassword2", "label": "Confirm Password", "type": "password", "mandatory": True},
            {"key": "notifications2", "label": "Receive Notifications", "type": "checkbox", "mandatory": False},
        ],
    },
]


tabs_data=[
                    {"id": 1, "name": "Alice", "age": 25},
                    {"id": 2, "name": "Bob", "age": 30},
                    {"id": 3, "name": "Charlie", "age": 35}
                ]


json_data = '''
            {
                "header": {
                    "id": "ID",
                    "name": "Name",
                    "age": "Age",
                    "action": "Action"
                },
                "data": [
                    {"id": 1, "name": "Alice", "age": 25},
                    {"id": 2, "name": "Bob", "age": 30},
                    {"id": 3, "name": "Charlie", "age": 35}
                ]
            }
            '''
