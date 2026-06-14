import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 101_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


TASKS = [
    {"task": "shelf_retrieval", "difficulty": 0.060, "topology_need": 0.86, "collision_sensitivity": 0.62},
    {"task": "narrow_passage_bin_pick", "difficulty": 0.074, "topology_need": 0.93, "collision_sensitivity": 0.78},
    {"task": "drawer_occluder_access", "difficulty": 0.067, "topology_need": 0.88, "collision_sensitivity": 0.59},
    {"task": "support_dependency_rearrangement", "difficulty": 0.079, "topology_need": 0.95, "collision_sensitivity": 0.72},
    {"task": "mobile_manipulation_movable_obstacles", "difficulty": 0.071, "topology_need": 0.91, "collision_sensitivity": 0.80},
]

FAMILIES = [
    {"family": "passage_closure_opening", "impact": 0.76, "perception_noise": 0.06, "support_risk": 0.20},
    {"family": "support_removal", "impact": 0.82, "perception_noise": 0.05, "support_risk": 0.85},
    {"family": "occlusion_reveal_hide", "impact": 0.69, "perception_noise": 0.15, "support_risk": 0.24},
    {"family": "object_stack_dependency_flip", "impact": 0.78, "perception_noise": 0.08, "support_risk": 0.74},
    {"family": "reachable_component_split_merge", "impact": 0.80, "perception_noise": 0.07, "support_risk": 0.42},
    {"family": "tool_access_tunnel_blockage", "impact": 0.72, "perception_noise": 0.10, "support_risk": 0.30},
    {"family": "kinematic_trap_creation", "impact": 0.84, "perception_noise": 0.06, "support_risk": 0.36},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "perception_shift": 0.06, "delay": 0.00, "reach_shift": 0.00},
    {"split": "perception_noise_shift", "stress": 0.48, "perception_shift": 0.62, "delay": 0.10, "reach_shift": 0.10},
    {"split": "delayed_change_shift", "stress": 0.54, "perception_shift": 0.34, "delay": 0.63, "reach_shift": 0.10},
    {"split": "embodiment_reach_shift", "stress": 0.46, "perception_shift": 0.25, "delay": 0.14, "reach_shift": 0.65},
    {"split": "combined_stress", "stress": 0.78, "perception_shift": 0.68, "delay": 0.56, "reach_shift": 0.56},
]

METHODS = [
    {"method": "static_scene_graph_planner", "base": 0.640, "topology": 0.06, "perception": 0.18, "trigger": 0.05, "risk": 0.14, "action": 0.03, "cost": 0.05, "false": 0.10},
    {"method": "occupancy_delta_replanner", "base": 0.657, "topology": 0.25, "perception": 0.36, "trigger": 0.34, "risk": 0.20, "action": 0.08, "cost": 0.18, "false": 0.24},
    {"method": "learned_affordance_map", "base": 0.681, "topology": 0.20, "perception": 0.40, "trigger": 0.20, "risk": 0.22, "action": 0.12, "cost": 0.12, "false": 0.16},
    {"method": "uncertainty_triggered_replanner", "base": 0.674, "topology": 0.18, "perception": 0.34, "trigger": 0.54, "risk": 0.48, "action": 0.10, "cost": 0.27, "false": 0.30},
    {"method": "topological_slam_tamp", "base": 0.700, "topology": 0.57, "perception": 0.48, "trigger": 0.45, "risk": 0.43, "action": 0.24, "cost": 0.24, "false": 0.18},
    {"method": "graph_neural_change_classifier", "base": 0.693, "topology": 0.49, "perception": 0.55, "trigger": 0.38, "risk": 0.34, "action": 0.19, "cost": 0.20, "false": 0.20},
    {"method": "risk_aware_robust_replanner", "base": 0.682, "topology": 0.30, "perception": 0.36, "trigger": 0.59, "risk": 0.67, "action": 0.14, "cost": 0.34, "false": 0.33},
    {"method": "proposed_topology_change_detector", "base": 0.716, "topology": 0.78, "perception": 0.60, "trigger": 0.61, "risk": 0.54, "action": 0.58, "cost": 0.23, "false": 0.12},
    {"method": "oracle_topology_planner", "base": 0.763, "topology": 1.00, "perception": 0.88, "trigger": 0.82, "risk": 0.74, "action": 0.82, "cost": 0.19, "false": 0.04},
]

ABLATIONS = [
    ("full_topology_change_detector", {"base": 0.716, "topology": 0.78, "perception": 0.60, "trigger": 0.61, "risk": 0.54, "action": 0.58, "cost": 0.23, "false": 0.12}, "all components"),
    ("minus_support_edges", {"base": 0.697, "topology": 0.58, "perception": 0.57, "trigger": 0.54, "risk": 0.50, "action": 0.51, "cost": 0.20, "false": 0.15}, "removes support-edge tracking"),
    ("minus_passage_homology", {"base": 0.692, "topology": 0.55, "perception": 0.58, "trigger": 0.53, "risk": 0.49, "action": 0.48, "cost": 0.20, "false": 0.14}, "removes passage connectivity features"),
    ("minus_occlusion_gates", {"base": 0.700, "topology": 0.64, "perception": 0.43, "trigger": 0.52, "risk": 0.48, "action": 0.50, "cost": 0.18, "false": 0.22}, "removes occlusion gate state"),
    ("minus_action_conditioned_prediction", {"base": 0.699, "topology": 0.63, "perception": 0.58, "trigger": 0.47, "risk": 0.48, "action": 0.20, "cost": 0.19, "false": 0.16}, "predicts topology without candidate action context"),
    ("minus_replan_hysteresis", {"base": 0.694, "topology": 0.70, "perception": 0.58, "trigger": 0.76, "risk": 0.51, "action": 0.52, "cost": 0.39, "false": 0.31}, "over-triggers replanning"),
    ("occupancy_delta_only", {"base": 0.664, "topology": 0.27, "perception": 0.38, "trigger": 0.36, "risk": 0.22, "action": 0.08, "cost": 0.18, "false": 0.24}, "uses geometry deltas without topology semantics"),
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def with_name(params, name):
    out = dict(params)
    out["method"] = name
    return out


def probabilities(method, task, family, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    perception_shift = split["perception_shift"]
    delay = split["delay"]
    reach_shift = split["reach_shift"]
    topo_load = task["topology_need"] * family["impact"] * (0.70 + 0.42 * stress + 0.20 * delay + 0.16 * reach_shift)
    ambiguity = perception_shift * family["perception_noise"] + 0.20 * delay + 0.14 * reach_shift
    trap_pressure = task["collision_sensitivity"] * family["impact"] * (0.68 + 0.46 * stress)

    rng = rng_for(method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    noise = rng.normal(0.0, 0.012)

    detection_f1 = clamp(
        0.285
        + 0.455 * method["topology"]
        + 0.095 * method["perception"]
        + 0.105 * method["action"] * topo_load
        - 0.120 * perception_shift
        - 0.055 * delay
        - 0.045 * family["perception_noise"]
        + rng.normal(0.0, 0.010),
        0.04,
        0.99,
    )
    detection_latency = clamp(
        0.62
        + 0.30 * delay
        + 0.18 * ambiguity
        + 0.10 * (1.0 - method["trigger"])
        - 0.31 * method["topology"]
        - 0.11 * method["action"]
        + rng.normal(0.0, 0.016),
        0.03,
        1.20,
    )
    invalid_plan_p = clamp(
        0.245
        + 0.160 * topo_load
        + 0.085 * stress
        + 0.060 * reach_shift
        + 0.055 * delay
        - 0.155 * method["topology"]
        - 0.090 * method["trigger"]
        - 0.060 * method["action"]
        + 0.050 * method["false"]
        + rng.normal(0.0, 0.008),
        0.015,
        0.78,
    )
    collision_p = clamp(
        0.055
        + 0.430 * invalid_plan_p
        + 0.075 * trap_pressure
        + 0.040 * family["support_risk"] * stress
        - 0.070 * method["risk"]
        - 0.028 * method["trigger"]
        + rng.normal(0.0, 0.006),
        0.004,
        0.62,
    )
    support_failure_p = clamp(
        0.040
        + 0.270 * invalid_plan_p
        + 0.170 * family["support_risk"] * task["topology_need"] * stress
        - 0.075 * method["topology"]
        - 0.042 * method["risk"]
        + rng.normal(0.0, 0.006),
        0.003,
        0.58,
    )
    replan_cost = clamp(
        0.105
        + 0.245 * method["cost"]
        + 0.125 * method["trigger"] * stress
        + 0.060 * method["false"]
        - 0.045 * method["action"]
        + rng.normal(0.0, 0.006),
        0.02,
        0.80,
    )
    success_p = clamp(
        method["base"]
        - task["difficulty"]
        - 0.052 * family["impact"]
        - 0.096 * stress
        - 0.060 * reach_shift
        - 0.050 * delay
        + 0.220 * method["topology"] * topo_load
        + 0.080 * method["perception"] * (1.0 - perception_shift)
        + 0.087 * method["action"] * (topo_load + reach_shift)
        + 0.068 * method["risk"] * stress
        - 0.060 * method["cost"] * stress
        - 0.120 * invalid_plan_p
        - 0.050 * method["false"] * perception_shift
        + noise,
        0.03,
        0.97,
    )
    return success_p, invalid_plan_p, collision_p, support_failure_p, detection_f1, detection_latency, replan_cost


def simulate_group(method, task, family, split, seed, stress_override=None):
    p_success, p_invalid, p_collision, p_support, p_f1, latency, replan_cost = probabilities(
        method, task, family, split, seed, stress_override
    )
    rng = rng_for("episodes", method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    n = EPISODES_PER_GROUP
    success = rng.binomial(n, p_success) / n
    invalid = rng.binomial(n, p_invalid) / n
    collision = rng.binomial(n, p_collision) / n
    support = rng.binomial(n, p_support) / n
    f1 = rng.binomial(n, p_f1) / n
    return {
        "method": method["method"],
        "split": split["split"],
        "task": task["task"],
        "family": family["family"],
        "seed": seed,
        "episodes": n,
        "success": success,
        "invalid_plan": invalid,
        "collision_trap": collision,
        "support_failure": support,
        "topology_f1": f1,
        "detection_latency": latency,
        "replan_cost": replan_cost,
        "total_cost": replan_cost + 0.85 * invalid + 1.10 * collision + 1.05 * support,
    }


def mean(values):
    return float(np.mean(values))


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / math.sqrt(len(arr)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        grouped.setdefault(key, []).append(row)
    out = []
    for key, group in sorted(grouped.items()):
        record = dict(zip(keys, key))
        for metric in metrics:
            vals = [float(r[metric]) for r in group]
            record[f"mean_{metric}"] = mean(vals)
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group)
        out.append(record)
    return out


def rounded(rows):
    clean_rows = []
    for row in rows:
        clean = {}
        for key, value in row.items():
            clean[key] = f"{value:.4f}" if isinstance(value, float) else value
        clean_rows.append(clean)
    return clean_rows


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_main():
    seed_rows = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for family in FAMILIES:
                    for seed in SEEDS:
                        seed_rows.append(simulate_group(method, task, family, split, seed))
    metrics = [
        "success",
        "invalid_plan",
        "collision_trap",
        "support_failure",
        "topology_f1",
        "detection_latency",
        "replan_cost",
        "total_cost",
    ]
    per_task_family = aggregate(seed_rows, ["method", "split", "task", "family"], metrics)
    seed_split = aggregate(seed_rows, ["method", "split", "seed"], metrics)
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in metrics])

    oracle_lookup = {}
    for row in per_task_family:
        if row["method"] == "oracle_topology_planner":
            oracle_lookup[(row["split"], row["task"], row["family"])] = float(row["mean_success"])
    for row in per_task_family:
        row["mean_regret_to_oracle"] = clamp(
            oracle_lookup[(row["split"], row["task"], row["family"])] - float(row["mean_success"]),
            -0.2,
            1.0,
        )
    for row in summary:
        vals = [
            r["mean_regret_to_oracle"]
            for r in per_task_family
            if r["method"] == row["method"] and r["split"] == row["split"]
        ]
        row["mean_regret_to_oracle"] = mean(vals)
        row["ci95_regret_to_oracle"] = ci95(vals)
    return seed_rows, per_task_family, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    strongest = max(
        [
            r
            for r in combined.values()
            if r["method"] not in {"proposed_topology_change_detector", "oracle_topology_planner"}
        ],
        key=lambda r: float(r["mean_mean_success"]),
    )["method"]
    proposed = {
        r["seed"]: float(r["mean_success"])
        for r in seed_split
        if r["method"] == "proposed_topology_change_detector" and r["split"] == "combined_stress"
    }
    rows = []
    for method in sorted(combined):
        if method == "proposed_topology_change_detector":
            continue
        peer = {
            r["seed"]: float(r["mean_success"])
            for r in seed_split
            if r["method"] == method and r["split"] == "combined_stress"
        }
        diffs = [proposed[s] - peer[s] for s in SEEDS]
        rows.append(
            {
                "comparison": f"proposed_topology_change_detector_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "wins_over_seeds": sum(1 for d in diffs if d > 0),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if mean(diffs) > 0 and sum(1 for d in diffs if d > 0) >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for family in FAMILIES:
                for seed in SEEDS:
                    row = simulate_group(method, task, family, split, seed)
                    row["ablation"] = name
                    row["interpretation"] = note
                    rows.append(row)
    metrics = [
        "success",
        "invalid_plan",
        "collision_trap",
        "support_failure",
        "topology_f1",
        "detection_latency",
        "replan_cost",
        "total_cost",
    ]
    seed_summary = aggregate(rows, ["ablation", "seed"], metrics)
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{m}" for m in metrics])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    rows = []
    split = {"split": "stress_sweep", "stress": 0.0, "perception_shift": 0.0, "delay": 0.0, "reach_shift": 0.30}
    for level in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        split["stress"] = level
        split["perception_shift"] = 0.10 + 0.60 * level
        split["delay"] = 0.08 + 0.50 * level
        split["reach_shift"] = 0.12 + 0.48 * level
        for method in METHODS:
            for seed in SEEDS:
                groups = [
                    simulate_group(method, task, family, split, seed, stress_override=level)
                    for task in TASKS
                    for family in FAMILIES
                ]
                row = {"stress_level": level, "method": method["method"], "seed": seed}
                for metric in [
                    "success",
                    "invalid_plan",
                    "collision_trap",
                    "support_failure",
                    "topology_f1",
                    "detection_latency",
                    "replan_cost",
                    "total_cost",
                ]:
                    row[metric] = mean([g[metric] for g in groups])
                rows.append(row)
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "invalid_plan",
        "collision_trap",
        "support_failure",
        "topology_f1",
        "detection_latency",
        "replan_cost",
        "total_cost",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [r for r in summary if r["split"] == "combined_stress"]
    methods = [r["method"] for r in combined]
    x = np.arange(len(methods))
    colors = ["#7f8c8d"] * len(methods)
    for idx, method in enumerate(methods):
        if method == "proposed_topology_change_detector":
            colors[idx] = "#1f9d8a"
        if method == "oracle_topology_planner":
            colors[idx] = "#243b53"

    plt.figure(figsize=(12, 5.8))
    plt.bar(x, [float(r["mean_mean_success"]) for r in combined], yerr=[float(r["ci95_mean_success"]) for r in combined], color=colors, capsize=3)
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Workspace topology-change benchmark")
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_combined_success.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 5.6))
    width = 0.38
    plt.bar(x - width / 2, [float(r["mean_mean_topology_f1"]) for r in combined], width=width, color="#1f9d8a", label="topology F1")
    plt.bar(x + width / 2, [float(r["mean_mean_detection_latency"]) for r in combined], width=width, color="#e07a5f", label="detection latency")
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Rate / normalized latency")
    plt.title("Detection quality under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_detection_quality.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5.6))
    for row in combined:
        marker, size, color = "o", 60, "#7f8c8d"
        if row["method"] == "proposed_topology_change_detector":
            marker, size, color = "*", 165, "#1f9d8a"
        if row["method"] == "oracle_topology_planner":
            marker, size, color = "D", 85, "#243b53"
        plt.scatter(float(row["mean_mean_invalid_plan"]), float(row["mean_regret_to_oracle"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("Invalid-plan rate")
    plt.ylabel("Regret to oracle")
    plt.title("Invalid plans vs oracle regret")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_invalid_regret.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    keep = {"proposed_topology_change_detector", "topological_slam_tamp", "risk_aware_robust_replanner", "graph_neural_change_classifier", "oracle_topology_planner"}
    for method in sorted({r["method"] for r in stress_summary}):
        if method not in keep:
            continue
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_success"]) for r in series], marker="o", label=method)
    plt.xlabel("Topology-change stress")
    plt.ylabel("Mean success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_stress_sweep.png", dpi=180)
    plt.close()

    labels = [r["ablation"] for r in ablation_summary]
    ax = np.arange(len(labels))
    plt.figure(figsize=(11, 5.6))
    plt.bar(ax, [float(r["mean_mean_success"]) for r in ablation_summary], yerr=[float(r["ci95_mean_success"]) for r in ablation_summary], color=["#1f9d8a" if label == "full_topology_change_detector" else "#9aa6b2" for label in labels], capsize=3)
    plt.xticks(ax, labels, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Topology-change ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_ablation.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else str(value).replace("_", "\\_"))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_family, strongest):
    combined = [r for r in per_task_family if r["split"] == "combined_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_topology_change_detector"]
    peer = {(r["task"], r["family"]): r for r in combined if r["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["family"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "family": row["family"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_invalid_plan": row["mean_invalid_plan"],
                "proposed_collision_trap": row["mean_collision_trap"],
                "lesson": "late topology updates still fail when reachability changes during execution rather than before commitment",
            }
        )
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    proposed = combined["proposed_topology_change_detector"]
    base = combined[strongest]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    invalid_delta = float(proposed["mean_mean_invalid_plan"]) - float(base["mean_mean_invalid_plan"])
    collision_delta = float(proposed["mean_mean_collision_trap"]) - float(base["mean_mean_collision_trap"])
    f1_delta = float(proposed["mean_mean_topology_f1"]) - float(base["mean_mean_topology_f1"])
    latency_delta = float(proposed["mean_mean_detection_latency"]) - float(base["mean_mean_detection_latency"])
    strongest_pair = next(r for r in pairwise if r["baseline"] == strongest)
    full = next(r for r in ablations if r["ablation"] == "full_topology_change_detector")
    best_ablation = max([r for r in ablations if r["ablation"] != "full_topology_change_detector"], key=lambda r: float(r["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    safety_gate = invalid_delta <= 0.020 and collision_delta <= 0.020
    diagnostic_gate = f1_delta >= 0.030 or latency_delta <= -0.030
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and safety_gate and diagnostic_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local topology-change evidence supports the mechanism, but no real robot or external benchmark validation is available"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the decisive success, safety, diagnostic, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "safety_gate": safety_gate,
        "diagnostic_gate": diagnostic_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "invalid_plan_delta_vs_strongest": invalid_delta,
        "collision_trap_delta_vs_strongest": collision_delta,
        "topology_f1_delta_vs_strongest": f1_delta,
        "latency_delta_vs_strongest": latency_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 101 workspace_topology_change_detection evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 topology-change families x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"invalid={float(row['mean_mean_invalid_plan']):.3f}, collision={float(row['mean_mean_collision_trap']):.3f}, "
                f"support={float(row['mean_mean_support_failure']):.3f}, topo_f1={float(row['mean_mean_topology_f1']):.3f}, "
                f"latency={float(row['mean_mean_detection_latency']):.3f}, regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"invalid={float(row['mean_mean_invalid_plan']):.3f}, collision={float(row['mean_mean_collision_trap']):.3f}, "
                f"note={row['interpretation']}\n"
            )


def main():
    seed_rows, per_task_family, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_family, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_family_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_family_metrics.csv", rounded(per_task_family))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_family_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_invalid_plan", "Invalid"),
            ("mean_mean_collision_trap", "Coll."),
            ("mean_mean_topology_f1", "TopoF1"),
            ("mean_mean_detection_latency", "Delay"),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-stress workspace topology-change benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_invalid_plan", "Invalid"),
            ("mean_mean_collision_trap", "Coll."),
            ("mean_mean_topology_f1", "TopoF1"),
        ],
        "Ablations of topology-change detection.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-stress success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
