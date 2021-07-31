from zensearch.constants import UserParam, TicketParam

def test_user_param_display():
    assert UserParam.display() == '1) _id\n2) name\n3) created_at\n4) verified'

def test_ticket_param_display():
    assert TicketParam.display() == '1) _id\n2) created_at\n3) type\n4) subject\n5) assignee_id\n6) tags'
