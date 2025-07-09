import os
import shutil

def move_orphan_labels(images_dir, labels_dir, removed_labels_dir, image_exts=(".jpg", ".png")):
    os.makedirs(removed_labels_dir, exist_ok=True)

    for label_file in os.listdir(labels_dir):
        if not label_file.endswith('.txt'):
            continue

        image_name = os.path.splitext(label_file)[0]
        image_exists = any(os.path.exists(os.path.join(images_dir, image_name + ext)) for ext in image_exts)

        if not image_exists:
            src_path = os.path.join(labels_dir, label_file)
            dst_path = os.path.join(removed_labels_dir, label_file)
            shutil.move(src_path, dst_path)
            print(f"🔄 Đã chuyển: {label_file}")

# Ví dụ sử dụng cho train
move_orphan_labels(
    images_dir="dataset/images/train",
    labels_dir="dataset/labels/train",
    removed_labels_dir="dataset/labels_removed/train"
)

# Và cho val
move_orphan_labels(
    images_dir="dataset/images/val",
    labels_dir="dataset/labels/val",
    removed_labels_dir="dataset/labels_removed/val"
)
