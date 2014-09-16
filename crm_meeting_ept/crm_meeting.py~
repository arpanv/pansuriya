from openerp.osv import fields, osv


class crm_meeting(osv.Model):
    _name = "crm.meeting"
    _inherit = "crm.meeting"

    def create(self, cr, uid, vals, context=None):
        if context :
            for key in context.keys() :
                if key.startswith('default') :
                    context.pop(key)
        else :
            context = {}
        return super(crm_meeting, self).create(cr, uid, vals, context=context)

crm_meeting()
