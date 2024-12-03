import os
import random
import shutil

# Đường dẫn đến các thư mục ảnh và nhãn trong coco8
images_dir = r'D:\Tuda\SoICT_Hackathon_Vehicle\datasets-full\coco8\images\train'
labels_dir = r'D:\Tuda\SoICT_Hackathon_Vehicle\datasets-full\coco8\labels\train'

# Đường dẫn đến các thư mục ảnh và nhãn validation
val_images_dir = r'D:\Tuda\SoICT_Hackathon_Vehicle\datasets-full\coco8\images\val'
val_labels_dir = r'D:\Tuda\SoICT_Hackathon_Vehicle\datasets-full\coco8\labels\val'

# Tạo thư mục 'val' nếu chưa tồn tại
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Lọc tất cả các thư mục trong 'images/train'
image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))]
label_files = [f.replace('.jpg', '.txt').replace('.png', '.txt') for f in image_files]

# Lọc các tên thư mục (tên file không phải đường dẫn)
image_files.sort()
label_files.sort()

# Trích xuất 10% ngẫu nhiên
num_val = int(len(image_files) * 0.1)
val_images = random.sample(image_files, num_val)

# Di chuyển các ảnh và nhãn đã chọn vào thư mục 'val' và xóa chúng khỏi 'train'
for img_file in val_images:
    # Tạo đường dẫn đầy đủ cho ảnh và nhãn
    img_path = os.path.join(images_dir, img_file)
    label_path = os.path.join(labels_dir, img_file.replace('.jpg', '.txt').replace('.png', '.txt'))

    # Di chuyển ảnh và nhãn vào thư mục 'val'
    shutil.move(img_path, os.path.join(val_images_dir, img_file))
    shutil.move(label_path, os.path.join(val_labels_dir, img_file.replace('.jpg', '.txt').replace('.png', '.txt')))

print(f"Đã di chuyển {num_val} ảnh và nhãn từ 'train' sang 'val' và xóa khỏi 'train'.")
