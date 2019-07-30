from __future__ import unicode_literals
import frappe
from frappe import throw, _

def get_context(context):
	context.read_only = 0

def get_list_context(context):
	context.row_template = 'education_fees/templates/includes/student_row_template.html'
	context.get_list = get_student_list
	#frappe.throw(str(context))
	return context


def get_student_list(doctype, txt, filters, limit_start, limit_page_length = 20, order_by = None):
	students = frappe.db.sql("""
		SELECT *
		FROM `tabStudent` student
		WHERE student.name in (select sg.parent as studentname
		from `tabStudent Guardian` sg
		LEFT JOIN `tabGuardian` g on g.name = sg.guardian
		where g.user = %s)
		""", frappe.session.user, as_dict=True)
	
	return students

def has_website_permission(doc, ptype, user, verbose=False):
	students = frappe.db.sql("""
		SELECT *
		FROM `tabStudent` student
		WHERE student.name in (select sg.parent as studentname
		from `tabStudent Guardian` sg
		LEFT JOIN `tabGuardian` g on g.name = sg.guardian
		where g.user = %s)
		AND student.name = '{student_name}'
		""".format(student_name=doc.name), frappe.session.user, as_dict=True)

	if students:
		return True
	else:
		return False
