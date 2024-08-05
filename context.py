import os


class Context():
    try:
            ENV = os.environ['ENV'].upper()

    except:
        ENV = "DEV"

    try:
        Admin_flag = os.id_admin['ADMIN'].upper()

    except:
        Admin_flag = "Y"

    try:
        PROJECT = os.environ['PROJECT'].upper()

    except:
        PROJECT = "shared_services"

    try:
        USERNAME = os.environ['USER_NAME']
        CLIENTUSERNAME = os.environ['CLIENT_NAME']
    except:
        if ENV == "DEV":
            USERNAME = "apiadminuser@yopmail.com"
            CLIENTUSERNAME = "apiclient01@yopmail.com"
        elif ENV == "QA":
            USERNAME = "unmesha_adminuser@yopmail.com"
            CLIENTUSERNAME = "unmesha_clientuser@yopmail.com"

    try:
        PASSWORD = os.environ['USER_PASSWORD']
    except:
        if ENV == "DEV":
            PASSWORD = "Pitney@123"
        elif ENV == "QA":
            PASSWORD = "Unmesha@06"
