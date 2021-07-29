import json
from columnar import columnar
from zensearch.constants import USER_JSON, TICKET_JSON

class Database:
    def __init__(self) -> None:
        self.users = None
        self.tickets = None

    # region Initialization

    def init(self):
        '''Initialize databases'''
        self.user_init()
        self.ticket_init()
    
    def user_init(self):
        '''Initialize user data'''
        user_dict = {}
        with open(USER_JSON) as file:
            users = json.load(file)
            for user in users:
                _id = user['_id']
                name = user['name']
                created_at = user['created_at']
                # VERIFIED is an optional property
                # If it is not provided, set to False by default
                verified = False
                try:
                    verified = user['verified']
                except:
                    pass

                user_dict[_id] = User(_id, name, created_at, verified)
            self.users = user_dict
        

    def ticket_init(self):
        '''Initialize ticket data'''
        with open(TICKET_JSON) as file:
            self.tickets = json.load(file)

    # endregion Initialization

    # region Search - User

    def search_user_id(self, _id):
        if _id in self.users:
            return self.users[_id]
        else:
            return None

    # endregion Search - User


class User:
    def __init__(self, _id, name, created_at, verified=False) -> None:
        self._id = _id
        self.name = name
        self.created_at = created_at
        self.verified = verified
    
    def __str__(self):
        headers = ['_id', 'name', 'created_at', 'verified']
        data = [[self._id, self.name, self.created_at, self.verified]]
        return columnar(data, headers, no_borders=True)



# class Ticket:
#     def __init__(self, _id, created_at, subject, tags, type=None, assignee_id=None) -> None:
#         self._id = _id
#         self.created_at = created_at
#         self.subject = subject
#         self.tags = tags,
#         self.type = type,
#         self.assignee_id = assignee_id
    