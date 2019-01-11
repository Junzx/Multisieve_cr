from pprint import pprint
lst_document = []
lst_gold_document = []
lst_result_document = []

with open('log_prf.txt','r') as hdl_prf:
	for line in hdl_prf:
		if line.startswith('====>'):
			lst_document.append(line)

with open('all_gold_data.v4_gold_conll','r') as hdl_gold:
	for line in hdl_gold:
		if 'begin' in line:
			lst_gold_document.append(line)

with open('result_conll.v4_result_conll','r') as hdl_result:
	for line in hdl_result:
		if 'begin' in line:
			lst_result_document.append(line)




# for i in range(10):
	# print lst_gold_document[i],lst_result_document[i]

set_docu = set(lst_document)
set_gold = set(lst_gold_document)
set_resu = set(lst_result_document)

pprint(set_gold - set_resu)

new_lst_document = list(set([i.strip('\n')[6:-1] for i in lst_document]))
new_lst_gold_document = list(set([i.strip('\n')[16:] for i in lst_gold_document]))
new_lst_result_document = list(set([i.strip('\n')[16:] for i in lst_gold_document]))

# for i in range(10):
	# print new_lst_document[i],'|',new_lst_gold_document[i],'|',new_lst_result_document[i]

print 'PRF:', len(lst_document),len(new_lst_document),len(set_docu)
print 'GOLD:',len(lst_gold_document),len(new_lst_gold_document),len(set_gold)
print 'RESULT:',len(lst_result_document),len(new_lst_result_document),len(set_resu)

# print '~',len(set(new_lst_document)),len(set(lst_document))
# print '~',len(set(new_lst_gold_document)),len(set(lst_gold_document))
# print '~',len(set(new_lst_result_document)),len(set(lst_result_document))