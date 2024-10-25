def label_approved(status):
    if status == "approved":
        return "Label is approved"
    elif status == "pending":
        return "Label is pending"
    else:
        return "Label is not approved"

