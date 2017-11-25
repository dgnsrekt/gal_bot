def GetToken():
    """Parses TOKEN file. Strips newlines and
    whitespaces. Returns token string.
    """
    with open('TOKEN', 'r') as TOKEN:
        return TOKEN.read().strip('\n').strip(' ')
