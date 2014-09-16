import time
from openerp.report import report_sxw

class product_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(product_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
        })
        
report_sxw.report_sxw('report.sale_test_report', 
                      'sale.order', 
                      'product_test/report/sale_test_report.rml', 
                      parser=product_report, 
                      header="external")

report_sxw.report_sxw('report.new_sale_report', 
                      'sale.order', 
                      'product_test/report/new_sale_report.rml', 
                      parser=product_report, 
                      header="external")

report_sxw.report_sxw('report.test', 
                      'sale.order',
                      'product_test/report/test.rml', 
                      parser=product_report, 
                      header="external")