from zensearch.database import *
from zensearch.cli import *
from zensearch.constants import UserParam, TicketParam

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
        option_dic = {
            '1': self.search,
            '2': self.view_searchable_fields,
        }
        if op:
            self.perform_option(op, option_dic)
    
    # def search(self):
    #     """Search controller"""
    #     # Get the search target from user
    #     op = self.cli.search()
    #     option_dic = {
    #         '1': self.search_user,
    #         '2': self.search_ticket,
    #     }
    #     if op:
    #         self.perform_option(op, option_dic, self.search)

    def search(self):
        """Search controller"""
        # Get the search target from user
        op = self.cli.search()
        option_dic = {
            '1': ('Users', UserParam),
            '2': ('Tickets', TicketParam),
        }
        if op in option_dic:
            self.search_target(option_dic[op][0], option_dic[op][1])
        else:
            self.cli.error_invalid_option()
            self.cli.wait()
            self.search()

    def search_target(self, target, param_enum):
        term, value = self.cli.search_target(target, param_enum)
        if term is not None:
            print('Search successful!')


    def search_user(self):
        """Search user controller"""
        term, value = self.cli.search_user()
        if term is not None:
            print('Search successful!')


    def search_ticket(self):
        """Search ticket controller"""
        term, value = self.cli.search_ticket()
        if term is not None:
            print('Search successful!')

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

    
if __name__ == '__main__':
    app = App()
    app.run()