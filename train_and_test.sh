#!/bin/bash

echo "Start training RT-DETR..."
python Code3/RT_DETR.py

if [ $? -eq 0 ]; then
    echo "Complete training. start testing ..."

    # Bước 2: Kiểm tra mô hình RT-DETR sau khi huấn luyện
    python Result2/Run_Result_RT_DETR.py
else
    echo "Error in training RT-DETR. Can not test."
    exit 1
fi