from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_mark_complete_changes_status():
    task = Task("Feed breakfast", "07:30")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Luna", "Dog", 4)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "08:00"))
    assert len(pet.tasks) == 1


def test_sorting_returns_tasks_in_time_order():
    owner = Owner("Alex")
    pet = Pet("Luna", "Dog", 4)
    owner.add_pet(pet)

    pet.add_task(Task("Late task", "18:00"))
    pet.add_task(Task("Early task", "08:00"))
    pet.add_task(Task("Middle task", "12:00"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    descriptions = [task.description for _, task in sorted_tasks]
    assert descriptions == ["Early task", "Middle task", "Late task"]


def test_marking_daily_task_complete_creates_next_occurrence():
    owner = Owner("Alex")
    pet = Pet("Luna", "Dog", 4)
    owner.add_pet(pet)

    today = date.today()
    pet.add_task(Task("Medication", "09:00", today, "daily"))

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Luna", "Medication", "09:00", today)

    assert result is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].due_date == today + timedelta(days=1)
    assert pet.tasks[1].completed is False


def test_conflict_detection_flags_same_time_tasks():
    owner = Owner("Alex")
    luna = Pet("Luna", "Dog", 4)
    milo = Pet("Milo", "Cat", 2)
    owner.add_pet(luna)
    owner.add_pet(milo)

    today = date.today()
    luna.add_task(Task("Walk", "08:00", today))
    milo.add_task(Task("Feed", "08:00", today))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]