from openerp.addons.base_status.base_state import base_state
from openerp.addons.base_status.base_stage import base_stage
from openerp.addons.crm import crm
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
from openerp.tools import html2plaintext

class crm_helpdesk_ept(osv.osv):
    _inherit = 'crm.helpdesk'
    
    def message_get_reply_to(self, cr, uid, ids, context=None):
#        result = super(crm_helpdesk_ept, self).message_get_reply_to(cr, uid,ids,context=context)
#        result = ["%s@%s" % (record['alias_name'], record['alias_domain'])
#                    if record.get('alias_domain') and record.get('alias_name')
#                    else False
#                    for record in self.read(cr, uid, ids, ['alias_name', 'alias_domain'], context=context)]
        self_obj = self.browse(cr, 1, ids, context=context)[0]
        return ["%s" %(self_obj.section_id.reply_to or '')]
    
    def assign_sales_person(self, cr, uid, ids, context=None):
        self_obj = self.browse(cr, uid, ids)[0]
        if hasattr(self_obj, 'state') and self_obj.state == 'draft':
            msg_ids = self.pool.get('mail.message').search(cr, uid, [('model', '=', context.get('active_model')), ('res_id','=', context.get('active_id'))],context=context)
            if msg_ids:
            #Assign Sales Team to Helpdesk record
                if self_obj and self_obj.partner_id and self_obj.partner_id.section_id:
                    self.write(cr, uid, context.get('active_id'), {
                                                                   'section_id':self_obj.partner_id.section_id.id,
                                                                   'state' : 'open',
                                                                   'user_id' : self_obj.partner_id.user_id and self_obj.partner_id.user_id.id or False
                                                                   }, context=context)
                if self_obj and self_obj.partner_id and self_obj.partner_id.user_id:
                    #Get Follower of user
                    user_followers = []
#                    follower_ids = self.pool.get('mail.followers').search(cr, 1, [('res_model', '=', 'res.partner'), ('res_id', '=', self_obj.partner_id.user_id.partner_id.id)])
#                    for follower_obj in self.pool.get('mail.followers').browse(cr, 1, follower_ids):
#                        user_followers.append(follower_obj.partner_id.id)
                    user_followers.append(self_obj.partner_id.user_id.partner_id.id)
                    self.pool.get('mail.message').write(cr,uid,msg_ids,{'notified_partner_ids':[(6,0,user_followers)]})
        return True
crm_helpdesk_ept()