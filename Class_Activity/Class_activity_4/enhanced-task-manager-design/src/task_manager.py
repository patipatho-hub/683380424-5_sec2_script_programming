# src/task_manager.py
"""
โมดูล task_manager.py: Business Logic Layer ของระบบ Enhanced Task Manager
ทำหน้าที่จัดการ collection ของ Task objects, ควบคุมการทำงาน CRUD,
และเป็นพื้นที่ให้นักศึกษาพัฒนาตรรกะสำหรับการค้นหา (Search), การกรอง (Filter), และการจัดเรียง (Sort)
"""

import datetime
try:
    from .task import Task, DueDateTask, PriorityTask
    from .data_persistence import DataPersistence
except ImportError:
    from task import Task, DueDateTask, PriorityTask
    from data_persistence import DataPersistence



class TaskManager:
    """
    คลาสจัดการงาน (Task Manager)
    มุ่งเน้นที่ Business Logic ล้วนๆ ไม่มีการเข้าถึงไฟล์ I/O หรือ CLI Input/Output โดยตรง
    ตามหลักการ Separation of Concerns
    """
    def __init__(self, data_file='data/tasks.json'):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self):
        """คำนวณหา ID ลำดับถัดไปที่ไม่ซ้ำกันสำหรับงานใหม่"""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def _save_changes(self):
        """บันทึกข้อมูลการเปลี่ยนแปลงไปยัง Data Persistence Layer"""
        self.persistence.save_tasks(self.tasks)

    # =========================================================================
    # การดำเนินการ CRUD พื้นฐาน (พร้อมใช้งาน)
    # =========================================================================

    def add_normal_task(self, description, tags=None):
        """เพิ่มงานทั่วไป (Normal Task)"""
        new_task = Task(self.next_id, description, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def add_due_date_task(self, description, due_date_str, tags=None):
        """เพิ่มงานที่มีวันครบกำหนด (Due Date Task)"""
        new_task = DueDateTask(self.next_id, description, due_date_str, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def add_priority_task(self, description, priority, tags=None):
        """เพิ่มงานที่มีระดับความสำคัญ (Priority Task)"""
        new_task = PriorityTask(self.next_id, description, priority, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def get_task_by_id(self, task_id):
        """ค้นหางานตาม ID"""
        return next((task for task in self.tasks if task.id == task_id), None)

    def complete_task(self, task_id):
        """ทำเครื่องหมายว่างานเสร็จสมบูรณ์แล้ว"""
        task = self.get_task_by_id(task_id)
        if task:
            if not task.completed:
                task.mark_complete()
                self._save_changes()
                return True, f"งาน ID {task_id} ถูกเปลี่ยนสถานะเป็น 'เสร็จสมบูรณ์ (Completed)' แล้ว"
            else:
                return False, f"งาน ID {task_id} มีสถานะเสร็จสมบูรณ์อยู่แล้ว"
        return False, f"ไม่พบงาน ID {task_id} ในระบบ"

    def delete_task(self, task_id):
        """ลบงานออกจากระบบตาม ID"""
        original_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) < original_len:
            self._save_changes()
            return True, f"ลบงาน ID {task_id} เรียบร้อยแล้ว"
        return False, f"ไม่พบงาน ID {task_id} ในระบบ"

    def get_all_tasks(self):
        """ส่งคืนรายการงานทั้งหมด"""
        return list(self.tasks)

    # =========================================================================
    # ฟังก์ชันเพิ่มเติมสำหรับนักศึกษาพัฒนาต่อ (Student Assignment Placeholders)
    # =========================================================================

    def search_tasks(self, keyword):
        """
        [TODO สำหรับนักศึกษา]: ค้นหางานตามคำสำคัญ (keyword)
        
        แนวทางการทำงาน:
        1. รับคำสำคัญ keyword (สตริง)
        2. ตรวจสอบว่า keyword ปรากฏอยู่ใน description (ไม่สนใจตัวพิมพ์เล็ก/ใหญ่)
           หรือปรากฏอยู่ใน tags ตัวใดตัวหนึ่งของ task นั้นหรือไม่
        3. ส่งคืนลิสต์ของ Task objects ที่ตรงตามเงื่อนไข
        
        ตัวอย่างโค้ดแนวทาง:
        keyword_lower = keyword.lower()
        return [
            task for task in self.tasks
            if keyword_lower in task.description.lower()
            or any(keyword_lower in tag.lower() for tag in task.tags)
        ]
        """
        print(f"[DEBUG]: ระบบค้นหาด้วยคำค้น '{keyword}' ยังไม่ได้ถูก Implement (Placeholder)")
        return []

    def filter_tasks(self, status=None, due_date_before=None, priority=None, tags=None):
        """
        [TODO สำหรับนักศึกษา]: กรองงานตามเงื่อนไขที่กำหนด
        
        พารามิเตอร์:
        - status (bool): True = เฉพาะที่เสร็จแล้ว, False = เฉพาะที่ยังไม่เสร็จ, None = ทั้งหมด
        - due_date_before (str | datetime.date): กรองเฉพาะ DueDateTask ที่มีวันกำหนดส่งก่อนหรือตรงกับวันที่นี้
        - priority (str): 'High', 'Medium', 'Low' กรองเฉพาะ PriorityTask ที่ตรงกับระดับที่ระบุ
        - tags (list หรือ str): กรองงานที่มี tag ตรงกับที่ระบุ
        
        แนวทางการทำงาน:
        1. เริ่มต้น filtered = self.tasks
        2. หาก status ไม่เป็น None ให้กรองตาม task.completed == status
        3. หาก due_date_before ระบุ ให้กรองเฉพาะ DueDateTask ที่ task.due_date <= due_date_obj
        4. หาก priority ระบุ ให้กรองเฉพาะ PriorityTask ที่ task.priority.lower() == priority.lower()
        5. หาก tags ระบุ ให้กรองเฉพาะงานที่มี tag อยู่ใน task.tags
        6. ส่งคืน filtered list
        """
        print("[DEBUG]: ระบบกรองงาน (Filter) ยังไม่ได้ถูก Implement (Placeholder)")
        return []

    def sort_tasks(self, criterion="id", reverse=False):
        """
        [TODO สำหรับนักศึกษา]: จัดเรียงงานตามเกณฑ์ที่ระบุ
        
        พารามิเตอร์:
        - criterion (str): "id", "due_date", หรือ "priority" (ค่าเริ่มต้น: "id")
        - reverse (bool): False = จากน้อยไปมาก (Ascending), True = จากมากไปน้อย (Descending)
        
        แนวทางการทำงาน:
        1. ถ้า criterion == "id": เรียงตาม task.id
        2. ถ้า criterion == "due_date":
           - นำ DueDateTask มาเรียงตาม due_date
           - จัดการ Task ทั่วไปที่ไม่มี due_date (เช่น กำหนดให้ไปอยู่ท้ายสุด โดยใช้ datetime.date.max)
        3. ถ้า criterion == "priority":
           - กำหนดค่าลำดับความสำคัญ เช่น priority_map = {"High": 1, "Medium": 2, "Low": 3}
           - Task ทั่วไปให้กำหนดค่าลำดับเป็น 99 เพื่อให้อยู่ลำดับท้ายสุด
        4. ส่งคืนรายการงานที่จัดเรียงแล้ว
        """
        print(f"[DEBUG]: ระบบจัดเรียงงานตาม '{criterion}' ยังไม่ได้ถูก Implement (Placeholder)")
        return list(self.tasks)
