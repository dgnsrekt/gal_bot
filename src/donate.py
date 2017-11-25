ADDRESSES = {
    'BTC': '34TJtHXxp5bE5PNp57dHdnX6P8ZxP6Uc5F',
    'BCH': '1LpEWzqo1xUwCLzjopH8r8K9ob6eDtkiWX',
    'ETH': '0x8f19991bE9Ea098792D07AcA93705B260350becD',
    'ETC': '0x68C1F2c2687d22f324fDa697b262AF389509b290',
    'ZEC': 't1ShXvBk1nmckrNJbpD6JFgc9kLd9mEQaCU'}

LINKS = {
    'BTC': 'https://blockchain.info/address/34TJtHXxp5bE5PNp57dHdnX6P8ZxP6Uc5F',
    'BCH': 'https://blockdozer.com/insight/address/1LpEWzqo1xUwCLzjopH8r8K9ob6eDtkiWX',
    'ETH': 'https://etherscan.io/address/0x8f19991bE9Ea098792D07AcA93705B260350becD',
    'ETC': 'http://gastracker.io/addr/0x68C1F2c2687d22f324fDa697b262AF389509b290',
    'ZEC': 'https://zchain.online/address/t1ShXvBk1nmckrNJbpD6JFgc9kLd9mEQaCU'}

MESSAGE = '<a href = "{link}">{name} Address : {address}</a>'


def getDonateLink(_name):
    for address, link in zip(ADDRESSES.items(), LINKS.items()):
        name = address[0]
        link = link[1]
        address = address[1]
        if name == _name:
            return MESSAGE.format(link=link, name=name, address=address)
