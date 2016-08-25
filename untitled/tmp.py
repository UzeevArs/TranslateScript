import codecs
import re
import os
import sqlite3
import requests

#global findALL
#Path = 'C:\\Users\\Jeggy\\Desktop\\Crcx160415_Rev4.13\\'
#con1 = '\".*\"|\'.*'
#con2 = '[一-龯ぁ-んァ-ンぁ-ゔゞァ-・ヽヾ゛゜ーバ－コﾘﾄﾗｲﾌｸﾞ]\w*'
# |\'[一-龯ぁ-んァ-ン]'

def translateFunction(Path, con1, con2):
    mass = array = [[], [], [], [], [], []]
    global allItem
    allItem = array = [[], [], [], [], [], []]
    namesWithPath = []
    namesWithPathf = []
    names = []
    namesf = []
    readStr = []
    readStr2 = []
    a = 0
    def sortByLength(inputStr):
        return len(inputStr)

    for top, dirs, files in os.walk(Path):
        for nm in files:
            namesWithPathf.append(os.path.join(top, nm))
            namesf.append(os.path.join(nm))
    for x in namesWithPathf:
        if ((x[len(x) - 3:len(x)] == 'bas') or (x[len(x) - 3:len(x)] == 'frm')):
            namesWithPath.append(x)

    for x in namesf:
        if ((x[len(x) - 3:len(x)] == 'bas') or (x[len(x) - 3:len(x)] == 'frm')):
            names.append(x)


    while a <= (namesWithPath.__len__() - 1):
        with codecs.open(namesWithPath[a], 'r', errors='ignore') as f:
            try:
                readStr = re.findall(con1, f.read())
            except BaseException:
                print(namesWithPath[a])
        l = readStr.__len__()
        i = 0
        while i <= (l - 1):
            if re.findall(con2, readStr[i]) != []:
                mass[0].append(readStr[i])
                mass[4].append(readStr[i])
                mass[2].append(names[a])

            print('stage {0}'.format(i) )
            i = i + 1
        if mass[0].__len__() == 0:
            print(names[a], 'Переведён')
        else:
            mass[0].sort(key = sortByLength, reverse=1)
            mass[4].sort(key = sortByLength, reverse=1)
        readStr = []
        l = mass[0].__len__()
        i = 0
        while i <= (l - 1):
            mass[1].append('; '.join(re.findall(con2, mass[0][i])))
            i += 1
        i = 0
        with codecs.open(namesWithPath[a], errors='ignore') as f:
            testText = f.read()
            CurrTextParse = []
        while i <= (mass[1].__len__() - 1):
            CurrText = mass[1][i]
            CurrTextParse = CurrText.split('; ')
            ReplText = ''
            ReplTextParse = []
            if len(CurrTextParse) > 1:
                CurrTextParse.sort(key = sortByLength, reverse=1)
                s = 0
                while s <= (CurrTextParse.__len__() - 1):
                    eng_request = requests.get('https://www.googleapis.com/language/translate/v2',
                                               {'key': 'AIzaSyA9yfFTNWv4MUOTmKj0I4_oHfszOFodrDI',
                                                'q': CurrTextParse[s],
                                                'source': 'ja',
                                                'target': 'en'})
                    if eng_request.status_code == 200:
                        eng = eng_request.json()['data']['translations'][0]['translatedText']
                    else:
                        eng = ''
                    ReplTextParse.append(eng)
                    mass[3].append(eng)
                    mass[4][i] = re.sub(CurrTextParse[s],ReplTextParse[s], mass[4][i])
                    s = s+1
                findALL = print('translate {0}'.format(i), names[a])
                i = i + 1
            else:
                eng_request = requests.get('https://www.googleapis.com/language/translate/v2',
                                           {'key': 'AIzaSyA9yfFTNWv4MUOTmKj0I4_oHfszOFodrDI',
                                            'q': CurrText,
                                            'source': 'ja',
                                            'target': 'en'})

                if eng_request.status_code == 200:
                    eng = eng_request.json()['data']['translations'][0]['translatedText']
                else:
                    eng = ''
                ReplText = eng
                mass[3].append(eng)
                mass[4][i] = re.sub(CurrText,ReplText, mass[4][i])
                print('translate {0}'.format(i), names[a])
                i = i + 1

        i = 0
        while i <= (mass[1].__len__() - 1):
            CurText = mass[0][i]
            RepText = mass[4][i]
            try:
                testText = testText.replace(CurText, RepText) #re.sub(CurText, RepText, testText)
            except BaseException:
                print(mass[0][1])
            i = i + 1
            print('write {0}'.format(i))
        i = 0
        testTextParse = testText.split('\n')

        if l != 0:
            with codecs.open(namesWithPath[a], 'w', errors='ignore') as f:
                for line in testTextParse:
                    try:
                        f.writelines('{0}\n'.format(line))
                    except Exception as error:
                        print('{0}\n{1}'.format(error,line))
                        f.writelines('{0}\n'.format('INVALID STRING'))

        allItem[0].append(mass[0])
        allItem[1].append(mass[1])
        allItem[2].append(mass[2])
        allItem[3].append(mass[3])
        allItem[4].append(mass[4])
        mass[0] = []
        mass[1] = []
        mass[2] = []
        mass[3] = []
        mass[4] = []
        mass[5] = []
        a = a + 1
    return (print (BaseException))



def writeToDatabase(nameDatabase):
    l = allItem[0].__len__()
    if (l != 0):
        count = 1
        con = sqlite3.connect('nameDatabase')
        cursor = con.cursor()
        i = 0
    while i <= (l - 1):
        data = [{'row': allItem[0][i], 'data': allItem[1][i], 'file': allItem[2][i], 'id': count, 'JPtoEN': allItem[3][i],
                 'RawEng': allItem[4][i]}]
        for japan in data:
            cursor.execute(
                "INSERT INTO japan (row, japaniese, files, id, English_google, russian_google) VALUES (:row, :data, :file, :id, :JPtoEN, :RawEng)",
                japan)
        for japan_full in data:
            cursor.execute(
                "INSERT INTO japan_full (row, japaniese, files, id, English_google, russian_google) VALUES (:row, :data, :file, :id, :JPtoEN, :RawEng)",
                japan_full)
        count = count + 1
        i = i + 1
    if l!= 0:
        cursor.execute("delete from japan WHERE exists (select 1 from japan_full where japan.id < japan_full.id AND japan.row = japan_full.row)")
        con.commit()
        cursor.close()
        con.close()
        allItem.clear()
    else:
        print('translated')
    return (print (BaseException))


