# -*- coding: utf-8 -*-
import logging
import time

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

class pos_order_line(osv.osv):
	_inherit = "pos.order.line"

	def _check_orderline_stock(self, cr, uid, ids, context=None):
		inventory_obj = self.pool.get('stock.inventory.report')
		for obj in self.browse(cr,uid,ids,context=context):
			inventory_ids = inventory_obj.search(cr,uid,[('product_id','=',obj.product_id.id),\
				('location_id','=',obj.order_id.session_id.config_id.stock_location_id.id)])
			if not inventory_ids:
				return False
			else:
				tot_stock = 0
				for inventory in inventory_obj.browse(cr,uid,inventory_ids):	
					tot_stock += inventory.qty
				if obj.qty > tot_stock:
					return False
		return True

	_constraints = [
        	(_check_orderline_stock, 'Not enough stock for selected item.', ['product_id']),
		]


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
