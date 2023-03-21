from odoo import  models,fields 

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

    # Estados = Nuevo Asignado En proceso Pendiente Resuelto Cancelado
    estado = fields.Selection(
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
        readonly=True)

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
    
    
    