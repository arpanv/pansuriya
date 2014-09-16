import logging
import werkzeug

import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp import http
from openerp.http import request
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)
    
class AuthSignupHome_ept(openerp.addons.web.controllers.main.Home):
        
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        #context = dict((key, qcontext.get(key)) ('login', 'name', 'password'))
        #context = dict((key, qcontext.get(key)) for key in qcontext if key in ('login', 'name', 'password'): continue)
        
        values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password'))
        assert any([k for k in values.values()]), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."
        context=qcontext or None
        
        self._signup_with_values(qcontext.get('token'), values, context=context)
        request.cr.commit()

    def _signup_with_values(self, token, values, context=None):
        db, login, password = request.registry['res.users'].signup(request.cr, openerp.SUPERUSER_ID, values, token, context=context)
        request.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
#         uid = request.session.authenticate(db, login, password)
#         if not uid:
#             raise SignupError(_('Authentification Failed.'))