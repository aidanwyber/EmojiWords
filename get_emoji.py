# -*- coding: UTF-8 -*-

emoji_chars_data = None
emoji_chars = None
emoji_phones = None

def init_emoji_data():
    global emoji_chars_data, emoji_chars, emoji_phones
    
    f = open('emoji_chars_utf-8.txt', 'r', encoding='utf-8')
    emoji_chars_data = f.read()
    f.close()
    
    emoji_chars = emoji_chars_data.split('\n')
    emoji_phones = 'tm wc i a b ab cl o sos vs id m p abc abcd ng ok up cool new free end back on top soon s atm c r'.split(' ')

    if len(emoji_phones) != len(emoji_chars):
        raise Exception('emoji_phones variable and emoji_chars file do not match in length ({} vs {}).'.format(len(emoji_phones), len(emoji_chars)))


def sort_chars():
    global emoji_chars, emoji_phones
    
    sortd = False
    while not sortd:
        sortd = True
        for i in range(len(emoji_phones) - 1):
            if len(emoji_phones[i]) < len(emoji_phones[i + 1]):
                sortd = False
                # switch phones
                temp_ph = emoji_phones[i]
                emoji_phones[i] = emoji_phones[i + 1]
                emoji_phones[i + 1] = temp_ph
                # switch chars
                temp_ch = emoji_chars[i]
                emoji_chars[i] = emoji_chars[i + 1]
                emoji_chars[i + 1] = temp_ch

def init():
    init_emoji_data()
    sort_chars()

def main():  
    init()

    try:
        print(emoji_chars)
    except:
        print('Can\'t print emoji\'s in this window.')
    print('emoji_phones: ' + ', '.join(emoji_phones))

def get_emoji():
    main()
    print('get_emoji.py: data in .emoji_chars and .emoji_phones')


if __name__ == '__main__':
    main()
else:
    get_emoji()

    
