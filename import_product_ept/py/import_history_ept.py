from openerp.osv import osv,fields
import csv
from StringIO import StringIO
import base64

class import_history_ept(osv.osv):
    _name='import.history.ept'
    _columns= {
               'imported_by' : fields.char('By'),
               'imported_date' : fields.datetime(),
               'file' : fields.binary('Choose File',filters='*.csv'),
               'reimported_file' : fields.binary('Reimportable file',filters='*.csv'),
               'total_stones' : fields.integer('Total Stones',readonly="1"),
               'imported_product' : fields.integer('Imported', readonly="1"),
               'updated_product' : fields.integer('Updated',readonly="1"),
               'not_imported_product' : fields.integer('Not Imported', readonly="1"),
               'file_path' : fields.char('File Path', readonly="1"),
            }
    _order='imported_date desc'