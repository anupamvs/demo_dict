from . import __version__ as app_version

app_name = "demo_dict"
app_title = "Demo Dict"
app_publisher = "anupamvs"
app_description = "Demo Dict"
app_email = "hello@anupamvs.dev"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/demo_dict/css/demo_dict.css"
# app_include_js = "/assets/demo_dict/js/demo_dict.js"

# include js, css files in header of web template
# web_include_css = "/assets/demo_dict/css/demo_dict.css"
# web_include_js = "/assets/demo_dict/js/demo_dict.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "demo_dict/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "demo_dict.utils.jinja_methods",
# 	"filters": "demo_dict.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "demo_dict.install.before_install"
# after_install = "demo_dict.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "demo_dict.uninstall.before_uninstall"
# after_uninstall = "demo_dict.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "demo_dict.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"File": "demo_dict.overrides.file.File"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"demo_dict.tasks.all"
# 	],
# 	"daily": [
# 		"demo_dict.tasks.daily"
# 	],
# 	"hourly": [
# 		"demo_dict.tasks.hourly"
# 	],
# 	"weekly": [
# 		"demo_dict.tasks.weekly"
# 	],
# 	"monthly": [
# 		"demo_dict.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "demo_dict.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"frappe.core.api.file.create_new_folder": "demo_dict.api.create_new_folder"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "demo_dict.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"demo_dict.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
