# flask_api

## 国际化

【帮助命令】列出所有支持语言的列表：

    pybabel --list-locales
    
### 首次生成本地化文件

1.生成翻译文件需要的本地化的字符串的概括文件：

    pybabel extract -F babel.cfg -o messages.pot .

2.生成各个语言的翻译文件：

    pybabel init -i messages.pot -d translations -l zh_Hans_CN
    pybabel init -i messages.pot -d translations -l en_US
    pybabel init -i messages.pot -d translations -l ja_JP

3.填写各个语言的翻译字符串

4.编译所有翻译文件：

    pybabel compile -d translations

### 更新本地化文件

1.重新生成翻译文件需要的本地化的字符串的概括文件：

    pybabel extract -F babel.cfg -o messages.pot .
    
2.更新各个语言的翻译文件：
    
    pybabel update -i messages.pot -d flask_api/translations
    
3.填写各个语言的翻译字符串

4.编译所有翻译文件：

    pybabel compile -d flask_api/translations
    
## 数据库迁移

### 首次运行：

    python migrate.py db init

运行这个命令后会在项目目录中添加 `migrations` 目录。

创建第一个版本：
    
    python migrate.py db migrate -m "initial migration"
      
运行迁移：

    python migrate.py db upgrade

### 后续迁移：

更新models目录下的文件
    
运行：

    python migrate.py db migrate -m "migrate message"
    python migrate.py db upgrade