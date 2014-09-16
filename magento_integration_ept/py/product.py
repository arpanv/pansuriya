import magento
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import StringIO
import os
import simplejson
import base64
from datetime import datetime, timedelta,date
class Product(osv.Model):
    """Product
    """
    _inherit = 'product.product'

    _columns = {
                'is_auction':fields.boolean('Is Auction ?'),
                'auction_time':fields.integer('Auction Time'),
                'auction_date':fields.datetime('Auction Date'),
                }
    
    def auction_info(self,cr, uid, ids, context={}):
        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'magento_integration_ept', 'product_auction_form_view')
        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id
          
        value = {
                   'name': _('Auction Information'),
                   'view_type': 'form',
                   'res_model': 'product.auction',
                   'view_id': False,
                   'views': [(view_id, 'form')],
                   'view_mode' : 'form',
                   'type': 'ir.actions.act_window',
                   'target': 'new',
                   'nodestroy': True,                    
               }
        return value
    
    def find_or_create_magento_shipping(self, cr, uid, context={}):
        #product_ids = self.search(cr, uid, [('default_code','=','service001')], context)
        product_ids = self.search(cr, uid, [('default_code','=','shipping001')], context=context)
        if product_ids:
            return product_ids[0]
        vals = {
                    'name':'shipping_charge',
                    'sale_ok':False,
                    'purchase_ok':False,
                    'type' : 'service',
                    'default_code' : 'shipping001'
                }
        new_product_id = self.create(cr, uid, vals, context)
        return new_product_id    
   
    def export_to_magento(self, cursor, user, product, category, context):
        """Export the given `product` to the magento category corresponding to
        the given `category` under the current website in context

        :param cursor: Database cursor
        :param user: ID of current user
        :param product: Browserecord of product to be exported
        :param category: Browserecord of category to which the product has
                         to be exported
        :param context: Application context
        :return: Browserecord of product
        """
                
        website_obj = self.pool.get('magento.instance.website')
        website_product_obj = self.pool.get('magento.website.product')

        if not product.default_code:
            raise osv.except_osv(
                _('Invalid Product!'),
                _('Product %s has a missing code.') %
                product.name,
            )
            
        website = website_obj.browse(
            cursor, user, context['magento_website'], context=context
        )
        instance = website.instance

        with magento.Product(
            instance.url, instance.api_user, instance.api_key
        ) as product_api:

            web_product_ids=website_product_obj.search(cursor,user,[('product','=',product.id),('website','=',context['magento_website'])])          
            if web_product_ids:
                magento_id = website_product_obj.browse(cursor,user,web_product_ids[0]).magento_id
                product_api.call(
                    'ol_catalog_product.update', [                
                         magento_id,
                        self.get_product_values_for_export_to_magento(
                            product, [category], [website], context
                        )
                    ]
                )

            else:
                magento_id = product_api.call('ol_catalog_product.create', ['simple',
                  int(context['magento_attribute_set']),
                  product.default_code,
                  self.get_product_values_for_export_to_magento(product, [category], [website], context)])
                    
            web_magento_ids = website_product_obj.search(cursor,user,[('magento_id','=',magento_id),('website','=',context['magento_website'])])
            if not web_magento_ids:
                website_product_obj.create(cursor, user, {
                    'magento_id': magento_id,
                    'website': context['magento_website'],
                    'product': product.id,
                }, context=context)
            self.write(cursor, user, product.id, {
                'magento_product_type': 'simple'
            }, context=context)
        return product

    
    def get_product_values_for_export_to_magento(
        self, product, categories, websites, context
    ):
        """Creates a dictionary of values which have to exported to magento for
        creating a product

        :param product: Browse record of product
        :param categories: List of Browse record of categories
        :param websites: List of Browse record of websites
        :param context: Application context
        """
        manufacturer_address = (product.company_id and product.company_id.street and (product.company_id.street + "\n")  or "")  + \
        (product.company_id and product.company_id.street2 and (product.company_id.street2 + "\n") or "")  + \
         (product.company_id and product.company_id.city  and (product.company_id.city + "\n") or "")  +\
         (product.company_id and product.company_id.zip and (product.company_id.zip + "\n") or "")  +\
         (product.company_id.state_id and product.company_id.state_id.name and (product.company_id.state_id.name + "\n")  or "")  +\
         (product.company_id.country_id and product.company_id.country_id.name and (product.company_id.country_id.name + "\n") or "")
        
	auction_date = product.auction_date and datetime.strptime(product.auction_date,'%Y-%m-%d %H:%M:%S') or '' 
        converted_auction_date =product.auction_date and datetime.strftime(auction_date,'%m/%d/%Y') or ''

        return {
            'categories': map(
                lambda mag_categ: mag_categ.magento_id,
                categories[0].magento_ids
            ),  
            'is_certified':product.is_certified,
            'image':product.image or None,
            'thumbnail':product.image or None,
            'small_image':product.image or None,
            'websites': map(lambda website: website.magento_id, websites),
            'name': product.name,
            'description': product.description or product.name,
            'short_description': product.description or product.name,
            'weight': product.weight,
            'special_price':product.list_price,
            'price': product.price_unit,
            'tax_class_id':'0',#1
            'status': '1',
            'visibility': '4',
            'color':product.color_id and product.color_id.name or None,
            'clarity':product.clarity_id.name,
            'cut':product.cut_id.name,
            'polish':product.polish_id.name,
            'shape':product.shape_id.name,
            'symmetry':product.symmetry_id.name,
            'fluorescence':product.fluorescence_intensity_id.name,
            'length':product.product_length,
            'width':product.product_width,
            'height':product.product_height,
            'milky':product.milky,
            'shade':product.shade,
            'lab':product.lab_id.name,
            'laser_inscription':product.laser_inspection,
            'tinge':product.tinge,
            'table':product.product_table,
            'girdle_thin':product.gridle_thin_id.name,
            'girdle_thick':product.gridle_thick_id.name,          
            'girdle':product.gridle_id.name,
            'girdle_percentage':product.gridle_percentage,
            'treatment':product.treatment,
            'diameter':product.diameter,
            'table_inc':product.table_inc,
            'report_no':product.certificate_no,
            'eye_clean':product.eye_clean,
            'natts':product.natts,
            'browness':product.browness,
            'hna':product.hna,
            'product_status':product.product_status,
            'girdle_condition':product.gridle_condition,
            'culet_size':product.culet_id.name,
            'culet_condition':product.culet_condition.name,
            'fluorescence_color':product.fluorescence_color_id.name,
            'crown_height':product.crown_height,
            'crown_angle':product.crown_angle,
            'pavilion_depth':product.pavilion_depth,
            'pavilion_angle':product.pavilion_height,
            'fancy_color':product.fancy_color_id.name,
            'fancy_color_intensity':product.fancy_color_intensity,
            'fancy_color_overtone':product.fancy_color_overtone,
            'depth':product.product_depth,
            'rapnet_price':product.rapnet_price,
            'back_percentage':product.discount,
            'carat_price':product.price_caret,
            'list_price':product.list_price,
            'report_no':product.certificate_no,
            'country_of_manufacture':product.location_id and product.location_id.name or '',
            'star_length':product.star_length,
            'lower_half':product.lower_half,
            'manufacturer':(product.company_id and product.company_id.name) or (self.pool.get('res.users').browse(self.cr,self.uid,self.uid).company_id.name),
	    'manufacturer_address' : str(manufacturer_address),
            'manufacturer_email' : (product.company_id and product.company_id.email) or (self.pool.get('res.users').browse(self.cr,self.uid,self.uid).company_id.email),
            'is_auction':product.is_auction or False,
            'auction_time':product.auction_time or None,
            'auction_date':converted_auction_date,
        }

    def _get_color_id(self,cr,uid,color=None,context={}):
        color_ids = self.pool.get('product.color').search(cr,uid,[('name','=',color)])
        if color_ids:
            return color_ids[0]
        else:
            return self.pool.get('product.color').create(cr,uid,{'name':color})
        
    def _get_clarity_id(self,cr,uid,clarity=None,context={}):
        clarity_ids = self.pool.get('product.clarity').search(cr,uid,[('name','=',clarity)])
        if clarity_ids:
            return clarity_ids[0]
        else:
            return self.pool.get('product.clarity').create(cr,uid,{'name':clarity})
        
    def _get_cut_id(self,cr,uid,cut=None,context={}):
        cut_ids = self.pool.get('product.cut').search(cr,uid,[('name','=',cut)])
        if cut_ids:
            return cut_ids[0]
        else:
            return self.pool.get('product.cut').create(cr,uid,{'name':cut})
    
    def _get_polish_id(self,cr,uid,polish=None,context={}):
        polish_ids = self.pool.get('product.polish').search(cr,uid,[('name','=',polish)])
        if polish_ids:
            return polish_ids[0]
        else:
            return self.pool.get('product.polish').create(cr,uid,{'name':polish})
    
    def _get_shape_id(self,cr,uid,shape=None,context={}):
        shape_ids = self.pool.get('product.shape').search(cr,uid,[('name','=',shape)])
        if shape_ids:
            return shape_ids[0]
        else:
            return self.pool.get('product.shape').create(cr,uid,{'name':shape})
    def _get_symmetry_id(self,cr,uid,symmetry=None,context={}):
        symmetry_ids = self.pool.get('product.symmetry').search(cr,uid,[('name','=',symmetry)])
        if symmetry_ids:
            return symmetry_ids[0]
        else:
            return self.pool.get('product.symmetry').create(cr,uid,{'name':symmetry})
        
    def _get_fluorescence_intensity_id(self,cr,uid,fluorescence=None,context={}):
        fluorescence_ids = self.pool.get('product.fluorescence.intensity').search(cr,uid,[('name','=',fluorescence)])
        if fluorescence_ids:
            return fluorescence_ids[0]
        else:
            return self.pool.get('product.fluorescence.intensity').create(cr,uid,{'name':fluorescence})
        
    def _get_lab_id(self,cr,uid,lab=None,context={}):
        lab_ids = self.pool.get('product.lab').search(cr,uid,[('name','=',lab)])
        if lab_ids:
            return lab_ids[0]
        else:
            return self.pool.get('product.lab').create(cr,uid,{'name':lab})
        
######added
    def _get_gridle_id(self,cr,uid,gridle=None,context={}):
        gridle_ids = self.pool.get('product.gridle').search(cr,uid,[('name','=',gridle)])
        if gridle_ids:
            return gridle_ids[0]
        else:
            return self.pool.get('product.gridle').create(cr,uid,{'name':gridle})        
    
    def _get_culet_condition(self,cr,uid,culet_condition=None,context={}):
        culet_condition_ids = self.pool.get('product.culet_condition').search(cr,uid,[('name','=',culet_condition)])
        if culet_condition_ids:
            return culet_condition_ids[0]
        else:
            return self.pool.get('product.culet_condition').create(cr,uid,{'name':culet_condition})
        
        
        
        
    def _get_gridle_thin_id(self,cr,uid,gridle_thin=None,context={}):
        gridle_thin_ids = self.pool.get('product.gridle_thin').search(cr,uid,[('name','=',gridle_thin)])
        if gridle_thin_ids:
            return gridle_thin_ids[0]
        else:
            return self.pool.get('product.gridle_thin').create(cr,uid,{'name':gridle_thin})
        
    def _get_gridle_thick_id(self,cr,uid,gridle_thick=None,context={}):
        gridle_thick_ids = self.pool.get('product.gridle_thick').search(cr,uid,[('name','=',gridle_thick)])
        if gridle_thick_ids:
            return gridle_thick_ids[0]
        else:
            return self.pool.get('product.gridle_thick').create(cr,uid,{'name':gridle_thick})
        
    def _get_culet_id(self,cr,uid,culet=None,context={}):
        culet_ids = self.pool.get('product.culet').search(cr,uid,[('name','=',culet)])
        if culet_ids:
            return culet_ids[0]
        else:
            return self.pool.get('product.culet').create(cr,uid,{'name':culet})
    def _get_fluorescence_color_id(self,cr,uid,fluorescence_color=None,context={}):
        f_color_ids = self.pool.get('product.fluorescence.color').search(cr,uid,[('name','=',fluorescence_color)])
        if f_color_ids:
            return f_color_ids[0]
        else:
            return self.pool.get('product.fluorescence.color').create(cr,uid,{'name':fluorescence_color})
        
    def _get_fancy_color_id(self,cr,uid,fancy_color=None,context={}):
        f_color_ids = self.pool.get('product.fancy.color').search(cr,uid,[('name','=',fancy_color)])
        if f_color_ids:
            return f_color_ids[0]
        else:
            return self.pool.get('product.fancy.color').create(cr,uid,{'name':fancy_color})
    
    def create_using_magento_data(
        self, cursor, user, product_data, context=None
    ):
        """Create product using magento data

        :param cursor: Database cursor
        :param user: ID of current user
        :param product_data: Product Data from magento
        :param context: Application context
        :returns: Browse record of product created
        """
        category_obj = self.pool.get('product.category')
        website_obj = self.pool.get('magento.instance.website')
        
        # Get only the first category from list of categories
        # If not category is found, put product under unclassified category
        # which is created by default data
        if product_data.get('categories'):
            category_id = category_obj.find_or_create_using_magento_id(
                cursor, user, int(product_data['categories'][0]),
                context=context
            ).id
        else:
            category_id, = category_obj.search(cursor, user, [('name', '=', 'Unclassified Magento Products')], context=context)


        product_values = self.extract_product_values_from_data(product_data)
        
        product_values.update({
            'categ_id': category_id,
            'uom_id':
                website_obj.get_default_uom(
                    cursor, user, context
                ).id,
            'magento_ids': [(0, 0, {
                'magento_id': int(product_data['product_id']),
                'website': context['magento_website'],
            })],   
            'is_certified':product_data.get('is_certified',0),           
#             'price_unit':product_data['price',0.00],
#             'rapnet_price':product_data['rapnet_price',0.00],
#             'price_caret':product_data['carat_price',0.00],

            'magento_product_type': product_data['type'],
            'procure_method': 'make_to_stock',
            'magento_id': int(product_data['product_id']),
            'website': context['magento_website'],
            'weight':product_data.get('weight',0.00),
            'color_id':product_data.get('color',False) and self._get_color_id(cursor,user,product_data.get('color',None),context=context) or False,
            'clarity_id':product_data.get('clarity',False) and self._get_clarity_id(cursor,user,product_data.get('clarity',None),context=context) or False,
            'cut_id':product_data.get('cut',False) and self._get_cut_id(cursor,user,product_data.get('cut',None),context=context) or False,
            'polish_id':product_data.get('polish',False) and self._get_polish_id(cursor,user,product_data.get('polish',None),context=context) or False,
            'shape_id':product_data.get('shape',False) and self._get_shape_id(cursor,user,product_data.get('shape',None),context=context) or False,
            'symmetry_id':product_data.get('symmetry',False) and self._get_symmetry_id(cursor,user,product_data.get('symmetry',None),context=context) or False,
            'fluorescence_intensity_id':product_data.get('fluorescence',False) and self._get_fluorescence_intensity_id(cursor,user,product_data.get('fluorescence',None),context=context) or False,
            'product_length':product_data.get('length',0.00),
            'product_width':product_data.get('width',0.00),
            'product_height':product_data.get('height',0.00),
            'milky':product_data.get('milky',0.00),
            'shade':product_data.get('shade',0.00),
            'lab_id':product_data.get('lab',False) and self._get_lab_id(cursor,user,product_data.get('lab',False),context=context) or False,
            'laser_inspection':product_data.get('laser_inspection',False),
            'tinge':product_data.get('tinge',False),
            'product_table':product_data.get('table',False),
            'gridle_thin_id':product_data.get('girdle_thin',False) and self._get_gridle_thin_id(cursor,user,product_data.get('girdle_thin',False),context=context) or False,
            'gridle_thick_id':product_data.get('girdle_thick',False) and self._get_gridle_thick_id(cursor,user,product_data.get('girdle_thick',False),context=context) or False,
            'gridle_id' : product_data.get('girdle',False) and self._get_gridle_id(cursor,user,product_data.get('gridle',False),context=context) or False,
            'gridle_percentage' : product_data.get('girdle_percentage',0.00),
            'culet_condition': product_data.get('culet_condition',False) and self._get_culet_condition(cursor,user,product_data.get('culet_condition',False),context=context) or False,
            'treatment':product_data.get('treatment',False),
            'diameter':product_data.get('diameter',False),
            'gridle_condition' : product_data.get('girdle_condition',False),
            'table_inc' : product_data.get('table_inc',False),
            'eye_clean' : product_data.get('eye_clean',False),
            
            'culet_id':self._get_culet_id(cursor,user,product_data.get('culet_size',False),context=context),            
            'fluorescence_color_id': self._get_fluorescence_color_id(cursor,user,product_data.get('fluorescence_color',False),context=context),
            'crown_height': product_data.get('crown_height',False),
            'crown_angle': product_data.get('crown_angle',False),
            'pavilion_depth': product_data.get('pavilion_depth',False),
            'pavilion_height': product_data.get('pavilion_angle',False),
            'fancy_color_id': self._get_fancy_color_id(cursor,user,product_data.get('fancy_color',False),context=context),   
            'fancy_color_intensity': product_data.get('fancy_color_intensity',False),
            'fancy_color_overtone': product_data.get('fancy_color_overtone',False),
            'rough_origin': product_data.get('rough_origin',False),
            'product_depth': product_data.get('depth',False),
            'pavilion_depth': product_data.get('pavilion_depth',False),
            'pavilion_depth': product_data.get('pavilion_depth',False),  
            'certificate_no':product_data.get('report_no',False),        
            'star_length':product_data.get('star_length',False),
            'lower_half':product_data.get('lower_half',False),
            
        })

        if product_data['type'] == 'bundle':
            # Bundles are produced
            product_values['supply_method'] = 'produce'

        product_id = self.create(cursor, user, product_values, context=context)
        
        return self.browse(cursor, user, product_id, context=context)
Product()

######Extended for image path
class product_image_path(osv.osv):
    _inherit = 'magento.website.product'
    _columns =dict(
                   mag_image_path=fields.char('Image Path',size=256),
                   mag_image_flag = fields.boolean('Image Flag')
                  )
    
####This code for directly update catalog in magento
#    def write(self, cr, uid, ids, vals, context):
#        res = super(Product, self).write(cr, uid, ids, vals, context=context)
#         if vals.get('magento_product_type',False):
#             return res
#         if not isinstance(ids,list):
#             ids= [ids]
#         
#         website_product_obj = self.pool.get('magento.website.product')
#         
#         for id in ids:
#             website_ids = self.pool.get('magento.instance.website').search(cr,uid,[('magento_products.product','=',id)])
#             for website_id in website_ids:
#                 context.update({'magento_website':website_id})
#                 product_browse = self.browse(cr,uid,id,context=context)
#                 self.export_to_magento(cr, uid, product_browse, product_browse.categ_id, context=context)        
#        return res
 
