from datetime import datetime, timedelta
import random
from urllib import urlencode
from urlparse import urljoin

from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.safe_eval import safe_eval
from openerp.tools.translate import _


class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def _get_signup_url_for_action(self, cr, uid, ids, action='login', view_type=None, menu_id=None, res_id=None, model=None, context=None):
        """ generate a signup url for the given partner ids and action, possibly overriding
            the url state components (menu_id, id, view_type) """
        res = dict.fromkeys(ids, False)
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'base_url_ept')
        for partner in self.browse(cr, uid, ids, context):
            # when required, make sure the partner has a valid signup token
            if context and context.get('signup_valid') and not partner.user_ids:
                self.signup_prepare(cr, uid, [partner.id], context=context)
                partner.refresh()

            # the parameters to encode for the query and fragment part of url
            query = {'db': cr.dbname}
            fragment = {'action': action, 'type': partner.signup_type}

            if partner.signup_token:
                fragment['token'] = partner.signup_token
            elif partner.user_ids:
                fragment['db'] = cr.dbname
                fragment['login'] = partner.user_ids[0].login
            else:
                continue        # no signup token, no user, thus no signup url!

            if view_type:
                fragment['view_type'] = view_type
            if menu_id:
                fragment['menu_id'] = menu_id
            if model:
                fragment['model'] = model
            if res_id:
                fragment['id'] = res_id

            res[partner.id] = urljoin(base_url, "?%s#%s" % (urlencode(query), urlencode(fragment)))

        return res
    def _get_signup_url(self, cr, uid, ids, name, arg, context=None):
        """ proxy for function field towards actual implementation """
        return self._get_signup_url_for_action(cr, uid, ids, context=context)
    _columns = {
        'signup_url': fields.function(_get_signup_url, type='char', string='Signup URL'),
    }
res_partner()