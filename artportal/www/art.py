import frappe
from frappe.utils.file_manager import save_file
import base64

@frappe.whitelist(allow_guest=True)
def get_images():
    # Allow everyone
    return frappe.get_all("Artwork", fields=["name", "image", "artist"], order_by="creation desc")


@frappe.whitelist()
def upload_image(image_data=None, filename=None, artist=None):
    if frappe.session.user == "Guest":
        frappe.throw("Login required to upload images.")

    if not image_data or not artist:
        frappe.throw("Missing image or artist")

    content = base64.b64decode(image_data)
    file_doc = save_file(filename, content, dt=None, dn=None, folder="Home", is_private=0)

    doc = frappe.get_doc({
        "doctype": "Artwork",
        "image": file_doc.file_url,
        "artist": artist
    })
    doc.insert()
    return doc


@frappe.whitelist()
def delete_image(name):
    if frappe.session.user == "Guest":
        frappe.throw("Login required to delete images.")

    frappe.delete_doc("Artwork", name)
    return "Deleted"