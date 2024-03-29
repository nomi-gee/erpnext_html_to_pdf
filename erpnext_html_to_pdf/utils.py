import frappe
import base64
import requests
from frappe.www.printview import validate_print_permission
from frappe.translate import print_language
from erpnext_html_to_pdf.pdf import generate_pdf, generate_pdf_from_template, generate_pdf_from_html
import asyncio
from frappe.utils import get_url
from frappe.utils.pdf import read_options_from_html
from bs4 import BeautifulSoup


def image_to_base64(image_url):
	try:
		# Fetch the image data from the URL
		response = requests.get(image_url)
		# Encode the image to base64
		base64_image = "data:image/jpeg;base64,{0}".format(base64.b64encode(response.content).decode('utf-8'))
		return base64_image
	except Exception as e:
		print("Error:", e)
	return None

def jinja_methods():
	return ["erpnext_html_to_pdf.utils.image_to_base64"]



@frappe.whitelist(allow_guest=True)
def generate_pdf(doctype, name, format=None, doc=None, no_letterhead=0, language=None, letterhead=None):
	doc = doc or frappe.get_doc(doctype, name)
	validate_print_permission(doc)

	with print_language(language):
		html = frappe.get_print(
			doctype, name, format, doc=doc, as_pdf=False, letterhead=letterhead, no_letterhead=no_letterhead
		)

	soup = BeautifulSoup(html, "html5lib")

	for tag in soup.find_all(attrs={"class": "visible-pdf"}):
		# remove visible-pdf class to unhide
		tag.attrs["class"].remove("visible-pdf")

	for tag in soup.find_all(attrs={"class": "hidden-pdf"}):
		# remove tag from html
		tag.extract()

	for tag in soup.find_all(attrs={"class": "action-banner"}):
		# remove tag from html
		tag.extract()

	stylesheet_links = soup.find_all('link', rel='stylesheet')

	for link in stylesheet_links:
		stylesheet_url = link['href']
		response = requests.get("{0}/{1}".format(get_url(),stylesheet_url))
		if response.status_code == 200:
			styles = response.text
			style_tag = soup.new_tag('style')
			style_tag.append(styles)
			soup.head.append(style_tag)
			link.extract()

	html = str(soup.prettify())

	filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
	output_filename = "{0}/{1}".format(frappe.utils.get_files_path(), filename)
	
	pdf = generate_pdf_from_html(html, output_filename)

	frappe.local.response.filename = filename
	frappe.local.response.filecontent = pdf
	frappe.local.response.type = "pdf"

	# return "{1}/files/{0}".format(filename, get_url())