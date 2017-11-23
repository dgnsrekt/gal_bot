def GetToken():
    with open('TOKEN', 'r') as TOKEN:
        return TOKEN.read()
