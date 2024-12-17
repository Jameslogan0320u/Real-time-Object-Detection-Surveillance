import time

def check_alert_condition(detected_ids, classes_of_interest, last_alert_time, cooldown):
    if any(cls in classes_of_interest for cls in detected_ids) and time.time() - last_alert_time > cooldown:
        return True, time.time()
    return False, last_alert_time
