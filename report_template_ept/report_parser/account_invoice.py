import time
from openerp.report import report_sxw

class account_invoice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_invoice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_sr_no' : self._get_sr_no, 
            'get_total_weight':self._get_total_weight, 
        })
        self.sr_no = 0
    def _get_total_weight(self,obj):
        total_weight = 0.00
        for line in obj.order_line:
            total_weight += line.weight
        return total_weight
    def _get_sr_no(self):
        self.sr_no = self.sr_no + 1
        return self.sr_no 
    
report_sxw.report_sxw(
    'report.account.invoice.ept',
    'account.invoice',
    'addons/report_template_ept/template/account_print_invoice.rml',
    parser=account_invoice
)