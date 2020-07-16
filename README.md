
OMFLOW 流程引擎(OMFLOW Workflow Engine)
=================

omflow是混合業務流程和IT自動化流程的引擎.  
`omflow is a form base and IT automation workflow engine.`  
你可以透過所見即所得的方式設計自己的表單,當然同時也可以用所見即所得的方式設計自己的資料流程.  
`you can use WYSIWYG(What You See Is What You Get) design your workflow , include form , automation , and data.`  
omflow的流程引擎是使用Python+Django開發,這代表除了方便的流程設計之外,  
`omflow workflow engine is developed using Python + Django , `  
也可以輕鬆的串接python程式碼和社群上的應用,達到自動化的效果.他非常適合用來做IT的維運管理和自動化以及企業的ERP和其他應用.  
`You can easily integrate your python application in the workflow.`  
 
 documents : https://doc.omflow.com.tw/
 

軟體功能(Functions)
=================

*  個人儀表板 `personal Dashboard`
*  訊息及附件 `message and attachment`
*  我的任務 `my mission`
*  服務請求 `service request`
*  應用管理 `app management`
*  自訂應用 `custom app`
*  人員管理 `user management`
*  系統設定 `system config`


畫面截圖(screenshot)
=================

<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/dashboard.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/flow.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/mission.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/new-field.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/schedule.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/self-service.png">



軟硬體需求(Hardware and Software Requirement)
=================

*  支援Windows以及Linux系統 `support windows and linux system`
*  Python3 以上的版本 `Python 3 or higher `
*  Django 2.2 以上的版本 `Django 2.2 or higher `

使用pip安裝Django: `you can install django using pip`
<pre><code>
pip install django

</code></pre>

*  支援的瀏覽器包含 Firefox , Chrome , Edge , Safari , IE11以上的版本. `support browser:Firefox , Chrome , Edge , Safari , IE11 or higher`
*  至少需要 1 Core 的 CPU , 1G的RAM , 和至少1GB以上的硬碟空間. `1 core cpu and 1g ram , 1g disk space`
*  若您的 Python 為 3.5 或以下版本，Django 請使用2.X版. `if your python is 3.5 or lower , please use django 2.x`

安裝及啟用(Install and Run)
===========

下載檔案後,解壓縮到指定的資料夾,執行下面的指令即可啟動  
`Download the omflow .zip file the unzip , then run server.`  

<pre><code>
python manage.py runserver 0.0.0.0:8000

</code></pre>

或是可以使用 docker 啟動
`or you can start omflow with docker hub image.`  
<pre><code>
docker pull -a omflow/open
docker run -d --name omflow -p 0.0.0.0:80:80 omflow/open

</code></pre>

預設的使用者為 admin/admin  
`default user is admin , password is admin`  

Roadmap
=======

*  多國語支援 `multi-language support`
*  更多的資料操作 - 資料關聯 `form and data relation`
*  更多的表單元件 - 子表單 , 日期時間 `subform and more form field`
*  流程支援取得其他參數 -  篩選新增抓取系統參數/表單資料參數 `more workflow chart`
*  雲端下載app `download app from cloud`

作者(Creator)
=======

omflow是由`凌群電腦股份有限公司 <https://www.syscom.com.tw>`開發及維護的業務流程和自動化流程的引擎.  
`omflow's creator is SYSCOM Computer Engineer co`

軟體授權(License)
=================

*  開源版(GNU General Public License v3.0)
   完整的功能，你可以發佈以及修改原始碼 , 在GPL V3的授權條款下.  
   `You can distribute and modify the source code, provided that you distribute all modifications under the GPLv3 as well.`   
  
