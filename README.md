# Thesis-Algorithms

Two scripts for comparing melodies. Run them in order.

## Requirements

```
numpy
```

## preprocessing.py

Converts raw `(time_s, hz)` software output into a grouped, octave-folded MIDI note file.

```bash
python preprocessing.py input_file.txt output_file.txt
```

```bash
# With optional p-ref (default: 60)
python preprocessing.py input_file.txt output_file.txt --p-ref 40
```

## Arguments
|----------|-------------|
| `input_file.txt` | Raw pitch file with columns `time_s freq_hz` |
| `output_file.txt` | (Optional) Output path. Defaults to `<input>_grouped.txt` |
| `--p-ref` | Reference MIDI pitch for octave folding (default: `60`) |

## dtw.py

Computes a DTW-based melody similarity score between the ground truth file and preprosessed file. Returns a value in `[0, 1]` where `1` is identical.

```bash
python dtw.py file_a.txt file_b.txt
```

```bash
# With optional scale and CSV output
python dtw.py file_a.txt file_b.txt --scale 3.0 --output results.csv
```

## Arguments
|----------|-------------|
| `file_a.txt` | First preprocessed melody file |
| `file_b.txt` | Second preprocessed melody file |
| `--scale` | Semitone sensitivity scale for similarity decay (default: `3.0`) |
| `--output` | (Optional) CSV file to append the result to |
