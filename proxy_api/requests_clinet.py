import requests

def call_compare_api_gauss(tablet_xml_path, phone_xml_path):
    url = "http://127.0.0.1:8000/compare_xml_by_gauss"
    headers = {
        "x-api-key": "key_pc1"  # Không cần Content-Type nếu dùng `files`
    }

    # Mở file ở dạng nhị phân để gửi
    files = {
        'tablet_xml': open(tablet_xml_path, 'rb'),
        'phone_xml': open(phone_xml_path, 'rb')
    }

    try:
        response = requests.post(url, headers=headers, files=files)
    finally:
        # Đóng file sau khi gửi (tránh leak file descriptor)
        for f in files.values():
            f.close()

    if response.status_code == 200:
        print("✅ Kết quả:")
        try:
            print("Dạng JSON:", response.json())
        except Exception as e:
            print("❌ Lỗi khi parse JSON:", e)
            print("Text trả về:", response.text)
    else:
        print("❌ Gặp lỗi:", response.status_code)
        print(response.text)

phone_xml_path ="/Users/game/Desktop/chi/auto_app_update/xml_compare/xml_file/window_dump_1.xml"
tablet_xml_path="/Users/game/Desktop/chi/auto_app_update/xml_compare/xml_file/window_dump_1.xml"
call_compare_api_gauss(tablet_xml_path, phone_xml_path)