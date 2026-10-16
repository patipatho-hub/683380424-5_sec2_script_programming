# main.py
"""
จุดเริ่มต้นการทำงานของโปรแกรม CLI Task Manager (Main Entry Point)
ทำหน้าที่จัดการแสดงผลเมนู รับค่าจากผู้ใช้ และส่งต่อไปประมวลผลยัง TaskManager
"""

import sys
import os

# ตั้งค่า stdout และ stderr ให้รองรับ UTF-8 เพื่อป้องกัน UnicodeEncodeError บน Windows (cp874)
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# เพิ่มไดเรกทอรี 'src' เข้าสู่ sys.path เพื่อให้สามารถ import โมดูลภายในโฟลเดอร์ src ได้โดยตรง
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import TaskManager


def display_menu():
    """แสดงเมนูหลักของโปรแกรม"""
    print("\n==============================")
    print("   📋 OOP TASK MANAGER CLI    ")
    print("==============================")
    print("1. Add Task (เพิ่มงานใหม่)")
    print("2. List Tasks (แสดงรายการงานทั้งหมด)")
    print("3. Complete Task (ทำเครื่องหมายงานเสร็จสิ้น)")
    print("4. Delete Task (ลบงาน)")
    print("5. Exit (ออกจากโปรแกรม)")
    print("------------------------------")


def main():
    """ฟังก์ชันหลักสำหรับรันลูปเมนู CLI"""
    # สร้าง Instance ของ TaskManager
    manager = TaskManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            description = input("Enter task description: ").strip()
            if description:
                manager.add_task(description)
            else:
                print("⚠️ Task description cannot be empty.")

        elif choice == '2':
            manager.list_tasks()

        elif choice == '3':
            task_id_str = input("Enter ID of task to complete: ").strip()
            try:
                task_id = int(task_id_str)
                manager.complete_task(task_id)
            except ValueError:
                print("❌ Invalid input! Please enter a valid number for Task ID.")

        elif choice == '4':
            task_id_str = input("Enter ID of task to delete: ").strip()
            try:
                task_id = int(task_id_str)
                manager.delete_task(task_id)
            except ValueError:
                print("❌ Invalid input! Please enter a valid number for Task ID.")

        elif choice == '5':
            print("\n👋 Exiting Task Manager. Happy Coding!")
            break

        else:
            print("⚠️ Invalid choice. Please choose a number between 1 and 5.")


if __name__ == "__main__":
    main()
