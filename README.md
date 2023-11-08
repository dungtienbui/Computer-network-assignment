# Computer-network-assignment
1. Bài tập nhóm của môn mạng máy tính học kỳ I năm 2023
2. Chủ đề: Lập trình ứng dụng cho hệ thống chia sẻ file trong mạng máy tính qua giao thức TCP/IP.
3. Mô tả hệ thống: Hệ thống chia sẻ file theo mô hình centralized peer to peer.
4. Hoàn thành:
   - Xây dựng được các tính năng cơ bản:
     + Bên người dùng: tài file, đăng file.
     + Bên máy chủ: ping kiểm tra người dùng, xem danh sách file chia sẻ của một người dùng.
   - Bổ sung các tính năng cơ bản khác:
     + Bên người dùng: đăng nhập, đăng ký, đăng xuất, ngừng chia sẻ file, thay đổi thư mục tải về, thay đổi thư mục chia sẻ.
     + Bên máy chủ: xem danh sách người dùng, xem danh sách tất cả các file chia sẻ, xoá tên một file chia sẻ của một người dùng xác định, xoá tên người dùng.
5. Không hoàn thành:
   - Giao diện: ứng dụng không có giao diện.
   - Các tính năng khác: ứng dụng còn chưa có đầy đủ tính năng cần thiết:
     + Bên người dùng: thêm thông tin vào tài khoản, quản lý thông tin tài khoản, xem danh sách file chia sẻ của bản thân trên máy chủ, thêm mô tả cho file chia sẻ, tự động cập nhật danh sách file chia sẻ, phân quyền chia sẻ đối với một file xác định, tìm kiếm danh sách người dùng chia sẻ file, tự do chọn người dùng để kết nối, báo cáo người dùng khác, kết bạn với người dùng khác, thông báo cho người dùng khác về file chia sẻ của mình.
     + Bên máy chủ: tự động cập nhật danh sách file chia sẻ, lọc file chia sẻ, phân quyền người dùng.
   - Phạm vi: chỉ có thể sử dụng được trong bạng nội bộ, ngoài mạng nội bộ không sử dụng được.
   - Địa chỉ ip: quy định một thiết bị chỉ sử dụng được một địa chỉ ip khi tham gia sử dụng ứng dụng.
   - Kết nối TCP: chưa sử dụng một cách tối ưu, ứng dụng mở một đường TCP chỉ cho một cặp tin nhắn yêu cầu và tin nhắn phản hồi đi qua. Do đó gặp vấn đề đóng mở kết công kết nối liên tục.
   - Kiểm thử: ứng dụng chưa được kiểm tra kĩ càng.
   - Giá trị: ứng dụng chưa được kiểm tra về giá trị.
   - Triển khai: ứng dụng chưa được triển khai.
6. Ứng dụng còn đang được phát triển.
