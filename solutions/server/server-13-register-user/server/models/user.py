class User:
    '''Represents one User'''

    @staticmethod
    def fromDict(dict):
        try:
            user = User(
                dict['email'],
                dict['password'],
                id = dict['id']
            )
            return user
        except Exception as e:
            return None


    def __init__(self, email, password, id=''):
        self.id = id
        self.email =  email
        self.password = password
