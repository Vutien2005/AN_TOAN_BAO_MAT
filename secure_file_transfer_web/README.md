# Secure File Transfer Web

## Giới thiệu

Đây là dự án hệ thống gửi và nhận file bảo mật qua mạng, sử dụng giao diện web hiện đại (Flask + Bootstrap). Hệ thống đảm bảo an toàn, toàn vẹn và xác thực file nhờ các kỹ thuật mã hóa DES, ký số và trao khóa RSA, kiểm tra hash SHA-512. Hỗ trợ gửi file qua Internet dễ dàng nhờ các dịch vụ tunnel như LocalTunnel hoặc ngrok.

## Tính năng
- Giao diện web cho cả gửi (sender) và nhận (receiver)
- Mã hóa file bằng DES, chia nhỏ tối ưu băng thông
- Ký số, kiểm tra toàn vẹn bằng RSA 1024-bit và SHA-512
- Hỗ trợ gửi file qua Internet bằng LocalTunnel hoặc ngrok
- Dễ sử dụng, giao diện tiếng Việt

## Cấu trúc dự án
```
secure_file_transfer_web/
├── app_receiver.py         # Flask app nhận file
├── app_sender.py           # Flask app gửi file
├── crypto_utils.py         # Hàm tiện ích mã hóa/giải mã, ký số, hash
├── requirements.txt        # Thư viện cần thiết
├── templates/
│   ├── receiver.html       # Giao diện nhận file
│   └── sender.html         # Giao diện gửi file
├── static/                 # (Tùy chọn) CSS
└── uploads/                # Thư mục lưu file nhận được
```

## Cài đặt
1. Cài Python 3.8+
2. Cài các thư viện:
   ```
   pip install -r requirements.txt
   ```
3. Tạo khóa RSA cho sender và receiver:
   - Thêm đoạn sau vào cuối `crypto_utils.py`:
     ```python
     if __name__ == "__main__":
         priv, pub = generate_rsa_keypair()
         with open("sender_private.pem", "wb") as f:
             f.write(priv)
         with open("sender_public.pem", "wb") as f:
             f.write(pub)
         priv, pub = generate_rsa_keypair()
         with open("receiver_private.pem", "wb") as f:
             f.write(priv)
         with open("receiver_public.pem", "wb") as f:
             f.write(pub)
         print("Đã tạo đủ 4 file key .pem")
     ```
   - Chạy:
     ```
     python crypto_utils.py
     ```
   - Sau khi chạy sẽ có 4 file: `sender_private.pem`, `sender_public.pem`, `receiver_private.pem`, `receiver_public.pem`

## Hướng dẫn sử dụng

### 1. Chạy receiver (máy nhận file)
- Chạy Flask receiver:
  ```
  python app_receiver.py
  ```
- Truy cập giao diện nhận tại: http://localhost:8000
- Địa chỉ này sẽ dùng để gửi file từ sender.

### 2. Chạy sender (máy gửi file)
- Chạy Flask sender:
  ```
  python app_sender.py
  ```
- Truy cập giao diện gửi tại: http://localhost:8001
- Chọn file, nhập địa chỉ receiver (ví dụ: http://localhost:8000 hoặc địa chỉ tunnel), nhấn Gửi file.

### 3. Gửi file qua Internet với LocalTunnel
- Cài LocalTunnel:
  ```
  npm install -g localtunnel
  ```
- Chạy tunnel cho receiver:
  ```
  lt --port 8000
  ```
- Lấy địa chỉ public (ví dụ: https://clear-eels-drum.loca.lt), nhập vào ô địa chỉ receiver ở sender.
- Gửi file như bình thường.

### 4. Gửi file qua Internet với ngrok (TCP/HTTP đều được)
- Tải ngrok: https://ngrok.com/
- Chạy:
  ```
  ngrok http 8000
  ```
- Lấy địa chỉ public (ví dụ: https://xxxx.ngrok.io), nhập vào sender.

### 5. Kiểm tra kết quả
- File nhận được sẽ lưu trong thư mục `uploads/` trên máy receiver.
- Log trạng thái sẽ hiển thị trên giao diện web.

## Lời kết

Dự án này giúp bạn gửi và nhận file bảo mật, xác thực, toàn vẹn qua mạng một cách dễ dàng, hiện đại và thân thiện. Bạn có thể mở rộng thêm các tính năng như xác thực người dùng, mã hóa mạnh hơn, hoặc tích hợp vào hệ thống lớn hơn.

Nếu có thắc mắc hoặc cần hỗ trợ, hãy liên hệ tác giả hoặc tham khảo tài liệu trong mã nguồn.

Chúc bạn thành công và sử dụng an toàn!
