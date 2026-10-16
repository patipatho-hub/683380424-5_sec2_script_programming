# main.py
"""
Main entry point for the OOP Task Manager CLI application.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import TaskManager


def display_menu():
    """Displays the main menu options to the user."""
    print("\n--- OOP Task Manager Menu ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    print("-------------------------")


def main():
    """Main function to run the Task Manager application."""
    manager = TaskManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            description = input("Enter task description: ").strip()
            if description:
                manager.add_task(description)
            else:
                print("Task description cannot be empty.")

        elif choice == '2':
            manager.list_tasks()

        elif choice == '3':
            task_id_str = input("Enter ID of task to complete: ").strip()
            try:
                task_id = int(task_id_str)
                manager.complete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a number for Task ID.")

        elif choice == '4':
            task_id_str = input("Enter ID of task to delete: ").strip()
            try:
                task_id = int(task_id_str)
                manager.delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a number for Task ID.")

        elif choice == '5':
            print("Exiting Task Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
