from openerp.osv import osv,fields
import csv
from StringIO import StringIO
import base64
import sys
import time
from datetime import datetime
import os
import logging
_logger = logging.getLogger(__name__)

class import_product(osv.osv_memory):
    _name='import.product.ept'
    _columns = {
               'file_name' : fields.binary('Select File'),
               'messages' : fields.text('Message', readonly=True),
               'is_update' : fields.boolean('Do you want to update already exist stone ?'),
              }
    
    def import_products_n_inventory(self, cr, uid, ids=None,context={}):
#from where to call       
        if context.get('from_reimport_button'):
            message_obj=self.pool.get('import.product.message.ept').browse(cr, uid, ids[0])
            file_obj = StringIO(base64.decodestring(message_obj.reimportable_file))
            if not message_obj.reimportable_file:
                raise osv.except_osv(('Unable to proceed'),('Please select file first!!!'))
            file_obj = StringIO(base64.decodestring(message_obj.reimportable_file))
        else:
            self_obj = self.browse(cr, uid,ids[0])
            if self_obj.file_name == False:
                raise osv.except_osv(('Unable to proceed'),('Please select file first!!!'))    
            file_obj = StringIO(base64.decodestring(self_obj.file_name))
#objects
        product_supplier_obj = self.pool.get('product.supplierinfo')
        res_partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        data_obj = self.pool.get('ir.model.data')
        shape_obj=self.pool.get('product.shape')
        fancy_color_obj=self.pool.get('product.fancy.color')
        color_obj=self.pool.get('product.color')
        cut_obj=self.pool.get('product.cut')
        clarity_obj=self.pool.get('product.clarity')
        polish_obj=self.pool.get('product.polish')
        symmentry_obj=self.pool.get('product.symmetry')
        fluorescence_color_obj = self.pool.get('product.fluorescence.color')
        fluorescence_intencity_obj=self.pool.get('product.fluorescence.intensity')  
        lab_obj=self.pool.get('product.lab')
        girdle_obj=self.pool.get('product.gridle')
        culet_size_obj=self.pool.get('product.culet')
        culet_condition_obj=self.pool.get('product.culet_condition')
               
#file import        
        current_date = datetime.strftime(datetime.now(),'%Y%m%d%H%M%S%f')
        imported_product = 0
        updated_product=0
        not_imported_product = 0
        product_data={}
        file_write = open('/tmp/import_stone_%s_%s.csv' %(uid,current_date),'wb')
        file_write.writelines(file_obj.getvalue())
        file_write.close()
        file_read = open('/tmp/import_stone_%s_%s.csv' %(uid,current_date), "rU")
        dialect = csv.Sniffer().sniff(file_read.readline())
        file_read.seek(0)
        reader = csv.DictReader(file_read,dialect=dialect,quoting=csv.QUOTE_NONE)
        fieldname= reader.fieldnames
        
#inventory
        inventory_obj = self.pool.get('stock.inventory')
        stock_location_obj=self.pool.get('stock.location')
        stock_inventory_line_obj=self.pool.get('stock.inventory.line')
                
        inventory_entry=False
                
        opening_stock = 'Opening Stock Of ' + time.strftime("%d-%B")
        new_inventory_id = inventory_obj.create(cr, uid, {'name':opening_stock,'location_id':1})
        inventory_obj.prepare_inventory(cr, uid,new_inventory_id,context={})
             
        
#for not imported product
        fault=False
        #fieldnames = ['id','order_id','default_code','name','quantity','price','discount']
        #file_write = open('/tmp/reimport_product.csv','wb')
        fieldname.append('Error')
            
        reimport_file_writer = open('/tmp/reimport_stone_%s_%s.csv' %(uid,current_date),'wb')
        csvwriter = csv.DictWriter(reimport_file_writer, delimiter=',', fieldnames=fieldname) 
        csvwriter.writeheader()
        count=0
        if fieldname < 31:
            raise osv.except_osv(('Fields not match!!!'),
                    ('Please match fields with Sample Column file...'))
        
        if 'Name' not in fieldname:
            raise osv.except_osv(('Field not match!!!'),
                    ('Name field not found...'))
        else:
            for row in reader:
                
                if row.get('Name')==None or row.get('Name')==False or row.get('Name')=="":
                    raise osv.except_osv(('Field not mached!!!'),
                                         ('Name field must required...'))
                    
                count += 1
                message=[]
                stock_line_value={}
                product_data.update({
                                     'is_certified' : True,
                                     'is_export' : True,
                                     'is_fancy_color' : row.get('Is fancy color?',False) and (row.get('Is fancy color?')).lower()=='true' or False, 
                                     'price_stone' : row.get('Price',0.0),
                                     'standard_price' : row.get('Cost Price',0.0),
                                     'cost_price_discount' : row.get('Cost Price Discount',0.0),
                                     'type' : 'product',
                                     'supply_method' : 'buy',
                                     'procure_method' : 'make_to_stock',
                                     'cost_method' : 'standard',
                                     'name' : row.get('Name'),
                                     'product_status' : 'available',
                                     'default_code' : row.get('Internal Reference',row.get('Name')),
                                     'certificate_no' : row.get('Certificate No.',''),
                                     'discount' : row.get('Discount',0.0),
                                     'product_length' : row.get('Length',0.0),
                                     'product_width' : row.get('Width',0.0),
                                     'product_height' : row.get('Height',0.0),
                                     'crown_angle' : row.get('Crown Angle',0.0), 
                                     'product_depth' : row.get('Depth',0.0),
                                     'product_table' : row.get('Table',0.0),
                                     'gridle_percentage' : row.get('Girdle%',0.0),
                                     'crown_height' : row.get('Crown Height',0.0),
                                     'pavilion_depth' : row.get('Pavillion Depth',0.0),
                                     'pavilion_height' : row.get('Pavillion Angle',0.0),
                                     'fancy_color_intensity' : row.get('Fancy Color Intensity',0.0),
                                     'fancy_color_overtone' : row.get('Fancy Color Overtone',0.0),
                                     'laser_inspection' : row.get('Laser Inscription',False) and (row.get('Laser Inscription')).lower()=='true' or False,
                                     'description' : row.get('Comment',''),
                                     'weight' : row.get('Weight',0.0),
                                    })
                                
                if row.get('Shape',False) and row.get('Shape')!='NA':
                    shape_id = shape_obj.search(cr, uid, [('name','=',(row.get('Shape')).strip())])
                    if shape_id:
                        product_data.update({'shape_id' : shape_id[0]})
                    else:
                        message.append("shape %s Not exist ,"%(row.get('Shape')))
                
                if row.get('Fancy Color',False) and row.get('Fancy Color')!='NA':
                    fancy_color_id = fancy_color_obj.search(cr, uid, [('name','=',(row.get('Fancy Color')).strip())])
                    if fancy_color_id:
                        product_data.update({'fancy_color_id' : fancy_color_id[0]})
                    else:
                        message.append("fancy color %s Not exist ,"%(row.get('Fancy Color')))
                                        
                if row.get('Color',False) and row.get('Color')!='NA':
                    color_id = color_obj.search(cr, uid, [('name','=',(row.get('Color')).strip())])
                    if color_id:
                        product_data.update({'color_id' : color_id[0]})
                    else:
                        message.append("color %s Not exist"%(row.get('Color')))
                    
                if row.get('Cut',False) and row.get('Cut')!='NA':
                    cut_id = cut_obj.search(cr, uid, [('name','=',(row.get('Cut')).strip())])
                    if cut_id:
                        product_data.update({'cut_id' : cut_id[0]})
                    else:
                        message.append("cut %s Not exist"%(row.get('Cut')))
                                            
                if row.get('Clarity',False) and row.get('Clarity')!='NA':
                    clarity_id = clarity_obj.search(cr, uid, [('name','=',(row.get('Clarity')).strip())])
                    if clarity_id:
                        product_data.update({'clarity_id' : clarity_id[0]})
                    else:
                        message.append("clarity %s Not exist"%(row.get('Clarity')))
                                            
                if row.get('Polish',False) and row.get('Polish')!='NA':
                    polish_id = polish_obj.search(cr, uid, [('name','=',(row.get('Polish')).strip())])
                    if polish_id:
                        product_data.update({'polish_id' : polish_id[0]})
                    else:
                        message.append("polish %s Not exist"%(row.get('Polish')))
                                            
                if row.get('Symmetry',False) and row.get('Symmetry')!='NA':
                    symmetry_id = symmentry_obj.search(cr, uid, [('name','=',(row.get('Symmetry')).strip())])
                    if symmetry_id:
                        product_data.update({'symmetry_id' : symmetry_id[0]})
                    else:
                        message.append("symmetry %s Not exist"%(row.get('Symmetry')))
                                             
                if row.get('Fluorescence Color',False) and row.get('Fluorescence Color')!='NA':
                    fluorescence_color_id = fluorescence_color_obj.search(cr, uid, [('name','=',(row.get('Fluorescence Color')).strip())])
                    if fluorescence_color_id:
                        product_data.update({'fluorescence_color_id' : fluorescence_color_id[0]})                        
                    else:
                        message.append("Fluorescence Color %s Not exist"%(row.get('Fluorescence Color')))
                        
                if row.get('Fluorescence Intensity',False) and row.get('Fluorescence Intensity')!='NA':
                    fluorescence_intensity_id = fluorescence_intencity_obj.search(cr, uid, [('name','=',(row.get('Fluorescence Intensity')).strip())])
                    if fluorescence_intensity_id:
                        product_data.update({'fluorescence_intensity_id' : fluorescence_intensity_id[0]})                        
                    else:
                        message.append("fluorescence intensity %s Not exist"%(row.get('Fluorescence Intensity')))
                        
                if row.get('Lab',False) and row.get('Lab')!='NA':
                    lab_id = lab_obj.search(cr, uid, [('name','=',(row.get('Lab')).strip())])
                    if lab_id:
                        product_data.update({'lab_id' : lab_id[0]})
                    else:
                        message.append("lab %s Not exist"%(row.get('Lab')))
 
                if row.get('Girdle',False) and row.get('Girdle')!='NA':
                    girdle_id = girdle_obj.search(cr, uid, [('name','=',(row.get('Girdle')).strip())])
                    if girdle_id:
                        product_data.update({'girdle_id' : girdle_id[0]})                      
                    else:
                        message.append("girdle %s Not exist"%(row.get('Girdle')))
                                              
                if row.get('Culet Size',False) and row.get('Culet Size')!='NA':
                    culet_id = culet_size_obj.search(cr, uid, [('name','=',(row.get('Culet Size')).strip())])
                    if culet_id:
                        product_data.update({'culet_id' : culet_id[0]})   
                    else:
                        message.append("culet %s Not exist"%(row.get('Culet Size')))
                        
                if row.get('Culet Condition',False) and row.get('Culet Condition')!='NA':
                    culet_condition_id = culet_condition_obj.search(cr, uid, [('name','=',(row.get('Culet Condition')).strip())])
                    if culet_condition_id:
                        product_data.update({'culet_condition' : culet_condition_id[0]})
                    else:
                        message.append("culet condition %s Not exist"%(row.get('Culet Condition')))
                        
#create or write product and fill inventory
                if row.get('Location',False):
                    location_id = stock_location_obj.search(cr, uid, [('name','=',(row.get('Location')).strip())])
                    if not location_id:
                        message.append("Location %s Not exist"%(row.get('Location')))
                        
                if row.get('Manufacturer',False):
                    res_partner_id = res_partner_obj.search(cr, uid, [('name','=',(row.get('Manufacturer')).strip())])
                    if not res_partner_id:
                        message.append("Manufacturer %s Not exist"%(row.get('Manufacturer')))
                                            
                        
                if len(message) <= 0:
                    context.update({'stone_import':True})  
                    product_id = product_obj.search(cr, uid,[('name','=',row.get('Name'))],context=context)
                    if not product_id:
                        new_product_id = product_obj.create(cr, uid, product_data, context={})
                        cr.commit()
                        if row.get('Manufacturer'):
                            product_template = product_obj.browse(cr, uid, new_product_id, context={})
                            res_partner_id = res_partner_obj.search(cr, uid, [('name','=',row.get('Manufacturer'))])
#for tick as manufacturer
                            #res_partner_data = res_partner_obj.read(cr,uid,res_partner_id[0])
                            #if res_partner_data('is_manufacture',False)==False:
                            #    res_partner_obj.write(cr, uid, res_partner_id[0],{'is_manufacture':True})
                                
                            if res_partner_id:
                                product_supplier_obj.create(cr, uid, {
                                                              'name' : res_partner_id[0],
                                                              'sequence' : 1,
                                                              'min_qty' :0.0,
                                                              'delay' : 1,
                                                              'product_code' : row.get('Manufacturer Code',''),
                                                              'product_tmpl_id' : product_template.product_tmpl_id.id,
                                                              })                         
                        if row.get('Location',False):
                            stock_line_value.update({'value': {'product_qty': 1.0,
                                                               'product_uom_id' : 1, 
                                                               'prod_lot_id': False,
                                                               'inventory_id' : new_inventory_id,
                                                               'product_id' : new_product_id,
                                                               'location_id': location_id[0],
                                                               }
                                                    })#'product_uom': 1, 
                            stock_inventory_line_obj.create(cr, uid, stock_line_value.get('value'), context={})
                            inventory_entry=True
                        imported_product += 1
                    else:
                        if self_obj.is_update==True:
                            product_obj.write(cr, uid, product_id,product_data, context={})
                            updated_product+=1
               
                else:
                    row.update({'Error':str(message)})
                    csvwriter.writerow(row)
                    not_imported_product+=1
                    
                print '%s-----%s'%(datetime.strftime(datetime.now(),'%H %M %S'),count)
                
########for inventory        
        if inventory_entry:
            try:
                config_param_obj = self.pool.get('ir.config_parameter')
                fill_inventory = config_param_obj.get_param(cr,uid,'fill_inventory')
                
                if fill_inventory and fill_inventory.lower()=='yes':
                    inventory_obj.action_done(cr, uid, [new_inventory_id], context=context)      
            
            except Exception,e:
                _logger.info('Error  : %s' %(e))
        else:
            inventory_obj.unlink(cr, uid, [new_inventory_id], context)
     
        data_id = data_obj._get_id(cr, uid, 'import_product_ept', 'import_product_message_form_view_ept')
        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id
            
        reimport_file_writer.close()
        
        file_read.close()                
        context.update({
                        'reimportable_file' : '/tmp/reimport_stone_%s_%s.csv' %(uid,current_date),
                        'imported_product' : imported_product,
                        'not_imported_product' : not_imported_product,
                        'updated_product' : updated_product,
                        'count' : count,
                       })
#send confirmation mail
        #self.send_mail(cr, uid, ids, reimport_file_path, context)

#for import history

        res_user_obj= self.pool.get('res.users').browse(cr, uid, uid,context)    
            
        file_read = open('/tmp/import_stone_%s_%s.csv' %(uid,current_date),'rb')
        out = base64.encodestring(file_read.read())
        file_read.close()
        
        file_read = open('/tmp/reimport_stone_%s_%s.csv' %(uid,current_date),'rb')
        reimportable_file_out = base64.encodestring(file_read.read())
        file_read.close()
                
        #os.remove('/tmp/product_product.csv')
                
        self.pool.get('import.history.ept').create(cr, uid, {
                                                             'imported_by':res_user_obj.name,
                                                             'imported_date':datetime.now(),
                                                             'imported_product':imported_product,
                                                             'not_imported_product':not_imported_product,
                                                             'updated_product':updated_product,
                                                             'total_stones':count,
                                                             'file':out,
                                                             'reimported_file':reimportable_file_out,
                                                             'file_path':'/tmp/reimport_stone_%s_%s.csv' %(uid,current_date),
                                                             })
        value = {
                'name': 'Import Details',
                'view_type': 'form',
                'res_model': 'import.product.message.ept',
                'view_id': False,
                'views': [(view_id, 'form')],
                'context': context,
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
        
        print '%s-after fill inventory-%s'%(datetime.strftime(datetime.now(),'%H %M %S'),count)
        return value          
    

#        _logger.info('Email successfully sent to: %s', addresses)

