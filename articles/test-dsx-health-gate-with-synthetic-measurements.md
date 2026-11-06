# Test a DSX health gate with example measurements

Health Validation's Go catalog returned overall PASS even though a required CPU assessment was missing. The application needs two assessed PASS results before it can continue: one from the CPU-count check, which compares possible and online CPUs, and one from an example assessment check that reports UNKNOWN when an assessment is unavailable.

In the missing-input scenario, the assessment check passes, but the CPU check is skipped as `SENSOR_MISSING`. A regression test sends that verdict to two callers. The unsafe reference trusts overall severity and continues once; the application's caller continues zero times. The test checks both counts.

The difference comes from the caller's policy. [The catalog aggregates checks that ran and excludes skips](https://github.com/dsx-ai-factory/health-validation/blob/f2d5e95af380ee17bcb8db84b4b2c03481d03a1d/catalog/health/verdict.go#L99-L140). It is behaving as designed; overall PASS does not show that every required check ran. Example measurements let you test this distinction through the real catalog without hardware.

## Run the example

The [example and tests](https://github.com/tridev-tej/health-validation/tree/4a709fcbbd6b893a46a19f675c7958c5a8faaff0) are in `catalog/examples/synthetic-health-gate/`. The contribution is proposed in [Health Validation PR #265](https://github.com/dsx-ai-factory/health-validation/pull/265).

You need Git, a shell and a writable `/tmp`. Use Go 1.27.3 on your `PATH` for the `go build` and `go test` commands. For the Bazel commands, use Bazelisk or Bazel 9.2.0. Bazel downloads the Go SDK version declared in `go.mod`, so those commands work without a separate Go installation.

Keep the repository's `go.mod` and `go.sum`. The first build needs access to the module dependencies. No GPU, NVIDIA driver, NVML or Linux sysfs is needed for this catalog-only example.

Clone and pin the tested revision:

```sh
git clone https://github.com/tridev-tej/health-validation.git
cd health-validation
git checkout --detach 4a709fcbbd6b893a46a19f675c7958c5a8faaff0
```

From that checkout:

```sh
go build -o /tmp/synthetic-health-gate ./catalog/examples/synthetic-health-gate
/tmp/synthetic-health-gate -scenario pass
/tmp/synthetic-health-gate -scenario critical
/tmp/synthetic-health-gate -scenario unknown
/tmp/synthetic-health-gate -scenario missing
/tmp/synthetic-health-gate -scenario disabled
/tmp/synthetic-health-gate -scenario collection-error
/tmp/synthetic-health-gate -scenario empty
```

Each scenario writes a `health.NodeVerdict` as JSON to stdout. Diagnostics and the harmless `continued synthetic workload` marker go to stderr. You must pass `-scenario`; an unrecognized value fails rather than selecting another case.

Built with Go 1.27.3 on Linux amd64, the executable produced the results below. Each Exit value is the executable's process status.

| Scenario | Observed result and caller action |
| --- | --- |
| `pass` | **Assessed:** CPU PASS; assessment PASS. **Skips:** None. **Overall:** PASS. **Exit:** 0. **Continuations:** 1. |
| `critical` | **Assessed:** CPU CRITICAL; assessment PASS. **Skips:** None. **Overall:** CRITICAL. **Exit:** 1. **Continuations:** 0. |
| `unknown` | **Assessed:** CPU PASS; assessment UNKNOWN. **Skips:** None. **Overall:** UNKNOWN. **Exit:** 1. **Continuations:** 0. |
| `missing` | **Assessed:** Assessment PASS. **Skips:** CPU `SENSOR_MISSING`. **Overall:** PASS. **Exit:** 1. **Continuations:** 0. |
| `disabled` | **Assessed:** Assessment PASS. **Skips:** CPU `CHECK_DISABLED`. **Overall:** PASS. **Exit:** 1. **Continuations:** 0. |
| `collection-error` | **Assessed:** CPU CRITICAL; assessment PASS. **Skips:** None. **Overall:** CRITICAL. **Exit:** 1. **Continuations:** 0. |
| `empty` | **Assessed:** None (`check_results: null`). **Skips:** Both `SENSOR_MISSING`. **Overall:** PASS. **Exit:** 1. **Continuations:** 0. |

For `-scenario typo`, it exited 2, printed a diagnostic to stderr, left stdout empty and never continued. Use the built executable to check exit statuses; `go run` or a build-system wrapper can report a different status.

## Why PASS does not mean complete

These are selected fields from the `missing` run's JSON:

```json
{
  "schema_version": "0.4",
  "catalog_version": "v0.0.0-20261103095631-4a709fcbbd6b",
  "overall_severity": "PASS",
  "check_results": [
    {
      "check_id": "synthetic_assessment",
      "severity": "PASS"
    }
  ],
  "skipped_checks": [
    {
      "check_id": "cpu_count",
      "severity": "PASS",
      "skipped": true,
      "skip_reason": "SENSOR_MISSING"
    }
  ]
}
```

That skipped record's `severity: PASS` does not mean the CPU was assessed. Missing input and disabled checks do not raise overall severity here. With no measurements at all, both checks are skipped and the overall result is still PASS.

## Feed measurements through the catalog

The program imports `catalog`, `catalog/cpu`, and `catalog/health` from `github.com/dsx-ai-factory/health-validation`. In [`newCatalog`](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/catalog/examples/synthetic-health-gate/main.go#L78-L90), `catalog.NewEmpty` starts a catalog with architecture `synthetic`, execution context `health.OperatorInfra` and the scenario's disabled checks. The program registers only `cpu.CPUCount()` and the assessment check.

The example uses `synthetic` as the catalog's architecture label; it does not detect hardware. The passing fixture supplies eight possible CPUs, eight online CPUs and `AssessmentAvailable: true`. `EvaluateAll` turns those Go measurements into a verdict. The example then sets only the verdict's optional `node_id` to `synthetic-node`.

The existing [`cpu.CPUCount()` check](https://github.com/dsx-ai-factory/health-validation/blob/f2d5e95af380ee17bcb8db84b4b2c03481d03a1d/catalog/cpu/cpu_count.go#L10-L38) reports CRITICAL when possible and online counts differ. That's why the `critical` scenario supplies seven online CPUs. Matching counts still do not prove collection worked; zero and zero match too.

The assessment check is named `synthetic_assessment` and marked `health.Private` and `health.Experimental`. Its Common Expression Language rule, `assessment_available == false`, produces `health.Unknown`. In the `unknown` scenario, the flag is present and false. This UNKNOWN comes from evaluation, rather than a missing input. The output carries `nvidia_endorsed: false`; the built-in CPU check keeps its original endorsement.

Missing input produces a skip. In `collection-error`, `cpu.ErroredCPU` instead produces CRITICAL and a `check_collection` recommendation. The program reports recommendations without executing remediation. If evaluation fails, for example on an invalid expression or duplicate host-wide measurements, it returns an error without a verdict.

## Require coverage before accepting PASS

Before it accepts a verdict, the caller checks three things: schema version is exactly `0.4`, catalog version is nonempty, and every numeric severity is supported.

It then requires one assessed result for each of two checks: `cpu_count` in category `cpu` (`health.CPU`), and `synthetic_assessment` in category `node` (`health.Node`). A missing, duplicate or unexpected ID stops the caller, as does a wrong category, any skipped check or a skip marker on a result. UNKNOWN is a valid severity; an unexpected check ID is a coverage problem.

The required set stays fixed regardless of which checks were registered or ran. Otherwise, an empty or narrowed registry could lower the application's requirements. [`completeCoverage`](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/catalog/examples/synthetic-health-gate/main.go#L138-L157) checks against that fixed set:

```go
func completeCoverage(verdict health.NodeVerdict) bool {
	required := map[string]health.Category{
		"cpu_count":            health.CPU,
		"synthetic_assessment": health.Node,
	}
	if len(verdict.SkippedChecks) != 0 || len(verdict.CheckResults) != len(required) {
		return false
	}
	seen := make(map[string]bool)
	for _, result := range verdict.CheckResults {
		category, expected := required[result.CheckID]
		if !expected || result.Category != category || result.Skipped ||
			result.SkipReason != health.NotSkipped ||
			seen[result.CheckID] {
			return false
		}
		seen[result.CheckID] = true
	}
	return true
}
```

The next step is severity. [`decide`](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/catalog/examples/synthetic-health-gate/main.go#L159-L171) takes the worst severity across the overall result and each check. Only PASS allows the application to continue:

```go
func decide(verdict health.NodeVerdict) (decision, error) {
	if err := validateContract(verdict); err != nil {
		return decision{}, err
	}
	if !completeCoverage(verdict) {
		return decision{reason: "coverage"}, nil
	}
	worst := verdict.OverallSeverity
	for _, result := range verdict.CheckResults {
		worst = health.Worse(worst, result.Severity)
	}
	return decision{reason: worst.String(), proceed: worst == health.Pass}, nil
}
```

So an overall PASS cannot hide a worse per-check result. INFO and WARNING also stop this caller. The library ranks UNKNOWN above CRITICAL.

The [upstream operator CLI](https://github.com/dsx-ai-factory/health-validation/blob/f2d5e95af380ee17bcb8db84b4b2c03481d03a1d/README.md#L170-L200) uses a different policy: it exits 0 for PASS, INFO or WARNING. Here both checks are mandatory, so any skip stops continuation. Other applications may handle the stock catalog's architecture and cadence skips differently.

## Write the verdict before continuing

[`consume`](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/catalog/examples/synthetic-health-gate/main.go#L173-L187) then writes the JSON before it calls the continuation:

```go
func consume(verdict health.NodeVerdict, output io.Writer, next func() error) (decision, error) {
	outcome, err := decide(verdict)
	if err != nil {
		return outcome, err
	}
	if err := json.NewEncoder(output).Encode(verdict); err != nil {
		return outcome, fmt.Errorf("write verdict: %w", err)
	}
	if outcome.proceed {
		if err := next(); err != nil {
			return outcome, fmt.Errorf("continue: %w", err)
		}
	}
	return outcome, nil
}
```

The order is evaluate, decide, write JSON, then branch. A supported verdict still gets written when the caller decides to stop.

If the writer returns an error, `consume` does not call the continuation, though stdout may already contain partial JSON. An error from `next` comes after valid JSON has been written. Neither path retries. Evaluation and verdict validation errors occur before output.

## Test and build the example

The continuation recorder decodes the already-written JSON and checks EOF when `consume` calls it. That tests the write-before-continue order. The missing-CPU regression verifies one continuation from the unsafe reference and none from the actual caller. Separate Go fixtures cover INFO/WARNING and malformed verdicts; they are not extra evaluator scenarios.

Serialization tests look for required keys, string enums, typed fields, check identities and exactly one JSON document followed by EOF.

Run the example suite and catalog tests from the repository root:

```sh
go test -count=1 -v ./catalog/examples/synthetic-health-gate
go test -count=1 ./catalog/...
```

Bazel is the repository's canonical build and test system. [Use Bazelisk or pinned Bazel](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/CONTRIBUTING.md#L54-L56), currently [9.2.0](https://github.com/tridev-tej/health-validation/blob/4a709fcbbd6b893a46a19f675c7958c5a8faaff0/.bazelversion), for these targets:

```sh
bazel build //catalog/examples/synthetic-health-gate
bazel test --config=ci //catalog/examples/synthetic-health-gate:synthetic-health-gate_test
bazel run //catalog/examples/synthetic-health-gate -- -scenario pass
```

Local Linux CI passed all 62 test targets, with 5 executed and 57 served from cache. Formatting, Gazelle and module tidy checks also passed.

## Boundaries

### Go checks and build identity

The caller works with a Go verdict in the same process. It does not ingest external JSON or perform full [JSON Schema instance validation](https://github.com/dsx-ai-factory/health-validation/blob/f2d5e95af380ee17bcb8db84b4b2c03481d03a1d/catalog/health/node-verdict.schema.json).

The JSON keeps the library's fields and recommendations. `catalog_version` tells you which library build produced it; it does not fingerprint the assessment check or imply a public release. Build versions, timestamps and trace/span IDs can vary.

These scenarios exercise the caller's decision at a point in time. They do not establish real hardware health, node readiness, production safety, fleet behavior, performance or success of a whole workload.

### Output, exit status and delivery

The program exits 2 when it handles a returned error. Signals can produce a different status, and exit 2 does not guarantee empty stdout. On Unix, a broken stdout or stderr pipe may terminate the process with [SIGPIPE](https://pkg.go.dev/os/signal#hdr-SIGPIPE) before the error handler runs.

Writing the verdict successfully does not confirm that a downstream consumer acknowledged it or that it was stored durably.

For your own integration, define the required checks independently of registration. Then remove one required measurement in a test and check that the real continuation stays uncalled even when the catalog returns overall PASS.

> © 2026 NVIDIA Corporation. All rights reserved. NVIDIA, the NVIDIA logo, and other NVIDIA product and service names are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries and regions. Other company, product, and service names may be trademarks of their respective owners.
