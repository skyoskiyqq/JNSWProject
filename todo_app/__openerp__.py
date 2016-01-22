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
{
    'name': 'To-Do Application',
    'description': 'Manage your personal Tasks with this module.',
    'version': '0.1',
    'author': 'Peter Hu',
    'depends': ['mail'],
    'data': [
        'todo_view.xml',
        'security/ir.model.access.csv',
        'security/todo_access_rules.xml',
    ],
    'application': True,
}