# Submission Attack Log

Paper: 101 workspace_topology_change_detection

## Attack 1: No real robot validation

Verdict: still valid. This blocks ICLR-main readiness.

Action: mark STRONG_REVISE, not ready.

## Attack 2: No external benchmark

Verdict: still valid. The v5 local benchmark is large and targeted, but local evidence is not enough.

Action: require external manipulation/navigation validation before submission.

## Attack 3: Baselines are weak

Verdict: materially improved. v5 includes 15 methods, including topological SLAM/TAMP, graph-neural change classification, robust replanning, uncertainty-triggered replanning, conformal risk filtering, particle-filter belief MPC, dynamic scene-graph transformer proxy, neural TAMP, active view probing, v4 detector, and oracle.

Action: keep as STRONG_REVISE because the baselines are stronger, but most remain executable proxies rather than deployed systems.

## Attack 4: The method only improves diagnostics

Verdict: addressed locally. v5 improves closed-loop success, invalid-plan rate, collision/trap rate, support-failure rate, regret, fixed-risk behavior, and utility.

Action: keep closed-loop metrics central in the manuscript.

## Attack 5: Replanning cost or abstention might be hidden

Verdict: addressed locally but not on hardware. Replanning and risk behavior are included, and fixed-risk strict coverage is `1.00000`, so the win is not caused by abstention.

Action: report fixed-risk and still list real-time robot validation as missing.

## Attack 6: Ablations may not isolate topology

Verdict: addressed locally. Removing replan hysteresis, active probing, risk calibration, occlusion persistence, passage homology, support-edge memory, action conditioning, or replacing v5 with v4 reduces success or utility.

Action: preserve ablation table and avoid overstating causality beyond the local benchmark.

## Attack 7: Related work is incomplete

Verdict: still valid.

Action: require manual survey before submission.

## Terminal Action

STRONG_REVISE. Continue only with external experiments; do not submit this version to ICLR main.
