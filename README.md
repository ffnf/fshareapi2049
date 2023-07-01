# FSHAREAPI2049
Mình muốn get link fshare vì server (thực ra là Rasperry Pi) của mình không hỗ trợ cài app và mình cũng không thích app nên mình viết code này.

Tài liệu chính thức: https://www.fshare.vn/api-doc

### Yêu cầu:
- Api chỉ dành cho tài khoản VIP nên đây là yêu cầu bắt buộc.
- Một ít kiến thức về Python.

### Cài đặt:
- Truy cập https://www.fshare.vn/api-doc để lấy App Key
- Cài thư viện cho python nếu cho có.
- Điền thông tin tài khoản fshare và app key.

### Cách sử dụng:

- Tải từng link:

`python3 fshareapi2049.py https://www.fshare.vn/file/5T2V4X9U7W1P`

- Tải nhiều link(1 link là 1 dòng - tất cả nằm trong `''`):

```
python3 fshareapi2049.py 'https://www.fshare.vn/file/5T2V4X9U7W1P
https://www.fshare.vn/file/3A7C6B8D4E9Z
https://www.fshare.vn/file/1K6N2R8M3L7Q'
```

- Get link folder:
  
`python3 fshareapi2049.py -f https://www.fshare.vn/file/5T1V4X9U7W1P`

(do mình không cần download folder nên chỉ mới code phần lấy link fshare)
