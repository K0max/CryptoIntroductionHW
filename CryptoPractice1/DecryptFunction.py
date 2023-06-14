import re
import enchant
import random
import string

def checkKey(key):
    if key.isnumeric():
        return True
    if len(key) == 26 and key.isalpha() and key.islower():
        return True
    return False

def checkCipherText(cipherText):
    if len(cipherText) == 0:
        return False
    if not all(c.isalpha() or c.isspace() for c in cipherText):
        return False
    return True

def decrypt(cipherText, key):
    if key.isnumeric():
        plainText = KaiserDecrypt(cipherText, key)
        # print("The plain text (using this key) is: ", KaiserDecrypt(cipherText, key), sep='\n')
    else:
        plainText = monoAlphabeticDecrypt(cipherText, key)
        # print("The plain text (using this key) is : ", monoAlphabeticDecrypt(cipherText, key), sep='\n')
    return plainText

def KaiserDecrypt(cipherText, key):
    plainText = ""
    key_num = int(key) % 26
    for i in range(len(cipherText)):
        if cipherText[i].isalpha():
            if cipherText[i].isupper():
                plainText += chr(((ord(cipherText[i]) - ord('A') - key_num) % 26) + ord('A'))
            else:
                plainText += chr(((ord(cipherText[i]) - ord('a') - key_num) % 26) + ord('a'))
        else:
            plainText += cipherText[i]
    return plainText

def monoAlphabeticDecrypt(cipherText, key):
    plainText = ""
    alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    key = list(key)
    for cipherChar in cipherText:
        if not cipherChar.isalpha():
            plainText += cipherChar
        else:
            plainText += alphabet[key.index(cipherChar.lower())].upper() if cipherChar.isupper() else alphabet[key.index(cipherChar)]
    return plainText

# 文件（密文）中的字母频率统计，返回值为字典，键为字母，值为频率
def countLetterFrequency(text):
    cipherLetterFrequency = {}
    text = text.lower()
    for letter in text:
        if letter.isalpha():
            if letter in cipherLetterFrequency:
                cipherLetterFrequency[letter] += 1
            else:
                cipherLetterFrequency[letter] = 1
    return cipherLetterFrequency

# 文件（密文）中的单词频率统计，返回值为字典，键为单词，值为频率
def countWordFrequency(text):
    cipherWordFrequency = {}
    text = text.lower()
    # replace all , and \n and . and ; with space
    text = re.sub(r'[,\n.;]', ' ', text)
    wordsInText = text.split()
    for word in wordsInText:
        if word in cipherWordFrequency:
            cipherWordFrequency[word] += 1
        else:
            cipherWordFrequency[word] = 1
    return cipherWordFrequency

def letterFrequencyAnalysis(cipherLetterFrequency):
    # 26个英文字母的出现频率
    ENGLISH_FREQUENT_LETTERS = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
    # 把字典按值排序，返回值为列表，列表中的元素为元组，元组中的第一个元素为键，第二个元素为值，然后再把他转换为字典
    # print(cipherLetterFrequency)
    sortedLetterFrequencyDict = dict(sorted(list(cipherLetterFrequency.items()), key=lambda x: x[1], reverse=True))
    # 把字典的键转换为字符串
    sortedLetterFrequencyStr = ''.join(sortedLetterFrequencyDict.keys())
    key = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    cipherLetterNum = len(sortedLetterFrequencyStr)
    unusedLetter = "".join([letter for letter in alphabet if letter not in sortedLetterFrequencyStr])
    unusedIndex = 0
    for letter in alphabet:
        # 由于明文中可能有部分字母没用到，所以只取频率最高的字母
        if ENGLISH_FREQUENT_LETTERS.index(letter) < cipherLetterNum:
            key += sortedLetterFrequencyStr[ENGLISH_FREQUENT_LETTERS.index(letter)]
        else:
            # 由于这部分字母在频率排列中大于密文中的字母数，所以取密文没用到的字母（频率最低）
            key += unusedLetter[unusedIndex]
            unusedIndex += 1
    # print("A possible key is: ", str(key), sep='')
    return key, sortedLetterFrequencyStr

def wordFrequencyAnalysis(cipherWordFrequency):
    ENGLISH_FREQUENT_WORDS = ['a', 'i', 'be', 'we', 'to', 'it', 'of', 'do', 'in', 'my', 'me', 'in', 'you', 'the', 'not', 'and', 'get', 'that', 'have', 'what', 'this']
    ENGLISH_FREQUENT_WORDS = str(ENGLISH_FREQUENT_WORDS)
    # sort the word frequency dictionary, key is word(string), value is frequency(int)
    sortedWordFrequency = dict(sorted(list(cipherWordFrequency.items()), key=lambda x: x[1]))
    # sort by length of word
    sortedWordFrequency = dict(sorted(sortedWordFrequency.items(), key=lambda x: len(x[0])))
    # convert the dictionary's key to string and put space between words
    sortedWordFrequency = ' '.join(sortedWordFrequency.keys())
    return ENGLISH_FREQUENT_WORDS, sortedWordFrequency
    
def addMapping(key, preimage, image):
    alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    # 去掉preimage, image中的非字母字符
    preimage = re.sub(r'[^a-zA-Z]', '', preimage)
    image = re.sub(r'[^a-zA-Z]', '', image)
    prevKey = key
    key = list(key)
    preimage = list(preimage)
    image = list(image)
    for i in range(len(preimage)):
        if not preimage[i].isalpha() or not image[i].isalpha():
            continue
        key[key.index(image[i])], key[alphabet.index(preimage[i])] = key[alphabet.index(preimage[i])], image[i] 
    key = ''.join(key)
    return key, prevKey

def similar(key, nextKey):
    # 检查两个密钥中位置相同的字母的个数
    sameLetterNum = 0
    for i in range(len(key)):
        if key[i] == nextKey[i]:
            sameLetterNum += 1
    return float(sameLetterNum) / len(key)

def wordTip(ciphertext, key, targetWord):
    currentPlainText = monoAlphabeticDecrypt(ciphertext, key)
    if not targetWord in currentPlainText:
        tip_text = "The target word is not in the current plain text."
        return tip_text
    else:
        currentPlainText = re.sub(r'[,\n.;]', ' ', currentPlainText)
        ciphertext = re.sub(r'[,\n.;]', ' ', ciphertext)
        currentPlainText = currentPlainText.split()
        ciphertext = ciphertext.split()
        cipherWord = ciphertext[currentPlainText.index(targetWord)]
        d = enchant.Dict("en_US")
        if not d.check(targetWord):
            possibleWords = d.suggest(targetWord)
            if len(possibleWords) == 0:
                tip_text = "There are no similar words in the dictionary."
                return tip_text
            possibleWords = [possibleWord.lower() for possibleWord in possibleWords]
            tip_text = f"Target word in cipher is {cipherWord}. Possible plain words are: "
            for possibleWord in possibleWords:
                tip_text += possibleWord + ", "
            return tip_text

def improveKey(ciphertext, key):
    currentPlainText = monoAlphabeticDecrypt(ciphertext, key)
    d = enchant.Dict("en_US")
    currentPlainText = re.sub(r'[,\n.;]', ' ', currentPlainText)
    ciphertext = re.sub(r'[,\n.;]', ' ', ciphertext)
    wordsInCipherText = ciphertext.split()
    wordsInCurrentPlainText = currentPlainText.split()
    wordsInCipherText = sorted(wordsInCipherText, key=lambda x: len(x), reverse=True)
    wordsInCurrentPlainText = sorted(wordsInCurrentPlainText, key=lambda x: len(x), reverse=True)
    correctWordNum = 0
    # 统计当前明文中正确的单词数
    for word in wordsInCurrentPlainText:
        if d.check(word):
            correctWordNum += 1
    for word in wordsInCurrentPlainText:
        # 如果单词不在字典中，给出类似的单词
        if not d.check(word):
            possibleWords = d.suggest(word)
            # 去除possibleWords中和word长度不同的单词
            possibleWords = [possibleWord for possibleWord in possibleWords if len(possibleWord) == len(word)]
            # 将possibleWords中的单词转为小写
            possibleWords = [possibleWord.lower() for possibleWord in possibleWords]
            # 如果没有类似的单词，跳过
            if len(possibleWords) == 0:
                continue
            for possibleWord in possibleWords:
                if similar(possibleWord, word) < 0.7:
                    continue
                # if possibleWord == possibleWords[-1]:
                #     continue
                else:
                    key, prevKey = addMapping(key, possibleWord, wordsInCipherText[wordsInCurrentPlainText.index(word)])
                    improvedPlainText = monoAlphabeticDecrypt(ciphertext, key)
                    improvedPlainText = re.sub(r'[,\n.;]', ' ', improvedPlainText)
                    improvedPlainText = improvedPlainText.split()
                    improvedCorrectWordNum = 0
                    for word in improvedPlainText:
                        if d.check(word):
                            improvedCorrectWordNum += 1
                    if improvedCorrectWordNum > correctWordNum:
                        if improvedCorrectWordNum - correctWordNum > 3:
                            print("The key has been greatly improved.")
                            return improveKey(ciphertext, key)
                        else:
                            return key
                    else:
                        key = prevKey
                        print("No improvement.")
                        return key
                    
def checkProcess(plaintext):
    plaintext = re.sub(r'[,\n.;]', ' ', plaintext)
    plaintext = plaintext.split()
    totalWordNum = len(plaintext)
    d = enchant.Dict("en_US")
    correctWordNum = 0
    wrongWords = []
    for word in plaintext:
        if d.check(word):
            correctWordNum += 1
        else:
            wrongWords.append(word)
    process = float(correctWordNum) / totalWordNum
    wrongWords = ', '.join(wrongWords)
    return process, wrongWords