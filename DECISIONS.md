# Design review

Student: Ho Thi Minh Ngan
Student ID: V202603134
AI tool/model, or "manual": Claude Code (Claude Opus 5.5)

Write at most 200 words total. Refer to requirements, code or test assertions.

1. **Architecture:** Defend one application deployable and one database for
   this team. Give one cost and one potential benefit of a microservice split.

   Answer: This project has one developer, one release and one database, so I
   chose a modular monolith. Saving and notifying stay in one process, and the
   `TaskRepository` and `NotificationChannel` interfaces keep the modules
   separate. A microservice split would add network failures and cross-service
   consistency work, although it could let notification scale and deploy independently.

2. **Patterns:** What does Strategy vary? What does Decorator add? Why is
   Observer optional while notification is the only reaction?

   Answer: Strategy varies the delivery method (`email`, `sms`, `push`), which is
   selected through registration (R5). Decorator adds an acceptance record around
   an existing channel while keeping its `send` contract (R7). In my view,
   Observer is only worthwhile when several independent subscribers react, so a
   single notification can remain a direct call.

3. **Changed requirement R6:** What must be written atomically? Who relays it?
   Why can duplicates occur? State one condition needed for eventual acceptance.

   Answer: The task update and an outbox row must be committed in one transaction.
   A relay worker then reads pending rows, sends them and marks them as done. If
   the relay crashes after the provider accepts a message but before marking it,
   the message is sent again, so delivery is at least once. Eventual acceptance
   requires the relay to keep retrying until the provider accepts.

4. **Independent evidence:** Name one assertion you inspected and its matching
   sequence message or branch. What remains unverified by the offline tests?

   Answer: I inspected `assertEqual(email.attempts, 0)`, which matches the
   `SaveError` branch with no send. The offline tests do not verify real commit
   durability, provider behavior or crash recovery.
