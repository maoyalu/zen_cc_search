from zensearch.database import *


def test_database():
    db = Database()
    assert db.users is None
    assert db.tickets is None
    assert db.cache_user_created_at == {}
    assert db.cache_user_name == {}
    assert db.cache_user_verified == {}
    assert db.cache_ticket_created_at == {}
    assert db.cache_ticket_type == {}
    assert db.cache_ticket_subject == {}
    assert db.cache_ticket_assignee_id == {}
    assert db.cache_ticket_tags == {}

def test_database_user_init():
    db = Database()
    assert db.users is None
    assert db.tickets is None
    db.user_init()
    assert db.users is not None
    assert db.tickets is None
    # Exception is handled when the file doesn't exist
    db.config.USER_JSON = ''
    db.user_init()

def test_database_ticket_init():
    db = Database()
    assert db.users is None
    assert db.tickets is None
    # tickets need to be initialized after users
    db.user_init()
    db.ticket_init()
    assert db.tickets is not None
    # Exception is handled when the file doesn't exist
    db.config.TICKET_JSON = ''
    db.ticket_init()

def test_database_init():
    db = Database()
    assert db.users is None
    assert db.tickets is None
    db.init()
    assert db.users is not None
    assert db.tickets is not None

def test_database_cache_user():
    db = Database()
    user = User(1, 'Yalu', 'today', True)
    db.config.CACHE_USER_CREATED_AT = False
    db.config.CACHE_USER_NAME = False
    db.config.CACHE_USER_VERIFIED = False
    db.cache_user(user)
    assert db.cache_user_created_at  == {}
    assert db.cache_user_name == {}
    assert db.cache_user_verified == {}
    db.config.CACHE_USER_CREATED_AT = True
    db.cache_user(user)
    assert db.cache_user_created_at != {}
    assert len(db.cache_user_created_at) == 1
    assert db.cache_user_name == {}
    assert db.cache_user_verified == {}
    db.config.CACHE_USER_NAME = True
    db.cache_user(user)
    assert db.cache_user_created_at != {}
    assert len(db.cache_user_created_at) == 1
    assert db.cache_user_name != {}
    assert len(db.cache_user_name) == 1
    assert db.cache_user_verified == {}
    db.config.CACHE_USER_VERIFIED = True
    db.cache_user(user)
    assert db.cache_user_created_at != {}
    assert len(db.cache_user_created_at) == 1
    assert db.cache_user_name != {}
    assert len(db.cache_user_name) == 1
    assert db.cache_user_verified != {}
    assert len(db.cache_user_verified) == 1

def test_database_cache_ticket():
    db = Database()
    ticket = Ticket('1', 'today', 'There is no subject', ['test'])
    db.config.CACHE_TICKET_CREATED_AT = False
    db.config.CACHE_TICKET_SUBJECT = False
    db.config.CACHE_TICKET_TAGS = False
    db.config.CACHE_TICKET_TYPE = False
    db.config.CACHE_TICKET_ASSIGNEE_ID = False
    db.cache_ticket(ticket)
    assert db.cache_ticket_created_at == {}
    assert db.cache_ticket_subject == {}
    assert db.cache_ticket_tags == {}
    assert db.cache_ticket_type == {}
    assert db.cache_ticket_assignee_id == {}
    db.config.CACHE_TICKET_CREATED_AT = True
    db.cache_ticket(ticket)
    assert db.cache_ticket_created_at != {}
    assert len(db.cache_ticket_created_at) == 1
    assert db.cache_ticket_subject == {}
    assert db.cache_ticket_tags == {}
    assert db.cache_ticket_type == {}
    assert db.cache_ticket_assignee_id == {}
    db.config.CACHE_TICKET_SUBJECT = True
    db.cache_ticket(ticket)
    assert db.cache_ticket_created_at != {}
    assert len(db.cache_ticket_created_at) == 1
    assert db.cache_ticket_subject != {}
    assert len(db.cache_ticket_subject) == 1
    assert db.cache_ticket_tags == {}
    assert db.cache_ticket_type == {}
    assert db.cache_ticket_assignee_id == {}
    db.config.CACHE_TICKET_TAGS = True
    db.cache_ticket(ticket)
    assert db.cache_ticket_created_at != {}
    assert len(db.cache_ticket_created_at) == 1
    assert db.cache_ticket_subject != {}
    assert len(db.cache_ticket_subject) == 1
    assert db.cache_ticket_tags != {}
    assert len(db.cache_ticket_tags) == 1
    assert db.cache_ticket_type == {}
    assert db.cache_ticket_assignee_id == {}
    db.config.CACHE_TICKET_TYPE = True
    db.cache_ticket(ticket)
    assert db.cache_ticket_created_at != {}
    assert len(db.cache_ticket_created_at) == 1
    assert db.cache_ticket_subject != {}
    assert len(db.cache_ticket_subject) == 1
    assert db.cache_ticket_tags != {}
    assert len(db.cache_ticket_tags) == 1
    assert db.cache_ticket_type != {}
    assert len(db.cache_ticket_type) == 1
    assert db.cache_ticket_assignee_id == {}
    db.config.CACHE_TICKET_ASSIGNEE_ID = True
    db.cache_ticket(ticket)
    assert db.cache_ticket_created_at != {}
    assert len(db.cache_ticket_created_at) == 1
    assert db.cache_ticket_subject != {}
    assert len(db.cache_ticket_subject) == 1
    assert db.cache_ticket_tags != {}
    assert len(db.cache_ticket_tags) == 1
    assert db.cache_ticket_type != {}
    assert len(db.cache_ticket_type) == 1
    assert db.cache_ticket_assignee_id != {}
    assert len(db.cache_ticket_assignee_id) == 1

def test_search_user_id():
    db = Database()
    db.init()
    assert all(x._id == 1 for x in db.search_user_id(1))
    assert all(x.name == "Cross Barlow" for x in db.search_user_id(2))
    assert all(x.created_at == "2016-07-28T05:29:25-10:00" for x in db.search_user_id(3))
    assert all(x.verified == True for x in db.search_user_id(4))
    assert db.search_user_id(0) == []
    assert db.search_user_id(76) == []
    assert db.search_user_id(None) == []
    assert db.search_user_id('') == []

def test_search_user_name():
    db = Database()
    db.config.CACHE_USER_NAME = False
    db.init()
    assert db.cache_user_name == {}
    assert all(x.name == 'Key Mendez' for x in db.search_user_name('Key Mendez'))
    assert db.search_user_name('Lu Yang') == []
    assert db.search_user_name('') == []
    assert db.search_user_name(None) == []
    db.config.CACHE_USER_NAME = True
    db.init()
    assert db.cache_user_name != {}
    assert all(x.name == 'Key Mendez' for x in db.search_user_name('Key Mendez'))
    assert db.search_user_name('Lu Yang') == []
    assert db.search_user_name('') == []
    assert db.search_user_name(None) == []

def test_search_user_created_at():
    db = Database()
    db.config.CACHE_USER_CREATED_AT = False
    db.init()
    assert db.cache_user_created_at == {}
    assert all(x.created_at == '2016-07-04T10:28:16-10:00' for x in db.search_user_created_at('2016-07-04T10:28:16-10:00'))
    assert db.search_user_created_at('2077') == []
    assert db.search_user_created_at('') == []
    assert db.search_user_created_at(None) == []
    db.config.CACHE_USER_CREATED_AT = True
    db.init()
    assert db.cache_user_created_at != {}
    assert all(x.created_at == '2016-07-04T10:28:16-10:00' for x in db.search_user_created_at('2016-07-04T10:28:16-10:00'))
    assert db.search_user_created_at('2077') == []
    assert db.search_user_created_at('') == []
    assert db.search_user_created_at(None) == []

def test_search_user_verified():
    db = Database()
    db.config.CACHE_USER_VERIFIED = False
    db.init()
    assert db.cache_user_verified == {}
    assert all(x.verified == True for x in db.search_user_verified(True))
    assert all(x.verified == False for x in db.search_user_verified(False))
    db.config.CACHE_USER_VERIFIED = True
    db.init()
    assert db.cache_user_verified != {}
    assert all(x.verified == True for x in db.search_user_verified(True))
    assert all(x.verified == False for x in db.search_user_verified(False))

def test_search_ticket_id():
    db = Database()
    db.init()
    assert all(x._id == '4d0ab657-4c59-43e4-aab3-162753043a59' for x in db.search_ticket_id('4d0ab657-4c59-43e4-aab3-162753043a59'))
    assert all(x.created_at == "2016-06-30T07:12:07-10:00" for x in db.search_ticket_id('53ae78d0-40a9-444f-9a47-bc0bf064d2ee'))
    assert all(x.type == "task" for x in db.search_ticket_id('53867869-0db0-4b8d-9d6c-9d1c0af4e693'))
    assert all(x.subject == "A Catastrophe in Netherlands Antilles" for x in db.search_ticket_id('7ef6cf9f-121d-41e7-832c-68d811da9379'))
    assert all(x.assignee_id == 15 for x in db.search_ticket_id('59d803f6-a9cd-448c-a6bd-91ce9f044305'))
    assert all(x.tags == ['New Mexico', 'Nebraska', 'Connecticut', 'Arkansas'] for x in db.search_ticket_id('13aafde0-81db-47fd-b1a2-94b0015803df'))
    assert db.search_ticket_id('') == []
    assert db.search_ticket_id(None) == []

def test_search_ticket_created_at():
    db = Database()
    db.config.CACHE_TICKET_CREATED_AT = False
    db.init()
    assert db.cache_ticket_created_at == {}
    assert all(x.created_at == '2016-04-28T11:19:34-10:00' for x in db.search_ticket_created_at('2016-04-28T11:19:34-10:00'))
    assert db.search_ticket_created_at('2077') == []
    assert db.search_ticket_created_at('') == []
    assert db.search_ticket_created_at(None) == []
    db.config.CACHE_TICKET_CREATED_AT = True
    db.init()
    assert db.cache_ticket_created_at != {}
    assert all(x.created_at == '2016-04-28T11:19:34-10:00' for x in db.search_ticket_created_at('2016-04-28T11:19:34-10:00'))
    assert db.search_ticket_created_at('2077') == []
    assert db.search_ticket_created_at('') == []
    assert db.search_ticket_created_at(None) == []

def test_search_ticket_type():
    db = Database()
    db.config.CACHE_TICKET_TYPE = False
    db.init()
    assert db.cache_ticket_type == {}
    assert all(x.type == 'task' for x in db.search_ticket_type('task'))
    # Ensure all tickets with no type is stored as None instead of empty string
    assert all(ticket.type != '' for ticket in db.tickets.values())
    assert all(x.type is None for x in db.search_ticket_type(None))
    assert all(x.type is None for x in db.search_ticket_type(''))
    assert db.search_ticket_type('????') == []
    db.config.CACHE_TICKET_TYPE = True
    db.init()
    assert db.cache_ticket_type != {}
    assert all(x.type == 'task' for x in db.search_ticket_type('task'))
    # Ensure all tickets with no type is stored as None instead of empty string
    assert all(ticket.type != '' for ticket in db.tickets.values())
    assert all(x.type is None for x in db.search_ticket_type(None))
    assert all(x.type is None for x in db.search_ticket_type(''))
    assert db.search_ticket_type('????') == []

def test_search_ticket_subject():
    db = Database()
    db.config.CACHE_TICKET_SUBJECT = False
    db.init()
    assert db.cache_ticket_subject == {}
    assert all(x.subject == 'A Problem in Malawi' for x in db.search_ticket_subject('A Problem in Malawi'))
    assert db.search_ticket_subject('This cannot be a subject title!') == []
    assert db.search_ticket_subject('') == []
    assert db.search_ticket_subject(None) == []
    db.config.CACHE_TICKET_SUBJECT = True
    db.init()
    assert db.cache_ticket_subject != {}
    assert all(x.subject == 'A Problem in Malawi' for x in db.search_ticket_subject('A Problem in Malawi'))
    assert db.search_ticket_subject('This cannot be a subject title!') == []
    assert db.search_ticket_subject('') == []
    assert db.search_ticket_subject(None) == []

def test_search_ticket_assignee_id():
    db = Database()
    db.config.CACHE_TICKET_ASSIGNEE_ID = False
    db.init()
    assert db.cache_ticket_assignee_id == {}
    assert all(x.assignee_id == 1 for x in db.search_ticket_assignee_id(1))
    assert len(db.search_ticket_assignee_id(1)) == 2
    assert all(x.assignee_id == None for x in db.search_ticket_assignee_id(None))
    assert db.search_ticket_assignee_id(0) == []
    assert db.search_ticket_assignee_id('') == []
    db.config.CACHE_TICKET_ASSIGNEE_ID = True
    db.init()
    assert db.cache_ticket_assignee_id != {}
    assert all(x.assignee_id == 1 for x in db.search_ticket_assignee_id(1))
    assert len(db.search_ticket_assignee_id(1)) == 2
    assert all(x.assignee_id == None for x in db.search_ticket_assignee_id(None))
    assert db.search_ticket_assignee_id(0) == []
    assert db.search_ticket_assignee_id('') == []

def test_search_ticket_tags():
    db = Database()
    db.config.CACHE_TICKET_TAGS = False
    db.init()
    assert db.cache_ticket_tags == {}
    assert all('New Mexico' in x.tags for x in db.search_ticket_tags('New Mexico'))
    assert db.search_ticket_tags(0) == []
    assert db.search_ticket_tags('') == []
    assert db.search_ticket_tags(None) == []
    db.config.CACHE_TICKET_TAGS = True
    db.init()
    assert db.cache_ticket_tags != {}
    assert all('New Mexico' in x.tags for x in db.search_ticket_tags('New Mexico'))
    assert db.search_ticket_tags(0) == []
    assert db.search_ticket_tags('') == []
    assert db.search_ticket_tags(None) == []

def test_user():
    user_1 = User(1, 'user_1', 'future')
    assert user_1._id == 1
    assert user_1.name == 'user_1'
    assert user_1.created_at == 'future'
    assert user_1.verified == False
    assert user_1.tickets == []
    user_2 = User(2, 'user_2', 'undertale', True)
    assert user_2._id == 2
    assert user_2.name == 'user_2'
    assert user_2.created_at == 'undertale'
    assert user_2.verified == True
    assert user_2.tickets == []

def test_ticket():
    ticket_1 = Ticket('a', 'future', 'subject_1', ['tag_1'])
    assert ticket_1._id == 'a'
    assert ticket_1.created_at == 'future'
    assert ticket_1.subject == 'subject_1'
    assert ticket_1.tags == ['tag_1']
    assert ticket_1.type == None
    assert ticket_1.assignee_id == None
    assert ticket_1.assignee == None
    ticket_2 = Ticket('b', 'today', 'subject_2', ['tag_1'], 'type')
    assert ticket_2._id == 'b'
    assert ticket_2.created_at == 'today'
    assert ticket_2.subject == 'subject_2'
    assert ticket_2.tags == ['tag_1']
    assert ticket_2.type == 'type'
    assert ticket_2.assignee_id == None
    assert ticket_2.assignee == None
    ticket_3 = Ticket('c', 'never', 'subject_3', ['tag_1'], assignee_id=1)
    assert ticket_3._id == 'c'
    assert ticket_3.created_at == 'never'
    assert ticket_3.subject == 'subject_3'
    assert ticket_3.tags == ['tag_1']
    assert ticket_3.type == None
    assert ticket_3.assignee_id == 1
    assert ticket_3.assignee == None

def test_user_assign():
    user = User(1, 'user_1', 'future')
    ticket_1 = Ticket('a', 'future', 'subject_1', ['tag_1'])
    ticket_2 = Ticket('b', 'today', 'subject_2', ['tag_1'], 'type')
    user.assign(ticket_1)
    assert len(user.tickets) == 1
    user.assign(ticket_1)
    assert len(user.tickets) == 1
    user.assign(ticket_2)
    assert len(user.tickets) == 2