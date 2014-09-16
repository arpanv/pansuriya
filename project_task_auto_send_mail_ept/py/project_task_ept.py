from openerp.osv import osv,fields

class project_task(osv.osv):
    _name="project.task"
    _inherit="project.task"
    
    def create(self,cr,uid,vals,context={}):
        task_id = super(project_task,self).create(cr,uid,vals,context)
        email_template=self.pool.get('email.template')
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'project_task_auto_send_mail_ept', 'email_template_project_task_ept')[1]
        except ValueError:
            template_id = False
        template=email_template.browse(cr,uid,template_id)
        post_values={}
        subtype="mail.mt_comment"
        post_values['subject'] = email_template.render_template(cr, uid, template.subject, 'project.task', task_id,context)
        post_values['body'] = email_template.render_template(cr, uid, template.body_html, 'project.task', task_id, context)
        
        br_prj_task = self.browse(cr ,uid, task_id, context = context)
#         post_values['to'] = br_prj_task.user_id.partner_id and br_prj_task.user_id.partner_id.email or False
        post_values['partner_ids'] = br_prj_task.user_id.partner_id and [br_prj_task.user_id.partner_id.id] or False
         
        self.message_post(cr,uid,task_id,type="comment",subtype=subtype,context=context,**post_values)
        return task_id