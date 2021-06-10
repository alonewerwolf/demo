# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Demo(models.Model):
    _name = 'demo.demo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'demo.demo'

    name = fields.Char(default=lambda self: 'Demo ' + str(self.env.uid))
    partner_id = fields.Many2one('res.partner' ,string="Customer")
    done_date = fields.Datetime(string='Done Date')
    user_id = fields.Many2one('res.users',string='Salesperson')
    state = fields.Selection([('planned', 'Planned'), ('done', 'Done'), ('cancelled', 'Cancelled')], string='State')
    lead_id = fields.Many2one('crm.lead', "Lead", readonly=True)

class Lead(models.Model):
    _inherit = 'crm.lead'

    demo_ids = fields.One2many('demo.demo', 'lead_id', string='Demos')
    demo_count = fields.Integer(compute='_compute_demo_count', string="Number of Quotations")

    #Not completely understand 11
    @api.depends('demo_ids')
    def _compute_demo_count(self):
        self.demo_count = (90 * self.expected_revenue) / 100


    def create_demo(self):
        return {
            'res_model': 'demo.demo',
            'type': 'ir.actions.act_window',
            'context': {},
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('demo.demo_view_form').id,
            'target': 'new'
        }

    # 11
    def action_view_demo(self):
        return {
            'res_model': 'demo.demo',
            'type': 'ir.actions.act_window',
            'context': {'lead_id': self.id},
            'view_mode': 'list',
            'view_type': 'list',
            'view_id': self.env.ref('demo.demo_demo_list_view').id,
            'target': 'current'
        }

