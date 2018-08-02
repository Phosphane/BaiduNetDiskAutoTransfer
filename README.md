# BaiduNetDiskAutoTransfer
百度云网盘批量转存工具 </br>
运行环境：Python3.7 </br>
  Python Selenium </br>
  Selenium Chrome Driver</br>
  
# 更新日志
2018-08-02 GUI Ver 0.0.1 Alpha</br>
           Console Ver 1.1.0 Beta</br>
1.新增图形界面</br>
2.修改程序以适应图形界面需求</br>

2018-07-30 Ver1.0.1 Stable</br>
1.修复部分Bug</br>
2.增加命令行帮助信息

2018-07-29 Ver1.0 Stable</br>
1.重构所有代码，构建为库文件的形式，支持import</br>
2.链接导入方式为使用SQLite3数据库，支持多种情况的报错以及日志记录</br>
3.优化部分等待算法，提高转存效率</br>
4.使用配置文件配置Xpath,ClassName,ID等搜索依据，方便修改以应对百度云日常的变化</br>

# Usage
修改代码中main函数的数据库为你自己的数据库文件</br>
运行程序，在浏览器界面中登陆百度云盘，切换到回收站并保证页面已加载完成，防止卡死（原因未知）</br>
然后在命令行界面中按下回车，程序将开始从数据库中读取数据并自动转存</br>

# 命令行参数
-h,--help : 显示帮助信息</br>
-e,--errorCheck : 重新检查错误链接（非被禁链接）</br>
-d,--databse : 数据库路径


# 相关参数解释
数据库格式：</br>
Name Text类型，名字</br>
PanLink Text类型，百度云盘链接</br>
PanPwd Text类型，百度云盘提取码</br>
isTransfered Int类型，状态码</br>

状态码：</br>
0表示未转存，1表示正常转存，-1表示链接错误，-2表示链接资源已被禁止分享

配置文件配置项解释：</br>
destnationPath:</br>目标文件夹，必须在百度云盘中创建，否则将会无法找到对应的文件夹而转存失败</br>
codeTextBoxXPath:</br>使用XPath定位提取码输入框，如何获取XPath请参考Chrome的开发人员工具</br>
codeEnterBtnXPath:</br>使用XPath定位提取码确认按钮</br>
transferBtnClassName:</br>使用Class名来定位转存按钮，处于Debug阶段，暂时无用</br>
transferBtnSelector:</br>使用CSS Selector定位转存按钮，当前版本为定位转存按钮的主要方法</br>
checkBoxClassName:</br>使用Class名定位复选框，用于多文件同时转存或者文件夹的转存</br>
fileTreeNodeClassName:</br>使用Class名定位保存路径的节点对象，一般无需修改</br>
fileTreeDialogXPath:</br>使用XPath定位保存路径选择窗口</br>
fileTreeConfirmBtnClassName:</br>使用Class名定位路径选择确认按钮</br>
notFoundID:</br>使用ID定位链接失效的提示，用于判断链接是否失效</br>


# 图形界面新增内容
1.支持自选数据库，方便自选



