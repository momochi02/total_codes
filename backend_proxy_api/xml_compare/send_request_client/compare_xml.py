# import xml.etree.ElementTree as ET
# from collections import Counter
# def get_nodes(xml_path):
#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#
#     nodes = []
#     for node in root.iter('node'):
#         info = {
#             'text': node.attrib.get('text', ''),
#             'bounds': node.attrib.get('bounds', ''),
#             'resource-id': node.attrib.get('resource-id', ''),
#             'class': node.attrib.get('class', ''),
#         }
#         nodes.append(info)
#     return nodes
#
# def compare_xml_combined(file1, file2, prompt=""):
#     nodes1 = get_nodes(file1)
#     nodes2 = get_nodes(file2)
#
#     len1 = len(nodes1)
#     len2 = len(nodes2)
#
#     print(f"\n🔍 Tổng node:")
#     print(f"📄 File 1: {len1} node")
#     print(f"📄 File 2: {len2} node")
#
#     # 1. So sánh theo thứ tự từng dòng
#     max_len = max(len1, len2)
#     diffs = []
#
#     for i in range(max_len):
#         n1 = nodes1[i] if i < len1 else None
#         n2 = nodes2[i] if i < len2 else None
#
#         if n1 != n2:
#             diffs.append((i + 1, n1, n2))  # +1 cho dễ đọc
#
#     if not diffs:
#         print("\n✅ Hai file XML giống nhau hoàn toàn.")
#     else:
#         print(f"\n❌ Phát hiện {len(diffs)} điểm khác biệt theo dòng:")
#
#         for idx, n1, n2 in diffs:
#             print(f"\n🔹 Khác biệt tại dòng node {idx}:")
#             print("📄 File 1:", n1 if n1 else "Không có (node mới)")
#             print("📄 File 2:", n2 if n2 else "Không có (node đã bị xoá)")
#
#     # 2. So sánh không theo thứ tự (để kiểm tra thiếu/thừa node thật)
#     counter1 = Counter(tuple(sorted(n.items())) for n in nodes1)
#     counter2 = Counter(tuple(sorted(n.items())) for n in nodes2)
#
#     only_in_1 = counter1 - counter2
#     only_in_2 = counter2 - counter1
#
#     if only_in_1 or only_in_2:
#         print("\n📌 Phân tích thêm – Node bị thêm hoặc bị xoá (không theo thứ tự):")
#
#         if only_in_1:
#             print("\n🔻 Node có trong file 1 nhưng không có trong file 2 (bị xoá?):")
#             for node, count in only_in_1.items():
#                 print(f"{dict(node)} × {count}")
#
#         if only_in_2:
#             print("\n🟢 Node có trong file 2 nhưng không có trong file 1 (mới thêm?):")
#             for node, count in only_in_2.items():
#                 print(f"{dict(node)} × {count}")
#     else:
#         print("\n✅ Không phát hiện node bị thêm/xoá.")
#
# # 🧪 Thử nghiệm với 2 file XML
# # 🔽 Thay bằng đường dẫn tới 2 file XML cần so sánh
# file1 = ('/Users/game/Desktop/chi/auto_app_update/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml')
# file2 =  ('/Users/game/Desktop/chi/auto_app_update/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml')
# prompt =''
# compare_xml_combined(file1, file2,prompt)
#
#
#
#
# import xml.etree.ElementTree as ET
# from collections import Counter
# def get_nodes(xml_path):
#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#
#     nodes = []
#     for node in root.iter('node'):
#         info = {
#             'text': node.attrib.get('text', ''),
#             'bounds': node.attrib.get('bounds', ''),
#             'resource-id': node.attrib.get('resource-id', ''),
#             'class': node.attrib.get('class', ''),
#         }
#         nodes.append(info)
#     return nodes
#
# def compare_xml_combined(file1, file2, prompt=""):
#     nodes1 = get_nodes(file1)
#     nodes2 = get_nodes(file2)
#
#     len1 = len(nodes1)
#     len2 = len(nodes2)
#
#     print(f"\n🔍 Tổng node:")
#     print(f"📄 File 1: {len1} node")
#     print(f"📄 File 2: {len2} node")
#
#     # 1. So sánh theo thứ tự từng dòng
#     max_len = max(len1, len2)
#     diffs = []
#
#     for i in range(max_len):
#         n1 = nodes1[i] if i < len1 else None
#         n2 = nodes2[i] if i < len2 else None
#
#         if n1 != n2:
#             diffs.append((i + 1, n1, n2))  # +1 cho dễ đọc
#
#     if not diffs:
#         print("\n✅ Hai file XML giống nhau hoàn toàn.")
#     else:
#         print(f"\n❌ Phát hiện {len(diffs)} điểm khác biệt theo dòng:")
#
#         for idx, n1, n2 in diffs:
#             print(f"\n🔹 Khác biệt tại dòng node {idx}:")
#             print("📄 File 1:", n1 if n1 else "Không có (node mới)")
#             print("📄 File 2:", n2 if n2 else "Không có (node đã bị xoá)")
#
#     # 2. So sánh không theo thứ tự (để kiểm tra thiếu/thừa node thật)
#     counter1 = Counter(tuple(sorted(n.items())) for n in nodes1)
#     counter2 = Counter(tuple(sorted(n.items())) for n in nodes2)
#
#     only_in_1 = counter1 - counter2
#     only_in_2 = counter2 - counter1
#
#     if only_in_1 or only_in_2:
#         print("\n📌 Phân tích thêm – Node bị thêm hoặc bị xoá (không theo thứ tự):")
#
#         if only_in_1:
#             print("\n🔻 Node có trong file 1 nhưng không có trong file 2 (bị xoá?):")
#             for node, count in only_in_1.items():
#                 print(f"{dict(node)} × {count}")
#
#         if only_in_2:
#             print("\n🟢 Node có trong file 2 nhưng không có trong file 1 (mới thêm?):")
#             for node, count in only_in_2.items():
#                 print(f"{dict(node)} × {count}")
#     else:
#         print("\n✅ Không phát hiện node bị thêm/xoá.")
#
# # 🧪 Thử nghiệm với 2 file XML
# # 🔽 Thay bằng đường dẫn tới 2 file XML cần so sánh
# file1 = ('/Users/game/Desktop/chi/auto_app_update/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml')
# file2 =  ('/Users/game/Desktop/chi/auto_app_update/backend_proxy_api/xml_compare/xml_file/window_dump_1.xml')
# prompt =''
# compare_xml_combined(file1, file2,prompt)
#
#
#
#
