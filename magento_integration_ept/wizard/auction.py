from openerp.osv import fields,osv
from openerp.tools.translate import _
from datetime import datetime, timedelta,date
from dateutil import tz
class product_auction(osv.osv_memory):
    _name = "product.auction"
    _columns = {
                'auction_time':fields.selection([
                                                (12,12),
                                                (24,24),
                                                (36,36),
                                                (48,48),
                                                (60,60),
                                                (72,72)
                                                ], 'Auction Time'),
                'auction_date':fields.date('Auction Date'),
                }
    def calculate_auction(self, cr, uid, ids, context={}):
        '''
        Called from wizard for calculation of auction time.
        '''
        self_data=self.browse(cr, uid, ids[0])
        auction_time=self_data.auction_time
        
        auction_starting_time = int((self.pool.get('ir.config_parameter').get_param(cr,uid,'auction_starting_time'))) - 0.70#if 9 is starting then stop editing at 8.30
        for product_obj in self.pool.get('product.product').browse(cr, uid, context.get('active_ids'), context={}):
#converting auction_date UCT to ind
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            
            current_date = (datetime.now().replace(tzinfo=from_zone)).astimezone(to_zone)
            current_date = datetime.strptime(datetime.strftime(current_date,'%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
            
    #Allocation of auction_date and auction_time
            entered_auction_date_utc = datetime.strptime(self_data.auction_date,'%Y-%m-%d')
            entered_auction_date=(entered_auction_date_utc.replace(tzinfo=from_zone)).astimezone(to_zone)
            
            remove_entered_auction_date_hours = datetime.strftime(entered_auction_date,'%Y-%m-%d 00:00:00')#from time to string
            cal_entered_auction_date = datetime.strptime(remove_entered_auction_date_hours,'%Y-%m-%d %H:%M:%S')#parse string to time
            
            if not product_obj.auction_time:
                '''
                    You are not allowed to put auction date as today after 8.30, 
                '''
                if current_date < (cal_entered_auction_date + timedelta(hours=auction_starting_time)):
                    self.pool.get('product.product').write(cr, uid, product_obj.id,{'is_auction':True,
                                                                                    'auction_time':auction_time,
                                                                                    'auction_date':entered_auction_date_utc}, 
                                                                                    context={})
                    continue;
                else:
                    raise osv.except_osv(
                         _('Invalid Operation!'),
                         _('You have entered invalid date!!!')
                                          )
    #Updating auction_date and auction_time
            old_auction_date = datetime.strptime(product_obj.auction_date,'%Y-%m-%d %H:%M:%S')
            old_auction_date=(old_auction_date.replace(tzinfo=from_zone)).astimezone(to_zone)
            
            remove_old_auction_date_hours = datetime.strftime(old_auction_date,'%Y-%m-%d 00:00:00')
            cal_old_auction_date = datetime.strptime(remove_old_auction_date_hours,'%Y-%m-%d %H:%M:%S')
    
            if (cal_entered_auction_date + timedelta(hours=auction_starting_time)) > current_date:
                #Before 30 minute of auction, update is allowed  
                #and after auction_time, allowed to modify
                if (cal_old_auction_date + timedelta(hours=auction_starting_time)) > current_date or  \
                   (cal_old_auction_date + timedelta(hours=(auction_starting_time+product_obj.auction_time))) < current_date:
                        self.pool.get('product.product').write(cr, uid, product_obj.id,{'auction_time':auction_time,
                                                                                        'auction_date':entered_auction_date_utc
                                                                                        }, context={})
                        continue;
                else:
                    raise osv.except_osv(
                         _('Invalid Operation!'),
                         _('You have entered invalid date!!!')
                                          )
            else:
                raise osv.except_osv(
                     _('Invalid Operation!'),
                     _('You are not allowed to modify the date!!!')
                                      )
        return True
    
    def remove_auction(self, cr, uid, ids, context={}):
        auction_starting_time = int((self.pool.get('ir.config_parameter').get_param(cr,uid,'auction_starting_time'))) - 0.70#if 9 is starting then stop editing at 8.30
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        current_date = (datetime.now().replace(tzinfo=from_zone)).astimezone(to_zone)
        current_date = datetime.strptime(datetime.strftime(current_date,'%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

        for product_obj in self.pool.get('product.product').browse(cr, uid, context.get('active_ids'), context={}):
            if product_obj.is_auction:
                auction_date_utc = datetime.strptime(product_obj.auction_date,'%Y-%m-%d %H:%M:%S')
                auction_date=(auction_date_utc.replace(tzinfo=from_zone)).astimezone(to_zone)
        
                remove_auction_date_hours = datetime.strftime(auction_date,'%Y-%m-%d 00:00:00')#from time to string
                cal_auction_date = datetime.strptime(remove_auction_date_hours,'%Y-%m-%d %H:%M:%S')#parse string to time
                
                if current_date < (cal_auction_date + timedelta(hours=auction_starting_time)) or \
                   current_date > (cal_auction_date + timedelta(hours=(auction_starting_time+product_obj.auction_time))):
                
                    self.pool.get('product.product').write(cr, uid, product_obj.id,{'is_auction':False,
                                                                                    'auction_time':0.0,
                                                                                    'auction_date':None}, context={}) 
                else:
                    raise osv.except_osv(
                                         _('Invalid Operation!'),
                                         _('%s is in auction!!!')%(product_obj.name_template)
                                        )
        return True    
