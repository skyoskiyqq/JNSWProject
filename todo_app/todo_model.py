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

class TodoTask(models.Model):
    _name = 'todo.task'
    name = fields.Char("Description", required=True)
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?', default=True)
    
    @api.one
    def do_toggle_done(self):
        self.is_done = not self.is_done
        return True
        
    @api.multi
    def do_clear_done(self):
        done_recs = self.search([('is_done', '=', True)])
        done_recs.write({'active': False})
        return True