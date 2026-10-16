# src/task_manager.py

import json
import os
from typing import List, Optional
try:
    from .task import Task
except ImportError:
    from task import Task


class TaskManager:
    """
    คลาสสำหรับจัดการกลุ่มของ Task Objects (Task Collection Management)
    รวมถึงการเพิ่ม แสดงผล แก้ไข ลบ และการบันทึก/โหลดข้อมูลจากไฟล์ JSON
    """

    def __init__(self, data_file: str = 'data/tasks.json'):
        """
        Constructor สำหรับสร้าง TaskManager
        
        Args:
            data_file (str): พาธไฟล์ JSON สำหรับจัดเก็บข้อมูล
        """
        self.data_file = data_file
        # กำหนด absolute path สำหรับไฟล์ข้อมูล เพื่อให้เปิดได้ถูกต้องไม่ว่าจะรันคำสั่งจากโฟลเดอร์ใด
        self._file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', self.data_file)
        )
        
        # TODO 2.1: เรียกใช้ method ภายในเพื่อกำหนดค่าเริ่มต้น
        # 1. โหลดข้อมูล tasks เข้าสู่ self.tasks โดยเรียก self._load_tasks()
        # 2. คำนวณ next_id ถัดไปเข้าสู่ self.next_id โดยเรียก self._get_next_task_id()
        self.tasks: List[Task] = self._load_tasks()
        self.next_id: int = self._get_next_task_id()

    def _get_next_task_id(self) -> int:
        """
        คำนวณ ID ถัดไปสำหรับงานใหม่แบบ Auto-increment
        
        Returns:
            int: ค่า ID สูงสุดที่มีอยู่ + 1 หรือถ้ายังไม่มีงานให้คืนค่า 1
        """
        # TODO 2.2: ตรวจสอบรายการ self.tasks
        # ถ้าไม่มี tasks อยู่เลย ให้ return 1
        # ถ้ามี ให้หา max ของ task.id ใน self.tasks แล้วบวกด้วย 1
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def _load_tasks(self) -> List[Task]:
        """
        โหลดข้อมูลจากไฟล์ JSON แล้วแปลงกลับมาเป็น List ของ Task Objects (Deserialization)
        
        Returns:
            List[Task]: รายการของ Task objects ทั้งหมด
        """
        # หากโฟลเดอร์หรือไฟล์ยังไม่มี ให้สร้างโฟลเดอร์ขึ้นมาและคืนค่าลิสต์ว่าง []
        if not os.path.exists(self._file_path):
            os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
            return []

        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
                # TODO 2.3: แปลง raw_data (list of dict) ให้กลายเป็น list of Task objects
                # เช่น: [Task(item['id'], item['description'], item['completed']) for item in raw_data]
                loaded_tasks = []
                # --- เติมโค้ดของคุณตรงนี้ ---
                for item in raw_data:
                    loaded_tasks.append(Task(item['id'], item['description'], item['completed']))
                return loaded_tasks

        except (json.JSONDecodeError, FileNotFoundError):
            print("Warning: tasks.json is empty or corrupted. Starting with an empty task list.")
            return []

    def _save_tasks(self):
        """
        แปลง Task Objects เป็น Dictionary แล้วบันทึกลงไฟล์ JSON (Serialization)
        """
        # TODO 2.4: แปลง Task objects ใน self.tasks แต่ละตัวให้เป็น dict โดยใช้ method task.to_dict()
        # จากนั้นบันทึกลงไฟล์ self._file_path ด้วย json.dump()
        tasks_as_dicts = [task.to_dict() for task in self.tasks]
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(tasks_as_dicts, f, indent=4, ensure_ascii=False)

    def add_task(self, description: str) -> Task:
        """
        สร้าง Task Object ใหม่ เพิ่มเข้าไปใน self.tasks, ปรับค่า next_id และบันทึกข้อมูล
        
        Args:
            description (str): ข้อความอธิบายงาน
            
        Returns:
            Task: ออบเจกต์งานที่เพิ่งสร้างขึ้น
        """
        # TODO 2.5: 
        # 1. สร้าง new_task = Task(self.next_id, description)
        # 2. เพิ่ม new_task ลงใน self.tasks
        # 3. เพิ่มค่า self.next_id ขึ้น 1
        # 4. บันทึกข้อมูลด้วย self._save_tasks()
        # 5. แสดงข้อความแจ้งเตือนผู้ใช้ และ return new_task
        new_task = Task(self.next_id, description)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_tasks()
        print(f"Task added: {new_task}")
        return new_task

    def list_tasks(self):
        """
        แสดงรายการงานทั้งหมด โดยเรียกใช้งาน __str__ ของแต่ละ Task
        """
        # TODO 2.6:
        # 1. ตรวจสอบหาก self.tasks ว่าง ให้แสดงข้อความว่า "No tasks found."
        # 2. หากมีงาน ให้วนลูปพิมพ์แต่ละ task ออกมา
        if not self.tasks:
            print("No tasks found.")
            return
        for task in self.tasks:
            print(task)

    def complete_task(self, task_id: int) -> bool:
        """
        ค้นหา Task ตาม task_id และเรียกใช้ method mark_complete() ของ Task นั้น
        
        Args:
            task_id (int): รหัสของงานที่ต้องการทำเครื่องหมายว่าเสร็จแล้ว
            
        Returns:
            bool: True หากสำเร็จ, False หากไม่พบงาน
        """
        # TODO 2.7:
        # 1. วนลูปหา task ใน self.tasks ที่ task.id == task_id
        # 2. ถ้าเจอ:
        #    - ถ้า task.completed เป็น True อยู่แล้ว ให้แจ้งเตือนว่างานนี้เสร็จแล้ว
        #    - ถ้ายังไม่เสร็จ ให้เรียก task.mark_complete(), บันทึกไฟล์ self._save_tasks(), แจ้งเตือน และ return True
        # 3. ถ้าไม่พบ ให้แสดง error และ return False
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    print(f"Task ID {task_id} is already completed.")
                else:
                    task.mark_complete()
                    self._save_tasks()
                    print(f"Task ID {task_id} marked as completed.")
                return True
        print(f"Error: Task with ID {task_id} not found.")
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        ลบงานออกจาก self.tasks ตาม task_id
        
        Args:
            task_id (int): รหัสของงานที่ต้องการลบ
            
        Returns:
            bool: True หากลบสำเร็จ, False หากไม่พบงาน
        """
        # TODO 2.8:
        # 1. ตรวจสอบจำนวนงานก่อนลบ
        # 2. กรองเอาเฉพาะ task ที่ id != task_id
        # 3. หากจำนวนลดลง แสดงว่าลบสำเร็จ: บันทึกไฟล์ self._save_tasks(), แจ้งเตือน และ return True
        # 4. หากไม่พบค่างาน ให้แจ้ง error และ return False
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) < initial_count:
            self._save_tasks()
            print(f"Task ID {task_id} deleted successfully.")
            return True
        print(f"Error: Task with ID {task_id} not found.")
        return False
