#!/usr/bin/env python
"""
Birthday simulator entry point — run full birthday reminder flow with report generation
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` can be imported when running script directly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.birthday_simulator import run_simulation


if __name__ == '__main__':
    run_simulation()
#!/usr/bin/env python
"""
Birthday simulator entry point — run full birthday reminder flow with report generation
"""
from src.birthday_simulator import run_simulation

if __name__ == '__main__':
    run_simulation()
