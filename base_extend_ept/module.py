from docutils import nodes
from docutils.core import publish_string
from docutils.transforms import Transform, writer_aux
from docutils.writers.html4css1 import Writer
import imp
import logging
import os
import re
import shutil
import tempfile
import urllib
import urllib2
import zipfile
import zipimport

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO   # NOQA

import openerp
from openerp import modules, pooler, tools, addons
from openerp.modules.db import create_categories
from openerp.tools.parse_version import parse_version
from openerp.tools.translate import _
from openerp.osv import fields, osv, orm

class module(osv.osv):
    _inherit = 'ir.module.module'
    
    def _button_immediate_function(self, cr, uid, ids, function, context=None):
        function(cr, uid, ids, context=context)

        cr.commit()
        _, pool = pooler.restart_pool(cr.dbname, update_module=True)

        return True
        config = pool.get('res.config').next(cr, uid, [], context=context) or {}
        if config.get('type') not in ('ir.actions.act_window_close',):
            return config
        # reload the client; open the first available root menu
        menu_obj = self.pool.get('ir.ui.menu')
        menu_ids = menu_obj.search(cr, uid, [('parent_id', '=', False)], context=context)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'menu_id': menu_ids and menu_ids[0] or False}
        }
module()