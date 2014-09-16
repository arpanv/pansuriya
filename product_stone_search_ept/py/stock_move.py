from openerp.osv import osv, fields
from openerp.tools.translate import _

class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    def create(self, cr, uid, vals, context={}):
        """
        Override for adding product_status in product when move is create.[for openerp]
        """
        id = vals.get('product_id')
        dest = vals.get('location_id',False)
        source = vals.get('location_dest_id',False)
        
        loc = self.pool.get('stock.location').browse(cr, uid, [dest,source], context=context)
        
        if loc[0].usage=='supplier' or loc[0].usage=='customer' and loc[1].usage=='internal':
            self.pool.get('product.product').write(cr, uid, [id], {'product_status' : 'available'}, context=context)
            
        #if loc[0].usage=='internal'  and loc[1].usage=='customer':
            #self.pool.get('product.product').write(cr, uid, [id], {'product_status' : 'sold'}, context=context)
        return super(stock_move, self).create(cr, uid, vals, context=context) 
    
    def _check_production_lot(self, cr, uid, ids, context=None):        
        for move in self.browse(cr, uid, ids, context=context):
            location_type = move.location_id.usage                               
            if move.prodlot_id and move.prodlot_id.type == 'Stone' and move.state == 'done':
                for m in move.prodlot_id.move_ids:
                    if m.state == 'done' and m.id!=move.id:
                        old_move_location_type = m.location_id.usage
#                        if old_move_location_type == 'supplier' and m.move_history_ids2:
#                            for hm in m.move_history_ids2:
#                                print hm.location_id.name
#                            return True
                        if location_type == 'supplier' or location_type == 'production' or location_type == 'inventory' or location_type == 'procurement':
                            if old_move_location_type == 'supplier' or old_move_location_type == 'production' or old_move_location_type == 'inventory' or old_move_location_type == 'procurement':                            
                                return False
        return True    
    
    def _check_quntity(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.prodlot_id :
                if obj.prodlot_id.type == 'Stone':
                    if obj.product_qty != 1:
                        return False
        return True
    
            
    
    _constraints = [
        (_check_quntity, 'Quantity must be only 1 for stone',['prodlot_id']),
        (_check_production_lot,
            'Please choose proper Stone, it has already been used.',
            ['prodlot_id']),]
    
stock_move()
   