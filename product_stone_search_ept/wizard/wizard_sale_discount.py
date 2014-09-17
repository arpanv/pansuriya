from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
class wizard_sale_discount_ept(osv.osv_memory):
    _name = 'wizard.sale.discount.ept'
    _description = 'Set Discount'
    
    _columns = {
                    'operation':fields.selection([('increase','Increase'), ('decrease','Decrease'),('set','Set'),('set_default_discount','Set Default Discount')],string='Discount'),
                    'value':fields.float(string='Value',digits_compute=dp.get_precision('Account'))
                }
    def set_discount(self,cr,uid,ids,context=None):
        active_ids = context.get('active_ids',False)
        product_obj = self.pool.get('product.product')
        sale_order_line = self.pool.get('sale.order.line')
        if active_ids and ids:
            data = self.browse(cr,uid,ids[0],context=context)
            if (data.operation and data.value) or data.operation=='set_default_discount':
                for sale in self.pool.get('sale.order').browse(cr,uid,active_ids,context=context):
                    for line in sale.order_line:
                        discount = line.discount
                        if data.operation=="set_default_discount":
                            product_data=product_obj.read(cr, uid, [line.product_id.id], ['discount'], context)
                            sale_order_line.write(cr,uid,[line.id],{'discount':product_data[0].get('discount',0.0)},context=context)
                            continue
                        if data.operation=='set':
                            sale_order_line.write(cr,uid,[line.id],{'discount':data.value or 0.00},context=context)
                        elif line.discount:
                            if data.operation == 'increase':
                                discount = line.discount + data.value
                            elif data.operation == 'decrease':
                                discount = line.discount - data.value
                            sale_order_line.write(cr,uid,[line.id],{'discount':discount},context=context)
        return True
wizard_sale_discount_ept()