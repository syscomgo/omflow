<a href="https://github.com/syscomgo/omflow/blob/master/README.md">English</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/syscomgo/omflow/blob/master/README_TW.md">中文</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/syscomgo/omflow/blob/master/README_JP.md">日本語</a>

OMFLOW 流程引擎
=================

omflow是混合業務流程和IT自動化流程的引擎.  
你可以透過所見即所得的方式設計自己的表單,當然同時也可以用所見即所得的方式設計自己的資料流程.  
omflow的流程引擎是使用Python+Django開發,這代表除了方便的流程設計之外,    
也可以輕鬆的串接python程式碼和社群上的應用,達到自動化的效果.他非常適合用來做IT的維運管理和自動化以及企業的ERP和其他應用.  
 
documents : https://doc.omflow.com.tw/
 

軟體功能
=================

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

*  支援Windows以及Linux系統 
*  Python3 以上的版本
*  Django 2.X 的版本

使用pip安裝Django:
<pre><code>
pip install django

</code></pre>

*  支援的瀏覽器包含 Firefox , Chrome , Edge , Safari , IE11以上的版本.
*  至少需要 1 Core 的 CPU , 1G的RAM , 和至少1GB以上的硬碟空間. 
*  若您的 Python 為 3.5 或以下版本，Django 請使用2.X版. 

安裝及啟用
===========

下載檔案後,解壓縮到指定的資料夾,執行下面的指令即可啟動  

<pre><code>
python manage.py runserver 0.0.0.0:8000

</code></pre>

或是可以使用 docker 啟動

<pre><code>
docker pull omflow/open
docker run -d --name omflow -p 0.0.0.0:80:80 omflow/open

</code></pre>

預設的使用者為 admin/admin  

Roadmap
=======

*  報表功能
*  前端表單元件互動
*  流程設計可以選擇Python要在哪個收集器執行
*  事件管理的API
*  子母單關聯功能
*  網頁自動化支援(selenium)

作者
=======

omflow是由`凌群電腦股份有限公司 <https://www.syscom.com.tw>`開發及維護的業務流程和自動化流程的引擎.  

軟體授權(License)
=================

*  開源版(GNU General Public License v3.0)
   完整的功能，你可以發佈以及修改原始碼 , 在GPL V3的授權條款下.  
