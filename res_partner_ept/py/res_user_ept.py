from datetime import datetime, timedelta
import random
from urlparse import urljoin
import werkzeug

from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr
from ast import literal_eval
from openerp.tools.translate import _
import base64

class SignupError(Exception):
    pass

class res_users_ept(osv.Model):
    _inherit = 'res.users'
    
    def _signup_create_user(self, cr, uid, values, context=None):
        """ create a new user from the template user """
        ir_config_parameter = self.pool.get('ir.config_parameter')
        template_user_id = literal_eval(ir_config_parameter.get_param(cr, uid, 'auth_signup.template_user_id', 'False'))
        assert template_user_id and self.exists(cr, uid, template_user_id, context=context), 'Signup: invalid template user'

        # check that uninvited users may sign up
        if 'partner_id' not in values:
            if not literal_eval(ir_config_parameter.get_param(cr, uid, 'auth_signup.allow_uninvited', 'False')):
                raise SignupError('Signup is not allowed for uninvited users')

        assert values.get('login'), "Signup: no login given for new user"
        assert values.get('partner_id') or values.get('name'), "Signup: no name or partner given for new user"

        # create a copy of the template user (attached to a specific partner_id if given)
        #values['active'] = False
        context = dict(context or {}, no_reset_password=True)
        try:
            with cr.savepoint():
                new_id = self.copy(cr, uid, template_user_id, values, context=context)
                self.write(cr,uid,[new_id],{'active':False},context=context)
                self.create_partner(cr, uid, new_id, context=context)
                return new_id
        except Exception, e:
            # copy may failed if asked login is not available.
            raise SignupError(ustr(e))
        
    def create_partner(self, cr, uid, id, context=None):
        user_obj = self.browse(cr, uid, id)
        values = {
                     'registration_type' : True,
                     'title' : context.get('prefix',False),
                     'first_name' : context.get('name',False),
                     'last_name'  : context.get('lastname',False),
                     'gender_ept' : context.get('gender',False),
                     'birthdate_ept' : context.get('dob',False),
                     'anniversary_date_ept' : context.get('anniversary',False),
                     'email' : context.get('login'),
                     'alternate_email_ept':context.get('alt_email',False),
                     'mobile':context.get('mobile_no',False),
                     'contact_number_ept':context.get('contact_no',False),
                     'extension_ept':context.get('extension',False),
                     'fax' : context.get('fax_no',False),
                     'name':context.get('company_name',False),
                     'owner_name_ept':context.get('owner_name',False),
                     'company_type' : context.get('company_type', False),
                     'street' : context.get('company_address',False),
                     'city' : context.get('city',False),
                     'state_id' :  context.get('state',False),
                     'country_id' : context.get('country',False),
                     'phone' :context.get('telephone',False),
                     'zip' : context.get('zip',False),
                     'website' : context.get('company_website',False),                    
                     'nature_of_business_ept':context.get('nature_of_business',False),
                     'broker_ept' : True if context.get('broker').lower()=='yes' else False,
                     'agent_ept' : True if context.get('agent').lower()=='yes' else False,  
                     'dun_bradstreet_number_ept':context.get('dun_bradstreet_no',False),
                     'members_of_trade_portal_ept':context.get('member_of_trade_portal',False),
                     'members_of_trade_association_ept':context.get('member_of_teade_association',False),
                     'third_party_name_ept':context.get('third_name',False),
                     'third_party_contact_number_ept':context.get('third_contact_number',False),
                     'third_party_address_ept':context.get('third_address',False),
                     'third_party_email_ept':context.get('third_email',False),
                  }
        self.pool.get('res.partner').write(cr,uid,[user_obj.partner_id.id],values,context=context)
        #bank data
        bank_values = {
                       'partner_id' :  user_obj.partner_id.id,
                       'state' : context.get('type_of_account',False),
                       'acc_number' : context.get('account_no'),
                       'bank_name' : context.get('bank_name',False),
                       'owner_name' : context.get('branch_name',False),
                       'street' : context.get('branch_address',False),
                       'city' : context.get('bank_city',False),
                       'state_id' : context.get('bank_state',False),
                       'zip' : context.get('bank_zip_code',False),
                       }
        res_parner_bank_obj = self.pool.get('res.partner.bank').create(cr, uid, bank_values, context=context)
        
        #attachmnet data
        if context.get('proof_of_business_reg_copy') :
            attach_business_reg_copy_values={
                         'name': 'Business Registration Copy',
                         'datas_fname': 'Business Registration Copy',
                         'res_model': 'res.partner',
                         'res_id': user_obj.partner_id.id,
                         'datas': base64.encodestring(context.get('proof_of_business_reg_copy').stream.read() if 'proof_of_business_reg_copy' in context else '' ),
                         }
            new_business_reg_id = self.pool.get('ir.attachment').create(cr, uid, attach_business_reg_copy_values,context=context)
        if context.get('photo_id_proof') : 
            attach_photo_values={
                         'name': 'Photo Identity Proof',
                         'datas_fname': 'Photo Identity Proof',
                         'res_model': 'res.partner',
                         'res_id': user_obj.partner_id.id,
                         'datas': base64.encodestring(context.get('photo_id_proof').stream.read() if 'photo_id_proof' in context else ''),
                         }
            new_photo_id = self.pool.get('ir.attachment').create(cr, uid, attach_photo_values,context=context)
  
        self._send_email(cr, uid, user_obj.id, user_obj.partner_id.id,context=context)
        return True
    
    def _send_email(self, cr, uid, id,partner_id, context={}):
        email_template=self.pool.get('email.template')
        ir_model_data = self.pool.get('ir.model.data')
        template_id = None
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'res_partner_ept', 'cust_reg_req_email_template')[1]
        except ValueError:
            template_id = False
        if template_id :    
            template=email_template.browse(cr,uid,template_id)
            post_values={}
            subtype="mail.mt_comment"
            subject =email_template.render_template(cr, uid, template.subject, 'res.partner', partner_id, context)
            body = email_template.render_template(cr, uid, template.body_html, 'res.partner', partner_id, context)
            post_values.update({'partner_ids':[partner_id]})
            self.pool.get('res.partner').message_post(cr, uid, [partner_id], body=body, subject=subject, type='email' , subtype=subtype, context=context, **post_values)
        return True