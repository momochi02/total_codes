import os
import shutil

# Cấu hình đường dẫn
folder = "/Users/game/Documents/image_train/new_folder/genshin/11_12_13_select_server_genshin"  # VD: "dataset/train"
invalid_img_dir = os.path.join('/Users/game/Documents/image_train/new_folder', "invalid_txt")
invalid_txt_dir = os.path.join('/Users/game/Documents/image_train/new_folder', "invalid_img")

# Tạo thư mục lưu file không khớp (nếu chưa có)

os.makedirs(invalid_img_dir, exist_ok=True)
os.makedirs(invalid_txt_dir, exist_ok=True)

# Tạo danh sách file theo tên (bỏ đuôi)
jpg_files = {os.path.splitext(f)[0] for f in os.listdir(folder) if f.endswith(".jpg")}
txt_files = {os.path.splitext(f)[0] for f in os.listdir(folder) if f.endswith(".txt")}

# Ảnh không có nhãn
img_only = jpg_files - txt_files
# Nhãn không có ảnh
txt_only = txt_files - jpg_files

# Di chuyển ảnh không có nhãn
for name in img_only:
    src = os.path.join(folder, name + ".jpg")
    dst = os.path.join(invalid_img_dir, name + ".jpg")
    shutil.move(src, dst)
    print(f"📷 Di chuyển ảnh thiếu nhãn: {name}.jpg")

# Di chuyển nhãn không có ảnh
for name in txt_only:
    src = os.path.join(folder, name + ".txt")
    dst = os.path.join(invalid_txt_dir, name + ".txt")
    shutil.move(src, dst)
    print(f"📝 Di chuyển nhãn thiếu ảnh: {name}.txt")