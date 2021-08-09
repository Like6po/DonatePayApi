
class API:
    def __init__(self, token, version=1):
        self.TOKEN = f"?access_token={token}"
        self.BASE = 'https://donatepay.ru/api/v{0}'.format(version)
        self.USER = self.BASE + '/user' + self.TOKEN
        self.TRANSACTIONS = self.BASE + '/transactions' + self.TOKEN
        self.NOTIFICATIONS = self.BASE + '/notification'
