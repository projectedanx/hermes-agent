"""
Loader for G0DM0D3 scripts. Handles scoping issues without using insecure exec().

Usage in execute_code:
    import sys, os
    sys.path.insert(0, os.path.join(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "skills/red-teaming/godmode/scripts"))
    from load_godmode import *
    
    # Now all functions are available:
    # - auto_jailbreak(), undo_jailbreak()
    # - race_models(), race_godmode_classic()
    # - generate_variants(), obfuscate_query(), detect_triggers()
    # - score_response(), is_refusal(), count_hedges()
    # - escalate_encoding()
"""

import os
import sys
from pathlib import Path

_gm_scripts_dir = Path(os.getenv("HERMES_HOME", Path.home() / ".hermes")) / "skills" / "red-teaming" / "godmode" / "scripts"

if not _gm_scripts_dir.exists():
    _gm_scripts_dir = Path(os.path.abspath(os.path.dirname(__file__)))

if str(_gm_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_gm_scripts_dir))

# Hide argparse from scripts that check sys.argv
_gm_old_argv = sys.argv
sys.argv = ["_godmode_loader"]

from parseltongue import *
from godmode_race import *
from auto_jailbreak import *

sys.argv = _gm_old_argv

# Cleanup loader vars
for _gm_cleanup in ['_gm_scripts_dir', '_gm_old_argv', '_gm_cleanup']:
    globals().pop(_gm_cleanup, None)
