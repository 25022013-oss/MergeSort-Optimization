# Nhật ký trao đổi với AI — Tối ưu hóa MergeSort với Cutoff

- **Sinh viên thực hiện:** Phạm Tiến Thành — MSSV: 25022013
- **Dự án:** MergeSort Optimization (Insertion Sort Cutoff)
- **Phạm vi ghi nhận:** Hỗ trợ cấu hình benchmark, xử lý/phân tích kết quả, vẽ biểu đồ và soạn báo cáo `report/REPORT.md` (*phần cài đặt `MergeCutoff.java` do sinh viên tự triển khai*).

---

## 1. Cấu hình thực nghiệm và điều chỉnh quy mô mảng
- **Tóm tắt trao đổi:**
  - Thống nhất đánh giá tham số `cutoff` (ngưỡng chuyển sang Insertion Sort) qua các phân phối `random`, `nearly_sorted`, `few_unique` với dải ngưỡng `0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 17, 20, 25, 30`, `WARMUP_RUNS = 3`, `MEASURED_RUNS = 7`, `SEED = 777777L`.
  - Khi thử nghiệm mở rộng tới `N = 1,000,000`, xuất hiện các đỉnh đo tăng cao bất thường ở một số ngưỡng làm lệch giá trị trung bình chung.
  - Quyết định điều chỉnh `SIZES` trong `ExperimentRunner.java` thành `{10_000, 50_000, 100_000, 500_000}` để giảm nhiễu đo ở kích thước quá lớn mà vẫn đảm bảo quy mô đánh giá rõ rệt.

---

## 2. Phân tích số liệu thực nghiệm và kiểm tra tính thực tế
- **Tóm tắt trao đổi:**
  - Đối chiếu bảng `BEST CUTOFF BY (TYPE, N)`, `SPEEDUP VS CUTOFF = 0` và `MEAN TIME ACROSS ALL TESTS BY CUTOFF` sau khi chạy tới `500,000`.
  - Kết quả trung bình chung ghi nhận `cutoff = 14` đạt mức thấp nhất (`32.8932 ms`), kế tiếp là `cutoff = 11` (`33.0541 ms`), `cutoff = 17` (`33.1036 ms`), `cutoff = 7` (`33.1310 ms`) và `cutoff = 9` (`33.1377 ms`), cải thiện so với `cutoff = 0` (`35.2033 ms`).
  - Nhấn mạnh nguyên tắc giữ nguyên dữ liệu đo thực tế (không sửa tay CSV) và giải thích đúng bản chất các biến động cục bộ trên từng đường biểu đồ.

---

## 3. Hoàn thiện báo cáo `report/REPORT.md` và chuẩn bị nộp lên GitHub
- **Tóm tắt trao đổi:**
  - Đặt báo cáo chính tại `report/REPORT.md` khớp với cấu trúc thư mục dự án (`src/`, `results/`, `report/`, `ai-logs/`).
  - Cập nhật đường dẫn ảnh tương đối `../results/figures/...` cho 4 biểu đồ (`cutoff_random_3.png`, `cutoff_nearly_sorted_3.png`, `cutoff_few_unique_3.png`, `cutoff_mean_by_type_3.png`).
  - Rà soát các hạng mục cần nộp trên repository trước khi thực hiện `git add .`, `git commit` và `git push`.