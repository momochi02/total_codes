import os

# 📁 Thư mục gốc chứa ảnh và label
folder = "/Users/game/Documents/image_train/data_collect/17_select_sever"
new_base_name = "select_game_resource_confirm_button"  # Tên bạn muốn đặt cho ảnh mới

# Lấy danh sách ảnh (có phần mở rộng)
image_files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

# Đổi tên từng ảnh và file .txt tương ứng
for idx, img_file in enumerate(image_files, 1):
    name, ext = os.path.splitext(img_file)
    new_img_name = f"{new_base_name}_{idx}{ext}"
    old_img_path = os.path.join(folder, img_file)
    new_img_path = os.path.join(folder, new_img_name)

    # Đổi tên ảnh
    os.rename(old_img_path, new_img_path)

    # Đổi tên file .txt tương ứng (nếu có)
    old_txt_path = os.path.join(folder, f"{name}.txt")
    new_txt_path = os.path.join(folder, f"{new_base_name}_{idx}.txt")
    if os.path.exists(old_txt_path):
        os.rename(old_txt_path, new_txt_path)
        print(f"✅ Đã đổi: {img_file} + {name}.txt → {new_img_name} + {new_base_name}_{idx}.txt")
    else:
        print(f"⚠️ Không tìm thấy file nhãn cho: {img_file}")
