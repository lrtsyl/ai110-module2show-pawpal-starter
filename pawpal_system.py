from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import List, Optional, Tuple


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
VALID_FREQUENCIES = {"once", "daily", "weekly"}


@dataclass
class Task:
    """Represents a pet care task with scheduling details."""

    description: str
    time_str: str
    due_date: date = field(default_factory=date.today)
    frequency: str = "once"
    priority: str = "medium"
    completed: bool = False
    category: str = "general"

    def __post_init__(self) -> None:
        """Normalize task values and validate the time format."""
        self.description = self.description.strip()
        self.time_str = self.time_str.strip()
        self.frequency = self.frequency.lower().strip()
        self.priority = self.priority.lower().strip()
        self.category = self.category.lower().strip()

        if self.frequency not in VALID_FREQUENCIES:
            self.frequency = "once"

        if self.priority not in PRIORITY_ORDER:
            self.priority = "medium"

        datetime.strptime(self.time_str, "%H:%M")

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Create the next recurring task if frequency is daily or weekly."""
        if self.frequency == "daily":
            return Task(
                description=self.description,
                time_str=self.time_str,
                due_date=self.due_date + timedelta(days=1),
                frequency=self.frequency,
                priority=self.priority,
                category=self.category,
            )
        if self.frequency == "weekly":
            return Task(
                description=self.description,
                time_str=self.time_str,
                due_date=self.due_date + timedelta(weeks=1),
                frequency=self.frequency,
                priority=self.priority,
                category=self.category,
            )
        return None

    def sort_key(self) -> datetime:
        """Return a datetime used for chronological sorting."""
        task_time = datetime.strptime(self.time_str, "%H:%M").time()
        return datetime.combine(self.due_date, task_time)

    def priority_rank(self) -> int:
        """Return a sortable numeric rank for priority."""
        return PRIORITY_ORDER[self.priority]

    def to_dict(self) -> dict:
        """Serialize the task to a JSON-friendly dictionary."""
        return {
            "description": self.description,
            "time_str": self.time_str,
            "due_date": self.due_date.isoformat(),
            "frequency": self.frequency,
            "priority": self.priority,
            "completed": self.completed,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task from serialized data."""
        return cls(
            description=data["description"],
            time_str=data["time_str"],
            due_date=date.fromisoformat(data["due_date"]),
            frequency=data.get("frequency", "once"),
            priority=data.get("priority", "medium"),
            completed=data.get("completed", False),
            category=data.get("category", "general"),
        )

    def __str__(self) -> str:
        """Return a readable string representation for CLI output."""
        status = "✓" if self.completed else "•"
        return (
            f"{status} {self.due_date.isoformat()} {self.time_str} - "
            f"{self.description} [{self.priority}] ({self.frequency})"
        )


@dataclass
class Pet:
    """Represents a pet and its scheduled tasks."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return this pet's tasks, optionally excluding completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]

    def to_dict(self) -> dict:
        """Serialize the pet to a JSON-friendly dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        """Create a Pet from serialized data."""
        pet = cls(name=data["name"], species=data["species"], age=data["age"])
        for task_data in data.get("tasks", []):
            pet.add_task(Task.from_dict(task_data))
        return pet


class Owner:
    """Represents a pet owner who manages multiple pets."""

    def __init__(self, name: str) -> None:
        """Initialize an owner with an empty pet list."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self, include_completed: bool = True) -> List[Tuple[Pet, Task]]:
        """Return all tasks across all pets."""
        all_tasks: List[Tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.get_tasks(include_completed=include_completed):
                all_tasks.append((pet, task))
        return all_tasks

    def to_dict(self) -> dict:
        """Serialize the owner to a JSON-friendly dictionary."""
        return {
            "name": self.name,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    def save_to_json(self, filepath: str = "pawpal_data.json") -> None:
        """Persist the owner, pets, and tasks to a JSON file."""
        path = Path(filepath)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load_from_json(cls, filepath: str = "pawpal_data.json") -> "Owner":
        """Load owner data from JSON or return a fresh owner if the file is missing."""
        path = Path(filepath)
        if not path.exists():
            return cls("Pet Owner")

        data = json.loads(path.read_text(encoding="utf-8"))
        owner = cls(data.get("name", "Pet Owner"))
        for pet_data in data.get("pets", []):
            owner.add_pet(Pet.from_dict(pet_data))
        return owner


class Scheduler:
    """Organizes, filters, and manages pet care tasks across pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_all_tasks(self, include_completed: bool = True) -> List[Tuple[Pet, Task]]:
        """Return all tasks from the owner's pets."""
        return self.owner.get_all_tasks(include_completed=include_completed)

    def sort_by_time(
        self, tasks: Optional[List[Tuple[Pet, Task]]] = None
    ) -> List[Tuple[Pet, Task]]:
        """Return tasks sorted by due date and time."""
        tasks = tasks if tasks is not None else self.get_all_tasks()
        return sorted(tasks, key=lambda item: item[1].sort_key())

    def sort_by_priority_then_time(
        self, tasks: Optional[List[Tuple[Pet, Task]]] = None
    ) -> List[Tuple[Pet, Task]]:
        """Return tasks sorted by priority first, then by time."""
        tasks = tasks if tasks is not None else self.get_all_tasks()
        return sorted(tasks, key=lambda item: (item[1].priority_rank(), item[1].sort_key()))

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        due_date: Optional[date] = None,
        priority: Optional[str] = None,
    ) -> List[Tuple[Pet, Task]]:
        """Filter tasks by pet name, completion status, due date, and/or priority."""
        tasks = self.get_all_tasks()

        if pet_name is not None:
            tasks = [
                (pet, task) for pet, task in tasks if pet.name.lower() == pet_name.lower()
            ]

        if completed is not None:
            tasks = [(pet, task) for pet, task in tasks if task.completed == completed]

        if due_date is not None:
            tasks = [(pet, task) for pet, task in tasks if task.due_date == due_date]

        if priority is not None:
            tasks = [
                (pet, task) for pet, task in tasks if task.priority == priority.lower()
            ]

        return tasks

    def mark_task_complete(
        self,
        pet_name: str,
        description: str,
        time_str: str,
        due_date: Optional[date] = None,
    ) -> bool:
        """Mark a matching task complete and create the next recurring task if needed."""
        due_date = due_date or date.today()
        pet = self.owner.get_pet(pet_name)

        if pet is None:
            return False

        for task in pet.tasks:
            if (
                task.description.lower() == description.lower()
                and task.time_str == time_str
                and task.due_date == due_date
                and not task.completed
            ):
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return True

        return False

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for tasks scheduled at the same exact date and time."""
        tasks = self.sort_by_time()
        conflicts: List[str] = []

        for i in range(len(tasks)):
            pet_a, task_a = tasks[i]
            for j in range(i + 1, len(tasks)):
                pet_b, task_b = tasks[j]

                if (
                    task_a.due_date == task_b.due_date
                    and task_a.time_str == task_b.time_str
                ):
                    conflicts.append(
                        f"Conflict: {pet_a.name} and {pet_b.name} both have tasks at "
                        f"{task_a.time_str} on {task_a.due_date.isoformat()}."
                    )

        return conflicts

    def todays_schedule(self) -> List[Tuple[Pet, Task]]:
        """Return today's tasks sorted by time."""
        today_tasks = self.filter_tasks(due_date=date.today())
        return self.sort_by_time(today_tasks)

    def next_available_slot(
        self,
        due_date: Optional[date] = None,
        start_hour: int = 6,
        end_hour: int = 22,
        interval_minutes: int = 30,
    ) -> Optional[str]:
        """Return the next unused time slot on a given date using exact task times."""
        due_date = due_date or date.today()
        occupied = {
            task.time_str
            for _, task in self.filter_tasks(due_date=due_date, completed=False)
        }

        current = datetime.combine(due_date, time(hour=start_hour, minute=0))
        end_time = datetime.combine(due_date, time(hour=end_hour, minute=0))

        while current <= end_time:
            slot = current.strftime("%H:%M")
            if slot not in occupied:
                return slot
            current += timedelta(minutes=interval_minutes)

        return None