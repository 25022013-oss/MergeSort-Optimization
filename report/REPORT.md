# Báo cáo Thực nghiệm: Tối ưu hóa MergeSort với ngưỡng chuyển sang Insertion Sort (Cutoff)

- **Sinh viên thực hiện:** Phạm Tiến Thành — MSSV: 25022013
- **Ngôn ngữ & Môi trường:** Java (`package main.java`), phân tích dữ liệu bằng Python (`pandas`, `matplotlib`)
- **Repository:** `https://github.com/25022013-oss/MergeSort-Optimization`

---

## 1. Mục tiêu và Cơ sở thuật toán
- **Mục tiêu:** Đánh giá ảnh hưởng của tham số `cutoff` (ngưỡng kích thước mảng con mà tại đó thuật toán chuyển từ đệ quy MergeSort sang Insertion Sort) đến thời gian thực thi trên các kích thước mảng và kiểu phân phối dữ liệu khác nhau.
- **Cơ chế cài đặt (`src/main/java/MergeCutoff.java`):**
  - Khi kích thước mảng con thỏa mãn `hi - lo + 1 <= cutoff`, gọi `insertionSort(a, lo, hi)` để giảm chi phí đệ quy và tận dụng tính cục bộ bộ nhớ trên đoạn nhỏ.
  - Có điều kiện dừng `if (hi <= lo) return;` để xử lý an toàn trường hợp biên `cutoff = 0`, tránh lỗi `StackOverflowError`.
  - Chỉ gọi `merge(a, aux, lo, mid, hi)` khi `less(a[mid + 1], a[mid])` đúng, tránh trộn lại khi hai nửa đã liền mạch về thứ tự.

---

## 2. Thiết lập thực nghiệm (`ExperimentRunner.java`)
- **Kích thước mảng ($N$):** `10,000`, `50,000`, `100,000`, `500,000`.
- **Kiểu dữ liệu (`TYPES`):** `random`, `nearly_sorted`, `few_unique`.
- **Dải giá trị `cutoff` (`CUTOFFS`):** `0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 17, 20, 25, 30`.
- **Tham số đo:** `WARMUP_RUNS = 3`, `MEASURED_RUNS = 7`, `SEED = 777777L`, kiểm tra tính đúng đắn bằng `MergeCutoff.isSorted(...)` và ghi đè kết quả ra `results/cutoff_results.csv`.

---

## 3. Kết quả thực nghiệm và Biểu đồ

### 3.1. Bảng `cutoff` tối ưu và mức cải thiện so với `cutoff = 0`
| Loại dữ liệu (`type`) | Kích thước ($N$) | `cutoff` tối ưu | Thời gian `cutoff = 0` (ms) | Thời gian tối ưu (ms) | Mức cải thiện (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `few_unique` | 10,000 | 25 | 1.1144 | 0.8605 | 22.78% |
| `few_unique` | 50,000 | 17 | 5.5144 | 4.8963 | 11.21% |
| `few_unique` | 100,000 | 20 | 11.7818 | 10.4923 | 10.94% |
| `few_unique` | 500,000 | 12 | 125.4036 | 113.1652 | 9.76% |
| `nearly_sorted` | 10,000 | 0 | 0.3867 | 0.3867 | 0.00% |
| `nearly_sorted` | 50,000 | 30 | 2.6811 | 2.6383 | 1.60% |
| `nearly_sorted` | 100,000 | 12 | 6.0656 | 5.7753 | 4.79% |
| `nearly_sorted` | 500,000 | 17 | 84.7389 | 82.1392 | 3.07% |
| `random` | 10,000 | 12 | 3.8177 | 1.0788 | 71.74% |
| `random` | 50,000 | 30 | 7.6598 | 6.7274 | 12.17% |
| `random` | 100,000 | 9 | 16.7964 | 15.1811 | 9.62% |
| `random` | 500,000 | 14 | 156.4787 | 147.2990 | 5.87% |

- **Trung bình toàn bộ các cấu hình theo `cutoff`:** Mốc `cutoff = 14` đạt thời gian trung bình thấp nhất là **32.8932 ms**, tiếp theo là `cutoff = 11` (**33.0541 ms**), `cutoff = 17` (**33.1036 ms**), `cutoff = 7` (**33.1310 ms**) và `cutoff = 9` (**33.1377 ms**), đều cải thiện so với `cutoff = 0` (**35.2033 ms**).

### 3.2. Biểu đồ thực nghiệm
- `![Random](../results/figures/cutoff_random.png)`
- `![Nearly Sorted](../results/figures/cutoff_nearly_sorted.png)`
- `![Few Unique](../results/figures/cutoff_few_unique.png)`
- `![Mean by Type](../results/figures/cutoff_mean_by_type.png)`

---

## 4. Phân tích và Nhận xét
- **Biểu đồ `random` (`cutoff_random.png`):** Ở quy mô $N = 500,000$, đường đồ thị chạm đáy tại `cutoff = 14` (`147.2990 ms`, giảm `5.87%` so với `156.4787 ms` ở `cutoff = 0`), giữ vùng giá trị thấp ổn định quanh mốc `7–25` trước khi tăng lên ở `cutoff = 30` (~160.5 ms) khi chi phí bậc hai của Insertion Sort trên đoạn con lớn hơn bắt đầu tăng lên.
- **Biểu đồ `nearly_sorted` (`cutoff_nearly_sorted.png`):** Các đường giữ độ ổn định cao trên toàn bộ dải `cutoff`. Ở $N = 500,000$, `cutoff = 17` đạt mức thấp nhất (`82.1392 ms`), chỉ có một nhịp tăng nhẹ cục bộ tại `cutoff = 3` (~94.5 ms). Ở $N = 10,000$, thời gian rất nhỏ (~0.39 ms) nên `cutoff = 0` đã đủ nhanh và không có cải thiện thêm.
- **Biểu đồ `few_unique` (`cutoff_few_unique.png`):** Ở quy mô lớn $N = 500,000$, thuật toán đạt thời gian tốt nhất tại `cutoff = 12` (`113.1652 ms`, giảm `9.76%` so với `125.4036 ms` tại `cutoff = 0`), giữ mặt bằng thấp trong khoảng `7–17` rồi tăng dần khi tiến tới `30` (~124 ms). Trên đường $N = 10,000$ có một điểm nhô nhẹ tại `cutoff = 5` (~7 ms) do dao động đo ngắn trên JVM.
- **Biểu đồ tổng hợp theo loại dữ liệu (`cutoff_mean_by_type.png`):** Thứ tự thời gian trung bình giữ nguyên rõ rệt: `nearly_sorted` nhanh nhất (~22.8–25.8 ms), tiếp đến là `few_unique` (~32.5–36.0 ms) và `random` (~42.7–46.2 ms). Cả ba phân phối đều có xu hướng đạt vùng hiệu quả tốt quanh dải `9–17` và tăng trở lại khi đẩy `cutoff` lên `30`.

---

## 5. Kết luận
- Ngưỡng `cutoff` tối ưu chung phù hợp nhất cho cấu hình thí nghiệm nằm trong khoảng **9–17** (với `cutoff = 14` đạt thời gian trung bình toàn cục thấp nhất là `32.8932 ms`).
- Việc chuyển sang Insertion Sort ở ngưỡng `cutoff` hợp lý giúp giảm chi phí đệ quy/trộn và cải thiện hiệu năng thực tế so với MergeSort thuần (`cutoff = 0`), đồng thời giữ nguyên độ phức tạp thời gian tiệm cận $O(N \log N)$.