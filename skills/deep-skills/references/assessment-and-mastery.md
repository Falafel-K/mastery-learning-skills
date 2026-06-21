# Assessment and Mastery

Read this file before scoring, progressing, scheduling reviews, or repairing errors.

## 1. Mastery score

| Score | Meaning | Minimum evidence |
|---:|---|---|
| 0 | No usable understanding | Answer is absent, unrelated, or contradicts the core concept. |
| 1 | Recognition only | Repeats a term or source phrase but cannot explain it or use it. |
| 2 | Partial explanation | Explains some of the idea but misses a necessary condition, relation, boundary, or step. |
| 3 | Near application | Independently solves or explains a similar problem with no concept-breaking error. |
| 4 | Stable transfer | Handles a changed context and explains conditions, boundaries, and a likely misconception. |
| 5 | Integrative mastery | Combines related points, independently diagnoses an error, and justifies a solution/design under constraints. |

A prompt, hint, or full solution lowers the strength of evidence. Do not assign 3+ solely because the learner followed a supplied scaffold. The learner needs a fresh independent task.

## 2. Progression gate

- Score below 3: do not proceed to the next knowledge point.
- Score 3: may proceed, but place the point in the review queue.
- Score 4: mark stable, schedule spaced verification.
- Score 5: eligible for synthesis/capstone credit.
- Key points must reach 4.
- A unit or topic cannot be declared complete until the coverage audit passes and agreed integrative evidence reaches 5 or is explicitly deferred.

If the learner requests to skip a blocked point, give a short preview of why it matters, mark it `DEFERRED`, and continue only if dependencies permit. Do not convert a skip into mastery.

## 3. Six evidence types

### Recall
Ask for a self-contained explanation, not a source quotation. Strong recall includes purpose, a concrete example, and a boundary.

### Discrimination
Ask the learner to compare near concepts, select a valid condition, or explain why an attractive wrong claim fails.

### Application
Use the same underlying structure with unfamiliar values or wording.

### Transfer
Change context, representation, constraints, or combine a known idea with another point. Ask why the method still applies or does not.

### Error repair
Provide a flawed derivation, calculation, code fragment, experiment, or conclusion. The learner must locate the earliest meaningful error and repair it.

### Synthesis
Require several `Kxx` points in a coherent artifact: proof, model, program, test suite, experimental plan, design, or case analysis.

## 4. Feedback protocol

When the learner is wrong or incomplete, follow this order:

1. **Credit:** name the specific part that is sound.
2. **Smallest gap:** identify the first missing condition, false inference, or malformed step.
3. **Classify:** choose an error type.
4. **Repair:** provide the smallest useful explanation or hint.
5. **Re-check:** ask one fresh, smaller or equivalent task.
6. **Record:** log durable errors only when they affect the learner's model or future review.

Avoid generic praise, answer dumping, and “almost” when the error would invalidate a result.

## 5. Error taxonomy

Use one primary category and optional secondary categories:

- concept confusion;
- missing prerequisite;
- definition memorized but not understood;
- representation or symbol error;
- logical gap;
- arithmetic or algebraic slip;
- unit/dimension error;
- invalid condition or boundary;
- causal/mechanistic error;
- code implementation error;
- debugging strategy error;
- experimental design/control error;
- data interpretation error;
- overconfidence/calibration error.

## 6. Repeated failure and deferral

After one failed attempt, use a smaller cue. After two, check the prerequisite explicitly. After three unsuccessful attempts on the same point:

1. reduce scope;
2. return to the missing prerequisite or use a more concrete representation;
3. give a fully worked related example only if needed;
4. require a fresh task afterward;
5. mark the original point `DEFERRED` if it remains blocked;
6. never mark it mastered just to keep the session moving.

## 7. Calibration

For key points, occasionally ask the learner for a confidence estimate before answering, such as 0–100%. Record only meaningful mismatches between confidence and performance. The goal is to correct “familiarity feels like mastery,” not to penalize uncertainty.

## 8. Spaced review

If a local date is known, schedule from the last verified date:

| Score | Suggested checks |
|---:|---|
| 0–2 | next session; repair before new content |
| 3 | +1 day, +3 days, +7 days |
| 4 | +3 days, +7 days, +14 days |
| 5 | +7 days, +21 days, +45 days |

Use retrieval first. Do not count rereading as a successful review. A failed review lowers the practical state and returns the point to repair. If the review was initiated with a specific `[target]` (e.g., `/review K01`), immediately run a retrieval test on that target Kxx point even if it is not currently marked as due in the review queue.

When a knowledge point reaches score 3 or higher for the first time, generate at least one flashcard in the daily session note under `### 闪卡制作 (Spaced Repetition)`. Flashcards must use the standard Obsidian Spaced Repetition syntax:
- Format: `Question :: Answer #flashcard/主题` (use a slugified or space-replaced name for the topic tag).
- Questions should target retrieval of definitions, conditions, boundaries, or diagnostic symptoms.

