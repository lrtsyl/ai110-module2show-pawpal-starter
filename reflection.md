# PawPal+ Project Reflection

## 1. System Design

### a. Initial design

Three core actions I wanted the system to support were:

1. Add a pet and store its basic information.
2. Schedule pet care tasks such as feeding, walks, medications, grooming, and appointments.
3. View and manage an organized schedule across multiple pets.

My initial UML design used four classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

- `Task` was responsible for storing one care activity, including its description, date, time, recurrence, and completion status.
- `Pet` stored the pet's identifying information and its list of tasks.
- `Owner` stored the owner's name and the list of pets.
- `Scheduler` acted as the logic layer that pulled tasks from all pets and performed scheduling operations on them.

### b. Design changes

My design changed during implementation in two important ways.

First, I added a `priority` field and a `category` field to `Task`. This made the UI and CLI output easier to read and gave me a stronger algorithmic feature: sorting by priority and then time.

Second, I added JSON persistence methods to `Owner` so the Streamlit app could save and load pets and tasks between runs. That made the project feel more complete without changing the core class structure.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

My scheduler considers these main constraints:

- due date
- due time
- completion status
- pet name
- priority level
- recurrence pattern

For everyday use, I treated date and time as the primary scheduling constraints because the app is built around a calendar-like workflow. I treated priority as an additional useful layer so the system can also show which tasks matter most first.

### b. Tradeoffs

A major tradeoff in my scheduler is that conflict detection only checks for exact matching date and time values.

That is reasonable for this project because the `Task` model does not include a start/end range or duration-based overlap logic. Keeping conflict detection lightweight made the code easier to understand, test, and connect to the UI, while still giving the user a helpful warning when two tasks collide exactly.

Another tradeoff is that `next_available_slot()` looks for unused exact time slots rather than building a full optimization schedule. I kept that method simple because the assignment emphasized readable, testable algorithmic features over heavy optimization.

---

## 3. AI Collaboration

### a. How you used AI

I used AI to help with:

- brainstorming the class design
- turning the UML into Python class skeletons
- drafting and revising scheduler methods
- generating pytest ideas
- cleaning up the Streamlit integration
- improving documentation wording

The most helpful prompts were specific prompts tied to one task at a time, such as asking for a Mermaid class diagram, asking how a `Scheduler` should retrieve tasks from an `Owner`, or asking what the most important scheduler edge cases were for testing.

Using separate chats for design, algorithms, and testing helped me stay more organized because each conversation had a narrower goal.

### b. Judgment and verification

One AI suggestion I rejected was the idea of introducing extra architecture too early, such as separate notification-style or database-style classes before the core scheduler was stable.

I decided against that because the rubric was focused on `Owner`, `Pet`, `Task`, and `Scheduler`. I compared the suggestion against the assignment requirements, kept the class design smaller, and verified correctness by running the CLI demo and the pytest suite after each major change.

---

## 4. Testing and Verification

### a. What you tested

I tested these core behaviors:

- marking a task complete
- adding a task to a pet
- sorting tasks in chronological order
- creating the next occurrence for a daily recurring task
- detecting exact-time conflicts across pets
- sorting by priority
- saving and loading owner data through JSON

These tests mattered because they covered the most important behaviors promised by the backend and documented in the README.

### b. Confidence

I am confident that the core system works well for the intended use case.

The areas I would test next are:

- invalid time input edge cases
- duplicate pet names
- weekly recurrence edge cases
- cases with no tasks
- larger numbers of pets and tasks
- more advanced overlap detection if task durations were ever added

---

## 5. Reflection

### a. What went well

The strongest part of the project is the separation between the backend logic and the UI. Once the classes were clear, it became much easier to build the CLI demo, write tests, and then connect the same logic to Streamlit.

### b. What you would improve

If I had another iteration, I would improve the system by adding task editing and deletion directly in the UI, stronger validation messages, and a richer scheduling model that could reason about duration-based overlaps instead of exact-time matches only.

### c. Key takeaway

My biggest takeaway is that AI is most useful when I stay in charge of the architecture. It was very helpful for scaffolding, refactoring, and testing ideas, but the project only stayed coherent when I kept checking whether each suggestion actually matched the rubric, the UML, and the final implementation.

---

## 6. Prompt / Strategy Comparison

I compared two different AI prompting strategies while working on the scheduler.

### Strategy 1: broad prompt
Example style:
“Build the whole PawPal+ project with classes, scheduling logic, tests, README, and Streamlit.”

This approach was useful for quickly getting a rough draft, but the suggestions were often too broad. It sometimes mixed together different project ideas, introduced features that were outside the rubric, or produced files that did not stay fully aligned with each other.

### Strategy 2: narrow step-by-step prompts
Example style:
- “Write only the `Task`, `Pet`, `Owner`, and `Scheduler` classes to match this rubric.”
- “Now update only `main.py` so it demonstrates two pets and scheduler output.”
- “Now write pytest tests for sorting, recurrence, and conflict detection.”
- “Now revise the README so it matches the actual implementation.”

This strategy worked much better. The outputs were more accurate, easier to verify, and easier to keep consistent with the UML and rubric.

### Which strategy was better and why

The narrow, step-by-step prompting strategy was clearly more useful for this project.

It reduced contradictions between files, made debugging easier, and gave me more control over design decisions. It also made it easier to reject AI suggestions that added unnecessary complexity. The experience showed me that AI is more reliable when I use it to solve one clearly defined problem at a time instead of asking for the entire project in one prompt.