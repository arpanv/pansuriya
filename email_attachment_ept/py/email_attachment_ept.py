import base64
import logging

from openerp import netsvc
from openerp.osv import osv, fields
from openerp.osv import fields
from openerp import tools
from openerp.tools.translate import _
from urllib import urlencode, quote as quote
import time

class email_attachment_eept(osv.osv):
    _inherit = "email.template"
    
    _columns = {
                "email_attachment_ids" : fields.many2many("ir.actions.report.xml","email_attachment","temp_id","rep_id","Attachment")
                }
    
    def generate_email(self, cr, uid, template_id, res_id, context=None):
        """Generates an email from the template for given (model, res_id) pair.

           :param template_id: id of the template to render.
           :param res_id: id of the record to use for rendering the template (model
                          is taken from template definition)
           :returns: a dict containing all relevant fields for creating a new
                     mail.mail entry, with one extra key ``attachments``, in the
                     format expected by :py:meth:`mail_thread.message_post`.
        """
        if context is None:
            context = {}
        report_xml_pool = self.pool.get('ir.actions.report.xml')
        template = self.get_email_template(cr, uid, template_id, res_id, context)
        values = {}
        for field in ['subject', 'body_html', 'email_from',
                      'email_to', 'email_recipients', 'email_cc', 'reply_to']:
            values[field] = self.render_template(cr, uid, getattr(template, field),
                                                 template.model, res_id, context=context) \
                                                 or False
        if template.user_signature:
            signature = self.pool.get('res.users').browse(cr, uid, uid, context).signature
            values['body_html'] = tools.append_content_to_html(values['body_html'], signature)

        if values['body_html']:
            values['body'] = tools.html_sanitize(values['body_html'])

        values.update(mail_server_id=template.mail_server_id.id or False,
                      auto_delete=template.auto_delete,
                      model=template.model,
                      res_id=res_id or False)

        attachments = []
        # Add report in attachments
        if template.email_attachment_ids:
            for email_attachment in template.email_attachment_ids: 
                report_name = email_attachment.name or '%s_report' %(template.model)
                if email_attachment.attachment:
                    report_name = eval(email_attachment.attachment)
                report_service = 'report.' + report_xml_pool.browse(cr, uid, email_attachment.id, context).report_name
                # Ensure report is rendered using template's language
                ctx = context.copy()
                if template.lang:
                    ctx['lang'] = self.render_template(cr, uid, template.lang, template.model, res_id, context)
                service = netsvc.LocalService(report_service)
                (result, format) = service.create(cr, uid, [res_id], {'model': template.model}, ctx)
                if result:
                    result = base64.b64encode(result)
                    if not report_name:
                        report_name = report_service
                    ext = "." + format
                    if not report_name.endswith(ext):
                        report_name += ext
                    attachments.append((report_name, result))

        attachment_ids = []
        # Add template attachments
        for attach in template.attachment_ids:
            attachment_ids.append(attach.id)

        values['attachments'] = attachments
        values['attachment_ids'] = attachment_ids
        return values
    
    
