from requests import get as get_
from requests.auth import HTTPBasicAuth


login = 'sav0l'
password = 'SitnikovSaveliy2001!'


def get(*args, **kwargs):
    if 'auth' in kwargs.keys():
        raise Exception()
    return get_(*args, **kwargs, auth=HTTPBasicAuth(login, password))
