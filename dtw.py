"""
Compare two melody files (time_s  midi_note) and return a similarity
score in [0, 1] where 1 = identical and 0 = maximally dissimilar

Algorithm: DTW on the pitch sequence only

DTW cost is normalised by the warping path length so scores are
comparable across pairs with different sequence lengths
The raw cost is then mapped to [0,1] via an exponential decay: similarity = exp(-normalised_cost / scale)
where scale (default 3.0) is the sensitivity in semitones

Command line usage:
python compare.py <file_a> <file_b> [--scale 3.0]
"""

import os
import csv
import argparse
import numpy as np


def load_midi(path: str) -> np.ndarray:
    """Return pitch column as float array, filtering out unvoiced (-1) frames"""

    data = np.loadtxt(path)
    pitches = data[:, 1].astype(float)
    return pitches[pitches >= 0]


def dtw_cost(a: np.ndarray, b: np.ndarray) -> tuple[float, int]:
    """
    Standard DTW with an absolute-difference cost matrix
    Returns (total_cost, path_length)
    """

    n, m = len(a), len(b)
    INF = float("inf")

    # Use two rolling rows, space complexity O(n*m) -> O(m)
    prev = np.full(m + 1, INF)
    prev[0] = 0.0
    curr = np.full(m + 1, INF)

    # Also track path length with the same DP
    prev_len = np.zeros(m + 1, dtype=int)
    curr_len = np.zeros(m + 1, dtype=int)

    for i in range(1, n + 1):
        curr[0] = INF
        for j in range(1, m + 1):
            cost = abs(a[i - 1] - b[j - 1])
            best = min(prev[j], curr[j - 1], prev[j - 1])
            curr[j] = cost + best
            if best == prev[j]:
                curr_len[j] = prev_len[j] + 1
            elif best == curr[j - 1]:
                curr_len[j] = curr_len[j - 1] + 1
            else:
                curr_len[j] = prev_len[j - 1] + 1
        prev, curr = curr, prev
        prev_len, curr_len = curr_len, prev_len

    return prev[m], prev_len[m]


def similarity(path_a: str, path_b: str, scale: float = 3.0) -> float:
    """
    Returns melody similarity in [0, 1]
    scale: semitones at which similarity drops to ~exp(-1) ≈ 0.37
    """

    a, b = load_midi(path_a), load_midi(path_b)
    if len(a) == 0 or len(b) == 0:
        return 0.0
    cost, path_len = dtw_cost(a, b)
    normalised = cost / max(path_len, 1)
    return float(np.exp(-normalised / scale))

def append_score(output_file, file_a, file_b, score):
    """Append similarity score to CSV file"""

    file_exists = os.path.isfile(output_file)

    with open(output_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        if not file_exists:
            writer.writerow(["file_a", "file_b", "similarity"])

        writer.writerow([
            file_a,
            file_b,
            f"{score:.4f}"
        ])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_a")
    ap.add_argument("file_b")
    ap.add_argument("--scale", type=float, default=3.0,
                    help="Semitone scale for similarity decay (default 3.0)")
    ap.add_argument("--output", type=str)
    args = ap.parse_args()

    score = similarity(args.file_a, args.file_b, scale=args.scale)
    print(f"Similarity: {score:.4f}")

    if args.output:
        append_score(args.output, args.file_a, args.file_b, score)
        print(f"Score appended to: {args.output}")


if __name__ == "__main__":
    main()