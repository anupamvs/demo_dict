import frappe
from frappe.utils import cint
import os
from mimetypes import guess_type

@frappe.whitelist()
def create_new_folder(file_name: str, folder: str):
	"""create new folder under current parent folder"""
	try:
		folder_ = frappe.get_doc("File", folder)
		if not (folder_.is_home_folder and  folder_.is_attachments_folder):
			file_url = "/".join(folder_.file_url.split("/")[1:])
			path = os.path.join(frappe.get_site_path('public', 'files'), file_url, file_name)
			private_path = os.path.join(frappe.get_site_path('private', 'files'), file_url, file_name)

		file = frappe.new_doc("File")
		file.file_name = file_name
		file.is_folder = 1
		file.folder = folder
		file.file_url = "/".join(path.split("/")[3:])
		file.insert(ignore_if_duplicate=True)

		folder_path = frappe.db.get_value("File", "Attachments")
		if not os.path.exists(path):
			os.mkdir(path)
		if not os.path.exists(private_path):
			os.mkdir(private_path)
	
	except Exception as err:
		frappe.throw(err)
		frappe.log_error()

	return file