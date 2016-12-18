class List:
    '''Represents one List'''

    @staticmethod
    def fromDict(dict):
        try:
            l = List(
                dict['title'],
                id = dict['id'],
                revision = int(dict['revision']),
                inbox = dict['inbox'] != 0 # if 0 then False
            )
            return l
        except Exception as e:
            raise e
            return None

    def __init__(self, title, id='', revision=1, inbox = False):
        self.id = id
        self.title =  title
        self.revision = revision
        self.inbox = inbox
