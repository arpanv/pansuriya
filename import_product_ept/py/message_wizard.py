from openerp.osv import osv,fields
import csv
from StringIO import StringIO
import base64

class product_message(osv.osv_memory):
    _name='import.product.message.ept'
    _columns= {
               'message' : fields.text('',readonly="1"),
               'reimportable_file' : fields.binary('Choose File',filters='*.csv'),
               'imported_product' : fields.integer('Imported', readonly="1"),
               'updated_product' : fields.integer('Updated',readonly="1"),
               'not_imported_product' : fields.integer('Not Imported', readonly="1"),
               'file_path' : fields.char('File Path', readonly="1"),
               'total_stones' : fields.integer('Total Stones', readonly="1"),
            }
    
    def default_get(self, cr, uid, fields, context={}):
        res = super(product_message, self).default_get(cr, uid, fields, context=context)
        imported_product = context.get('imported_product',0)
        updated_product = context.get('updated_product',0)
        not_imported_product = context.get('not_imported_product',0)
        total_stones = context.get('count',0)
        if context.get('not_imported_product')>0:
            reimportable_file=context.get('reimportable_file','')
            path=context.get('reimportable_file','')
            file_read = open(reimportable_file,'rb')
            reimportable_file_out = base64.encodestring(file_read.read())
            file_read.close()
            
            res.update(reimportable_file=reimportable_file_out, file_path=path)
            
        res.update(
                   imported_product = imported_product,
                   not_imported_product = not_imported_product,
                   updated_product = updated_product,
                   total_stones = total_stones,
                   )
        return res
    
    def import_products_n_inventory(self,cr, uid, ids, context):
        context.update({'from_reimport_button':True})
        return self.pool.get('import.product.ept').import_products_n_inventory(cr, uid, ids, context)     
  