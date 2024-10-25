from scripts.label_approved import label_approved

def test_label_approved_approved():
    result = label_approved("approved")
    assert result == "Label is approved"

def test_label_approved_pending():
    result = label_approved("pending")
    assert result == "Label is pending"

def test_label_approved_rejected():
    result = label_approved("rejected")
    assert result == "Label is not approved"

def test_label_approved_empty():
    result = label_approved("")
    assert result == "Label is not approved"
