

#### exact match 

    {'bcub': ('93.36%', '1.46%', '2.88%'),
     'blanc': ('91.78%', '0.63%', '1.25%'),
     'ceafe': ('62.84%', '2.48%', '4.78%'),
     'muc': ('89.95%', '2.03%', '3.97%')}
     
#### precise_constructs
 
     {'bcub': ('43.28%', '5.55%', '9.85%'),
     'blanc': ('16.16%', '0.92%', '1.74%'),
     'ceafe': ('41.1%', '7.14%', '12.18%'),
     'muc': ('29.23%', '4.09%', '7.17%')}
     ss
#### relaxing_head_matching
 
     {'bcub': ('15.74%', '87.31%', '26.68%'),
     'blanc': ('6.04%', '87.89%', '11.31%'),
     'ceafe': ('67.51%', '8.74%', '15.48%'),
     'muc': ('73.43%', '89.06%', '80.49%')}
     
     
     ！ 修正了一个bug，这个是之后的结果，已添加到excel中
     {'bcub': ('32.59%', '75.59%', '45.55%'),
     'blanc': ('7.61%', '68.28%', '13.69%'),
     'ceafe': ('73.7%', '20.29%', '31.82%'),
     'muc': ('74.22%', '82.33%', '78.06%')}
 
 
#### 代词
    # ---------------------------
    # 所有的属性
    # ---------------------------
    {'bcub': ('53.19%', '5%', '9.15%'),
     'blanc': ('54.07%', '13.21%', '21.23%'),
     'ceafe': ('58.87%', '1.63%', '3.18%'),
     'muc': ('78.32%', '6.68%', '12.32%')}
    
    
    # ---------------------------
    # 仅使用动物属性
    # ---------------------------
    规则： 
    {'bcub': ('36.65%', '12.24%', '18.35%'),
     'blanc': ('30.12%', '26.78%', '28.35%'),
     'ceafe': ('52.46%', '2.66%', '5.07%'),
     'muc': ('74.95%', '16.83%', '27.49%')}
     
     cnn：
     {'bcub': ('38.47%', '13.15%', '19.6%'),
     'blanc': ('32.14%', '28.49%', '30.21%'),
     'ceafe': ('53.21%', '3.18%', '6.01%'),
     'muc': ('74.35%', '17.85%', '28.79%')}
     
     规则+cnn
     ------------------------------
    {'bcub': ('36.38%', '13.59%', '19.79%'),
     'blanc': ('30.19%', '29.27%', '29.72%'),
     'ceafe': ('51.64%', '2.88%', '5.46%'),
     'muc': ('74.82%', '18.32%', '29.44%')}
     
      ！ 加上距离约束后
     {'bcub': ('54.82%', '6.67%', '11.9%'),
     'blanc': ('39.3%', '3.79%', '6.91%'),
     'ceafe': ('37.6%', '8.27%', '13.56%'),
    'muc': ('53.64%', '11.05%', '18.33%')}
 
#### strict A

    {'bcub': ('88.69%', '37.72%', '52.93%'),
     'blanc': ('77.06%', '30.15%', '43.35%'),
     'ceafe': ('77.38%', '38.28%', '51.23%'),
     'muc': ('91.1%', '44.79%', '60.06%')}
     
#### strict B
 
     {'bcub': ('87.38%', '41.66%', '56.42%'),
     'blanc': ('74.96%', '33.18%', '46%'),
     'ceafe': ('77.02%', '41.98%', '54.34%'),
     'muc': ('90.08%', '48.77%', '63.28%')}
     
#### strict C

    {'bcub': ('87.66%', '38.74%', '53.73%'),
     'blanc': ('76.01%', '30.66%', '43.69%'),
     'ceafe': ('77.89%', '38.52%', '51.55%'),
     'muc': ('90.61%', '45.62%', '60.69%')}

#### proper_header_word_match_sieve

    {'bcub': ('85.72%', '43.58%', '57.79%'),
     'blanc': ('73.48%', '33.87%', '46.37%'),
     'ceafe': ('76.93%', '43.19%', '55.32%'),
     'muc': ('88.74%', '50.24%', '64.16%')}
     
#### discourse  
    {'bcub': ('51.49%', '0.71%', '1.4%'),
     'blanc': ('32.92%', '0.31%', '0.61%'),
     'ceafe': ('37.01%', '1%', '1.96%'),
     'muc': ('43.75%', '1.06%', '2.07%')}
     
     
#### other sieve

    'bcub': ('91.97%', '32.14%', '47.63%'),
    'blanc': ('80.35%', '14.08%', '23.97%'),
    'ceafe': ('60.44%', '44.36%', '51.17%'),
    'muc': ('92.25%', '43.19%', '58.84%')}

---
---

#### 综合版本

1. 实验1；按照bcub的排序
    
        sieve_order = [
                # test_sieve,
                exact_match,
                strict_head_matching_A,
                strict_head_matching_B,
                strict_head_matching_C,
                proper_header_word_match_sieve,
                precise_constructs,
                relaxing_head_matching,
                discourse_processing,
                pronoun_sieve,
                other_sieve,
                filter_sieve,
            ]
        
        {'bcub': ('26.18%', '90.34%', '40.6%'),
        'blanc': ('6.92%', '93.27%', '12.89%'),
        'ceafe': ('74.83%', '22.03%', '34.04%'),
        'muc': ('75.02%', '92.14%', '82.7%')}
        
2. 实验2

        exact_match,
        strict_head_matching_A,
        
        {'bcub': ('89.06%', '37.37%', '52.64%'),
         'blanc': ('78.56%', '29.67%', '43.07%'),
         'ceafe': ('75.55%', '38.7%', '51.18%'),
         'muc': ('90.81%', '44.49%', '59.72%')}
        
3. 实验3

        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        
        {'bcub': ('87.92%', '40.84%', '55.77%'),
        'blanc': ('76.57%', '32.1%', '45.24%'),
        'ceafe': ('74.75%', '42.44%', '54.14%'),
        'muc': ('89.75%', '48.06%', '62.6%')}
        
4. 实验4

        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        
        {'bcub': ('87.46%', '41.69%', '56.47%'),
         'blanc': ('76.05%', '32.34%', '45.38%'),
         'ceafe': ('74.99%', '43.04%', '54.7%'),
         'muc': ('89.46%', '48.76%', '63.12%')}
         
5. 实验5

        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        proper_header_word_match_sieve,
        
        {'bcub': ('86.91%', '42.53%', '57.11%'),
        'blanc': ('75.69%', '32.47%', '45.45%'),
        'ceafe': ('74.57%', '44.15%', '55.46%'),
        'muc': ('88.66%', '49.33%', '63.39%')}
        
6. 实验6
       
        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        proper_header_word_match_sieve,
        precise_constructs,
        
        {'bcub': ('80.85%', '45.18%', '57.97%'),
         'blanc': ('68.06%', '33.64%', '45.03%'),
         'ceafe': ('73.24%', '45.15%', '55.86%'),
         'muc': ('83.61%', '51.25%', '63.55%')}
        
7. 实验7-relax性能太差

        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        proper_header_word_match_sieve,
        precise_constructs,
        relaxing_head_matching,
        
        
        {'bcub': ('26.58%', '83.48%', '40.32%'),
         'blanc': ('6.61%', '84.93%', '12.26%'),
         'ceafe': ('73.87%', '20.85%', '32.53%'),
         'muc': ('74.3%', '85.78%', '79.63%')}
        
8. **实验8-结果最好**

        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        proper_header_word_match_sieve,
        precise_constructs,
        pronoun_sieve,
        other_sieve,
        filter_sieve,
        
        {'bcub': ('68.63%', '66.82%', '67.71%'),
         'blanc': ('34.78%', '66.84%', '45.75%'),
         'ceafe': ('76.51%', '56.09%', '64.73%'),
         'muc': ('82.84%', '74.71%', '78.56%')}
         
9. 实验9
         
        exact_match,        
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        proper_header_word_match_sieve,
        precise_constructs,
        pronoun_sieve
        
        
        {'bcub': ('65.67%', '59.65%', '62.51%'),
         'blanc': ('34.45%', '65.85%', '45.24%'),
         'ceafe': ('72.86%', '43.32%', '54.33%'),
         'muc': ('81.93%', '69.37%', '75.13%')}

10. 实验10-效果也很好

        sieve_order = [
            test_sieve,
            exact_match,
            strict_head_matching_A,
            strict_head_matching_B,
            strict_head_matching_C,
            proper_header_word_match_sieve,
            precise_constructs,
            discourse_processing,
            pronoun_sieve,
            other_sieve,
            filter_sieve,
        ]
        
        {'bcub': ('64.63%', '67.88%', '66.21%'),
        'blanc': ('24.28%', '68.81%', '35.89%'),
        'ceafe': ('76.71%', '54.19%', '63.51%'),
        'muc': ('82.47%', '75.44%', '78.8%')}


11. 实验11

        sieve_order = [
        test_sieve,
        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        proper_header_word_match_sieve,
        # precise_constructs,
        # relaxing_head_matching,
        discourse_processing,
        pronoun_sieve,
        other_sieve,
        filter_sieve,
   
        {'bcub': ('70.24%', '65.43%', '67.75%'),
        'blanc': ('28.53%', '65.8%', '39.81%'),
        'ceafe': ('77.25%', '56.84%', '65.49%'),
        'muc': ('84.83%', '74.22%', '79.17%')}

   
             
---
---

        
    # 按照Precision降序
    sieve_order = [
            test_sieve,
            exact_match,
            strict_head_matching_A,
            strict_head_matching_B,
            strict_head_matching_C,
            proper_header_word_match_sieve,
            pronoun_sieve,
            discourse_processing,
            precise_constructs,
            relaxing_head_matching,
            other_sieve,
            filter_sieve,
    ]
    
    Precision | recall | f1_score
    ------------------------------
    {'bcub': ('40.37%', '81.19%', '53.93%'),
    'blanc': ('8.48%', '81.87%', '15.36%'),
    'ceafe': ('74.58%', '33.74%', '46.46%'),
    'muc': ('75.58%', '86.11%', '80.5%')}
    
    
    # 按照Recall升序
    sieve_order = [
        discourse_processing,
        exact_match,
        pronoun_sieve,
        precise_constructs,
        strict_head_matching_A,
        strict_head_matching_C,
        other_sieve,
        strict_head_matching_B,
        proper_header_word_match_sieve,
        relaxing_head_matching,
    ]
    
    Precision | recall | f1_score
    ------------------------------
    {'bcub': ('44%', '76.57%', '55.89%'),
    'blanc': ('9.29%', '75.81%', '16.56%'),
    'ceafe': ('71.19%', '39.63%', '50.91%'),
    'muc': ('74.24%', '81.64%', '77.76%')}