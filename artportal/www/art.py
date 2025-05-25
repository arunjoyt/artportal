import frappe
from frappe.utils.file_manager import save_file
from frappe.utils import now

@frappe.whitelist(allow_guest=True)
def upload_image(image_data=None, filename=None, artist=None):
    
    if not image_data or not artist:
        frappe.throw("Image and Artist are required")

    # Decode base64 image and save
    from frappe.utils.file_manager import save_file
    import base64

    content = base64.b64decode(image_data)
    file_doc = save_file(filename, content, dt=None, dn=None, folder="Home", is_private=0)

    doc = frappe.get_doc({
        "doctype": "Artwork",
        "image": file_doc.file_url,
        "artist": artist
    })
    doc.insert(ignore_permissions=True)
    return doc

@frappe.whitelist(allow_guest=True)
def get_images():
    return frappe.get_all("Artwork", fields=["name", "image", "artist"], order_by="creation desc")

@frappe.whitelist(allow_guest=True)
def delete_image(name):
    frappe.delete_doc("Artwork", name, ignore_permissions=True)
    return "Deleted"