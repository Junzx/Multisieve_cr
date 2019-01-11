from os import popen

with open('log_prf.txt','w') as hdl_prf:
	output = popen('perl scorer.pl muc all_gold_data.v4_gold_conll result_conll.v4_result_conll')
	for i in output.read():
		hdl_prf.write(i)