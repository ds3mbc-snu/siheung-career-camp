"""Small helper functions for the student lecture notebooks.

The notebooks keep the lesson flow in visible cells.  This file only holds
repeated mechanics such as CSV loading, graph search, and plotting.
"""

from __future__ import annotations

import csv
import heapq
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def find_project_root() -> Path:
    current = Path.cwd().resolve()
    for path in [current, *current.parents]:
        if (path / "data/routes/routes_long.csv").is_file():
            return path
        if (path / "output/00_merged_edges.csv").is_file():
            return path
    raise FileNotFoundError("project root 또는 notebooks 배포 폴더를 찾을 수 없습니다.")


def output_dir(project_root: Path) -> Path:
    if (project_root / "data/routes/routes_long.csv").is_file():
        out = project_root / "analysis/output"
    else:
        out = project_root / "output"
    out.mkdir(parents=True, exist_ok=True)
    return out


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    if fields is None:
        fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def as_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def load_current_data(project_root: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    if (project_root / "data/routes/routes_long.csv").is_file():
        stations = read_csv(project_root / "data/routes/station_index.csv")
        w1 = read_csv(project_root / "data/routes/routes_long.csv")
        w2 = {row["pair_id"]: row for row in read_csv(project_root / "data/output/w2/latest/W2_pairs_long.csv")}
        w3 = {row["pair_id"]: row for row in read_csv(project_root / "data/output/w3/latest/W3_pairs_long.csv")}
        w4 = {row["pair_id"]: row for row in read_csv(project_root / "data/output/w4/latest/W4_pairs_long.csv")}
        edges: list[dict[str, object]] = []
        for row in w1:
            pair_id = row["pair_id"]
            edges.append(
                {
                    "pair_order": int(row["pair_order"]),
                    "pair_id": pair_id,
                    "from_order": int(row["from_order"]),
                    "from_station_id": row["from_station_id"],
                    "from_station_name": row["from_station_name"],
                    "to_order": int(row["to_order"]),
                    "to_station_id": row["to_station_id"],
                    "to_station_name": row["to_station_name"],
                    "w1_distance_m": as_float(row, "distance_m"),
                    "distance_km": as_float(row, "distance_m") / 1000.0,
                    "w2_average_lanes": as_float(w2[pair_id], "w2_average_lanes"),
                    "w3_protection_proxy": as_float(w3[pair_id], "w3_protection_proxy"),
                    "w3_child_protection_proxy": as_float(w3[pair_id], "w3_child_protection_proxy"),
                    "w3_senior_protection_proxy": as_float(w3[pair_id], "w3_senior_protection_proxy"),
                    "w3_disabled_protection_proxy": as_float(w3[pair_id], "w3_disabled_protection_proxy"),
                    "w3_classification": w3[pair_id]["result_classification"],
                    "w4_average_absolute_grade_pct": as_float(w4[pair_id], "w4_average_absolute_grade_pct"),
                    "w4_classification": w4[pair_id]["result_classification"],
                }
            )
    else:
        edges = read_csv(output_dir(project_root) / "00_merged_edges.csv")
        for edge in edges:
            for key in ["pair_order", "from_order", "to_order"]:
                edge[key] = int(edge[key])
            for key in numeric_edge_columns():
                if key in edge:
                    edge[key] = float(edge[key])
        by_id: dict[str, dict[str, object]] = {}
        for edge in edges:
            by_id[str(edge["from_station_id"])] = {
                "station_order": edge["from_order"],
                "station_id": edge["from_station_id"],
                "station_name": edge["from_station_name"],
            }
            by_id[str(edge["to_station_id"])] = {
                "station_order": edge["to_order"],
                "station_id": edge["to_station_id"],
                "station_name": edge["to_station_name"],
            }
        stations = [by_id[key] for key in sorted(by_id)]
    return stations, edges


def numeric_edge_columns() -> list[str]:
    return [
        "w1_distance_m",
        "distance_km",
        "w2_average_lanes",
        "w3_protection_proxy",
        "w3_child_protection_proxy",
        "w3_senior_protection_proxy",
        "w3_disabled_protection_proxy",
        "w4_average_absolute_grade_pct",
        "distance_norm",
        "lane_inverse_norm",
        "lane_penalty_norm",
        "protection_norm",
        "slope_norm",
        "scenario_cost",
    ]


def print_table(rows: list[dict[str, object]], columns: list[str], limit: int = 8) -> None:
    rows = rows[:limit]
    widths = {col: max(len(col), *(len(str(row.get(col, ""))) for row in rows)) for col in columns}
    print(" | ".join(col.ljust(widths[col]) for col in columns))
    print("-+-".join("-" * widths[col] for col in columns))
    for row in rows:
        print(" | ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns))


def minmax(values: list[float]) -> list[float]:
    values = [float(value) for value in values]
    low, high = min(values), max(values)
    if math.isclose(low, high):
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def max_scale(values: list[float]) -> list[float]:
    values = [float(value) for value in values]
    high = max(values)
    if high <= 0 or math.isclose(high, 0.0):
        return [0.0 for _ in values]
    return [value / high for value in values]


def inverse_lane_penalty(lanes: float) -> float:
    lanes = float(lanes)
    if lanes <= 0:
        return 1.0
    return min(1.0, 1.0 / lanes)


def slope_limit_penalty(grade_pct: float, limit_pct: float = 6.0, excess_penalty: float = 30.0) -> float:
    grade_pct = float(grade_pct)
    if grade_pct > limit_pct:
        return excess_penalty
    return grade_pct / limit_pct


def score_edges(
    edges: list[dict[str, object]],
    weights: dict[str, float],
    min_average_lanes: float = 0.0,
) -> list[dict[str, object]]:
    filtered_edges = [
        edge for edge in edges
        if float(edge["w2_average_lanes"]) >= float(min_average_lanes)
    ]
    if not filtered_edges:
        raise ValueError("no edges remain after applying min_average_lanes")

    distance = max_scale([float(edge["w1_distance_m"]) for edge in filtered_edges])
    lane_inverse = [inverse_lane_penalty(float(edge["w2_average_lanes"])) for edge in filtered_edges]
    protection = max_scale([float(edge["w3_protection_proxy"]) for edge in filtered_edges])
    slope = [slope_limit_penalty(float(edge["w4_average_absolute_grade_pct"])) for edge in filtered_edges]
    rows: list[dict[str, object]] = []
    for idx, edge in enumerate(filtered_edges):
        item = dict(edge)
        item["distance_norm"] = distance[idx]
        item["lane_inverse_norm"] = lane_inverse[idx]
        item["lane_penalty_norm"] = lane_inverse[idx]
        item["protection_norm"] = protection[idx]
        item["slope_norm"] = slope[idx]
        item["scenario_cost"] = (
            weights["distance"] * distance[idx]
            + weights["lane_capacity"] * lane_inverse[idx]
            + weights["protection_proxy"] * protection[idx]
            + weights["preliminary_slope"] * slope[idx]
        )
        rows.append(item)
    return sorted(rows, key=lambda item: (float(item["scenario_cost"]), float(item["w1_distance_m"])))


def station_ids(stations: list[dict[str, object]]) -> list[str]:
    return [str(station["station_id"]) for station in stations]


def adjacency(nodes: list[str], edges: list[dict[str, object]], weight: str) -> dict[str, list[tuple[str, float, dict[str, object]]]]:
    graph: dict[str, list[tuple[str, float, dict[str, object]]]] = {node: [] for node in nodes}
    for edge in edges:
        u = str(edge["from_station_id"])
        v = str(edge["to_station_id"])
        w = float(edge[weight])
        graph.setdefault(u, []).append((v, w, edge))
        graph.setdefault(v, []).append((u, w, edge))
    return graph


def components(nodes: list[str], edges: list[dict[str, object]], weight: str = "scenario_cost") -> list[list[str]]:
    graph = adjacency(nodes, edges, weight) if edges else {node: [] for node in nodes}
    seen: set[str] = set()
    result: list[list[str]] = []
    for node in nodes:
        if node in seen:
            continue
        stack = [node]
        seen.add(node)
        comp: list[str] = []
        while stack:
            cur = stack.pop()
            comp.append(cur)
            for nxt, _, _ in graph.get(cur, []):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        result.append(sorted(comp))
    return sorted(result, key=len, reverse=True)


class UnionFind:
    def __init__(self, nodes: list[str]):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node: str) -> str:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def mst(nodes: list[str], edges: list[dict[str, object]], weight: str) -> list[dict[str, object]]:
    uf = UnionFind(nodes)
    selected: list[dict[str, object]] = []
    for edge in sorted(edges, key=lambda item: (float(item[weight]), float(item["w1_distance_m"]))):
        if uf.union(str(edge["from_station_id"]), str(edge["to_station_id"])):
            selected.append(edge)
            if len(selected) == len(nodes) - 1:
                break
    return selected


def dijkstra(nodes: list[str], edges: list[dict[str, object]], source: str, weight: str) -> dict[str, float]:
    graph = adjacency(nodes, edges, weight)
    dist = {node: math.inf for node in nodes}
    dist[source] = 0.0
    queue = [(0.0, source)]
    while queue:
        cost, node = heapq.heappop(queue)
        if cost > dist[node]:
            continue
        for neighbor, edge_weight, _ in graph.get(node, []):
            new_cost = cost + edge_weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
    return dist


def shortest_path_length(nodes: list[str], edges: list[dict[str, object]], source: str, target: str, weight: str) -> float:
    return dijkstra(nodes, edges, source, weight)[target]


def all_pair_metrics(nodes: list[str], reference_edges: list[dict[str, object]], structure_edges: list[dict[str, object]]) -> tuple[dict[str, float], list[dict[str, object]]]:
    ref_dist = {node: dijkstra(nodes, reference_edges, node, "distance_km") for node in nodes}
    sub_dist = {node: dijkstra(nodes, structure_edges, node, "distance_km") for node in nodes}
    rows: list[dict[str, object]] = []
    path_values: list[float] = []
    stretch_values: list[float] = []
    for i, u in enumerate(nodes):
        for v in nodes[i + 1 :]:
            ref = ref_dist[u][v]
            sub = sub_dist[u][v]
            stretch = sub / ref if ref > 0 else 1.0
            rows.append({"from_station_id": u, "to_station_id": v, "reference_distance_km": ref, "structure_distance_km": sub, "distance_stretch": stretch})
            path_values.append(sub)
            stretch_values.append(stretch)
    return {
        "average_shortest_path_km": float(np.mean(path_values)),
        "diameter_km": float(max(path_values)),
        "mean_distance_stretch": float(np.mean(stretch_values)),
        "max_distance_stretch": float(max(stretch_values)),
    }, rows


def bridges(nodes: list[str], edges: list[dict[str, object]]) -> list[tuple[str, str]]:
    edge_keys = {tuple(sorted((str(edge["from_station_id"]), str(edge["to_station_id"])))) for edge in edges}
    result = []
    for a, b in sorted(edge_keys):
        reduced = [edge for edge in edges if tuple(sorted((str(edge["from_station_id"]), str(edge["to_station_id"])))) != (a, b)]
        if len(components(nodes, reduced)[0]) < len(nodes):
            result.append((a, b))
    return result


def greedy_spanner(nodes: list[str], edges: list[dict[str, object]], t: float) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    for edge in sorted(edges, key=lambda item: float(item["scenario_cost"])):
        u = str(edge["from_station_id"])
        v = str(edge["to_station_id"])
        if not selected or math.isinf(shortest_path_length(nodes, selected, u, v, "scenario_cost")):
            selected.append(edge)
            continue
        current = shortest_path_length(nodes, selected, u, v, "scenario_cost")
        if current > t * float(edge["scenario_cost"]):
            selected.append(edge)
    return selected


def degree_limited_kruskal(nodes: list[str], edges: list[dict[str, object]], max_degree: int) -> list[dict[str, object]]:
    uf = UnionFind(nodes)
    degree: Counter[str] = Counter()
    selected: list[dict[str, object]] = []
    for edge in sorted(edges, key=lambda item: float(item["scenario_cost"])):
        u = str(edge["from_station_id"])
        v = str(edge["to_station_id"])
        if degree[u] >= max_degree or degree[v] >= max_degree:
            continue
        if uf.union(u, v):
            selected.append(edge)
            degree[u] += 1
            degree[v] += 1
            if len(selected) == len(nodes) - 1:
                break
    return selected


def build_candidate(stations: list[dict[str, object]], scored: list[dict[str, object]]) -> tuple[list[str], list[str], list[dict[str, object]]]:
    nodes = station_ids(stations)
    comps = components(nodes, scored)
    active_nodes = comps[0]
    unresolved = [node for comp in comps[1:] for node in comp]
    active_edges = [edge for edge in scored if edge["from_station_id"] in active_nodes and edge["to_station_id"] in active_nodes]
    tree = mst(active_nodes, active_edges, "scenario_cost")
    candidate = []
    for edge in tree:
        item = dict(edge)
        item["selection_role"] = "SCENARIO_MST"
        candidate.append(item)
    return active_nodes, unresolved, candidate


def structure_metrics(name: str, nodes: list[str], reference_edges: list[dict[str, object]], selected_edges: list[dict[str, object]]) -> tuple[dict[str, object], list[dict[str, object]]]:
    connected = len(components(nodes, selected_edges)) == 1
    if connected:
        metric, stretch_rows = all_pair_metrics(nodes, reference_edges, selected_edges)
        bridge_count = len(bridges(nodes, selected_edges))
    else:
        metric = {"average_shortest_path_km": math.nan, "diameter_km": math.nan, "mean_distance_stretch": math.nan, "max_distance_stretch": math.nan}
        stretch_rows = []
        bridge_count = math.nan
    row = {
        "structure": name,
        "connected": connected,
        "edge_count": len(selected_edges),
        "total_w1_distance_km": sum(float(edge["distance_km"]) for edge in selected_edges),
        "total_composite_cost": sum(float(edge["scenario_cost"]) for edge in selected_edges),
        "bridge_count": bridge_count,
        "max_degree": max(Counter(endpoint for edge in selected_edges for endpoint in (edge["from_station_id"], edge["to_station_id"])).values()) if selected_edges else 0,
        **metric,
    }
    for stretch in stretch_rows:
        stretch["structure"] = name
    return row, stretch_rows


def plot_network(stations: list[dict[str, object]], edges: list[dict[str, object]], output: Path, title: str) -> None:
    pos = {
        str(station["station_id"]): (float(station["longitude"]), float(station["latitude"]))
        for station in stations
        if "longitude" in station and "latitude" in station
    }
    if not pos:
        return
    fig, ax = plt.subplots(figsize=(11, 9))
    for edge in edges:
        u, v = str(edge["from_station_id"]), str(edge["to_station_id"])
        color = "#2563eb" if edge.get("selection_role") == "SCENARIO_MST" else "#f97316"
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=color, alpha=0.65, linewidth=1.2)
    ax.scatter([p[0] for p in pos.values()], [p[1] for p in pos.values()], s=16, color="#111827")
    for sid, (x, y) in pos.items():
        ax.text(x, y, sid.replace("ST", ""), fontsize=5)
    ax.set_title(title)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)
