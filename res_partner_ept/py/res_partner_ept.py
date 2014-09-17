from openerp.osv import fields, osv
from openerp.tools.translate import _
class Partner(osv.Model):
    "Partner"
    _inherit = 'res.partner'

    _columns = {     
                    'registration_type' : fields.boolean('Registred through website?'),
                    'state' : fields.selection([('on_draft','Draft'),
                                                ('on_approval','Approved'),
                                                ('on_reject','Rejected')],string='State'),
                    #Personal Information
                    'first_name' : fields.char('First Name'),
                    'second_name'  :fields.char('Second Name'),
                    'last_name'  :fields.char('Last Name'),
                    'anniversary_date_ept':fields.date('Anniversary Date'),
                    'birthdate_ept':fields.date('Birthdate'),
                    'gender_ept':fields.selection([('male','Male'),('female','Male')],string="Gender"),
                    
                    #Contact Informations
                    'alternate_email_ept':fields.char('Alternate Email'),
                    'contact_mobile_number_ept':fields.char('Contact Mobile Number'),
                    'contact_number_ept':fields.char('Contact Number'),
                    'extension_ept':fields.char('Extension'),
                    
                    #Company Informations
                    'company_name_ept':fields.char('Company Name'),
                    'owner_name_ept':fields.char('Owner Name'),
                    'company_type' : fields.selection([('individual','Individual'),
                                                       ('partnership','Partnership'),
                                                       ('private_ltd','Private Ltd'),
                                                       ('limited_liability_partnership','Limited Liability Partnership'),
                                                       ],string = 'Company Type'),                    
                    
                    #Business Information
                    'nature_of_business_ept':fields.selection([('jewellary_manufacturer','Jewellary Manufacturer'),
                                                               ('polish_distributor','Polish Distributor'),
                                                               ('retailer','Retailer'),
                                                               ('other','Other'),
                                                               ],string='Nature of Business'),
                
                    'broker_ept':fields.boolean('Broker'),
                    'agent_ept':fields.boolean('Agent'),
                    'dun_bradstreet_number_ept':fields.char('Dun & Bradstreet Number'),
                    
                    #Member Of
                    'members_of_trade_portal_ept':fields.char('Members of Trade Portal'),
                    'members_of_trade_association_ept':fields.char('Members of Trade Association'),
                    
                    #Third Party Reference
                    'third_party_name_ept':fields.char('Name'),
                    'third_party_contact_number_ept':fields.char('Contact'),
                    'third_party_address_ept':fields.text('Address'),
                    'third_party_email_ept':fields.char('Email'),
                    
                    #Bank Details.
                    'branch_name_ept':fields.char('Branch Name'),
                    'branch_address_ept':fields.text('Branch Address'),
                    'branch_city_ept':fields.char('Branch City'),
                    'branch_state_ept':fields.char('Branch State'),
                    'branch_postal_code_ept':fields.char('Branch zip code'),
                    'is_manufacturer' : fields.boolean('Manufacturer'),
                }
    _defaults = {
                 'registration_type' : False,
                 'state' : 'on_draft',
                 }
    def set_body(self,cr,uid,ids,new_state):
        body = ''
        object = self.browse(cr,uid,ids[0])
        state = ''
        if object.state == 'on_draft' :
            state = 'Draft'
        elif object.state == 'on_approval':
            state = "Approved"
        elif object.state == 'on_reject':
            state = "Rejected"
        body = 'State changed from <b> ' + state + '</b> To <b> ' + new_state + '.</b>'
        return body
    
    def set_to_approve(self, cr, uid, ids=None, context={}):
        user_id = self.pool.get('res.users').search(cr, uid, ['|',('active','=',True),('active','=',False),('partner_id','=',ids[0])])
        if user_id:
            self.pool.get('res.users').write(cr, uid, user_id, {'active':True}, context=context)
            self.send_email(cr, uid, ids, context=context)
            self.message_post(cr, uid, ids[0], body=self.set_body(cr, uid, ids, 'Approved'), subject='', type='notification' , context=context)
        return self.write(cr, uid, ids, {'state':'on_approval'}, context=context)
    
    def set_to_draft(self, cr, uid, ids=None, context={}):
        self.message_post(cr, uid, ids[0], body=self.set_body(cr, uid, ids, 'Draft'), subject='', type='notification' , context=context)
        return self.write(cr, uid, ids, {'state':'on_draft'}, context=context)
    
    def set_to_reject(self, cr, uid, ids=None, context={}):
        user_id = self.pool.get('res.users').search(cr, uid, ['|',('active','=',True),('active','=',False),('partner_id','=',ids[0])])
        if user_id:
            self.pool.get('res.users').write(cr, uid, user_id, {'active':False}, context=context)
        self.message_post(cr, uid, ids[0], body=self.set_body(cr, uid, ids, 'Rejected'), subject='', type='notification' , context=context)
        return self.write(cr, uid, ids, {'state':'on_reject'}, context=context)
    
    def send_email(self, cr, uid, ids, context={}):
        email_template=self.pool.get('email.template')
        ir_model_data = self.pool.get('ir.model.data')
        template_id = None
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'res_partner_ept', 'cust_reg_email_template')[1]
        except ValueError:
            template_id = False
        if template_id :    
            template=email_template.browse(cr,uid,template_id)
            post_values={}
            subtype="mail.mt_comment"
            subject =email_template.render_template(cr, uid, template.subject, 'res.partner', ids[0], context)
            body = email_template.render_template(cr, uid, template.body_html, 'res.partner', ids[0], context)
            post_values.update({'partner_ids':ids})
            self.message_post(cr, uid, ids[0], body=body, subject=subject, type='email' , subtype=subtype, context=context, **post_values)
        return True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    