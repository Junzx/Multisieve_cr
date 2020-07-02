from LoadConll import load_one_file
import config
from SubjectUtils.unit_test_utils import print_gold_cluster

shit = """
/opt/tmp/DataSets/conll_test/test/cts_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0059_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnn_0004_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/phoenix_0009_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0109_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0049_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0059_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0129_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0289_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0139_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0009_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_010.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0319_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0029_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0049_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cctv_0007_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0219_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0029_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_003.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_003.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0259_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0069_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0039_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0199_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0059_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0139_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0099_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/e2c_0009_003.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0179_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0009_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0149_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0109_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0169_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0119_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0009_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0009_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0099_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_005.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cctv_0007_005.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0119_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0049_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0169_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0279_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0119_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0059_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0229_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0299_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0049_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0149_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0079_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0109_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0049_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0029_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0039_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0239_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0239_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0009_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0189_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0249_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0019_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0099_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0029_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0089_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0079_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0219_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0299_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0019_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0159_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0189_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0029_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0019_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/phoenix_0009_003.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_006.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0229_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0009_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0069_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0009_003.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0159_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0009_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_009.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cctv_0007_006.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0119_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0269_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0239_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0209_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_008.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0009_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0059_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0079_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0009_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0159_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0189_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/e2c_0009_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0099_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_007.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0029_003.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cctv_0007_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0079_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0009_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0249_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0099_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_005.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0029_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_1019_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0079_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0159_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cnr_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0029_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0089_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/chtb_0019_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0299_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0099_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0189_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0269_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/phoenix_0009_006.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0269_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_007.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0079_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0309_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0109_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0139_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0089_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0029_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0279_000.v4_gold_conll
"""

shit2 = """
/opt/tmp/DataSets/conll_test/test/cts_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0049_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0139_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0009_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_010.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0049_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cctv_0007_004.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0119_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0009_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0049_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/dev_09_cmn_0039_001.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0009_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0189_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0019_006.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cctv_0007_006.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0119_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ch_0039_007.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cctv_0007_002.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0249_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0099_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/vom_0299_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cmn_0039_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/ctv_0079_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cbs_0089_000.v4_gold_conll
/opt/tmp/DataSets/conll_test/test/cts_0279_000.v4_gold_conll
"""

file_path = config.gold_test
for file_idx, file in enumerate([i for i in shit.split('\n') if i != '']):
    data = load_one_file(file)
    # if 30 < len(data.gold_mention) < 50:
    #     print file
        # print data.article
        # print
    print file
    print data.article