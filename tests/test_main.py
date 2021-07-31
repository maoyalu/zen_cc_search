from zensearch.__main__ import App
from zensearch.database import *
from zensearch.cli import *

def test_app():
    app = App()
    assert app.cli is not None
    assert app.db is not None

def test_is_valid_user_id():
    app = App()
    assert app.is_valid_user_id(1) == True
    assert app.is_valid_user_id('1') == True
    assert app.is_valid_user_id(None) == False
    assert app.is_valid_user_id('') == False
    assert app.is_valid_user_id('abc') == False

def test_value_to_bool():
    app = App()
    assert app.value_to_bool('') == False
    assert app.value_to_bool('1') == False
    assert app.value_to_bool(None) == False
    assert app.value_to_bool('True') == True
    assert app.value_to_bool('Y') == True