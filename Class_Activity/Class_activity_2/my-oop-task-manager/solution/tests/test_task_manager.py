# tests/test_task_manager.py
import unittest
import sys
import os
import json
import shutil
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from task import Task
from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    """
    ชุดทดสอบสำหรับตรวจสอบความถูกต้องของคลาส TaskManager (Milestone 2)
    """

    def setUp(self):
        """เตรียมโฟลเดอร์ชั่วคราวและไฟล์ทดสอบแยกเดี่ยวในแต่ละ Test Case"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file_name = os.path.join(self.test_dir, 'temp_tasks.json')
        self.manager = TaskManager(data_file=self.test_file_name)

    def tearDown(self):
        """ลบโฟลเดอร์ชั่วคราวทิ้งหลังการทดสอบเสร็จสิ้น"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_initial_state_empty(self):
        """ทดสอบค่าเริ่มต้นเมื่อไฟล์ยังว่างเปล่า"""
        self.assertEqual(len(self.manager.tasks), 0, "รายการเริ่มต้นควรมี 0 รายการ")
        self.assertEqual(self.manager.next_id, 1, "next_id เริ่มต้นควรเป็น 1")

    def test_add_task(self):
        """ทดสอบการเพิ่มงานใหม่และการเพิ่มขึ้นของ next_id"""
        task = self.manager.add_task("Complete OOP Lab")
        self.assertIsInstance(task, Task, "add_task ควรคืนค่ากลับมาเป็น Task Instance")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Complete OOP Lab")
        self.assertFalse(task.completed)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.next_id, 2, "next_id ควรเพิ่มขึ้นเป็น 2 หลังเพิ่มงานแรก")

    def test_complete_task(self):
        """ทดสอบการเปลี่ยนสถานะงานให้เสร็จสมบูรณ์ผ่าน TaskManager"""
        t1 = self.manager.add_task("Task 1")
        t2 = self.manager.add_task("Task 2")

        success = self.manager.complete_task(1)
        self.assertTrue(success, "complete_task ควรคืนค่า True เมื่องานถูกทำให้เสร็จ")
        self.assertTrue(self.manager.tasks[0].completed, "งานชิ้นที่ 1 สถานะ completed ควรเปลี่ยนเป็น True")
        self.assertFalse(self.manager.tasks[1].completed, "งานชิ้นที่ 2 สถานะ completed ต้องไม่เปลี่ยน")

        fail = self.manager.complete_task(999)
        self.assertFalse(fail, "complete_task ควรคืนค่า False เมื่องานไม่มีอยู่ในระบบ")

    def test_delete_task(self):
        """ทดสอบการลบงานออกจากระบบ"""
        self.manager.add_task("Task to delete")
        self.manager.add_task("Task to keep")

        success = self.manager.delete_task(1)
        self.assertTrue(success, "delete_task ควรคืนค่า True เมื่อลบสำเร็จ")
        self.assertEqual(len(self.manager.tasks), 1, "จำนวนงานต้องลดลงเหลือ 1")
        self.assertEqual(self.manager.tasks[0].id, 2, "งานที่เหลือต้องมี ID เป็น 2")

        fail = self.manager.delete_task(999)
        self.assertFalse(fail, "delete_task ควรคืนค่า False เมื่องานไม่มีอยู่ในระบบ")

    def test_data_persistence_reload(self):
        """ทดสอบว่าข้อมูลถูกบันทึกลงไฟล์ JSON จริง และสามารถโหลดกลับมาเป็น Task Objects ได้สมบูรณ์"""
        self.manager.add_task("Persistent Task 1")
        self.manager.add_task("Persistent Task 2")
        self.manager.complete_task(1)

        reloaded_manager = TaskManager(data_file=self.test_file_name)
        self.assertEqual(len(reloaded_manager.tasks), 2, "ต้องโหลดงานกลับมาได้ครบ 2 รายการ")
        self.assertIsInstance(reloaded_manager.tasks[0], Task, "ข้อมูลที่โหลดมาต้องถูก Deserialized เป็น Task Object")
        self.assertEqual(reloaded_manager.tasks[0].description, "Persistent Task 1")
        self.assertTrue(reloaded_manager.tasks[0].completed, "สถานะงานที่เสร็จแล้วต้องยังคงเป็น True")
        self.assertEqual(reloaded_manager.next_id, 3, "next_id ที่คำนวณใหม่ต้องเป็น 3")


if __name__ == '__main__':
    unittest.main()
