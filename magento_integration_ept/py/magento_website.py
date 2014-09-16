import logging
import xmlrpclib
from copy import deepcopy
from datetime import datetime, timedelta,date
from pytz import timezone
import time
from dateutil import tz

from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import magento

from magento_integration.api import OrderConfig


_logger = logging.getLogger(__name__)
class InstanceWebsite(osv.Model):

    _name = 'magento.instance.website'
    _inherit = 'magento.instance.website'
       
    _columns = dict(
             magento_customers=fields.one2many(
             'magento.website.partner', 'website', 'Stores',
             readonly=True),
                    
            category_id=fields.many2one(
            'product.category', 'Magento Category',
            domain=[('magento_ids', '!=', None)]),
                    
            attribute_id=fields.many2one('magento.attributes','Attribute'),
             
             )    
InstanceWebsite()

##########Added from cron

class mag_instance_website(osv.osv):
    _name = 'magento.instance.website'
    _inherit = 'magento.instance.website'
    
    _columns = {
                'attribute_ids' : fields.one2many('magento.attributes','website_id','Attribute Sets')
                }
    
    def get_attribute_sets(self, cr, uid, ids, context={}):
        
        website = self.browse(cr, uid, ids[0], context)
        instance = website.instance
        
        with magento.ProductAttributeSet(
            instance.url, instance.api_user, instance.api_key
        ) as attribute_set_api:
            attribute_sets = attribute_set_api.list()
        
        magento_web_attr_obj=self.pool.get('magento.attributes')
            
        for attribute in attribute_sets:
            set_id = self.pool.get('magento.attributes').search(cr,uid,[('set_id','=',attribute['set_id'])])
            if not set_id:
                magento_web_attr_obj.create(cr, uid, {'set_id':attribute['set_id'], 'website_id':ids[0], 'name':attribute['name']})
        return True    
      
    def export_catalog_to_magento(self, cr, uid, ids=None, context={}):
        
        website_ids = self.search(cr, uid, [])
        for mag_ins_web_obj in self.browse(cr, uid, website_ids):
            if not mag_ins_web_obj.category_id or not mag_ins_web_obj.attribute_id:
                continue
            context.update({
                            'magento_website': mag_ins_web_obj.id,
                            'magento_attribute_set': mag_ins_web_obj.attribute_id.set_id,
                        })
            current_tz_obj = self.pool.get('res.users').browse(cr, uid, uid)
            
            if current_tz_obj:
                config_param = self.pool.get('ir.config_parameter')
                export_time = config_param.get_param(cr,uid,'time_for_export_catalog_to_magento_ept')
                
                print "****************"
                print current_tz_obj.tz
                print datetime.now()
                print "Export Time : ",export_time
                product_ids = [] 
                if ids is not None:
                    product_data = self.pool.get('exception.handler').read(cr, uid, ids, ['exce_id'], context)
                    for item in product_data:
                        product_ids.append(item.get('exce_id'))
                
                
                if not product_ids:
		    product_ids = self.pool.get('product.product').search(cr,uid,[])
		    #product_ids = self.pool.get('product.product').search(cr,uid,['|',
                    #('create_date','>=', datetime.now() - timedelta(hours=int(export_time) or 1)),
                    #('write_date','>=', datetime.now() - timedelta(hours=int(export_time) or 1)),
                    #('is_export','=',True)])
#                 for product in self.pool.get('product.product').browse(cr, uid, product_ids):
#                         self.pool.get('product.product').export_to_magento(
#                             cr, uid, product, mag_ins_web_obj.category_id, context=context
#                         )
		print product_ids
                import_limit=0
                for product in self.pool.get('product.product').browse(cr, uid, product_ids):
                    if import_limit==10:
			break;
                    print"masha h allah"
                    try:
			import_limit+=1
                        self.pool.get('product.product').export_to_magento(
                            cr, uid, product, mag_ins_web_obj.category_id, context=context
                        
                        )
                    except Exception,e:
                        vals = {
                                'exce_id' : product.id,
                                'data' : e,
                                'state' : 'exception',
                                'model_nm' : 'product.product',
                                }
                        self.pool.get('exception.handler').create(cr, uid, vals, context=context)
                return
mag_instance_website()
               

class magento_attributes(osv.osv):
    _description = 'Magento Attribute Sets'
    _name = 'magento.attributes'
    
    _columns = {
                'name' : fields.char("Name", size=256),
                'set_id':fields.char("Set Id", size=512),
                'website_id' : fields.many2one('magento.instance.website', 'Website')
               }

magento_attributes()
