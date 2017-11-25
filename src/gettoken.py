def GetToken():
    """Parses TOKEN file. Strips newlines and
    whitespaces. Returns token string.
    """
    with open('TOKEN', 'r') as TOKEN:
        return TOKEN.read().strip('\n').strip(' ')


def GetDonateAddresses():
    """Returns donations addresses."""
    with open('DONATE', 'r') as DONATE:
        return DONATE.read()
