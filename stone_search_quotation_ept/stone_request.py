from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta
import time

from dateutil.tz import *
import pytz
from pytz import timezone
from collections import OrderedDict
import netsvc
from operator import itemgetter
import logging
from openerp.osv import orm

_logger = logging.getLogger(__name__)

class stone_request(osv.osv_memory):
    _name = 'stone.request'

    """ This method set default source location in form view"""    
#     def default_get(self, cr, uid, fields_list, context=None):
#         # merge defaults from stock.picking with possible defaults defined on stock.picking.in
#         defaults = self.pool['stock.picking'].default_get(cr, uid, fields_list, context=context)
#         if context.get('active_ids'):
#             product_data = self.pool.get('product.product').read(cr, uid, context.get('active_ids')[0], context=context)
#             location = product_data.get('location_id')[0]
#             defaults.update({
#                          'src_location':location,
#                          })
#         return defaults
        
    _columns = {
                'partner_id' : fields.many2one('res.partner', 'Customer'),
                'src_location':fields.many2one('stock.location', string='Source Location'),
                'dest_location':fields.many2one('stock.location', string='Destination Location'),
                }
    
    def confirm_stone_request(self, cr, uid, ids, context={}):
        #product_ids = [x.id for x in request_obj.stone_m2m_ids or []]
        self_obj = self.browse(cr, uid, ids[0])
        stock_line=self.pool.get('stock.picking').create(cr, uid, {
                                                                   'partner_id': self_obj.partner_id and self_obj.partner_id.id or False,
                                                                   'date' : datetime.now(),
                                                                   'requested' : True,
                                                                   'requester_uid' : uid,
                                                                   'dest_loc_id': self_obj.dest_location and self_obj.dest_location.id or False,
                                                                   'is_returned':False, 
                                                                   }, context=context)
        
        create_val = {}
        for id in context.get('active_ids'):
            create_val = self.pool.get('stock.move').onchange_product_id(cr, uid, [], id, 
                                                                self_obj.src_location and self_obj.src_location.id or False, \
                                                                self_obj.dest_location and self_obj.dest_location.id or False, False)
            create_val.get('value').update({
                               'picking_id' : stock_line,
                               'product_id' : id,
                                           })
            self.pool.get('stock.move').create(cr, uid, create_val.get('value'), context={})
        self.pool.get('stock.picking').draft_force_assign(cr, uid, [stock_line])
        #self.pool.get('stock.picking').action_assign(cr, uid, [stock_line])
        self.pool.get('stock.picking').force_assign(cr, uid, [stock_line])
        return stock_line
    
    def confirm_stone_request_view(self, cr, uid, ids, context={}):
        stock_line = self.confirm_stone_request(cr, uid, ids, context)
        model_obj = self.pool.get('ir.model.data')
        data_id = model_obj._get_id(cr, uid, 'stone_search_quotation_ept', 'stock_internal_move_form_ept')
        view_id = model_obj.browse(cr, uid, data_id, context=context).res_id
        context.update({'active_ids': stock_line})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Internal Moves'),
            'res_model': 'stock.picking',
            'res_id': stock_line,
            'view_type' : 'form',
            'view_mode' : 'form',
            'view_id' : view_id,
            'target' : 'current',
            'nodestroy' : True,
              }

class stock_move(osv.osv):
    _inherit = 'stock.move'
        
    _columns = {
                'product_rfid' : fields.char("RFID tag", size=126),
                }
    
    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):
        """
            It will add RFID tag into product in stock_move form view.
        """
        result = super(stock_move, self).onchange_product_id(cr, uid, ids, prod_id, loc_id,loc_dest_id, partner_id)
        if prod_id:
            product = self.pool.get('product.product').read(cr, uid, [prod_id],['rfid_tag'] ,context={})[0]
            pro_rfid = product.get('rfid_tag','')
            result.get('value').update({
                                        'product_rfid' : pro_rfid,
                                        })
            return result
        return result

       
class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    def calculate_qty(self, cr, uid, ids, Name=None, args=None, context=None):
        '''
        Count total stone in picking.
        '''
        res = {}  
        for id in ids:
            cr.execute('select count(id) from stock_move where picking_id  = %s',(id,))
            val = cr.dictfetchone()
            res[id] = val['count'] or 0
        return res
    
    _columns = {
                'requested' : fields.boolean("Requested"),
                'requester_uid' : fields.many2one("res.users","Requested By"),
                'issued_uid' : fields.many2one("res.users","Issued By"),
                'returned_uid' : fields.many2one("res.users","Returned By"),
                'dest_loc_id': fields.many2one("stock.location","Destination Location"),
                'total_pro' : fields.function(calculate_qty, type='integer', string='Total Product'),
                'is_returned' : fields.boolean("Returned"),
                'is_fully_returned' : fields.boolean("Fully Returned"),
                } 
    

    def issued_return_info(self, cr, uid, ids):#get_picking_info_for_issuied
        '''
            This method return information of specific picking and its moves given by .Net application
            (applying search method in .net)
        '''
        res = []
        user = self.pool.get('res.users').browse(cr, uid, uid)
        if ids:
            vals = self.read(cr,uid, ids, ['name','partner_id','dest_loc_id','date','requester_uid','issued_uid','returned_uid','total_pro','state','is_returned','is_fully_returned'])  
            for v in vals :
                loc= self.pool.get('stock.location').read(cr, uid, v.get('dest_loc_id')[0],['name'])
                #dt = time.strptime(v.get('date'),'%Y-%m-%d %H:%M:%S.%f')
                utc = pytz.timezone('UTC')
                current_tz = pytz.timezone(user.tz)
                dt = datetime.strptime(v.get('date'),'%Y-%m-%d %H:%M:%S.%f')
                utc_today = utc.localize(dt, is_dst=False)
                context_today = utc_today.astimezone(current_tz)
                curr_date_time = context_today.strftime("%Y-%m-%d %H:%M:%S")
                requester = v.get('requester_uid', False) and v.get('requester_uid')[1] or '-'
                issuer = v.get('issued_uid',False) and v.get('issued_uid')[1] or '-'
                returner = v.get('returned_uid',False) and v.get('returned_uid')[1] or '-'
                
                res.append(
                   {
                     'ID' : v.get('id'),  
                     'Name' : v.get('name'),
                     'Customer' : v.get('partner_id')[1],
                     'Location' : loc.get('name'),
                     'Date' : curr_date_time,#time.strftime('%d-%m-%Y %H:%M:%S',dt),
                     'Requester' : requester,
                     'Issuer' : issuer,
                     'Returner' : returner,
                     'Total Product' : v.get('total_pro'),
                     'State' : v.get('state'),
                     'Returned': v.get('is_returned'),
                     'Fully Returned' : v.get('is_fully_returned'),
                     }
                           )
        return res
    
    def move_info(self, cr, uid, picking_id):
        '''
            This method called when double click on any picking in .net.
            It return moves information of given picking.
        '''
        res = []
        _query="""
            select sm.id as "StockMoveId",pro.id as "StoneId",pro.name_template as "StoneName",coalesce(pro_shape.name,'') as "Shape",
            coalesce(pro.rfid_tag,'') as "RFIDtag",
            coalesce(pro_color.name,'') as "Color",coalesce(pro_cut.name,'') as "Cut",
            coalesce(pro_polish.name,'') as "Polish",coalesce(pro_symmetry.name,'') as "Symmetry",coalesce(pro_lab.name,'') as "Lab",
            coalesce(pro_gridle_thin.name,'') as "GridleThin",coalesce(pro_gridle_thick.name,'') as "GridleThick",
            coalesce(pro_gridle.name,'') as "Gridle",coalesce(pro_culet_con.name,'') as "CuletCondition",
            coalesce(pfc.name,'') as "FluorescenceColor",
            coalesce(pro_fancy_clr.name,'') as "FancyColor",coalesce(pfi.name,'') as "FluorescenceIntensityName",
            coalesce(pro.product_length,0) as "Length",coalesce(pro.product_width,0) as "Width",coalesce(pro.product_height,0) as "Height"
            ,coalesce(pro.product_depth,0) as "Depth",
            coalesce(pro_status.name,'') as "Status",
            coalesce(pro.weight,0) as "Weight",coalesce(pro.gridle_condition,'') as "GridleCondition",coalesce(pro.diameter,'') as "Diameter",
            coalesce(pro_clarity.name,'') as "Clarity" 
            from stock_picking sp join stock_move sm on sm.picking_id = sp.id and sp.id = %(picking_id)s
            join product_product pro on pro.id = sm.product_id
            left join product_shape pro_shape on pro.shape_id = pro_shape.id
            left join product_color pro_color on pro.color_id = pro_color.id
            left join product_cut pro_cut on pro.cut_id = pro_cut.id
            left join product_polish pro_polish on pro.polish_id = pro_polish.id
            left join product_symmetry pro_symmetry on pro.symmetry_id = pro_symmetry.id
            left join product_lab pro_lab on pro.lab_id = pro_lab.id
            left join product_gridle_thin pro_gridle_thin on pro.gridle_thin_id = pro_gridle_thin.id
            left join product_gridle_thick pro_gridle_thick on pro.gridle_thick_id = pro_gridle_thick.id
            left join product_gridle pro_gridle on pro.gridle_id = pro_gridle.id
            left join product_culet_condition pro_culet_con on pro.culet_condition = pro_culet_con.id
            left join product_fluorescence_color pfc on pro.fluorescence_color_id = pfc.id
            left join product_fancy_color pro_fancy_clr on pro.fancy_color_id = pro_fancy_clr.id
            left join product_fluorescence_intensity pfi on pro.fluorescence_intensity_id = pfi.id
            left join product_status pro_status on pro.status_id = pro_status.id 
            left join product_clarity pro_clarity on pro.clarity_id = pro_clarity.id
            """%({'picking_id':picking_id})
        cr.execute(_query)     
        res=cr.dictfetchall()
        return res
    
    def do_partial_ept(self, cr, uid, picking_id, move_ids, rfid_tag):
        '''
            This method called when move selected for issue.
            It return new picking with selected move in issued panel 
        '''
        move_data = self.pool.get("stock.move").read(cr ,uid, move_ids)
        partial_datas = {}
        for data in move_data:
            mid = ('move%s'%(data.get('id')))
            product_id = data.get('product_id', False)[0]
            product_uom = data.get('product_uom', False)[0]
            product_qty = data.get('product_qty', False)
            delivery_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')
            partial_datas.update({
                                  mid : {
                                         'prodlot_id': False, 
                                         'product_id': product_id, 
                                         'product_uom': product_uom, 
                                         'product_qty':product_qty,
                                         },
                                  })
        partial_datas.update({'delivery_date':delivery_date})
        context={}
        picking_info = super(stock_picking, self).do_partial(cr, uid, [picking_id], partial_datas, context)
        data=self.pool.get('res.users').read(cr, uid, uid, ['name'])
        issued_by=data.get('id')
        pick_id = self.browse(cr, uid, picking_info.keys(), context)
        id = pick_id[0].backorder_id and pick_id[0].backorder_id.id 
        if id:
            if not pick_id[0].issued_uid:
                self.write(cr, uid, [id],{'issued_uid':issued_by}, context)
        else:
            if not pick_id[0].is_returned:
                self.write(cr, uid, pick_id[0].id,{'issued_uid':issued_by}, context)
                
        """            
        This will change the status of product, 
        if picking done then it will clear the rfid tag.
        """
        
        for move in self.pool.get('stock.move').browse(cr, uid, move_ids, context):
            if move.location_id.usage=='internal' and move.location_dest_id.usage=='customer':
                self.pool.get('product.product').write(cr, uid, move.product_id.id, {'product_status':'sold','rfid_tag':''}, context)
            
            if move.location_id.usage=='customer' or move.location_dest_id.usage=='supplier' and move.location_dest_id.usage=='internal':
                self.pool.get('product.product').write(cr, uid, move.product_id.id, {'product_status':'available'}, context)
        return picking_info.keys()  or picking_info
    
    def action_process(self, cr, uid, ids, context={}):
        """
        Requested picking not allow to process manually .
        """
        data = self.read(cr, uid, ids[0],['requested'], context)
        if data.get('requested'):
            raise osv.except_osv(_('Warning!'), _("You are not allowed to process this picking!"))
        return super(stock_picking, self).action_process(cr, uid, ids, context)

    def write(self, cr, uid, ids, vals, context={}):
        name = ''
        sequence_obj = self.pool.get('ir.sequence')
        if vals.has_key('name') and vals['name'] != '/' :
            pick = self.browse(cr,uid,ids[0],context=context)
            if pick:
                if pick.type == 'internal' :
                    name = sequence_obj.get(cr, uid,'stock.picking')
                    vals['name'] = name    
        return super(stock_picking, self).write(cr, uid,ids,vals,context=context)
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default.get('name').find('return')!=-1:
            default.update({'is_returned':True})
        return super(stock_picking, self).copy(cr, uid, id, default, context)
        
    def return_stone_info(self, cr, uid, ids):
        '''
        This method called when move selected in issued panel.
        It return new picking with selected move in return panel. 
        '''
        pid={}
        return_picking_ids=[]
        stock_return_obj = self.pool.get('stock.return.picking')
        context={}
        cr.execute('select distinct picking_id from stock_move where id in %s', (tuple(ids),))
        for pid in cr.dictfetchall():
            for id in pid.values():
            
                move_ids = self.pool.get('stock.move').search(cr, uid, [('id','in',ids),('picking_id','=',id)])
                return_moves = []
######move is already returned or not
                if context is None:
                    context = {}
                valid_lines = 0
                return_history = {}
                move_line = self.pool.get('stock.move').browse(cr, uid, move_ids, context)
                for m  in move_line:
                    if m.state == 'done':
                        return_history[m.id] = 0
                        if m.move_history_ids2:
                            raise osv.except_osv(_('Warning!'), _("No products to return (only lines in Done state and not fully returned yet can be returned)!"))
##################
                for stock_move in self.pool.get('stock.move').browse(cr ,uid, move_ids, context):
                    return_moves.append((0,0,{'product_id':stock_move.product_id.id, 
                                              'quantity': stock_move.product_qty,
                                              'move_id':stock_move.id, 
                                              'prodlot_id': stock_move.prodlot_id and stock_move.prodlot_id.id or False}))
                if return_moves:
                    stock_return_id = stock_return_obj.create(cr, uid, {
                                                           'product_return_moves': return_moves,
                                                            'invoice_state':'none',
                                                                    })
                    move_obj = self.pool.get('stock.move')
                    uom_obj = self.pool.get('product.uom')
                    data_obj = self.pool.get('stock.return.picking.memory')
                    wf_service = netsvc.LocalService("workflow")
                    pick = self.browse(cr, uid, id, context=context)
                    data = self.pool.get('stock.return.picking').read(cr, uid, stock_return_id, context=context)
                    date_cur = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    set_invoice_state_to_none = True
                    returned_lines = 0
##########Create new picking for returned products
                    seq_obj_name = 'stock.picking'
                    new_type = 'internal'
                    if pick.type =='out':
                        new_type = 'in'
                        seq_obj_name = 'stock.picking.in'
                    elif pick.type =='in':
                        new_type = 'out'
                        seq_obj_name = 'stock.picking.out'
                    new_pick_name = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)
                    new_picking = self.copy(cr, uid, pick.id, {
                                                    'name': _('%s-%s-return') % (new_pick_name, pick.name),
                                                    'move_lines': [], 
                                                    'state':'draft', 
                                                    'type': new_type,
                                                    'date':date_cur, 
                                                    'invoice_state': data['invoice_state'],
                    })
                    val_id = data['product_return_moves']
                    for v in val_id:
                        data_get = data_obj.browse(cr, uid, v, context=context)
                        mov_id = data_get.move_id.id
                        if not mov_id:
                            raise osv.except_osv(_('Warning !'), _("You have manually created product lines, please delete them to proceed"))
                        new_qty = data_get.quantity
                        move = move_obj.browse(cr, uid, mov_id, context=context)
                        new_location = move.location_dest_id.id
                        returned_qty = move.product_qty
                        for rec in move.move_history_ids2:
                            returned_qty -= rec.product_qty
                        if returned_qty != new_qty:
                            set_invoice_state_to_none = False
                        if new_qty:
                            returned_lines += 1
                            move_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            new_move=move_obj.copy(cr, uid, move.id, {
                                                        'product_qty': new_qty,
                                                        'product_uos_qty': uom_obj._compute_qty(cr, uid, move.product_uom.id, new_qty, move.product_uos.id),
                                                        'picking_id': new_picking, 
                                                        'state': 'draft',
                                                        'location_id': new_location, 
                                                        'location_dest_id': move.location_id.id,
                                                        'date': move_date,
                            })
                            move_obj.write(cr, uid, [move.id], {'move_history_ids2':[(4,new_move)]}, context=context)
                    if not returned_lines:
                        raise osv.except_osv(_('Warning!'), _("Please specify at least one non-zero quantity."))
                    if set_invoice_state_to_none:
                        self.write(cr, uid, [pick.id], {'invoice_state':'none'}, context=context)
                    wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_confirm', cr)
                    self.force_assign(cr, uid, [new_picking], context)
                    return_picking_ids.append(new_picking)
                    move_ids = move_obj.search(cr, uid, [('picking_id','=',new_picking)])
                    partial_data = self.do_partial_ept(cr, uid, new_picking, move_ids, [])
                    
                    data=self.pool.get('res.users').read(cr, uid, uid, ['name'])
                    returned_uid=data.get('id')
                    self.write(cr, uid, [new_picking],{'returned_uid':returned_uid}, context)
####Fully returned                    
                    pick = self.browse(cr, uid, id, context=context)
                    valid_lines = 0
                    return_history = stock_return_obj.get_return_history(cr, uid, id, context)
                    for m  in pick.move_lines:
                        if m.state == 'done' and m.product_qty * m.product_uom.factor > return_history.get(m.id, 0):
                            valid_lines += 1
                    if not valid_lines:
                        self.write(cr, uid, id,{'is_fully_returned' : True}, context)
                    #self.do_partial(cr, uid, new_picking, partial_data, context)
        return return_picking_ids

# class stock_inventory(osv.osv):
#     """
#         Inherit for set default product quantity.
#     """
#     _inherit = 'stock.inventory.line'
#      
#     def on_change_product_id(self, cr, uid, ids, location_id, product, uom=False, to_date=False, default_qty=False):
#         result = super(stock_move_ept, self).onchange_product_id(cr, uid, ids,location_id,product, uom, to_date)
#             
#         obj_product = self.pool.get('product.product').browse(cr, uid, product)
#         uom = uom or obj_product.uom_id.id
#         amount = self.pool.get('stock.location')._product_get(cr, uid, location_id, [product], {'uom': uom, 'to_date': to_date, 'compute_child': False})[product]
#         result = {'product_qty': amount, 'product_uom': uom, 'prod_lot_id': False}
#         return {'value': result}

    

        
#dt = datetime.strptime(v.get('date'), '%Y-%m-%d %H:%M:%S:%f')
#dt1=dt.strftime('%d-%m-%Y')        
