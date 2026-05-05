#!/usr/bin/env python
"""Generate Brazilian Portuguese translation file."""
import re
import os
import sys
from datetime import datetime

translations = {
    "Did you forget a colon `:`?": "Você esqueceu dois-pontos `:`?",
    "Did you forget to write a colon?": "Você esqueceu de escrever dois-pontos?",
    "Line `{number}` identified above is more indented than expected.": "A linha `{number}` identificada acima possui mais indentação que o esperado.",
    "Line `{number}` identified above was expected to begin a new indented block.": "A linha `{number}` identificada acima deveria começar um novo bloco indentado.",
    "Line `{number}` identified above is less indented than expected.": "A linha `{number}` identificada acima possui menos indentação que o esperado.",
    "In your program, no object with the name `{var_name}` exists.": "Em seu programa, não existe nenhum objeto com o nome `{var_name}`.",
    "`{name}` is a name found in module `{mod}`. Perhaps you forgot to write\n\n    from {mod} import {name}": "`{name}` é um nome encontrado no módulo `{mod}`. Talvez você tenha esquecido de escrever\n\n    from {mod} import {name}",
    "Did you forget to import `{name}`?": "Você esqueceu de importar `{name}`?",
    "You tried to concatenate (add) two different types of objects:\n{first} and {second}.": "Você tentou concatenar (somar) dois tipos diferentes de objetos:\n{first} e {second}.",
    "You tried to add two incompatible types of objects:\n{first} and {second}.": "Você tentou somar dois tipos incompatíveis de objetos:\n{first} e {second}.",
    "\nNote: `NoneType` means that the object has a value of `None`.\n": "\nNota: `NoneType` significa que o objeto tem um valor de `None`.\n",
    "Python indicates that you have an object of type `{obj_type}`,\nfollowed by something surrounded by parentheses, `(...)`,\nwhich Python took as an indication of a function call.\nEither the object of type `{obj_type}` was meant to be a function,\nor you forgot a comma before `(...)`.\n": "Python indica que você tem um objeto do tipo `{obj_type}`,\nseguido por algo entre parênteses, `(...)`,\nque Python interpretou como uma chamada de função.\nOu o objeto do tipo `{obj_type}` deveria ser uma função,\nou você esqueceu de uma vírgula antes de `(...)`.\n",
    "You are attempting to access the attribute `{attr}`\nfor a variable whose value is `None`.": "Você está tentando acessar o atributo `{attr}`\npara uma variável cujo valor é `None`.",
    "You can only multiply sequences, such as list, tuples,\n strings, etc., by integers.": "Você pode multiplicar apenas sequências, como listas, tuplas,\n cadeias de caracteres, etc., por inteiros.",
    "You have tried to get the item with index `{index}` of `{name}`,\n{obj_type} of length `{length}`.": "Você tentou obter o item com índice `{index}` de `{name}`,\n{obj_type} de comprimento `{length}`.",
    "Remember: the first item of {obj_type} is not at index 1 but at index 0.": "Lembre-se: o primeiro item de {obj_type} não está no índice 1 mas no índice 0.",
    "The key `{key}` cannot be found in the dict `{name}`.": "A chave `{key}` não pode ser encontrada no dicionário `{name}`.",
    "`{value}` is an invalid argument for `int()` in base `{base}`.": "`{value}` é um argumento inválido para `int()` na base `{base}`.",
    "The string `{string}` cannot be converted to a `float`\nas it does not represent a number.": "A cadeia de caracteres `{string}` não pode ser convertida para `float`\npois não representa um número.",
    "You are dividing by zero.": "Você está dividindo por zero.",
    "The object `{obj}` has no attribute named `{attr}`.": "O objeto `{obj}` não possui um atributo chamado `{attr}`.",
    "The object `{obj_name}` has no attribute named `{attribute}`.": "O objeto `{obj_name}` não possui um atributo chamado `{attribute}`.",
    "Perhaps you need to type\n\n     print({message})\n\nIn older version of Python, `print` was a keyword.\nNow, `print` is a function; you need to use parentheses to call it.": "Talvez você precise digitar\n\n     print({message})\n\nEm versões antigas do Python, `print` era uma palavra-chave.\nAgora, `print` é uma função; você precisa usar parênteses para chamá-la.",
    "Did you forget a closing quote?\nYou started writing a string with a single or double quote\nbut never ended the string with another quote on that line.": "Você esqueceu de uma aspas de fechamento?\nVocê começou a escrever uma cadeia de caracteres com uma aspas simples ou dupla\nmas nunca terminou a cadeia de caracteres com outra aspas naquela linha.",
    "Did you mean `{num}`?\nPerhaps you meant to write the octal number `{num}`\nand forgot the letter 'o', or perhaps you meant to write\na decimal integer and did not know that it could not start with zeros.": "Você quis dizer `{num}`?\nTalvez você tenha pretendido escrever o número octal `{num}`\ne esqueceu a letra 'o', ou talvez você tenha pretendido escrever\num inteiro decimal e não soubesse que ele não poderia começar com zeros.",
    "You're trying to use the name `{name}` identified by Python as being\nin the local scope of a function before having assigned it a value.": "Você está tentando usar o nome `{name}` identificado por Python como estando\nno escopo local de uma função antes de ter atribuído um valor a ele.",
    "Did you forget to write `in`?": "Você esqueceu de escrever `in`?",
    "Perhaps you meant `==` instead of `=`.": "Talvez você tenha quiseste `==` em vez de `=`.",
    "It is possible that you used an equal sign `=` instead of a colon `:`\nto assign values to keys in a dict\nbefore or at the position indicated by ^.": "É possível que você tenha usado um sinal de igualdade `=` em vez de dois-pontos `:`\npara atribuir valores a chaves em um dicionário\nantes ou na posição indicada por ^.",
    "Did you forget to call `{name}`?": "Você esqueceu de chamar `{name}`?",
    "A `RecursionError` is raised when a function calls itself,\ndirectly or indirectly, too many times.\nIt almost always indicates that you made an error in your code\nand that your program would never stop.": "Um `RecursionError` é levantado quando uma função chama a si mesma,\ndireta ou indiretamente, muitas vezes.\nQuase sempre indica que você cometeu um erro em seu código\ne que seu programa nunca pararia.",
    "Only hashable objects can be used\nas elements of `set` or keys of `dict`.\nHashable objects are objects that do not change value\nonce they have been created.": "Apenas objetos hash podem ser usados\ncomo elementos de `set` ou chaves de `dict`.\nObjetos hash são objetos que não mudam de valor\ndepois de terem sido criados.",
    "Perhaps you forgot `self` when defining `{fn_name}`.\n": "Talvez você tenha esquecido de `self` ao definir `{fn_name}`.\n",
    "The Python keyword `break` can only be used inside a `for` loop or inside a `while` loop.\n": "A palavra-chave Python `break` só pode ser usada dentro de um loop `for` ou dentro de um loop `while`.\n",
    "The Python keyword `continue` can only be used inside a `for` loop or inside a `while` loop.\n": "A palavra-chave Python `continue` só pode ser usada dentro de um loop `for` ou dentro de um loop `while`.\n",
    "The `else` keyword does not begin a code block that matches\na valid code block, possibly because `else` is not indented correctly.\n": "A palavra-chave `else` não começa um bloco de código que corresponde\na um bloco de código válido, possivelmente porque `else` não está indentado corretamente.\n",
    "The `elif` keyword does not begin a code block that matches\nan `if` block, possibly because `elif` is not indented correctly.\n": "A palavra-chave `elif` não começa um bloco de código que corresponde\na um bloco `if`, possivelmente porque `elif` não está indentado corretamente.\n",
    "The `except` keyword does not begin a code block that matches\na `try` block, possibly because `except` is not indented correctly.\n": "A palavra-chave `except` não começa um bloco de código que corresponde\na um bloco `try`, possivelmente porque `except` não está indentado corretamente.\n",
    "Outside of Python, `^` is often used to indicate exponentiation.": "Fora do Python, `^` é frequentemente usado para indicar exponenciação.",
    "Perhaps you meant `{line}`.": "Talvez você tenha quiseste `{line}`.",
    "You wrote three equal signs in a row which is allowed in some\nprogramming languages, but not in Python. To check if two objects\nare equal, use two equal signs, `==`; to see if two names represent\nthe exact same object, use the operator `is`.\n": "Você escreveu três sinais de igualdade seguidos, o que é permitido em algumas\nlinguagens de programação, mas não em Python. Para verificar se dois objetos\nsão iguais, use dois sinais de igualdade, `==`; para ver se dois nomes representam\no exato mesmo objeto, use o operador `is`.\n",
    "You can only use a `return` statement inside a function or method.\n": "Você só pode usar uma declaração `return` dentro de uma função ou método.\n",
    "You can only use a `yield` statement inside a function.\n": "Você só pode usar uma declaração `yield` dentro de uma função.\n",
    "You have attempted to remove `{item}` from the list `{the_list}`.\nHowever, `{the_list}` does not contain `{item}`.\n": "Você tentou remover `{item}` da lista `{the_list}`.\nNo entanto, `{the_list}` não contém `{item}`.\n",
    "Python keywords cannot be used as identifiers (variable names).\n": "Palavras-chave do Python não podem ser usadas como identificadores (nomes de variáveis).\n",
    "Valid names cannot begin with a number.\n": "Nomes válidos não podem começar com um número.\n",
    "Friendly warning: you have redefined the python builtin `{name}`.\n": "Aviso amigável: você redefiniu o builtin do Python `{name}`.\n",
    "Did you mean `{number}j`?\nPerhaps you thought that `i` could be used to represent\nthe square root of `-1`. In Python, the symbol used for this is `j`\nand the complex part is written as `some_number` immediately\nfollowed by `j`, with no spaces in between.\n": "Você quis dizer `{number}j`?\nTalvez você tenha pensado que `i` pudesse ser usado para representar\na raiz quadrada de `-1`. Em Python, the símbolo usado para isso é `j`\ne a parte complexa é escrita como `some_number` imediatamente\nseguida por `j`, sem espaços entre eles.\n",
    "Did you forget to convert the string `{name}` into {number_type}?\n": "Você esqueceu de converter a cadeia de caracteres `{name}` em {number_type}?\n",
    "You wrote two operators (`{first}` and `{second}`)\nin the wrong order: `{wrong}` instead of `{correct}`.\n": "Você escreveu dois operadores (`{first}` e `{second}`)\nna ordem errada: `{wrong}` em vez de `{correct}`.\n",
    "Perhaps you needed `==` instead of `=`.\nYou likely used an assignment operator `=` instead of an equality operator `==`.\n": "Talvez você tenha precisado de `==` em vez de `=`.\nVocê provavelmente usou um operador de atribuição `=` em vez de um operador de igualdade `==`.\n",
}

# Ensure we are in the correct directory or provide full path
pot_path = os.path.join(os.path.dirname(__file__), 'friendly_tb.pot')
if not os.path.exists(pot_path):
    print(f"Error: {pot_path} not found")
    sys.exit(1)

with open(pot_path, 'r', encoding='utf-8') as f:
    template = f.read()

now = datetime.now().strftime("%Y-%m-%d %H:%M+0000")
header = f'# Brazilian Portuguese translation for friendly-traceback.\n# Copyright (C) 2024 FRIENDLY-TRACEBACK\n#\nmsgid ""\nmsgstr ""\n"Project-Id-Version: friendly-traceback\\n"\n"POT-Creation-Date: 2022-11-28 09:29-0400\\n"\n"PO-Revision-Date: {now}\\n"\n"Language: pt_BR\\n"\n"MIME-Version: 1.0\\n"\n"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"\n\n'

lines = template.split('\n')
out = [header.rstrip('\n')]
i = 0

while i < len(lines):
    line = lines[i]
    if line.startswith('#:'):
        out.append(line)
        i += 1
        msgid_lines = []
        while i < len(lines) and (lines[i].startswith('msgid') or (lines[i].startswith('"') and i > 0)):
            msgid_lines.append(lines[i])
            out.append(lines[i])
            i += 1

        msgid_parts = []
        for ml in msgid_lines:
            for match in re.finditer(r'"([^"]*)"', ml):
                msgid_parts.append(match.group(1).replace('\\n', '\n'))
        msgid_text = ''.join(msgid_parts)

        # We skip the original msgstr and any following lines
        if i < len(lines) and lines[i].startswith('msgstr'):
            i += 1
            while i < len(lines) and lines[i].startswith('"'):
                i += 1

        trans = translations.get(msgid_text, '')
        if not trans and msgid_text.endswith('\n'):
            trans = translations.get(msgid_text[:-1], '')
        
        if msgid_text.startswith("You are dividing by zero"):
             print(f"DEBUG: Found target msgid: {repr(msgid_text)}")
             print(f"DEBUG: Found translation: {repr(trans)}")

        if trans:
            if '\n' in trans:
                out.append('msgstr ""')
                parts = trans.split('\n')
                for j, p in enumerate(parts):
                    esc = p.replace('\\', '\\\\').replace('"', '\\"')
                    if j < len(parts) - 1:
                        out.append(f'"{esc}\\n"')
                    elif p:
                        out.append(f'"{esc}"')
            else:
                esc = trans.replace('\\', '\\\\').replace('"', '\\"')
                out.append(f'msgstr "{esc}"')
        else:
            out.append('msgstr ""')
        out.append('')
    else:
        out.append(line)
        i += 1

po_path = os.path.join(os.path.dirname(__file__), 'pt_BR/LC_MESSAGES/friendly_tb_pt_BR.po')
os.makedirs(os.path.dirname(po_path), exist_ok=True)
with open(po_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out).strip() + '\n')

print(f"Created {po_path}")
print(f"Translated {len(translations)} messages")
