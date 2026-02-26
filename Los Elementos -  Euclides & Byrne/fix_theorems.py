import sys
import os

def get_braced_content(text, start_pos):
    if start_pos >= len(text) or text[start_pos] != '{':
        return None, start_pos
    
    count = 0
    for i in range(start_pos, len(text)):
        if text[i] == '{':
            count += 1
        elif text[i] == '}':
            count -= 1
            if count == 0:
                return text[start_pos:i+1], i+1
    return None, start_pos

def process_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    pos = 0
    new_text = ""
    while pos < len(text):
        found = text.find('\\theorem', pos)
        if found == -1:
            new_text += text[pos:]
            break
        
        # Check if it's literally \theorem (not \starttheorem)
        if found > 0 and text[found-1] == 't': # likely starttheorem
             new_text += text[pos:found+1]
             pos = found + 1
             continue
             
        new_text += text[pos:found]
        current = found + len('\\theorem')
        
        g1, next_pos = get_braced_content(text, current)
        if g1:
            g2, next_pos2 = get_braced_content(text, next_pos)
            if g2:
                g3, next_pos3 = get_braced_content(text, next_pos2)
                if g3:
                    new_text += '\\problem' + g1 + g2 + g3
                    pos = next_pos3
                    continue
            
            new_text += '\\starttheorem' + g1
            pos = next_pos
        else:
            new_text += '\\theorem'
            pos = current

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(new_text)

if __name__ == "__main__":
    process_file(sys.argv[1])
