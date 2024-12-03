Kiểm tra data Augmentation tại Folder : Full_data_Augmentation
Chỉnh đường dẫn đến folder coco trong file coco8.yaml trong datasets-full
Chỉnh đường dẫn đến folder coco trong file coco8.yaml trong Full_data_Augmentation
Để Train model :
    Mở folder Code3
    chỉnh DATASET_PATH trong file RT_DETR.py
    Run : RT_DETR.py ở folder Code3 để train model
Để chạy kết quả :
    Mở file Run_Result_RT_DETR.py trong folder Result2
    Tinh chỉnh đường dẫn đến weight tốt nhất - best weight - nằm trong Code3\runs\detect\rtdetr_experiment35\weights - ( sau khi train mới có )
  => kết quả được lưu ở Result2



