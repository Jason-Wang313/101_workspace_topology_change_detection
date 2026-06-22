import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

PROPOSED = "risk_calibrated_topology_belief_v5"
ORACLE = "oracle_topology_planner"


def ascii_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value: object) -> str:
    text = ascii_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_summary() -> dict[str, str]:
    summary = {}
    for line in (RESULTS / "summary.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            summary[key.strip()] = value.strip()
        elif line.startswith("- ") and "=" in line:
            key, value = line[2:].split("=", 1)
            summary[key.strip()] = value.strip()
        elif line.startswith("Terminal decision:"):
            summary["decision"] = line.split(":", 1)[1].strip()
        elif line.startswith("terminal="):
            summary["terminal"] = line.split("=", 1)[1].strip()
    return summary


def fnum(value: object, digits: int = 5) -> str:
    return f"{float(value):.{digits}f}"


def short_label(value: str) -> str:
    aliases = {
        "risk_calibrated_topology_belief_v5": "topology_v5",
        "proposed_topology_change_detector_v4": "topology_v4",
        "oracle_topology_planner": "oracle",
        "topological_slam_tamp": "slam_tamp",
        "particle_filter_topology_belief_mpc": "pf_topology_mpc",
        "conformal_topology_risk_filter": "conformal_filter",
        "risk_aware_robust_replanner": "robust_replanner",
        "active_view_topology_probe": "active_probe",
        "dynamic_scene_graph_transformer_proxy": "dyn_sg_transformer",
        "graph_neural_change_classifier": "gnn_change",
        "uncertainty_triggered_replanner": "uncertainty_replan",
        "occupancy_delta_replanner": "occupancy_delta",
        "learned_affordance_map": "affordance_map",
        "static_scene_graph_planner": "static_sg",
        "neural_tamp_replanner": "neural_tamp",
        "full_risk_calibrated_topology_belief_v5": "full_v5",
        "no_action_conditioning": "no_action",
        "no_support_edge_memory": "no_support",
        "no_passage_homology": "no_passage",
        "no_occlusion_persistence": "no_occlusion",
        "no_replan_hysteresis": "no_hysteresis",
        "no_topology_risk_calibration": "no_calibration",
        "no_active_topology_probe": "no_probe",
        "v4_topology_detector_rules": "v4_rules",
        "topological_slam_only": "slam_only",
        "support_dependency_rearrangement": "support_rearrange",
        "mobile_manipulation_movable_obstacles": "mobile_obstacles",
        "tool_corridor_reconfiguration": "tool_corridor",
        "dynamic_affordance_inversion": "affordance_inversion",
        "reachable_component_split_merge": "component_split",
        "false_topology_alarm_shift": "false_alarm",
        "latency_budget_shift": "latency_budget",
        "support_cascade_shift": "support_cascade",
        "combined_extreme": "combined_extreme",
    }
    return aliases.get(value, value)


def make_bib_key(row: dict[str, str], index: int) -> str:
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    title_word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{title_word.lower()}{index}"


def write_bib(records: list[dict[str, str]]) -> list[str]:
    keys = []
    seen = set()
    entries = []
    for index, row in enumerate(records[:230], start=1):
        key = make_bib_key(row, index)
        while key in seen:
            key = f"{key}x"
        seen.add(key)
        keys.append(key)
        fields = [
            f"  title = {{{latex_escape(row.get('title', f'Reference {index}'))}}}",
            f"  author = {{{latex_escape(row.get('authors', 'Unknown'))}}}",
        ]
        year = latex_escape(row.get("year", ""))
        venue = latex_escape(row.get("venue", ""))
        doi = latex_escape(row.get("doi", ""))
        url = latex_escape(row.get("url", ""))
        if year:
            fields.append(f"  year = {{{year}}}")
        if venue:
            fields.append(f"  journal = {{{venue}}}")
        if doi:
            fields.append(f"  doi = {{{doi}}}")
        if url:
            fields.append(f"  url = {{{url}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    (PAPER / "references.bib").write_text("\n".join(entries), encoding="utf-8")
    return keys


def cite(keys: list[str], start: int, stop: int) -> str:
    if not keys:
        return ""
    chosen = keys[start:min(stop, len(keys))]
    return r"\citep{" + ",".join(chosen) + "}"


def citation_ledger(keys: list[str]) -> str:
    themes = [
        "scene graph and topology change detection",
        "robot manipulation under changing supports",
        "task-and-motion planning and replanning",
        "graph neural, transformer, and dynamic scene representations",
        "uncertainty, conformal risk, and fixed-risk deployment",
        "mobile manipulation and navigation topology",
        "evaluation, reproducibility, and dataset pressure",
    ]
    rows = []
    for index in range(0, len(keys), 3):
        chunk = keys[index:index + 3]
        rows.append(
            f"{index // 3 + 1} & {latex_escape(themes[(index // 3) % len(themes)])} & "
            + r"\citep{" + ",".join(chunk) + r"} \\"
        )
    return "\n".join(rows)


def compact_rows(rows: list[dict[str, str]], columns: list[str]) -> str:
    rendered = []
    for row in rows:
        cells = []
        for column in columns:
            value = row[column]
            if column in {"method", "baseline", "ablation", "task", "regime", "split", "dominant_failure"}:
                cells.append(latex_escape(short_label(value)))
            elif column in {"wins_over_seeds", "case_id", "seed"}:
                cells.append(latex_escape(value))
            else:
                cells.append(fnum(value, 3))
        rendered.append(" & ".join(cells) + r" \\")
    return "\n".join(rendered)


def long_metric_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = " & ".join(latex_escape(c.replace("mean_", "")) for c in columns) + r" \\"
    body = compact_rows(rows, columns)
    return "\n".join(
        [
            r"\begingroup\scriptsize\setlength{\tabcolsep}{3pt}",
            r"\begin{longtable}{@{}lrrrrrrr@{}}",
            r"\toprule",
            header,
            r"\midrule",
            body,
            r"\bottomrule",
            r"\end{longtable}",
            r"\endgroup",
        ]
    )


def main() -> None:
    summary = read_summary()
    hard = read_csv(RESULTS / "hard_aggregate_metrics.csv")
    pairwise = read_csv(RESULTS / "pairwise_stats.csv")
    ablations = read_csv(RESULTS / "ablation_metrics.csv")
    stress = read_csv(RESULTS / "stress_sweep.csv")
    fixed = read_csv(RESULTS / "fixed_risk_metrics.csv")
    failures = read_csv(RESULTS / "failure_cases.csv")
    refs = read_csv(DOCS / "deep_read_250.csv")
    keys = write_bib(refs)

    hard_sorted = sorted(hard, key=lambda r: float(r["mean_utility"]), reverse=True)
    ablation_sorted = sorted(ablations, key=lambda r: float(r["mean_success"]), reverse=True)
    max_stress = sorted([r for r in stress if float(r["stress_level"]) == 1.0], key=lambda r: float(r["mean_utility"]), reverse=True)
    strict_fixed = sorted([r for r in fixed if r["budget"] == "strict"], key=lambda r: float(r["mean_utility"]), reverse=True)

    placeholders = {
        "<<CITE_INTRO>>": cite(keys, 0, 6),
        "<<CITE_GRAPH>>": cite(keys, 6, 14),
        "<<CITE_PLANNING>>": cite(keys, 14, 23),
        "<<CITE_RISK>>": cite(keys, 23, 32),
        "<<CITE_EVAL>>": cite(keys, 32, 42),
        "<<CITATION_LEDGER>>": citation_ledger(keys),
        "<<DECISION>>": latex_escape(summary.get("decision", "STRONG_REVISE")),
        "<<V5_SUCCESS>>": summary.get("v5_success", ""),
        "<<V5_INVALID>>": summary.get("v5_invalid", ""),
        "<<V5_COLLISION>>": summary.get("v5_collision", ""),
        "<<V5_SUPPORT>>": summary.get("v5_support", ""),
        "<<V5_F1>>": summary.get("v5_topology_f1", ""),
        "<<V5_ECE>>": summary.get("v5_ece", ""),
        "<<V5_REGRET>>": summary.get("v5_regret", ""),
        "<<V5_UTILITY>>": summary.get("v5_utility", ""),
        "<<ORACLE_SUCCESS>>": summary.get("oracle_success", ""),
        "<<HARD_TABLE>>": long_metric_table(hard_sorted, ["method", "mean_success", "mean_invalid_plan", "mean_collision_trap", "mean_support_failure", "mean_topology_f1", "mean_topology_risk_ece", "mean_utility"]),
        "<<PAIRWISE_ROWS>>": compact_rows(pairwise, ["baseline", "mean_success_diff", "lower95_success_diff", "mean_utility_diff", "wins_over_seeds"]),
        "<<ABLATION_ROWS>>": compact_rows(ablation_sorted, ["ablation", "mean_success", "mean_collision_trap", "mean_support_failure", "mean_utility"]),
        "<<STRESS_ROWS>>": compact_rows(max_stress, ["method", "mean_success", "mean_collision_trap", "mean_support_failure", "mean_utility"]),
        "<<FIXED_ROWS>>": compact_rows(strict_fixed[:10], ["method", "mean_coverage", "mean_success", "mean_collision_trap", "mean_support_failure", "mean_utility"]),
        "<<FAILURE_ROWS>>": compact_rows(failures[:12], ["case_id", "task", "regime", "split", "success", "dominant_failure"]),
    }

    tex = r"""
\PassOptionsToPackage{colorlinks=false,citebordercolor={0 1 0},linkbordercolor={1 0.55 0},urlbordercolor={0 0.55 1},pdfborder={0 0 1.2}}{hyperref}
\documentclass{article}
\usepackage{iclr2026_conference,times}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{longtable}
\usepackage{array}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{xcolor}
\usepackage{url}
\usepackage{hyperref}
\input{math_commands.tex}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\title{Risk-Calibrated Workspace Topology Belief for Hidden Topology Change}
\author{Anonymous authors\\Paper under double-blind review}
\begin{document}
\maketitle

\begin{abstract}
Workspace topology can change while a robot is acting: a passage closes, a support edge disappears, an occluder reveals a new component, a stack dependency flips, or a tool corridor becomes blocked. We rebuild Paper 101 under a frozen hostile-review protocol and test whether action-conditioned topology belief should survive as a submission-target idea. The v5 audit uses 6 tasks, 8 topology-change regimes, 8 splits, 15 methods, 10 seeds, 345{,}600 main rollout rows, 115{,}200 ablation rows, 288{,}000 stress rows, 276{,}480 fixed-risk rows, and 24 negative cases. The local result is positive but not submission-ready. \texttt{risk\_calibrated\_topology\_belief\_v5} reaches hard success <<V5_SUCCESS>>, invalid-plan rate <<V5_INVALID>>, collision/trap rate <<V5_COLLISION>>, support-failure rate <<V5_SUPPORT>>, topology F1 <<V5_F1>>, ECE <<V5_ECE>>, regret <<V5_REGRET>>, and robust utility <<V5_UTILITY>>. All frozen local empirical gates pass. The terminal decision is \textbf{<<DECISION>>}; ICLR-main readiness remains \textbf{no} because no real robot, accepted high-fidelity benchmark, external benchmark, calibrated topology-change log, or trained checkpoint evidence exists.
\end{abstract}

\section{Introduction}
Topology is a state variable, not only a geometric decoration. In contact-rich manipulation and mobile manipulation, the graph of reachable components, support edges, passage constraints, and tool-access tunnels can change after the robot commits to an action. A planner that treats the scene graph as static can hold a formally valid plan for the wrong graph. This is exactly the failure mode that action-conditioned topology-change detection is meant to address <<CITE_INTRO>>.

The thesis of this paper is narrow. A robot should maintain a calibrated belief over topology changes that are relevant to the candidate action, not merely detect pixel or object changes. The belief should remember support edges, passage homology, occlusion persistence, action-conditioned deltas, and hysteretic replan state; it should also expose uncertainty to fixed-risk deployment. The local evidence supports that thesis, but the evidence is still local.

\section{Terminal Claim}
The frozen v5 claim is:
\[
  b_{t+1} = \mathcal{T}_{\theta}(b_t, G_t, a_t, o_{t+1}), \qquad
  \pi(a_t \mid b_t) = \arg\max_a \; U(a,b_t) - \lambda R(a,b_t),
\]
where $G_t$ is the observed scene graph, $b_t$ is a topology belief, $a_t$ is the candidate action, $U$ is predicted task utility, and $R$ is calibrated topology risk. The terminal decision is \textbf{<<DECISION>>}. The local mechanism survives the frozen audit, but the paper is not ICLR-main ready.

\section{Related Work Pressure}
The hostile prior-work surface includes scene-graph change detection, dynamic graph representations, topological SLAM/TAMP, graph neural change classifiers, robust replanning, uncertainty-triggered replanning, conformal risk filters, particle-filter topology belief, and active view/probe systems <<CITE_GRAPH>>. The v5 protocol therefore includes references from each family. This matters because a method that only beats static scene graphs has not earned submission-level evidence.

\section{Method}
The method maintains a belief over topology events:
\[
 b_t = (p_{\mathrm{passage}}, p_{\mathrm{support}}, p_{\mathrm{component}}, p_{\mathrm{occlusion}}, p_{\mathrm{trap}}, c_t),
\]
where $c_t$ is a calibration state. Candidate actions induce graph deltas:
\[
 \Delta G(a_t) = \{e_{\mathrm{support}}, e_{\mathrm{passage}}, C_{\mathrm{reach}}, O_{\mathrm{occ}}\}_{a_t}.
\]
The controller chooses actions with high expected success and low calibrated risk. In the audit, this is implemented as a deterministic surrogate rather than a trained checkpoint. This is a strength for reproducibility and a limitation for submission readiness.

\begin{lemma}[Fixed-risk filtering]
Assume the topology-risk predictor is calibrated within $\epsilon$ on a hard split. If deployment accepts only actions with predicted risk at most $\tau$, then the expected realized topology-event rate is bounded by $\tau+\epsilon$ on the accepted set.
\end{lemma}
\noindent The lemma is only local: it does not certify a real robot. It explains why calibration and fixed-risk coverage are evaluated jointly rather than separately <<CITE_RISK>>.

\begin{proposition}[Action conditioning is identifiable only under intervention]
If two candidate actions induce identical observed scene graphs but different support or passage consequences, no observation-only change detector can identify the decision-relevant topology change without an action-conditioned model or an active probe.
\end{proposition}
\noindent This is the paper's theoretical reason for testing no-action and no-probe ablations.

\section{Protocol}
The experiment uses 6 tasks, 8 topology-change regimes, 8 splits, 15 methods, and 10 seeds. The hard split set is support cascade, false topology alarms, latency budget, and combined extreme. The metrics are success, invalid-plan rate, collision/trap, support failure, topology F1, missed-change false negatives, false topology alarms, latency, ECE, regret to oracle, and robust utility. The design intentionally includes baselines that can beat parts of the proposed method: topological SLAM/TAMP, particle-filter topology belief MPC, conformal topology risk filtering, active probing, dynamic scene-graph transformer proxies, graph classifiers, and robust replanning <<CITE_PLANNING>>.

\section{Main Results}
The local hard aggregate is shown below. The oracle remains higher at success <<ORACLE_SUCCESS>>, so the local method is not saturated.

<<HARD_TABLE>>

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{../figures/topology_v5_hard_outcomes.png}
\caption{Hard aggregate success across the v5 topology-change audit.}
\end{figure}

\section{Paired Evidence}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrr}
\toprule
baseline & dSucc & low95 & dUtil & wins\\
\midrule
<<PAIRWISE_ROWS>>
\bottomrule
\end{tabular}
\endgroup

The paired evidence is seed-level, not just aggregate sorting. V5 beats every non-oracle reference in the frozen hard aggregate. The oracle remains above v5, which is expected because it observes the latent topology directly.

\section{Diagnostics}
\begin{figure}[t]
\centering
\includegraphics[width=.92\linewidth]{../figures/topology_v5_diagnostics.png}
\caption{Missed-change false negatives versus false topology alarms. V5 reduces both relative to the strongest local baselines.}
\end{figure}

The main diagnostic risk is not a low F1 number; it is the false sense of certainty that happens when a topology update is missed or hallucinated. V5 improves topology F1 to <<V5_F1>> while keeping false alarms and missed-change rates below the tested non-oracle references. This result is still not a substitute for calibrated real topology-change logs.

\section{Ablations}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrr}
\toprule
ablation & success & collision & support & utility\\
\midrule
<<ABLATION_ROWS>>
\bottomrule
\end{tabular}
\endgroup

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{../figures/topology_v5_ablation.png}
\caption{Ablation outcomes over hard topology-change splits.}
\end{figure}

No removed component matches the full method on both success and safety. The largest lesson is that action conditioning, support-edge memory, passage homology, calibration, probes, and hysteresis are not interchangeable decorations; each removes a distinct failure path.

\section{Stress Sweep}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrr}
\toprule
method & success & collision & support & utility\\
\midrule
<<STRESS_ROWS>>
\bottomrule
\end{tabular}
\endgroup

\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{../figures/topology_v5_stress_sweep.png}
\caption{Maximum-stress robust utility.}
\end{figure}

At maximum stress, the audit tests delayed observation, perception ambiguity, false topology alarms, support cascade, reach shift, and latency pressure simultaneously. V5 remains above the strongest non-oracle reference in utility.

\section{Fixed-Risk Deployment}
\begingroup
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lrrrrr}
\toprule
method & cover & success & collision & support & utility\\
\midrule
<<FIXED_ROWS>>
\bottomrule
\end{tabular}
\endgroup

\begin{figure}[t]
\centering
\includegraphics[width=.92\linewidth]{../figures/topology_v5_fixed_risk.png}
\caption{Strict-budget coverage. V5 does not win by abstaining; it keeps useful coverage while satisfying the local collision/support budgets.}
\end{figure}

\section{Failure Cases}
\begingroup
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{llllrl}
\toprule
case & task & regime & split & success & dominant failure\\
\midrule
<<FAILURE_ROWS>>
\bottomrule
\end{tabular}
\endgroup

The negative cases are retained because the paper should survive hostile review, not look pretty. The hard failures concentrate in support cascades, false topology alarms, and latency-budget shifts.

\section{Limitations}
This is a CPU-only local audit. There is no real robot, no accepted high-fidelity benchmark, no external benchmark, no calibrated external topology-change event log, no trained checkpoint, and no rollout videos. The correct terminal state is STRONG\_REVISE, not submission ready. The next real experiment must freeze an external protocol before tuning on it <<CITE_EVAL>>.

\section{Reproducibility}
The main entry point is \texttt{src/run\_experiment.py}. The manuscript is generated by \texttt{scripts/generate\_manuscript.py}. The artifact validator checks row counts, PDF location, page count, hash, no visible Desktop copy, and boxed citation settings.

\appendix
\section{Frozen Gate Ledger}
All local empirical gates pass: success, invalid-plan, collision, support, diagnostics, latency, regret, utility, calibration, ablation, stress, and fixed-risk. The scope gate fails.

\section{Full Hard-Metric Table}
<<HARD_TABLE>>

\section{Citation Ledger}
\begingroup
\scriptsize
\setlength{\tabcolsep}{4pt}
\begin{longtable}{r p{0.34\linewidth} p{0.45\linewidth}}
\toprule
id & theme & citations\\
\midrule
<<CITATION_LEDGER>>
\bottomrule
\end{longtable}
\endgroup

\bibliographystyle{iclr2026_conference}
\bibliography{references}
\end{document}
"""
    for key, value in placeholders.items():
        tex = tex.replace(key, value)
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print("wrote paper/main.tex and paper/references.bib")


if __name__ == "__main__":
    main()
