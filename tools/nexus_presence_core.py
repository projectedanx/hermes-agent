import json
import os
import re
from datetime import datetime
import math

class NexusMemoryState:
    def __init__(self, storage_dir="~/.nexus_presence"):
        self.storage_dir = os.path.expanduser(storage_dir)
        os.makedirs(self.storage_dir, exist_ok=True)
        self.him_path = os.path.join(self.storage_dir, "him.json")
        self.ctm_path = os.path.join(self.storage_dir, "ctm.json")
        self.cpl_path = os.path.join(self.storage_dir, "cpl.json")
        self.opp_path = os.path.join(self.storage_dir, "opp.json")
        self._init_defaults()

    def _init_defaults(self):
        if not os.path.exists(self.him_path):
            self.save_him({"voice_fingerprint": {}, "intellectual_identity": {}, "life_context": {}, "drift_detection": {}})
        if not os.path.exists(self.ctm_path):
            self.save_ctm({"communities": [], "topology_insights": {}})
        if not os.path.exists(self.cpl_path):
            self.save_cpl({"posts": [], "pattern_library": {}})
        if not os.path.exists(self.opp_path):
            self.save_opp({"active_opportunities": [], "financial_context": {}})

    def load_him(self): return json.load(open(self.him_path))
    def save_him(self, data): json.dump(data, open(self.him_path, 'w'), indent=2)
    def load_ctm(self): return json.load(open(self.ctm_path))
    def save_ctm(self, data): json.dump(data, open(self.ctm_path, 'w'), indent=2)
    def load_cpl(self): return json.load(open(self.cpl_path))
    def save_cpl(self, data): json.dump(data, open(self.cpl_path, 'w'), indent=2)
    def load_opp(self): return json.load(open(self.opp_path))
    def save_opp(self, data): json.dump(data, open(self.opp_path, 'w'), indent=2)

def calculate_text_metrics(text):
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    avg_sentence_len = len(words) / len(sentences) if sentences else 0

    hedging_words = ['might', 'could', 'perhaps', 'maybe', 'possibly', 'think', 'seems', 'usually', 'often']
    hedge_count = sum(1 for w in words if w in hedging_words)
    hedging_level = hedge_count / len(words) if words else 0

    return {
        "avg_sentence_length": avg_sentence_len,
        "hedging_level": hedging_level,
        "word_count": len(words)
    }

def check_voice_drift(him_metrics, current_metrics):
    if not him_metrics:
        return 0.0 # No baseline

    # Simple drift calculation (Euclidean distance on normalized features)
    # This is a basic mock of the cosine_sim / fingerprint check mentioned in DRP
    rhythm_drift = abs(current_metrics.get("avg_sentence_length", 0) - him_metrics.get("avg_sentence_length", 0)) / max(him_metrics.get("avg_sentence_length", 1), 1)
    hedge_drift = abs(current_metrics.get("hedging_level", 0) - him_metrics.get("hedging_level", 0))

    drift_score = min((rhythm_drift * 0.5) + (hedge_drift * 5.0), 1.0)
    return drift_score

if __name__ == "__main__":
    # Quick test
    state = NexusMemoryState("./nexus_test_data")
    print("Nexus Data Layer Initialized at ./nexus_test_data")
