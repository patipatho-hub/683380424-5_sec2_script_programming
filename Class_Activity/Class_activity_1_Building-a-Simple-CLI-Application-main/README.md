# 📚 Week 7: Building a Simple CLI Application, Error Handling & Project Structure
> **คลังเอกสารและโปรเจกต์ปฏิบัติการสำหรับนักศึกษาชั้นปีที่ 2**  
> สาขาวิทยาการคอมพิวเตอร์ / วิศวกรรมซอฟต์แวร์ / เทคโนโลยีสารสนเทศ

---

## 🎯 เกี่ยวกับสัปดาห์นี้

สัปดาห์ที่ 7 มุ่งเน้นการเปลี่ยนผ่านจากการเขียนโปรแกรมแบบสคริปต์ไฟล์เดียว สู่การพัฒนาซอฟต์แวร์มาตรฐานวิศวกรรมซอฟต์แวร์ โดยครอบคลุม:
1. **สถาปัตยกรรมแบบแยกส่วน (Modular Architecture):** แยกความรับผิดชอบตามหลัก Separation of Concerns (SoC)
2. **การเขียนโปรแกรมเชิงป้องกัน (Defensive Programming):** จัดการข้อผิดพลาดด้วย `try...except` ป้องกันโปรแกรมแครช
3. **การจัดเก็บข้อมูลถาวร (Persistence):** อ่านและบันทึกข้อมูลในรูปแบบ JSON
4. **การดีบักขั้นสูง (VS Code Debugging):** ฝึกใช้ Breakpoint, Step-through, และ Call Stack
5. **การควบคุมเวอร์ชัน (Version Control):** การส่งงานผ่าน Git และ GitHub อย่างมืออาชีพ

---

## 📂 โครงสร้างภายในคลังข้อมูล (Directory Overview)

```text
Week-7-Building-a-Simple-CLI-Application/
├── LAB_GUIDE_WEEK7.md                  # 📘 ใบสั่งงานปฏิบัติการฉบับเต็ม 3 ชั่วโมง (100 คะแนน)
├── Week 7_ ... .docx                   # 📄 เอกสารคำบรรยายต้นฉบับ
├── README.md                           # 📌 เอกสารสรุปภาพรวมประจำสัปดาห์ (ไฟล์นี้)
├── .gitignore                          # ⚙️ กำหนดไฟล์ที่ Git ควรละเว้น
└── my-task-manager/                    # 🚀 โฟลเดอร์โปรเจกต์โค้ดจริง (Starter Code & Solution)
    ├── src/
    │   ├── __init__.py                 # กำหนดเป็น Python Package
    │   ├── task_data.py                # Data Access Layer & JSON Persistence
    │   └── task_logic.py               # Business Logic Layer (Add, List, Complete, Delete, Search)
    ├── data/
    │   └── tasks.json                  # Persistent JSON storage (สร้างอัตโนมัติ)
    ├── main.py                         # Presentation Layer (CLI Menu & Defensive Input)
    ├── .gitignore                      # Gitignore สำหรับโปรเจกต์ย่อย
    └── README.md                       # 🌟 คู่มือโปรเจกต์ภาษาไทยฉบับละเอียด
```

---

## 🔗 ลิงก์ด่วน (Quick Links)

- 📘 **[คู่มือปฏิบัติการฉบับเต็ม (LAB_GUIDE_WEEK7.md)](LAB_GUIDE_WEEK7.md):** ศึกษาขั้นตอนการทดลองทั้ง 5 กิจกรรม, แบบฝึกหัด Debugging และเกณฑ์การให้คะแนน Rubric 100 คะแนน
- 🚀 **[คู่มือโปรเจกต์ Task Manager (my-task-manager/README.md)](my-task-manager/README.md):** ศึกษา Architecture Diagram, คู่มือการใช้งาน CLI และตาราง Exception Matrix
- 💻 **การเริ่มรันโปรแกรม:**
  ```bash
  cd my-task-manager
  python main.py
  ```

---

## 📄 สัญญาอนุญาต (License)
เผยแพร่ภายใต้สัญญาอนุญาต [MIT License](https://opensource.org/licenses/MIT) เพื่อการศึกษาและการเรียนรู้
