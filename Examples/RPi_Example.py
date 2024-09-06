import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import time
# LCD Configuration

#change to whatever screen you have here 
lcd_columns = 8
lcd_rows = 2
#and GPIO connections here
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D17)
lcd_d6 = digitalio.DigitalInOut(board.D18)
lcd_d7 = digitalio.DigitalInOut(board.D22)

lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows)

def read_custom_chars(file_path):
    custom_chars = {}
    current_char = None
    char_data = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Character"):
                if current_char is not None:
                    custom_chars[current_char] = char_data
                current_char = int(line.split()[1])
                char_data = []
            elif line.startswith("0b"):
                char_data.append(int(line[2:-1], 2))
    
    if current_char is not None:
        custom_chars[current_char] = char_data
    
    return custom_chars

# Read custom characters from file
file_path = "LCDchar.txt"  # Replace with your file path
custom_chars = read_custom_chars(file_path)

# Create custom characters
for char_num, char_data in custom_chars.items():
    if char_num < 16:  # LCD can only store 8 custom characters
        lcd.create_char(char_num, char_data)

# Define a mapping dictionary with multiple strings for each character
char_map = ""
def char_base():
    global char_map
    char_map = {
        ('1', 'Char1'): '\x00',
        ('2', 'MyShape'): '\x01',
        ('o'): '\x02',
        ('a'): '\x03',
        ('b'): '\x04',
        ( 'c'): '\x05',
        ('d'): '\x06',
        ('g'): '\x07',
        (' ', 'space'): ' '
    }



def get_char(key):
    char_base()
    global char_map
    for strings, char in char_map.items():
        if key in strings:
            return char
    return key  # Return the original key if no match is found

def LCDprintChar(message):
    lines = message.split('\n')
    for i, line in enumerate(lines[:2]):  # Only process first two lines
        words = line.split()
        translated_line = ''.join(get_char(word) for word in words)
        lcd.cursor_position(0, i)
        lcd.message = translated_line[:8]  # Limit to 8 characters per line




def LCDprint(message):
    try:
        lcd.message=message
    except Exception as e:
        lcd.message = message
        print(e)
        exit()


def LCDclear():
    lcd.clear()



LCDclear()
LCDprint("test\n one")
time.sleep(1)
LCDclear()
lcd.message = "\x00\x01\x02\x03\x04\x05"
time.sleep(1)
LCDclear()
LCDprintChar("Char1 MyShape")

