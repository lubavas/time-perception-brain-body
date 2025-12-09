# time-perception-brain-body
Tools and analysis code for a multimodal physiology study in teenagers, combining EEG, ECG, PPG, breathing, and behavioral data to investigate connection between time perception, external stumuli, and bodily states.

---

## Project Overview

This repository contains the code for analyzing a multimodal dataset collected in teenagers.  
The data include:

- EEG
- ECG & PPG
- Breathing
- Task/behavioral responses
- (Optionally) Eye-tracking

> **Note:** Raw data are not included in this repository for privacy reasons.

---

## Main Goals

- (in progress) Preprocess behavioral data, fit psychometric curves, identify PSEs
- Preprocess EEG, define and implement data inclusion criteria
- Preprocess ECG, breathing, PPG, eyetracking signals
- Synchronize physiological and behavioral data
- Extract relevant features (e.g. HRV, ERPs, spectral power)
- Test hypotheses about brain-body interactions
- Provide reproducible analysis pipelines in Python

---

## License and Usage Notice
This repository is shared for transparency and academic visibility only.
The code and materials are not licensed for reuse, modification, or redistribution.  
Please contact the author if you are interested in collaboration.

---

## Repository Structure

```text
.
|-- notebooks/
|-- src/                 # Python modules
|   |-- parsing/         # codes for data import
|   |-- processing/      # codes for data preprocessing
|   -- plotting/        # for plotting
|-- data/                # not tracked in git
|   |-- raw/
|   |   |-- beh/         # raw behavioral data (PsychoPy)
|   |   -- eeg-edf/      # EEG data in EDF
|   |       |-- 1star/
|   |       |-- 2min1/
|   |       |-- 2min2/
|   |       |-- 3video/
|   |       |-- 4star/
|   |       |-- 5min1/
|   |       -- 5min2/
|   -- parsed/
|       |-- beh/
|       -- beh_orig/
|-- experiment_archives/ # task scenarios (not tracked in git)
|-- README.md
-- requirements.txt
`

## Batch parsing PsychoPy behavioral logs

Run the batch helper to convert all `.log` / `.log.gz` files to CSVs:

**From Python**
```python
import batch_parse_psychopy as bp

results = bp.batch_parse_logs(
    input_dir="data/raw/beh",
    output_dir="data/parsed/beh",
    pattern="*.log*",
    overwrite=False,
)
bp._print_summary(results)  # or inspect results list directly
```