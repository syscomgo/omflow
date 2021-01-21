<a href="https://github.com/syscomgo/omflow/blob/master/README.md">English</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/syscomgo/omflow/blob/master/README_TW.md">中文</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/syscomgo/omflow/blob/master/README_JP.md">日本語</a>

This is a machine translation page

OMFLOW Workflow Engine
=================
omflow is a form base and IT automation workflow engine.
you can use WYSIWYG(What You See Is What You Get) design your workflow , user form , do automation things , and process data.
omflow workflow engine is developed using Python and Django ,    
so , You can easily integrate your python application in the workflow.

documents website : https://doc.omflow.com.tw/v/english/
 

Software Functions
=================

*  personal Dashboard
*  message and attachment
*  my mission
*  service request
*  app management
*  user management
*  system config


screenshot
=================

<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/dashboard.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/flow.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/mission.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/new-field.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/schedule.png">
<img width="594" src="https://raw.githubusercontent.com/syscomgo/omlib/master/screenshot/self-service.png">



Hardware and Software Requirement
=================

*  support windows and linux system
*  Python 3 or higher 
*  Django < 3


<pre><code>
you can install conda invironment as
conda create -n omflow python==3.7

in windows
source activate omflow

in linux
conda activate omflow
</code></pre>

*  support browser:Firefox , Chrome , Edge , Safari , IE11 or higher
*  1 core cpu and 1g ram , 1g disk space
*  if your python is 3.5 or lower , please use django 2.x
*  if your python is 3.7 or lower , please use django 3.x

Install and Run
===========

Download the omflow .zip file the unzip , then run server.

change "settings - Copy.py" in workflow to settings.py (becuase its special for every developer for its passowrd sites)

install package by 
pip install -r requirements.txt

<pre><code>
python manage.py runserver

</code></pre>

or you can start omflow with docker hub image.
<pre><code>
docker pull omflow/open
docker run -d --name omflow -p 0.0.0.0:80:80 omflow/open

</code></pre>

default user is admin , password is admin 
if not work you can create you admeb by

python manage.py createsuperuser

Roadmap
=======

*  Report
*  Form front-end change actions
*  workflow's Python Point assign a collector 
*  Event API
*  data sub relations
*  web automation support(selenium)
*  menu control by level herarcy

Creator
=======
 
omflow's creator is SYSCOM Computer Engineer co

License
=================

*  GNU General Public License v3.0
*  You can distribute and modify the source code, provided that you distribute all modifications under the GPLv3 as well.
  

   
