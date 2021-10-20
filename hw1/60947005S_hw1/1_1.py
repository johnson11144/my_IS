import math


def hw1_1_2():
    data = {}
    for _ in range(7):
        tmp = input().split()
        for i in range(0, len(tmp), 2):
            data[tmp[i]] = float(tmp[i+1])
    cal = []
    for d in sorted(data):
        print(d)
        cal.append(round(data[d] * math.log(data[d], 2), 3))
    print(sum(cal))


def hw1_1_3():
    data = {}  # record alpha and probability
    for _ in range(7):
        tmp = input().split()
        for i in range(0, len(tmp), 2):
            data[tmp[i]] = float(tmp[i+1])
    show_prob = {**data}  # 複製一份，用於計算期望值
    # huffman = {root: {0: left_child, 1: right_child}}}
    huffman_tree = {}
    while len(data) > 1:
        key_set = sorted(data, key=lambda x: data[x])
        k = [key_set[i] for i in range(2)]
        p = [data.pop(k[i]) for i in range(2)]
        new_k, new_p = k[0]+k[1], p[0]+p[1]
        data[new_k] = new_p  # key表示擁有的字母，val表示總機率
        tree = {}  # 建新樹
        for i in range(2):  # i=0, 建左子樹; i=1, 建右子樹
            if len(k[i]) == 1:  # leaf node
                tree[k[i]] = i
            else:  # sub_tree，去樹集合找
                tree[k[i]] = huffman_tree.pop(k[i])
        if len(data) == 1:
            huffman_tree['root'] = tree  # 根結點
        else:
            huffman_tree[new_k] = tree  # 加入樹集合
    print(show_prob)
    expect = 0  # 統計期望值
    for i in range(26):
        find = huffman_tree['root']
        alpha = chr(ord('a')+i)
        s = ''
        print(alpha, end=': ')
        while find.get(alpha) != 0 and find.get(alpha) != 1:  # 未找到leaf_node
            code = 0
            for k in find:  # check each key
                if alpha in k:  # if the alphabet in key
                    s += str(code)
                    find = find[k]
                    break
                code += 1
        s += str(find[alpha])
        print(s)  # show huffman code
        expect += (len(s)*show_prob[alpha])  # 計算長度的期望值
    print(expect)


hw1_1_3()
