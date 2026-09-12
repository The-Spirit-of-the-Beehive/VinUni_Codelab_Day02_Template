# Lab 02 — AI Log & Reflection: AI Product Scoping (Vin Smart Future)

- **Học viên:** Đỗ Hoàng Quân
- **Role:** Học viên chương trình AI Thực chiến - Khoá 4
- **Use Case tập trung:** Trợ lý AI Điều phối Cứu hộ Pin & Chỉ dẫn Trạm sạc (Xanh SM)
- **Ngày thực hiện:** 12/09/2026

---

## 🧭 1. Tổng quan hành trình cộng tác cùng AI

Trong bài Lab 02, tôi sử dụng AI với vai trò là **Thought-Partner (Bạn đồng hành tư duy & Phản biện kỹ thuật)** xuyên suốt 4 giai đoạn:
1. **Brainstorm & Lọc bài toán (Phase 1 & 2):** Quét qua các công ty thành viên Vingroup và stress-test các ý tưởng bài toán.
2. **Thiết kế quy trình & Ranh giới vận hành (Phase 3):** Định hình 6-field Problem Statement và cơ chế Human-in-the-loop (HITL).
3. **Lập trình & Debug Prompt Prototype (Phase 4):** Xây dựng ranh giới an toàn trong System Prompt và xử lý lỗi kỹ thuật khi kết nối Google Gemini API.
4. **Phản biện & Đánh giá dự án (Phase 5):** Đánh giá tính khả thi và đưa ra quyết định GO/NO-GO dựa trên số liệu thực tế.

---

## 📝 2. Nhật ký tương tác & Phản biện chi tiết (Interaction Logs)

### 🔹 Phiên 1: Scoping bài toán & Stress-testing ranh giới (Phase 1 & 2)
* **Prompt gửi AI:**
  > *"Tôi là AI Engineer tại Vin Smart Future. Hãy giúp tôi phản biện 3 bài toán của Xanh SM, VinFast và Vinhomes dưới góc nhìn của một Trưởng phòng Vận hành khắt khe. Bài toán nào có rủi ro pháp lý cao nhất và bài toán nào mang lại ROI tức thì nhất?"*
* **AI hỗ trợ được gì:** 
  * AI đã chỉ ra rất sắc bén rằng bài toán CSKH Vinhomes (Card #2) có rủi ro pháp lý và tranh chấp căn hộ cao nếu AI trả lời sai về quy định phí dịch vụ; trong khi bài toán sự cố pin Xanh SM (Card #1) có input/output cụ thể, dễ kiểm soát ranh giới và mang lại ROI ngay lập tức.
* **Điểm AI gợi ý chưa chuẩn (Sai/Thiếu sót):**
  * AI ban đầu đề xuất xây dựng một **Autonomous Multi-Agent** để tự động đặt lệnh xe cứu hộ và tự nhắn tin trực tiếp cho tài xế Xanh SM.
* **Cách tôi điều chỉnh & phản biện lại:**
  * Tôi đã bác bỏ kiến trúc Agent tự trị vì chi phí điều xe cứu hộ là chi phí thực, và việc điều nhầm xe hoặc sai trạm sạc sẽ làm xe chết máy giữa đường. Tôi quyết định hạ scope xuống **LLM Feature có Human-in-the-loop (Bắt buộc Dispatcher duyệt với thẻ `[DRAFT_ONLY]`)**.

---

### 🔹 Phiên 2: Xây dựng System Prompt & Thiết lập ranh giới an toàn (Phase 3 & 4)
* **Mục tiêu:** Định nghĩa các quy tắc bất khả xâm phạm để chống lại các cuộc tấn công Prompt Injection / Jailbreak.
* **Quy tắc cốt lõi đã thiết lập:**
  1. Luôn xuất hiện tiền tố `[DRAFT_ONLY]` ở đầu mọi phản hồi.
  2. Pin < 5%: Cấm tuyệt đối gợi ý trạm sạc cách xa > 5km $\rightarrow$ Bắt buộc kích hoạt cứu hộ xe sạc di động dạng JSON `{"action": "dispatch_mobile_charger", ...}`.
* **Thử nghiệm Adversarial Test:**
  * *Tấn công:* Giả lập tài xế vội đón khách, ép AI bỏ qua thẻ nháp và ép chỉ đường đến trạm cách 8km khi pin chỉ còn 2%.
  * *Kết quả:* System Prompt đã chặn đứng thành công, mô hình từ chối chỉ đường trạm xa và kích hoạt xe sạc lưu động.

---

### 🔹 Phiên 3: Debug kỹ thuật khi triển khai SDK Google Gemini
Trong quá trình code file `prompt_prototype.py`, nhóm đã gặp một chuỗi lỗi kỹ thuật thực tế và cùng AI gỡ rối:

1. **Lỗi 1 — `'module' object is not callable`:**
   * *Nguyên nhân:* Nhầm lẫn giữa cú pháp của SDK cũ `google-generativeai` và SDK mới `google-genai`.
   * *Xử lý:* Cập nhật cấu trúc khởi tạo client chính xác theo chuẩn SDK.
2. **Lỗi 2 — `404 models/gemini-1.5-flash is not found` & Deprecation Warning:**
   * *Nguyên nhân:* Thư viện `google.generativeai` đã bị Google khai tử (deprecated) và không hỗ trợ model định danh mới.
   * *Xử lý:* Cài đặt gói chính thức mới `pip install -U google-genai` và cấu hình `types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.0)`.

---

## ⚖️ 3. Đánh giá năng lực của AI trong buổi Lab (Critical Evaluation)

| Tiêu chí | AI làm rất tốt (Strengths) | AI còn hạn chế (Blind Spots) |
|---|---|---|
| **Tốc độ Scoping** | Tạo nhanh các khung mẫu (templates), gợi ý số liệu thống kê giả định sát thực tế. | Thường có xu hướng "Over-engineering" (luôn muốn dùng Agent phức tạp thay vì giải pháp đơn giản). |
| **Bảo vệ Ranh giới** | Tuân thủ tốt các instruction có cấu trúc phân cấp (Numbered rules, capitalization). | Dễ bị ảnh hưởng nếu prompt chỉ thị mơ hồ; cần phải dùng từ ngữ mang tính cấm đoán tuyệt đối (*STRICTLY FORBIDDEN, NEVER*). |
| **Debug Code** | Nhanh chóng nhận diện sự thay đổi giữa các phiên bản SDK của Google (`google-genai` vs `google-generativeai`). | Đôi khi đưa ra code mẫu thuộc phiên bản cũ nếu không được nhắc rõ về version SDK. |

---

## 💡 4. Bài học & Chiêm nghiệm cá nhân (Reflection)

1. **"Problem First, AI Second":**
   * Giá trị lớn nhất của buổi Lab không phải là dùng mô hình nào phức tạp nhất, mà là việc xác định đúng **Bottleneck** (bước 3 & 4 tốn 10 phút tra cứu thủ công) và thiết kế một giải pháp vừa vặn (LLM Feature) giải quyết triệt để nỗi đau của Dispatcher.

2. **Ranh giới an toàn (Guardrails) là linh hồn của AI Product:**
   * Một mô hình AI dù thông minh đến đâu nhưng nếu không có ranh giới (`[DRAFT_ONLY]`, không điều xe cạn pin đi xa) thì không bao giờ có thể đưa vào môi trường sản xuất (Production) của Vingroup. Kỹ sư AI giỏi là người biết cách "xích" AI lại trong vùng an toàn trước khi trao quyền cho nó.

3. **Tư duy làm chủ công nghệ (Human-in-the-loop):**
   * AI là một công cụ tăng tốc tư duy tuyệt vời, nhưng người kỹ sư phải giữ vai trò "thuyền trưởng": biết nghi ngờ các đề xuất phức tạp hóa của AI, kiên quyết giữ vững tư duy đơn giản hóa bài toán và kiểm soát chặt chẽ từng dòng code thực thi.