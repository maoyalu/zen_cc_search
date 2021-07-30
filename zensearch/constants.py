from enum import Enum

# Data json files
USER_JSON = 'zensearch/data/users.json'
TICKET_JSON = 'zensearch/data/tickets.json'

# Model parameters
class UserParam(Enum):
    def display():
        return '\n'.join([str(param.value) + ') '
                        + field.lower() for field, param in UserParam.__members__.items()])

    _ID = 1
    NAME = 2
    CREATED_AT = 3
    VERIFIED = 4

class TicketParam(Enum):
    def display():
        return '\n'.join([str(param.value) + ') '
                        + field.lower() for field, param in TicketParam.__members__.items()])
    
    _ID = 1
    CREATED_AT = 2
    TYPE = 3
    SUBJECT = 4
    ASSIGNEE_ID = 5
    TAGS = 6

class SearchTarget(Enum):
    USERS = 'Users'
    TICKETS = 'Tickets'
