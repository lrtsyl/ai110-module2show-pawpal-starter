# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design used four classes: Task, Pet, Owner, and Scheduler.
- Task was responsible for storing the details of a single pet care activity, including title, duration, priority, preferred time, and completion status. Pet stored the pet's basic info and a list of tasks. Owner stored the owner's name and the total time available for pet care in a day. Scheduler handled the main logic for sorting tasks, choosing which tasks fit in the day, and explaining why the final schedule was chosen.

**b. Design changes**

- Yes, my design changed during implementation.
- At first, I only planned to store task title, duration, and priority. During implementation, I added a preferred_time attribute so the scheduler could make more structured choices when tasks had the same priority. This made the plan easier to explain and gave the app a clearer scheduling rule.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers four main constraints: the owner's available time, the priority of each task, the duration of each task, and the preferred time of day.
- I treated priority as the most important factor because essential pet care tasks like medication or feeding should happen before lower-priority tasks. After that, I used available time as the next major constraint because the owner may not have enough time to complete everything in one day.

**b. Tradeoffs**

- One tradeoff my scheduler makes is that it uses a greedy strategy. It selects the highest-priority tasks first until the time budget runs out.
- This is reasonable for the scenario because the app is meant to be simple, understandable, and useful for a busy pet owner. A more advanced optimization system might produce a different plan, but it would also be harder to explain and test.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI for design brainstorming, generating starter class structures, checking test ideas, and revising explanations in the reflection and README.
- The most helpful prompts were the ones that asked for step-by-step help, such as asking for class responsibilities, sample test cases, and how to connect a Python backend to Streamlit.

**b. Judgment and verification**

- One moment where I did not accept an AI suggestion as-is was when I reviewed the project scope and noticed that some ideas were more complex than the starter app required.
- I evaluated the suggestion by comparing it to the assignment requirements and simplifying the design so it stayed focused on priority, duration, time limits, and explainable scheduling. I also verified the logic by running tests.

---

## 4. Testing and Verification

**a. What you tested**

- I tested adding tasks to a pet, sorting tasks by priority, limiting the schedule to the owner's available minutes, and generating explanations for the final plan.
- These tests were important because they covered the most important behaviors of the scheduler and helped confirm that the app produced a valid daily plan.

**b. Confidence**

- I am fairly confident that the scheduler works correctly for the core use case.
- If I had more time, I would test more edge cases such as tasks with equal priorities, empty task lists, invalid durations, editing tasks, and more advanced tie-breaking rules.

---

## 5. Reflection

**a. What went well**

- The part I am most satisfied with is the separation of responsibilities between the classes. The backend logic stayed organized, and it was straightforward to connect it to the Streamlit interface.

**b. What you would improve**

- If I had another iteration, I would improve the scheduler by allowing task editing, saving data between sessions, and supporting more advanced planning rules such as deadlines or recurring tasks.

**c. Key takeaway**

- One important thing I learned is that a clear class design makes implementation much easier. I also learned that AI is most useful when I treat it as a collaborator and still verify whether its suggestions fit the actual project requirements.
