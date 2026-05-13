import argparse
import sys
import os
import json
from nexus_presence_core import NexusMemoryState, calculate_text_metrics, check_voice_drift

def cmd_init_profile(args):
    state = NexusMemoryState()

    if args.sample_file and os.path.exists(args.sample_file):
        with open(args.sample_file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Error: Must provide --sample-file or --text")
        sys.exit(1)

    metrics = calculate_text_metrics(text)

    him = state.load_him()
    him["voice_fingerprint"] = metrics
    him["drift_detection"]["last_calibration"] = "just now"
    state.save_him(him)

    print("HIM (Human Identity Model) Initialized.")
    print(json.dumps(metrics, indent=2))

def cmd_add_community(args):
    state = NexusMemoryState()
    ctm = state.load_ctm()

    new_community = {
        "id": args.name.lower().replace(" ", "_"),
        "platform": args.platform,
        "trust_density": 0.0,
        "current_position": {
            "presence_score": 0.0,
            "trust_capital": 0.0
        }
    }

    # Check if exists
    for c in ctm["communities"]:
        if c["id"] == new_community["id"]:
            print(f"Community {c['id']} already exists.")
            return

    ctm["communities"].append(new_community)
    state.save_ctm(ctm)
    print(f"Added community: {args.name} on {args.platform}")

def cmd_verify_draft(args):
    state = NexusMemoryState()
    him = state.load_him()

    baseline = him.get("voice_fingerprint", {})
    if not baseline:
        print("Error: HIM not initialized. Run init-profile first.")
        sys.exit(1)

    current_metrics = calculate_text_metrics(args.text)
    drift = check_voice_drift(baseline, current_metrics)

    passed = drift < 0.3  # DRP spec sets >0.3 as flag threshold

    print(f"Draft Verification:")
    print(f"Drift Score: {drift:.3f} (Threshold: 0.3)")
    print(f"Result: {'PASSED' if passed else 'FAILED - VOICE DRIFT DETECTED'}")
    if not passed:
        print("Recommendation: Rewrite to match baseline sentence rhythm and hedging levels.")
        sys.exit(1)

def cmd_status(args):
    state = NexusMemoryState()
    print("=== NEXUS-PRESENCE STATUS ===")

    him = state.load_him()
    print("\n[HIM] Voice Fingerprint Baseline:")
    print(json.dumps(him.get("voice_fingerprint", {}), indent=2))

    ctm = state.load_ctm()
    print(f"\n[CTM] Tracked Communities: {len(ctm.get('communities', []))}")
    for c in ctm.get("communities", []):
        print(f" - {c['id']} ({c['platform']}) | Trust Capital: {c['current_position']['trust_capital']}")

def main():
    parser = argparse.ArgumentParser(description="NEXUS-PRESENCE CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init profile
    p_init = subparsers.add_parser("init-profile")
    p_init.add_argument("--sample-file", help="Path to text file with human writing sample")
    p_init.add_argument("--text", help="Raw text sample")

    # Add community
    p_add = subparsers.add_parser("add-community")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--platform", required=True)

    # Verify draft
    p_verify = subparsers.add_parser("verify-draft")
    p_verify.add_argument("--text", required=True)

    # Status
    p_status = subparsers.add_parser("status")

    args = parser.parse_args()

    if args.command == "init-profile":
        cmd_init_profile(args)
    elif args.command == "add-community":
        cmd_add_community(args)
    elif args.command == "verify-draft":
        cmd_verify_draft(args)
    elif args.command == "status":
        cmd_status(args)

if __name__ == "__main__":
    main()
