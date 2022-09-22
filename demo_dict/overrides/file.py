from frappe.core.doctype.file.file import File as FrappeFile
from frappe.core.doctype.file.utils import update_existing_file_docs
import frappe
from frappe.utils import cint, encode
import os
import shutil
import zipfile
from pathlib import Path
from frappe import _
from typing import List
from demo_dict.api import create_new_folder

class File(FrappeFile):
	def save_file_on_filesystem(self):
		folder_ = frappe.get_doc("File", self.folder)
		if not (folder_.is_home_folder and  folder_.is_attachments_folder):
			self.file_url =  f"/{folder_.file_url}/{self.file_name}"
			if self.is_private:
				self.file_url =  f"/private{self.file_url}"
		else:
			if self.is_private:
				self.file_url = f"/private/files/{self.file_name}"
			else:
				self.file_url = f"/files/{self.file_name}"

		fpath = self.write_file()

		return {"file_name": os.path.basename(fpath), "file_url": self.file_url}
	
	def handle_is_private_changed(self):
		if self.is_remote_file:
			return

		old_file_url = self.file_url
		file_name = self.file_url.split("/")[-1]
		folder_ = frappe.get_doc("File", self.folder)
		if not (folder_.is_home_folder and  folder_.is_attachments_folder):
			public_file_path_ =  f"/{folder_.file_url}/{file_name}"
			private_file_path = Path(f"{frappe.local.site_path}/private{public_file_path_}")
			public_file_path = Path(f"{frappe.local.site_path}/public{public_file_path_}")

			if cint(self.is_private):
				source = public_file_path
				target = private_file_path
				updated_file_url = f"/private{public_file_path_}"
			else:
				source = private_file_path
				target = public_file_path
				updated_file_url = public_file_path_
	
		else:
			private_file_path = Path(frappe.get_site_path("private", "files", file_name))
			public_file_path = Path(frappe.get_site_path("public", "files", file_name))

			if cint(self.is_private):
				source = public_file_path
				target = private_file_path
				url_starts_with = "/private/files/"
			else:
				source = private_file_path
				target = public_file_path
				url_starts_with = "/files/"
			updated_file_url = f"{url_starts_with}{file_name}"

		# if a file document is created by passing dict throught get_doc and __local is not set,
		# handle_is_private_changed would be executed; we're checking if updated_file_url is same
		# as old_file_url to avoid a FileNotFoundError for this case.
		if updated_file_url == old_file_url:
			return

		if not source.exists():
			frappe.throw(
				_("Cannot find file {} on disk").format(source),
				exc=FileNotFoundError,
			)
		if target.exists():
			frappe.throw(
				_("A file with same name {} already exists").format(target),
				exc=FileExistsError,
			)

		# Uses os.rename which is an atomic operation
		shutil.move(source, target)
		self.flags.original_path = {"old": source, "new": target}
		frappe.local.rollback_observers.append(self)

		self.file_url = updated_file_url
		update_existing_file_docs(self)

		if (
			not self.attached_to_doctype
			or not self.attached_to_name
			or not self.fetch_attached_to_field(old_file_url)
		):
			return

		frappe.db.set_value(
			self.attached_to_doctype,
			self.attached_to_name,
			self.attached_to_field,
			self.file_url,
		)
	
	def on_trash(self):
		if self.is_home_folder or self.is_attachments_folder:
			frappe.throw(_("Cannot delete Home and Attachments folders"))
		if self.is_folder:
			files = frappe.get_all("File", filters={"folder": self.name}, pluck="name")
			for file in files:
				file = frappe.get_doc("File", file)
				if not file.is_private:
					file.file_url = f"/public{file.file_url}"
				frappe.delete_doc("File", file.name)
				delete_file(file.file_url)

			public_file_path_ =  f"/{self.file_url}"
			private_file_path = Path(f"{frappe.local.site_path}/private{public_file_path_}")
			public_file_path = Path(f"{frappe.local.site_path}/public{public_file_path_}")
			os.rmdir(private_file_path)
			os.rmdir(public_file_path)
		elif self.file_url.endswith(".zip"):
			file_url = self.file_url
			if not self.is_private:
				file_url = f"/public{file_url}"
			path = Path(f"{frappe.local.site_path}{file_url}")
			if path.is_file():
				os.remove(path)

		else:
			self._delete_file_on_disk()
			if not self.is_folder:
				self.add_comment_in_reference_doc("Attachment Removed", _("Removed {0}").format(self.file_name))

	def unzip(self) -> List["File"]:
		"""Unzip current file and replace it by its children"""
		if not self.file_url.endswith(".zip"):
			frappe.throw(_("{0} is not a zip file").format(self.file_name))

		zip_path = self.get_full_path()
		folder_ = frappe.get_doc("File", self.folder)
		if folder_.is_home_folder or  folder_.is_attachments_folder:
			FrappeFile.unzip(self)
			return

		file_url = self.file_url if self.is_private else f"/public{file_url}"
		file_url = "/".join(f"{frappe.local.site_path}{file_url}".split("/")[:-1])

		with zipfile.ZipFile(zip_path) as z:
			z.extractall(Path(file_url))
			create_file_docs(self.folder, self.is_private)
			frappe.delete_doc("File", self.name)
	
def create_file_docs(folder, is_private):
	folder_ = frappe.get_doc("File", folder)
	folder_url = f"/private/{folder_.file_url}" if is_private else f"/public/{folder_.file_url}"
	folder_url = f"{frappe.local.site_path}{folder_url}"
	for i in os.listdir(folder_url):
		if os.path.isfile(f"{folder_url}/{i}"):
			file_url = folder_.file_url
			if is_private:
				file_url = f"/private/{file_url}/{i}"
			
			if not file_url.endswith(".zip"):
				file_doc = frappe.get_doc(
					{
						"doctype": "File",
						"folder": folder,
						"file_name": i,
						"file_url": file_url,
						"is_private": cint(is_private),
					}
				).insert(ignore_permissions=1)
		elif os.path.isdir(f"{folder_url}/{i}"):
			new_folder = create_new_folder(i, folder)
			create_file_docs(new_folder.name, is_private)

	
def delete_file(path):
	if path:
		if ".." in path.split("/"):
			frappe.throw(
				_("It is risky to delete this file: {0}. Please contact your System Manager.").format(path)
			)
		path = f"{frappe.local.site_path}{path}"

		path = encode(path)
		if os.path.exists(path):
			os.remove(path)