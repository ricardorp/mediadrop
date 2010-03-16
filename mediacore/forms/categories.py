# This file is a part of MediaCore, Copyright 2009 Simple Station Inc.
#
# MediaCore is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MediaCore is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tw.forms import TextField, HiddenField, CalendarDatePicker, SingleSelectField, TextArea
from tw.forms.validators import Int, NotEmpty, DateConverter, DateValidator
from tw.api import WidgetsList

from mediacore.model import DBSession
from mediacore.model.categories import Category
from mediacore.lib import helpers
from mediacore.forms import Form, ListForm, SubmitButton

def option_tree(cats):
    indent = helpers.decode_entities(u'&nbsp;') * 4
    return [(None, None)] + \
        [(c.id, indent * (depth - 1) + c.name) for c, depth in cats.traverse()]

class CategoryForm(ListForm):
    template = 'mediacore.templates.admin.categories.form'
    id = None
    css_classes = ['category-form', 'form']
    submit_text = None

    # required to support multiple named buttons to differentiate between Save & Delete?
    _name = 'vf'

    fields = [
        SubmitButton('save', default='Save', named_button=True, css_classes=['f-rgt', 'btn', 'btn-save']),
        TextField('name', validator=NotEmpty),
        TextField('slug', validator=NotEmpty),
        SingleSelectField('parent_id', label_text='Parent Category', options=lambda: option_tree(Category.query.roots().order_by(Category.name.asc()))),
    ]

class CategoryRowForm(Form):
    template = 'mediacore.templates.admin.categories.row-form'
    id = None
    submit_text = None
    params = ['category', 'depth', 'first_child']

    fields = [
        HiddenField('name'),
        HiddenField('slug'),
        HiddenField('parent_id'),
        SubmitButton('delete', default='Delete', css_classes=['btn', 'btn-inline-delete']),
    ]
