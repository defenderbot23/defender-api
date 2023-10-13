from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.Client()
admins_col = db.collection("admins")

def check_by_mail(mail: str):
	"""
	Checks if an admin with the given mail exists
	:param mail: The mail to check
	:return: The result of the check
	"""
	query = admins_col.where(filter=FieldFilter("mail", "==", mail))
	return {
		"status": "success",
		"result": len(list(query.stream())) > 0
	}


def get_admin_details(mail: str) -> dict:
	"""
	Gets the details of an admin
	:param mail: The mail of the admin
	:return: The details of the admin
	"""
	query = admins_col.where(filter=FieldFilter("mail", "==", mail))
	
	if len(list(query.stream())) == 0:
		return {
			"status": "error",
			"message": "Mail not found"
		}
	
	admin = list(query.stream())[0]
	
	return {
		"status": "success",
		"result": {
			"mail": admin.get("mail"),
			"phone": admin.get("phone"),
			"name": admin.get("name"),
		}
	}


def get_admin_group(mail: str) -> dict:
	"""
	Gets the group of an admin
	:param mail: The mail of the admin
	:return: The group of the admin
	"""
	query = admins_col.where(filter=FieldFilter("mail", "==", mail))
	
	if len(list(query.stream())) == 0:
		return {
			"status": "error",
			"message": "Mail not found"
		}
	
	admin = list(query.stream())[0]
	
	group_info = admin.get("grup_info")
	
	return {
		"status": "success",
		"response": {
			"grup_name": group_info.get("grup_name"),
			"grup_id": group_info.get("grup_id")
		}
	}