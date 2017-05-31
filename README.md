# flask_api

## 测试

测试分为两种：

1.API接口测试

2.model测试

在命令行下执行：
    
    单独测试api接口：sh scripts/test.sh --api
    单独测试model：sh scripts/test.sh --model
    运行全部测试：sh scripts/test.sh --all

## 国际化

【帮助命令】列出所有支持语言的列表：

    pybabel --list-locales
    
### 首次生成本地化文件

首次生成本地化文件需要执行以下四个步骤：

1.生成翻译文件需要的本地化的字符串的概括文件。

2.生成各个语言的翻译文件。

3.填写各个语言的翻译字符串，这个需要由开发者自己完成。

4.然后编译所有翻译文件。

具体执行步骤如下：

1.在命令行下执行：
    
    sh scripts/translation_new.sh

`translation_new.sh`会执行上面<1, 2>两个步骤。

2.然后你需要填写各个语言的翻译字符串。

3.在命令行下执行：
    
    sh scripts/translation_compile.sh

`translation_compile.sh`会编译所有翻译文件。

### 更新本地化文件

如果之前已经生成过本地化文件并翻译和编译了，就必须更新本地化文件，这需要执行以下四个步骤：


1.重新生成翻译文件需要的本地化的字符串的概括文件。

2.更新各个语言的翻译文件。

3.填写各个语言的翻译字符串，这个需要由开发者自己完成。

4.编译所有翻译文件。

具体执行步骤如下：

1.在命令行下执行：
    
    sh scripts/translation.sh

`translation_new.sh`会执行上面的<1>步骤。

2.然后你需要填写各个语言的翻译字符串。

3.更新各个语言的翻译文件，在命令行下执行：
    
    sh scripts/translation_update.sh
    
4.在命令行下执行：
    
    sh scripts/translation_compile.sh

`translation_compile.sh`会编译所有翻译文件。
    
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
    