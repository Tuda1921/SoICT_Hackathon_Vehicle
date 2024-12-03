import os

# Đường dẫn đến tập dữ liệu
train_images_dir = r"F:/detr/Full_data_Augmentation/coco8/image/train"
train_labels_dir = r"F:/detr/Full_data_Augmentation/coco8/label/train"

# Kiểm tra số lượng file
train_images = sorted(os.listdir(train_images_dir))
train_labels = sorted(os.listdir(train_labels_dir))

# Kiểm tra số lượng ảnh và nhãn
print(f"Number of images: {len(train_images)}")
print(f"Number of labels: {len(train_labels)}")

# Kiểm tra file nhãn khớp với ảnh
missing_labels = [img for img in train_images if f"{os.path.splitext(img)[0]}.txt" not in train_labels]
if missing_labels:
    print(f"Images without labels: {missing_labels}")
else:
    print("All images have corresponding labels.")

# Kiểm tra nội dung nhãn
for label_file in train_labels:
    label_path = os.path.join(train_labels_dir, label_file)
    with open(label_path, 'r') as f:
        content = f.read().strip()
        if not content:
            print(f"Empty label file: {label_file}")
