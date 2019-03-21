### 文件结构

- ClassDefinition 定义各个类的结构
    - Definition_Document.py
    - Definition_Sentence.py
    - Definition_Mention.py
    - Definition_Entity.py
    - Definition_Token.py
- MentionDetection 负责提取表述
    - exact_np_by_tree.py 通过括号提取候选表述
- Multisieve 定义各个sieve
- RunResults 存放运行时及运行结束的prf结果
- Scorer 会议提供的评测程序
- SubjectUtils 各个util程序
    - experiment_utils.py 实验中需要的utils
    - sieve_utils.py 各个sieve处理时需要的utils
    - unit_test_utils.py 一些打印函数
- UserCorpus 自定义的语料资源
    - Corpus 个人定义的语料
    - api_user_corpus.py 用来定义调用语料的结构函数
- api_cr_all_file.py [指代消解部分]根据config.py 处理一个文件夹的文档
- api_cr_one_file.py [指代消解部分]设置需要用的sieve，处理一个文档，返回对应的prf
- api_md_all_file.py [表述提取部分]根据config.py 处理一个文件夹的文档
- api_md_one_file.py [表述提取部分]对一个文档进行表述提取
- InitDocument.py 处理句子/文章，构成Document对象给MD
- nlp_tools.py 设置调用斯坦福工具
- config.py 定义数据路径等内容
- ConstantVariable.py 定义一些常量
- LoadConll.py 读取conll格式文件的函数，分为读取普通的和读取文件用于表述提取实验的
- tmp.py *
- LAB.py 临时函数

### 数据统计

#### train
```
bn
(918, 219814, 26505, 7475)
mz
(64, 128390, 19478, 4941)
nw
(261, 78889, 25673, 9047)
bc
(198, 119388, 12252, 2793)
wb
(179, 129910, 10043, 2419)
tc
(190, 79672, 8903, 1582)
```

#### test
```
(218, 92308, 12801, 3559)
```

---

### Bug fix

- 打log不完整
- SubjectUtils.sieve_utils.py  get_candidate_mentions
- SubjectUtils.sieve_utils.py  get_modifier
- Experiment.ExperimentResult.load_mention_info_result.py 改为load json
- Multisieve.exact_match.py 增加了确定字符串比较
- Scorer.api_prf 改成写入log文件，不再print


---
### 重要备忘：

2019-3-6 新增了Mention Detection的实验，可能后续版本开始混乱
2019-3-20 开始修复bug
    - 所有的print都用pprint工具
    - bug fix
    - 将sieve order新建了一个config py
    - 词林实现参考：https://github.com/norybaby/cilin_similarity