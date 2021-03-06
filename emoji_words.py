# -*- coding: UTF-8 -*-
# python36

'''
Find words that can be written with emoji only.
List of 354986 English words from: https://github.com/dwyl/english-words
'''


import get_emoji


lang = ['english', 'dutch'][0]

#
# parsing word list (dict)
#

print('Loading file.')

f = open('dict/dict_' + lang + '.txt', 'r')
cont = f.readlines()
f.close()

# take away \n at end of line
cont = [x.replace('\n','') for x in cont]

print('Loaded {} {} words.'.format(len(cont), lang.upper()))

print('Sorting list.')
cont = [x.lower() for x in cont]
cont.sort()
print('Sorted list.')




##if extended:
##    # these are not in all block form
##    # s: dollar sign; z: zzz sleeping icon; r, c, and tm: registered, copyright and trade mark;
##    #   y: yen icon on graph; x: cross, sy: dollar/yen icon, e: email icon;
##    emoji = ['free', 'soon', 'cool', 'sos', 'atm', 'off', 'new', 'top', 'abc', 'up', 'ok',
##             'tm', 'on', 'ab', 'id', 'cl', 'ng', 'vs', 'sy', 'wc', 'o', 'a', 'm', 'p', 'b',
##             'v', 'i', 'x', 'e', 'c', 'r', 's', 'y' ,'z']
##else:
##    # emoji letters in a block
##    emoji = ['free', 'soon', 'cool', 'sos', 'atm', 'off', 'new', 'top', 'abc', 'up', 'ok',
##             'on', 'ab', 'id', 'cl', 'ng', 'vs', 'wc', 'o', 'a', 'm', 'p', 'b', 'v', 'i']


#
# the emoji finding algorithm
#

# from get_emoji.py
chars = get_emoji.emoji_chars
phones = get_emoji.emoji_phones

def emojify(s, verbose=False):
    # returns ([phones],[chars]) tuple

    if len(s) <= 0:
        return None
        
    index = 0
    count = 0
    phs = []
    chs = []

    s = s.lower().replace(' ', '')
    
    while count < len(s):
        no_matches = True
        for i in range(len(phones)):
            match = False
            if count+len(phones[i]) <= len(s):
                match = s[count:count+len(phones[i])] == phones[i]
                if verbose:
                    print( s[count:count+len(phones[i])], phones[i], phs, count)
            else:
                if verbose:
                    print(phones[i], 'too long')
                continue

            if match:
                phs.append(phones[i])
                chs.append(chars[i])
                count += len(phones[i])
                no_matches = False
                break
            
        if no_matches:
            #raise Exception('No emoji full emoji transscription possible.')
            return None
            
    return (phs, chs)

# test
##w = 'babamend cool'
###w = 'abacadabra'
##print(w)
##e = emojify(w)
##print(' '.join(e[0]))
###print(''.join(e[1]))


#
# test all words in dict, collect list in results
#

view_list = False
view_min_length = 6

results = []

print('Started checking...')

for w in cont:
    e = emojify(w)
    if e != None:
        results.append([w, e])
        
print('Done checking.')
print()

if view_list:
    for x in [q for q in results if len(q[1][0]) >= view_min_length]:
        w = x[0]
        e = x[1]
        print(w, '\t\t', ' '.join(e[0]))

print()
print('Found {} words that can be written in emoji.'.format(len(results)))


def write_emoji_file(emoji_list, file_name, ext='txt'):
    # modular for different sortings
    path = file_name + '_' + lang + '.' + ext
    output = open(path, 'wb')
    for x in emoji_list:
        line = x[0] + ',' + ' '.join(x[1][0]) + ',' + ''.join(x[1][1]) + u'\n'
        output.write(line.encode('utf-8'))
    output.close()


#
# saving to file
#

print('Writing to file...')

write_emoji_file(results, 'emoji_words_alphabetical', ext='csv')

print('Written.')
print()


#
# statistics report
#

max_len = 0
max_word = None
for x in results:
    w = x[0]
    if len(w) > max_len:
        max_len = len(w)
        max_word = x

print('Max word length ({} leters):'.format(max_len), max_word[0], max_word[1][0])

max_chars = 0
max_chars_word = None
for x in results:
    e = x[1]
    if len(e[0]) > max_chars:
        max_chars = len(e[0])
        max_chars_word = x

print('Max char count ({} chars):'.format(max_chars), max_chars_word[0], max_chars_word[1][0])

print('Ratio of \'emojiable\' words versus all words:', len(results), '/', len(cont), '=', float(len(results))/len(cont))

print()

#
# top 20's
#

n = 20
print('Top {} longest words:'.format(n))
# sort on word length
sortd = False
results_sorted_word_len = results.copy()
while not sortd:
    sortd = True
    for i in range(len(results_sorted_word_len) - 1):
        x0 = results_sorted_word_len[i]
        x1 = results_sorted_word_len[i + 1]
        if len(x1[0]) > len(x0[0]):
            sortd = False
            results_sorted_word_len[i] = x1
            results_sorted_word_len[i + 1] = x0
for i in range(len(results_sorted_word_len[:n])):
    x = results_sorted_word_len[i]
    print('{}. {} letters: {} \t({})'.format(i + 1, len(x[0]), x[0], ' '.join(x[1][0])))

# write this list to a file as well
print('\nWriting word length sorted file...')
write_emoji_file(results_sorted_word_len, 'emoji_words_word_length', ext='csv')
print('Written.')


##print('Top {} number of characters:'.format(n))
### sort on char count
##sortd = False
##results_sorted_char_count = results.copy()
##while not sortd:
##    sortd = True
##    for i in range(len(results_sorted_char_count) - 1):
##        x0 = results_sorted_char_count[i]
##        x1 = results_sorted_char_count[i + 1]
##        if len(x1[1][0]) > len(x0[1][0]):
##            sortd = False
##            results_sorted_char_count[i] = x1
##            results_sorted_char_count[i + 1] = x0
##for i in range(len(results_sorted_char_count[:n])):
##    x = results_sorted_char_count[i]
##    print('{}. {} chars: {} \t({})'.format(i + 1, len(x[1][0]), x[0], ' '.join(x[1][0])))



print('\nDone.\n')



