from odoo.tests import  common
from odoo.exceptions import ValidationError


class TestHelpdeskJmpp(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.test_ticket = self.env['helpdesk.ticket'].create({'nombre': 'Test del modulo helpdesk_ticket'})
        self.user_id = self.ref('base.user_admin')

    def test_01_ticket_name(self):
        self.assertEqual(self.test_ticket.nombre, 'Test del modulo helpdesk_ticket')
    
    def test_02_ticket_userid(self):
        self.assertEqual(self.test_ticket.user_id, self.env['res.users'])
        self.test_ticket.user_id = self.user_id
        self.assertEqual(self.test_ticket.user_id.id, self.user_id)
    
    def test_03_ticket_name_not_equal(self):
        self.assertFalse(self.test_ticket.nombre == 'asdfg cvbn')

    def test_04_ticket(self):
        self.test_ticket.tiempo = 2
        self.assertEqual(self.test_ticket.tiempo, 2)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.test_ticket.tiempo = -7