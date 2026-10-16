# tests/test_task.py
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from task import Task


class TestTaskClass(unittest.TestCase):
    """
    ชุดทดสอบสำหรับตรวจสอบความถูกต้องของคลาส Task (Milestone 1)
    """

    def test_task_initialization(self):
        """ทดสอบการสร้าง Instance และการกำหนดค่าเริ่มต้นให้กับ Attributes"""
        t = Task(1, "Read OOP textbook")
        self.assertEqual(t.id, 1, "Attribute 'id' ควรมีค่าเท่ากับ 1")
        self.assertEqual(t.description, "Read OOP textbook", "Attribute 'description' ไม่ตรงกับที่กำหนด")
        self.assertFalse(t.completed, "ค่าเริ่มต้นของ 'completed' ควรเป็น False เสมอ")

    def test_task_initialization_with_completed_true(self):
        """ทดสอบการส่งพารามิเตอร์ completed=True เข้ามาใน Constructor"""
        t = Task(2, "Submit lab report", completed=True)
        self.assertEqual(t.id, 2)
        self.assertEqual(t.description, "Submit lab report")
        self.assertTrue(t.completed, "Attribute 'completed' ควรเป็น True เมื่อถูกกำหนดมา")

    def test_mark_complete(self):
        """ทดสอบ Method mark_complete() ว่าเปลี่ยนสถานะเป็น True หรือไม่"""
        t = Task(3, "Practice Python coding")
        self.assertFalse(t.completed)
        t.mark_complete()
        self.assertTrue(t.completed, "หลังเรียก mark_complete() สถานะ completed ต้องเป็น True")

    def test_to_dict(self):
        """ทดสอบการแปลง Object เป็น Dictionary สำหรับ JSON Serialization"""
        t = Task(10, "Refactor CLI code", completed=False)
        expected = {
            "id": 10,
            "description": "Refactor CLI code",
            "completed": False
        }
        result = t.to_dict()
        self.assertIsInstance(result, dict, "to_dict() ต้องคืนค่าเป็น type dict")
        self.assertEqual(result, expected, "Dictionary ที่ได้จาก to_dict() มีโครงสร้างหรือค่าไม่ถูกต้อง")

    def test_str_representation(self):
        """ทดสอบ __str__ เมธอดสำหรับการแสดงผลให้ผู้ใช้ (User-friendly)"""
        t_pending = Task(1, "Write tests", completed=False)
        str_pending = str(t_pending)
        self.assertIn("ID: 1", str_pending)
        self.assertIn("Write tests", str_pending)
        self.assertIn("Pending", str_pending, "ถ้า completed เป็น False ต้องแสดงสถานะ Pending")

        t_done = Task(2, "Review PR", completed=True)
        str_done = str(t_done)
        self.assertIn("Completed", str_done, "ถ้า completed เป็น True ต้องแสดงสถานะ Completed")

    def test_repr_representation(self):
        """ทดสอบ __repr__ เมธอดสำหรับการ Debug (Developer-friendly)"""
        t = Task(5, "Fix bug", completed=True)
        repr_str = repr(t)
        self.assertEqual(
            repr_str,
            "Task(id=5, description='Fix bug', completed=True)",
            "__repr__ ควรมีรูปแบบตรงตามมาตรฐาน 'Task(id=..., description='...', completed=...)'"
        )


if __name__ == '__main__':
    unittest.main()
