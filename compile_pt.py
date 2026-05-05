
import struct
import array
import re
import os

def msgfmt(po_file, mo_file):
    M1 = 0x950412de

    def make_mo(messages):
        keys = sorted(messages.keys())
        offsets = []
        ids = b''
        strs = b''
        for k in keys:
            v = messages[k]
            offsets.append((len(ids), len(k), len(strs), len(v)))
            ids += k + b'\0'
            strs += v + b'\0'

        keystart = 7 * 4 + 16 * len(keys)
        valstart = keystart + len(ids)
        k_offsets = []
        v_offsets = []
        for o1, l1, o2, l2 in offsets:
            k_offsets += [l1, o1 + keystart]
            v_offsets += [l2, o2 + valstart]

        output = struct.pack('<Iiiiiii',
                             M1, 0, len(keys), 7 * 4,
                             7 * 4 + len(keys) * 8, 0, 0)
        output += array.array('i', k_offsets).tobytes()
        output += array.array('i', v_offsets).tobytes()
        output += ids
        output += strs
        return output

    messages = {}
    with open(po_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_id = None
    current_str = None
    state = None

    def unescape(s):
        return s.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if line.startswith('msgid'):
            if current_id is not None and current_str:
                messages[current_id.encode('utf-8')] = current_str.encode('utf-8')
            
            match = re.search(r'msgid "(.*)"', line)
            current_id = match.group(1)
            current_str = None
            state = 'msgid'
        elif line.startswith('msgstr'):
            match = re.search(r'msgstr "(.*)"', line)
            current_str = match.group(1)
            state = 'msgstr'
        elif line.startswith('"'):
            match = re.search(r'"(.*)"', line)
            if state == 'msgid':
                current_id += match.group(1)
            elif state == 'msgstr':
                current_str += match.group(1)

    if current_id is not None and current_str:
        messages[current_id.encode('utf-8')] = current_str.encode('utf-8')

    # Unescape keys and values
    final_messages = {}
    for k, v in messages.items():
        # Keys in .po are already escaped, but we need raw bytes for .mo
        # Wait, gettext stores them escaped? No, raw.
        # But my parser got the escaped version.
        final_messages[unescape(k.decode('utf-8')).encode('utf-8')] = unescape(v.decode('utf-8')).encode('utf-8')

    with open(mo_file, 'wb') as f:
        f.write(make_mo(final_messages))

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    po = os.path.join(base_path, 'friendly_traceback/locales/pt_BR/LC_MESSAGES/friendly_tb_pt_BR.po')
    mo = os.path.join(base_path, 'friendly_traceback/locales/pt_BR/LC_MESSAGES/friendly_tb_pt_BR.mo')
    print(f"Compiling {po} to {mo}")
    msgfmt(po, mo)
    print("Done")
