# Submission Version Log

## v1

Generated draft and repository scaffold.

## v2

Initial hardening pass.

## v3

ICLR-main gate archive. Decision: KILL_ARCHIVE because evidence was synthetic/template-only.

## v4

Paper-specific topology-change evidence rebuild. Added deterministic NumPy benchmark, strong baselines, ablations, stress sweep, pairwise seed tests, generated figures, LaTeX tables, failure cases, rewritten docs, and a new manuscript. Decision changed to STRONG_REVISE because the local mechanism is supported, while submission readiness remains blocked by missing external robotics validation.

## v4.1

- Added a pre-execution ICLR-main submission-readiness plan for Paper 101.
- Reran `python src/run_experiment.py` on 2026-06-15 with thread caps and saved the continuation log.
- Reconfirmed CSV coverage: 45 metric rows, 1,575 per-task/family rows, 11,025 seed/task/family rows, 315 seed/split rows, 8 pairwise rows, 7 ablation rows, 49 ablation seed rows, 1,715 ablation task/family/seed rows, 54 stress-sweep rows, 378 stress-sweep seed rows, and 8 failure cases.
- Evidence outcome unchanged: proposed method beats `topological_slam_tamp` on combined-stress success (0.677 vs 0.564), improves invalid-plan/collision/support safety, improves topology F1 and latency, wins the paired seed gate, and survives core ablations.
- Terminal decision: STRONG_REVISE, still not ICLR-main ready without external robot or benchmark validation.
