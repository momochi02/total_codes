import cv2
import os
import shutil
import numpy as np
from PIL import Image

AUGMENTATIONS = {
    'brighter': lambda img: cv2.convertScaleAbs(img, alpha=0.7, beta=20),
    'darker': lambda img: cv2.convertScaleAbs(img, alpha=0.8, beta=-20),
    'light_blue': lambda img: blend_tint(img, (255, 200, 200), alpha=0.2),
    'light_green': lambda img: blend_tint(img, (200, 255, 200), alpha=0.2),
    'light_purple': lambda img: blend_tint(img, (220, 200, 255), alpha=0.2),
}

# 📁 Cấu hình thư mục
image_dir = "/Users/game/Documents/image_train/data_collect/17_select_sever"   # chứa ảnh gốc
label_dir = "/Users/game/Documents/image_train/data_collect/17_select_sever"   # chứa file .txt nhãn gốc
output_img_dir = "/Users/game/Documents/image_train/data_collect/17_select_sever"
output_lbl_dir = "/Users/game/Documents/image_train/data_collect/17_select_sever"

os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_lbl_dir, exist_ok=True)
os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_lbl_dir, exist_ok=True)

def blend_tint(image, color, alpha=0.2):
    overlay = np.full_like(image, color)
    return cv2.addWeighted(image, 1 - alpha, overlay, alpha, 0)

def augment_image(image_path):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    image = cv2.imread(image_path)
    if image is None:
        print(f"⚠️ Không đọc được ảnh: {image_path}")
        return

    label_path = os.path.join(label_dir, f"{base_name}.txt")
    if not os.path.exists(label_path):
        print(f"⚠️ Không tìm thấy file label: {label_path}")
        return

    for aug_name, func in AUGMENTATIONS.items():
        augmented = func(image)
        new_img_name = f"{base_name}_{aug_name}.png"
        new_lbl_name = f"{base_name}_{aug_name}.txt"

        out_img_path = os.path.join(output_img_dir, new_img_name)
        out_lbl_path = os.path.join(output_lbl_dir, new_lbl_name)

        # Lưu ảnh mới
        cv2.imwrite(out_img_path, augmented)

        # Copy nhãn
        shutil.copy(label_path, out_lbl_path)

        print(f"✅ Tạo: {new_img_name} & {new_lbl_name}")

# 🔁 Duyệt toàn bộ ảnh
for file in os.listdir(image_dir):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        augment_image(os.path.join(image_dir, file))