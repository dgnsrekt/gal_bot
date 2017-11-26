import os

PATH = os.path.dirname(os.path.abspath(__file__))

def GetToken():
    """Parses TOKEN file. Strips newlines and
    whitespaces. Returns token string.
    """
    with open('TOKEN', 'r') as TOKEN:
        return TOKEN.read().strip('\n').strip(' ')

def GetPrivate():
    return os.path.join(PATH, 'private.key')

def GetCert():
    return os.path.join(PATH, 'cert.pem')

