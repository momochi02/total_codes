import time
import xml.etree.ElementTree as ET
import json
import re
from collections import defaultdict
from http.client import HTTPException

def parse_bounds(bounds_str):
    match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
    if match:
        return tuple(map(int, match.groups()))
    return None

def get_node_path(node, parent_path=''):
    cls = node.attrib.get('class', 'UnknownClass')
    idx = node.attrib.get('index', '0')
    current = f"{parent_path}/{cls}[{idx}]"
    return current

def flatten_tree(root):
    result = []

    def recurse(node, path):
        current_path = get_node_path(node, path)
        raw_bounds = node.attrib.get('bounds', '')
        bounds = parse_bounds(raw_bounds)

        result.append({
            'path': current_path,
            'bounds': bounds,
            'class': node.attrib.get('class', ''),
            'focusable': node.attrib.get('focusable', ''),
            'clickable': node.attrib.get('clickable', ''),
            'enabled': node.attrib.get('enabled', ''),
            'text': node.attrib.get('text', ''),
            'resource-id': node.attrib.get('resource-id', ''),
            'visible': node.attrib.get('visible-to-user', 'true'),
        })

        for child in node:
            recurse(child, current_path)

    recurse(root, '')
    return result

def bounds_difference(b1, b2):
    if not b1 and not b2:
        return False
    if not b1 or not b2:
        return True
    diff_threshold = 0.02
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
    w_diff = abs(w1 - w2) / max(w1, w2)
    h_diff = abs(h1 - h2) / max(h1, h2)
    return w_diff > diff_threshold or h_diff > diff_threshold

def compare_nodes(t_nodes, p_nodes):
    discrepancies = defaultdict(list)
    tablet_map = {node['path']: node for node in t_nodes}
    phone_map = {node['path']: node for node in p_nodes}
    all_paths = set(tablet_map.keys()) | set(phone_map.keys())

    for path in all_paths:
        t_node = tablet_map.get(path)
        p_node = phone_map.get(path)

        if not t_node:
            discrepancies['critical'].append({
                'title': 'Missing Node on Tablet',
                'description': [f"Node {path} exists on Phone but missing on Tablet."],
                'path': [path]
            })
        elif not p_node:
            discrepancies['critical'].append({
                'title': 'Missing Node on Phone',
                'description': [f"Node {path} exists on Tablet but missing on Phone."],
                'path': [path]
            })
        else:
            if bounds_difference(t_node['bounds'], p_node['bounds']):
                discrepancies['major'].append({
                    'title': 'Bounds Mismatch',
                    'description': [
                        f"Tablet bounds: {t_node['bounds']}",
                        f"Phone bounds: {p_node['bounds']}"
                    ],
                    'path': [path]
                })

            for attr in ['class', 'focusable', 'clickable', 'enabled', 'visible']:
                if t_node[attr] != p_node[attr]:
                    discrepancies['minor'].append({
                        'title': f"{attr.capitalize()} Mismatch",
                        'description': [
                            f"Tablet: {t_node[attr]}",
                            f"Phone: {p_node[attr]}"
                        ],
                        'path': [path]
                    })
    return discrepancies

def generate_conclusion(discrepancies):
    if discrepancies['critical']:
        return "Validation FAILED due to missing critical UI elements."
    elif discrepancies['major']:
        return "Validation FAILED due to structural or bounds mismatches."
    elif discrepancies['minor']:
        return "Validation PASSED with minor discrepancies that don’t affect core structure."
    else:
        return "Validation PASSED. No discrepancies found."

# Hàm mới để gọi từ API: nhận 2 chuỗi XML rồi so sánh trả về dict JSON
def compare_xml_lgcode(tablet_xml_str, phone_xml_str):
    print("Tablet XML snippet: >>>", repr(tablet_xml_str[:300]), "<<<")
    print("Phone XML snippet: >>>", repr(phone_xml_str[:300]), "<<<")

    try:
        t_root = ET.fromstring(tablet_xml_str)
        p_root = ET.fromstring(phone_xml_str)
    except Exception as e:
        return {"error": f"XML parse error: {str(e)}"}

    t_nodes = flatten_tree(t_root)
    p_nodes = flatten_tree(p_root)

    discrepancies = compare_nodes(t_nodes, p_nodes)
    time.sleep(10)
    result = {
        "Overall_Validation_Result": "FAIL" if discrepancies['critical'] or discrepancies['major'] else "PASS",
        "Discrepancy Log": discrepancies,
        "conclusion": generate_conclusion(discrepancies)
    }
    #
    # result = {
    #     "Overall_Validation_Result": "FAIL" ,
    #     "Discrepancy Log": "discrepancies",
    #     "conclusion": "1",
    #     "status" : 200
    # }
    return result


# Giữ lại hàm main để chạy thử local (bạn có thể gọi file path bình thường)
def main(tablet_path, phone_path, output_path='validation_result.json'):
    print("🛠️ Đang chạy compare_xml_with_prompt...")
    # with open(tablet_path, encoding='utf-8') as f:
    #     tablet_xml_str = f.read()
    # with open(phone_path, encoding='utf-8') as f:
    #     phone_xml_str = f.read()


    tablet_xml = open(tablet_path, 'rb')
    phone_xml = open(phone_path, 'rb')

    try:
        tablet_xml_str = ( tablet_xml.read()).decode("utf-8")
        phone_xml_str = ( phone_xml.read()).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded files: {str(e)}")


    print("Tablet XML snippet: >>>", repr(tablet_xml_str[:300]), "<<<")
    print("Phone XML snippet: >>>", repr(phone_xml_str[:300]), "<<<")
    result = compare_xml_lgcode(tablet_xml_str, phone_xml_str)

    print("\n=== ✅ KẾT QUẢ SO SÁNH XML ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Kết quả đã được xuất ra: {output_path}")


# if __name__ == "__main__":
#     tablet_xml_path = "/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml"
#     phone_xml_path = "/backend_proxy_api/xml_compare/xml_file/window_dump_3.xml"
#     main(tablet_xml_path, phone_xml_path)
