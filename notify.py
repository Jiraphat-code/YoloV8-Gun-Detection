import requests
def send_line_notify(image_path, confidences):
    line_notify_token = "Fill your notify token"
    
    # สร้างข้อความแจ้งเตือน
    confidence_str = ", ".join([f"{conf*100:.2f}%" for conf in confidences])
    message = f"Weapon detected with confidence: {confidence_str}\nAddress : ร้านทองป้าแช่ม ซอย4"
    
    # ส่งข้อมูลไปยัง LINE Notify
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {line_notify_token}"
    }

    payload = {
        "message": message,
    }

    files = {
        "imageFile": (image_path, open(image_path, "rb"), "image/jpeg")
    }

    response = requests.post(url, headers=headers, data=payload, files=files)

    if response.status_code == 200:
        print("LINE Notify sent successfully")
    else:
        print("Error sending LINE Notify:", response.status_code)