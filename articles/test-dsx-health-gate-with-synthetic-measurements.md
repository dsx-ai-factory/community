# A DSX health result can say PASS with a required check missing

Health Validation can return overall PASS even when a check your job needs didn't run. In the pinned Go catalog used here, [skipped checks are left out of the overall result](https://github.com/dsx-ai-factory/health-validation/blob/f2d5e95af380ee17bcb8db84b4b2c03481d03a1d/catalog/health/verdict.go#L99-L140). If the checks that ran pass, a missing CPU check leaves the summary at PASS.

The caller in this example requires both a CPU-count check and an example assessment check to run and pass before work starts. You can test this rule with example measurements, without reading hardware.

## The same PASS, two different decisions

The example registers the built-in CPU-count check and a private, experimental assessment check. The example assessment is not NVIDIA-endorsed.

These results come from the 3 November 2026 GST run of [revision `4a709fc`](https://github.com/tridev-tej/health-validation/tree/4a709fcbbd6b893a46a19f675c7958c5a8faaff0), built with Go 1.27.3 on Linux amd64. The missing case removes only the CPU measurement:

| Case | CPU check | Example check | Overall | Caller action |
| --- | --- | --- | --- | --- |
| Both required checks pass | PASS | PASS | PASS | Continue |
| CPU measurement missing | Skipped | PASS | PASS | Stop |

A PASS label on a skipped CPU record does not mean the CPU check ran. Only the example check contributes to overall PASS. The caller stops because the required CPU assessment is missing.

## Decide which checks your job needs

Keep the required checks independent of which checks were registered or ran. This caller expects:

- CPU-count check: `cpu_count`, category `cpu`.
- Example assessment: `synthetic_assessment`, category `node`.

The [coverage check](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/catalog/examples/synthetic-health-gate/main.go#L138-L157) requires exactly these checks, once each and in the right category. Both must actually be assessed; any skip stops the caller. Registering fewer checks doesn't change what the job needs.

Both assessed checks and the overall result must be PASS. Any other severity, including UNKNOWN, stops this caller. The [complete caller](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/catalog/examples/synthetic-health-gate/main.go#L106-L171) also checks the result format before applying this rule.

The [upstream operator CLI](https://github.com/dsx-ai-factory/health-validation/blob/f2d5e95af380ee17bcb8db84b4b2c03481d03a1d/README.md#L170-L200) uses a different policy: it exits 0 for PASS, INFO or WARNING. Here both checks are mandatory, so missing input, a disabled check or any other skip stops continuation. Other integrations can choose different required checks and skip policies.

## Try the two cases

The complete example and tests are in `catalog/examples/synthetic-health-gate/` at the pinned revision above. The contribution is proposed in [Health Validation PR #265](https://github.com/dsx-ai-factory/health-validation/pull/265).

You need Git, a shell, a writable `/tmp` and Go 1.27.3 on your `PATH`. Keep the repository's `go.mod` and `go.sum`; the first build needs access to module dependencies. This catalog-only example does not read hardware.

Clone the pinned source, run the example tests, then try the two cases. The `missing` case is expected to exit 1:

```sh
(
  git clone https://github.com/tridev-tej/health-validation.git || exit "$?"
  cd health-validation || exit "$?"
  git checkout --detach 4a709fcbbd6b893a46a19f675c7958c5a8faaff0 || exit "$?"
  go build -o /tmp/synthetic-health-gate ./catalog/examples/synthetic-health-gate || exit "$?"
  go test -count=1 -v ./catalog/examples/synthetic-health-gate || exit "$?"
  /tmp/synthetic-health-gate -scenario pass || exit "$?"
  printf 'pass exit: %s\n' "$?"
  missing_exit=0
  /tmp/synthetic-health-gate -scenario missing || missing_exit=$?
  printf 'missing exit: %s\n' "$missing_exit"
  test "$missing_exit" -eq 1
)
```

In the recorded run, `pass` exited 0 and `missing` exited 1. The program writes verdict JSON to stdout, with diagnostics and a harmless continuation marker on stderr. Check exit statuses on the built executable; a build-system wrapper can report a different status.

The caller works with a Go result inside one process; it doesn't validate external JSON. These cases test one decision at a point in time. They don't prove real hardware health, node readiness, production safety, fleet behavior, performance or success of a whole workload.

When adapting the example, remove one required measurement in a test. Verify that the actual continuation stays uncalled even when the catalog reports overall PASS.

> © 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
