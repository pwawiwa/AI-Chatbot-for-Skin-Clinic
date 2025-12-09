#!/usr/bin/env python
"""
Birthday messenger entry point — generate and print birthday messages from CSV data
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` can be imported when running script directly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.birthday_messenger import main


if __name__ == "__main__":
    main()
#!/usr/bin/env python
"""
Birthday messenger entry point — generate and print birthday messages from CSV data
"""
from src.birthday_messenger import main

if __name__ == "__main__":
    main()
