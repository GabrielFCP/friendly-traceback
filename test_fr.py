
import os
import sys

# Ensure friendly_traceback is in path
sys.path.insert(0, os.path.abspath('.'))

import friendly_traceback

try:
    friendly_traceback.set_lang('fr')
    print(f"Current language: {friendly_traceback.get_lang()}")
    
    from friendly_traceback.ft_gettext import current_lang
    msg = "I have no suggestion to offer."
    translated = current_lang.translate(msg)
    print(f"Original: {msg}")
    print(f"Translated: {translated}")
    
except Exception as e:
    print(f"ERROR: {e}")
