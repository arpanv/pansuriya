from openerp.osv import fields, osv, orm
from openerp import tools

class stock_location_ept(osv.osv):
    _inherit = 'stock.location'
    _columns = {
                'location_rfid_tag' : fields.char("RFID Tag", size=256)
                }
    
stock_location_ept()
class stock_picking_ept(osv.osv):
    _inherit = 'stock.picking'
    
    def daily_stock_report(self, cr, uid, loc_rfid_tag):
        #context={}
        #product_ids = self.pool.get('product.product').search(cr, uid, [('is_certified','=','True'),('product_status','in',['available','hold']),('rfid_tag','=',True)], context)
        #product_data = self.pool.get('product.product').read(cr, uid, product_ids, context)
        res = []
        query="""
            select pro.id as "StoneId",pro.name_template as "StoneName",coalesce(pro_shape.name,'') as "Shape",
            coalesce(pro.certificate_no,'') as "Certificate No.",
            coalesce(pro.rfid_tag,'') as "RFIDtag",coalesce(pro.weight,0) as "Weight",
            coalesce(pro_color.name,'') as "Color",coalesce(pro_cut.name,'') as "Cut",
            coalesce(pro_polish.name,'') as "Polish",coalesce(pro_symmetry.name,'') as "Symmetry",
            coalesce(pro_lab.name,'') as "Lab",coalesce(pro_gridle_thin.name,'') as "GridleThin",
            coalesce(pro_gridle_thick.name,'') as "GridleThick",coalesce(pro_gridle.name,'') as "Gridle",
            coalesce(pro_culet_con.name,'') as "CuletCondition",coalesce(pfc.name,'') as "FluorescenceColor",
            coalesce(pro_fancy_clr.name,'') as "FancyColor",coalesce(pfi.name,'') as "FluorescenceIntensityName",
            coalesce(pro.product_length,0) as "Length",coalesce(pro.product_width,0) as "Width",
            coalesce(pro.product_height,0) as "Height",coalesce(pro.product_depth,0) as "Depth",
            coalesce(pro.product_table,0) as "Table",coalesce(pro.weight,0) as "Weight",
            coalesce(pro.gridle_condition,'') as "GridleCondition",coalesce(pro.diameter,'') as "Diameter",
            coalesce(pro_clarity.name,'') as "Clarity",coalesce(product_status,'') as "Status",
            coalesce(pro.price_caret,0) as "Price/caret",coalesce(pro.rapnet_price,0) as "RapnetPrice",
            coalesce(pro.discount,0) as "Discount",coalesce(pro.list_price,0) as "Total"
            from product_product pro
            join stock_location loc on pro.location_id = loc.id
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
            left join product_clarity pro_clarity on pro.clarity_id = pro_clarity.id
            where product_status in ('available','hold') and is_certified=true and loc.location_rfid_tag='%(loc_rfid_tag)s'
               """%({'loc_rfid_tag':loc_rfid_tag})
        #left join product_status pro_status on pro.status_id = pro_status.id
        cr.execute(query)     
        res=cr.dictfetchall()
        return res
    
    def get_box_rfid(self,cr, uid):
        query = """
                select name,location_rfid_tag from stock_location where name like ('%BOX%')
                """
        cr.execute(query)     
        res=cr.dictfetchall()
        return res
    

