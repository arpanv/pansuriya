# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import logging
import werkzeug

import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp import http
from openerp.http import request
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class AuthSignupHome(openerp.addons.web.controllers.main.Home):

    @http.route('/web/registration_complete', type="http", auth="public", website=True)
    def web_registration_complete(self,*args,**kw):
        return request.render("auth_signup.thankyou", {})

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                #return super(AuthSignupHome, self).web_login(*args, **kw)
                #return request.render("auth_signup.thankyou")
                return request.redirect("/web/registration_complete")
            except (SignupError, AssertionError), e:
                qcontext['error'] = _(e.message)

        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        res_country = pool.get('res.country')
        res_state = pool.get('res.country.state')
        bank_type = pool.get('res.partner.bank.type')
        prefix = pool.get('res.partner.title')
        prefix_objects = prefix.browse(cr,uid,prefix.search(cr,uid,[]))
        country_objects = res_country.browse(cr,uid,res_country.search(cr,uid,[]))
        state_objects = res_state.browse(cr,uid,res_state.search(cr,uid,[]))
        bank_types = bank_type.browse(cr,uid,bank_type.search(cr,uid,[]))
        qcontext = qcontext or {}
        qcontext.update({
                  'country_objects':country_objects,
                  'state_objects':state_objects,
                  'bank_types':bank_types,
                  'prefix_objects':prefix_objects,
                  })
        
        return request.render('auth_signup.signup', qcontext )
