# src/task.py

class Task:
    """
    คลาสสำหรับจำลองข้อมูลงานแต่ละรายการ (Single Task)
    
    Attributes:
        id (int): รหัสประจำงานที่ไม่ซ้ำกัน
        description (str): รายละเอียดข้อความของงาน
        completed (bool): สถานะการทำงาน (True = ทำเสร็จแล้ว, False = ยังไม่เสร็จ)
    """

    def __init__(self, id: int, description: str, completed: bool = False):
        """
        Initializes a new Task object.
        
        Args:
            id (int): A unique identifier for the task.
            description (str): A brief description of the task.
            completed (bool, optional): The completion status of the task. Defaults to False.
        """
        self.id = id
        self.description = description
        self.completed = completed

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """
        Converts the Task object to a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the task.
        """
        status = "Completed" if self.completed else "Pending"
        return f"ID: {self.id} | Description: {self.description} | Status: {status}"

    def __repr__(self) -> str:
        """
        Returns an official string representation of the task object for debugging.
        """
        return f"Task(id={self.id}, description='{self.description}', completed={self.completed})"
