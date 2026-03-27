from __future__ import annotations

from datetime import date
from pathlib import Path

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


DATA_FILE = "pawpal_data.json"
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


def load_owner() -> Owner:
    """Load saved app data or create a fresh owner."""
    if Path(DATA_FILE).exists():
        return Owner.load_from_json(DATA_FILE)
    return Owner("Jordan")


def save_owner() -> None:
    """Save the in-memory owner object to disk."""
    st.session_state.owner.save_to_json(DATA_FILE)


def schedule_rows(tasks):
    """Convert scheduler output to table rows for Streamlit."""
    rows = []
    for pet, task in tasks:
        rows.append(
            {
                "Date": task.due_date.isoformat(),
                "Time": task.time_str,
                "Pet": pet.name,
                "Task": f"{CATEGORY_ICON.get(task.category, '📌')} {task.description}",
                "Priority": f"{PRIORITY_ICON[task.priority]} {task.priority.title()}",
                "Frequency": task.frequency.title(),
                "Status": "✅ Done" if task.completed else "⏳ Pending",
            }
        )
    return rows


def task_option_label(item):
    """Create a readable selectbox label for a task tuple."""
    pet, task = item
    return (
        f"{pet.name} | {task.due_date.isoformat()} {task.time_str} | "
        f"{task.description} | {task.frequency}"
    )


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

if "owner" not in st.session_state:
    st.session_state.owner = load_owner()
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.title("🐾 PawPal+")
st.caption(
    "A multi-pet care scheduler with sorting, filtering, conflict warnings, recurrence, and JSON save/load."
)

with st.sidebar:
    st.header("Data")
    st.write(f"Saved file: `{DATA_FILE}`")
    if st.button("Save now"):
        save_owner()
        st.success("Saved to pawpal_data.json")
    if st.button("Reset all demo data"):
        st.session_state.owner = Owner("Jordan")
        st.session_state.scheduler = Scheduler(st.session_state.owner)
        if Path(DATA_FILE).exists():
            Path(DATA_FILE).unlink()
        st.rerun()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name
    save_owner()

col_a, col_b = st.columns([1, 2])

with col_a:
    st.markdown("### Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
        age = st.number_input("Age", min_value=0, max_value=40, value=1, step=1)
        add_pet_clicked = st.form_submit_button("Add pet")

        if add_pet_clicked:
            if not pet_name.strip():
                st.error("Enter a pet name.")
            elif owner.get_pet(pet_name.strip()) is not None:
                st.error("A pet with that name already exists.")
            else:
                owner.add_pet(Pet(pet_name.strip(), species, int(age)))
                save_owner()
                st.success(f"Added {pet_name.strip()}.")
                st.rerun()

    st.markdown("### Current Pets")
    if owner.pets:
        st.table(
            [
                {"Name": pet.name, "Species": pet.species, "Age": pet.age, "Tasks": len(pet.tasks)}
                for pet in owner.pets
            ]
        )
    else:
        st.info("No pets yet. Add one to begin.")

with col_b:
    st.markdown("### Schedule a Task")
    if owner.pets:
        with st.form("add_task_form", clear_on_submit=True):
            selected_pet = st.selectbox("Choose pet", [pet.name for pet in owner.pets])
            description = st.text_input("Task description")
            due_date = st.date_input("Due date", value=date.today())
            time_str = st.text_input("Time (HH:MM)", value="08:00")
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
            priority = st.selectbox("Priority", ["high", "medium", "low"])
            category = st.selectbox(
                "Category",
                ["feeding", "walk", "medication", "vet", "grooming", "play", "general"],
            )
            add_task_clicked = st.form_submit_button("Add task")

            if add_task_clicked:
                pet = owner.get_pet(selected_pet)
                if pet is None:
                    st.error("Select a valid pet.")
                elif not description.strip():
                    st.error("Enter a task description.")
                else:
                    try:
                        pet.add_task(
                            Task(
                                description=description.strip(),
                                time_str=time_str,
                                due_date=due_date,
                                frequency=frequency,
                                priority=priority,
                                category=category,
                            )
                        )
                    except ValueError:
                        st.error("Time must use 24-hour HH:MM format, such as 08:30.")
                    else:
                        save_owner()
                        st.success(f"Added task for {selected_pet}.")
                        st.rerun()
    else:
        st.info("Add a pet first so tasks have somewhere to go.")

st.divider()
st.subheader("Today’s Schedule")

todays_tasks = scheduler.todays_schedule()
if todays_tasks:
    st.table(schedule_rows(todays_tasks))
else:
    st.info("No tasks scheduled for today.")

conflicts = scheduler.detect_conflicts()
if conflicts:
    st.markdown("### Conflict Warnings")
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No scheduling conflicts detected.")

next_slot = scheduler.next_available_slot()
if next_slot:
    st.info(f"Next available exact slot today: {next_slot}")

st.divider()
st.subheader("Filter Tasks")

filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    pet_filter = st.selectbox("Pet filter", ["All pets"] + [pet.name for pet in owner.pets])
with filter_col2:
    status_filter = st.selectbox("Status filter", ["All", "Pending", "Completed"])
with filter_col3:
    priority_filter = st.selectbox("Priority filter", ["All", "high", "medium", "low"])

completed_filter = None
if status_filter == "Pending":
    completed_filter = False
elif status_filter == "Completed":
    completed_filter = True

filtered_tasks = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All pets" else pet_filter,
    completed=completed_filter,
    priority=None if priority_filter == "All" else priority_filter,
)

if filtered_tasks:
    st.table(schedule_rows(scheduler.sort_by_priority_then_time(filtered_tasks)))
else:
    st.info("No tasks match the current filters.")

st.divider()
st.subheader("Mark a Task Complete")

incomplete_tasks = scheduler.sort_by_time(scheduler.filter_tasks(completed=False))

if incomplete_tasks:
    selected_task = st.selectbox(
        "Choose an incomplete task",
        incomplete_tasks,
        format_func=task_option_label,
    )
    if st.button("Mark selected task complete"):
        pet, task = selected_task
        was_updated = scheduler.mark_task_complete(
            pet.name,
            task.description,
            task.time_str,
            task.due_date,
        )
        if was_updated:
            save_owner()
            st.success("Task marked complete. Recurring tasks were advanced automatically if needed.")
            st.rerun()
        else:
            st.error("Task could not be updated.")
else:
    st.info("There are no incomplete tasks right now.")