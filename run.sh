#!/bin/sh

echo "=============== begin ================="

start=$(date +%s)

# 对文本进行预处理, 得到tokens  all: 728s
echo "=============== token ================="
# python token_based_features.py

# 对文本进行预处理, 得到title、url、snippet
# python title_url_snippet.py

# 求每个token的tf-idf  all: 1s
echo "=============== tfidf ================="
# python tfidf_based_feature.py

# 层次聚类（层次聚类算法的主要优点在于无需事先知道最终所需集群数量）
echo "=============== cluster ==============="
# python hierarchy_clustering.py

# 格式转换为评测需要的XML格式
echo "=============== convert ==============="
# python format_conversion.py

# evaluation
echo "=============== evaluation ============"

# 如果文件夹不存在，创建文件夹
if [ ! -d "./outputDir" ]; then
  mkdir ./outputDir
fi

java -cp wepsEvaluation.jar es.nlp.uned.weps.evaluation.SystemScorer ./weps2007_data_1.1/training/truth_files/ ./training/systemsDir/ ./training/outputDir -ALLMEASURES -AllInOne -OneInOne -Combined -average

end=$(date +%s)
time=$(( $end - $start ))
printf "Time: %ds\n" $time


# java -jar wepsScorer.jar ./weps-2-test/data/test/metadata/ ./weps-2-test/data/test/gold_standard/ ./test/systemsDir/ ./test/outputDir/ -ALLMEASURES -AllInOne -OneInOne -Combined

echo "=============== end   ================="
