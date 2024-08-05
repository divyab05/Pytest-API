import random
import string
import datetime

'''
This function is used to generate random alphanumeric string
'''


def generate_random_alphanumeric_string():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return random_str


def generate_random_alphanumeric_string_locker():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return random_str


'''
This function is used to generate random digit number based on the range provided
'''


def generate_random_number(number):
    n = 10
    return ''.join(["{}".format(random.randint(0, 9)) for num in range(0, number)])


def generate_random_string(uppercase=True, lowercase=True, digits=True, char_count=10):
    rand_string = ''

    if not uppercase and lowercase and digits:  # Ex: 30nqg2t45c
        rand_string = rand_string.join((random.choices(string.ascii_lowercase + string.digits, k=char_count)))

    elif uppercase and not lowercase and digits:  # Ex: 609WN80HCW
        rand_string = rand_string.join((random.choices(string.ascii_uppercase + string.digits, k=char_count)))

    elif uppercase and lowercase and not digits:  # Ex: WDUDWOLduY
        rand_string = rand_string.join((random.choices(string.ascii_uppercase
                                                       + string.ascii_lowercase, k=char_count)))

    elif not uppercase and not lowercase and digits:  # Ex: 0878794852
        rand_string = rand_string.join((random.choices(string.digits, k=char_count)))

    elif not uppercase and lowercase and not digits:  # Ex: iutqanaczp
        rand_string = rand_string.join((random.choices(string.ascii_lowercase, k=char_count)))

    elif uppercase and not lowercase and not digits:  # Ex: JHOZJKEFUQ
        rand_string = rand_string.join((random.choices(string.ascii_uppercase, k=char_count)))

    else:  # Ex: pEDTXB0FXv
        rand_string = rand_string.join((random.choices(string.ascii_uppercase + string.ascii_lowercase
                                                       + string.digits, k=char_count)))

    return str(rand_string)


def get_current_timestamp(utc=False, iso_format=False, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
    # if fmt='%Y%m%d%H%M%S' then time_stamp='20230817145944'

    if utc and iso_format:
        time_stamp = datetime.datetime.utcnow().isoformat() + 'Z'  # Format: '2023-08-17T09:26:27.792566Z'
    elif utc:
        now = datetime.datetime.utcnow()
        time_stamp = now.strftime(fmt)  # Format: '2023-08-17T09:24:08.025987Z'
    elif iso_format:
        time_stamp = datetime.datetime.now().isoformat() + 'Z'  # Format: '2023-08-17T14:57:53.844056Z'
    else:
        now = datetime.datetime.now()
        time_stamp = now.strftime(fmt)  # Format: '2023-08-17T14:52:46.251634Z'

    return time_stamp
