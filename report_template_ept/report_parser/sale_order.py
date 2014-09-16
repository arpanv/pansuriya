# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_sr_no' : self._get_sr_no,     
            'get_total_weight':self._get_total_weight,      
        })
        self.context = context 
        self.sr_no = 0
    
    def _get_total_weight(self,obj):
        total_weight = 0.00
        for line in obj.order_line:
            total_weight += line.th_weight
        return total_weight
    def _get_sr_no(self):
        self.sr_no = self.sr_no + 1
        return self.sr_no    
report_sxw.report_sxw('report.sale.order.ept', 'sale.order', 'addons/report_template_ept/template/Sale_quote_srk.rml', parser=order)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

