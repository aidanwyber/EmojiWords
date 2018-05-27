#python36

'''
Find words that can be written with emoji only.
List of 354986 English words from: https://github.com/dwyl/english-words
'''

import re

extended = False
lang = ['english', 'dutch'][1]

outfilename = 'emoji_{}_words_{}.txt'.format(lang, 'extended' if extended else 'blocks_only')


print('Loading file.')

f = open('dict' + lang + '.txt', 'r')
cont = f.readlines()
f.close()

# take away \n at end of line
cont = [x[:-1].replace(' ','') for x in cont]

print('Sorting list.')
cont.sort()
print('Sorted list.')

emoji = None

if extended:
    # these are not in all block form
    # s: dollar sign; z: zzz sleeping icon; r, c, and tm: registered, copyright and trade mark;
    #   y: yen icon on graph; x: cross, sy: dollar/yen icon, e: email icon;
    emoji = ['free', 'soon', 'cool', 'sos', 'atm', 'off', 'new', 'top', 'abc', 'up', 'ok',
             'tm', 'on', 'ab', 'id', 'cl', 'ng', 'vs', 'sy', 'wc', 'o', 'a', 'm', 'p', 'b',
             'v', 'i', 'x', 'e', 'c', 'r', 's', 'y' ,'z']
else:
    # emoji letters in a block
    emoji = ['free', 'soon', 'cool', 'sos', 'atm', 'off', 'new', 'top', 'abc', 'up', 'ok',
             'on', 'ab', 'id', 'cl', 'ng', 'vs', 'wc', 'o', 'a', 'm', 'p', 'b', 'v', 'i']



def emojiparts(w):
    # not so lovely algo that somehow works well
    parts = []
    occ = []
    while len(occ) < len(w):
        found = False
        
        for c in emoji:
            matches = [m.start() for m in re.finditer(c, w)]
            if len(matches) > 0:
                locs = [[m + x for x in range(len(c))] for m in matches]
                
                if not any(any(x in occ for x in l) for l in locs):
                    found = True
                    for k in locs:
                        occ.extend(k)
                    for x in range(len(matches)):
                        parts.append(c)
        
        if not found:
            break

    if len(occ) == len(w):
        return parts
    else:
        return []


res = []
resparts = []

print('Started checking.')
for x in cont:
    ep = emojiparts(x)
    if ep != []:
        res.append(x)
        resparts.append(ep)
        if len(x) > 11:
            print(x, '\t', '-'.join(ep))

print('Done checking.')

max_len = 0
max_word = ''
for x in res:
    if len(x) > max_len:
        max_len = len(x)
        max_word = x

print('Writing.')
f = open(outfilename, 'w')
for i in range(len(res)):
    # margin of 4 spaces between longest word and emojis
    f.write(str(res[i]) + (' ' * (max_len - len(res[i]) + 4)) + '-'.join(resparts[i]) + '\n')
f.close()

print('Done writing.')


print('Longest word:', max_word, max_len)

print('Amt of emoji words versus all:', len(res), '/', len(cont), '=', float(len(res))/len(cont))


