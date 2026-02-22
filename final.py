#! /usr/bin/python
print('Content-type: text/html\n\n')

import cgi, cgitb
cgitb.enable()
html = open("final_simulation.html")
html_string = html.read()

#encoded_paragraph = html_string.find('<div class="enigma-machine">')
#html_noEnigma = html_string[:encoded_paragraph:]

#keyboard_div = html_string.find('<div class="keyboard">')
#html_noKeyboard = html_string[:keyboard_div:]

#print(html1)
#Storage of Input String


#start of encryption code ---------------------------------------------------

#HALLO this is jessica :)
#This is keyboard starter
keys="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def connect (list):
    keybinds={}
    for x in list:
        keybinds[x]=x
    return keybinds
        
current_keybinds = connect(keys)
#print(current_keybinds)

#This is the plugboard
def wire_plugboard (chosen_letter, connected_letter, keybinds):
    keybinds[chosen_letter]=connected_letter
    keybinds[connected_letter]=chosen_letter
    return keybinds

def process_plugboard (letter):
    if(letter < 'A' or letter > 'Z'):
        return letter
    return current_keybinds[letter]

rotor_wiring = ["EJMZALYXVBWFCRQUONTSPIKHGD", "DMTWSILRUYQNKFEJCAZBPGXOHV", "HQZGPJTMOBLNCIFDYAWVEUSRKX", "UQNTLSZFMREHDPXKIBVYGJCWOA"]
# reflector, rotor 1, rotor 2, rotor 3
rotors = ['A', 'A', 'A', 'A']
def process_rotors(text_input):
    #go through rotors
    text_output = ""
    j = 0
    while j < len(text_input): # loop through each letter
        c = text_input[j].upper()
        c = process_plugboard(c)
        i = 3
        while i >= -3: #loop through 3 rotors, reflector, and 3 rotors again
            #print("Step " + str(4 - i) + ": " + c)
            c = process_letter(c, i)
            i -= 1
        j += 1
        increment_by_one(rotors)
        c = process_plugboard(c)
        text_output += c
        
    return text_output

def process_letter(letter_input, rotor_number):
    result = ""
    key = rotor_wiring[abs(rotor_number)]
    # key is a 26-letter string
    letterID = ord(letter_input) - ord('A') #index of the input letter, A is 1, B is 2, etc
    shift = ord(rotors[abs(rotor_number)]) - ord('A') #how much to shift the rotor by
    shifted_key = key[shift:] + key[:shift] #key after shifting
    if(rotor_number < 0):
        shifted_key = invert(shifted_key)

    #print("Input: " + letter_input)
    #print(shifted_key)
    #print("Shift: " + str(shift))
    #print(letterID)

    if(letterID < 0 or letterID > 25):
        #letter is not between A and Z, don't try to encode it
        return letter_input
    else:
        encodedLetter = shifted_key[letterID]
        #print(encodedLetter)
        return encodedLetter

def invert(key):
    result = ""
    i = 'A'
    while i <= 'Z':
        result += chr(key.index(i) + ord('A'))
        i = chr(ord(i) + 1)
    return result

def increment_by_one(rotor_list):
    # increments rotors by one
    # at Z, goes back to A and increments the next rotor by 1
    rotor_list[3] = chr(ord(rotor_list[3]) + 1)
    i = 1
    while i < len(rotor_list):      
        pos = len(rotor_list) - i
        if(rotor_list[pos] > 'Z'):
            rotor_list[pos] = 'A'
            rotor_list[pos-1] = chr(ord(rotor_list[pos-1]) + 1)
        i += 1
    rotors[0] = 'A' #reflector shouldn't shift

#testing it out

#text = "hi my name is richard"
#print("Original: " + text)
#text = process_rotors(text)
#print("Encrypted: " + text)
#rotors = ['A', 'A', 'A', 'A']
#text = process_rotors(text)
#print("Decrypted: " + text)
    
    
#end of encryption code ---------------------------------------------------
    
#Input Text from HTML page
#Adding forms to the keyboard
    
#keyboard_start = html_string.find('<div class="keyboard">')
#keyboard_end = html_string.find('<div class="key">Z</div>')
    

    
# allow keyboard input --------------------------
i = 0
while i < 26:
    curLetter = str(chr(ord('A') + i))
    newKey = '''<div class="key">
<form action="final.py" method="get">
<input type="hidden" name="k_in" value='''+ '"' + curLetter + '"'+ '''>
<input type="hidden" name="rotors" value="">
<input type="hidden" name="t_out" value="">
<input type="hidden" name="p_in" value="">
<input type="hidden" name="p_out" value="">
<button class = "key" type="submit">''' + curLetter +'''</button>
</form>
  </div>'''
    oldKey = '<div class="key">' + curLetter + '</div>'
    html_string = html_string.replace(oldKey, newKey)
    i += 1
    
    #print(oldKey)
    #print(newKey)
# -----------------------------------------------

# allow plugboard input -------------------------
i = 0
while i < 26:
    curLetter = str(chr(ord('A') + i))
    newKey = '''<div class="plug">
<form action="final.py" method="get">
<input type="hidden" name="k_in" value="">
<input type="hidden" name="rotors" value="">
<input type="hidden" name="t_out" value="">
<input type="hidden" name="p_in" value= ''' + curLetter + '''>
<input type="hidden" name="p_out" value="">
<button class = "plug" type="submit">''' + curLetter +'''</button>
</form>
  </div>'''
    oldKey = '<div class="plug">' + curLetter + '</div>'
    html_string = html_string.replace(oldKey, newKey)
    i += 1
# -----------------------------------------------

def arrange_plugs(plug_data):
    #APELK --> A,P  E,L  K
    #CIKKT --> C,I  T
    #JUEAJW --> U,W E,A
    i = 0
    past_pairs = ""
    cur_pair = ""
    while i < len(plug_data):
        cur_letter = plug_data[i]
        if cur_letter in cur_pair:
            #delete current pair
            cur_pair = ""
        elif cur_letter in past_pairs:
            #delete previous pair
            start = int(past_pairs.find(cur_letter) / 2) * 2
            past_pairs = past_pairs[:start] + past_pairs[start + 2:]
        else:
            #add new pair
            if(len(cur_pair) == 0):
                cur_pair = cur_letter
            else:
                past_pairs += (cur_pair + cur_letter)
                cur_pair = ""
        i += 1
    #create lists
    pairs = []
    i = 0
    while i < len(past_pairs):
        pairs.append([past_pairs[i], past_pairs[i+1]])
        i += 2
    return pairs

def update_rotors(rotor_input):
    rotor_input = rotor_input.upper()
    r_num = 1
    i = 0
    while r_num <= 3 and i < len(rotor_input):
        cur = rotor_input[i]
        if(cur >= 'A' and cur <= 'Z'):
            rotors[r_num] = cur
            r_num += 1
            i +=1
        else:
            i +=1

def modify_rotors(orig_html, rotors):
    #rotors --> ["A", "A", "B", "C"]
    i = 1
    while i < len(rotors):
        orig_html = orig_html.replace('<div class="rotor">A</div>', '<div class = "rotor">' + rotors[i] + '</div>', 1)
        i += 1
    return orig_html

def modify_lampboard(orig_html, litKey):
    orig_html = orig_html.replace('<div class="lamp">' + litKey + '</div>', '<div class="lamp lit">' + litKey + '</div>')
    return orig_html

def modify_plugs(orig_html, plug_pairs):
    colors = [50, 168, 82]
    for pair in plug_pairs:
        #print(pair)
        #modify colors
        i = 0
        while i < len(colors):
            colors[i] = (colors[i] + 76) % 255
            i += 1
        colorString = "rgb(" + str(colors[0]) + ", " + str(colors[1]) + ", " + str(colors[2]) + ")"
            
        p1 = pair[0]
        p2 = pair[1]
        #<button class = "plug" type="submit">K</button>
        orig_html = orig_html.replace('<button class = "plug" type="submit">' + p1 + '</button>', '<button class="plug" type="submit" style="background-color:'+ colorString + ';">' + p1 + '</button>')
        orig_html = orig_html.replace('<button class = "plug" type="submit">' + p2 + '</button>', '<button class="plug" type="submit" style="background-color:'+ colorString + ';">' + p2 + '</button>')
    return orig_html
        

def modify_output(orig_html, rotors, plugs, text):
    orig_html = orig_html.replace('<input type="hidden" name="rotors" value="">', '<input type="hidden" name="rotors" value="'+ rotors[1] + rotors[2] + rotors[3] + '">')
    orig_html = orig_html.replace('<input type="hidden" name="t_out" value="">', '<input type="hidden" name="t_out" value="' + text + '">')
    orig_html = orig_html.replace('<input type="hidden" name="p_out" value="">', '<input type="hidden" name="p_out" value="' + plugs + '">')
    return orig_html

#print(keyboard)
#print(html_noKeyboard + generate_keyboard())

html_data = cgi.FieldStorage()
output_text = ""

if 'rotors' in html_data:
    rotor_input = html_data.getvalue("rotors")
    update_rotors(rotor_input)
    
    
# plugs ------------------------------
plug_data = ""
if 'p_out' in html_data:
    plug_data = html_data.getvalue("p_out")
    
if 'p_in' in html_data:
    #process plugs
    plug_data += html_data.getvalue("p_in")
plug_pairs = arrange_plugs(plug_data)  
for pair in plug_pairs:
    current_keybinds = wire_plugboard(pair[0], pair[1], current_keybinds)
#print("<h1>" + plug_data + "</h1>")
    
#update plugs
html_string = modify_plugs(html_string, plug_pairs)
#-----------------------------------------

if 't_out' in html_data:
    output_text += html_data.getvalue("t_out")

if 't_in' in html_data:
    input_text = html_data.getvalue("t_in") # "text input"
    encoded_text = process_rotors(input_text)
    output_text += encoded_text
    
# lampboard and keyboard -----------------
if 'k_in' in html_data:
    input_key = html_data.getvalue('k_in')
    encoded_key = process_rotors(input_key)
    output_text += encoded_key
    
    #update lampboard
    html_string = modify_lampboard(html_string, encoded_key)
#-----------------------------------------
    
#update html rotors
html_string = modify_rotors(html_string, rotors)

#preserve output data
html_string = modify_output(html_string, rotors, plug_data, output_text)

#display final output text
html_string = html_string.replace("{insert output here}", output_text)

print(html_string)
