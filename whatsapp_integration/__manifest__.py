{
    "name": "WhatsApp Business Integration",
    "version": "18.0.1.0.0",
    "summary": "Integración oficial con WhatsApp Business Platform (Meta)",
    "author": "Tu Empresa",
    "website": "https://tuempresa.com",
    "category": "Tools",
    "depends": ["base", "mail", "calendar", "sale_management", "purchase", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/whatsapp_config_views.xml",
        "views/whatsapp_message_views.xml",
        "views/whatsapp_template_views.xml",
        "views/sale_order_whatsapp_action.xml",
        "views/calendar_event_whatsapp_action.xml",
        "views/calendar_event_whatsapp_wizard_views.xml",
        "views/calendar_event_whatsapp_wizard_action.xml",
        "views/sale_order_whatsapp_wizard_views.xml",
        "views/sale_order_whatsapp_wizard_action.xml",
        "views/purchase_order_whatsapp_wizard_views.xml",
        "views/purchase_order_whatsapp_wizard_action.xml",
        "views/account_move_whatsapp_wizard_views.xml",
        "views/account_move_whatsapp_wizard_action.xml",
        "views/whatsapp_message_tree.xml",
        "views/whatsapp_template_tree.xml"
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "description": """
Módulo para integrar Odoo 18.0 con WhatsApp Business Platform (Meta).
Permite enviar y recibir mensajes, compartir documentos y automatizar notificaciones.
"""
}
