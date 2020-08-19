<a href="https://github.com/syscomgo/omflow/blob/master/README.md">English</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/syscomgo/omflow/blob/master/README_TW.md">中文</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/syscomgo/omflow/blob/master/README_JP.md">日本語</a>

これは機械翻訳のページです

OMFLOWプロセスエンジン
=================

omflowは、ビジネスプロセスとIT自動化プロセスを組み合わせたエンジンです。
独自のフォームをWYSIWYGの方法で設計できます。もちろん、独自のデータフローをWYSIWYGの方法で設計することもできます。
omflowのプロセスエンジンはPython + Djangoを使用して開発されています。つまり、便利なプロセス設計に加えて、
また、Pythonコードとコミュニティアプリケーションを簡単に接続して自動化を実現できるため、ITメンテナンスの管理と自動化だけでなく、エンタープライズERPやその他のアプリケーションにも非常に適しています。
 
documents : https://doc.omflow.com.tw/
 

ソフトウェア機能
=================

*パーソナルダッシュボード
*メッセージと添付ファイル
*私の仕事
*サービスのリクエスト
*アプリケーション管理
*カスタムアプリケーション
* 人事管理
*  システム設定


ソフトウェアおよびハードウェア要件
=================

* WindowsおよびLinuxシステムをサポート
* Python3以降
* Django 2.Xバージョン

pipを使用してDjangoをインストールします。
<pre> <code>
pip install django

</code></pre>

*サポートされるブラウザーには、Firefox、Chrome、Edge、Safari、IE11以上が含まれます。
*少なくとも1コアCPU、1G RAM、および1GB以上のハードディスク容量が必要です。
* Pythonのバージョンが3.5以下の場合、Djangoにはバージョン2.Xを使用してください。

インストールとアクティベーション
===========

ファイルをダウンロードしたら、指定したフォルダに解凍し、次のコマンドを実行して開始します

<pre><code>
python manage.py runserver 0.0.0.0:8000

</code></pre>

またはあなたが使うことができます docker 起動

<pre><code>
docker pull omflow/open
docker run -d --name omflow -p 0.0.0.0:80:80 omflow/open

</code></pre>

デフォルトのユーザーは admin/admin  

Roadmap
=======

*より多くのデータ操作とデータの関連付け
*その他のフォームコンポーネント-サブフォーム、日付と時刻
*他のパラメーターフィルターを取得し、新しいクロールシステムパラメーター/フォームデータパラメーターを追加するためのプロセスサポート

著者
=======

omflowは、 `SYSCOM Computer Co.、Ltd. <https://www.syscom.com.tw>`によって開発および保守されているビジネスプロセスおよび自動化プロセスのエンジンです。 

軟體授權(License)
=================

*オープンソースバージョン（GNU General Public License v3.0）
    完全な機能、GPL V3のライセンス条項に基づいて、ソースコードを公開および変更できます。
