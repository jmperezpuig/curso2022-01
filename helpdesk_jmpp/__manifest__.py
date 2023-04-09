# Copyright <2023> <AEODOO>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Helpdesk Jose M Perez",
    "version": "14.0.1.0.0",  
    "author": "AEODOO, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail"
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "views/helpdesk_menu.xml",
        "views/helpdesk_tag_view.xml",
        "views/helpdesk_view.xml",
        "data/delete_tag_cron.xml", 
    ],
}