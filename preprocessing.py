"""
Converts (time, hz) output to comparable format
1. hz -> midi conversion
2. group frames to coherent notation
3. fold all MIDI pitches to a reference octave

Command line usage:
conversion.py <--p-ref 60> input_file.txt output_file.txt
"""


import numpy as np

def hz_to_midi(freq: np.ndarray) -> np.ndarray:
    """Vectorised Hz → MIDI (A4=440). Non-positive values become -1"""

    with np.errstate(divide="ignore", invalid="ignore"):
        midi = np.where(freq > 0, 69 + 12 * np.log2(freq / 440.0), -1)
    return np.round(midi).astype(int)

def group_notes(path: str, gap_threshold: float = 0.1, pitch_tolerance: int = 1) -> list[tuple[float, int]]:
    """
    Load a raw frame file (time_s  freq_hz) and collapse consecutive frames into single notes
    Grouping rules extend the current group while
        -time gap to next frame  < gap_threshold   (seconds)
        -MIDI pitch stays within +-pitch_tolerance  (semitones)

    Returns list of (onset_time, midi_note) for each group
    """

    data = np.loadtxt(path, usecols=(0, 1))          # shape (n, 2)
    times, pitches = data[:, 0], hz_to_midi(data[:, 1])

    groups: list[tuple[float, int]] = []
    start_idx = 0

    for i in range(1, len(times)):
        gap   = times[i] - times[i - 1]
        pdiff = abs(int(pitches[i]) - int(pitches[start_idx]))
        if gap >= gap_threshold or pdiff > pitch_tolerance:
            groups.append((float(times[start_idx]), int(pitches[start_idx])))
            start_idx = i

    groups.append((float(times[start_idx]), int(pitches[start_idx])))  # final group
    groups = [(t, m) for t, m in groups if m != -1]
    return groups

def octave_squish(notes: list[tuple[float, int]], p_ref: int = 40) -> list[tuple[float, int]]:
    """
    fold all MIDI pitches into the octave [p_ref, p_ref + 11]
    
    maps every pitch to its pitch class within the reference octave, eliminating octave displacement errors
 
    equation: p' = ((p - p_ref) % 12) + p_ref
    """

    return [(t, ((m - p_ref) % 12) + p_ref) for t, m in notes]

if __name__ == "__main__":
    import pathlib, argparse
 
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output",  nargs="?")
    parser.add_argument("--p-ref", type=int, default=60)
    args = parser.parse_args()
 
    out_path = args.output or pathlib.Path(args.input).stem + "_grouped.txt"
 
    notes = group_notes(args.input)
    notes = octave_squish(notes, p_ref=args.p_ref)

    with open(out_path, "w") as f:
        f.writelines(f"{t:.6f} {m}\n" for t, m in notes)

    print(f"Grouped {len(notes)} notes → {out_path}")