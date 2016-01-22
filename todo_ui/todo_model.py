# -*- coding: utf-8 -*-
##############################################################################
#
#    JNSWProject
#    Copyright 2016 HQQ <huqianglingdu@163.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from openerp.addons.base.res import res_request
from openerp.exceptions import ValidationError

class Tag(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True
    
    name = fields.Char('Name', size=40, translate=True)
    task_ids = fields.Many2many('todo.task', string='Tasks')
    parent_id = fields.Many2one('todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')
    
class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence, name'
    
    name = fields.Char('Name', size=40, translate=True)
    desc = fields.Text('Description')
    state = fields.Selection(
        [('draft', 'New'), ('open', 'Started'), ('done', 'Closed')],
        'State')
    docs = fields.Html('Documentation')
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete', (3, 2))
    date_effective = fields.Date('Effective date')
    date_changed = fields.Datetime('Last changed')
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')
    tasks = fields.One2many('todo.task', 'stage_id', 'Tasks in this stage')
    
class TodoTask(models.Model):
    _inherit = 'todo.task'
    _sql_constraints = [
        ('todo_task_name_uniq',
         'UNIQUE (name, user_id, active)',
         'Task title must be unique!')]
    
    def referencable_models(self):
        return res_request.referencable_models(self, self.env.cr, self.env.uid, self.env.context)
        
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tags', 'todo_task_tag_rel', 'task_ids', 'tag_ids', string='Tags')
    refers_to = fields.Reference(referencable_models, 'Refers to')
    stage_fold = fields.Boolean(
        string='Stage Folded?',
        compute='_compute_stage_fold',
        search='_search_stage_fold',
        inverse='_write_stage_fold')
    stage_state = fields.Selection(
        related='stage_id.state',
        string='Stage State')
    user_todo_count = fields.Integer('User To-Do Count', compute='_compute_user_todo_count')
    
    @api.one
    def _compute_user_todo_count(self):
        self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)])
    
    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold
    
    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]
    
    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold
    
    @api.one
    @api.constrains('name')
    def _check_name_size(self):
        if len(self.name) < 5:
            raise ValidationError('Must have 5 chars!')