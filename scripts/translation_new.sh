# 生成翻译文件需要的本地化的字符串的概括文件
pybabel extract -F babel.cfg -o messages.pot .

# 生成各个语言的翻译文件
pybabel init -i messages.pot -d Baicycle_API/translations -l zh_Hans_CN
pybabel init -i messages.pot -d Baicycle_API/translations -l en_US
pybabel init -i messages.pot -d Baicycle_API/translations -l ja_JP