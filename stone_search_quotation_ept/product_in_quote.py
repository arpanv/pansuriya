from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _

class product_in_quote(osv.osv_memory):
    _name = 'product.in.quote'
    _columns = {
                'partner_id' : fields.many2one('res.partner', 'Customer'),
                'order_id':fields.many2one('sale.order',string='Quotation')
                }
    
    def on_change_partner_id(self,cr,uid,ids,partner_id):
        result = {}
        result.update({'value':{'order_id':False}})
        return result
    def create_quote_ept(self, cr, uid, ids, context=None):
        self_obj = self.browse(cr, uid, ids[0], context=context)
        vals = {}        
        vals = self.pool.get('sale.order').onchange_partner_id(cr, uid, [], self_obj.partner_id.id, context=context)
        vals.get('value').update({
                     'partner_id' : self_obj.partner_id.id
                     })
        if not self_obj.order_id:
            new_quote_id = self.pool.get('sale.order').create(cr, uid, vals.get('value'), context=context)
        else:
            new_quote_id = self_obj.order_id.id
        so_obj = self.pool.get('sale.order').browse(cr, uid, new_quote_id,context=context)
        for obj in self.pool.get(context.get('active_model')).browse(cr, uid, context.get('active_ids')):
            product_obj = obj
            order_line_value = {}
            context.update({'lot_id':obj.id})
            order_line_value = self.pool.get('sale.order.line').product_id_change(cr, uid, [], so_obj.pricelist_id and so_obj.pricelist_id.id or False, \
                                                                                  product_obj.id, 1, product_obj.uom_id.id, 1, product_obj.uom_id.id, product_obj.name,\
                                                                                  self_obj.partner_id.id, False, True, so_obj.date_order, False, so_obj.fiscal_position,\
                                                                                  False,context=context)
            order_line_value.get('value').update({
                                                  'order_id' : new_quote_id
                                                  })
            new_line_id = self.pool.get(
                'sale.order.line').create(cr, uid, order_line_value.get('value'), context=context)
            
        #Redirect to newly create quotation
        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'product_stone_search_ept', 'view_order_form_ept')
        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id
                
        context.update({'active_ids': new_quote_id})
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Quotation'),
            'res_model': 'sale.order',
            'res_id': new_quote_id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
product_in_quote()