class List:
    '''Represents one List'''

    @staticmethod
    def fromDict(dict):
        try:
            l = List(
                dict['title'],
                dict['owner'],
                id = dict['id'],
                revision = int(dict['revision']),
                inbox = dict['inbox']
            )
            return l
        except Exception as e:
            return None


    def __init__(self, title, owner, id='', revision=1, inbox=0):
        self.id = id
        self.title =  title
        self.owner = owner
        self.inbox = inbox != 0
        self.revision = revision
        self.collaborators = []
