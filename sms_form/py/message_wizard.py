from openerp.osv import osv,fields
from openerp.tools.translate import _
import urllib
import re



class message(osv.osv):
    _name='message.ept'
    _res_name="seq_ept"
    _order = "create_date desc"
    _columns= {
               'create_date':fields.datetime('Created On'),
               'customer_name': fields.char('Customer Name',size=156),
               'company_name':fields.char('Company',size=156),
               'address':fields.text('Address*'),
               'contry_code' : fields.char('Contry Code*',size=26),
               'phone_no':fields.char('Mobile No.*',size=256),
               'email1':fields.char('Email*',size=256),
               'email2' : fields.char('Company Email*',size=256),
               'required_area':fields.char('Required Area(Sq.foot)*',size=256),
               'four_wheeler':fields.integer('4 Wheeler'),
               'two_wheeler':fields.integer('2 Wheeler'),
               'seq_ept':fields.char('Form Number',size=156,readonly=True),
               'change_state' : fields.boolean('States'),
               'business_nature':fields.selection([
                                   ('dimond_manufacturer','Dimond Manufacturer'),
                                   ('export','Exporter'),
                                   ('trade','Trader'),
                                   ('broker','Broker'),
                                   ('other','Other'),
                                   ],'Nature Of Business*'),
               'partner1':fields.char('1',size=256),
               'partner2':fields.char('2',size=256),
               'partner3':fields.char('3',size=256),
               'partner4':fields.char('4',size=256),
               'partner5':fields.char('5',size=256),
               'phone1':fields.char('phone1',size=256),
               'phone2':fields.char('phone2',size=256),
               'phone3':fields.char('phone3',size=256),
               'phone4':fields.char('phone4',size=256),
               'phone5':fields.char('phone5',size=256),
               'terms_agreed' : fields.boolean('Terms & Conditions Agreed ?'),
               'lend_line_no' : fields.char('Land Line No.',size=256),
               'country_id' : fields.many2one('res.country','Country'),
               'city' : fields.char('City',size=256),


            }
    def number_validater(self, cr, uid, ids, number, context={}):
#         if not re.match(r'^[0-9]', number):
#             warning = {
#                         'title': _('Validation Warning!'),
#                         'message': _("'You have Entered Invalid Mobile Number")
#                      }
#             return {'warning': warning}
        return number
        
    def mail_validater(self, cr, uid, ids, mail_address,context={}):
        if mail_address and not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mail_address):
            warning = {
                        'title': _('Validation Warning!'),
                        'message': _("'You have Entered Invalid Email Address")
                     }
            return {'value':{'email1':''}, 'warning': warning}
        return {}
    

    def mail_validater2(self, cr, uid, ids, mail_address,context={}):
        
        if mail_address and not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mail_address):
            warning = {
                        'title': _('Validation Warning!'),
                        'message': _("'You have Entered Invalid Email Address")
                     }
            return {'value':{'email2':''}, 'warning': warning}
        return {}
            
        
    def create(self, cr, uid, vals, context=None):
        if vals.get('seq_ept','/')=='/':
            vals['seq_ept'] = self.pool.get('ir.sequence').get(cr, uid, 'form.sequence') or '/'
        vals.update({
                     'change_state' : True
                     })
        return super(message, self).create(cr, uid, vals, context=context)
    
    def submit_information(self, cr, uid, ids, context={}):
        self_obj = self.browse(cr, uid, ids[0])
        return True
    
    
    def _send_sms(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr,uid,ids[0])
        if data :
            gateway_ids = self.pool.get('sms.smsclient').search(cr,uid,[])
            if gateway_ids :
                gateway = self.pool.get('sms.smsclient').browse(cr,uid,gateway_ids[0])
                if gateway:
	            sms = "Dear "+ str(data.customer_name) +", Thank you for your registration, your Application ID : "+str(data.seq_ept)+", use it for future reference, for any query call 91 22 4321 5555."
                    url = gateway.url
                    name = url
                    if gateway.method == 'http':
                        prms = {}
                        for p in gateway.property_ids:
                            if p.type == 'user':
                                prms[p.name] = p.value
                            elif p.type == 'password':
                                prms[p.name] = p.value
                            elif p.type == 'to':
                                prms[p.name] = '%s%s' %(data.contry_code,data.phone_no)
                            elif p.type == 'sms':
                                prms[p.name] = sms
                            elif p.type == 'extra':
                                prms[p.name] = p.value
                        params = urllib.urlencode(prms)
                        name = url + "?" + params
                    queue_obj = self.pool.get('sms.smsclient.queue')
                    vals = {
                            'name': name,
                            'gateway_id': gateway.id,
                            'state': 'draft',
                            'mobile': '%s%s' %(data.contry_code,data.phone_no),
                            'msg': sms,
                            'validity': gateway.validity, 
                            'classes': gateway.classes, 
                            'deffered': gateway.deferred, 
                            'priorirty': gateway.priority, 
                            'coding': gateway.coding, 
                            'tag': gateway.tag, 
                            'nostop': gateway.nostop,
                        }
                    queue_obj.create(cr, uid, vals, context=context)
        return True    
    
    def _send_email(self,cr,uid,ids,context=None):
        ir_mail_server = self.pool.get('ir.mail_server')
        data = self.browse(cr,uid,ids[0])
        mail_server = ir_mail_server.search(cr,uid,[])
        mail_server_obj = False
        if mail_server :
            mail_server_obj = ir_mail_server.browse(cr,uid,mail_server[0])
        if mail_server_obj:
            if data :
                body = """<p>Thank you for your participation, your Application ID is <b>%s</b>, please fell free to call us at 022 4321 5555 for any query.</p><br><br>
                        --<br>
                        Best Regards<br>
                        Surat Diamond Bourse Committee
                       """ %(data.seq_ept)
                msg = ir_mail_server.build_email(
                                email_from = mail_server_obj.smtp_user,
                                email_to = ['%s <%s>' % (data.customer_name, data.email1)],
                                subject = 'Surat Diamond Bourse Committee : Confirmation Form No.',
                                body = body,
                                body_alternative = '',
                                email_cc = False,
                                reply_to = False,
                                attachments = False,
                                message_id = False,
                                references = False,
                                object_id = False,
                                subtype = 'html',
                                subtype_alternative = 'plain')
                res = ir_mail_server.send_email(cr, uid, msg,
                                mail_server_id=mail_server_obj.id, context=context)
        return True
    
    def send_message(self, cr, uid, ids, context = {}):
        self_obj = self.browse(cr, uid, ids[0])
        if not self_obj.terms_agreed :
            raise osv.except_osv(_('Warning !'),_("You can't submit form without accept Terms & Conditions !"))
        
        #send SMS
        self._send_sms(cr,uid,ids,context=context)
        #send Email
        self._send_email(cr,uid,ids,context=context)
        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'sms_form', 'message_send_notification_ept')
        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id
          
        value = {
                   'name': _('Thank You'),
                   'view_type': 'form',
                   'res_model': 'message.notification.ept',
                   'view_id': False,
                   'context': context,
                   'views': [(view_id, 'form')],
                   'view_mode' : 'form',
                   'type': 'ir.actions.act_window',
                   'target': 'new',
                   'nodestroy': True,
                   'flags' : { 'search_view': False, 
                        'sidebar' : False,
                        'views_switcher' : False, 
                        'action_buttons' : False,
                        'pager': False
                        }
                    
               }
        return value
    
class partner_message_ept(osv.osv):
    _name='partner.message.ept'
    _columns = {
                'partner_id':fields.integer('Partner',size=256),
                'name':fields.char('Name',size=256),
                'contact':fields.char('contect',size=256),
                'email' : fields.char('Email',size=256),
                }
    
    
class message_notification(osv.osv_memory):
    _name = 'message.notification.ept'
    _columns = {
                'name' :fields.char('Name', size=1)
                }
    
    def form_close(self, cr, uid, ids, context={}):
        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'sms_form', 'message_form_view_ept')
        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id
 
        value = {
                   'name': _('Message'),
                   'view_type': 'form',
                   'res_model': 'message.ept',
                   'view_id': False,
                   'context': context,
                   'views': [(view_id, 'form')],
                   'view_mode' : 'form',
                   'type': 'ir.actions.act_window',
                   'target': 'inline',
                   'nodestroy': True,
                   'flags' : { 'search_view': False, 
                        'sidebar' : False,
                        'views_switcher' : False, 
                        'action_buttons' : False,
                        'pager': False
                        }
                    
               }
        return value
message_notification()
