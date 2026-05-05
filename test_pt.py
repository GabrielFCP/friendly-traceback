
import os
import sys

# Ensure friendly_traceback is in path
sys.path.insert(0, os.path.abspath('.'))

import friendly_traceback

try:
    friendly_traceback.set_lang('pt_BR')
    print(f"Current language: {friendly_traceback.get_lang()}")
    
    from friendly_traceback.ft_gettext import current_lang
    
    # Test 1: With newline (as in template)
    msg1 = "You are dividing by zero.\n"
    translated1 = current_lang.translate(msg1)
    print(f"Test 1 - Original: {repr(msg1)}")
    print(f"Test 1 - Translated: {repr(translated1)}")
    
    # Test 2: Another common one
    msg2 = "Did you forget a colon `:`?"
    # It might have a newline too, let's try both
    translated2 = current_lang.translate(msg2)
    if translated2 == msg2:
        translated2 = current_lang.translate(msg2 + "\n")
        msg2 += "\n"
    print(f"Test 2 - Original: {repr(msg2)}")
    print(f"Test 2 - Translated: {repr(translated2)}")

    if "Você está dividindo por zero." in translated1 or "Você esqueceu dois-pontos" in translated2:
        print("SUCCESS: Portuguese translation is working!")
    else:
        print("FAILURE: Translation returned original string or wrong translation.")
except Exception as e:
    print(f"ERROR: {e}")
