import os
import cv2

data_folder = 'test'
output_folder = 'ProcessAfterTrain'
os.makedirs(output_folder, exist_ok=True)  # Tạo folder nếu chưa tồn tại

# Lấy danh sách tất cả các file trong folder dữ liệu
all_files = os.listdir(data_folder)

# Lặp qua tất cả các file để tìm file ảnh PNG và file TXT tương ứng
for file in all_files:
    if file.endswith('.jpg'):  # Kiểm tra file có đuôi .png không
        # Lấy tên file TXT tương ứng (cùng tên với file ảnh)
        txt_file = file.replace('.jpg', '.txt')

        if txt_file in all_files:  # Kiểm tra file TXT có tồn tại không
            # Đọc file ảnh PNG
            image_path = os.path.join(data_folder, file)
            img = cv2.imread(image_path)  # Mở ảnh bằng OpenCV
            height, width, _ = img.shape  # Lấy kích thước ảnh (cao, rộng)

            # Đọc file TXT
            txt_path = os.path.join(data_folder, txt_file)
            with open(txt_path, 'r') as f:
                annotations = f.readlines()  # Đọc tất cả các dòng trong file TXT

            # Xử lý từng dòng annotation trong file TXT
            for annotation in annotations:
                parts = annotation.strip().split()  # Chia dòng thành các phần: nhãn, x, y, w, h
                label, x, y, w, h = map(float, parts)  # Chuyển tất cả thành số thực

                # Chuyển tọa độ YOLO (tâm, tỷ lệ) sang tọa độ góc trên-trái và dưới-phải
                x_center = int(x * width)  # Tọa độ x của tâm hộp
                y_center = int(y * height)  # Tọa độ y của tâm hộp
                box_width = int(w * width)  # Chiều rộng của hộp
                box_height = int(h * height)  # Chiều cao của hộp

                # Tính tọa độ góc trên-trái (x1, y1) và góc dưới-phải (x2, y2)
                x1 = int(x_center - box_width / 2)
                y1 = int(y_center - box_height / 2)
                x2 = int(x_center + box_width / 2)
                y2 = int(y_center + box_height / 2)

                # Vẽ hình chữ nhật lên ảnh với OpenCV
                color = (0, 255, 0)  # Màu xanh lá cây cho khung
                thickness = 2  # Độ dày của đường vẽ
                cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)  # Vẽ khung

                # Tuỳ chọn: thêm nhãn (số) lên ảnh
                cv2.putText(img, f'Label {int(label)}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)  # Vẽ nhãn phía trên hộp

            # Lưu ảnh đã xử lý vào folder mới
            output_path = os.path.join(output_folder, file)
            cv2.imwrite(output_path, img)  # Ghi ảnh đã chỉnh sửa vào file

print(f"Đã xử lý xong! Ảnh đã được lưu vào: {output_folder}")
