from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}
CATEGORY_ICON = {
    "feeding": "🍽️",
    "walk": "🚶",
    "medication": "💊",
    "vet": "🩺",
    "grooming": "🛁",
    "play": "🎾",
    "general": "📌",
}


def print_schedule(title: str, tasks) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("No tasks found.")
        return

    header = f"{'Date':<12} {'Time':<6} {'Pet':<8} {'Task':<18} {'Priority':<8} {'Freq':<8} {'Status':<8}"
    print(header)
    print("-" * len(header))

    for pet, task in tasks:
        status = "Done" if task.completed else "Pending"
        priority = f"{PRIORITY_ICON[task.priority]} {task.priority.title()}"
        icon = CATEGORY_ICON.get(task.category, "📌")
        label = f"{icon} {task.description}"
        print(
            f"{task.due_date.isoformat():<12} {task.time_str:<6} {pet.name:<8} "
            f"{label:<18} {priority:<8} {task.frequency:<8} {status:<8}"
        )


def main() -> None:
    owner = Owner("Alex")

    luna = Pet("Luna", "Dog", 4)
    milo = Pet("Milo", "Cat", 2)

    owner.add_pet(luna)
    owner.add_pet(milo)

    today = date.today()

    luna.add_task(Task("Morning walk", "08:00", today, "daily", "high", False, "walk"))
    luna.add_task(Task("Medication", "18:00", today, "daily", "high", False, "medication"))
    milo.add_task(Task("Vet appointment", "10:30", today, "once", "high", False, "vet"))
    milo.add_task(Task("Brush fur", "07:30", today, "weekly", "medium", False, "grooming"))
    milo.add_task(Task("Feed dinner", "18:00", today, "daily", "high", False, "feeding"))

    scheduler = Scheduler(owner)

    print_schedule("Today's Schedule", scheduler.todays_schedule())
    print_schedule(
        "Priority View (Across All Pets)",
        scheduler.sort_by_priority_then_time(scheduler.filter_tasks(completed=False)),
    )

    print("\nConflict Warnings")
    print("-----------------")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"⚠️  {warning}")
    else:
        print("No conflicts detected.")

    next_slot = scheduler.next_available_slot(today)
    print("\nNext Available Slot")
    print("-------------------")
    print(next_slot or "No open slot found.")

    scheduler.mark_task_complete("Luna", "Morning walk", "08:00", today)

    print_schedule(
        "Incomplete Tasks for Luna",
        scheduler.sort_by_time(
            scheduler.filter_tasks(pet_name="Luna", completed=False)
        ),
    )


if __name__ == "__main__":
    main()