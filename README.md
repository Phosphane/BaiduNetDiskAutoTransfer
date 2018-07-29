# BaiduNetDiskAutoTransfer
百度云网盘批量转存工具 </br>
运行环境：Python2.7 </br>
  Python Selenium </br>
  Selenium Chrome Driver</br>
  
# 更新日志
2018-07-29 Ver1.0 Stable</br>
1.重构所有代码，构建为库文件的形式，支持import</br>
2.链接导入方式为使用SQLite3数据库，支持多种情况的报错以及日志记录</br>
3.优化部分等待算法，提高转存效率</br>
4.使用配置文件配置Xpath,ClassName,ID等搜索依据，方便修改以应对百度云日常的变化</br>

# Usage
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


