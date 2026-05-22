import re

path = 'nix/tui.nix'

with open(path, 'r') as f:
    content = f.read()

content = re.sub(
    r'hash = "sha256-MHZ8lnmnSiZ7TpDN/V61Etj851dJT/9RzZxfQOM2nz0="',
    'hash = "sha256-JgPKgs/zArcs6v3fBwHKPJBFriq8HMPcw+fw9TfCzlY="',
    content
)

with open(path, 'w') as f:
    f.write(content)
