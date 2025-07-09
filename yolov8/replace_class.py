import os

# Mapping class cũ → class mới
class_mapping = {
    3: 23,
    # 1: 12,
    # 2: 13
    # thêm mapping nếu cần
}

# Đường dẫn đến thư mục chứa các file .txt
labels_folder = "/Users/game/Documents/image_train/new_folder/fornite/3_updating_fortnite"  # ví dụ: "dataset/labels/train"

def replace_classes_in_txt(folder, mapping):
    for filename in os.listdir(folder):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(folder, filename)

        with open(file_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            class_id = int(parts[0])
            if class_id in mapping:
                parts[0] = str(mapping[class_id])
            new_lines.append(" ".join(parts))

        # Ghi đè lại file
        with open(file_path, "w") as f:
            f.write("\n".join(new_lines) + "\n")

        print(f"✅ Đã xử lý: {filename}")

# Chạy
replace_classes_in_txt(labels_folder, class_mapping)
