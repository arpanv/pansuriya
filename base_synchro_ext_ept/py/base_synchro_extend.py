from openerp.osv import osv
import time
import threading
import xmlrpclib
from openerp.osv import fields, orm
from openerp import pooler

import logging
_logger = logging.getLogger(__name__)

class base_synchro(orm.TransientModel):
    """Synchronization Wizard Extend"""
    _inherit = 'base.synchro'
      
    def download_product(self, cr, uid):
        dt = time.strftime('%Y-%m-%d %H:%M:%S')
        _logger.info('***************************')
        _logger.info('synchro start at : %s'%(dt))
        server_ids = self.pool.get('base.synchro.server').search(cr, uid, [])
        for sid in server_ids:
            server = self.pool.get('base.synchro.server').browse(cr, uid, sid)
            for obj in self.pool.get('base.synchro.obj').search(cr, uid, [('server_id','=',sid)]):
                server_obj=self.pool.get('base.synchro.obj').browse(cr, uid, obj)
                
                self.synchronize(cr, uid, server, server_obj, context=None)
                #if server_obj.model_id.model=='product.product':
                    #self.supplier_synchro(cr, uid, server, context=None)
                self.pool.get('base.synchro.obj').write(cr, uid, [server_obj.id], {'synchronize_date': dt}, context={})
        _logger.info('***************************')
        _logger.info('synchro stop at : %s'%(dt))
        return True
    
    def synchronize(self, cr, uid, server, object_, context=None):
        '''
        Main controller function for synchronisation
        Establishes server connections, finds ids to sync and then
        either writes or creates them depending on requirement
        @return: True
        '''
        pool1 = RPCProxy(server)#ERPSyste
        pool2 = pooler.get_pool(cr.dbname)#ocentag
        
        self.meta = {}
        ids = []
        model = object_.model_id.model
        _logger.info('****Model**** : %s'%(model))
        if object_.action in ('d', 'b'):
            ids = pool1.get('base.synchro.obj').get_ids(
             cr, uid, model, object_.synchronize_date, eval(object_.domain), {'action':'d'}
                                                        )

        if object_.action in ('u', 'b'):
            ids += pool2.get('base.synchro.obj').get_ids(cr, uid,
                model,
                object_.synchronize_date,
                eval(object_.domain),
                {'action':'u'}
            )
        ids = [list(id_) for id_ in ids]
        ids.sort()
        for idx, (dt, id, action) in enumerate(ids):
            if action == 'd':
                pool_src = pool1
                pool_dest = pool2
            else:
                pool_src = pool2
                pool_dest = pool1

            record_fields = getattr(base_synchro,
                                    '_special_case_%s'.replace('.', '_')
                                    % model, [])

            record = pool_src.get(model).read(cr, uid, [id], record_fields,
                                              context=context)[0]
                                              
            
            if 'create_date' in record:
                del record['create_date']
            [record.update({key:val[0]}) for key, val in record.iteritems() if isinstance(val, tuple)]
            record = self.data_transform(cr, uid, pool_src, pool_dest, model,
                                         record, action, context=context)
            id2 = self.get_id(cr, uid, object_.id, id, action, context=context)
            if not (idx % 50):
                pass
############### Filter fields to not sync
            if object_.sync_only:
                fields = {}
                fields.update(record)
                data=[]
                for record_field in object_.avoid_ids:
                    if record_field.name in record:
                        data.append(record_field.name)
                
                for r in record : 
                    if r not in data :
                        del fields[r]
                record={}
                record.update(fields)
	        print "final fields data : %s"%(record)
            else :
                for record_field in object_.avoid_ids:
                    if  record_field.name in record:
                        del record[record_field.name]

            if id2:
                pool_dest.get(model).write(cr, uid, [id2], record,
                                           context=context)
                self.report_write += 1
            else:
                record = self.input(cr, uid, ids, record, context=context)
                idnew = pool_dest.get(model).create(cr, uid, record,
                                                    context=context)
                self.pool.get('base.synchro.obj.line').create(
                        cr, uid, {'obj_id': object_.id,
                                  'local_id': (action == 'u') and id or idnew,
                                  'remote_id': (action == 'd') and id or idnew
                                  }, context=context
                                                                      )
                self.report_create += 1
            self.meta = {}
        return True
#############################only test

class RPCProxyOne(object):
    '''
    returns specific object xmlrpc instances for the RPCProxy object
    '''
    def __init__(self, server, resource):
        self.server = server
        local_url = 'http://%s:%d/xmlrpc/common' % (server.server_url,
                                                    server.server_port)
        rpc = xmlrpclib.ServerProxy(local_url)
        self.uid = rpc.login(server.server_db, server.login, server.password)
        local_url = 'http://%s:%d/xmlrpc/object' % (server.server_url,
                                                    server.server_port)
        self.rpc = xmlrpclib.ServerProxy(local_url)
        self.resource = resource

    def __getattr__(self, name):
        return lambda cr, uid, *args, **kwargs: self.rpc.execute(
                                        self.server.server_db, self.uid,
                                        self.server.password, self.resource,
                                        name, *args
                                        )


class RPCProxy(object):
    '''
    Creates an instance of remote server credentials suitable for using over
    xmlrpc
    '''
    def __init__(self, server):
        self.server = server

    def get(self, resource):
        '''
        Returns the object model of the remote server.  Analagous to
        self.pool.get('res.partner') for example
        '''
        return RPCProxyOne(self.server, resource)   



class base_synchro_obj(osv.osv):
    _inherit = "base.synchro.obj"
    
    _columns = {
                'sync_only' : fields.boolean('Only below list need to Sync. ?'),
                }
    
    def unlink(self, cr, uid,ids, context={}):
        raise osv.except_osv(('Warning!'), ('You are not allow to delete this Object!'))
   
class base_syncho_Server(osv.osv):
    _inherit = 'base.synchro.server'
            
    def unlink(self, cr, uid, ids, context={}):
        raise osv.except_osv(('Warning!'), ('You are not allow to delete this Server!'))
    
class base_synchro_obj_line(osv.osv):
    _inherit = "base.synchro.obj.line"
        
    def unlink(self, cr, uid, ids, context={}):
        raise osv.except_osv(('Warning!'), ('You are not allow to delete this Object Line!'))
