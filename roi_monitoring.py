def define_roi(frame):
    roi_x, roi_y, roi_w, roi_h = 100, 100, 400, 400
    roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    return roi, (roi_x, roi_y, roi_w, roi_h)

def draw_roi(frame, roi_coords):
    roi_x, roi_y, roi_w, roi_h = roi_coords
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
