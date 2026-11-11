# Design review

Student: Ho Thi Minh Ngan
Student ID: V202603134
AI tool/model, or "manual": Claude Code (Claude Opus 5.5)

Write at most 200 words total. Refer to requirements, code or test assertions.

1. **Architecture:** Defend one application deployable and one database for
   this team. Give one cost and one potential benefit of a microservice split.

   Answer: One small team, one release cadence: a modular monolith keeps
   save-then-notify in one process and one transaction, with module boundaries
   enforced by `TaskRepository`/`NotificationChannel`. A split costs network
   failures and distributed consistency; it could let notification scale and
   deploy independently.

2. **Patterns:** What does Strategy vary? What does Decorator add? Why is
   Observer optional while notification is the only reaction?

   Answer: Strategy varies delivery (`email`, `sms`, `push`) selected by
   registration (R5). Decorator adds an acceptance record around an existing
   channel, keeping the same interface (R7). Observer only pays off with
   several independent subscribers; one reaction needs no event bus.

3. **Changed requirement R6:** What must be written atomically? Who relays it?
   Why can duplicates occur? State one condition needed for eventual acceptance.

   Answer: The task update and an outbox row commit in one transaction. A relay
   worker polls pending rows, sends, then marks them done. If it crashes after
   provider acceptance but before marking, it resends: at-least-once. Eventual
   acceptance needs retries until success (provider idempotency keys limit duplicates).

4. **Independent evidence:** Name one assertion you inspected and its matching
   sequence message or branch. What remains unverified by the offline tests?

   Answer: `assertEqual(email.attempts, 0)` matches the SaveError branch with
   no send. Real commit durability, provider behaviour and crash recovery remain unverified.
