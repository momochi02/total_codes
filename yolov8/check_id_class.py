import os

# Thư mục chứa các file .txt
folder_path = '/Users/game/Documents/image_train/new_folder/fornite/3_updating_fortnite'  # sửa đường dẫn tại đây

# Danh sách các id class hợp lệ
valid_classes = ['23']

# Duyệt qua từng file trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
            if first_line:  # đảm bảo dòng không rỗng
                class_id = first_line.split()[0]  # lấy id class ở đầu dòng
                if class_id not in valid_classes:
                    print(f"Invalid class ID in file: {filename} {class_id}")
            else:
                print(f"Empty file: {filename}")
