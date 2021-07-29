import json
from zensearch.constants import USER_JSON, TICKET_JSON

class Database:
    def __init__(self) -> None:
        self.users = None
        self.tickets = None

    def init(self):
        '''Initialize databases'''
        self.user_init()
        self.ticket_init()
    
    def user_init(self):
        '''Initialize user data'''
        with open(USER_JSON) as file:
            self.users = json.load(file)

    def ticket_init(self):
        '''Initialize ticket data'''
        with open(TICKET_JSON) as file:
            self.tickets = json.load(file)


# class User:
#     def __init__(self, _id, name, created_at, verified=False) -> None:
#         self._id = _id,
#         self.name = name,
#         self.created_at = created_at,
#         self.verified = verified


# class Ticket:
#     def __init__(self, _id, created_at, subject, tags, type=None, assignee_id=None) -> None:
#         self._id = _id
#         self.created_at = created_at
#         self.subject = subject
#         self.tags = tags,
#         self.type = type,
#         self.assignee_id = assignee_id
        

if __name__ == '__main__':
    db = Database()
    print(db.tickets)
    