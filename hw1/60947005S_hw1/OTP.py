import os


def get_text(filename):
    if os.path.isfile(filename):
        ciphertext = []
        with open(filename, encoding='UTF-8') as f:
            for line in f:
                ciphertext.append(line.strip().replace(' ', ''))
        return ciphertext, ciphertext[-1]  # 最後一行為目標
    print('Please put the ciphertext in the right position!')


def collect_col(text):  # 收集所有同一行的字
    each_col = []
    for i in range(0, len(text[-1]), 2):
        tmp = []
        for c in text:
            add = None
            if len(c) >= i+2:
                if c[i:i+2] not in tmp:
                    add = c[i:i+2]
            tmp.append(add)
        each_col.append(tmp)
    return each_col


def do_xor(word1, word2):  # 轉成10進位，使用 ^ 運算
    return int(word1, 16) ^ int(word2, 16)


def correct(text, key, word, index):  # 手動校正金鑰; 參數: 密文, 金鑰, 字母, 第幾行第幾個字
    key[index[1]] = hex(do_xor(hex(ord(word))[2:], text[index[0]][index[1]*2: index[1]*2+2]))[2:]


def show(text, key):
    # 表格索引值
    print('result({0}):'.format(len(key)))
    print(end='   ')
    for i in range(len(key)):
        if i % 10:
            print(end=' ')
        else:
            print(i//10, end='')
    print()
    print(end='   ')
    for i in range(len(key)):
        print(i % 10, end='')
    print()

    index = 0
    for t in text:
        print('{:<2}'.format(index), end=' ')  # 顯示行數
        index += 1
        for i in range(len(key)):
            if key[i]:
                if len(t) >= i*2+2:
                    print(chr(do_xor(t[i*2:i*2+2], key[i])), end='')
            else:
                print(end='@')  # 未找到
        print()


def main():
    cipher, target = get_text("2021_otp/ciphertext.txt")
    key = []  # elements' type is string
    key_file = "2021_otp/key.txt"
    if os.path.isfile(key_file):
        with open(key_file, encoding='UTF-8') as f:
            for line in f:
                key = line.split()
    else:
        # get each col's ciphertexts
        data = collect_col(cipher)

        # statistics and generate key
        for word in data:
            record = [[0]*len(word) for _ in range(len(word))]
            for i in range(len(word)-1):
                if word[i]:
                    for j in range(i+1, len(word)):
                        if word[j]:
                            if chr(do_xor(word[i], word[j])).isalpha():
                                record[i][j] += 1
                                record[j][i] += 1
            # 找出與其他字 XOR 後，出現最多字母的設為空格
            max_id, total = 0, sum(record[0])
            for i in range(1, len(word)):
                tmp = sum(record[i])
                if tmp > sum(record[max_id]):
                    max_id, total = i, tmp
            if total:
                key.append(hex(do_xor(hex(ord(' '))[2:], word[max_id]))[2:])
            else:
                key.append(None)

    # correct the key with the ciphertext
    while True:
        show(cipher, key)
        change = input('input: word and pos to correct the ans>>> ').split()
        if len(change) != 3:
            break
        else:
            correct(cipher, key, change[0], [int(change[1]), int(change[2])])
        print('\n')

    # save the key
    save = input('save? (y/n)').lower()
    if save == 'y':
        with open(key_file, 'w', encoding='UTF-8') as f:
            print(*key, file=f)


if __name__ == '__main__':
    main()
