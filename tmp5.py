# coding: utf-8

import InitDocument
import api_md_one_file
import api_cr_one_file
from SubjectUtils.unit_test_utils import print_cluster

article = '濮城油气田隶属于中国石油化工股份有限公司中原油田分公司釆油二厂（前身为东濮石油会战指 挥部釆油第二指挥部）管理，地理上位于河南省濮阳市境内，由范县王楼乡向西南延伸至濮阳县户部寨 乡，油田区域构造位于东濮凹陷中央隆起带东北部。濮城油气田是中国“六五”期间投入开发的储量亿 吨级油气田之一，也是中原油气区动用储量最大、累计生产油气量最多的油气田。'
article1 = '濮城探区到1978年先后进行了6次地震勘探，相继发现了濮城断层和濮城构造，并认识到濮城断层具有同生断层性质，濮城构造是处于洼陷中的屋脊式隆起构造，具有较好的生储盖条件。'
article2 = '1979年1月7日部署在濮城断层屋脊部位的第一口探井-文35井开钻，钻至井深2660m时，在古近系沙河街组沙二段上部发现巨厚砂岩且有良好油气显示，决定提前完钻。'
article3 = '2326.2~2570.8m井段电测解释油层20层62.1m、油水同层1层5.2m。3月5日用4mm油嘴在沙二上2390~2438.8m井段试油，日产原油23t、气2150m3,从而发现了濮城油气田。'

data = InitDocument.Article2DocumentObject(article=article)

api_md_one_file.main(data)

print dir(data)

print '---------------------------'
print data.first_line
for token in data.lst_tokens:
    print token.line

for sent in data.dic_sentences.values():
    print sent.get_sent()
    for token in sent.lst_tokens:
        print "%s/%s " % (token.word_itself, token.token_id),
    print
    print sent.get_sent_parse()
    for m in sent.lst_mentions:
        print m.chinese_word, m.mention_id, m.start_token_id, m.end_token_id, m
    print '--------------------------------------\n'

api_cr_one_file.main(data)
print_cluster(data)
