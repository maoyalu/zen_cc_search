import click
from zensearch.constants import UserParam, TicketParam, SearchTarget


class CLI:
    def __init__(self) -> None:
        pass

    def main(self):
        """ZENDESK search - main page.
        
        Returned options:

            1 - zendesk search

            2 - view searchable fields

            quit - Exit the app
        """
        click.echo("""
  _____ U _____ u _   _    ____  U _____ u ____       _  __    
 |"_  /u\| ___"|/| \ |"|  |  _"\ \| ___"|// __"| u   |"|/ /    
 U / //  |  _|" <|  \| |>/| | | | |  _|" <\___ \/    | ' /     
 \/ /_   | |___ U| |\  |uU| |_| |\| |___  u___) |  U/| . \\u   
 /____|  |_____| |_| \_|  |____/ u|_____| |____/>>   |_|\_\    
 _//<<,- <<   >> ||   \\,-.|||_   <<   >>  )(  (__),-,>> \\,-. 
(__) (_/(__) (__)(_")  (_/(__)_) (__) (__)(__)      \.)   (_/  
        """)
        click.echo('### Welcome to Zendesk Search ###')
        click.echo("""
Search options:
 * Press 1 to search Zendesk
 * Press 2 to view a list of searchable fields
 * Type 'quit' to exit 
        """)
        # Prompt for choices
        op = click.prompt('Select options')
        if self.is_quit(op):
            return None
        else:
            return op

    def view_searchable_fields(self):
        """Display searchable fields for users and tickets."""
        click.echo("""
----------------------
Search {} with
{}
----------------------
Search {} with
{}
----------------------""".format(SearchTarget.USERS.value,
                                 UserParam.display(),
                                 SearchTarget.TICKETS.value,
                                 TicketParam.display()
                                ))

        self.wait()

    def search(self):
        """ZENDESK search - search page.
        
        Returned options:

            1 - Users

            2 - Tickets

            quit - Exit the app
        """
        click.echo("""
Press the number to search:
 1) {}
 2) {}
        """.format(SearchTarget.USERS.value, SearchTarget.TICKETS.value))
        op = click.prompt('Select options')
        if self.is_quit(op):
            return None
        else:
            return op

    def search_target(self, target, param_enum):
        click.echo("""
----------------------
Search {0} with
{1}
----------------------""".format(target, param_enum.display()))
        field = click.prompt('Enter field number')
        if self.is_quit(field):
            return None, None
        # Ensure the number given can be lookup in the param enum
        elif self.is_valid_field(field, param_enum):
            field = int(field)
            value = click.prompt('Enter value', default="", show_default=False)
            if self.is_quit(value):
                return None, None
            else:
                click.echo('Searching {0} for {1} with a value of {2}'.format(
                            target,
                            param_enum(field).name.lower(), 
                            value if value else '(null)')
                        )
                return field, value
        else:
            self.error_invalid_option()
            self.wait()
            return None, None

    def exit(self):
        """Require confirmation before exiting app."""
        confirmed = click.confirm('The app is shutting down. Are you sure?')
        if confirmed:
            exit()
        else:
            # Take users back to the main page
            # Potentially we can let users remain in the same page to continue
            click.clear()
    
    def error_invalid_option(self):
        """Prompt error to user that the input option is invalid."""
        click.echo('\n[ERROR] The selected option does not exist.')

    def wait(self):
        """Stop the app and press ENTER to continue."""
        click.confirm('\nPress <ENTER> to continue',
                        default=True,
                        prompt_suffix='', 
                        show_default=False)

    def is_quit(self, op):
        """Check every prompt input for quit request."""
        if op == 'quit':
            self.exit()
        return op == 'quit'

    def is_valid_field(self, op, param_enum):
        try:
            # Option should be an integer
            op = int(op)
            return op in set(p.value for p in param_enum)
        except:
            return False

