from osv import fields, osv
from tools.translate import _

class emipro_execute_python(osv.osv):
    _name = "emipro.execute.python"
    _columns = {
        'name' : fields.char('Name',size=1024,required=True),
        'code': fields.text('Python Code',required=True),
        'result':fields.text('Result',readonly=True),
        }
    
    def execute_code(self,cr,uid,ids,context=None):
        localdict = {'self':self,'cr':cr,'uid':uid, 'context':context,'user_obj':self.pool.get('res.users').browse(cr,uid,uid,context=context)}
        for obj in self.browse(cr,uid,ids,context=context):
            try :
                exec obj.code in localdict
                if localdict.get('result', False):
                    self.write(cr,uid,ids,{'result':localdict['result']})
                else : 
                    self.write(cr,uid,ids,{'result':''})
            except Exception, e:
                raise osv.except_osv(_('Error !'), _('Python code is not able to run ! message : %s' %(e)))
        return True
    def execute_code_by_cron(self,cr,uid,args,context=None):
        localdict = {'self':self,'cr':cr,'uid':uid, 'context':context,'user_obj':self.pool.get('res.users').browse(cr,uid,uid,context=context)}
        for obj in args:
            try :
                exec obj in localdict
            except Exception, e:
                raise osv.except_osv(_('Error !'), _('Python code is not able to run ! message : %s' %(e)))
        return True    

emipro_execute_python()
