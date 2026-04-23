import numpy as np
from sklearn.ensemble import IsolationForest

EVENT_TYPE_MAP = {
    "DDoS": 10,
    "Phishing": 8,
    "Malware": 9,
    "SQL Injection": 7,
    "Brute Force": 8,
    "Ransomware": 10,
    "Port Scan": 6,
    "Suspicious Login": 7,
}


def build_matrix(events):
    matrix = []
    for event in events:
        matrix.append([
            EVENT_TYPE_MAP.get(event.event_type, 5),
            event.severity,
            event.bytes_in,
            event.bytes_out,
        ])
    return np.array(matrix, dtype=float)


def is_anomaly(candidate, recent_events):
    if len(recent_events) < 30:
        return candidate[1] >= 9

    X = build_matrix(recent_events)
    model = IsolationForest(contamination=0.07, random_state=42)
    model.fit(X)
    prediction = model.predict([candidate])[0]
    return prediction == -1
