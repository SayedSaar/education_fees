from __future__ import unicode_literals
import frappe
from frappe import throw, _

def get_context(context):
	context.read_only = 1

def get_list_context(context):
	context.row_template = 'education_fees/templates/includes/fee/fee_row.html'
	context.get_list = get_fee_list
	#frappe.throw(str(context))
	return context


def get_fee_list(doctype, txt, filters, limit_start, limit_page_length = 20, order_by = None):
	fees = frappe.db.sql("""
		SELECT *
		FROM `tabFees` fee
		WHERE fee.student in (select sg.parent as studentname
		from `tabStudent Guardian` sg
		LEFT JOIN `tabGuardian` g on g.name = sg.guardian
		where g.user = %s)
		""", frappe.session.user, as_dict=True)
	
	return fees

def has_website_permission(doc, ptype, user, verbose=False):
	return True
