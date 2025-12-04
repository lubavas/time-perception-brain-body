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
├─ notebooks/
├─ src/
├─ data/            # not tracked in git
├─ README.md
└─ requirements.txt
