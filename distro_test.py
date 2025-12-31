#!/usr/bin/env python3
import conchfetch

# Fix imports when running from /usr/local/bin
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now import
try:
    from conchfetch import print_info
except ImportError:
    # Try parent directory (if installed)
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    from conchfetch import print_info


print("test distro logos")

distro = input("> ")
conchfetch.get_distro_name = lambda: distro

print_info()