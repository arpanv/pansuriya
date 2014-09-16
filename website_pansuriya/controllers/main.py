import base64
from datetime import datetime, timedelta,date
import werkzeug
import werkzeug.urls
import pusher
from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website_sale.models.sale_order import website as sale_website 


class website_test(http.Controller):
    @http.route(['/website-pansuriya'], type='http', auth="public", website=True)
    def website_test_data(self, **kwargs):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        product_shape = pool.get('product.shape')
        product_shape_ids = product_shape.search(cr,uid,[],order="name")
        product_shape_objects = product_shape.browse(cr,uid,product_shape_ids)
        
        product_color = pool.get('product.color')
        product_color_ids = product_color.search(cr,uid,[],order="seq")
        product_color_objects = product_color.browse(cr,uid,product_color_ids)
        
        product_clarity = pool.get('product.clarity')
        product_clarity_ids = product_clarity.search(cr,uid,[],order="seq")
        product_clarity_objects = product_clarity.browse(cr,uid,product_clarity_ids)
        
        product_cut = pool.get('product.cut')
        product_cut_ids = product_cut.search(cr,uid,[],order="seq")
        product_cut_objects = product_cut.browse(cr,uid,product_cut_ids)
        
        product_polish = pool.get('product.polish')
        product_polish_ids = product_polish.search(cr,uid,[],order="seq")
        product_polish_objects = product_polish.browse(cr,uid,product_polish_ids)
        
        product_symmetry = pool.get('product.symmetry')
        product_symmetry_ids = product_symmetry.search(cr,uid,[],order="seq")
        product_symmetry_objects = product_symmetry.browse(cr,uid,product_symmetry_ids)
        
        product_fluorescence_intensity = pool.get('product.fluorescence.intensity')
        product_fluorescence_intensity_ids = product_fluorescence_intensity.search(cr,uid,[],order="seq")
        product_fluorescence_intensity_objects = product_fluorescence_intensity.browse(cr,uid,product_fluorescence_intensity_ids)
        
        product_lab = pool.get('product.lab')
        product_lab_ids = product_lab.search(cr,uid,[],order="name")
        product_lab_objects = product_lab.browse(cr,uid,product_lab_ids)
        
        product_culet_size = pool.get('product.culet')
        product_culet_size_ids = product_culet_size.search(cr,uid,[],order="name")
        product_culet_size_objects = product_culet_size.browse(cr,uid,product_culet_size_ids)
        
        product_culet_condition = pool.get('product.culet_condition')
        product_culet_condition_ids = product_culet_condition.search(cr,uid,[],order="name")
        product_culet_condition_objects = product_culet_condition.browse(cr,uid,product_culet_condition_ids)
        
        product_girdle = pool.get('product.gridle')
        product_girdle_ids = product_girdle.search(cr,uid,[],order="seq")
        product_girdle_objects = product_girdle.browse(cr,uid,product_girdle_ids)
        
        values = {
                  'product_shapes':product_shape_objects,
                  'product_colors':product_color_objects,
                  'product_clarities':product_clarity_objects,
                  'product_cuts':product_cut_objects,
                  'product_polishes':product_polish_objects,
                  'product_symmetries':product_symmetry_objects,
                  'product_fluorescence_intensities':product_fluorescence_intensity_objects,
                  'product_labs':product_lab_objects,
                  'product_culet_sizes':product_culet_size_objects,
                  'product_culet_conditions':product_culet_condition_objects,
                  'product_girdles':product_girdle_objects,
                  
                  }
        return request.website.render("website_pansuriya.website_test_search_stone", values)
    
    @http.route(['/website-pansuriya/submit_json'], type='json', auth="public", methods=['POST'], website=True)
    def website_test_thanks(self, **kwargs):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        product_stone = pool.get('product.product')
        color_pool = pool.get('product.color')
        clarity_pool = pool.get('product.clarity')
        polish_pool = pool.get('product.polish')
        symmetry_pool = pool.get('product.symmetry')
        fluorescence_intensity_pool = pool.get('product.fluorescence.intensity')
        
        domain =[]
        filter_params = kwargs['data']
        
        domain.append(('is_certified','=',True))
        
        if filter_params.get('shape',False):
            domain.append(('shape_id','=',int(filter_params.get('shape'))))
        
        if filter_params.get('carat',False) and not filter_params.get('carat_to'):
           domain.append(('weight','>=',float(filter_params.get('carat'))))
        elif filter_params.get('carat',False) and filter_params.get('carat_to',False):
           domain.append(('weight','>=',float(filter_params.get('carat'))))
           domain.append(('weight','<=',float(filter_params.get('carat_to'))))
        
        
        color_from = int(filter_params.get('color','0') or '0')
        color_to = int(filter_params.get('color_to','0') or '0')
        if color_from and color_to and color_from > color_to:
            color_temp = color_from
            color_from = color_to
            color_to = color_temp
        if not color_from and color_to:
            domain.append(('color_id.seq','<=',color_to))
        if not color_to and color_from:
            domain.append(('color_id.seq','>=',color_from))
        if color_from and color_to:
            domain.append(('color_id.seq','>=',color_from))
            domain.append(('color_id.seq','<=',color_to))

            
        clarity_from = int(filter_params.get('clarity','0') or '0')
        clarity_to = int(filter_params.get('clarity_to','0') or '0')
        if clarity_from and clarity_to and clarity_from > clarity_to:
            clarity_temp = clarity_from
            clarity_from = clarity_to
            clarity_to = clarity_temp
        if not clarity_from and clarity_to:
            domain.append(('clarity_id.seq','<=',clarity_to))
        if not clarity_to and clarity_from:
            domain.append(('clarity_id.seq','>=',clarity_from))
        if clarity_from and clarity_to:
            domain.append(('clarity_id.seq','>=',clarity_from))
            domain.append(('clarity_id.seq','<=',clarity_to))
            
            
        cut_from = int(filter_params.get('cut','0') or '0')
        cut_to = int(filter_params.get('cut_to','0') or '0')
        if cut_from and cut_to and cut_from > cut_to:
            cut_temp = cut_from
            cut_from = cut_to
            cut_to = cut_temp
        if not cut_from and cut_to:
            domain.append(('cut_id.seq','<=',cut_to))
        if not cut_to and cut_from:
            domain.append(('cut_id.seq','>=',cut_from))
        if cut_from and cut_to:
            domain.append(('cut_id.seq','>=',cut_from))
            domain.append(('cut_id.seq','<=',cut_to))
        
        
        polish_from = int(filter_params.get('polish','0') or '0')
        polish_to = int(filter_params.get('polish_to','0') or '0')
        if polish_from and polish_to and polish_from > polish_to:
            polish_temp = polish_from
            polish_from = polish_to
            polish_to = polish_temp
        if not polish_from and polish_to:
            domain.append(('polish_id.seq','<=',polish_to))
        if not polish_to and polish_from:
            domain.append(('polish_id.seq','>=',polish_from))
        if polish_from and polish_to:
            domain.append(('polish_id.seq','>=',polish_from))
            domain.append(('polish_id.seq','<=',polish_to))
            
        
        sym_from = int(filter_params.get('symmetry','0') or '0')
        sym_to = int(filter_params.get('symmetry_to','0') or '0')
        if sym_from and sym_to and sym_from > sym_to:
            sym_temp = sym_from
            sym_from = sym_to
            sym_to = sym_temp
        if not sym_from and sym_to:
            domain.append(('symmetry_id.seq','<=',sym_to))
        if not sym_to and sym_from:
            domain.append(('symmetry_id.seq','>=',sym_from))
        if sym_from and sym_to:
            domain.append(('symmetry_id.seq','>=',sym_from))
            domain.append(('symmetry_id.seq','<=',sym_to))
        
        
        fluorescence_from = int(filter_params.get('fluorescence','0') or '0')
        fluorescence_to = int(filter_params.get('fluorescence_to','0') or '0')
        if fluorescence_from and fluorescence_to and fluorescence_from > fluorescence_to:
            fluorescence_temp = fluorescence_from
            fluorescence_from = fluorescence_to
            fluorescence_to = fluorescence_temp
        if not fluorescence_from and fluorescence_to:
            domain.append(('fluorescence_intensity_id.seq','<=',fluorescence_to))
        if not fluorescence_to and fluorescence_from:
            domain.append(('fluorescence_intensity_id.seq','>=',fluorescence_from))
        if fluorescence_from and fluorescence_to:
            domain.append(('fluorescence_intensity_id.seq','>=',fluorescence_from))
            domain.append(('fluorescence_intensity_id.seq','<=',fluorescence_to))
        
        
        if filter_params.get('lab',False):
            domain.append(('lab_id','=',int(filter_params.get('lab'))))
        
        
        if filter_params.get('table',False) and not filter_params.get('table_to'):
           domain.append(('product_table','>=',float(filter_params.get('table'))))
        elif filter_params.get('table',False) and filter_params.get('table_to',False):
           domain.append(('product_table','>=',float(filter_params.get('table'))))
           domain.append(('product_table','<=',float(filter_params.get('table_to'))))
            
        
        if filter_params.get('selLocation',False):
            location_ids = [ int(x) for x in filter_params.get('selLocation',[]) ]
            domain.append(('location_id','in',location_ids))
            
        
        if filter_params.get('m1',False) and not filter_params.get('m1_to'):
           domain.append(('product_length','>=',float(filter_params.get('m1'))))
        elif filter_params.get('m1',False) and filter_params.get('m1_to',False):
           domain.append(('product_length','>=',float(filter_params.get('m1'))))
           domain.append(('product_length','<=',float(filter_params.get('m1_to'))))
        
           
        if filter_params.get('m2',False) and not filter_params.get('m2_to'):
           domain.append(('product_width','>=',float(filter_params.get('m2'))))
        elif filter_params.get('m1',False) and filter_params.get('m2_to',False):
           domain.append(('product_width','>=',float(filter_params.get('m2'))))
           domain.append(('product_width','<=',float(filter_params.get('m2_to')))) 
           
        
        if filter_params.get('m3',False) and not filter_params.get('m3_to'):
           domain.append(('product_height','>=',float(filter_params.get('m3'))))
        elif filter_params.get('m3',False) and filter_params.get('m3_to',False):
           domain.append(('product_height','>=',float(filter_params.get('m3'))))
           domain.append(('product_height','<=',float(filter_params.get('m3_to'))))
        
        
        girdle_from = int(filter_params.get('girdle_from','0') or '0')
        girdle_to = int(filter_params.get('girdle_to','0') or '0')
        if girdle_from and girdle_to and girdle_from > girdle_to:
            girdle_temp = girdle_from
            girdle_from = girdle_to
            girdle_to = girdle_temp
        if not girdle_from and girdle_to:
            domain.append(('girdle_id.seq','<=',girdle_to))
        if not girdle_to and girdle_from:
            domain.append(('girdle_id.seq','>=',girdle_from))
        if girdle_from and girdle_to:
            domain.append(('girdle_id.seq','>=',girdle_from))
            domain.append(('girdle_id.seq','<=',girdle_to))


        if filter_params.get('culet_size',False):
            culet_ids = [ int(x) for x in filter_params.get('culet_size',[]) ]
            domain.append(('culet_id','in',culet_ids))        
            
        if filter_params.get('culet_condition',False):
            culet_condition_ids = [ int(x) for x in filter_params.get('culet_condition',[]) ]
            domain.append(('culet_condition','in',culet_condition_ids))

        if filter_params.get('carat_price',False) and not filter_params.get('carat_price_to'):
           domain.append(('price_caret','>=',float(filter_params.get('carat_price'))))
        elif filter_params.get('carat_price',False) and filter_params.get('carat_price_to',False):
           domain.append(('price_caret','>=',float(filter_params.get('carat_price'))))
           domain.append(('price_caret','<=',float(filter_params.get('carat_price_to'))))
        
        
        if filter_params.get('price',False) and not filter_params.get('price_to'):
           domain.append(('list_price','>=',float(filter_params.get('price'))))
        elif filter_params.get('price',False) and filter_params.get('price_to',False):
           domain.append(('list_price','>=',float(filter_params.get('price'))))
           domain.append(('list_price','<=',float(filter_params.get('price_to'))))
           
        
        if filter_params.get('back',False) and not filter_params.get('back_to'):
           domain.append(('discount','>=',float(filter_params.get('back'))))
        elif filter_params.get('back',False) and filter_params.get('back_to',False):
           domain.append(('discount','>=',float(filter_params.get('back'))))
           domain.append(('discount','<=',float(filter_params.get('back_to'))))
        
        
        if filter_params.get('report_no',False):
            domain.append(('certificate_no','=',filter_params.get('report_no')))
            
        
        if filter_params.get('reference_no',False):
            domain.append(('default_code','=',filter_params.get('reference_no')))                           
        
       
        if(filter_params.get('isfirstreq',0)==1):
            offset = 0
            stone_ids = product_stone.search(cr,uid,domain,offset=offset,limit=30)
        else:
            stone_ids = product_stone.search(cr,uid,domain)
            
        stone_objects =  product_stone.browse(cr,uid,stone_ids)
        stone_count = len(stone_objects)
        
        #########################
        #limit 30 stones to load more stones on scroll
        #########################
        
        values = []
        for stone in stone_objects:            
            val = {
                'id' : stone.id or '-',            
                'count_collection' : stone_count,
                'entity_id' : stone.id or '-',
                'sku' : stone.default_code or '-',
                'shape' : stone.shape_id.name or '-',
                'carat' : round(stone.weight,2) or '-',
                'color' :  stone.color_id.name or '-',
                'clarity' :  stone.clarity_id.name or '-',
                'cut' :  stone.cut_id.name or '-',
                'polish' :  stone.polish_id.name or '-',
                'symmetry' : stone.symmetry_id.name or '-',
                'florescence' : stone.fluorescence_intensity_id.name or '-',
                'table' : stone.table_inc or '-',
                'm1' :stone.product_length,
                'm2' : stone.product_width,
                'm3' : stone.product_height,
                'imgStatus' : 0,
                'lab' :  stone.lab_id.name or '-',
                'back_percentage' : stone.current_bid_amount,
                'is_auction' : stone.is_auction,
                'customer_bid_amount' : '',
                'certificate_link' : '',
                'rapnet_price' : stone.rapnet_price,
                'carat_price' : stone.price_caret,
                'price' : stone.price_unit,
                'booked' : 0,
                'product_bid_count': len(stone.stone_bid_ids),
            }
            if stone.is_auction and stone.auction_date and stone.auction_time:
                # add current_bid code here
                #auction_start_date_object = datetime.strftime(datetime.strptime(stone.auction_date,'%Y-%m-%d %H:%M:%S'),'%b %d, %Y 09:00:00')
                auction_end_time = datetime.strptime(stone.auction_date,'%Y-%m-%d %H:%M:%S') + timedelta(hours=int(stone.auction_time))
                current_date = datetime.strftime(datetime.now(),'%b %d, %Y %H:%M:%S')
                if stone.auction_extension_time:
                    auction_end_time=stone.auction_extension_time
                
                if datetime.now() > (datetime.strptime(stone.auction_date,'%Y-%m-%d %H:%M:%S')+ timedelta(hours=int(4))) and \
                datetime.now() < datetime.strptime(stone.auction_date,'%Y-%m-%d %H:%M:%S') + timedelta(hours=int(stone.auction_time)) :
                    if stone.is_auction:
                        is_auction = 1
                    else:
                        is_auction = 0
                else:
                    is_auction = 0
                if stone.auction_extension_time and datetime.now() > datetime.strptime(stone.auction_extension_time,'%Y-%m-%d %H:%M:%S'):
                    is_auction = 0
                    
                val.update({
                            'auction_start_time':datetime.strftime(datetime.strptime(stone.auction_date,'%Y-%m-%d %H:%M:%S'),'%b %d, %Y 09:00:00'),
                            'auction_end_time': datetime.strftime(auction_end_time,'%b %d, %Y 09:00:00'),
                            'current_time':current_date,
                            'is_auction':is_auction,
                            })
            else:
                val.update({'is_auction':0})
            
            values.append(val)
        return values
    
    @http.route(['/website-pansuriya/ajaxpopup'], type='http', auth="public", website=True)
    def ajax_popup(self,  **kwargs):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry        
        entity_id = int(kwargs.get('id','0') or '0')        
        product_stone = pool.get('product.product')
        stones = product_stone.browse(cr,uid,[entity_id],context=context)
        return request.website.render("website_pansuriya.ajax_popup", {'stone_objects':stones})
#        val = {
#                'entity_id': entity_id,
#                'sku':product.default_code,
#                'shape': product.shape_id.name,
#                'carat': product.weight,
#                'color':  product.color_id.name,
#                'clarity':  '',
#                'cut': '' ,
#                'polish':  '',
#                'symmetry':  '',
#                'florescence': '' ,
#                'table': '',
#                'm1': 0.00,
#                'm2': 0.00,
#                'm3': 0.00,
#                'depth': 0.00,
#                'girdle': '' ,
#                'hna': '',
#                'fluorescence_color': '',
#                'lower_half': '',
#                'measurements':'' ,
#                'report_no': '',
#                'star_length':'' ,
#                'natts': 'No',
#                'browness': 'No',
#                'short_description': 'test4',
#                'price': 50000,
#                'back_percentage': -50,
#                'current_bid': 0,
#                'rapnet_price': 0,
#                'carat_price': 0,
#                'manufacturer': '' ,
#                'customer_bid_amount': -1,
#                'is_auction': 0,
#                'lab': '' ,
#                'crown_height': 0,
#                'crown_angle': 0,
#                'culet_condition': 0,
#                'culet_size':  0,
#                'fancy_color': '',
#                'fancy_color_intensity': '',
#                'fancy_color_overtone':'' ,
#                'milky': '',
#                'girdle_condition': '',
#                'girdle_percentage': 1,
#                'girdle_thick': '',
#                'girdle_thin': '',
#                'pavilion_angle': 0,
#                'pavilion_depth': 0,
#                'pavilion_height': 0,
#                'shade': '',
#                'diameter':0 ,
#                'treatment': '',
#                'tinge': '',
#                'certificate_link': '',
#                'report_link': '',
#                'laser_inscription': 'No',
#                'eye_clean': '',
#                'imgProd': 0,
#                'country_of_manufacture': '',
#                'imgProdOrig': '',
#                'bid_end_date': '',
#                'manufacturer_email': '',
#               }
    
    @http.route(['/savebid'], type='json', auth="public", methods=['POST'], website=True)
    def savebid(self,  **kwargs):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        product_id = int(kwargs['data'].get('product_id','0') or '0')
        bid_amount = float(kwargs['data'].get('bid_amount','0.0') or '0.0')
        stone_bid = pool.get('stone.bid.ept')
        values = {
                  'partner_id':uid,
                  'product_id':product_id,
                  'bid_amount':bid_amount,
                  }
        new_bid_id = stone_bid.create(cr,uid,values,context=context) 
        
        #load product by id
        product_data = pool.get('product.product').read(cr,uid,product_id,['default_code','stone_bid_ids'])
        
        #set current bid of product
        #set extended time
        #save product
        #get bid count
        
        args = {}
        args.update({'product_id':product_id})
        args.update({'product_sku':product_data.get('default_code','')})
        args.update({'bid_amount':bid_amount})
        args.update({'current_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        args.update({'product_bid_count':len(product_data.get('stone_bid_ids',[]))})
        args.update({'is_extend_time':'false'})
        args.update({'extend_time':''})
        args.update({'message':'Bid Update:- Stone: ' + product_data.get("default_code",'')+' Bid: ' + str(bid_amount)})
        
        
        p = pusher.Pusher(app_id='78177', key='83c063b15546d28a09c6', secret='918d17f38096033549ca')
        p['ocentag_bid_channel'].trigger('bidevent', args)
        
        #return 'bid'
