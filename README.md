# Thesis-Algorithms

Two scripts for comparing melodies. Run them in order.

## Requirements

```
numpy
```

## preprocessing.py

Converts raw `(time_s, hz)` output into a grouped, octave-folded MIDI note file.

```bash
python preprocessing.py input_file.txt output_file.txt
```

```bash
# optional p-ref (default: 60 = middle C)
python preprocessing.py input_file.txt output_file.txt --p-ref 40
```

- `input_file.txt` | raw pitch file with columns `time_s freq_hz`
- `output_file.txt` | (optional) output path, defaults to `<input>_grouped.txt`
- `--p-ref` | reference MIDI note for octave folding (default: `60` = midde C)

## dtw.py

Computes a DTW-based melody similarity score between two files. Returns a value in `[0, 1]` where `1` is identical.

```bash
python dtw.py file_a.txt file_b.txt
```

```bash
# optional scale and CSV output
python dtw.py file_a.txt file_b.txt --scale 3.0 --output results.csv
```

- `file_a.txt` | file to compare to
- `file_b.txt` | preprocessed melody file
- `--scale` | semitone sensitivity scale for similarity decay (default: `3.0`)
- `--output` | (optional) CSV file to append the result to
