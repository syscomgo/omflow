def status_format(status_id=None):
    if status_id == "1":
        final_status = "開發前審核"
    elif status_id == "3":
        final_status = "上線前審核"
    elif status_id == "6":
        final_status = "結案審核"
    else:
        final_status = "None"
    return final_status
status_display = status_format(change_status_id)