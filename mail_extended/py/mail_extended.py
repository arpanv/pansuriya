from openerp.osv import osv,fields
import json

import logging
_logger = logging.getLogger(__name__)

class mail_extended(osv.osv):
    _inherit = 'mail.message'

    def get_notification(self, cr, uid, ids=None,context={}):
        _logger.info('User ID : %s' %(uid))
        _logger.info('context : %s' %(context))
        messages_data =self.pool.get('mail.message').message_read(cr, uid, ids=None, domain=[['to_read', '=', True], ['starred', '=', False]],
                            message_unload_ids=None,thread_level=0,
                            context={'uid': 1, 'needaction_menu_ref': ['mail.mail_tomefeeds', 'mail.mail_starfeeds'], 'default_model': 'res.users', 'default_res_id': 1},
                            parent_id=False,
                            limit=None
                            )
        return json.dumps(messages_data) 
