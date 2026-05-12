#!/bin/bash
echo "Verifying CIPHER integration..."
if [ -d "skills/red-teaming/cipher" ]; then
    echo "✔ Cipher directory exists"
else
    echo "❌ Cipher directory missing"
fi
if [ -f "skills/red-teaming/cipher/SKILL.md" ]; then
    echo "✔ SKILL.md exists"
else
    echo "❌ SKILL.md missing"
fi
if [ -f "skills/red-teaming/cipher/scripts/load_cipher.py" ]; then
    echo "✔ load_cipher.py exists"
else
    echo "❌ load_cipher.py missing"
fi
if grep -q "CIPHER Security Agent" README.md; then
    echo "✔ README.md updated correctly"
else
    echo "❌ README.md missing CIPHER section"
fi
echo "Verification complete."
