#!/bin/sh

echo "=============== begin ================="

start=$(date +%s)

# 对文本进行预处理, 得到tokens  all: 728s
echo "=============== token ================="
python token_based_features.py

# 求每个token的tf-idf  all: 1s
echo "=============== tfidf ================="
python tfidf_based_feature.py

# 层次聚类（层次聚类算法的主要优点在于无需事先知道最终所需集群数量）
echo "=============== cluster ==============="
python hierarchy_clustering.py

# 格式转换为评测需要的XML格式
echo "=============== convert ==============="
python format_conversion.py

# evaluation
# java -cp wepsEvaluation.jar es.nlp.uned.weps.evaluation.SystemScorer ./keysDir/ ./systemsDir/ ./outputDir -ALLMEASURES -AllInOne -OneInOne -Combined -average

end=$(date +%s)
time=$(( $end - $start ))
echo $time

echo "=============== end   ================="
