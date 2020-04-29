
OMFLOW 流程引擎
=================

omflow是混合業務流程和自動化流程的引擎.  
你可以透過所見即所得的方式設計自己的表單,當然同時也可以用所見即所得的方式設計自己的資料流程.  
omflow的流程引擎是使用Python+Django開發,這代表除了方便的流程設計之外,  
也可以輕鬆的串接python程式碼和社群上的應用,達到自動化的效果.他非常適合用來做IT的維運管理和自動化以及企業的ERP和其他應用.  


說明:原始碼預計將於2020/4/30日上傳
  
  
軟體下載
=================

*  開源版下載
   https://github.com/syscomgo/omflow  

*  免費版本(免費版非GPL V3授權)  
   免費版本包含資料收集以及服務管理功能，個人及學術機構與評估用途免費使用  
   包裝好的免費版本可以至 https://www.syscomgo.com/ 下載.  


軟體功能
=================

*  功能：
*  個人儀表板
*  訊息及附件
*  我的任務
*  服務請求
*  應用管理
*  自訂應用
*  人員管理
*  系統設定

軟硬體需求
=================

*  Python3 以上的版本
*  Django 2.2 以上的版本

*  至少需要 1 Core 的 CPU , 1G的RAM , 和至少1GB以上的硬碟空間.

安裝及啟用
===========

下載檔案後,解壓縮到指定的資料夾

<pre><code>
#安裝Django  
pip install django  

#安裝ldap3(非必要)  
pip install ldap3  

#建立omflow專案
django-admin.py startproject omflow  

#將解壓縮的omflow檔案貼到資料夾內,然後啟動omflow  
manage.py runserver  

</code></pre>


Roadmap
=======

*  英文/簡體中文支援
*  雲端下載app

作者
=======

omflow是由`凌群電腦股份有限公司 <https://www.syscom.com.tw>`開發及維護的業務流程和自動化流程的引擎.


License
=======

GNU General Public License v3.0 or later