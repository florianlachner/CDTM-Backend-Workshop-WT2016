class Task():

    NORMAL = 'normal'
    COMPLETED = 'completed'

    def __init__(self, title, list, id='', status=NORMAL, description='', due='', revision=1):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.due = due
        self.revision = revision

    @staticmethod
    def fromDict(dict):
        try:
            task = Task(
                dict['title'],
                dict['list'],
                id=dict['id'],
                status=dict['status'],
                description=dict['description'],
                due=dict['due'],
                revision=int(dict['revision'])
            )
            return task
        except Exception as e:
            return None