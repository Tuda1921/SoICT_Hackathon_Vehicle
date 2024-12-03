# Bắt đầu từ image cơ sở có hỗ trợ CUDA 11.x và cuDNN
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Cập nhật hệ thống và cài đặt các công cụ cơ bản (curl, git, python3, pip, v.v.)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3-pip \
    python3-dev \
    python3-venv \
    wget bzip2 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Anaconda
RUN curl -sSL https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh -o /tmp/anaconda.sh && \
    bash /tmp/anaconda.sh -b -p /opt/anaconda && \
    rm /tmp/anaconda.sh && \
    /opt/anaconda/bin/conda init bash

ENV PATH /opt/anaconda/bin:$PATH

# Đặt thư mục làm việc trong container
WORKDIR /project

# Sao chép file môi trường conda vào container
COPY environment.yml /project/

# Tạo môi trường conda từ file environment.yml
RUN /opt/anaconda/bin/conda env create -f environment.yml

# Thiết lập để môi trường conda `hkt` tự động kích hoạt mỗi khi mở container
RUN echo "conda activate hakt" >> ~/.bashrc

# Cài đặt các yêu cầu bổ sung từ file requirements.txt
#RUN pip install -r requirements.txt

# Sao chép toàn bộ mã nguồn và dữ liệu vào container
COPY . /project/

# Sao chép shell script vào container và cấp quyền thực thi
COPY train_and_test.sh /project/train_and_test.sh
RUN chmod +x /project/train_and_test.sh

# Chạy shell script khi container khởi động
CMD ["/project/train_and_test.sh"]












