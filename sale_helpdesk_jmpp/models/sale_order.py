from odoo import models, api, fields, _ 

class OrderSale(models.Model):
    _inherit = 'sale.order'

    ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket', 
        inverse_name='sale_id', 
        string='Tickets')
    
    # para el boton de crear ticket
    def create_ticket(self):
        self.ensure_one()
        tags_del_ticket=self.order_line.mapped('product_id.helpdesk_tag_id').ids
        self.env['helpdesk.ticket'].create({
            'nombre': '%s Issue' %(self.name),
            'tag_ids': [(6,0, tags_del_ticket)],
            'sale_id': self.id
        })
    
    # para el boton Cancelar, de los pedidos
    def action_cancel(self):
        # extendemos la función del metodo llamando al super
        self.ticket_ids.cancelar_multi()
        return super().action_cancel()