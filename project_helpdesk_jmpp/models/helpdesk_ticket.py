from odoo import  models,fields,api,_


# ====================================================================================
class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'  
    _description = 'Ticket'
    # -------------------- v12 --------------------
    _inherits = {'project.task': 'task_id'}
 
    @api.model 
    def default_get(self, fields):
        defaults = super().default_get(fields)
        defaults.update({
            # cuando cree un ticket actualizará el project de la tarea
            'project_id': self.env.ref('project_helpdesk_jmpp.project_helpdesk').id
        })
        return defaults


    task_id = fields.Many2one(
        comodel_name='project.task', 
        string='Task',
        auto_join=True, index=True, ondelete='cascade', required=True)
     

    def action_assign_to_me(self):
        self.ensure_one()
        return self.task_id.action_assign_to_me()
    
    def action_subtask(self):
        self.ensure_one()
        return self.task_id.action_subtask()
    
    def action_recurring_tasks(self):
        self.ensure_one()
        return self.task_id.action_recurring_tasks()
    
    def _message_get_suggested_recipients(self):
        self.ensure_one()
        return self.task_id._message_get_suggested_recipients()
    

    # -------------------- v12 --------------------

    # Acción correctiva (html)
    accion_correctiva = fields.Html(
        string='Acción correctiva',
        help='Indica la acción correctiva a realizar')
    
    # Accion preventiva
    accion_preventiva = fields.Html(
        string='Acción preventiva',
        help='Indica la acción preventiva a tomar')
    
