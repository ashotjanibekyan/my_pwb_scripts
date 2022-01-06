import pywikibot as pw
from pywikibot import pagegenerators as pg

commons = pw.Site('commons', 'commons')

cat = pw.Category(commons, 'Images from Wiki Loves Earth 2021 in Armenia')
members = list(cat.members())

users = {}
for file in members:
    if file.is_filepage():
        if file.oldest_file_info['user'] in users:
            users[file.oldest_file_info['user']] += 1
        else:
            users[file.oldest_file_info['user']] = 1
    else:
        print(file)

text = '''{| class="wikitable sortable"
! Մասնակից !! Ֆայլերի քանակ'''

users_m = []

for user in users:
    users_m.append([user, users[user]])

users = sorted(users_m, key=lambda x : (-x[1], x[0]))

for user in users:
    text += '\n|-\n| ' + user[0] + ' || ' + str(user[1])
text += '\n|}'

hywiki = pw.Site('hy', 'wikipedia')

page = pw.Page(hywiki, 'Մասնակից:Beko/Վիքիհաշվիչ')

page.text = text

page.save(summary='թարմացնել')

