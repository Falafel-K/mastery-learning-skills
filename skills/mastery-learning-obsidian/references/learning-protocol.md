# Learning Protocol

Read this file at the start of every learning session.

## 1. Establish the learning contract

Infer what is already known from the user's request and supplied material. Ask only for missing information that changes the workflow:

- the topic or outcome the learner wants;
- whether the material is primary source material or only a pointer;
- current level when it is not observable;
- whether the learner wants a Vault-backed record;
- deadlines, assessment format, or capstone constraints if explicitly relevant.

Default goal when none is provided:

> The learner should explain the material in their own words, distinguish it from similar concepts, apply it, detect errors, and transfer it to a new context.

Do not turn setup into an interview that delays the first useful lesson. Make a reasonable default, state it, and start with the smallest teachable unit.

## 1.5 Command Routing

When the user enters a slash command, execute the corresponding protocol motion:
- `/study [target]` (or `/learn [target]`): Proceed directly to Section 3 (Select the next objective) and Section 4 (Teach). If `[target]` is provided, locate it in the source or ledger and force it as the next objective.
- `/review [target]`: Skip new teaching. If `[target]` is provided (e.g. `K01`), immediately start a retrieval-practice review session for that specific point. If no target is provided, perform a review session for due points in the queue (Section 6, Practice design).
- `/audit`: Perform the coverage audit comparing the knowledge map (`02-知识点地图.md`) against raw sources, reporting any unmapped details or gaps.
- `/handoff`: Immediately execute Section 7 (Session closure) and write a compact handoff state block summarizing topics, scores, and active errors.
- `/sync`: Invoke the local python script `sync_course.py` with the appropriate action parameters to force a synchronization of vault documents.

## 2. Ingest and map material

### Source register

Assign stable IDs in order of receipt: `S1`, `S2`, and so on. Record source type and import date. Do not rewrite source text as if it were the original; preserve original material or a permitted extract in the source log.

### Knowledge points

A knowledge point `Kxx` is an assessable unit, not a paragraph heading. It must contain:

- a short name;
- at least one source anchor;
- prerequisite IDs or an explicit “none known” note;
- a learner outcome beginning with an observable verb;
- likely misconceptions;
- an assessment method;
- assignment or artifact evidence;
- a current status.

Use a dependency order rather than blindly following source order. Preserve the original source order in anchors so the learner can return to it.

### Coverage audit before teaching

Before declaring a source “covered,” check that every important claim, rule, formula, procedure, or code behavior is mapped to at least one `Kxx`. Minor prose examples may support a mapped point; do not inflate the map with trivial fragments.

## 3. Select the next objective

If the user initiated a command with a `[target]` parameter (e.g., `/study K03` or `/study "第2节"`):
1. Locate the requested knowledge point or section in the ledger, knowledge map, or raw source.
2. If it is a new/unmapped section, parse it and define it as a new `Kxx` point in the knowledge map.
3. Force it as the current active objective, bypassing the default priority queue.
4. Warn the user if there are missing/uncompleted prerequisite knowledge points, but proceed if they confirm.

Otherwise, follow the default priority order:

1. A due review for a weak or key point;
2. A blocked prerequisite;
3. The next dependency-ready unlearned point;
4. A requested capstone subtask that exposes a missing concept.

Select only one concept or one inseparable micro-cluster. If a concept requires more than a few minutes of explanation, split it into smaller points.

## 4. Teach with a controlled cognitive load

Teach in this order:

1. **Purpose:** What failure, question, or real task does this solve?
2. **Intuition:** Give a compact mental model, analogy, picture, or concrete situation.
3. **Formal statement:** Define symbols, operations, constraints, assumptions, and boundaries.
4. **Source callback:** Explain what the supplied material meant, including any hidden step.
5. **Worked example:** Demonstrate one simple complete instance and name why each step exists.
6. **One learner task:** Ask a single task that produces evidence.

Do not mix several new concepts inside one learner task. For difficult topics, alternate example → partial attempt → feedback → independent attempt.

## 5. Hint ladder

Use the least revealing support that can unlock progress:

1. **Metacognitive prompt:** “What are you trying to find? Which condition seems relevant?”
2. **Directional cue:** Point to one source term, condition, diagram feature, or test.
3. **Partial structure:** Supply the first step, a formula frame, test scaffold, or code signature.
4. **Faded example:** Solve a closely related part while leaving the critical step blank.
5. **Full worked example:** Use only after earlier support fails.
6. **Fresh verification:** After level 5, give a different task. The example does not earn mastery.

## 6. Practice design

Do not test the same fact in the same wording repeatedly. Vary one or more of:

- context or narrative;
- data values;
- representation (words, graph, equation, code, table, diagram);
- constraints;
- required explanation;
- error pattern;
- combination with a neighboring concept.

Each key knowledge point should eventually have evidence from at least four of these categories:

- **Recall:** explain in own words;
- **Discrimination:** distinguish from a near neighbor or reject a misconception;
- **Application:** solve a near-transfer task;
- **Transfer:** solve under changed context or representation;
- **Error repair:** locate and repair a flawed solution;
- **Synthesis:** combine with other points in a capstone, proof, design, experiment, or project.

## 7. Session closure

At a meaningful pause, state:

- what was actually evidenced;
- what remains uncertain;
- the next smallest action;
- due reviews and any generated flashcards;
- any files updated or previewed.

Do not write a full transcript. Record the durable state changes described in the Obsidian contract.

