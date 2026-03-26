# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Final Design

PawPal+ is a Streamlit app that helps a pet owner choose which pet care tasks to do in a day.

### Core classes

- `Task`: stores title, duration, priority, preferred time, and completion state
- `Pet`: stores pet info and its list of care tasks
- `Owner`: stores owner info and time available for the day
- `Scheduler`: sorts tasks, selects tasks that fit the time limit, and explains the schedule

## Scheduling Rules

The scheduler considers:

- task priority
- task duration
- preferred time of day
- total available time for the owner

Higher-priority tasks are selected first. If a task would exceed the owner's available time, it is skipped.

## Running the app

```bash
streamlit run app.py
```

## Running tests

```bash
python -m pytest
```