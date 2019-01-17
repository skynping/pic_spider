# coding: utf-8

import io

sort_list = []
f = io.open("pic_pex_sorts.txt","r")
for sort in f.readlines():
    sort_list.append(sort.replace("\n",""))
    print sort
print sort_list
