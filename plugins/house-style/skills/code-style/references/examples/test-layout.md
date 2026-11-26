<!-- Shared rules: regression and observable behavior, real integration boundaries
[GOOGLE-REVIEW]; deterministic isolated tests [GOOGLE-GO]; explicit dependencies
[CPP-CORE] [UBER-GO]; meaningful failure paths and honest coverage [OWASP]. -->

# Testing a reservation deadline

This language-neutral layout is pseudocode, not a runnable test suite. File suffixes
and assertion APIs belong to the consuming project's language and test runner.

The contract: a reservation may be redeemed strictly before its deadline. At the
deadline it fails with `Expired` and remains unused. A failed storage update must
surface as `StorageUnavailable`; it must never return success.

```text
src/reservations/                 redemption logic and repository interface
tests/unit/reservations/          deadline and failure contracts with local fakes
tests/integration/reservations/   real storage adapter with a temporary local store
```

Inject a clock and repository into the service. Each test gets a fresh repository,
literal fixture data, and a fixed clock; no live network, wall-clock wait, random
identifier, shared database, or ordering dependency is needed.

```text
test "the exact deadline rejects redemption without consuming the reservation":
  arrange:
    repository = fresh memory repository containing reservation "r-7"
      with expires_at_seconds = 120 and used = false
    service = redemption service(repository, fixed clock at 120 seconds)

  act:
    outcome = service.redeem("r-7")

  assert:
    outcome is Expired
    repository.read("r-7").used is false

test "a storage failure is observable and leaves the reservation unused":
  arrange:
    repository = fresh memory repository containing unused reservation "r-7"
      with expires_at_seconds = 120; saving fails before mutation
    service = redemption service(repository, fixed clock at 119 seconds)

  act:
    outcome = service.redeem("r-7")

  assert:
    outcome is StorageUnavailable
    repository.read("r-7").used is false
```

Add separate cases for success at 119 seconds, rejection at 121 seconds, and an
unknown reservation. Assert literal public outcomes and persisted state instead of
recomputing the service's deadline expression or checking private helper calls.
The exact-deadline case catches the regression where equality was accepted.

Use the real storage adapter to test persistence and rollback in a fresh temporary
local store, with cleanup on success and failure. A memory fake cannot establish
transaction guarantees. A production remote adapter also needs its own integration
check in an authorized environment; the local suite makes no claim about it.
Record that check as unavailable if it cannot run, keeping the required assertion
and check enabled. Report commands, outcomes, and limits with the change.
