from zensearch.database import *
from zensearch.cli import *
from zensearch.constants import UserParam, TicketParam, SearchTarget

class App:
    def __init__(self) -> None:
        self.cli = CLI()
        self.db = Database()

    def run(self):
        """Start app"""
        # Load up data
        self.db.init()

        # Entry point
        while True:
            self.main()

    def main(self):
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
                self.cli.wait()

    def search(self):
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
                    self.cli.wait()
            else:
                self.cli.error_invalid_option()
                self.cli.wait()
                self.search()

    def search_user(self, field_num, value):
        """Search user controller"""
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
        # Check if any user is found
        if users:
            # Display result
            for user in users:
                print(user)
        else:
            print('No user found')
        print('Search successful! - {}: {}'. format(UserParam(field_num).name, value))

    def search_ticket(self, field_num, value):
        """Search ticket controller"""
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
            if value == '':
                value = None
            tickets = self.db.search_ticket_assignee_id(value)
        elif field == TicketParam.TAGS:
            tickets = self.db.search_ticket_tags(value)
        # Check if any ticket is found
        if tickets:
            for ticket in tickets:
                print(ticket)
        else:
            print('No ticket found')
        print('Search successful! - {}: {}'. format(TicketParam(field_num).name, value))

    def view_searchable_fields(self):
        """Fields controller"""
        self.cli.view_searchable_fields()

    def perform_option(self, op, option_dic, redirect=None):
        # Look up option functions
        if op in option_dic:
            option_dic[op]()
        # Show error if the option is invalid
        else:
            self.cli.error_invalid_option()
            self.cli.wait()
            if redirect:
                redirect()

    # region validations

    def is_valid_user_id(self, id):
        try:
            id = int(id)
            return True
        except:
            return False

    def value_to_bool(self, val):
        # Typo auto-fixed...by me :P
        true = ['True', 'true', 'Ture', 'ture',
                'Y', 'y', 'Yes', 'yes']
        return val in true

    # endregion validations

    
if __name__ == '__main__':
    app = App()
    app.run()