# wiki_cleaner
对wikidump数据进行数据清洗，wikidump数据地址https://dumps.wikimedia.org/zh_yuewiki/。


首先下载数据到本地，执行如下命令即可对wiki数据进行清洗。代码主要参考了苏神的wiki抽取逻辑[1]。初步抽取后进一步对数据进行清洗，去掉特殊符号的等。

```shell
python wiki_clean.py \
    --input_file xxx-wiki.xml.bz2 \
    --output_file xxx-wiki.txt \
    --need_clean True \
    --cleaned_file xxx-wiki.cleaned.txt
```

### 参考
[1] https://kexue.fm/archives/4176

