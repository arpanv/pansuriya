from openerp.osv import osv, fields

class product_clarity(osv.osv):
    _name = 'product.clarity'
    _columns = {
                'name' : fields.char('Clarity', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product clarity must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_clarity()

class product_color(osv.osv):
    _name = 'product.color'
    _columns = {
                'name' : fields.char('Color', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
         ('name_unique', 'unique(name)', 'Product color must be unique'),
         ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
         ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
     ]
product_color()

class product_cut(osv.osv):
    _name = 'product.cut'
    _columns = {
                'name' : fields.char('Cut', size=512),
                'seq' : fields.integer('Sequence'),
                }
    def _check_seq(self, cr, uid, ids, context={}):
        for id in self.browse(cr, uid, ids, context=context):
            if int(id.seq) <= 0:
                return False
        return True        
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product cut must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK(seq>0)','Sequence must be grater than zero'),
    ]
product_cut()

class product_culet(osv.osv):
    _name = 'product.culet'
    _columns = {
                'name' : fields.char('Culet Size', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_culet()

class product_culet_condition(osv.osv):
    _name = 'product.culet_condition'
    _columns = {
                'name' : fields.char('Culet Condition',size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product culet condition must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_culet_condition()

class product_fancy_color_intensity(osv.osv):
    _name = 'product.fancy.color.intensity'
    _columns = {
                'name' : fields.char('Fancy Color Intensity', size=512),
                'seq' : fields.integer('Sequence'),
                }
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product Fancy Color Intensity must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK(seq>0 )','Sequence must be grater than zero'),
    ]
    #
product_fancy_color_intensity()

class product_fancy_color_overtone(osv.osv):
    _name = 'product.fancy.color.overtone'
    _columns = {
                'name' : fields.char('Fancy Color Overtone', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product Fancy Color Overtone must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK(seq>0 )','Sequence must be grater than zero'),
    ]
product_fancy_color_overtone()

class product_fancy_color(osv.osv):
    _name = 'product.fancy.color'
    _columns = {
                'name' : fields.char('Fancy Color', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fancy color must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK(seq>0 )','Sequence must be grater than zero'),
    ]
product_fancy_color()

class product_fluorescence_color(osv.osv):
    _name = 'product.fluorescence.color'
    _columns = {
                'name' : fields.char('Fluorescence Color', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fluorescence color must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK(seq>0 )','Sequence must be grater than zero'),
    ]
product_fluorescence_color()

class product_fluorescence_intensity(osv.osv):
    _name = 'product.fluorescence.intensity'
    _columns = {
                'name' : fields.char('Fluorescence Intensity', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fluorescence intensity must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_fluorescence_intensity()

class product_gridle(osv.osv):
    _name = 'product.gridle'
    _columns = {
                'name' : fields.char('Gridle', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product gridle must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_gridle()

class product_insure(osv.osv):
    _name = 'product.insure'
    _columns = {
                'name' : fields.char('Insured By', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product insure must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK(seq>0 )','Sequence must be grater than zero'),
    ]
product_insure()

# class product_gridle_thick(osv.osv):
#     _name = 'product.gridle_thick'
#     _columns = {
#                 'name' : fields.char('Girdle Thick', size=512),
#                 'seq' : fields.integer('Sequence'),
#                 }
#     
#     _sql_constraints = [
#         ('name_unique', 'unique(name)', 'product Girdle Thick must be unique'),
#         ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
#         ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),        
#     ]
# product_gridle_thick()
# 
# class product_gridle_thin(osv.osv):
#     _name = 'product.gridle_thin'
#     _columns = {
#                 'name' : fields.char('Girdle Thin', size=512),
#                 'seq' : fields.integer('Sequence'),
#                 }
#     _sql_constraints = [
#         ('name_unique', 'unique(name)', 'product Girdle Thin must be unique'),
#         ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
#         ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
#     ]
# product_gridle_thin()

class product_lab(osv.osv):
    _name = 'product.lab'
    _columns = {
                'name' : fields.char('Lab', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product lab must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_lab()

class product_polish(osv.osv):
    _name = 'product.polish'
    _columns = {
                'name' : fields.char('Polish', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product polish must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_polish()

class product_shape(osv.osv):
    _name = 'product.shape'
    _columns = {
                'name' : fields.char('Shape', size=512),
                'seq' : fields.integer('Sequence'),
                }
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product shape must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_shape()

class product_symmetry(osv.osv):
    _name = 'product.symmetry'
    _columns = {
                'name' : fields.char('Symmetry', size=512),
                'seq' : fields.integer('Sequence'),
                }
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Product fluorescence intensity must be unique'),
        ('seq_unique', 'unique(seq)', 'Sequence must be unique'),
        ('check_seq','CHECK (seq>=0 )','Sequence must be grater than zero'),
    ]
product_symmetry()