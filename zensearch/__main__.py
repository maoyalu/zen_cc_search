import columnar
from zensearch.database import *
from zensearch.cli import *
from zensearch.constants import UserParam, TicketParam, SearchTarget


class App:
    def __init__(self) -> None:
        self.cli = CLI()
        self.db = Database()

    def run(self) -> None:
        """Start app"""
        # Load up data
        self.db.init()

        # Entry point
        while True:
            self.main()

    def main(self) -> None:
        """Main controller"""
        # Get the function selection from user
        op = self.cli.main()
        # User didn't quit
        if op:
            option_dic = {
                '1': self.search,
                '2': self.view_searchable_fields,
            }
            if op in option_dic:
                option_dic[op]()
            # Show error if the option is invalid
            else:
                self.cli.error_invalid_option()

    def search(self) -> None:
        """Search controller"""
        # Get the search target from user
        op = self.cli.search()
        # User didn't quit
        if op:
            target_dic = {
                '1': (SearchTarget.USERS.value, UserParam),
                '2': (SearchTarget.TICKETS.value, TicketParam),
            }
            if op in target_dic:
                target, param = target_dic[op]
                term, value = self.cli.search_target(target, param)
                if term is not None:
                    search_function = {
                        SearchTarget.USERS.value: self.search_user,
                        SearchTarget.TICKETS.value: self.search_ticket
                    }
                    search_function[target](term, value)
            else:
                self.cli.error_invalid_option()
                self.search()

    def search_user(self, field_num: int, value: str) -> None:
        """Search user controller
        
        Parameters:
            field_num: int - the field number used in the param enum class
            value: str - the input value of the term
        """
        users = []
        field = UserParam(field_num)
        if field == UserParam._ID and self.is_valid_user_id(value):
            users = self.db.search_user_id(int(value))
        elif field == UserParam.NAME:
            users = self.db.search_user_name(value)
        elif field == UserParam.CREATED_AT:
            users = self.db.search_user_created_at(value)
        elif field == UserParam.VERIFIED:
            value = self.value_to_bool(value)
            users = self.db.search_user_verified(value)
        self.show_user_result(users)

    def show_user_result(self, users) -> None:
        """Display search result for users"""
        result = 'No user found'
        # Check if any user is found
        if users:
            # Prepare display result
            headers = ['_id', 'name', 'created_at', 'verified', 'tickets']
            data = []
            for user in users:
                data.append([user._id,
                             user.name,
                             user.created_at,
                             user.verified,
                             '\n'.join([t.subject for t in user.tickets])
                             ])
            result = columnar(data, headers)
        self.cli.display_search_result(result)

    def search_ticket(self, field_num: int, value: str) -> None:
        """Search ticket controller
        
        Parameters:
            field_num: int - the field number used in the param enum class
            value: str - the input value of the term
        """
        tickets = []
        field = TicketParam(field_num)
        if field == TicketParam._ID:
            tickets = self.db.search_ticket_id(value)
        elif field == TicketParam.CREATED_AT:
            tickets = self.db.search_ticket_created_at(value)
        elif field == TicketParam.TYPE:
            if value == '':
                value = None
            tickets = self.db.search_ticket_type(value)
        elif field == TicketParam.SUBJECT:
            tickets = self.db.search_ticket_subject(value)
        elif field == TicketParam.ASSIGNEE_ID:
            if value == '' or not self.is_valid_user_id(value):
                value = None
            else:
                value = int(value)
            tickets = self.db.search_ticket_assignee_id(value)
        elif field == TicketParam.TAGS:
            tickets = self.db.search_ticket_tags(value)
        self.show_ticket_result(tickets)

    def show_ticket_result(self, tickets) -> None:
        """Display search result for tickets"""
        result = 'No ticket found'
        # Check if any ticket is found
        if tickets:
            # Prepare display result
            headers = ['_id', 'created_at', 'type', 'subject',
                       'assignee_id', 'tags', 'assignee_name']
            data = []
            for ticket in tickets:
                assignee_name = None
                if ticket.assignee:
                    assignee_name = ticket.assignee.name
                data.append([ticket._id,
                             ticket.created_at,
                             ticket.type,
                             ticket.subject,
                             ticket.assignee_id,
                             '\n'.join(ticket.tags),
                             assignee_name])
            result = columnar(data, headers)
        self.cli.display_search_result(result)

    def view_searchable_fields(self):
        """Fields controller"""
        self.cli.view_searchable_fields()

    def perform_option(self, op: str, option_dict: dict, redirect = None) -> None:
        """Perfrom function according to the option selected
        
        Parameters:
            op: str - The input option string from the user

            option_dict: dict - A dictionary of functions that options associated with.

            redirect - The following up page to redirect, go back to main page if not provided
        """
        # Look up option functions
        if op in option_dict:
            option_dict[op]()
        # Show error if the option is invalid
        else:
            self.cli.error_invalid_option()
            if redirect:
                redirect()

    # region validations

    def is_valid_user_id(self, id: str) -> bool:
        """Check if the input string can convert to int
        
        Parameters:
            id: str - The input string from user
        """
        try:
            id = int(id)
            return True
        except:
            return False

    def value_to_bool(self, val: str) -> bool:
        """Convert the input string can convert to bool
        
        Parameters:
            val: str - The input string from user. If it is not true, set to False by default.
        """
        # Typo auto-fixed...by me :P
        true = ['True', 'true', 'Ture', 'ture',
                'Y', 'y', 'Yes', 'yes']
        return val in true

    # endregion validations


if __name__ == '__main__':
    app = App()
    app.run()
