import json
from zensearch.config import Config


class Database:
    def __init__(self) -> None:
        self.users = None
        self.tickets = None
        self.config = Config()
        # User cache
        self.cache_user_created_at = {}
        self.cache_user_name = {}
        self.cache_user_verified = {}
        # Ticket cache
        self.cache_ticket_created_at = {}
        self.cache_ticket_type = {}
        self.cache_ticket_subject = {}
        self.cache_ticket_assignee_id = {}
        self.cache_ticket_tags = {}

    # region Initialization

    def init(self) -> None:
        '''Initialize databases'''
        self.user_init()
        self.ticket_init()

    def user_init(self) -> None:
        '''Initialize user data'''
        user_dict = {}
        try:
            with open(self.config.USER_JSON) as file:
                users = json.load(file)
                for user in users:
                    _id = user['_id']
                    name = user['name']
                    created_at = user['created_at']
                    # VERIFIED is an optional property
                    # If it is not provided, set to False by default
                    verified = user.get('verified', False)
                    # Create a new User
                    new_user = User(_id, name, created_at, verified)
                    user_dict[_id] = new_user
                    # Check if we need to cache the user in other ways
                    self.cache_user(new_user)
        except Exception as e:
            print('\n** User initialization failed. **\n')
            print(e)
        self.users = user_dict

    def ticket_init(self) -> None:
        '''Initialize ticket data'''
        ticket_dict = {}
        try:
            with open(self.config.TICKET_JSON) as file:
                tickets = json.load(file)
                for ticket in tickets:
                    _id = ticket['_id']
                    created_at = ticket['created_at']
                    # TYPE is an optional property
                    type_of = ticket.get('type', None)
                    subject = ticket['subject']
                    # ASSIGNEE_ID is an optional property
                    assignee_id = ticket.get('assignee_id', None)
                    tags = ticket['tags']
                    # Create a new Ticket
                    new_ticket = Ticket(_id, created_at, subject,
                                        tags, type_of, assignee_id)
                    new_ticket.assignee = self.users.get(assignee_id, None)
                    ticket_dict[_id] = new_ticket
                    # Check if we need to cache the ticket in other ways
                    self.cache_ticket(new_ticket)
                    # Associate ticket with user
                    if new_ticket.assignee_id is not None and new_ticket.assignee_id in self.users:
                        self.users[new_ticket.assignee_id].assign(new_ticket)
        except Exception as e:
            print('\n** Ticket initialization failed. **\n')
            print(e)
        self.tickets = ticket_dict

    def cache_user(self, user) -> None:
        """Create reverse indexes for user data"""
        # A user list by the given created_at
        if self.config.CACHE_USER_CREATED_AT:
            if user.created_at in self.cache_user_created_at:
                self.cache_user_created_at[user.created_at].append(user)
            else:
                self.cache_user_created_at[user.created_at] = [user]

        # A user list by the given name
        if self.config.CACHE_USER_NAME:
            if user.name in self.cache_user_name:
                self.cache_user_name[user.name].append(user)
            else:
                self.cache_user_name[user.name] = [user]

        # A user list by the given verified
        if self.config.CACHE_USER_VERIFIED:
            if user.verified in self.cache_user_verified:
                self.cache_user_verified[user.verified].append(user)
            else:
                self.cache_user_verified[user.verified] = [user]

    def cache_ticket(self, ticket) -> None:
        """Create reverse indexes for ticket data"""
        # A ticket list by the given created_at
        if self.config.CACHE_TICKET_CREATED_AT:
            if ticket.created_at in self.cache_ticket_created_at:
                self.cache_ticket_created_at[ticket.created_at].append(ticket)
            else:
                self.cache_ticket_created_at[ticket.created_at] = [ticket]

        # A ticket list by the given type
        if self.config.CACHE_TICKET_TYPE:
            if ticket.type in self.cache_ticket_type:
                self.cache_ticket_type[ticket.type].append(ticket)
            else:
                self.cache_ticket_type[ticket.type] = [ticket]

        # A ticket list by the given subject
        if self.config.CACHE_TICKET_SUBJECT:
            if ticket.subject in self.cache_ticket_subject:
                self.cache_ticket_subject[ticket.subject].append(ticket)
            else:
                self.cache_ticket_subject[ticket.subject] = [ticket]

        # A ticket list by the given assignee_id
        if self.config.CACHE_TICKET_ASSIGNEE_ID:
            if ticket.assignee_id in self.cache_ticket_assignee_id:
                self.cache_ticket_assignee_id[ticket.assignee_id].append(
                    ticket)
            else:
                self.cache_ticket_assignee_id[ticket.assignee_id] = [ticket]

        # A ticket list by the given tags
        if self.config.CACHE_TICKET_TAGS:
            # Iterate through the tag list
            for tag in ticket.tags:
                # Cache per tag
                if tag in self.cache_ticket_tags:
                    self.cache_ticket_tags[tag].append(ticket)
                else:
                    self.cache_ticket_tags[tag] = [ticket]

    # endregion Initialization

    # region Search - User

    def search_user_id(self, _id: int) -> list:
        """
        Search user by its _id field
        
        Parameters:
            _id: int - The unique _id of the user

        Returns:
            result: list - A list of users found ( [User] | [ ] )
        """
        if _id in self.users:
            return [self.users[_id]]
        else:
            return []

    def search_user_name(self, name: str) -> list:
        """
        Search user by its name field
        
        Parameters:
            name: str - The name of the user

        Returns:
            result: list - A list of users found ( [User] | [ ] )
        """
        if self.config.CACHE_USER_NAME:
            if name in self.cache_user_name:
                return self.cache_user_name[name]
            else:
                return []
        else:
            return [user for user in self.users.values() if user.name == name]

    def search_user_created_at(self, created_at: str) -> list:
        """
        Search user by its created_at field
        
        Parameters:
            created_at: str - The created datetime string of the user
                                Example: "2016-04-06T06:55:28-10:00"

        Returns:
            result: list - A list of users found ( [User] | [ ] )
        """
        if self.config.CACHE_USER_CREATED_AT:
            if created_at in self.cache_user_created_at:
                return self.cache_user_created_at[created_at]
            else:
                return []
        else:
            return [user for user in self.users.values() if user.created_at == created_at]

    def search_user_verified(self, verified: bool) -> list:
        """
        Search user by its verified field
        
        Parameters:
            verified: bool - Whether the user is verified

        Returns:
            result: list - A list of users found ( [User] | [ ] )
        """
        if self.config.CACHE_USER_VERIFIED:
            return self.cache_user_verified[verified]
        else:
            return [user for user in self.users.values() if user.verified == verified]

    # endregion Search - User

    # region Search - Ticket

    def search_ticket_id(self, _id: str) -> list:
        """
        Search ticket by its _id field
        
        Parameters:
            _id: str - The _id of the ticket

        Returns:
            result: list - A list of tickets found ( [Ticket] | [ ] )
        """
        if _id in self.tickets:
            return [self.tickets[_id]]
        else:
            return []

    def search_ticket_created_at(self, created_at):
        """
        Search ticket by its created_at field
        
        Parameters:
            created_at: str - The created datetime string of the ticket
                                Example: "2016-04-06T06:55:28-10:00"

        Returns:
            result: list - A list of tickets found ( [Ticket] | [ ] )
        """
        if self.config.CACHE_TICKET_CREATED_AT:
            if created_at in self.cache_ticket_created_at:
                return self.cache_ticket_created_at[created_at]
            else:
                return []
        else:
            return [ticket for ticket in self.tickets.values() if ticket.created_at == created_at]

    def search_ticket_type(self, type: str) -> list:
        """
        Search ticket by its type field
        
        Parameters:
            type: str | None - The type of the ticket

        Returns:
            result: list - A list of tickets found ( [Ticket] | [ ] )
        """
        if self.config.CACHE_TICKET_TYPE:
            if type in self.cache_ticket_type:
                return self.cache_ticket_type[type]
            else:
                return []
        else:
            return [ticket for ticket in self.tickets.values() if ticket.type == type]

    def search_ticket_subject(self, subject: str) -> list:
        """
        Search ticket by its subject field
        
        Parameters:
            subject: str - The subject title of the ticket

        Returns:
            result: list - A list of tickets found ( [Ticket] | [ ] )
        """
        if self.config.CACHE_TICKET_SUBJECT:
            if subject in self.cache_ticket_subject:
                return self.cache_ticket_subject[subject]
            else:
                return []
        else:
            return [ticket for ticket in self.tickets.values() if ticket.subject == subject]

    def search_ticket_assignee_id(self, a_id: int) -> list:
        """
        Search ticket by its assignee_id field
        
        Parameters:
            assignee_id: int | None - Whom the ticket is assigned to

        Returns:
            result: list - A list of tickets found ( [Ticket] | [ ] )
        """
        if self.config.CACHE_TICKET_ASSIGNEE_ID:
            if a_id in self.cache_ticket_assignee_id:
                return self.cache_ticket_assignee_id[a_id]
            else:
                return []
        else:
            return [ticket for ticket in self.tickets.values() if ticket.assignee_id == a_id]

    def search_ticket_tags(self, tag: str) -> list:
        """
        Search ticket by a tag
        
        Parameters:
            tag: str - The name of the tag

        Returns:
            result: list - A list of tickets found ( [Ticket] | [ ] )
        """
        if self.config.CACHE_TICKET_TAGS:
            if tag in self.cache_ticket_tags:
                return self.cache_ticket_tags[tag]
            else:
                return []
        else:
            return [ticket for ticket in self.tickets.values() if tag in ticket.tags]

    # endregion Search - Ticket


class User:
    def __init__(self, _id: int, name: str, created_at: str, verified: bool = False) -> None:
        self._id = _id
        self.name = name
        self.created_at = created_at
        self.verified = verified
        self.tickets = []

    def assign(self, ticket) -> None:
        """
        Add a ticket to the user's ticket list
        
        Parameters:
            ticket: Ticket - The ticket that needs to be assigned
        """
        if ticket not in self.tickets:
            self.tickets.append(ticket)


class Ticket:
    def __init__(self, _id, created_at, subject, tags, type=None, assignee_id=None) -> None:
        self._id = _id
        self.created_at = created_at
        self.subject = subject
        self.tags = tags
        self.type = type
        self.assignee_id = assignee_id
        self.assignee = None
