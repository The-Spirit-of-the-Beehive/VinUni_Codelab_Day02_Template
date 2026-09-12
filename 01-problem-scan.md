# 🔍 Phase 1 — SCAN (Cá nhân)

Sử dụng **4 Lenses** quét qua hoạt động vận hành của các công ty thành viên Vingroup và ghi nhận 5 bài toán thực tế:

### 📝 List bài toán của tôi:
| # | Subsidiary (VinFast/Xanh SM...) | Lens | Mô tả ngắn bài toán |
|---|----------------------------------|------|---------------------|
| 1 | **Xanh SM** | Tốn thời gian | Xử lý sự cố cạn kiệt pin thực địa & điều phối xe cứu hộ sạc di động (Mobile Charging Vehicle) cho tài xế taxi điện trong giờ cao điểm. |
| 2 | **VinFast** | AI có thể tốt hơn | Chẩn đoán sơ bộ mã lỗi kỹ thuật và phân loại mức độ khẩn cấp của sự cố xe điện từ mô tả ngôn ngữ tự nhiên của khách hàng qua Hotline/App. |
| 3 | **Vinhomes** | Lặp lại | Tự động phân loại, trích xuất thông tin và điều hướng phản ánh sự cố cư dân (hỏng đèn hành lang, rò rỉ nước, ồn ào) trên App Vinhomes Resident về đúng BQL tòa nhà. |
| 4 | **Vinmec** | Pain từ người khác | Bác sĩ mất quá nhiều thời gian viết tóm tắt hồ sơ xuất viện (Discharge Summary) từ dữ liệu bệnh án điện tử, dẫn đến quá tải hành chính. |
| 5 | **Vinpearl** | AI-upgrade | Tổng hợp, phân tích đa kênh đánh giá của khách hàng (Google Maps, Agoda, Booking) để tự động phát hiện phản ánh tiêu cực khẩn cấp về vệ sinh/dịch vụ phòng. |

---

# 🃏 Phase 2 — QUICK-ASSESS (Cá nhân)

Chọn **top 3 bài toán** từ danh sách trên để xây dựng 3 Quick Problem Cards:

### Quick Problem Card #1
```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán (1 câu): Xử lý sự cố pin nguy cấp (<5%) và điều   │
│ phối xe sạc pin di động/trạm sạc trống cho tài xế Xanh SM. │
│ Công ty thành viên: [x] Xanh SM  [ ] VinFast  [ ] Vinhomes  │
│                                                             │
│ Ai đang đau (Actor)? Tài xế (chờ đợi, sợ chết máy),         │
│ Điều phối viên Trung tâm Điều vận Xanh SM (quá tải thao tác)│
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Nhận cuộc gọi ──> 2. Tra cứu GPS xe ──> 3. Tra cứu     │
│   trạm sạc trống & cổng tương thích ──> 4. Soạn SMS chỉ dẫn │
│   ──> 5. Điều xe cứu hộ nếu pin dưới 5%.                   │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 & 4 (⏱ 10 phút/lượt) │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 3 & 4            │
│ (Phân tích mức pin -> Tự động draft lệnh cứu hộ hoặc SMS)    │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian xử lý sự cố từ 15 phút ──> dưới 2.5 phút;    │
│ 100% trường hợp pin <5% không bị điều đến trạm xa >5km.    │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

### Quick Problem Card #2
```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán (1 câu): Phân loại và định tuyến tự động phản ánh  │
│ cư dân trên App Vinhomes Resident về đúng bộ phận kỹ thuật. │
│ Công ty thành viên: [ ] Xanh SM  [ ] VinFast  [x] Vinhomes  │
│                                                             │
│ Ai đang đau (Actor)? Cư dân (chờ xử lý lâu), Nhân viên CSKH  │
│ Vinhomes (phải đọc và chuyển tiếp thủ công hàng nghìn ticket│
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Tiếp nhận ticket ──> 2. Đọc nội dung & gắn tag lỗi     │
│   ──> 3. Chọn BQL tòa nhà/kỹ thuật ──> 4. Gửi thông báo     │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 8 phút/ticket)│
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3            │
│ (Trích xuất vị trí căn hộ, mức độ nghiêm trọng, route tự động)│
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian phân loại ticket từ 8 phút ──> dưới 15 giây; │
│ Độ chính xác định tuyến đạt trên 92%.                       │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

### Quick Problem Card #3
```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán (1 câu): Trợ lý chẩn đoán sơ bộ mã lỗi xe điện     │
│ VinFast từ mô tả bằng tiếng Việt của khách hàng.            │
│ Công ty thành viên: [ ] Xanh SM  [x] VinFast  [ ] Vinhomes  │
│                                                             │
│ Ai đang đau (Actor)? Kỹ thuật viên tiếp nhận xưởng dịch vụ, │
│ Khách hàng (không biết diễn đạt đúng thuật ngữ kỹ thuật).    │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Nghe mô tả ──> 2. Hỏi lại triệu chứng ──> 3. Tra cứu   │
│   sổ tay kỹ thuật ──> 4. Nhập mã lỗi dự kiến vào hệ thống.  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 & 3 (⏱ 12 phút/lượt) │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 2 & 3            │
│ (Hiểu tiếng Việt tự nhiên -> Map với bảng mã lỗi OBD/CAN-bus)│
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian tiếp nhận xe từ 15 phút ──> 4 phút;          │
│ Độ chính xác gợi ý đúng cụm chi tiết hỏng hóc đạt trên 85%. │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```