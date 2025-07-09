import os

# 📁 Thư mục chứa ảnh và nhãn
folder = "/Users/game/Documents/image_train/data_collect/0_begin"  # Đặt tên thư mục của bạn tại đây

# 🔍 Danh sách từ khóa cần xóa
keywords = ["light_green_darker_light_purple", "darker_brighter", "_darker_light_blue"]

# 🗑️ Duyệt và xóa nếu tên file chứa bất kỳ từ khóa nào
for file in os.listdir(folder):
    if any(keyword in file for keyword in keywords):
        file_path = os.path.join(folder, file)
        os.remove(file_path)
        print(f"🗑️ Đã xóa: {file}")
