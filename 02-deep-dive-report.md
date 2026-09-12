# 🏗️ Phase 3 — DEEP-DIVE (Nhóm)

Nhóm thống nhất chọn bài toán **Quick Problem Card #1: Trợ lý AI Điều phối Cứu hộ Pin & Chỉ dẫn Trạm sạc Thông minh cho Xanh SM**.

## 3.1. Current-State Workflow Mapping
Quy trình thủ công hiện tại của Điều phối viên (Dispatcher):
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Nhận cuộc    │     │ Tra cứu GPS  │     │ Tra cứu trụ  │     │ Soạn nội dung│
│ gọi/tin nhắn │ ──→ │ vị trí xe &  │ ──→ │ sạc trống &  │ ──→ │ SMS/Lệnh     │
│ báo hết pin  │     │ % pin còn lại│     │ cổng phù hợp │     │ cứu hộ       │
│ Ai: Dispatch │     │ Ai: Dispatch │     │ Ai: Dispatch │     │ Ai: Dispatch │
│ ⏱ 2 phút     │     │ ⏱ 2 phút     │     │ ⏱ 5 phút 🔴  │     │ ⏱ 5 phút 🔴  │
│ In: SĐT/Biển │     │ In: Biển số  │     │ In: GPS, Pin │     │ In: Raw info │
│ Out: Ticket  │     │ Out: Toạ độ  │     │ Out: Địa chỉ │     │ Out: Draft   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────────┐
                                                               │ Bước 5       │
                                                               │ Duyệt & gửi  │
                                                               │ SMS / Điều xe│
                                                               │ Ai: Dispatch │
                                                               │ ⏱ 1 phút     │
                                                               └──────────────┘

🔴 = Bottleneck chính (Bước 3 & 4 ngốn 10 phút, dễ nhầm lẫn cổng sạc xe VF5/VF8/VF9).
⏱ Tổng thời gian vận hành trung bình: 15 phút/lượt.
```

---

## 3.2. Problem Statement (6-field) & Metrics

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Điều phối viên (Dispatcher) tại Trung tâm Điều vận Xanh SM toàn quốc. |
| **2. Current Workflow** | Khi nhận cảnh báo xe sắp hết pin hoặc cuộc gọi khẩn cấp của tài xế, điều phối viên mở dashboard định vị xe, mở hệ thống giám sát trạm sạc VinFast để tìm trụ sạc trống phù hợp, tính toán khoảng cách, sau đó tự gõ tin nhắn SMS hướng dẫn đường đi hoặc gọi đội cứu hộ lưu động nếu pin dưới 5%. Quy trình 5 bước thủ công mất trung bình 15 phút. |
| **3. Bottleneck** | **Bước 3 & 4 (mất ~10 phút):** Phải đối chiếu thủ công nhiều màn hình (tọa độ xe, dung lượng pin hiện tại, danh sách trạm sạc còn trụ trống, loại cổng sạc tương thích với dòng xe) và tự soạn thảo tin nhắn hướng dẫn rõ ràng, chuẩn xác. |
| **4. Business Impact** | Trung bình 120 sự cố pin/ngày tại các thành phố lớn. Tiêu tốn ~30 giờ lao động/ngày của đội ngũ điều phối. Xe nằm chờ lâu gây rò rỉ ~18% doanh thu cuốc xe giờ cao điểm, tăng nguy cơ xe chết máy giữa đường gây ùn tắc và ảnh hưởng nghiêm trọng đến hình ảnh Xanh SM. |
| **5. Success Metric** | 1. **Thời gian xử lý:** Giảm tổng thời gian xử lý từ 15 phút xuống dưới 2.5 phút/lượt (giảm >80%).<br>2. **An toàn pin:** 100% trường hợp pin < 5% được kích hoạt lệnh xe sạc di động (không điều xe đi xa > 5km).<br>3. **Chất lượng draft:** 95% tin nhắn nháp do AI sinh ra được điều phối viên duyệt mà không cần sửa lại nội dung. |
| **6. Operational Boundary** | **AI ĐƯỢC PHÉP:** Đọc dữ liệu xe (GPS, % pin), đọc dữ liệu trạm sạc VinFast, tự động tạo tin nhắn nháp (bắt buộc gắn tag `[DRAFT_ONLY]`) hoặc tạo cấu trúc JSON yêu cầu cứu hộ.<br>**AI TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP:** Tự động gửi tin nhắn đến tài xế mà chưa qua điều phối viên duyệt; Không được đề xuất trạm sạc cách xa >5km khi pin xe <5%. |

---

## 3.3. Future-State Flow & AI Fit

* **AI Fit:** Chọn **LLM Feature (tích hợp Prompt Guardrail)**. (Không dùng Autonomous Agent hoàn toàn vì quyết định điều xe cứu hộ phát sinh chi phí vận hành và rủi ro an toàn giao thông, bắt buộc phải có Human-in-the-loop).
* **Sơ đồ quy trình tương lai (Future-State):**

```
┌─────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│ Bước 1          │      │ Bước 2 (🔵 AI Step)     │      │ Bước 3 (🟢 HITL Step)  │
│ Tiếp nhận yêu   │ ───> │ Gemini 2.5 phân tích   │ ───> │ Dispatcher kiểm tra    │
│ cầu/sự cố pin   │      │ pin, vị trí, trạm sạc  │      │ bản nháp [DRAFT_ONLY]  │
│ (Hệ thống Xanh) │      │ & soạn Draft/Cứu hộ    │      │ và bấm 1-Click Duyệt   │
└─────────────────┘      └────────────────────────┘      └────────────────────────┘
                                                                      │
                                                                      ▼
                                                               ┌────────────────────────┐
                                                               │ ↩️ Fallback Step       │
                                                               │ Nếu AI timeout/lỗi/    │
                                                               │ parser fail: Chuyển về │
                                                               │ quy trình thủ công cũ  │
                                                               └────────────────────────┘
```

# 🏁 Phase 5 — EVALUATE (Nhóm)

### AI Readiness Checklist:
1. [x] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test (Logs GPS, telemetry pin xe Xanh SM và API trạng thái trạm sạc VinFast).
2. [x] Rủi ro khi AI sai có nằm trong tầm kiểm soát (Bắt buộc Human-in-the-loop duyệt tin + Cơ chế fallback quay về gõ tay).
3. [x] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ (Đội ngũ điều phối viên rất hào hứng vì được giảm tải áp lực giờ cao điểm).

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:
- [x] **GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp (Pilot tại 1 Hub điều vận Hà Nội).
- [ ] **NOT YET**
- [ ] **NO-GO**

**Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí):**
1. **Giá trị kinh tế & vận hành (ROI cao):** Cắt giảm 80% thời gian xử lý sự cố (từ 15 phút xuống <2.5 phút), giải phóng 30 giờ công lao động/ngày của dispatchers và giảm thiểu đáng kể số cuốc xe bị hủy do chết máy.
2. **Độ khả thi kỹ thuật cao:** Sử dụng kiến trúc LLM Feature với Gemini 2.5 Flash có độ trễ thấp, chi phí API cực rẻ (< $0.001/lượt xử lý), hoàn toàn phù hợp với ngân sách vận hành của Xanh SM.
3. **An toàn tuyệt đối:** Bản mẫu kỹ thuật đã chứng minh được tính vững chắc trước các prompt tấn công; cơ chế `[DRAFT_ONLY]` đảm bảo con người luôn làm chủ quyết định cuối cùng.