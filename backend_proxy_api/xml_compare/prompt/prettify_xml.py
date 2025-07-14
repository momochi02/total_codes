from lxml import etree

def prettify_xml_1(input_path, output_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(input_path, parser)

    # Ghi ra file với pretty print
    tree.write(output_path, pretty_print=True, encoding="utf-8", xml_declaration=True)

    print(f"✅ Đã lưu file XML đã format vào: {output_path}")


import xml.etree.ElementTree as ET
import xml.dom.minidom

def prettify_xml(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Chuyển tree sang string
    rough_string = ET.tostring(root, encoding='utf-8')

    # Format bằng minidom
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Xoá dòng trắng
    pretty_xml = "\n".join([line for line in pretty_xml.split('\n') if line.strip() != ""])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print(f"✅ Đã lưu file XML đã format vào: {output_path}")

# ▶ Thay đường dẫn tại đây:
input_xml_path = '/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml'
output_xml_path = '/backend_proxy_api/xml_compare/xml_file/window_dump_3.xml'

prettify_xml_1(input_xml_path, output_xml_path)
