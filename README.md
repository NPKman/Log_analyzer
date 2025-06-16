
# ------------------------- Thai ------------------------- 

# 🧠 Log Analyzer GUI

โปรแกรม GUI สำหรับวิเคราะห์ไฟล์ Log (.txt / .log) แบบรวดเร็วและยืดหยุ่น โดยสามารถค้นหา keyword, กรองช่วงเวลา, นับจำนวนเหตุการณ์แยกตาม IP และ export ออกเป็น CSV ได้ง่าย ๆ

## ✅ ฟีเจอร์หลัก

- 📂 **เลือกไฟล์ Log ได้หลายไฟล์** (.txt, .log)
- 🔍 **ค้นหา Keyword** ที่ระบุได้เอง
- 📅 **เลือกช่วงเวลาเริ่มต้น / สิ้นสุด** ด้วย ComboBox
- 📊 **โหมด Count / Show**
  - Count: แสดงจำนวนครั้งของ IP ที่พบ
  - Show: แสดงข้อความ log ที่ตรงเงื่อนไข
- 📤 **Export เป็น CSV**
- 🔁 **Reset ระบบทั้งหมด**
- 🌀 **Progress Bar แบบ Animation**
  - ขณะ Import / Analyze ไฟล์
  - แสดงชื่อไฟล์ที่กำลังอ่าน
- ❌ **Cancel** กระบวนการกลางทางได้
- 🎨 **ฟอนต์ Comic Sans MS** (ถ้ามี)
- 🪟 **ตั้ง Icon ไฟล์** (`icon.ico`)

## 🖼️ Layout UI

-```plaintext
[🧠 Log Analyzer]
[📂 Browse Files]

Keyword: [______________]

(•) Count   ( ) Show

Start Date:  [Dropdown ▼]
End Date:    [Dropdown ▼]

[🔍 Analyze] [📤 Export CSV] [🔁 Reset]

[ผลลัพธ์จะแสดงใน Listbox ที่ด้านล่าง]

- ```

# ----------------------------- English ----------------------------------------

# 🧠 Log Analyzer GUI

A user-friendly Python GUI application for analyzing log files. Search specific keywords across multiple `.txt` or `.log` files, filter by time range, count matching IPs, and export results — all with real-time progress feedback.

---

## ✅ Features

- 📂 **Multi-file Log Import** – Supports `.txt` and `.log` files
- 🔍 **Keyword Search** – Custom keyword input field
- 📅 **Datetime Filter** – Selectable `Start` and `End` from log timestamps
- 📊 **Count / Show Modes**
  - **Count:** Summarize matches by date and IP address
  - **Show:** Display full matching lines
- 📤 **Export to CSV** – Save analyzed data
- 🔁 **Reset Function** – Clears all fields and results
- 🌀 **Progress Animation**
  - While importing or analyzing logs
  - Shows current file being processed
- ❌ **Cancel Button** – Interrupt operations in real-time
- 🎨 **Comic Sans MS Font** – Applied globally if available
- 🪟 **Custom Window Icon** – Uses `icon.ico` if present

---

## 🖥️ User Interface Layout

-```plaintext

🧠 Log Analyzer

[📂 Browse Files]

Keyword: [__________]

(•) Count ( ) Show

Start Date: [dropdown ▼]
End Date: [dropdown ▼]

[🔍 Analyze] [📤 Export CSV] [🔁 Reset]

[Listbox for results displayed here]

-```
