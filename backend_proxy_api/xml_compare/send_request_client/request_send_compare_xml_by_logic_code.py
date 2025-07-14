import requests
def call_compare_api(tablet_xml_path, phone_xml_path, api_url="http://localhost:8000/compare_xml_by_logic_code"):

    files = {
        'tablet_xml': open(tablet_xml_path, 'rb'),
        'phone_xml': open(phone_xml_path, 'rb')
    }

    try:
        response = requests.post(api_url, files=files)
        response.raise_for_status()  # nếu status != 200 thì raise lỗi
        return response.json()       # trả về dữ liệu JSON từ API
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        print(f"API call failed: {e}")
        print(f"Response content: {response.text}")
        return None
    finally:
        # Đóng file sau khi gửi request xong
        files['tablet_xml'].close()
        files['phone_xml'].close()

if __name__ == "__main__":
    tablet_path = "/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml"
    phone_path = "/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml"
    comparison_result = call_compare_api(tablet_path, phone_path)
    if comparison_result:
        import json
        print(json.dumps(comparison_result, indent=2, ensure_ascii=False))

