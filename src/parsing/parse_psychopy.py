import os
import re
import csv
import gzip

# ---------------------------
# Helpers to read PsychoPy log
# ---------------------------

def iter_log_events(log_path):
    """Yield (time, event_type, message) for each proper log line."""
    opener = gzip.open if log_path.endswith(".gz") else open
    with opener(log_path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            try:
                t = float(parts[0])
            except ValueError:
                continue
            yield t, parts[1], parts[2]

def extract_experiment_datetime(log_path):
    """Return experiment date/time parsed from the log filename."""
    filename = os.path.basename(log_path)
    m = re.search(r"(\d{4}-\d{2}-\d{2})_(\d{2})h(\d{2})\.(\d{2})\.(\d{3})", filename)
    if not m:
        raise ValueError(f"Could not extract experiment datetime from filename: {filename}")
    date_part, hour, minute, second, ms = m.groups()
    time_part = f"{hour}:{minute}:{second}.{ms}"
    return {"experiment_date": date_part, "experiment_time": time_part}

def extract_periods(events, stim_name):
    """Extract (onset, offset) periods for stimuli based on autoDraw true/null."""
    on = None
    periods = []
    for t, etype, msg in events:
        if f"{stim_name}: autoDraw = true" in msg and on is None:
            on = t
        elif f"{stim_name}: autoDraw = null" in msg and on is not None:
            periods.append((on, t))
            on = None
    return periods

# ---------------------------
# Main parsing logic
# ---------------------------

def parse_time_interval_log(log_path):
    events = list(iter_log_events(log_path))
    metadata = extract_experiment_datetime(log_path)

    # Extract onset/offset periods
    first_periods = extract_periods(events, "firstImg")
    second_periods = extract_periods(events, "secondImg")
    response_periods = extract_periods(events, "responseImg")

    # Key responses
    key_events = []
    for t, etype, msg in events:
        if etype == "DATA":
            m = re.match(r"Keydown:\s*(.*)", msg)
            if m:
                key_events.append((t, m.group(1)))

    trials = []
    n = min(len(first_periods), len(second_periods), len(response_periods))

    for i in range(n):
        stim1_on, stim1_off = first_periods[i]
        stim2_on, stim2_off = second_periods[i]
        resp_on, resp_off = response_periods[i]

        stim1_dur = stim1_off - stim1_on
        stim2_dur = stim2_off - stim2_on
        delta = stim1_dur - stim2_dur

        choice_key = None
        choice_time = None
        for t, key in key_events:
            if key in ("1", "2") and resp_on <= t <= resp_off + 1.0:
                choice_key = key
                choice_time = t
                break
        choice_rt = choice_time - resp_on if choice_time is not None else None

        trials.append({
            "experiment_date": metadata["experiment_date"],
            "experiment_time": metadata["experiment_time"],
            "stim1_onset": stim1_on,
            "stim1_offset": stim1_off,
            "stim2_onset": stim2_on,
            "stim2_offset": stim2_off,
            "stim1_duration": stim1_dur,
            "stim2_duration": stim2_dur,
            "stim_dur_delta": delta,
            "choice_key": choice_key,
            "choice_time": choice_time,
            "choice_rt": choice_rt,
        })

    return trials

def save_trials_to_csv(trials, csv_path):
    if not trials:
        raise ValueError("No trials parsed.")

    fieldnames = [
        "experiment_date",
        "experiment_time",
        "stim1_onset",
        "stim1_offset",
        "stim2_onset",
        "stim2_offset",
        "stim1_duration",
        "stim2_duration",
        "stim_dur_delta",
        "choice_key",
        "choice_time",
        "choice_rt",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trials)

# ---------------------------
# Example usage
# ---------------------------

if __name__ == "__main__":
    log_file = "PARTICIPANT_time_perception_2Phases_ENRU_2021-07-16_09h56.52.759.log.gz"
    out_csv = "behavior.csv"

    trials = parse_time_interval_log(log_file)
    save_trials_to_csv(trials, out_csv)
    print(f"Saved {len(trials)} trials to {out_csv}")
