from odoo import  models,fields,api

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'  
    _description = 'Action'

    name = fields.Char(string='Nombre')
    date = fields.Date(string='Fecha')
    # una accion solo puede estar en un ticket. Son N:1 (como las líneas de una factura)
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket', 
        string='Ticket')
    
class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'  
    _description = 'Tag'

    name = fields.Char(string='Nombre')

    # un tag tiene uno o muchos ticket y un ticket tiene uno o muchos tag. Es N:N
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket', 
        relation='helpdesk_ticket_tag_rel',
        column1='tag_id',
        column2='ticket_id',
        string='Tickets')

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'  
    _description = 'Ticket'

    nombre = fields.Char(
        string='Nombre',
        required=True)
    descripcion = fields.Text(
        string='Descripcion')
    fecha = fields.Date(
        string='Fecha')
    
    # un ticket puede tener muchas accciones. Son 1:N (una factura puede tener muchas línas)
    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id', 
        string='Actions')
    
    # un ticket tiene uno o muchos tag y un tag tiene uno o muchos ticket. Es N:N
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag', 
        relation='helpdesk_ticket_tag_rel',
        column1='ticket_id',
        column2='tag_id',
        string='Tags')
    
    # un user puede tener uno o muchos ticket PERO un ticket solo puede tener un usurio. Es un 1:N
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='Asignado a')
    

    # Estados = Nuevo Asignado En proceso Pendiente Resuelto Cancelado
    state = fields.Selection(
        string='Estado', 
        default='nuevo',
        selection=[('nuevo', 'Nuevo'), 
                   ('asignado', 'Asignado'),
                   ('proceso', 'En proceso'), 
                   ('pendiente', 'Pendiente'),
                   ('resuelto', 'Resuelto'), 
                   ('cancelado', 'Cancelado')])
    
    # Tiempo dedicado (en horas)
    tiempo = fields.Float(
        string='Tiempo')
    
    # Asignado (tipo check), nos piden que sea solo de lectura
    asignado = fields.Boolean(
        string='Asignado',
        # readonly=True,
        compute='_compute_asignado') # ahora será unn campo calculado

    # Fecha limite
    fecha_limite = fields.Date(
        string='Fecha Límite')
    
    # Acción correctiva (html)
    accion_correctiva = fields.Html(
        string='Acción correctiva',
        help='Indica la acción correctiva a realizar')
    
    # Accion preventiva
    accion_preventiva = fields.Html(
        string='Acción preventiva',
        help='Indica la acción preventiva a tomar')
    
    def asignar(self):
        self.ensure_one()
        self.write({
            'estado': 'asignado',
            'asignado': True
        })

    def proceso(self):
        self.ensure_one()
        self.estado = 'proceso'

    def pendiente(self):
        self.ensure_one()
        self.estado = 'pendiente'

    def finalizar(self):
        self.ensure_one()
        self.estado = 'resuelto'

    def cancelar(self):
        self.ensure_one()
        self.estado = 'cancelado'

    # hacer que el campo asignado sea calculado:
    @api.depends('user_id')
    def _compute_asignado(self):
        for elem in self:
            # si existe user_id --> asignado será True. El usa self a la decha del =
            elem.asignado = elem.user_id and True or False 
    
    # hacer un campo calculado que indique, dentro de un ticket, el número de tickets que tiene nuestro user:
    ticket_qty = fields.Integer(
        string='Número de Tickets',
        compute='_compute_ticket_qty')
    
    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for elem in self:
            elem.ticket_qty = len(self.env['helpdesk.ticket'].search([('user_id','=',elem.user_id.id)]))

    # crear un campo nombre de etiqueta. Y un botón que cree la nueva etiqueta con ese nombre y la asocie al ticket
    tag_name = fields.Char(
        string='Tag Name')
    

    def create_tag(self):
        self.ensure_one() # pq estará en el form de un ticket
        # opcion 1
        self.write({
            'tag_ids': [(0,0, {'name': self.tag_name})] # la key debe coincidir con el campo definido en la relacion
        })
        # # opcion 2
        # tag = self.env['helpdesk.ticket.tag'].create({'name': self.tag_name})
        # self.write({'tag_ids': [(4,tag.ids,0)]}) # se añade el id a la relacion
        # # opcion 3
        # tag = self.env['helpdesk.ticket.tag'].create({'name': self.tag_name})
        # self.write({'tag_ids': [(6,0,tag.ids)]}) # se añaden todos los id a la relacion
        self.tag_name = False # para limpiar el cuadro de texto
    

    