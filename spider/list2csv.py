# -*- coding: utf-8 -*-
import csv

out     = [] 
with open('line.list','rb') as f:
	while 1:
		l = f.readline()
		if not l:break
		lst = l.split('||')
		out.append(lst)


csvfile1 = file('phoneNum.csv', 'wb')
writer  = csv.writer(csvfile1)
writer.writerow(['公司名', '项目名', '项目年份', '固定电话', '手机', '所在地区', '来源网页'])
writer.writerows(out)
print out
csvfile1.close()

out     = [] 
with open('legalButNoTel.txt','rb') as f:
	while 1:
		l = f.readline()
		if not l:break
		lst = l.split('||')
		out.append(lst)

csvfile2 = file('noTel.csv', 'wb')
writer   = csv.writer(csvfile2)
writer.writerow(['公司名', '项目名'])
writer.writerows(out)
csvfile2.close()