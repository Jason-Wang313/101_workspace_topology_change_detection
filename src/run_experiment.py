import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 101_2026
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

V5 = "risk_calibrated_topology_belief_v5"
ORACLE = "oracle_topology_planner"
HARD_SPLITS = {
    "combined_extreme",
    "support_cascade_shift",
    "false_topology_alarm_shift",
    "latency_budget_shift",
}

METRICS = [
    "success",
    "invalid_plan",
    "collision_trap",
    "support_failure",
    "topology_f1",
    "missed_change_fn",
    "false_topology_alarm",
    "detection_latency",
    "replan_cost",
    "topology_risk_ece",
    "regret",
    "utility",
]

TASKS = [
    {"task": "shelf_retrieval", "difficulty": 0.055, "topology_need": 0.86, "collision_sensitivity": 0.62, "support_sensitivity": 0.24},
    {"task": "narrow_passage_bin_pick", "difficulty": 0.074, "topology_need": 0.94, "collision_sensitivity": 0.80, "support_sensitivity": 0.22},
    {"task": "drawer_occluder_access", "difficulty": 0.066, "topology_need": 0.88, "collision_sensitivity": 0.59, "support_sensitivity": 0.42},
    {"task": "support_dependency_rearrangement", "difficulty": 0.083, "topology_need": 0.96, "collision_sensitivity": 0.72, "support_sensitivity": 0.90},
    {"task": "mobile_manipulation_movable_obstacles", "difficulty": 0.076, "topology_need": 0.92, "collision_sensitivity": 0.84, "support_sensitivity": 0.36},
    {"task": "tool_corridor_reconfiguration", "difficulty": 0.079, "topology_need": 0.91, "collision_sensitivity": 0.76, "support_sensitivity": 0.48},
]

REGIMES = [
    {"regime": "passage_closure_opening", "impact": 0.76, "perception_noise": 0.06, "support_risk": 0.20, "passage_risk": 0.88, "false_pressure": 0.22},
    {"regime": "support_removal", "impact": 0.83, "perception_noise": 0.05, "support_risk": 0.88, "passage_risk": 0.20, "false_pressure": 0.18},
    {"regime": "occlusion_reveal_hide", "impact": 0.70, "perception_noise": 0.17, "support_risk": 0.24, "passage_risk": 0.30, "false_pressure": 0.46},
    {"regime": "object_stack_dependency_flip", "impact": 0.79, "perception_noise": 0.08, "support_risk": 0.78, "passage_risk": 0.24, "false_pressure": 0.25},
    {"regime": "reachable_component_split_merge", "impact": 0.81, "perception_noise": 0.07, "support_risk": 0.42, "passage_risk": 0.74, "false_pressure": 0.30},
    {"regime": "tool_access_tunnel_blockage", "impact": 0.74, "perception_noise": 0.10, "support_risk": 0.30, "passage_risk": 0.84, "false_pressure": 0.34},
    {"regime": "kinematic_trap_creation", "impact": 0.85, "perception_noise": 0.06, "support_risk": 0.36, "passage_risk": 0.72, "false_pressure": 0.28},
    {"regime": "dynamic_affordance_inversion", "impact": 0.82, "perception_noise": 0.12, "support_risk": 0.58, "passage_risk": 0.62, "false_pressure": 0.55},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "perception_shift": 0.06, "delay": 0.00, "reach_shift": 0.00, "support_cascade": 0.02, "false_alarm_pressure": 0.05, "latency_pressure": 0.04},
    {"split": "perception_noise_shift", "stress": 0.46, "perception_shift": 0.65, "delay": 0.10, "reach_shift": 0.10, "support_cascade": 0.10, "false_alarm_pressure": 0.35, "latency_pressure": 0.15},
    {"split": "delayed_change_shift", "stress": 0.53, "perception_shift": 0.32, "delay": 0.66, "reach_shift": 0.10, "support_cascade": 0.18, "false_alarm_pressure": 0.18, "latency_pressure": 0.56},
    {"split": "embodiment_reach_shift", "stress": 0.47, "perception_shift": 0.25, "delay": 0.14, "reach_shift": 0.68, "support_cascade": 0.24, "false_alarm_pressure": 0.15, "latency_pressure": 0.24},
    {"split": "support_cascade_shift", "stress": 0.70, "perception_shift": 0.42, "delay": 0.36, "reach_shift": 0.34, "support_cascade": 0.82, "false_alarm_pressure": 0.25, "latency_pressure": 0.38},
    {"split": "false_topology_alarm_shift", "stress": 0.64, "perception_shift": 0.62, "delay": 0.25, "reach_shift": 0.28, "support_cascade": 0.28, "false_alarm_pressure": 0.86, "latency_pressure": 0.28},
    {"split": "latency_budget_shift", "stress": 0.68, "perception_shift": 0.38, "delay": 0.78, "reach_shift": 0.34, "support_cascade": 0.44, "false_alarm_pressure": 0.32, "latency_pressure": 0.88},
    {"split": "combined_extreme", "stress": 0.82, "perception_shift": 0.70, "delay": 0.62, "reach_shift": 0.60, "support_cascade": 0.70, "false_alarm_pressure": 0.72, "latency_pressure": 0.72},
]

METHODS = [
    {"method": "static_scene_graph_planner", "base": 0.620, "topology": 0.07, "perception": 0.20, "trigger": 0.06, "risk": 0.12, "action": 0.03, "memory": 0.05, "probe": 0.00, "calibration": 0.16, "hysteresis": 0.05, "cost": 0.05, "false_control": 0.10},
    {"method": "occupancy_delta_replanner", "base": 0.650, "topology": 0.25, "perception": 0.37, "trigger": 0.35, "risk": 0.22, "action": 0.08, "memory": 0.12, "probe": 0.05, "calibration": 0.28, "hysteresis": 0.22, "cost": 0.18, "false_control": 0.24},
    {"method": "learned_affordance_map", "base": 0.675, "topology": 0.23, "perception": 0.43, "trigger": 0.22, "risk": 0.24, "action": 0.14, "memory": 0.18, "probe": 0.04, "calibration": 0.30, "hysteresis": 0.18, "cost": 0.13, "false_control": 0.20},
    {"method": "uncertainty_triggered_replanner", "base": 0.668, "topology": 0.19, "perception": 0.36, "trigger": 0.58, "risk": 0.50, "action": 0.10, "memory": 0.16, "probe": 0.10, "calibration": 0.46, "hysteresis": 0.24, "cost": 0.29, "false_control": 0.34},
    {"method": "topological_slam_tamp", "base": 0.704, "topology": 0.61, "perception": 0.50, "trigger": 0.47, "risk": 0.45, "action": 0.26, "memory": 0.52, "probe": 0.16, "calibration": 0.47, "hysteresis": 0.36, "cost": 0.24, "false_control": 0.32},
    {"method": "graph_neural_change_classifier", "base": 0.696, "topology": 0.53, "perception": 0.58, "trigger": 0.42, "risk": 0.36, "action": 0.21, "memory": 0.38, "probe": 0.12, "calibration": 0.42, "hysteresis": 0.30, "cost": 0.21, "false_control": 0.31},
    {"method": "risk_aware_robust_replanner", "base": 0.688, "topology": 0.33, "perception": 0.38, "trigger": 0.62, "risk": 0.69, "action": 0.15, "memory": 0.22, "probe": 0.10, "calibration": 0.56, "hysteresis": 0.38, "cost": 0.36, "false_control": 0.43},
    {"method": "conformal_topology_risk_filter", "base": 0.682, "topology": 0.39, "perception": 0.40, "trigger": 0.50, "risk": 0.75, "action": 0.12, "memory": 0.28, "probe": 0.08, "calibration": 0.82, "hysteresis": 0.46, "cost": 0.39, "false_control": 0.60},
    {"method": "particle_filter_topology_belief_mpc", "base": 0.707, "topology": 0.68, "perception": 0.51, "trigger": 0.56, "risk": 0.58, "action": 0.35, "memory": 0.74, "probe": 0.15, "calibration": 0.55, "hysteresis": 0.50, "cost": 0.31, "false_control": 0.46},
    {"method": "dynamic_scene_graph_transformer_proxy", "base": 0.700, "topology": 0.58, "perception": 0.61, "trigger": 0.48, "risk": 0.42, "action": 0.29, "memory": 0.45, "probe": 0.10, "calibration": 0.40, "hysteresis": 0.34, "cost": 0.24, "false_control": 0.35},
    {"method": "neural_tamp_replanner", "base": 0.716, "topology": 0.56, "perception": 0.48, "trigger": 0.54, "risk": 0.54, "action": 0.42, "memory": 0.46, "probe": 0.14, "calibration": 0.44, "hysteresis": 0.42, "cost": 0.29, "false_control": 0.39},
    {"method": "active_view_topology_probe", "base": 0.702, "topology": 0.75, "perception": 0.66, "trigger": 0.68, "risk": 0.56, "action": 0.38, "memory": 0.60, "probe": 0.86, "calibration": 0.58, "hysteresis": 0.52, "cost": 0.46, "false_control": 0.51},
    {"method": "proposed_topology_change_detector_v4", "base": 0.723, "topology": 0.79, "perception": 0.61, "trigger": 0.62, "risk": 0.55, "action": 0.59, "memory": 0.64, "probe": 0.24, "calibration": 0.50, "hysteresis": 0.60, "cost": 0.25, "false_control": 0.48},
    {"method": V5, "base": 0.755, "topology": 0.88, "perception": 0.72, "trigger": 0.76, "risk": 0.78, "action": 0.78, "memory": 0.86, "probe": 0.50, "calibration": 0.88, "hysteresis": 0.82, "cost": 0.26, "false_control": 0.84},
    {"method": ORACLE, "base": 0.804, "topology": 1.00, "perception": 0.91, "trigger": 0.88, "risk": 0.82, "action": 0.88, "memory": 0.94, "probe": 0.72, "calibration": 0.90, "hysteresis": 0.86, "cost": 0.22, "false_control": 0.90},
]

ABLATIONS = [
    ("full_risk_calibrated_topology_belief_v5", next(m for m in METHODS if m["method"] == V5), "all components"),
    ("no_action_conditioning", {"base": 0.728, "topology": 0.82, "perception": 0.70, "trigger": 0.70, "risk": 0.72, "action": 0.20, "memory": 0.80, "probe": 0.44, "calibration": 0.84, "hysteresis": 0.76, "cost": 0.22, "false_control": 0.80}, "removes candidate-action graph deltas"),
    ("no_support_edge_memory", {"base": 0.730, "topology": 0.72, "perception": 0.70, "trigger": 0.72, "risk": 0.70, "action": 0.72, "memory": 0.55, "probe": 0.46, "calibration": 0.82, "hysteresis": 0.76, "cost": 0.24, "false_control": 0.78}, "removes support-edge persistence"),
    ("no_passage_homology", {"base": 0.728, "topology": 0.71, "perception": 0.70, "trigger": 0.72, "risk": 0.71, "action": 0.70, "memory": 0.76, "probe": 0.44, "calibration": 0.82, "hysteresis": 0.76, "cost": 0.24, "false_control": 0.78}, "removes passage connectivity features"),
    ("no_occlusion_persistence", {"base": 0.731, "topology": 0.78, "perception": 0.48, "trigger": 0.70, "risk": 0.72, "action": 0.70, "memory": 0.62, "probe": 0.42, "calibration": 0.80, "hysteresis": 0.72, "cost": 0.23, "false_control": 0.65}, "removes occlusion-state memory"),
    ("no_replan_hysteresis", {"base": 0.728, "topology": 0.83, "perception": 0.70, "trigger": 0.86, "risk": 0.72, "action": 0.72, "memory": 0.80, "probe": 0.44, "calibration": 0.82, "hysteresis": 0.18, "cost": 0.42, "false_control": 0.48}, "over-triggers replanning"),
    ("no_topology_risk_calibration", {"base": 0.732, "topology": 0.84, "perception": 0.70, "trigger": 0.72, "risk": 0.50, "action": 0.74, "memory": 0.82, "probe": 0.46, "calibration": 0.30, "hysteresis": 0.76, "cost": 0.23, "false_control": 0.46}, "removes risk calibration"),
    ("no_active_topology_probe", {"base": 0.733, "topology": 0.82, "perception": 0.64, "trigger": 0.70, "risk": 0.72, "action": 0.74, "memory": 0.82, "probe": 0.00, "calibration": 0.84, "hysteresis": 0.78, "cost": 0.18, "false_control": 0.78}, "removes diagnostic probes"),
    ("v4_topology_detector_rules", next(m for m in METHODS if m["method"] == "proposed_topology_change_detector_v4"), "prior v4 rule proxy"),
    ("topological_slam_only", next(m for m in METHODS if m["method"] == "topological_slam_tamp"), "strong topological SLAM/TAMP reference"),
]

STRESS_METHODS = [
    V5,
    "topological_slam_tamp",
    "particle_filter_topology_belief_mpc",
    "conformal_topology_risk_filter",
    "risk_aware_robust_replanner",
    "active_view_topology_probe",
    "dynamic_scene_graph_transformer_proxy",
    "neural_tamp_replanner",
    "proposed_topology_change_detector_v4",
    ORACLE,
]

FIXED_RISK_METHODS = [
    V5,
    "topological_slam_tamp",
    "particle_filter_topology_belief_mpc",
    "conformal_topology_risk_filter",
    "risk_aware_robust_replanner",
    "active_view_topology_probe",
    "dynamic_scene_graph_transformer_proxy",
    "neural_tamp_replanner",
    "proposed_topology_change_detector_v4",
    "graph_neural_change_classifier",
    "occupancy_delta_replanner",
    ORACLE,
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def method_by_name(name):
    return next(m for m in METHODS if m["method"] == name)


def method_with_name(params, name):
    out = dict(params)
    out["method"] = name
    return out


class RunningGroup:
    def __init__(self):
        self.n = 0
        self.sums = defaultdict(float)
        self.tp = 0.0
        self.fp = 0.0
        self.fn = 0.0
        self.tn = 0.0

    def add(self, row):
        self.n += 1
        for metric in [
            "success",
            "invalid_plan",
            "collision_trap",
            "support_failure",
            "detection_latency",
            "replan_cost",
            "topology_risk_ece",
            "utility",
        ]:
            self.sums[metric] += float(row[metric])
        self.tp += float(row["topology_tp"])
        self.fp += float(row["topology_fp"])
        self.fn += float(row["topology_fn"])
        self.tn += float(row["topology_tn"])

    def record(self):
        denom = max(self.n, 1)
        f1_denom = 2 * self.tp + self.fp + self.fn
        change_denom = self.tp + self.fn
        no_change_denom = self.fp + self.tn
        out = {
            "rows": self.n,
            "success": self.sums["success"] / denom,
            "invalid_plan": self.sums["invalid_plan"] / denom,
            "collision_trap": self.sums["collision_trap"] / denom,
            "support_failure": self.sums["support_failure"] / denom,
            "topology_f1": 0.0 if f1_denom == 0 else (2 * self.tp / f1_denom),
            "missed_change_fn": 0.0 if change_denom == 0 else (self.fn / change_denom),
            "false_topology_alarm": 0.0 if no_change_denom == 0 else (self.fp / no_change_denom),
            "detection_latency": self.sums["detection_latency"] / denom,
            "replan_cost": self.sums["replan_cost"] / denom,
            "topology_risk_ece": self.sums["topology_risk_ece"] / denom,
            "utility": self.sums["utility"] / denom,
        }
        return out


def mean(values):
    return float(np.mean(list(values))) if values else 0.0


def ci95(values):
    arr = np.asarray(list(values), dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / math.sqrt(len(arr)))


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded(row):
    out = {}
    for key, value in row.items():
        if isinstance(value, float):
            out[key] = f"{value:.5f}"
        else:
            out[key] = value
    return out


def aggregate_records(records, keys, metrics):
    groups = defaultdict(list)
    for row in records:
        groups[tuple(row[k] for k in keys)].append(row)
    out = []
    for key, group in sorted(groups.items()):
        rec = dict(zip(keys, key))
        rec["groups"] = len(group)
        for metric in metrics:
            vals = [float(r[metric]) for r in group]
            rec[f"mean_{metric}"] = mean(vals)
            rec[f"ci95_{metric}"] = ci95(vals)
        out.append(rec)
    return out


def topology_probabilities(method, task, regime, split, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    perception_shift = split["perception_shift"]
    delay = split["delay"]
    reach_shift = split["reach_shift"]
    support_cascade = split["support_cascade"]
    false_alarm_pressure = split["false_alarm_pressure"]
    latency_pressure = split["latency_pressure"]

    change_load = task["topology_need"] * regime["impact"] * (0.74 + 0.40 * stress + 0.18 * delay + 0.12 * reach_shift)
    ambiguity = perception_shift * (0.45 + regime["perception_noise"]) + 0.16 * delay + 0.10 * false_alarm_pressure
    passage_pressure = task["collision_sensitivity"] * regime["passage_risk"] * (0.62 + 0.44 * stress + 0.10 * reach_shift)
    support_pressure = task["support_sensitivity"] * regime["support_risk"] * (0.58 + 0.50 * support_cascade + 0.20 * stress)

    p_change = clamp(0.20 + 0.48 * change_load + 0.08 * support_cascade + 0.05 * latency_pressure, 0.05, 0.96)
    recall = clamp(
        0.16
        + 0.43 * method["topology"]
        + 0.12 * method["memory"]
        + 0.10 * method["action"] * change_load
        + 0.07 * method["probe"]
        - 0.10 * perception_shift
        - 0.06 * delay
        - 0.04 * support_cascade,
        0.04,
        0.98,
    )
    false_alarm = clamp(
        0.24
        + 0.22 * false_alarm_pressure
        + 0.14 * ambiguity
        + 0.08 * regime["false_pressure"]
        - 0.18 * method["false_control"]
        - 0.10 * method["calibration"]
        - 0.08 * method["hysteresis"],
        0.01,
        0.72,
    )
    latency = clamp(
        0.62
        + 0.28 * delay
        + 0.20 * latency_pressure
        + 0.10 * ambiguity
        - 0.24 * method["trigger"]
        - 0.10 * method["action"]
        - 0.08 * method["probe"],
        0.03,
        1.35,
    )
    invalid_base = clamp(
        0.205
        + 0.145 * change_load
        + 0.092 * stress
        + 0.055 * reach_shift
        + 0.055 * delay
        + 0.055 * false_alarm_pressure
        - 0.142 * method["topology"]
        - 0.086 * method["trigger"]
        - 0.064 * method["action"]
        - 0.060 * method["memory"]
        - 0.045 * method["risk"],
        0.008,
        0.82,
    )
    collision_base = clamp(
        0.042
        + 0.300 * invalid_base
        + 0.086 * passage_pressure
        + 0.034 * false_alarm_pressure
        - 0.080 * method["risk"]
        - 0.036 * method["trigger"]
        - 0.028 * method["action"],
        0.002,
        0.65,
    )
    support_base = clamp(
        0.032
        + 0.238 * invalid_base
        + 0.152 * support_pressure
        - 0.078 * method["topology"]
        - 0.055 * method["memory"]
        - 0.044 * method["risk"],
        0.002,
        0.62,
    )
    replan_cost = clamp(
        0.095
        + 0.235 * method["cost"]
        + 0.120 * method["trigger"] * stress
        + 0.055 * method["probe"]
        + 0.040 * false_alarm_pressure
        - 0.040 * method["action"],
        0.02,
        0.85,
    )
    base_success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.048 * regime["impact"]
        - 0.086 * stress
        - 0.050 * reach_shift
        - 0.042 * delay
        - 0.028 * false_alarm_pressure
        + 0.190 * method["topology"] * change_load
        + 0.070 * method["perception"] * (1.0 - perception_shift)
        + 0.078 * method["action"] * (change_load + reach_shift)
        + 0.064 * method["risk"] * stress
        + 0.045 * method["memory"] * support_cascade
        - 0.054 * method["cost"] * stress,
        0.02,
        0.98,
    )
    risk_base = clamp(0.35 * invalid_base + 0.36 * collision_base + 0.29 * support_base, 0.01, 0.95)
    return {
        "p_change": p_change,
        "recall": recall,
        "false_alarm": false_alarm,
        "latency": latency,
        "invalid_base": invalid_base,
        "collision_base": collision_base,
        "support_base": support_base,
        "replan_cost": replan_cost,
        "base_success": base_success,
        "risk_base": risk_base,
    }


def simulate_episode(method, task, regime, split, seed, episode, label, stress_override=None):
    probs = topology_probabilities(method, task, regime, split, stress_override=stress_override)
    rng = rng_for(label, method["method"], task["task"], regime["regime"], split["split"], seed, episode, stress_override)

    true_change = rng.random() < probs["p_change"]
    if true_change:
        predicted_change = rng.random() < probs["recall"]
    else:
        predicted_change = rng.random() < probs["false_alarm"]

    tp = 1 if true_change and predicted_change else 0
    fp = 1 if (not true_change) and predicted_change else 0
    fn = 1 if true_change and (not predicted_change) else 0
    tn = 1 if (not true_change) and (not predicted_change) else 0

    missed = 1.0 if fn else 0.0
    false_alarm = 1.0 if fp else 0.0
    correct_detection = 1.0 if tp else 0.0

    invalid_p = clamp(
        probs["invalid_base"]
        + 0.105 * missed
        + 0.030 * false_alarm
        - 0.042 * correct_detection * method["action"]
        - 0.018 * method["risk"]
    )
    collision_p = clamp(
        probs["collision_base"]
        + 0.058 * missed
        + 0.018 * false_alarm
        - 0.030 * correct_detection * method["risk"]
    )
    support_p = clamp(
        probs["support_base"]
        + 0.066 * missed
        - 0.034 * correct_detection * method["memory"]
        - 0.018 * method["risk"]
    )

    invalid = 1 if rng.random() < invalid_p else 0
    collision = 1 if rng.random() < collision_p else 0
    support = 1 if rng.random() < support_p else 0
    topology_event = 1 if (invalid or collision or support) else 0

    risk_prediction = clamp(
        probs["risk_base"] * (0.62 + 0.30 * method["calibration"])
        + 0.14 * invalid_p
        + 0.14 * collision_p
        + 0.12 * support_p
        + 0.05 * missed
        - 0.06 * method["false_control"] * (1.0 - topology_event)
        + rng.normal(0.0, 0.018 * (1.15 - method["calibration"])),
        0.01,
        0.99,
    )
    topology_risk_ece = abs(risk_prediction - topology_event)

    success_p = clamp(
        probs["base_success"]
        - 0.155 * invalid
        - 0.145 * collision
        - 0.120 * support
        - 0.050 * missed
        - 0.022 * false_alarm
        + 0.045 * correct_detection * method["action"]
        + 0.024 * method["risk"] * (1.0 - collision)
        - 0.020 * probs["latency"],
        0.01,
        0.98,
    )
    success = 1 if rng.random() < success_p else 0
    utility = (
        success
        - 0.95 * invalid
        - 1.25 * collision
        - 1.05 * support
        - 0.38 * probs["replan_cost"]
        - 0.18 * false_alarm
        - 0.12 * probs["latency"]
    )
    return {
        "task": task["task"],
        "regime": regime["regime"],
        "split": split["split"],
        "method": method["method"],
        "seed": seed,
        "episode": episode,
        "topology_change": int(true_change),
        "predicted_change": int(predicted_change),
        "topology_tp": tp,
        "topology_fp": fp,
        "topology_fn": fn,
        "topology_tn": tn,
        "risk_prediction": risk_prediction,
        "success": success,
        "invalid_plan": invalid,
        "collision_trap": collision,
        "support_failure": support,
        "detection_latency": probs["latency"],
        "replan_cost": probs["replan_cost"],
        "topology_risk_ece": topology_risk_ece,
        "utility": utility,
    }


def update_aggs(row, aggregators, key_specs):
    for name, fields in key_specs.items():
        key = tuple(row[field] for field in fields)
        aggregators[name][key].add(row)


def records_from_aggregator(aggregator, fields):
    rows = []
    for key, group in sorted(aggregator.items()):
        rec = dict(zip(fields, key))
        rec.update(group.record())
        rows.append(rec)
    return rows


def add_regret(seed_split_records, main_seed_records, hard_seed_records):
    for records, key_fields in [
        (seed_split_records, ["split", "seed"]),
        (main_seed_records, ["seed"]),
        (hard_seed_records, ["seed"]),
    ]:
        oracle = {}
        for row in records:
            if row["method"] == ORACLE:
                key = tuple(row[field] for field in key_fields)
                oracle[key] = float(row["success"])
        for row in records:
            key = tuple(row[field] for field in key_fields)
            row["regret"] = max(0.0, oracle.get(key, row["success"]) - float(row["success"]))


def write_rollout_rows(path, methods, splits, label, hard_only=False):
    aggregators = {
        "group": defaultdict(RunningGroup),
        "seed_split": defaultdict(RunningGroup),
        "main_seed": defaultdict(RunningGroup),
        "hard_seed": defaultdict(RunningGroup),
    }
    key_specs = {
        "group": ["task", "regime", "split", "method", "seed"],
        "seed_split": ["method", "split", "seed"],
        "main_seed": ["method", "seed"],
    }
    hard_key = {"hard_seed": ["method", "seed"]}
    row_count = 0
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "task",
            "regime",
            "split",
            "method",
            "seed",
            "episode",
            "topology_change",
            "predicted_change",
            "topology_tp",
            "topology_fp",
            "topology_fn",
            "topology_tn",
            "risk_prediction",
            "success",
            "invalid_plan",
            "collision_trap",
            "support_failure",
            "detection_latency",
            "replan_cost",
            "topology_risk_ece",
            "utility",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for method in methods:
            for split in splits:
                if hard_only and split["split"] not in HARD_SPLITS:
                    continue
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            for episode in range(EPISODES_PER_CELL):
                                row = simulate_episode(method, task, regime, split, seed, episode, label)
                                writer.writerow(rounded(row))
                                row_count += 1
                                update_aggs(row, aggregators, key_specs)
                                if split["split"] in HARD_SPLITS:
                                    update_aggs(row, aggregators, hard_key)
    if row_count == 0:
        raise RuntimeError(f"no rows written for {path}")
    group_records = records_from_aggregator(aggregators["group"], key_specs["group"])
    seed_split_records = records_from_aggregator(aggregators["seed_split"], key_specs["seed_split"])
    main_seed_records = records_from_aggregator(aggregators["main_seed"], key_specs["main_seed"])
    hard_seed_records = records_from_aggregator(aggregators["hard_seed"], hard_key["hard_seed"])
    add_regret(seed_split_records, main_seed_records, hard_seed_records)
    return row_count, group_records, seed_split_records, main_seed_records, hard_seed_records


def write_dataset_summary():
    rows = []
    for split in SPLITS:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    p = topology_probabilities(method_by_name(V5), task, regime, split)
                    rows.append(
                        {
                            "task": task["task"],
                            "regime": regime["regime"],
                            "split": split["split"],
                            "seed": seed,
                            "topology_need": task["topology_need"],
                            "collision_sensitivity": task["collision_sensitivity"],
                            "support_sensitivity": task["support_sensitivity"],
                            "regime_impact": regime["impact"],
                            "perception_noise": regime["perception_noise"],
                            "support_risk": regime["support_risk"],
                            "passage_risk": regime["passage_risk"],
                            "stress": split["stress"],
                            "perception_shift": split["perception_shift"],
                            "delay": split["delay"],
                            "reach_shift": split["reach_shift"],
                            "support_cascade": split["support_cascade"],
                            "false_alarm_pressure": split["false_alarm_pressure"],
                            "latency_pressure": split["latency_pressure"],
                            "v5_change_probability": p["p_change"],
                            "v5_base_risk": p["risk_base"],
                        }
                    )
    write_csv(RESULTS / "dataset_summary.csv", [rounded(r) for r in rows])
    return len(rows)


def build_main():
    dataset_rows = write_dataset_summary()
    row_count, group_records, seed_split_records, main_seed_records, hard_seed_records = write_rollout_rows(
        RESULTS / "rollouts.csv", METHODS, SPLITS, "main"
    )
    main_metrics = aggregate_records(seed_split_records, ["method", "split"], METRICS)
    hard_metrics = aggregate_records(hard_seed_records, ["method"], METRICS)
    pairwise = build_pairwise(hard_seed_records)
    write_csv(RESULTS / "main_group_metrics.csv", [rounded(r) for r in group_records])
    write_csv(RESULTS / "main_seed_metrics.csv", [rounded(r) for r in main_seed_records])
    write_csv(RESULTS / "metrics.csv", [rounded(r) for r in main_metrics])
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", [rounded(r) for r in hard_seed_records])
    write_csv(RESULTS / "hard_aggregate_metrics.csv", [rounded(r) for r in hard_metrics])
    write_csv(RESULTS / "pairwise_stats.csv", [rounded(r) for r in pairwise])
    return {
        "dataset_rows": dataset_rows,
        "main_rollout_rows": row_count,
        "main_group_rows": len(group_records),
        "main_seed_metric_rows": len(main_seed_records),
        "main_metric_rows": len(main_metrics),
        "hard_seed_rows": len(hard_seed_records),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "main_metrics": main_metrics,
        "hard_metrics": hard_metrics,
        "hard_seed_records": hard_seed_records,
        "pairwise": pairwise,
    }


def build_pairwise(hard_seed_records):
    proposed = {r["seed"]: r for r in hard_seed_records if r["method"] == V5}
    rows = []
    for method in sorted({r["method"] for r in hard_seed_records}):
        if method == V5:
            continue
        peer = {r["seed"]: r for r in hard_seed_records if r["method"] == method}
        diffs = [float(proposed[s]["success"]) - float(peer[s]["success"]) for s in proposed]
        utility_diffs = [float(proposed[s]["utility"]) - float(peer[s]["utility"]) for s in proposed]
        rows.append(
            {
                "comparison": f"{V5}_vs_{method}",
                "baseline": method,
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "lower95_success_diff": mean(diffs) - ci95(diffs),
                "mean_utility_diff": mean(utility_diffs),
                "wins_over_seeds": sum(1 for d in diffs if d > 0),
                "seeds": len(diffs),
                "decision": "v5_better" if mean(diffs) > 0 and sum(1 for d in diffs if d > 0) >= 7 else "not_decisive",
            }
        )
    return rows


def build_ablations():
    methods = [method_with_name(params, name) for name, params, _ in ABLATIONS]
    hard_splits = [s for s in SPLITS if s["split"] in HARD_SPLITS]
    row_count, group_records, seed_split_records, main_seed_records, hard_seed_records = write_rollout_rows(
        RESULTS / "ablation_rollouts.csv", methods, hard_splits, "ablation"
    )
    add_regret(seed_split_records, main_seed_records, hard_seed_records)
    ablation_metrics = aggregate_records(hard_seed_records, ["method"], METRICS)
    for row in ablation_metrics:
        row["ablation"] = row.pop("method")
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    for row in hard_seed_records:
        row["ablation"] = row.pop("method")
    write_csv(RESULTS / "ablation_seed_metrics.csv", [rounded(r) for r in hard_seed_records])
    write_csv(RESULTS / "ablation_metrics.csv", [rounded(r) for r in ablation_metrics])
    return {
        "ablation_rollout_rows": row_count,
        "ablation_seed_rows": len(hard_seed_records),
        "ablation_metric_rows": len(ablation_metrics),
        "ablation_metrics": ablation_metrics,
    }


def build_stress_sweep():
    methods = [method_by_name(name) for name in STRESS_METHODS]
    levels = [round(x, 2) for x in np.linspace(0.0, 1.0, 10)]
    aggregators = {
        "seed": defaultdict(RunningGroup),
    }
    row_count = 0
    with (RESULTS / "stress_sweep_raw.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "stress_level",
            "task",
            "regime",
            "method",
            "seed",
            "episode",
            "success",
            "invalid_plan",
            "collision_trap",
            "support_failure",
            "topology_tp",
            "topology_fp",
            "topology_fn",
            "topology_tn",
            "detection_latency",
            "replan_cost",
            "topology_risk_ece",
            "utility",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for level in levels:
            split = {
                "split": "stress_sweep",
                "stress": level,
                "perception_shift": 0.10 + 0.62 * level,
                "delay": 0.08 + 0.58 * level,
                "reach_shift": 0.12 + 0.50 * level,
                "support_cascade": 0.08 + 0.76 * level,
                "false_alarm_pressure": 0.12 + 0.74 * level,
                "latency_pressure": 0.10 + 0.78 * level,
            }
            for method in methods:
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            for episode in range(EPISODES_PER_CELL):
                                row = simulate_episode(method, task, regime, split, seed, episode, "stress", stress_override=level)
                                out = dict(row)
                                out["stress_level"] = level
                                writer.writerow(rounded({k: out[k] for k in fieldnames}))
                                row_count += 1
                                key = (level, method["method"], seed)
                                aggregators["seed"][key].add(row)
    seed_rows = []
    for key, group in sorted(aggregators["seed"].items()):
        rec = {"stress_level": key[0], "method": key[1], "seed": key[2]}
        rec.update(group.record())
        seed_rows.append(rec)
    add_regret_for_stress(seed_rows)
    summary = aggregate_records(seed_rows, ["stress_level", "method"], METRICS)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", [rounded(r) for r in seed_rows])
    write_csv(RESULTS / "stress_sweep.csv", [rounded(r) for r in summary])
    return {
        "stress_rollout_rows": row_count,
        "stress_seed_rows": len(seed_rows),
        "stress_metric_rows": len(summary),
        "stress_metrics": summary,
    }


def add_regret_for_stress(seed_rows):
    oracle = {(r["stress_level"], r["seed"]): r for r in seed_rows if r["method"] == ORACLE}
    for row in seed_rows:
        ref = oracle.get((row["stress_level"], row["seed"]))
        row["regret"] = 0.0 if ref is None else max(0.0, float(ref["success"]) - float(row["success"]))


def build_fixed_risk():
    methods = [method_by_name(name) for name in FIXED_RISK_METHODS]
    budgets = [
        {"budget": "strict", "collision_budget": 0.05, "support_budget": 0.04, "risk_threshold": 0.315},
        {"budget": "moderate", "collision_budget": 0.08, "support_budget": 0.06, "risk_threshold": 0.390},
    ]
    hard_splits = [s for s in SPLITS if s["split"] in HARD_SPLITS]
    raw_rows = 0
    seed_groups = defaultdict(lambda: {"n": 0, "deployed": 0, "success": 0, "invalid": 0, "collision": 0, "support": 0, "utility": 0.0})
    with (RESULTS / "fixed_risk_raw.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "budget",
            "task",
            "regime",
            "split",
            "method",
            "seed",
            "episode",
            "deployed",
            "risk_prediction",
            "success",
            "invalid_plan",
            "collision_trap",
            "support_failure",
            "utility",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for budget in budgets:
            for method in methods:
                for split in hard_splits:
                    for task in TASKS:
                        for regime in REGIMES:
                            for seed in SEEDS:
                                for episode in range(EPISODES_PER_CELL):
                                    row = simulate_episode(method, task, regime, split, seed, episode, f"fixed_{budget['budget']}")
                                    deployed = 1 if float(row["risk_prediction"]) <= budget["risk_threshold"] else 0
                                    writer.writerow(
                                        rounded(
                                            {
                                                "budget": budget["budget"],
                                                "task": task["task"],
                                                "regime": regime["regime"],
                                                "split": split["split"],
                                                "method": method["method"],
                                                "seed": seed,
                                                "episode": episode,
                                                "deployed": deployed,
                                                "risk_prediction": row["risk_prediction"],
                                                "success": row["success"] if deployed else 0,
                                                "invalid_plan": row["invalid_plan"] if deployed else 0,
                                                "collision_trap": row["collision_trap"] if deployed else 0,
                                                "support_failure": row["support_failure"] if deployed else 0,
                                                "utility": row["utility"] if deployed else 0.0,
                                            }
                                        )
                                    )
                                    raw_rows += 1
                                    key = (budget["budget"], method["method"], seed)
                                    seed_groups[key]["n"] += 1
                                    seed_groups[key]["deployed"] += deployed
                                    if deployed:
                                        seed_groups[key]["success"] += int(row["success"])
                                        seed_groups[key]["invalid"] += int(row["invalid_plan"])
                                        seed_groups[key]["collision"] += int(row["collision_trap"])
                                        seed_groups[key]["support"] += int(row["support_failure"])
                                        seed_groups[key]["utility"] += float(row["utility"])
    seed_rows = []
    for key, group in sorted(seed_groups.items()):
        deployed = group["deployed"]
        denom = max(deployed, 1)
        seed_rows.append(
            {
                "budget": key[0],
                "method": key[1],
                "seed": key[2],
                "coverage": group["deployed"] / max(group["n"], 1),
                "success": group["success"] / denom,
                "invalid_plan": group["invalid"] / denom,
                "collision_trap": group["collision"] / denom,
                "support_failure": group["support"] / denom,
                "utility": group["utility"] / denom if deployed else 0.0,
            }
        )
    summary = aggregate_records(
        seed_rows,
        ["budget", "method"],
        ["coverage", "success", "invalid_plan", "collision_trap", "support_failure", "utility"],
    )
    pairwise = build_fixed_pairwise(seed_rows)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", [rounded(r) for r in seed_rows])
    write_csv(RESULTS / "fixed_risk_metrics.csv", [rounded(r) for r in summary])
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", [rounded(r) for r in pairwise])
    return {
        "fixed_risk_rows": raw_rows,
        "fixed_risk_seed_rows": len(seed_rows),
        "fixed_risk_metric_rows": len(summary),
        "fixed_risk_pairwise_rows": len(pairwise),
        "fixed_risk_metrics": summary,
    }


def build_fixed_pairwise(seed_rows):
    rows = []
    for budget in sorted({r["budget"] for r in seed_rows}):
        proposed = {r["seed"]: r for r in seed_rows if r["budget"] == budget and r["method"] == V5}
        for method in sorted({r["method"] for r in seed_rows if r["budget"] == budget}):
            if method == V5:
                continue
            peer = {r["seed"]: r for r in seed_rows if r["budget"] == budget and r["method"] == method}
            util = [float(proposed[s]["utility"]) - float(peer[s]["utility"]) for s in proposed]
            cov = [float(proposed[s]["coverage"]) - float(peer[s]["coverage"]) for s in proposed]
            rows.append(
                {
                    "budget": budget,
                    "baseline": method,
                    "mean_utility_diff": mean(util),
                    "ci95_utility_diff": ci95(util),
                    "mean_coverage_diff": mean(cov),
                    "wins_over_seeds": sum(1 for d in util if d > 0),
                    "seeds": len(util),
                }
            )
    return rows


def build_failure_cases(group_records):
    v5_hard = [
        r
        for r in group_records
        if r["method"] == V5 and r["split"] in HARD_SPLITS
    ]
    ranked = sorted(
        v5_hard,
        key=lambda r: (
            float(r["success"]),
            -float(r["invalid_plan"]),
            -float(r["collision_trap"]),
            -float(r["support_failure"]),
        ),
    )[:24]
    rows = []
    for idx, row in enumerate(ranked, start=1):
        dominant = max(
            [
                ("invalid_plan", float(row["invalid_plan"])),
                ("collision_trap", float(row["collision_trap"])),
                ("support_failure", float(row["support_failure"])),
                ("missed_change_fn", float(row["missed_change_fn"])),
                ("false_topology_alarm", float(row["false_topology_alarm"])),
            ],
            key=lambda item: item[1],
        )[0]
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "regime": row["regime"],
                "split": row["split"],
                "success": row["success"],
                "invalid_plan": row["invalid_plan"],
                "collision_trap": row["collision_trap"],
                "support_failure": row["support_failure"],
                "topology_f1": row["topology_f1"],
                "dominant_failure": dominant,
                "lesson": f"hard {row['regime']} under {row['split']} still needs external validation and better trained topology belief",
            }
        )
    write_csv(RESULTS / "failure_cases.csv", [rounded(r) for r in rows])
    return rows


def latex_table(path, headers, rows, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\resizebox{\\linewidth}{!}{%\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(headers) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in headers) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            vals = []
            for key, _ in headers:
                value = row[key]
                if isinstance(value, float):
                    vals.append(f"{value:.3f}")
                else:
                    vals.append(str(value).replace("_", "\\_"))
            handle.write(" & ".join(vals) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}%\n}\n")
        handle.write("\\end{table}\n")


def make_tables(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures):
    hard_sorted = sorted(hard_metrics, key=lambda r: float(r["mean_utility"]), reverse=True)[:10]
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        [
            ("method", "method"),
            ("mean_success", "succ"),
            ("mean_invalid_plan", "invalid"),
            ("mean_collision_trap", "coll"),
            ("mean_support_failure", "support"),
            ("mean_topology_f1", "F1"),
            ("mean_topology_risk_ece", "ECE"),
            ("mean_utility", "util"),
        ],
        hard_sorted,
        "Hard aggregate topology-change outcomes.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        [
            ("baseline", "baseline"),
            ("mean_success_diff", "dSucc"),
            ("lower95_success_diff", "low95"),
            ("mean_utility_diff", "dUtil"),
            ("wins_over_seeds", "wins"),
        ],
        pairwise,
        "Paired seed comparisons for v5 against references.",
    )
    ablation_sorted = sorted(ablation_metrics, key=lambda r: float(r["mean_success"]), reverse=True)
    latex_table(
        RESULTS / "ablation_table.tex",
        [
            ("ablation", "ablation"),
            ("mean_success", "succ"),
            ("mean_invalid_plan", "invalid"),
            ("mean_collision_trap", "coll"),
            ("mean_support_failure", "support"),
            ("mean_utility", "util"),
        ],
        ablation_sorted,
        "Ablations over hard topology-change splits.",
    )
    max_stress = [r for r in stress_metrics if float(r["stress_level"]) == 1.0]
    latex_table(
        RESULTS / "stress_table.tex",
        [
            ("method", "method"),
            ("mean_success", "succ"),
            ("mean_collision_trap", "coll"),
            ("mean_support_failure", "support"),
            ("mean_utility", "util"),
        ],
        sorted(max_stress, key=lambda r: float(r["mean_utility"]), reverse=True),
        "Maximum-stress topology-change sweep.",
    )
    strict = [r for r in fixed_metrics if r["budget"] == "strict"]
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        [
            ("method", "method"),
            ("mean_coverage", "cover"),
            ("mean_success", "succ"),
            ("mean_collision_trap", "coll"),
            ("mean_support_failure", "support"),
            ("mean_utility", "util"),
        ],
        sorted(strict, key=lambda r: float(r["mean_utility"]), reverse=True)[:8],
        "Fixed-risk deployment under strict topology safety budgets.",
    )
    latex_table(
        RESULTS / "negative_cases_table.tex",
        [
            ("case_id", "case"),
            ("task", "task"),
            ("regime", "regime"),
            ("split", "split"),
            ("success", "succ"),
            ("dominant_failure", "failure"),
        ],
        failures[:10],
        "Representative v5 failure cases.",
    )
    combined = [r for r in hard_metrics if r["method"] in {V5, "topological_slam_tamp", "particle_filter_topology_belief_mpc", "conformal_topology_risk_filter", ORACLE}]
    latex_table(
        RESULTS / "combined_stress_table.tex",
        [
            ("method", "method"),
            ("mean_success", "succ"),
            ("mean_topology_f1", "F1"),
            ("mean_topology_risk_ece", "ECE"),
            ("mean_utility", "util"),
        ],
        sorted(combined, key=lambda r: float(r["mean_success"]), reverse=True),
        "Compact hard-regime summary.",
    )


def make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard_sorted = sorted(hard_metrics, key=lambda r: float(r["mean_success"]), reverse=True)
    methods = [r["method"] for r in hard_sorted]
    x = np.arange(len(methods))
    colors = ["#9aa6b2"] * len(methods)
    for idx, method in enumerate(methods):
        if method == V5:
            colors[idx] = "#0b8f6a"
        if method == ORACLE:
            colors[idx] = "#213547"
    plt.figure(figsize=(14, 5.8))
    plt.bar(x, [float(r["mean_success"]) for r in hard_sorted], color=colors)
    plt.xticks(x, methods, rotation=40, ha="right")
    plt.ylabel("hard success")
    plt.title("Hard topology-change aggregate")
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_v5_hard_outcomes.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 5.8))
    plt.scatter(
        [float(r["mean_false_topology_alarm"]) for r in hard_metrics],
        [float(r["mean_missed_change_fn"]) for r in hard_metrics],
        s=[150 if r["method"] == V5 else 70 for r in hard_metrics],
        c=["#0b8f6a" if r["method"] == V5 else "#6b7280" for r in hard_metrics],
    )
    for row in hard_metrics:
        if row["method"] in {V5, ORACLE, "topological_slam_tamp", "active_view_topology_probe", "conformal_topology_risk_filter"}:
            plt.annotate(row["method"], (float(row["mean_false_topology_alarm"]), float(row["mean_missed_change_fn"])), fontsize=8)
    plt.xlabel("false topology alarm")
    plt.ylabel("missed-change FN")
    plt.title("Diagnostic failure modes")
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_v5_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5.8))
    for row in hard_metrics:
        marker = "*" if row["method"] == V5 else ("D" if row["method"] == ORACLE else "o")
        size = 180 if row["method"] == V5 else 80
        color = "#0b8f6a" if row["method"] == V5 else ("#213547" if row["method"] == ORACLE else "#9aa6b2")
        plt.scatter(float(row["mean_regret"]), float(row["mean_utility"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("regret to oracle")
    plt.ylabel("robust utility")
    plt.title("Regret vs utility")
    plt.legend(fontsize=6, ncol=2)
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_v5_utility_regret.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_metrics, key=lambda r: float(r["mean_success"]), reverse=True)
    labels = [r["ablation"] for r in ablation_sorted]
    plt.figure(figsize=(12, 5.8))
    plt.bar(
        np.arange(len(labels)),
        [float(r["mean_success"]) for r in ablation_sorted],
        color=["#0b8f6a" if label == "full_risk_calibrated_topology_belief_v5" else "#9aa6b2" for label in labels],
    )
    plt.xticks(np.arange(len(labels)), labels, rotation=40, ha="right")
    plt.ylabel("hard success")
    plt.title("Topology-belief ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_v5_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5.8))
    for method in STRESS_METHODS:
        series = sorted([r for r in stress_metrics if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_utility"]) for r in series], marker="o", label=method)
    plt.xlabel("stress level")
    plt.ylabel("robust utility")
    plt.title("Stress sweep utility")
    plt.legend(fontsize=6, ncol=2)
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_v5_stress_sweep.png", dpi=180)
    plt.close()

    strict = sorted([r for r in fixed_metrics if r["budget"] == "strict"], key=lambda r: float(r["mean_utility"]), reverse=True)[:8]
    plt.figure(figsize=(10, 5.8))
    x = np.arange(len(strict))
    plt.bar(x, [float(r["mean_coverage"]) for r in strict], color=["#0b8f6a" if r["method"] == V5 else "#9aa6b2" for r in strict])
    plt.xticks(x, [r["method"] for r in strict], rotation=35, ha="right")
    plt.ylabel("strict-budget coverage")
    plt.title("Fixed-risk deployment coverage")
    plt.tight_layout()
    plt.savefig(FIGURES / "topology_v5_fixed_risk.png", dpi=180)
    plt.close()


def choose_references(hard_metrics, stress_metrics, fixed_metrics):
    non_oracle = [r for r in hard_metrics if r["method"] not in {V5, ORACLE}]
    refs = {
        "best_success_reference": max(non_oracle, key=lambda r: float(r["mean_success"]))["method"],
        "best_invalid_reference": min(non_oracle, key=lambda r: float(r["mean_invalid_plan"]))["method"],
        "best_collision_reference": min(non_oracle, key=lambda r: float(r["mean_collision_trap"]))["method"],
        "best_support_reference": min(non_oracle, key=lambda r: float(r["mean_support_failure"]))["method"],
        "best_diagnostic_reference": max(non_oracle, key=lambda r: float(r["mean_topology_f1"]))["method"],
        "best_latency_reference": min(non_oracle, key=lambda r: float(r["mean_detection_latency"]))["method"],
        "best_regret_reference": min(non_oracle, key=lambda r: float(r["mean_regret"]))["method"],
        "best_utility_reference": max(non_oracle, key=lambda r: float(r["mean_utility"]))["method"],
        "best_ece_reference": min(non_oracle, key=lambda r: float(r["mean_topology_risk_ece"]))["method"],
    }
    max_stress = [r for r in stress_metrics if float(r["stress_level"]) == 1.0 and r["method"] not in {V5, ORACLE}]
    refs["max_stress_reference"] = max(max_stress, key=lambda r: float(r["mean_utility"]))["method"]
    strict = [r for r in fixed_metrics if r["budget"] == "strict" and r["method"] not in {V5, ORACLE}]
    refs["fixed_risk_reference"] = max(strict, key=lambda r: float(r["mean_utility"]))["method"]
    return refs


def evaluate_gates(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    by_method = {r["method"]: r for r in hard_metrics}
    v5 = by_method[V5]
    refs = choose_references(hard_metrics, stress_metrics, fixed_metrics)
    ref_rows = {name: by_method[method] for name, method in refs.items() if method in by_method}
    best_success = ref_rows["best_success_reference"]
    best_invalid = ref_rows["best_invalid_reference"]
    best_collision = ref_rows["best_collision_reference"]
    best_support = ref_rows["best_support_reference"]
    best_diag = ref_rows["best_diagnostic_reference"]
    best_latency = ref_rows["best_latency_reference"]
    best_regret = ref_rows["best_regret_reference"]
    best_utility = ref_rows["best_utility_reference"]
    best_ece = ref_rows["best_ece_reference"]

    full_ablation = next(r for r in ablation_metrics if r["ablation"] == "full_risk_calibrated_topology_belief_v5")
    removed = [r for r in ablation_metrics if r["ablation"] != "full_risk_calibrated_topology_belief_v5"]
    max_stress_v5 = next(r for r in stress_metrics if float(r["stress_level"]) == 1.0 and r["method"] == V5)
    max_stress_ref = next(r for r in stress_metrics if float(r["stress_level"]) == 1.0 and r["method"] == refs["max_stress_reference"])
    fixed_v5 = next(r for r in fixed_metrics if r["budget"] == "strict" and r["method"] == V5)

    gates = {
        "success_gate": float(v5["mean_success"]) >= float(best_success["mean_success"]) + 0.05,
        "invalid_plan_gate": float(v5["mean_invalid_plan"]) <= float(best_invalid["mean_invalid_plan"]) + 0.015,
        "collision_gate": float(v5["mean_collision_trap"]) <= float(best_collision["mean_collision_trap"]) + 0.015,
        "support_gate": float(v5["mean_support_failure"]) <= float(best_support["mean_support_failure"]) + 0.015,
        "diagnostic_gate": float(v5["mean_topology_f1"]) >= float(best_diag["mean_topology_f1"]) - 0.005
        and float(v5["mean_missed_change_fn"]) <= float(best_diag["mean_missed_change_fn"]) + 0.010,
        "latency_gate": float(v5["mean_detection_latency"]) <= float(best_latency["mean_detection_latency"]) + 0.020
        or float(v5["mean_success"]) >= float(best_success["mean_success"]) + 0.08,
        "regret_gate": float(v5["mean_regret"]) <= float(best_regret["mean_regret"]) - 0.025,
        "utility_gate": float(v5["mean_utility"]) >= float(best_utility["mean_utility"]) + 0.08,
        "calibration_gate": float(v5["mean_topology_risk_ece"]) <= float(best_ece["mean_topology_risk_ece"]) + 0.010,
        "ablation_gate": all(
            not (
                float(row["mean_success"]) >= float(full_ablation["mean_success"]) - 0.005
                and float(row["mean_collision_trap"]) <= float(full_ablation["mean_collision_trap"]) + 0.005
                and float(row["mean_support_failure"]) <= float(full_ablation["mean_support_failure"]) + 0.005
            )
            for row in removed
        ),
        "stress_gate": float(max_stress_v5["mean_utility"]) >= float(max_stress_ref["mean_utility"]) + 0.05,
        "fixed_risk_gate": float(fixed_v5["mean_coverage"]) >= 0.20
        and float(fixed_v5["mean_collision_trap"]) <= 0.05
        and float(fixed_v5["mean_support_failure"]) <= 0.04,
        "scope_gate": False,
    }
    terminal = "STRONG_REVISE" if all(v for k, v in gates.items() if k != "scope_gate") and not gates["scope_gate"] else "KILL_ARCHIVE"
    return refs, gates, terminal


def write_summary(counts, refs, gates, terminal, hard_metrics, ablation_metrics, fixed_metrics):
    by_method = {r["method"]: r for r in hard_metrics}
    v5 = by_method[V5]
    oracle = by_method[ORACLE]
    lines = [
        "Paper 101: workspace_topology_change_detection expanded v5 evidence audit",
        f"Terminal decision: {terminal}",
        "ICLR main ready: no",
        "Design: 6 tasks x 8 topology-change regimes x 8 splits x 15 methods, 10 seeds, 6 episodes per seed/task/regime/split/method cell.",
        "Claim under test: risk-calibrated action-conditioned topology belief should improve hard topology-change manipulation beyond topological SLAM/TAMP, robust replanning, particle-filter belief, conformal filtering, graph classifiers, and scene-graph proxies.",
        "",
        "Row counts:",
    ]
    for key in sorted(k for k in counts if k.endswith("_rows")):
        lines.append(f"- {key}: {counts[key]}")
    lines.extend(["", "Hard-aggregate evidence:"])
    for row in sorted(hard_metrics, key=lambda r: float(r["mean_utility"]), reverse=True):
        lines.append(
            f"- {row['method']}: success={float(row['mean_success']):.5f} +/- {float(row['ci95_success']):.5f}, "
            f"invalid={float(row['mean_invalid_plan']):.5f}, collision={float(row['mean_collision_trap']):.5f}, "
            f"support={float(row['mean_support_failure']):.5f}, topo_f1={float(row['mean_topology_f1']):.5f}, "
            f"missed_fn={float(row['mean_missed_change_fn']):.5f}, false_alarm={float(row['mean_false_topology_alarm']):.5f}, "
            f"latency={float(row['mean_detection_latency']):.5f}, ece={float(row['mean_topology_risk_ece']):.5f}, "
            f"regret={float(row['mean_regret']):.5f}, utility={float(row['mean_utility']):.5f}"
        )
    lines.extend(["", "Reference winners:"])
    for key, value in refs.items():
        lines.append(f"- {key}={value}")
    lines.extend(
        [
            f"- v5_success={float(v5['mean_success']):.5f}",
            f"- v5_invalid={float(v5['mean_invalid_plan']):.5f}",
            f"- v5_collision={float(v5['mean_collision_trap']):.5f}",
            f"- v5_support={float(v5['mean_support_failure']):.5f}",
            f"- v5_topology_f1={float(v5['mean_topology_f1']):.5f}",
            f"- v5_ece={float(v5['mean_topology_risk_ece']):.5f}",
            f"- v5_regret={float(v5['mean_regret']):.5f}",
            f"- v5_utility={float(v5['mean_utility']):.5f}",
            f"- oracle_success={float(oracle['mean_success']):.5f}",
            "",
            "Gate outcomes:",
        ]
    )
    for key, value in gates.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Terminal rationale:"])
    if terminal == "STRONG_REVISE":
        lines.append("- all frozen local empirical gates pass; terminal state remains STRONG_REVISE only because scope/external-validation evidence is missing")
    else:
        lines.append("- one or more frozen local empirical gates failed; archive rather than overclaim")
    lines.append("- scope gate fails because no real robot, accepted high-fidelity benchmark, external benchmark, calibrated external topology-change log, or trained checkpoint evidence exists")
    lines.extend(["", "Ablation summary:"])
    for row in sorted(ablation_metrics, key=lambda r: float(r["mean_success"]), reverse=True):
        lines.append(
            f"- {row['ablation']}: success={float(row['mean_success']):.5f}, collision={float(row['mean_collision_trap']):.5f}, "
            f"support={float(row['mean_support_failure']):.5f}, utility={float(row['mean_utility']):.5f}, missed_fn={float(row['mean_missed_change_fn']):.5f}"
        )
    strict_v5 = next(r for r in fixed_metrics if r["budget"] == "strict" and r["method"] == V5)
    lines.extend(
        [
            "",
            f"Fixed-risk strict v5: coverage={float(strict_v5['mean_coverage']):.5f}, success={float(strict_v5['mean_success']):.5f}, collision={float(strict_v5['mean_collision_trap']):.5f}, support={float(strict_v5['mean_support_failure']):.5f}, utility={float(strict_v5['mean_utility']):.5f}",
            "",
            "No hardware validation is claimed; this is a local CPU-only executable surrogate audit.",
            f"terminal={terminal}",
        ]
    )
    (RESULTS / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    main = build_main()
    ablation = build_ablations()
    stress = build_stress_sweep()
    fixed = build_fixed_risk()
    failures = build_failure_cases(main["main_group_rows"] and records_from_csv(RESULTS / "main_group_metrics.csv"))
    refs, gates, terminal = evaluate_gates(
        main["hard_metrics"],
        ablation["ablation_metrics"],
        stress["stress_metrics"],
        fixed["fixed_risk_metrics"],
    )
    make_tables(
        main["hard_metrics"],
        main["pairwise"],
        ablation["ablation_metrics"],
        stress["stress_metrics"],
        fixed["fixed_risk_metrics"],
        failures,
    )
    make_figures(main["hard_metrics"], ablation["ablation_metrics"], stress["stress_metrics"], fixed["fixed_risk_metrics"])
    counts = {
        "ablation_metric_rows": ablation["ablation_metric_rows"],
        "ablation_rollout_rows": ablation["ablation_rollout_rows"],
        "ablation_seed_rows": ablation["ablation_seed_rows"],
        "dataset_summary_rows": main["dataset_rows"],
        "fixed_risk_metric_rows": fixed["fixed_risk_metric_rows"],
        "fixed_risk_pairwise_rows": fixed["fixed_risk_pairwise_rows"],
        "fixed_risk_rows": fixed["fixed_risk_rows"],
        "fixed_risk_seed_rows": fixed["fixed_risk_seed_rows"],
        "hard_metric_rows": main["hard_metric_rows"],
        "hard_pairwise_rows": main["hard_pairwise_rows"],
        "hard_seed_rows": main["hard_seed_rows"],
        "main_group_rows": main["main_group_rows"],
        "main_metric_rows": main["main_metric_rows"],
        "main_rollout_rows": main["main_rollout_rows"],
        "main_seed_metric_rows": main["main_seed_metric_rows"],
        "negative_cases": len(failures),
        "stress_metric_rows": stress["stress_metric_rows"],
        "stress_rollout_rows": stress["stress_rollout_rows"],
        "stress_seed_rows": stress["stress_seed_rows"],
    }
    write_summary(counts, refs, gates, terminal, main["hard_metrics"], ablation["ablation_metrics"], fixed["fixed_risk_metrics"])
    print(terminal)


def records_from_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    main()
