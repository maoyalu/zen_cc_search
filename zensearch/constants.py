from enum import Enum

# Data json files
USER_JSON = 'zensearch/data/users.json'
TICKET_JSON = 'zensearch/data/tickets.json'

# Model parameters


class UserParam(Enum):
    """
    User parameters

    1) _id
    2) name
    3) created_at
    4) verified
    """
    def display() -> str:
        """
        Return a formatted string for display

        Returns:
            result: str - Formatted string for all params
        """
        return '\n'.join([str(param.value) + ') '
                          + field.lower() for field, param in UserParam.__members__.items()])

    _ID = 1
    NAME = 2
    CREATED_AT = 3
    VERIFIED = 4


class TicketParam(Enum):
    """
    Ticket parameters

    1) _id
    2) created_at
    3) type
    4) subject
    5) assignee_id
    6) tags
    """
    def display() -> str:
        """
        Return a formatted string for display

        Returns:
            result: str - Formatted string for all params
        """
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
