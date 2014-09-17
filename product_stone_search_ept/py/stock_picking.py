from openerp.osv import fields, osv

# set lot in invoice line when invoice based on picking
class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    
    def _prepare_invoice_line(self, cr, uid, group, picking, move_line, invoice_id, invoice_vals, context=None):
        invoice_vals = super(stock_picking, self)._prepare_invoice_line(cr, uid, group, picking, move_line, invoice_id, invoice_vals, context=context)
        if move_line.sale_line_id:
            invoice_vals['weight'] = move_line.sale_line_id.th_weight or 0.0                    
            invoice_vals['color_id'] = move_line.sale_line_id.color_id and move_line.sale_line_id.color_id.id or False
            invoice_vals['clarity_id'] =move_line.sale_line_id.clarity_id and move_line.sale_line_id.clarity_id.id or False 
            invoice_vals['cut_id'] = move_line.sale_line_id.cut_id and move_line.sale_line_id.cut_id.id or False 
            invoice_vals['polish_id'] =move_line.sale_line_id.polish_id and move_line.sale_line_id.polish_id.id or False
            invoice_vals['symmetry_id'] =move_line.sale_line_id.symmetry_id and move_line.sale_line_id.symmetry_id.id or False 
            invoice_vals['fluorescence_intensity_id'] =move_line.sale_line_id.fluorescence_intensity_id and move_line.sale_line_id.fluorescence_intensity_id.id or False
            invoice_vals['rapnet_price'] =move_line.sale_line_id.rapnet_price or 0.0
            invoice_vals['price_caret'] = move_line.sale_line_id.price_caret or 0.0
            invoice_vals['discount'] = move_line.sale_line_id.discount or 0.0
            invoice_vals['certificate_no'] = move_line.sale_line_id.certificate_no or ''
            invoice_vals['shape_id'] = move_line.sale_line_id.shape_id and move_line.sale_line_id.shape_id.id or 0.0
        return invoice_vals

    
    def do_partial(self, cr, uid, picking_id, partial_datas, context):
        """
        This method will change the status of product, 
        if picking done then it will clear the rfid tag.
                [called from openerp not from .net app] 
        """
        mid=[]
        key=partial_datas.keys()
        for k in key:
            if 'move' in k:
                mid.append(int(k.split('move')[1]))
        for move in self.pool.get('stock.move').browse(cr, uid, mid, context):
            #sale
            if move.location_id.usage=='internal' and move.location_dest_id.usage=='customer':
                self.pool.get('product.product').write(cr, uid, move.product_id.id, {'product_status':'sold','rfid_tag':''}, context)
            #return
            if move.location_id.usage=='customer' or move.location_dest_id.usage=='supplier' and move.location_dest_id.usage=='internal':
                self.pool.get('product.product').write(cr, uid, move.product_id.id, {'product_status':'available'}, context)
                       
        picking_info = super(stock_picking, self).do_partial(cr, uid, picking_id, partial_datas, context)
                
        return picking_info
stock_picking()
