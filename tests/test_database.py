from zensearch.database import *


def test_database():
    db = Database()
    assert db.users is None
    assert db.tickets is None

def test_database_user_init():
    db = Database()
    assert db.users is None
    assert db.tickets is None
    db.user_init()
    assert db.users is not None
    assert db.tickets is None

def test_database_ticket_init():
    db = Database()
    assert db.users is None
    assert db.tickets is None
    # tickets need to be initialized after users
    db.user_init()
    db.ticket_init()
    assert db.tickets is not None

def test_database_init():
    db = Database()
    assert db.users is None
    assert db.tickets is None
    db.init()
    assert db.users is not None
    assert db.tickets is not None

def test_search_user_id():
    db = Database()
    db.init()
    assert all(x._id == 1 for x in db.search_user_id(1))
    assert all(x.name == "Cross Barlow" for x in db.search_user_id(2))
    assert all(x.created_at == "2016-07-28T05:29:25-10:00" for x in db.search_user_id(3))
    assert all(x.verified == True for x in db.search_user_id(4))
    assert db.search_user_id(0) is None
    assert db.search_user_id(76) is None
