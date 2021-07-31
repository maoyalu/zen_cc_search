from zensearch.cli import CLI
from zensearch.constants import UserParam, TicketParam

def test_is_quit():
    cli = CLI()
    assert cli.is_quit('') == False
    assert cli.is_quit(None) == False

def test_is_valid_field():
    cli = CLI()
    assert cli.is_valid_field('0', UserParam) == False
    assert cli.is_valid_field('1', UserParam) == True
    assert cli.is_valid_field('5', UserParam) == False
    assert cli.is_valid_field('4', UserParam) == True
    assert cli.is_valid_field(None, UserParam) == False
    assert cli.is_valid_field('abc', UserParam) == False
    assert cli.is_valid_field('0', TicketParam) == False
    assert cli.is_valid_field('1', TicketParam) == True
    assert cli.is_valid_field('7', TicketParam) == False
    assert cli.is_valid_field('6', TicketParam) == True
    assert cli.is_valid_field(None, TicketParam) == False
    assert cli.is_valid_field('abc', TicketParam) == False
