/**
 * SYSCOM OMFLOW FLOW ENGINE
 * for Workflow diagram design ui 
 * 2019/11/6 beta
 * author:Pen Lin
 * ------------------
 */
var omfloweng = function(div_id)
{
	//====================
	//===public variable==
	//====================
	var _self_ = this;
	
	//====================
	//===private variable==
	//====================
	var active_id = div_id;
	var name ='';
	var description='';
	var uid = 0;
	var flowobject = null;
	var flowcontent = $('#' + div_id);
	var formobject_for_modal = null; //form_object (javascript)
	var action_item_for_modal = null;
	var selected_source_chart_item = null;
	var selected_target_chart_item = null;
	var selected_ball = '';
	var event_chart_selected_callback = null;
	
	var event_get_group_list_callback = null;
	var event_get_user_list_callback = null;
	
	var event_get_app_list_callback = null;
	var event_get_flow_list_callback = null;
	var event_get_flowIO_list_callback = null;
	
	var event_get_my_flow_list_callback = null;
	var event_get_my_flowIO_list_callback = null;

	var design_mode = false;
	var policy_mode = false;
	var myCodeMirror = null;
	var box_ball_content = '<div id="' + active_id + '_ball_left" style="z-index:1000;width: 10px;height: 10px;background-color: #fff;border: 1px solid #777;border-radius: 5px;margin: 0px auto 0;position: absolute;top:0px;left:0px;display:none" ></div>'
		+ '<div id="' + active_id + '_ball_right" style="z-index:1000;width: 10px;height: 10px;background-color: #fff;border: 1px solid #777;border-radius: 5px;margin: 0px auto 0;position: absolute;top:0px;left:0px;display:none" ></div>'
		+ '<div id="' + active_id + '_ball_bottom" style="z-index:1000;width: 10px;height: 10px;background-color: #fff;border: 1px solid #777;border-radius: 5px;margin: 0px auto 0;position: absolute;top:0px;left:0px;display:none" ></div>'
		+ '<div id="' + active_id + '_tball_left" style="z-index:1000;width: 10px;height: 10px;background-color: #fff;border: 1px solid #777;border-radius: 5px;margin: 0px auto 0;position: absolute;top:0px;left:0px;display:none" ></div>'
		+ '<div id="' + active_id + '_tball_right" style="z-index:1000;width: 10px;height: 10px;background-color: #fff;border: 1px solid #777;border-radius: 5px;margin: 0px auto 0;position: absolute;top:0px;left:0px;display:none" ></div>'
		+ '<div id="' + active_id + '_tball_top" style="z-index:1000;width: 10px;height: 10px;background-color: #fff;border: 1px solid #777;border-radius: 5px;margin: 0px auto 0;position: absolute;top:0px;left:0px;display:none" ></div>';
	
	//_pid_:
	//_top_:
	//_left_:
	//_type_:
	//_button_:
	//_des_:
	//_style_:
	//_iconarea_:
	var item_content = '<div id="' + active_id + '__pid_' + '" style="position: absolute;top:' + '_top_' + 'px;left:' + '_left_' + 'px;width:120px;z-index:999;">'
		+'<div style="width: 120px;height: 20px;"><div id="' + active_id + '_display_' + '_pid_' + '" style="display:none">' + '_button_' + '</div></div>'
		+'<div id="' + active_id + '_chart_' + '_pid_' + '" style="position: absolute;top:22px;_style_"></div>'
		+'<div style="position: absolute;_iconoffset_"><i class="_icon_" style="color:#_iconcolor_;font-size: _iconsize_px"></i></div>'
		+'<div style="position: absolute;top:22px;" id="' + active_id + '_itext_' + '_pid_' + '"><table><tr ><td width="120" height="60" align="right" valign="bottom" ><span style="color:#00008B;" id="' + active_id + '_itext_content_' + '_pid_' + '">' + '_des_' + '</span></td></tr></table></div>'
		+'</div>';

	var line_content = '<div id="' + active_id + '_FLINE__pid_" style="width: _width_px;height: _height_px;position: absolute ;border-_direction_: 2px solid;border-color:#777;top:_top_px;left:_left_px;z-index:990" ></div>';
	var arrow_content = '<div id="' + active_id + '_FLINE__pid_" style="position: absolute ;top:_top_px;left:_left_px;border: solid #777;border-width: 0 2px 2px 0;display: inline-block;padding: 4px;transform: rotate(_direction_deg);-webkit-transform: rotate(_direction_deg);z-index:990"></div>';
	
	var item_content_button_remove = '<button id="' + active_id + '_item_remove__pid_" class="btn btn-box-tool pull-right"><i class="fa fa-remove"></i></button>';
	var item_content_button_config = '<button id="' + active_id + '_item_config__pid_" class="btn btn-box-tool pull-left"><i class="fa fa-gear"></i></button>';
	var item_content_button_copy = '<button id="' + active_id + '_item_copy__pid_" class="btn btn-box-tool pull-left"><i class="fa fa-copy"></i></button>';
	
	var item_content_style_start = 'left:0px;width: 120px;height: 60px;background-color: #FD4F32;border-radius: 30px;margin: 0px auto 0;';
	var item_content_style_end = 'left:0px;width: 120px;height: 60px;background-color: #FD4F32;border-radius: 30px;margin: 0px auto 0;';
	var item_content_style_process = 'left:0px;width: 120px;height: 60px;background-color: #89B4A3;border-radius: 5px;margin: 0px auto 0;';
	var item_content_style_process_small = 'width: 60px;height: 30px;background-color: #89B4A3;border-radius: 5px;margin: 0px auto 0;';
	var item_content_style_select = 'left:30px;width: 60px;height: 60px;background-color: #fce4a8;margin: 0px auto 0;transform: rotate(45deg) skew(-18deg,-18deg);';
	var item_content_style_select_small = 'width: 30px;height: 30px;background-color: #fce4a8;margin: 0px auto 0;transform: rotate(45deg) skew(-18deg,-18deg);';
	var item_content_style_form = 'left:0px;width: 110px;height: 60px;background-color: #89B4A3;margin: 0px auto 0;transform:skewX(-15deg);';
	var item_content_style_form_small = 'width: 55px;height: 30px;background-color: #89B4A3;margin: 0px auto 0;transform:skewX(-15deg);';
	var item_content_style_outflow = 'left:0px;width: 120px;height: 60px;background-color: #5E656D;border-radius: 30px;margin: 0px auto 0;';
	var item_content_style_outflow_small = 'width: 60px;height: 30px;background-color: #909090;border-radius: 15px;margin: 0px auto 0;';
	var item_content_style_async = 'left:30px;width: 60px;height: 60px;background-color: #dc8239;margin: 0px auto 0;transform: rotate(45deg) skew(-18deg,-18deg);';
	var item_content_style_async_small = 'width: 30px;height: 30px;background-color: #dc8239;margin: 0px auto 0;transform: rotate(45deg) skew(-18deg,-18deg);';
	var item_content_style_collection = 'left:0px;width: 120px;height: 60px;background-color: #dc8239;border-radius: 30px;margin: 0px auto 0;';
	var item_content_style_collection_small = 'width: 60px;height: 30px;background-color: #dc8239;border-radius: 15px;margin: 0px auto 0;';
	
	//====================
	//===MODAL NAME ID==
	//====================
	var baseID_NEW = active_id + '_' + 'add_chart_modal';
	var baseID_START = active_id + '_' + 'start_chart_modal';
	var baseID_END = active_id + '_' + 'end_chart_modal';
	var baseID_PYTHON = active_id + '_' + 'python_chart_modal';
	var baseID_SUBFLOW = active_id + '_' + 'subflow_chart_modal';
	var baseID_SWITCH = active_id + '_' + 'switch_chart_modal';
	var baseID_FORM = active_id + '_' + 'form_chart_modal';
	var baseID_SLEEP = active_id + '_' + 'sleep_chart_modal';
	var baseID_ASYNC = active_id + '_' + 'async_chart_modal';
	var baseID_COLLECTION = active_id + '_' + 'collection_chart_modal';
	var baseID_OUTFLOW = active_id + '_' + 'outflow_chart_modal';
	var baseID_INFLOW = active_id + '_' + 'inflow_chart_modal';
	var baseID_SETFORM = active_id + '_' + 'setform_chart_modal';
	
	var baseID_ORG1 = active_id + '_' + 'org1_chart_modal';
	var baseID_ORG2 = active_id + '_' + 'org2_chart_modal';
	
	//====================
	//===public method====
	//====================
	/**
	 * initialization  omfloweng for new subflow
	 * input: mode design_mode = true  , ready only is false)
	 * return: 
	 * author:Pen Lin
	 */
	_self_.init_subflow = function(mode)
	{
		
		_self_.init(mode);
		flowobject.is_sub = true;
	}
	_self_.setPolicyMode = function()
	{
		policy_mode = true;
	}
	/**
	 * initialization  omfloweng for new flow
	 * input: mode design_mode = true  , ready only is false)
	 * return: 
	 * author:Pen Lin
	 */
	_self_.init = function(mode)
	{
		design_mode = mode;
		uid = Date.now();
		flowobject = flow_object();
		flowobject.uid = uid;
		flowcontent.css('overflow','scroll');
		flowcontent.css('position','relative');
		//flowcontent.css('background','blue');
		if ($('#' + active_id + '_ball_left').length == 0)
		{
			flowcontent.append(box_ball_content);
			
			$('[id^="' + active_id + '_ball_"]').mousedown(function(){
				ball_mousedown(this.id);
			});
			$('[id^="' + active_id + '_tball_"]').mousedown(function(){
				tball_mousedown(this.id);
			});
		}
		//====================
		//===MODAL CHART NEW FLOW 
		//====================
		var add_chart_modal_id = 'add_chart_modal';
		if ($('#' + baseID_NEW).length == 0)
		{
			//====================
			//===MODAL NEW CHART CHART 
			//====================
			var modal_add_item = '<div class="modal fade" id="' + baseID_NEW + '">'
                           +'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
                           +' <div class="modal-content">'
                           +'  <div class="modal-header">'
                           +'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
                           +'   <h4 class="modal-title"> ' + gettext('新增元件') + '</h4>'
                           +'  </div>'
                           +'  <div class="modal-body">'
                           +'   <div class="nav-tabs-custom">'
                           +'    <ul class="nav nav-tabs">'
                           +'     <li class="active"><a href="#' + baseID_NEW + '_exec" data-toggle="tab">' + gettext('執行') + '</a></li>'
                           +'     <li><a href="#' + baseID_NEW + '_rule" data-toggle="tab">' + gettext('路線') + '</a></li>'
                        +'     <li><a href="#' + baseID_NEW + '_rolemap" data-toggle="tab">' + gettext('組織圖') + '</a></li>'
                           +'    </ul>'
                           
                           +'    <div class="tab-content">'

                           +'     <div class="tab-pane active" id="' + baseID_NEW + '_exec">'

                           +'      <div class="table-responsive" style="z-index:1001">'
                           +'      <table class="table no-margin">'
                           +'      <thead><tr><th>' + gettext('元件') + '</th><th>' + gettext('說明') + '</th></tr></thead>'
                           +'      <tbody>'
                           //+'      <tr>'
                           //+'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_start" class="iradio_minimal-blue" value="start"><label for="' + baseID_NEW + '_start"></label><b>  <i class="fa fa-play-circle"></i>  ' + gettext('開始(測試用)') + '</b></td>'
                           //+'      <td>'+gettext('流程開始執行的起始元件，可以定義輸入參數以及預先執行子流程處理資料。')+'</td>'
                           //+'      </tr>'
                           //+'      <tr>'
                           //+'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_end" class="iradio_minimal-blue" value="end"><label for="' + baseID_NEW + '_end"></label><b>  <i class="fas fa-flag-checkered"></i>  '+gettext('結束(測試用)')+'</b></td>'
                           //+'      <td>'+gettext('流程結束的終止元件，進入結束後的資料代表生命週期已結束。')+'</td>'
                           //+'      </tr>'  
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_form" class="iradio_minimal-blue" value="form"><label for="' + baseID_NEW + '_form"></label><b>  <i class="fa fa-pencil-square-o"></i> '+gettext('人工輸入')+'</b></td>'
                           +'      <td>' + gettext('使用者填寫表單。') + ' </td>'
                           +'      </tr>'    
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_setform" class="iradio_minimal-blue" value="setform"><label for="' + baseID_NEW + '_setform"></label><b>  <i class="fas fa-database"></i> '+gettext('欄位設定')+'</b></td>'
                            +'      <td>'+gettext('直接設定表單欄位的值。')+'</td>'
                           +'      </tr>'    
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_inflow" class="iradio_minimal-blue" value="inflow"><label for="' + baseID_NEW + '_inflow"></label><b>  <i class="fas fa-share"></i>  '+gettext('呼叫流程')+'</b></td>'
                           +'      <td>'+gettext('呼叫此應用的其他流程。')+'</td>'
                           +'      </tr>'                           
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_subflow" class="iradio_minimal-blue" value="subflow" checked><label for="' + baseID_NEW + '_subflow"></label><b>  <i class="fa fa-play-circle-o"></i>  '+gettext('子流程')+'</b></td>'
                           +'      <td>'+gettext('呼叫自身的子流程。')+'</td>'
                           +'      </tr>'    
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_python" class="iradio_minimal-blue" value="python"><label for="' + baseID_NEW + '_python"></label><b>  <i class="fab fa-python"></i>  '+gettext('程式碼')+'</b></td>'
                           +'      <td>'+gettext('執行自定義的Python程式碼。')+'</td>'
                           +'      </tr>'
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_outflow" class="iradio_minimal-blue" value="outflow"><label for="' + baseID_NEW + '_outflow"></label><b>  <i class="far fa-share-square"></i>  '+gettext('外部流程')+'</b></td>'
                           +'      <td>'+gettext('呼叫系統中已上架的流程。')+'</td>'
                           +'      </tr>'
                           +'      </tbody>'
                           +'      </table></div>'
                           +'     </div>'
                           
                           +'     <div class="tab-pane" id="' + baseID_NEW + '_rule">'
                           +'      <div class="table-responsive" style="z-index:1001">'
                           +'      <table class="table no-margin">'
                           +'      <thead><tr><th>'+gettext('元件')+'</th><th>'+gettext('說明')+'</th></tr></thead>'
                           +'      <tbody>'
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_switch" class="iradio_minimal-blue" value="switch"><label for="' + baseID_NEW + '_switch"></label><b>  <i class="fa fa-map-signs"></i>  '+gettext('條件判斷')+'</b></td>'
                           +'      <td>'+gettext('依據規則判斷，將流程導往指定的一條路線。')+'</td>'
                           +'      </tr>'
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_async" class="iradio_minimal-blue" value="async"><label for="' + baseID_NEW + '_async"></label><b>  <i class="fas fa-people-arrows"></i>  '+gettext('並行')+'</b></td>'
                           +'      <td>'+gettext('流程會同時往所有的路線前進，並在並行匯集的時候回歸到單一路線。')+'</td>'
                           +'      </tr>'    
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_collection" class="iradio_minimal-blue" value="collection"><label for="' + baseID_NEW + '_collection"></label><b>  <i class="fas fa-compress-arrows-alt"></i>  '+gettext('並行匯集')+'</b></td>'
                           +'      <td>'+gettext('所有指向自己的路線都抵達時，流程會繼續前進。')+'</td>'
                           +'      </tr>'                           
                           +'      <tr>'
                           +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_sleep" class="iradio_minimal-blue" value="sleep"><label for="' + baseID_NEW + '_sleep"></label><b>  <i class="far fa-clock"></i>  '+gettext('暫停')+'</b></td>'
                           +'      <td>'+gettext('流程執行到暫停時，會暫時停止指定的毫秒後才繼續往前。')+'</td>'
                           +'      </tr>'    
                           +'      </tbody>'
                           +'      </table></div>'
                           +'     </div>'
                           
                        +'     <div class="tab-pane" id="' + baseID_NEW + '_rolemap">'
                        +'      <div class="table-responsive" style="z-index:1001">'
                        +'      <table class="table no-margin">'
                        +'      <thead><tr><th>'+gettext('元件')+'</th><th>'+gettext('說明')+'</th></tr></thead>'
                        +'      <tbody>'
                        +'      <tr>'
                        +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_org1" class="iradio_minimal-blue" value="org1"><label for="' + baseID_NEW + '_org1"></label><b>  <i class="fas fa-user-tie"></i>  '+gettext('同系職務')+'</b></td>'
                        +'      <td>'+gettext('取得在組織圖上，指定使用者同組織最先碰到的職務使用者。')+'</td>'
                        +'      </tr>'
                        +'      <tr>'
                        +'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_org2" class="iradio_minimal-blue" value="org2"><label for="' + baseID_NEW + '_org2"></label><b>  <i class="fas fa-user-tag"></i>  '+gettext('部門職務')+'</b></td>'
                        +'      <td>'+gettext('搜尋組織圖上，指定部門以下的第一個職務。')+'</td>'
                        +'      </tr>'
                        +'      </tbody>'
                        +'      </table></div>'
                        +'     </div>'
            
                           +'    </div>'
                           
                           +'   </div>'
                           +'  </div>'
                           +'  <div class="modal-footer">'
                           +'   <button type="button" class="btn btn-default pull-left" id="' + baseID_NEW + '_close">'+gettext('取消')+'</button>'
                           +'   <button type="button" class="btn btn-primary"  id="' + baseID_NEW + '_submit" >'+gettext('確定')+'</button>'
                           +'  </div>'
                           +' </div>'
                           +'</div>'
                           +'</div>';

			flowcontent.append(modal_add_item);
			//====================
			//===MODAL INIT
			//====================


			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_NEW + '_submit').click(function ()
			{
				_self_.add_item($('input[name="' + baseID_NEW + '_options"]:checked').val(),'public');
				$('#' + baseID_NEW).modal('hide');
			});
			$('#' +  baseID_NEW + '_close').click(function ()
			{
				$('#' + baseID_NEW).modal('hide');
			});
			
		}
		//====================
		//===MODAL CHART START 
		//====================
		if ($('#' + baseID_START).length == 0)
		{
			var modal_START = '<div class="modal fade" id="' + baseID_START + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('開始-')+'<span id="' + baseID_START + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_START + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_START + '_input" data-toggle="tab">'+gettext('輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_START + '_subflow" data-toggle="tab">'+gettext('驗證')+'</a></li>'
						+'     <li><a href="#' + baseID_START + '_subflow_input" data-toggle="tab">'+gettext('驗證輸入')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_START + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_START + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_START + '_config_callable" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_START + '_config_callable"></label>'
						+'       <label> '+gettext('允許外部呼叫')+'</label>'
						+'      </div>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_START + '_input">'
						+'      <button id="' + baseID_START + '_input_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_START + '_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_START + '_subflow">'
						+'      <ul id="' + baseID_START + '_subflow_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_START + '_subflow_input">'
						+'      <ul id="' + baseID_START + '_subflow_content_input" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_START + '_subflow_output">' //保留
						+'      <ul id="' + baseID_START + '_subflow_content_output" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_START + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_START + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_START);
			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_START + '_input_content' ).sortable();
			$( '#' + baseID_START + '_input_content' ).disableSelection();

			
			$('#' + baseID_START + '_input_content_add').click(function () 
			{
				chart_input_sortable_add( baseID_START + '_input_content' , true , false);
			});
			
			//when _subflow_input click , input to output
			$('a[href="#' + baseID_START + '_subflow_input"]').on('shown.bs.tab', function (e) 
			{
				//input content name only string
				$('[id^="' + baseID_START + '_input_content' +'_name_"]').each(function()
				{
					var option_name = $(this).val();
					if(option_name != '')
					{
						$('[id^="' + baseID_START + '_subflow_content_input' + '_value_"]').each(function(i)
						{
							if($(this).html().indexOf('$(' + option_name + ')') > 0)
							{
								//已存在
							}
							else
							{
								select2_new_option(baseID_START + '_subflow_content_input' + '_value_' + i,'$(' + option_name + ')',gettext('變數:') + option_name );
							}
						});
					}
				});
			});


			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_START + '_submit').click(function ()
			{
				item = action_item_for_modal;

				//save real to object
				item.text = $('#' + baseID_START + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);		
				item.config.callable = $('#' + baseID_START + '_config_callable').prop("checked");
				
				modal_save_input(baseID_START , item);
				modal_save_subflow(baseID_START , item);

				$('#' + baseID_START).modal('hide');
			});
			$('#' +  baseID_START + '_close').click(function ()
			{
				$('#' + baseID_START).modal('hide');
			});
		}
		//====================
		//===MODAL CHART END 
		//====================
		if ($('#' + baseID_END).length == 0)
		{
			var modal_END = '<div class="modal fade" id="' + baseID_END + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('結束-')+'<span id="' + baseID_END + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_END + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_END + '_calculate" data-toggle="tab">'+gettext('篩選')+'</a></li>'
						+'     <li><a href="#' + baseID_END + '_output" data-toggle="tab">'+gettext('輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' + baseID_END + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label >'+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_END + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_END + '_calculate">'
						+'      <button id="' + baseID_END + '_calculate_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_END +  '_calculate_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_END + '_output">'
						+'      <button id="' + baseID_END + '_output_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_END + '_output_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_END + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_END + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_END);
			
			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_END + '_output_content' ).sortable();
			$( '#' + baseID_END + '_output_content' ).disableSelection();
			$( '#' + baseID_END +  '_calculate_content' ).sortable();
			$( '#' + baseID_END +  '_calculate_content' ).disableSelection();
			
			$('#' + baseID_END + '_output_content_add').click(function () 
			{
				chart_output_sortable_add( baseID_END + '_output_content',true,true);
				//caculate to only variable
				$('[id^="' + baseID_END + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_END + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_END + '_output_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_END + '_output_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_END + '_output_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
				
			});
			$('#'+ baseID_END + '_calculate_content_add').click(function () 
			{
				chart_calculate_sortable_add(baseID_END +  '_calculate_content'); 
			});
			
			//when output tab show
			$('a[href="#' + baseID_END + '_output"]').on('shown.bs.tab', function (e) 
			{
				//caculate to only variable
				$('[id^="' + baseID_END + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_END + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_END + '_output_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_END + '_output_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_END + '_output_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_END + '_submit').click(function ()
			{
				item = action_item_for_modal;

				//save real to object
				item.text = $('#' + baseID_END + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);
				
				modal_save_output(baseID_END , item);
				modal_save_calculate(baseID_END , item);

				$('#' + baseID_END).modal('hide');
			});
			$('#' +  baseID_END + '_close').click(function ()
			{
				$('#' + baseID_END).modal('hide');
			});
			
		}
		//====================
		//===MODAL CHART PYTHON 
		//====================
		if ($('#' + baseID_PYTHON).length == 0)
		{
			var modal_PYTHON = '<div class="modal fade" id="' + baseID_PYTHON + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('程式碼-')+'<span id="' + baseID_PYTHON + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_PYTHON + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li ><a href="#' +baseID_PYTHON + '_calculate" data-toggle="tab">'+gettext('篩選')+'</a></li>'
						+'     <li><a href="#' + baseID_PYTHON + '_input" data-toggle="tab">'+gettext('輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_PYTHON + '_python" data-toggle="tab">Python</a></li>'
						+'     <li><a href="#' + baseID_PYTHON + '_output" data-toggle="tab">'+gettext('輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_PYTHON + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label >'+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_PYTHON + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_PYTHON + '_config_autoinstall" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_PYTHON + '_config_autoinstall"></label>'
						+'       <label> '+gettext('自動安裝缺少的套件')+'</label>'
						+'      </div>'						
						+'      <div class="form-group">'
						+'       <input id="' + baseID_PYTHON + '_config_error_pass" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_PYTHON + '_config_error_pass"></label>'
						+'       <label> '+gettext('異常時通過/標示異常')+'</label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_PYTHON + '_config_load_balance" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_PYTHON + '_config_load_balance"></label>'
						+'       <label> '+gettext('分散運算')+'</label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_PYTHON + '_config_callable" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_PYTHON + '_config_callable"></label>'
						+'       <label> '+gettext('允許外部呼叫')+'</label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_PYTHON + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_PYTHON + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'						
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_PYTHON + '_calculate">'
						+'      <button id="' + baseID_PYTHON + '_calculate_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_PYTHON +  '_calculate_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_PYTHON + '_input">'
						+'      <button id="' + baseID_PYTHON + '_input_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_PYTHON + '_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_PYTHON + '_python">'						
						+'      <div class="form-group">'
						+'       <textarea id="' + baseID_PYTHON + '_python_content" rows="10"  placeholder="'+gettext('輸入您的程式碼...')+'"></textarea>'
						+'      </div>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_PYTHON + '_output">'
						+'      <button id="' + baseID_PYTHON + '_output_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_PYTHON + '_output_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_PYTHON + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_PYTHON + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_PYTHON);
			
			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_PYTHON + '_output_content' ).sortable();
			$( '#' + baseID_PYTHON + '_output_content' ).disableSelection();
			$( '#' + baseID_PYTHON + '_input_content' ).sortable();
			$( '#' + baseID_PYTHON + '_input_content' ).disableSelection();
			$( '#' + baseID_PYTHON +  '_calculate_content' ).sortable();
			$( '#' + baseID_PYTHON +  '_calculate_content' ).disableSelection();

			
			myCodeMirror = CodeMirror.fromTextArea(document.getElementById(baseID_PYTHON + '_python_content'), {
				lineNumbers: true,
				mode: "python",
				theme: "eclipse",
				indentUnit: 4,
				});
			myCodeMirror.setOption("extraKeys", {
				  Tab: function(cm) {
				    var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
				    cm.replaceSelection(spaces);
				  }
				});
			
			$('a[href="#' + baseID_PYTHON + '_python"]').on('shown.bs.tab', function (e) 
			{
				myCodeMirror.refresh();
			});
			
			//when input tab show
			$('a[href="#' + baseID_PYTHON + '_input"]').on('shown.bs.tab', function (e) 
			{
				//caculate to only variable
				$('[id^="' + baseID_PYTHON + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_PYTHON + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_PYTHON + '_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_PYTHON + '_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_PYTHON + '_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			
			//when output click , input to output
			$('a[href="#' + baseID_PYTHON + '_output"]').on('shown.bs.tab', function (e) 
			{
				//input content name only string
				$('[id^="' + baseID_PYTHON + '_input_content' +'_name_"]').each(function(i)
				{
					var option_name = $(this).val();
					if(option_name != '')
					{
						$('[id^="' + baseID_PYTHON + '_output_content' + '_value_"]').each(function(i)
						{
							if($(this).html().indexOf('$(' + option_name + ')') > 0)
							{
								//已存在
							}
							else
							{
								select2_new_option(baseID_PYTHON + '_output_content' + '_value_' + i,'$(' + option_name + ')',gettext('變數:') + option_name );
							}
						});
					}
				});
			});

			$('#' + baseID_PYTHON + '_output_content_add').click(function () 
			{
				chart_output_sortable_add( baseID_PYTHON + '_output_content',false,true);
				//input content name only string
				$('[id^="' + baseID_PYTHON + '_input_content' +'_name_"]').each(function(i)
				{
					var option_name = $(this).val();
					if(option_name != '')
					{
						$('[id^="' + baseID_PYTHON + '_output_content' + '_value_"]').each(function(i)
						{
							if($(this).html().indexOf('$(' + option_name + ')') > 0)
							{
								//已存在
							}
							else
							{
								select2_new_option(baseID_PYTHON + '_output_content' + '_value_' + i,'$(' + option_name + ')',gettext('變數:')+ option_name );
							}
						});
					}
				});

			});
			
			$('#' + baseID_PYTHON + '_input_content_add').click(function () 
			{
				chart_input_sortable_add( baseID_PYTHON + '_input_content',true,true);
				//caculate to only variable
				$('[id^="' + baseID_PYTHON + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_PYTHON + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_PYTHON + '_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_PYTHON + '_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_PYTHON + '_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});

			});
			$('#'+ baseID_PYTHON + '_calculate_content_add').click(function () 
			{
				chart_calculate_sortable_add(baseID_PYTHON +  '_calculate_content'); 
			});
			
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_PYTHON + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_PYTHON + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);
				item.config.autoinstall = $('#' + baseID_PYTHON + '_config_autoinstall').prop("checked");
				item.config.error_pass = $('#' + baseID_PYTHON + '_config_error_pass').prop("checked");
				item.config.load_balance = $('#' + baseID_PYTHON + '_config_load_balance').prop("checked");
				item.config.log = $('#' + baseID_PYTHON + '_config_log').prop("checked");
				item.config.code = myCodeMirror.getValue();
				
				modal_save_input(baseID_PYTHON , item);
				modal_save_output(baseID_PYTHON , item);
				modal_save_calculate(baseID_PYTHON , item);

				$('#' + baseID_PYTHON).modal('hide');
			});
			
			$('#' +  baseID_PYTHON + '_close').click(function ()
			{
				$('#' + baseID_PYTHON).modal('hide');
			});
			
		}
		//====================
		//===MODAL CHART SUBFLOW 
		//====================
		if ($('#' +baseID_SUBFLOW).length == 0)
		{
			var modal_SUBFLOW = '<div class="modal fade" id="' + baseID_SUBFLOW + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('子流程-')+'<span id="' + baseID_SUBFLOW + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_SUBFLOW + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_SUBFLOW + '_subflow" data-toggle="tab">'+gettext('子流程')+'</a></li>'
						+'     <li><a href="#' + baseID_SUBFLOW + '_subflow_input" data-toggle="tab">'+gettext('子流程輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_SUBFLOW + '_subflow_output" data-toggle="tab">'+gettext('子流程輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_SUBFLOW + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_SUBFLOW + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_SUBFLOW + '_config_error_pass" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_SUBFLOW + '_config_error_pass"></label>'
						+'       <label> '+gettext('異常時通過/標示異常')+'</label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_SUBFLOW + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_SUBFLOW + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_SUBFLOW + '_subflow">'
						+'      <ul id="' + baseID_SUBFLOW + '_subflow_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_SUBFLOW + '_subflow_input">'
						+'      <ul id="' + baseID_SUBFLOW + '_subflow_content_input" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_SUBFLOW + '_subflow_output">'
						+'      <ul id="' + baseID_SUBFLOW + '_subflow_content_output" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_SUBFLOW + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_SUBFLOW + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_SUBFLOW);
			
			//====================
			//===MODAL INIT
			//====================
			
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_SUBFLOW + '_submit').click(function ()
			{
				item = action_item_for_modal;

				//save real to object
				item.text = $('#' + baseID_SUBFLOW + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);		
				item.config.error_pass = $('#' + baseID_SUBFLOW + '_config_error_pass').prop("checked");
				item.config.log = $('#' + baseID_SUBFLOW + '_config_log').prop("checked");
				
				modal_save_subflow(baseID_SUBFLOW , item);


				$('#' + baseID_SUBFLOW).modal('hide');
			});
			$('#' +  baseID_SUBFLOW + '_close').click(function ()
			{
				$('#' + baseID_SUBFLOW).modal('hide');
			});
		}
		
		//====================
		//===MODAL CHART SWITCH 
		//====================
		if ($('#' + baseID_SWITCH).length == 0)
		{
			var modal_SWITCH = '<div class="modal fade" id="' + baseID_SWITCH + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('條件判斷-')+'<span id="' + baseID_SWITCH + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_SWITCH + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' +baseID_SWITCH + '_calculate" data-toggle="tab">'+gettext('篩選')+'</a></li>'
						+'     <li><a href="#' + baseID_SWITCH + '_rule" data-toggle="tab">'+gettext('規則')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' + baseID_SWITCH + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_SWITCH + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_SWITCH + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_SWITCH + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_SWITCH + '_calculate">'
						+'      <button id="' + baseID_SWITCH + '_calculate_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_SWITCH +  '_calculate_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_SWITCH + '_rule">'
						+'      <ul id="' + baseID_SWITCH + '_rule_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'

						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_SWITCH + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_SWITCH + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_SWITCH);
			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_SWITCH +  '_calculate_content' ).sortable();
			$( '#' + baseID_SWITCH +  '_calculate_content' ).disableSelection();
			
			$('#'+ baseID_SWITCH + '_calculate_content_add').click(function () 
			{
				chart_calculate_sortable_add(baseID_SWITCH +  '_calculate_content'); 
				//caculate to only variable
				$('[id^="' + baseID_SWITCH + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_SWITCH + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_SWITCH + '_rule_content' + '_value1_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_SWITCH + '_rule_content' +'_value1_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_SWITCH + '_rule_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
						$('[id^="' + baseID_SWITCH + '_rule_content' + '_value2_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_SWITCH + '_rule_content' +'_value2_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_SWITCH + '_rule_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			
			//when output tab show
			$('a[href="#' + baseID_SWITCH + '_rule"]').on('shown.bs.tab', function (e) 
			{
				//caculate to only variable
				$('[id^="' + baseID_SWITCH + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_SWITCH + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_SWITCH + '_rule_content' + '_value1_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_SWITCH + '_rule_content' +'_value1_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{

							}
							else
							{
								select2_new_option(baseID_SWITCH + '_rule_content' + '_value1_' + i,option_name,gettext('變數:') + option_text );
							}
						});
						$('[id^="' + baseID_SWITCH + '_rule_content' + '_value2_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_SWITCH + '_rule_content' +'_value2_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_SWITCH + '_rule_content' + '_value2_' + i , option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_SWITCH + '_submit').click(function ()
			{
				
				item = action_item_for_modal;
				item.text = $('#' + baseID_SWITCH + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);
				item.config.log = $('#' + baseID_SWITCH + '_config_log').prop("checked");

				//save real to object
				modal_save_rule(baseID_SWITCH , item);
				modal_save_calculate(baseID_SWITCH , item);


				$('#' + baseID_SWITCH).modal('hide');
			});
			$('#' +  baseID_SWITCH + '_close').click(function ()
			{
				$('#' + baseID_SWITCH).modal('hide');
			});
		}
		
		//====================
		//===MODAL CHART FORM 
		//====================
		if ($('#' + baseID_FORM).length == 0)
		{
			var modal_FORM = '<div class="modal fade" id="' + baseID_FORM + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('人工處理-')+'<span id="' + baseID_FORM + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_FORM + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_calculate" data-toggle="tab">'+gettext('篩選')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_input" data-toggle="tab">'+gettext('欄位設定')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_myform" data-toggle="tab">'+gettext('自訂表單')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_subflow" data-toggle="tab">'+gettext('驗證')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_subflow_input" data-toggle="tab">'+gettext('驗證輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_output" data-toggle="tab">'+gettext('輸出')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_quickok" data-toggle="tab">'+gettext('動作1')+'</a></li>'
						+'     <li><a href="#' + baseID_FORM + '_quickno" data-toggle="tab">'+gettext('動作2')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_FORM + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_FORM + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_FORM + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_FORM + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	

						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_calculate">'
						+'      <button id="' + baseID_FORM + '_calculate_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_FORM +  '_calculate_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_subflow">'
						+'      <ul id="' + baseID_FORM + '_subflow_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_subflow_input">'
						+'      <ul id="' + baseID_FORM + '_subflow_content_input" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_subflow_output">'
						+'      <ul id="' + baseID_FORM + '_subflow_content_output" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_input">'
						+'      <button id="' + baseID_FORM + '_input_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_FORM + '_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_quickok">'
						+'      <ul style="list-style-type: none; margin: 0; padding: 0">'
						+'        <li class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'          <table width="100%"><tr>'
						+'            <td width="15%" nowrap><input id="' + baseID_FORM + '_action1" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_FORM + '_action1"></label> '+gettext('啟用')+'</td>'
						+'            <td width="85%"><input id="' + baseID_FORM + '_action1_text" type="text" class="form-control " placeholder="'+gettext('名稱')+'"></td>'
						+'          </tr></table>'
						+'        </li>'
						+'        <li><hr style="border-color:silver"></li>'
						+'      </ul>'
						+'      <button id="' + baseID_FORM + '1_input_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_FORM + '1_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_quickno">'
						+'      <ul style="list-style-type: none; margin: 0; padding: 0">'
						+'        <li class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'          <table width="100%"><tr>'
						+'            <td width="15%" nowrap><input id="' + baseID_FORM + '_action2" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_FORM + '_action2"></label> '+gettext('啟用')+'</td>'
						+'            <td width="85%"><input id="' + baseID_FORM + '_action2_text" type="text" class="form-control " placeholder="'+gettext('名稱')+'"></td>'
						+'          </tr></table>'
						+'        </li>'
						+'        <li><hr style="border-color:silver"></li>'
						+'      </ul>'
						+'      <button id="' + baseID_FORM + '2_input_content_add" type="button" class="btn btn-default" ><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_FORM + '2_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						
						+'     <div class="tab-pane" id="' + baseID_FORM + '_myform">'						
						+'      <div class="form-group">'
						+'       <div>'
						+'         <button id="' + baseID_FORM + '_myform_button_load" type="button" class="btn btn-default">'+gettext('載入')+'</button><button id="' + baseID_FORM + '_myform_button_cancel" type="button" class="btn btn-default">'+gettext('取消')+'</button>'
						+'         <button id="' + baseID_FORM + '_myform_button_new_box6" style="display:none" type="button" class="btn btn-default">'+gettext('新增半區塊')+'</button>' //(JOB)
						+'         <button id="' + baseID_FORM + '_myform_button_new_box12" style="display:none" type="button" class="btn btn-default">'+gettext('新增全區塊')+'</button>'
						+'       </div>' 
						+'       <div id="' + baseID_FORM + '_myform_content">'
						+'       </div>' 
						+'      </div>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' +baseID_FORM + '_output">'
						+'      <button id="' + baseID_FORM + '_output_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_FORM + '_output_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left"id="' + baseID_FORM + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_FORM + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_FORM);

			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_FORM + '_input_content' ).sortable();
			$( '#' + baseID_FORM + '_input_content' ).disableSelection();
			$( '#' + baseID_FORM + '1_input_content' ).sortable();
			$( '#' + baseID_FORM + '1_input_content' ).disableSelection();
			$( '#' + baseID_FORM + '2_input_content' ).sortable();
			$( '#' + baseID_FORM + '2_input_content' ).disableSelection();
			$( '#' + baseID_FORM + '_output_content' ).sortable();
			$( '#' + baseID_FORM + '_output_content' ).disableSelection();
			
			$( '#' + baseID_FORM +  '_calculate_content' ).sortable();
			$( '#' + baseID_FORM +  '_calculate_content' ).disableSelection();
			
			$('#'+ baseID_FORM + '_calculate_content_add').click(function () 
			{
				chart_calculate_sortable_add(baseID_FORM +  '_calculate_content'); 
			});
			
			//subflow_load(baseID_FORM + '_subflow_content'); //read my subflow name
			
			$('#' + baseID_FORM + '_input_content_add').click(function () 
			{
				chart_input_sortable_form_add( baseID_FORM + '_input_content');
				$('[id^="' + baseID_FORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_FORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_FORM + '_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_FORM + '_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_FORM + '_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			$('#' + baseID_FORM + '1_input_content_add').click(function () 
			{
				chart_input_sortable_form_add( baseID_FORM + '1_input_content');
				$('[id^="' + baseID_FORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_FORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_FORM + '1_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_FORM + '1_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_FORM + '1_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			$('#' + baseID_FORM + '2_input_content_add').click(function () 
			{
				chart_input_sortable_form_add( baseID_FORM + '2_input_content');
				$('[id^="' + baseID_FORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_FORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_FORM + '2_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_FORM + '2_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_FORM + '2_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			
			$('#' + baseID_FORM + '_output_content_add').click(function () 
			{
				chart_output_sortable_add( baseID_FORM + '_output_content',true,false);
				if(formobject_for_modal != null)
				{
					if(formobject_for_modal.getObject().items != null)
					{
						formobject_for_modal.getObject().items.forEach(function(item, index, array) 
						{
							if(item.type.startsWith('box'))
							{

							}
							else
							{
								$('[id^="' + baseID_FORM + '_output_content' +'_value_"]').each(function(i)
								{
									select2_new_option(baseID_FORM + '_output_content' + '_value_' + i,'#(' + item.id + ')',gettext('欄位:') + item.config.title);
								});
							}
						});
					}
				}
			});
			
			$('#' + baseID_FORM + '_myform_button_load').click(function () 
			{
				item = action_item_for_modal;

				formobject_for_modal = new omformeng(baseID_FORM + '_myform_content');
				formobject_for_modal.init(true);
				formobject_for_modal.event_group_list(event_get_group_list_callback);
				formobject_for_modal.event_user_list(event_get_user_list_callback);
				formobject_for_modal.load(JSON.stringify(flowobject.form_object));
				
				//setData
				//formobject_for_modal.setData(item.config.form_setdata);
				
				$('#' + baseID_FORM + '_myform_button_new_box6').css('display','');
				$('#' + baseID_FORM + '_myform_button_new_box12').css('display','');
			});
			
			$('#' + baseID_FORM + '_myform_button_cancel').click(function () 
			{
				item = action_item_for_modal;
				item.config.flow_object = null;
				$('#' + baseID_FORM + '_myform_content').html('');
				formobject_for_modal = null;
				$('#' + baseID_FORM + '_myform_button_new_box6').css('display','none');
				$('#' + baseID_FORM + '_myform_button_new_box12').css('display','none');

			});
			$('#' + baseID_FORM + '_myform_button_new_box6').click(function () 
			{
				formobject_for_modal.add_item('box6');
			});
			$('#' + baseID_FORM + '_myform_button_new_box12').click(function () 
			{
				formobject_for_modal.add_item('box12');
			});
			//when input tab show
			$('a[href="#' + baseID_FORM + '_input"]').on('shown.bs.tab', function (e) 
			{
				//caculate to only variable
				$('[id^="' + baseID_FORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_FORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_FORM + '_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_FORM + '_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_FORM + '_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			$('a[href="#' + baseID_FORM + '_input1"]').on('shown.bs.tab', function (e) 
			{
				//caculate to only variable
				$('[id^="' + baseID_FORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_FORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_FORM + '1_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_FORM + '1_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_FORM + '1_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			$('a[href="#' + baseID_FORM + '_input2"]').on('shown.bs.tab', function (e) 
			{
				//caculate to only variable
				$('[id^="' + baseID_FORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_FORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_FORM + '2_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_FORM + '2_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_FORM + '2_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			//when output click , input to output
			$('a[href="#' + baseID_FORM + '_output"]').on('shown.bs.tab', function (e) 
			{
				if(formobject_for_modal != null)
				{
					if(formobject_for_modal.getObject().items != null)
					{
						formobject_for_modal.getObject().items.forEach(function(item, index, array) 
						{
							if(item.type.startsWith('box'))
							{

							}
							else
							{
								$('[id^="' + baseID_FORM + '_output_content' +'_value_"]').each(function(i)
								{
									select2_new_option(baseID_FORM + '_output_content' + '_value_' + i,'#(' + item.id + ')',gettext('欄位:') + item.config.title);
								});
							}
						});
					}
				}

			});
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_FORM + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_FORM + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);
				item.config.log = $('#' + baseID_FORM + '_config_log').prop("checked");
				item.config.action1 = $('#' + baseID_FORM + '_action1').prop("checked");
				item.config.action1_text = $('#' + baseID_FORM + '_action1_text').val();
				item.config.action2 = $('#' + baseID_FORM + '_action2').prop("checked");
				item.config.action2_text = $('#' + baseID_FORM + '_action2_text').val();
				
				//save real to object
				 modal_save_calculate(baseID_FORM , item);
				 modal_save_input(baseID_FORM , item);
				 modal_save_subflow(baseID_FORM , item);
				 modal_save_output(baseID_FORM , item);
				 
				 if(formobject_for_modal == null)
				 {
					 item.config.form_object = null;
					 //item.config.form_setdata = [];
				 }
				 else
				 {
					 //更新最大ID給主Form(要比誰比較大)(JOB)
					 flowobject.form_object.form_item_counter = formobject_for_modal.getObject().form_item_counter;
					 flowobject.form_object.form_box_counter = formobject_for_modal.getObject().form_box_counter;
					 item.config.form_object = JSON.parse( formobject_for_modal.toString());
					 //
				 }
				$('#' + baseID_FORM).modal('hide');
			});
			$('#' +  baseID_FORM + '_close').click(function ()
			{
				$('#' + baseID_FORM).modal('hide');
			});
		}
		//====================
		//===MODAL CHART SLEEP 
		//====================
		if ($('#' + baseID_SLEEP).length == 0)
		{
			var modal_SLEEP = '<div class="modal fade" id="' + baseID_SLEEP + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('暫停-')+'<span id="' + baseID_SLEEP + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' +baseID_SLEEP + '_input" data-toggle="tab">'+gettext('輸入')+'</a></li>'
						+'     <li><a href="#' +baseID_SLEEP + '_config" data-toggle="tab">'+gettext('預設值')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' + baseID_SLEEP + '_input">'
						+'      <ul style="list-style-type: none; margin: 0; padding: 0">'
						+'        <li class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'         <table width="100%"><tr>'
						+'           <td width="4%"></span></td>'
						+'          <td width="6%"></td>'
						+'          <td width="30%"><select id="' + baseID_SLEEP + '_input_value" class="form-control select2" placeholder="'+gettext('輸入資料')+'" style="width:100%"></select></td>'
						+'          <td width="30%"><input type="text" class="form-control " value="msec" readonly></td>'
						+'          <td width="30%"><input type="text" class="form-control " placeholder="'+gettext('設定暫停的豪秒(ms)數')+'" readonly></td>'
						+'         </tr></table>'
						+'        </li>'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_SLEEP + '_config">'
						+'		<div class="form-group">'
						+'		  <label>'+gettext('暫停豪秒')+'</label>'
						+'		  <input id="' + baseID_SLEEP + '_config_msec" type="text" name="refresh_rate_$" class="js-range-slider">'
						+'		</div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_SLEEP + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_SLEEP + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_SLEEP);
			//====================
			//===MODAL INIT
			//====================
			$('#' + baseID_SLEEP + '_config_msec').ionRangeSlider({
				min     : 0,
			  	max     : 60000,
				step    : 500,
				from	: 5000,
				type    : 'single',
				postfix : gettext(' 豪秒'),
				prettify: false,
				grid	: true,
				grid_num: 200,
		    });
			$('#' + baseID_SLEEP + '_input_value').select2({tags: false,placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			//$('#' + baseID_SLEEP + '_input_value').val(null).trigger('change');
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_SLEEP + '_submit').click(function ()
			{
				item = action_item_for_modal;
				var from_value = $("#" + baseID_SLEEP + '_config_msec').data().from; //選的預設值
				item.config.msec = from_value;
				item.config.value = $('#' + baseID_SLEEP + '_input_value').val();
				

				$('#' + baseID_SLEEP).modal('hide');
			});
			$('#' +  baseID_SLEEP + '_close').click(function ()
			{
				$('#' + baseID_SLEEP).modal('hide');
			});
		}
		
		//====================
		//===MODAL CHART ASYNC 
		//====================
		if ($('#' + baseID_ASYNC).length == 0)
		{
			var modal_ASYNC = '<div class="modal fade" id="' + baseID_ASYNC + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('並行-')+'<span id="' + baseID_ASYNC + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_ASYNC + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li ><a href="#' +baseID_ASYNC + '_rule" data-toggle="tab">'+gettext('規則')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_ASYNC + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_ASYNC + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_ASYNC + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_ASYNC + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_ASYNC + '_rule">'
						+'      <ul id="' + baseID_ASYNC + '_rule_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'

						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_ASYNC + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_ASYNC + '_submit">'+gettext('關閉')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_ASYNC);
			//====================
			//===MODAL INIT
			//====================
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_ASYNC + '_submit').click(function ()
			{
				item = action_item_for_modal;
				item.text = $('#' + baseID_ASYNC + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);
				item.config.log = $('#' + baseID_ASYNC + '_config_log').prop("checked");
				$('#' + baseID_ASYNC).modal('hide');
			});
			$('#' +  baseID_ASYNC + '_close').click(function ()
			{
				$('#' + baseID_ASYNC).modal('hide');
			});
		}
		//====================
		//===MODAL CHART COLLECTION 
		//====================
		if ($('#' + baseID_COLLECTION).length == 0)
		{
			var modal_COLLECTION = '<div class="modal fade" id="' + baseID_COLLECTION + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('並行匯集-')+'<span id="' + baseID_COLLECTION + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_COLLECTION + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li ><a href="#' +baseID_COLLECTION + '_rule" data-toggle="tab">'+gettext('規則')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_COLLECTION + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_COLLECTION + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_COLLECTION + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_COLLECTION + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_COLLECTION + '_rule">'
						+'      <ul id="' + baseID_COLLECTION + '_rule_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'

						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_COLLECTION + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_COLLECTION + '_submit">'+gettext('關閉')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_COLLECTION);
			//====================
			//===MODAL INIT
			//====================
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_COLLECTION + '_submit').click(function ()
			{
				item = action_item_for_modal;
				item.text = $('#' + baseID_COLLECTION + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);
				item.config.log = $('#' + baseID_COLLECTION + '_config_log').prop("checked");
				item.config.main = $('input[type=radio][name=' + baseID_COLLECTION + '_rule_content' + '_targetR' + ']:checked').val();
				$('#' + baseID_COLLECTION).modal('hide');
			});
			$('#' +  baseID_COLLECTION + '_close').click(function ()
			{
				$('#' + baseID_COLLECTION).modal('hide');
			});
		}
		
		//====================
		//===MODAL CHART OUTFLOW 
		//====================
		if ($('#' +baseID_OUTFLOW).length == 0)
		{
			var modal_OUTFLOW = '<div class="modal fade" id="' + baseID_OUTFLOW + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('外部流程-')+'<span id="' + baseID_OUTFLOW + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_OUTFLOW + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_OUTFLOW + '_subflow" data-toggle="tab">'+gettext('外部流程')+'</a></li>'
						+'     <li><a href="#' + baseID_OUTFLOW + '_subflow_input" data-toggle="tab">'+gettext('流程輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_OUTFLOW + '_subflow_output" data-toggle="tab">'+gettext('流程輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_OUTFLOW + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_OUTFLOW + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_OUTFLOW + '_config_error_pass" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_OUTFLOW + '_config_error_pass"></label>'
						+'       <label> '+gettext('異常時通過/標示異常')+'</label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_OUTFLOW + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_OUTFLOW + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_OUTFLOW + '_subflow">'
						+'      <ul id="' + baseID_OUTFLOW + '_subflow_content" style="list-style-type: none; margin: 0; padding: 0">' 
						+'<li class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="50%"><select id="' + baseID_OUTFLOW + '_select_app" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="50%"><select id="' + baseID_OUTFLOW + '_select_flow" class="form-control select2" style="width:100%"></select></td>'
						+'</tr></table>'
						+'</li>'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_OUTFLOW + '_subflow_input">'
						+'      <ul id="' + baseID_OUTFLOW + '_subflow_content_input" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_OUTFLOW + '_subflow_output">'
						+'      <ul id="' + baseID_OUTFLOW + '_subflow_content_output" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_OUTFLOW + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_OUTFLOW + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_OUTFLOW);
			
			//====================
			//===MODAL INIT
			//====================
			var app_data = [];
			var flow_data = [];
			var app_option = '';
			var flow_option = '';
			$('#' + baseID_OUTFLOW + '_select_app').select2({tags: false,placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			$('#' + baseID_OUTFLOW + '_select_flow').select2({tags: false,placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});

			if(event_get_app_list_callback == null)
			{
				app_data = [ 
						{"id":"1","app_name":"測試用app1"},
						{"id":"2","app_name":"測試用app2"}
						]
			}
			else
			{
				app_data = event_get_app_list_callback();
			}
			
			app_data.forEach(function(app_item) 
			{
				app_option += '<option value="' + app_item.app_name + '">' + app_item.app_name + '</option>'
			});
			$('#' +  baseID_OUTFLOW + '_select_app').html(app_option);
			$('#' +  baseID_OUTFLOW + '_select_app').val(null).trigger('change');
			$('#' +  baseID_OUTFLOW + '_select_app').change(function ()
			{
				flow_option = '';
				//變更時查詢flow
				if(event_get_flow_list_callback == null)
				{
					flow_data =[
						{"flow_uuid":"3644a15122304e93a475312841c72643","flow_name":"流程1","flow_app_id":"1"},
						{"flow_uuid":"f909603f3b004666b69516ba259765b0","flow_name":"流程2","flow_app_id":"1"}
						]
				}
				else
				{
					flow_data = event_get_flow_list_callback($('#' + this.id).val());
				}
				
				flow_data.forEach(function(flow_item) 
				{
					flow_option += '<option value="' + flow_item.flow_name + '">' + flow_item.flow_name + '</option>'
				});
				
				$('#' +  baseID_OUTFLOW + '_select_flow').html(flow_option);
				$('#' +  baseID_OUTFLOW + '_select_flow').val(null).trigger('change');
				
			});
			$('#' +  baseID_OUTFLOW + '_select_flow').change(function ()
			{
				var ul_id = baseID_OUTFLOW + '_subflow_content';
				$( '#' + ul_id + '_input' ).html("");
				$( '#' + ul_id + '_output').html("");
				var item_li_input_content = '<li id="' + ul_id + '_input_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
							+'<table width="100%"><tr>'
							+'<td width="2%"><span class="fa fa-arrows-v"></span></td>'
							+'<td width="8%" nowrap><input id="' + ul_id + '_input_require__index_" type="checkbox" class="icheckbox_minimal-blue"><label for="' + ul_id + '_input_require__index_" readonly></label> '+gettext('必填')+'</td>'
							+'<td width="30%"><select id="' + ul_id + '_input_value__index_" class="form-control select2" placeholder="'+gettext('輸入資料')+'" style="width:100%"></select></td>'
							+'<td width="30%"><select id="' + ul_id + '_input_name__index_" type="text" class="form-control " placeholder="'+gettext('變數名稱')+'" style="width:100%" readonly></select></td>'
							+'<td width="30%"><input id="' + ul_id + '_input_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
							+'</tr></table>'
							+'</li>';
				var item_li_output_content = '<li id="' + ul_id + '_output_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
							+'<table width="100%"><tr>'
							+'<td width="4%"><span class="fa fa-arrows-v"></span></td>'
							+'<td width="32%"><select id="' + ul_id + '_output_value__index_" class="form-control select2" placeholder="'+gettext('輸出值')+'" style="width:100%" readonly></select></td>'
							+'<td width="32%"><select id="' + ul_id + '_output_name__index_" class="form-control select2" placeholder="'+gettext('輸出名稱')+'" style="width:100%"></select></td>'
							+'<td width="32%"><input id="' + ul_id + '_output_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
							+'</tr></table>'
							+'</li>';
				//query
				var input_option = [];
				var output_option = [];
				if(event_get_flowIO_list_callback != null)
				{
					var result = event_get_flowIO_list_callback($('#' +  baseID_OUTFLOW + '_select_app').val(), $('#' +  baseID_OUTFLOW + '_select_flow').val());
					if(result != null)
					{
						input_option = result.outside_input;
						output_option = result.outside_output;
					}
				}
				var index_recoder = 0;
				input_option.forEach(function(input_item, index)
				{
					$( '#' + ul_id + '_input' ).append(item_li_input_content.replace(/_index_/g,index));
					

					//read form field to select2
					$( '#' + ul_id + '_input_value_' + index ).html(select_option_value() + select_option_form());
					//select2 enable
					$( '#' + ul_id + '_input_value_' + index ).select2({tags: true , placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
					
					var item_text = '';
					if(input_item.name.startsWith('$('))
					{
						item_text = input_item.name.substring(2);
						item_text = item_text.substring(0,item_text.length -1);
						$( '#' + ul_id + '_input_name_' + index ).html('<option value="$(' + item_text + ')">'+gettext('變數:') + item_text + '</option>');
						$( '#' + ul_id + '_input_name_' + index ).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
						$( '#' + ul_id + '_input_name_' + index ).prop("disabled", true);
					}
					else if(input_item.name.startsWith('#'))
					{
						if(input_item.name.startsWith('#('))
						{
							item_text = input_item.name.substring(2);
							item_text = item_text.substring(0,item_text.length -1);
							$( '#' + ul_id + '_input_name_' + index ).html('<option value="#(' + item_text + ')">'+gettext('欄位:') + input_item.des + '</option>');
							$( '#' + ul_id + '_input_name_' + index ).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
							$( '#' + ul_id + '_input_name_' + index ).prop("disabled", true);
						}
						else if(input_item.name.startsWith('#G1(')||input_item.name.startsWith('#G2('))
						{
							$( '#' + ul_id + '_input_name_' + index ).html('<option value="' + input_item.name + '">'+gettext('欄位:') + input_item.des + '</option>');
							$( '#' + ul_id + '_input_name_' + index ).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
							$( '#' + ul_id + '_input_name_' + index ).prop("disabled", true);
						}
						
					}
					else
					{
						item_text = input_item.name;
					}
						
					
					//相同名稱自動帶入(僅限變數)
					if($( '#' + ul_id + '_input_value_' + index ).html().indexOf('$(' + item_text + ')') > 0 )
					{
						$( '#' + ul_id + '_input_value_' + index ).val('$(' + item_text + ')').trigger('change');
					}
					else
					{
						$( '#' + ul_id + '_input_value_' + index ).val(null).trigger('change');
					}
					
					//寫設定值
					//$( '#' + ul_id + '_input_name_' + index ).val(input_item.name);
					if(input_item.name.startsWith('#('))
					{
						$( '#' + ul_id + '_input_des_' + index ).val(gettext('表單欄位'));
					}
					else
					{
						$( '#' + ul_id + '_input_des_' + index ).val(input_item.des);
					}
					index_recoder = index;
				});
				
				output_option.forEach(function(output_item, index)
				{
					$( '#' + ul_id + '_output' ).append(item_li_output_content.replace(/_index_/g,index));

					//read form field to select2
					$( '#' + ul_id + '_output_name_' + index ).html(select_option_value());
					//select2 enable
					//$( '#' + ul_id + '_output_name_' + index ).select2({tags: false ,placeholder: '' ,allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
					$( '#' + ul_id + '_output_name_' + index ).select2({tags: true,placeholder : gettext("輸出變數"),dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}},
								createTag: function(params) 
								{
									var term = $.trim(params.term);

									if (term == '') 
									{
									  return null;
									}
									
									if ((term.startsWith(gettext('變數:'))))
									{
										term = term.substring(3);
									}
									
									return {
									  id: '$(' + term + ')',
									  text: gettext('變數:') + term,
									  newTag: true // add additional parameters
									}
								}});
					
					var item_text = '';
					if(output_item.name.startsWith('$('))
					{
						item_text = output_item.name.substring(2);
						item_text = item_text.substring(0,item_text.length -1);
						$( '#' + ul_id + '_output_value_' + index ).html('<option value="$(' + item_text + ')">'+gettext('變數:') + item_text + '</option>');
						$( '#' + ul_id + '_output_value_' + index ).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
						$( '#' + ul_id + '_output_value_' + index ).prop("disabled", true);
					}
					else
					{
						item_text = output_item.name;
					}
					
					
					//寫設定值
					//$( '#' + ul_id + '_output_value_' + index ).val(gettext('變數:') + item_text );
					$( '#' + ul_id + '_output_des_' + index ).val(output_item.des);

					//相同名稱自動帶入
					if($( '#' + ul_id + '_output_name_' + index ).html().indexOf('$(' + item_text + ')') > 0 )
					{
						$( '#' + ul_id + '_output_name_' + index ).val('$(' + item_text + ')').trigger('change');;
					}
					else
					{
						$( '#' + ul_id + '_output_name_' + index ).val(null).trigger('change');
					}
				});
				
			});
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_OUTFLOW + '_submit').click(function ()
			{
				item = action_item_for_modal;

				//save real to object
				item.text = $('#' + baseID_OUTFLOW + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);		
				item.config.error_pass = $('#' + baseID_OUTFLOW + '_config_error_pass').prop("checked");
				item.config.log = $('#' + baseID_OUTFLOW + '_config_log').prop("checked");
				
				item.config.app_name = $('#' + baseID_OUTFLOW + '_select_app').val();
				item.config.flow_name = $('#' + baseID_OUTFLOW + '_select_flow').val();
				
				modal_save_outflow(baseID_OUTFLOW , item);


				$('#' + baseID_OUTFLOW).modal('hide');
			});
			$('#' +  baseID_OUTFLOW + '_close').click(function ()
			{
				$('#' + baseID_OUTFLOW).modal('hide');
			});
		}
		//====================
		//===MODAL CHART INFLOW 
		//====================
		if ($('#' +baseID_INFLOW).length == 0)
		{
			var modal_INFLOW = '<div class="modal fade" id="' + baseID_INFLOW + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('呼叫流程-')+'<span id="' + baseID_INFLOW + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_INFLOW + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_INFLOW + '_subflow" data-toggle="tab">'+gettext('流程')+'</a></li>'
						+'     <li><a href="#' + baseID_INFLOW + '_subflow_input" data-toggle="tab">'+gettext('流程輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_INFLOW + '_subflow_output" data-toggle="tab">'+gettext('流程輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_INFLOW + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_INFLOW + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_INFLOW + '_config_error_pass" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_INFLOW + '_config_error_pass"></label>'
						+'       <label> '+gettext('異常時通過/標示異常')+'</label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_INFLOW + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_INFLOW + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_INFLOW + '_subflow">'
						+'      <ul id="' + baseID_INFLOW + '_subflow_content" style="list-style-type: none; margin: 0; padding: 0">' 
						+'<li class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="50%"><select id="' + baseID_INFLOW + '_select_flow" class="form-control select2" style="width:100%"></select></td>'
						+'</tr></table>'
						+'</li>'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_INFLOW + '_subflow_input">'
						+'      <ul id="' + baseID_INFLOW + '_subflow_content_input" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_INFLOW + '_subflow_output">'
						+'      <ul id="' + baseID_INFLOW + '_subflow_content_output" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_INFLOW + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_INFLOW + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_INFLOW);
			
			//====================
			//===MODAL INIT
			//====================
			var app_data = [];
			var flow_data = [];
			var app_option = '';
			var flow_option = '';
			
			$('#' + baseID_INFLOW + '_select_flow').select2({tags: false,placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});


			if(event_get_my_flow_list_callback == null)
			{
				app_data = [
						{"flow_name":"流程1"},
						{"flow_name":"流程2"}
						]
			}
			else
			{
				app_data = event_get_my_flow_list_callback();
			}
			
			app_data.forEach(function(app_item) 
			{
				app_option += '<option value="' + app_item.flow_name + '">' + app_item.flow_name + '</option>'
			});
			$('#' +  baseID_INFLOW + '_select_flow').html(app_option);
			$('#' +  baseID_INFLOW + '_select_flow').val(null).trigger('change');
			$('#' +  baseID_INFLOW + '_select_flow').change(function ()
			{
				var ul_id = baseID_INFLOW + '_subflow_content';
				$( '#' + ul_id + '_input' ).html("");
				$( '#' + ul_id + '_output').html("");
				var item_li_input_content = '<li id="' + ul_id + '_input_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
							+'<table width="100%"><tr>'
							+'<td width="2%"><span class="fa fa-arrows-v"></span></td>'
							+'<td width="8%" nowrap><input id="' + ul_id + '_input_require__index_" type="checkbox" class="icheckbox_minimal-blue"><label for="' + ul_id + '_input_require__index_" readonly></label> '+gettext('必填')+'</td>'
							+'<td width="30%"><select id="' + ul_id + '_input_value__index_" class="form-control select2" placeholder="'+gettext('輸入資料')+'" style="width:100%" readonly></select></td>'
							+'<td width="30%"><select id="' + ul_id + '_input_name__index_" type="text" class="form-control " placeholder="'+gettext('變數名稱')+'" style="width:100%" readonly></select></td>'
							+'<td width="30%"><input id="' + ul_id + '_input_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
							+'</tr></table>'
							+'</li>';
				var item_li_output_content = '<li id="' + ul_id + '_output_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
							+'<table width="100%"><tr>'
							+'<td width="4%"><span class="fa fa-arrows-v"></span></td>'
							+'<td width="32%"><select id="' + ul_id + '_output_value__index_"class="form-control select2" placeholder="'+gettext('輸出值')+'" readonly style="width:100%"></select?</td>'
							+'<td width="32%"><select id="' + ul_id + '_output_name__index_" class="form-control select2" placeholder="'+gettext('輸出名稱')+'" style="width:100%"></select></td>'
							+'<td width="32%"><input id="' + ul_id + '_output_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
							+'</tr></table>'
							+'</li>';
				//query
				var input_option = [];
				var output_option = [];
				if(event_get_my_flowIO_list_callback != null)
				{
					var result = event_get_my_flowIO_list_callback($('#' +  baseID_INFLOW + '_select_flow').val());
					if(result != null)
					{
						input_option = result.outside_input;
						output_option = result.outside_output;
					}
					else
					{
					}
				}
				else
				{
				}

				var index_recoder = 0;
				input_option.forEach(function(input_item, index)
				{
					$( '#' + ul_id + '_input' ).append(item_li_input_content.replace(/_index_/g,index));
					//read form field to select2
					$( '#' + ul_id + '_input_value_' + index ).html(select_option_value() + select_option_form());
					//select2 enable
					$( '#' + ul_id + '_input_value_' + index ).select2({tags: true , placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
					
					var item_text = '';
					if(input_item.name.startsWith('$('))
					{
						item_text = input_item.name.substring(2);
						item_text = item_text.substring(0,item_text.length -1);
						$( '#' + ul_id + '_input_name_' + index ).html('<option value="$(' + item_text + ')">'+gettext('變數:') + item_text + '</option>');
						$( '#' + ul_id + '_input_name_' + index ).select2({tags: false , placeholder: '',allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
					}
					else if(input_item.name.startsWith('#'))
					{
						if(input_item.name.startsWith('#('))
						{
							item_text = input_item.name.substring(2);
							item_text = item_text.substring(0,item_text.length -1);
							$( '#' + ul_id + '_input_name_' + index ).html('<option value="#(' + item_text + ')">'+gettext('欄位:') + input_item.des + '</option>');
							$( '#' + ul_id + '_input_name_' + index ).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
							$( '#' + ul_id + '_input_name_' + index ).prop("disabled", true);
						}
						else if(input_item.name.startsWith('#G1(')||input_item.name.startsWith('#G2('))
						{
							$( '#' + ul_id + '_input_name_' + index ).html('<option value="' + input_item.name + '">'+gettext('欄位:') + input_item.des + '</option>');
							$( '#' + ul_id + '_input_name_' + index ).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
							$( '#' + ul_id + '_input_name_' + index ).prop("disabled", true);
						}
					}
					else
					{
						item_text = input_item.name;
					}
						
					
					//相同名稱自動帶入(僅限變數)
					if($( '#' + ul_id + '_input_value_' + index ).html().indexOf('$(' + item_text + ')') > 0 )
					{
						$( '#' + ul_id + '_input_value_' + index ).val('$(' + item_text + ')').trigger('change');
					}
					else
					{
						$( '#' + ul_id + '_input_value_' + index ).val(null).trigger('change');
					}
					
					//寫設定值
					//$( '#' + ul_id + '_input_name_' + index ).val(input_item.name);
					if(input_item.name.startsWith('#('))
					{
						$( '#' + ul_id + '_input_des_' + index ).val(gettext('表單欄位'));
					}
					else
					{
						$( '#' + ul_id + '_input_des_' + index ).val(input_item.des);
					}
					index_recoder = index;
				});
				
				output_option.forEach(function(output_item, index)
				{
					$( '#' + ul_id + '_output' ).append(item_li_output_content.replace(/_index_/g,index));

					//read form field to select2
					$( '#' + ul_id + '_output_name_' + index ).html(select_option_value());
					//select2 enable
					//$( '#' + ul_id + '_output_name_' + index ).select2({tags: false ,placeholder: '' ,allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
					$( '#' + ul_id + '_output_name_' + index ).select2({tags: true,placeholder : gettext("輸出變數"),dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}},
								createTag: function(params) 
								{
									var term = $.trim(params.term);

									if (term == '') 
									{
									  return null;
									}
									
									if ((term.startsWith(gettext('變數:'))))
									{
										term = term.substring(3);
									}
									
									return {
									  id: '$(' + term + ')',
									  text: gettext('變數:') + term,
									  newTag: true // add additional parameters
									}
								}});
					
					var item_text = '';
					
					if(output_item.name.startsWith('$('))
					{
						item_text = output_item.name.substring(2);
						item_text = item_text.substring(0,item_text.length -1);
						$( '#' + ul_id + '_output_value_' + index ).html('<option value="$(' + item_text + ')">'+gettext('變數:') + item_text + '</option>');
						$( '#' + ul_id + '_output_value_' + index ).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
						$( '#' + ul_id + '_output_value_' + index ).prop("disabled", true);
					}
					else
					{
						item_text = output_item.name;
					}
					
					//寫設定值
					$( '#' + ul_id + '_output_value_' + index ).html('<option value="$(' + item_text + ')">'+gettext('變數:') + item_text + '</option>');
					$( '#' + ul_id + '_output_des_' + index ).val(output_item.des);

					//相同名稱自動帶入
					if($( '#' + ul_id + '_output_name_' + index ).html().indexOf('$(' + item_text + ')') > 0 )
					{
						$( '#' + ul_id + '_output_name_' + index ).val('$(' + item_text + ')').trigger('change');;
					}
					else
					{
						$( '#' + ul_id + '_output_name_' + index ).val(null).trigger('change');
					}
				});
				
			});
			
			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_INFLOW + '_submit').click(function ()
			{
				item = action_item_for_modal;

				//save real to object
				item.text = $('#' + baseID_INFLOW + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);		
				item.config.error_pass = $('#' + baseID_INFLOW + '_config_error_pass').prop("checked");
				item.config.log = $('#' + baseID_INFLOW + '_config_log').prop("checked");
				
				item.config.flow_name = $('#' + baseID_INFLOW + '_select_flow').val();
				
				modal_save_outflow(baseID_INFLOW , item);


				$('#' + baseID_INFLOW).modal('hide');
			});
			$('#' +  baseID_INFLOW + '_close').click(function ()
			{
				$('#' + baseID_INFLOW).modal('hide');
			});
		}
		
		//====================
		//===MODAL CHART SETFORM 
		//====================
		if ($('#' + baseID_SETFORM).length == 0)
		{
			var modal_SETFORM = '<div class="modal fade" id="' + baseID_SETFORM + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title">  '+gettext('欄位設定-')+'<span id="' + baseID_SETFORM + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_SETFORM + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_SETFORM + '_calculate" data-toggle="tab">'+gettext('篩選')+'</a></li>'
						+'     <li><a href="#' + baseID_SETFORM + '_input" data-toggle="tab">'+gettext('欄位設定')+'</a></li>'
						+'     <li><a href="#' + baseID_SETFORM + '_output" data-toggle="tab">'+gettext('輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_SETFORM + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_SETFORM + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <input id="' + baseID_SETFORM + '_config_log" type="checkbox" class="icheckbox_minimal-blue"><label for="' + baseID_SETFORM + '_config_log"></label>'
						+'       <label> '+gettext('紀錄Log')+'</label>'
						+'      </div>'	
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_SETFORM + '_calculate">'
						+'      <button id="' + baseID_SETFORM + '_calculate_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_SETFORM +  '_calculate_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'

						+'     <div class="tab-pane" id="' + baseID_SETFORM + '_input">'
						+'      <button id="' + baseID_SETFORM + '_input_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_SETFORM + '_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' +baseID_SETFORM + '_output">'
						+'      <button id="' + baseID_SETFORM + '_output_content_add" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_SETFORM + '_output_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left"id="' + baseID_SETFORM + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_SETFORM + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_SETFORM);

			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_SETFORM + '_input_content' ).sortable();
			$( '#' + baseID_SETFORM + '_input_content' ).disableSelection();
			$( '#' + baseID_SETFORM + '_output_content' ).sortable();
			$( '#' + baseID_SETFORM + '_output_content' ).disableSelection();
			
			$( '#' + baseID_SETFORM +  '_calculate_content' ).sortable();
			$( '#' + baseID_SETFORM +  '_calculate_content' ).disableSelection();
			
			$('#'+ baseID_SETFORM + '_calculate_content_add').click(function () 
			{
				chart_calculate_sortable_add(baseID_SETFORM +  '_calculate_content'); 
			});
			
			//subflow_load(baseID_SETFORM + '_subflow_content'); //read my subflow name
			
			$('#' + baseID_SETFORM + '_input_content_add').click(function () 
			{
				chart_input_sortable_form_add( baseID_SETFORM + '_input_content');
				$('[id^="' + baseID_SETFORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_SETFORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_SETFORM + '_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_SETFORM + '_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_SETFORM + '_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});
			
			$('#' + baseID_SETFORM + '_output_content_add').click(function () 
			{
				chart_output_sortable_add( baseID_SETFORM + '_output_content',true,false);
				if(formobject_for_modal != null)
				{
					if(formobject_for_modal.getObject().items != null)
					{
						formobject_for_modal.getObject().items.forEach(function(item, index, array) 
						{
							if(item.type.startsWith('box'))
							{

							}
							else
							{
								$('[id^="' + baseID_SETFORM + '_output_content' +'_value_"]').each(function(i)
								{
									select2_new_option(baseID_SETFORM + '_output_content' + '_value_' + i,'#(' + item.id + ')',gettext('欄位:') + item.config.title);
								});
							}
						});
					}
				}
			});
				
			//when input tab show
			$('a[href="#' + baseID_SETFORM + '_input"]').on('shown.bs.tab', function (e) 
			{
				//caculate to only variable
				$('[id^="' + baseID_SETFORM + '_calculate_content' +'_to_"]').each(function(i)
				{
					var my = $('#' + baseID_SETFORM + '_calculate_content' +'_to_' + i);
					var option_name = my.val();
					if(option_name != null)
					{
						var option_text = option_name.substring(2);
						option_text = option_text.substring(0,option_text.length -1);
						$('[id^="' + baseID_SETFORM + '_input_content' + '_value_"]').each(function(i)
						{
							var input_name_select_object = $('#' + baseID_SETFORM + '_input_content' +'_value_' + i);
							if(input_name_select_object.html().indexOf('value="' + option_name + '"') > 0)
							{
								//已存在
							}
							else
							{
								//加上
								select2_new_option(baseID_SETFORM + '_input_content' + '_value_' + i,option_name,gettext('變數:') + option_text );
							}
						});
					}
				});
			});

			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_SETFORM + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_SETFORM + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);
				item.config.log = $('#' + baseID_SETFORM + '_config_log').prop("checked");
				
				//save real to object
				modal_save_calculate(baseID_SETFORM , item);
				modal_save_input(baseID_SETFORM , item);
				modal_save_output(baseID_SETFORM , item);
				 
				$('#' + baseID_SETFORM).modal('hide');
			});
			$('#' +  baseID_SETFORM + '_close').click(function ()
			{
				$('#' + baseID_SETFORM).modal('hide');
			});
		}
		//====================
		//===MODAL CHART ORG1 
		//====================
		if ($('#' + baseID_ORG1).length == 0)
		{
			var modal_ORG1 = '<div class="modal fade" id="' + baseID_ORG1 + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('組織-同系職務-')+'<span id="' + baseID_ORG1 + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_ORG1 + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_ORG1 + '_input" data-toggle="tab">'+gettext('輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_ORG1 + '_output" data-toggle="tab">'+gettext('輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_ORG1 + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label >'+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_ORG1 + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'					
						+'     </div>'
						
						
						+'     <div class="tab-pane" id="' + baseID_ORG1 + '_input">'
						+'      <ul id="' + baseID_ORG1 + '_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_ORG1 + '_output">'
						+'      <ul id="' + baseID_ORG1 + '_output_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_ORG1 + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_ORG1 + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_ORG1);
			
			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_ORG1 + '_output_content' ).sortable();
			$( '#' + baseID_ORG1 + '_output_content' ).disableSelection();
			$( '#' + baseID_ORG1 + '_input_content' ).sortable();
			$( '#' + baseID_ORG1 + '_input_content' ).disableSelection();

			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_ORG1 + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_ORG1 + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);

				modal_save_input(baseID_ORG1 , item);
				modal_save_output(baseID_ORG1 , item);

				$('#' + baseID_ORG1).modal('hide');
			});
			
			$('#' +  baseID_ORG1 + '_close').click(function ()
			{
				$('#' + baseID_ORG1).modal('hide');
			});
			
		}
		//====================
		//===MODAL CHART ORG2 
		//====================
		if ($('#' + baseID_ORG2).length == 0)
		{
			var modal_ORG2 = '<div class="modal fade" id="' + baseID_ORG2 + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('組織-部門職務-')+'<span id="' + baseID_ORG2 + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_ORG2 + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_ORG2 + '_input" data-toggle="tab">'+gettext('輸入')+'</a></li>'
						+'     <li><a href="#' + baseID_ORG2 + '_output" data-toggle="tab">'+gettext('輸出')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_ORG2 + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label >'+gettext('顯示名稱')+'</label>'
						+'       <input id="' + baseID_ORG2 + '_config_text" type="text" class="form-control" placeholder="'+gettext('請輸入名稱...')+'" >'
						+'      </div>'					
						+'     </div>'
						
						
						+'     <div class="tab-pane" id="' + baseID_ORG2 + '_input">'
						+'      <ul id="' + baseID_ORG2 + '_input_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_ORG2 + '_output">'
						+'      <ul id="' + baseID_ORG2 + '_output_content" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_ORG2 + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_ORG2 + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			flowcontent.append(modal_ORG2);
			
			//====================
			//===MODAL INIT
			//====================
			$( '#' + baseID_ORG2 + '_output_content' ).sortable();
			$( '#' + baseID_ORG2 + '_output_content' ).disableSelection();
			$( '#' + baseID_ORG2 + '_input_content' ).sortable();
			$( '#' + baseID_ORG2 + '_input_content' ).disableSelection();

			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_ORG2 + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_ORG2 + '_config_text').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);

				modal_save_input(baseID_ORG2 , item);
				modal_save_output(baseID_ORG2 , item);

				$('#' + baseID_ORG2).modal('hide');
			});
			
			$('#' +  baseID_ORG2 + '_close').click(function ()
			{
				$('#' + baseID_ORG2).modal('hide');
			});
			
		}
		
		
	}
	
	//====================
	//===MODAL ITEM LOAD SAVE FUNCTION 
	//====================
	
	
	function modal_load_input(baseID , item)
	{
		item.config.input.forEach(function(input_item, index) //input
		{
			if(item.type == 'start')
			{
				chart_input_sortable_add(baseID + '_input_content',true , false);
			}	
			else if(item.type == 'python')
			{
				chart_input_sortable_add(baseID + '_input_content',true , true);
			}	
			else if(item.type == 'form')
			{
				chart_input_sortable_form_add(baseID + '_input_content',true , true);
			}
			else if(item.type == 'setform')
			{
				chart_input_sortable_form_add(baseID + '_input_content',true , true);
			}
			else
			{
				chart_input_sortable_add(baseID + '_input_content',true , true);
			}
			
			
			$('#' + baseID + '_input_content' + '_require_' + index).prop("checked", input_item.require);
			
			select2_put_value(baseID + '_input_content' + '_value_' + index , input_item.value);
			
			if(item.type == 'form')
			{
				select2_put_value(baseID + '_input_content' + '_name_' + index , input_item.name);
			}
			else if(item.type == 'setform')
			{
				select2_put_value(baseID + '_input_content' + '_name_' + index , input_item.name);
			}
			else
			{
				$('#' + baseID + '_input_content' + '_name_' + index).val(input_item.name);
			}

			$('#' + baseID + '_input_content' + '_des_' + index).val(input_item.des);
		});
		
		if('input1' in item.config)
		{
			item.config.input1.forEach(function(input_item, index)
			{
				chart_input_sortable_form_add(baseID + '1_input_content',true , true);
				select2_put_value(baseID + '1_input_content' + '_value_' + index , input_item.value);
				select2_put_value(baseID + '1_input_content' + '_name_' + index , input_item.name);
				$('#' + baseID + '1_input_content' + '_des_' + index).val(input_item.des);
			});
		}
		if('input2' in item.config)
		{
			item.config.input2.forEach(function(input_item, index)
			{
				chart_input_sortable_form_add(baseID + '2_input_content',true , true);
				select2_put_value(baseID + '2_input_content' + '_value_' + index , input_item.value);
				select2_put_value(baseID + '2_input_content' + '_name_' + index , input_item.name);
				$('#' + baseID + '2_input_content' + '_des_' + index).val(input_item.des);
			});
		}
	
	}
	
	function load_outside_option()
	{
		
	}
	function modal_save_input(baseID , item)
	{
		item.config.input = [];
		$('[id^=' + baseID + '_input_content' + '_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_input = new item_input_object();
			item_input.require = $('#' + my_id.replace('_li_','_require_')).is(":checked");
			item_input.name = $('#' + my_id.replace('_li_','_name_')).val();
			item_input.value = $('#' + my_id.replace('_li_','_value_')).val();
			item_input.des = $('#' + my_id.replace('_li_','_des_')).val();
			item.config.input.push(item_input);
		});
		if('input1' in item.config)
		{
			item.config.input1 = [];
			$('[id^=' + baseID + '1_input_content' + '_li_]').each(function()
			{
				var my_id = $(this).attr('id');
				var item_input1 = new item_input_object();
				item_input1.name = $('#' + my_id.replace('_li_','_name_')).val();
				item_input1.value = $('#' + my_id.replace('_li_','_value_')).val();
				item_input1.des = $('#' + my_id.replace('_li_','_des_')).val();
				item.config.input1.push(item_input1);
			});
		}
		if('input2' in item.config)
		{
			item.config.input2 = [];
			$('[id^=' + baseID + '2_input_content' + '_li_]').each(function()
			{
				var my_id = $(this).attr('id');
				var item_input2 = new item_input_object();
				item_input2.name = $('#' + my_id.replace('_li_','_name_')).val();
				item_input2.value = $('#' + my_id.replace('_li_','_value_')).val();
				item_input2.des = $('#' + my_id.replace('_li_','_des_')).val();
				item.config.input2.push(item_input2);
			});
		}
		
	}
	function modal_load_calculate(baseID , item)
	{
		item.config.calculate.forEach(function(calculate_item, index) 
		{
			chart_calculate_sortable_add(baseID + '_calculate_content');
			select2_put_value(baseID + '_calculate_content' + '_type_' + index , calculate_item.type);
			select2_put_value(baseID + '_calculate_content' + '_from_' + index , calculate_item.from);
			select2_put_value(baseID + '_calculate_content' + '_para1_' + index , calculate_item.para1);
			select2_put_value(baseID + '_calculate_content' + '_para2_' + index , calculate_item.para2);
			select2_put_value(baseID + '_calculate_content' + '_to_' + index , calculate_item.to);
		});
	}
	function modal_save_calculate(baseID , item)
	{
		item.config.calculate = [];
		$('[id^=' + baseID + '_calculate_content' + '_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_calculate = new item_calculate_object();
			item_calculate.type = $('#' + my_id.replace('_li_','_type_')).val();
			item_calculate.from = $('#' + my_id.replace('_li_','_from_')).val();
			item_calculate.para1 =$('#' + my_id.replace('_li_','_para1_')).val();
			item_calculate.para2 = $('#' + my_id.replace('_li_','_para2_')).val();
			item_calculate.to = $('#' + my_id.replace('_li_','_to_')).val();
			item.config.calculate.push(item_calculate);
		});
		
	}
	function modal_load_output(baseID , item)
	{
		item.config.output.forEach(function(output_item, index) 
		{
			if(item.type == 'form')
			{
				chart_output_sortable_add(baseID + '_output_content',true,false);
			}	
			else
			{
				chart_output_sortable_add(baseID + '_output_content',true,true);
			}
			select2_put_value(baseID + '_output_content' + '_value_' + index , output_item.value);
			select2_put_value(baseID + '_output_content' + '_name_' + index,output_item.name);
			$('#' + baseID + '_output_content' + '_des_' + index).val(output_item.des);
		});
	}
	function modal_save_output(baseID , item)
	{
		item.config.output = [];
		$('[id^=' + baseID + '_output_content' + '_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_output = new item_output_object();
			item_output.name = $('#' + my_id.replace('_li_','_name_')).val();
			item_output.value = $('#' + my_id.replace('_li_','_value_')).val();
			item_output.des =$('#' + my_id.replace('_li_','_des_')).val();
			item.config.output.push(item_output);
		});
	}
	
	function modal_load_subflow(baseID , item)
	{
		subflow_load(baseID + '_subflow_content');
		$('input[name=' + baseID + '_subflow_content' + '_radio' + '][value="' + item.config.subflow_id + '"]').prop('checked',true);
		subflow_load_change_event(baseID + '_subflow_content', item.config.subflow_id);
		
		item.config.subflow_input.forEach(function(input_item, index)
		{
			$('#' + baseID + '_subflow_content' + '_input_require_' + index).prop("checked", input_item.require);
			select2_put_value(baseID + '_subflow_content' + '_input_value_' + index , input_item.value);
		});
		
		item.config.subflow_output.forEach(function(output_item, index)
		{
			select2_put_value(baseID + '_subflow_content' + '_output_name_' + index , output_item.name);
		});
	}
	function modal_save_subflow(baseID , item)
	{

		item.config.subflow_id = $('input[type=radio][name=' + baseID + '_subflow_content' + '_radio' + ']:checked').val();

		item.config.subflow_input = [];
		$('[id^=' + baseID + '_subflow_content' + '_input_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_input = new item_input_object();
			item_input.require = $('#' + my_id.replace('_li_','_require_')).is(":checked");
			item_input.value = $('#' + my_id.replace('_li_','_value_')).val();
			item_input.name = $('#' + my_id.replace('_li_','_name_')).val();
			item.config.subflow_input.push(item_input);
		});
		
		item.config.subflow_output = [];
		$('[id^=' + baseID + '_subflow_content' + '_output_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_output = new item_output_object();
			item_output.value = $('#' + my_id.replace('_li_','_value_')).val();
			item_output.name = $('#' + my_id.replace('_li_','_name_')).val();
			item.config.subflow_output.push(item_output);
		});
	}
	
	function modal_load_outflow(baseID , item) //DELETE
	{	
		//$('#' + baseID + '_select_app').val(item.config.app_id).trigger('change');
		//$('#' + baseID + '_select_flow').val(item.config.flow_uuid).trigger('change');
		
		item.config.subflow_input.forEach(function(input_item, index)
		{
			$('#' + baseID + '_subflow_content' + '_input_require_' + index).prop("checked", input_item.require);
			select2_put_value(baseID + '_subflow_content' + '_input_value_' + index , input_item.value);
		});
		
		item.config.subflow_output.forEach(function(output_item, index)
		{
			select2_put_value(baseID + '_subflow_content' + '_output_name_' + index , output_item.name);
		});
	}
	function modal_save_outflow(baseID , item)
	{
		item.config.subflow_input = [];
		$('[id^=' + baseID + '_subflow_content' + '_input_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_input = new item_input_object();
			item_input.require = $('#' + my_id.replace('_li_','_require_')).is(":checked");
			item_input.value = $('#' + my_id.replace('_li_','_value_')).val();
			item_input.name = $('#' + my_id.replace('_li_','_name_')).val();
			item.config.subflow_input.push(item_input);
		});
		
		item.config.subflow_output = [];
		$('[id^=' + baseID + '_subflow_content' + '_output_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_output = new item_output_object();
			item_output.value = $('#' + my_id.replace('_li_','_value_')).val();
			item_output.name = $('#' + my_id.replace('_li_','_name_')).val();
			item.config.subflow_output.push(item_output);
		});
		
	}
	
	
	function modal_load_rule(baseID , item)
	{
		item.config.rules.forEach(function(rule_item, index) 
		{
			chart_rule_sortable_add(baseID + '_rule_content');
			$('#' + baseID + '_rule_content' + '_target_' + index).val(rule_item.target);
			select2_put_value(baseID + '_rule_content' + '_value1_' + index , rule_item.value1);
			select2_put_value(baseID + '_rule_content' + '_value2_' + index , rule_item.value2);
			select2_put_value(baseID + '_rule_content' + '_rule_' + index , rule_item.rule);
		});
	}
	function modal_load_rule_name(baseID , item)
	{
		var main_index = 0;
		item.config.rules.forEach(function(rule_item, index) 
		{
			
			chart_rule_name_sortable_add(baseID + '_rule_content');
			$('#' + baseID + '_rule_content' + '_target_' + index).val(rule_item.target);
			
			if(item.type == 'collection')
			{
				$('#' + baseID + '_rule_content' + '_targetR_' + index).prop('value',rule_item.target);
				if(rule_item.target == item.config.main )
				{
					$('input[name=' + baseID + '_rule_content' + '_targetR' + '][value="' + item.config.main + '"]').prop('checked',true);
				}
			}
		});
	}
	function modal_save_rule(baseID , item)
	{
		item.config.rules = [];
		$('[id^=' + baseID + '_rule_content' + '_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_rule = {};
			item_rule['target'] = $('#' + my_id.replace('_li_','_target_')).val();
			item_rule['value1'] = $('#' + my_id.replace('_li_','_value1_')).val();
			item_rule['value2'] = $('#' + my_id.replace('_li_','_value2_')).val();
			item_rule['rule'] = $('#' + my_id.replace('_li_','_rule_')).val();
			
			item.config.rules.push(item_rule);
		});
		
		if(item.type == 'collection')
		{
			item.config.main = $('input[type=radio][name=' + baseID + '_rule_content' + '_targetR' + ']:checked').val();
		}
	}
	
	/**
	 * link subflow array 
	 * input: [flowobject,flowobject...]
	 * return: 
	 * author:Pen Lin
	 */
	_self_.subflow = function(subflows)
	{
		flowobject.subflow = subflows;
	}
	/**
	 * link form object 
	 * input: formobject
	 * return: 
	 * author:Pen Lin
	 */
	_self_.form = function(formobject)
	{
		flowobject.form_object = formobject;

	}
	
	_self_.setFocus = function(obj_id)
	{
		
		item_select($('#' + active_id + '_' + 'chart_' + obj_id) , true);
	}
	
	/**
	 * create a new workflow item 
	 * input: item type:start , end , process , outside , select , async , collection
	 * return: 
	 * author:Pen Lin
	 */
	_self_.getName = function()
	{
		return flowobject.name;
	}
	_self_.setName = function(new_name)
	{
		flowobject.name = new_name;
	}
	_self_.getDes = function()
	{
		return flowobject.description;
	}
	_self_.setDes = function(new_des)
	{
		flowobject.description = new_des;
	}
	_self_.getUID = function()
	{
		return flowobject.uid;
	}
	_self_.setUID = function(new_uid)
	{
		flowobject.uid = new_uid;
	}
	/**
	 * create a new workflow item 
	 * input: item type:start , end , process , outside , select , async , collection
	 * return: 
	 * author:Pen Lin
	 */
	_self_.add_item = function(item_type)
	{
		var item = new item_object();
		flowobject.flow_item_counter++;
		item.id = "FITEM_" + flowobject.flow_item_counter;
		item.text = '';
		item.type = item_type;
		item.top = 0;
		item.left = 0;
		switch(item.type)
		{
			case 'start':
				item.text = gettext('開始');
				item.config = new start_object();
				break;
			case 'end':
				item.text = gettext('結束');
				item.config = new end_object();
				break;
			case 'python':
				item.text = gettext('執行');
				item.config = new python_object();		
				break;
			case 'subflow':
				item.text = gettext('子流程');
				item.config = new subflow_object();				
				break;
			case 'outflow':
				item.text = gettext('外部流程');
				item.config = new outflow_object();	
				break;
			case 'inflow':
				item.text = gettext('流程');
				item.config = new inflow_object();	
				break;
			case 'switch':
				item.text = gettext('判斷');
				item.config = new switch_object();	
				break;
			case 'form':
				item.text = gettext('人工輸入');
				item.config = new cform_object();	
				break;
			case 'setform':
				item.text = gettext('欄位設定');
				item.config = new setform_object();	
				break;
			case 'async':
				item.text = gettext('並行');
				item.config = new async_object();	
				break;
			case 'collection':
				item.text = gettext('匯集');
				item.config = new collection_object();	
				break;
			case 'sleep':
				item.text = gettext('暫停');
				item.config = new sleep_object();	
				break;
			case 'org1':
				item.text = gettext('同系職務');
				item.config = new org1_object();	
				break;
			case 'org2':
				item.text = gettext('部門職務');
				item.config = new org2_object();	
				break;
			
		}
		flowobject.items.push(item);
		item_create(item);
		
	}
	
	_self_.event_group_list = function(function_name)
	{
		event_get_group_list_callback = function_name;
	}
	_self_.event_user_list = function(function_name)
	{
		event_get_user_list_callback = function_name;
	}
	_self_.event_app_list = function(function_name)
	{
		event_get_app_list_callback = function_name;
	}
	_self_.event_flow_list = function(function_name)
	{
		event_get_flow_list_callback = function_name;
	}
	_self_.event_flowIO_list = function(function_name)
	{
		event_get_flowIO_list_callback = function_name;
	}
	
	_self_.event_my_flow_list = function(function_name)
	{
		event_get_my_flow_list_callback = function_name;
	}
	_self_.event_my_flowIO_list = function(function_name)
	{
		event_get_my_flowIO_list_callback = function_name;
	}
	/**
	 * get flow design by string
	 * input:
	 * return: string
	 * author:Pen Lin
	 */
	_self_.toString = function()
	{
		if(flowobject.is_sub == true)
		{
			var obj = JSON.parse(JSON.stringify(flowobject));
			obj.subflow = [];
			obj.form_object = {};
			return JSON.stringify(obj);
		}
		else
		{
			return JSON.stringify(flowobject);
		}
		
	}

	 /**
	 * return flowobject
	 * input:
	 * return: flowobject
	 * author:Pen Lin
	 */
	_self_.getObject = function()
	{
		if(flowobject.is_sub == true)
		{
			var obj = JSON.parse(JSON.stringify(flowobject));
			obj.subflow = [];
			obj.form_object = {};
			return obj;
		}
		else
		{
			return JSON.parse(JSON.stringify(flowobject));
		}
	}
	/**
	 * put flow design by string
	 * input: string
	 * return: true / false
	 * author:Pen Lin
	 */
	_self_.load = function(flow)
	{
		flowobject = JSON.parse(flow);
		//check and compare version
		if(!flowobject["version"])
		{
			flowobject["version"] = 000100000000;
		}
		flowobject.items.forEach(function(item, index, array)
		{
			if(item.type == 'start')
			{
				if(!item.config.hasOwnProperty("callable"))
				{
					item.config["callable"] = false;
				}
				if(!item.config.hasOwnProperty("subflow_id"))
				{
					item.config["subflow_id"] = '';
				}
				if(!item.config.hasOwnProperty("input"))
				{
					item.config["input"] = [];
				}
				if(!item.config.hasOwnProperty("output"))
				{
					item.config["output"] = [];
				}
				if(!item.config.hasOwnProperty("subflow_input"))
				{
					item.config["subflow_input"] = [];
				}
				if(!item.config.hasOwnProperty("subflow_output"))
				{
					item.config["subflow_output"] = [];
				}
			}
			else if(item.type == 'end')
			{
				if(!item.config.hasOwnProperty("output"))
				{
					item.config["output"] = [];
				}
				if(!item.config.hasOwnProperty("calculate"))
				{
					item.config["calculate"] = [];
				}
			}
			else if(item.type == 'subflow')
			{
				if(!item.config.hasOwnProperty("error_pass"))
				{
					item.config["error_pass"] = false;
				}
				if(!item.config.hasOwnProperty("log"))
				{
					item.config["log"] = false;
				}
				if(!item.config.hasOwnProperty("subflow_id"))
				{
					item.config["subflow_id"] = '';
				}
				if(!item.config.hasOwnProperty("subflow_input"))
				{
					item.config["subflow_input"] = [];
				}
				if(!item.config.hasOwnProperty("subflow_output"))
				{
					item.config["subflow_output"] = [];
				}
			}
			else if(item.type == 'python')
			{
				if(!item.config.hasOwnProperty("autoinstall"))
				{
					item.config["autoinstall"] = false;
				}
				if(!item.config.hasOwnProperty("error_pass"))
				{
					item.config["error_pass"] = false;
				}
				if(!item.config.hasOwnProperty("load_balance"))
				{
					item.config["load_balance"] = false;
				}
				if(!item.config.hasOwnProperty("log"))
				{
					item.config["log"] = false;
				}
				if(!item.config.hasOwnProperty("input"))
				{
					item.config["input"] = [];
				}
				if(!item.config.hasOwnProperty("output"))
				{
					item.config["output"] = [];
				}
				if(!item.config.hasOwnProperty("calculate"))
				{
					item.config["calculate"] = [];
				}
				if(!item.config.hasOwnProperty("code"))
				{
					item.config["code"] = '';
				}
			}
			else if(item.type == 'outflow')
			{
				if(!item.config.hasOwnProperty("error_pass"))
				{
					item.config["error_pass"] = false;
				}
				if(!item.config.hasOwnProperty("log"))
				{
					item.config["log"] = false;
				}
				if(!item.config.hasOwnProperty("app_name"))
				{
					item.config["app_name"] = '';
				}
				if(!item.config.hasOwnProperty("flow_name"))
				{
					item.config["flow_name"] = '';
				}
				if(!item.config.hasOwnProperty("subflow_input"))
				{
					item.config["subflow_input"] = [];
				}
				if(!item.config.hasOwnProperty("subflow_output"))
				{
					item.config["subflow_output"] = [];
				}
				
			}
			else if(item.type == 'inflow')
			{
				if(!item.config.hasOwnProperty("error_pass"))
				{
					item.config["error_pass"] = false;
				}
				if(!item.config.hasOwnProperty("log"))
				{
					item.config["log"] = false;
				}
				if(!item.config.hasOwnProperty("flow_name"))
				{
					item.config["flow_name"] = '';
				}
				if(!item.config.hasOwnProperty("subflow_input"))
				{
					item.config["subflow_input"] = [];
				}
				if(!item.config.hasOwnProperty("subflow_output"))
				{
					item.config["subflow_output"] = [];
				}
				
			}
			else if(item.type == 'switch')
			{
				if(!item.config.hasOwnProperty("calculate"))
				{
					item.config["calculate"] = [];
				}
				if(!item.config.hasOwnProperty("rules"))
				{
					item.config["rules"] = [];
				}
			}
			else if(item.type == 'form')
			{
				if(!item.config.hasOwnProperty("calculate"))
				{
					item.config["calculate"] = [];
				}
				if(!item.config.hasOwnProperty("input"))
				{
					item.config["input"] = [];
				}
				if(!item.config.hasOwnProperty("input1"))
				{
					item.config["input1"] = [];
				}
				if(!item.config.hasOwnProperty("input2"))
				{
					item.config["input2"] = [];
				}
				if(!item.config.hasOwnProperty("output"))
				{
					item.config["output"] = [];
				}
				if(!item.config.hasOwnProperty("cform_object"))
				{
					item.config["cform_object"] = null;
				}
				if(!item.config.hasOwnProperty("subflow_id"))
				{
					item.config["subflow_id"] = '';
				}
				if(!item.config.hasOwnProperty("subflow_input"))
				{
					item.config["subflow_input"] = [];
				}
				if(!item.config.hasOwnProperty("subflow_output"))
				{
					item.config["subflow_output"] = [];
				}
				
				if(!item.config.hasOwnProperty("log"))
				{
					item.config["log"] = false;
				}
				if(!item.config.hasOwnProperty("action1"))
				{
					item.config["action1"] = false;
				}
				if(!item.config.hasOwnProperty("action2"))
				{
					item.config["action2"] = false;
				}
				if(!item.config.hasOwnProperty("action1_text"))
				{
					item.config["action1_text"] = '';
				}
				if(!item.config.hasOwnProperty("action2_text"))
				{
					item.config["action2_text"] = '';
				}
			}
			else if(item.type == 'setform')
			{
				if(!item.config.hasOwnProperty("calculate"))
				{
					item.config["calculate"] = [];
				}
				if(!item.config.hasOwnProperty("input"))
				{
					item.config["input"] = [];
				}
				if(!item.config.hasOwnProperty("output"))
				{
					item.config["output"] = [];
				}
				if(!item.config.hasOwnProperty("log"))
				{
					item.config["log"] = false;
				}
				
			}
			else if(item.type == 'async')
			{
				if(!item.config.hasOwnProperty("rules"))
				{
					item.config["rules"] = [];
				}
			}
			else if(item.type == 'collection')
			{
				if(!item.config.hasOwnProperty("main"))
				{
					item.config["main"] = '';
				}
				if(!item.config.hasOwnProperty("rules"))
				{
					item.config["rules"] = [];
				}
			}
			else if(item.type == 'sleep')
			{
				if(!item.config.hasOwnProperty("msec"))
				{
					item.config["msec"] = 5000;
				}
				if(!item.config.hasOwnProperty("require"))
				{
					item.config["require"] = false;
				}
				if(!item.config.hasOwnProperty("value"))
				{
					item.config["value"] = null;
				}
			}
		});
		
		flowobject.items.forEach(function(item, index, array)
		{
			if(item.type == 'line')
			{
				line_create(item);
				line_renew(item);
			}
			else
			{
				item_create(item);
			}
		});
	}
	/**
	 * object selected call back
	 * input: function
	 * return: 
	 * author:Pen Lin
	 */
	_self_.event_chart_selected = function(function_name)
	{
		event_chart_selected_callback = function_name;
	}
	//====================
	//===object definition
	//====================

	/**
	 * inside object definition    -- start
	 * author:Pen Lin
	 */
	function flow_object()
	{
		var output = {};
		output["version"] = 000100000000;
		output["flow_item_counter"] = 0;
		output["flow_line_counter"] = 0;
		output["uid"] = 0;
		output["form_object"] = {};
		output.form_object.items = [];
		output["is_sub"] = false;
		output["subflow"] = []; //flowobject
		output["items"] = [];
		return output;
	}
	function item_object()
	{
		var output = {};
		var config = {};
		output["id"] = '';
		output["type"] = '';
		output["text"] = '';
		output["left"] = 0;
		output["top"] = 0;
		output["config"] = config;

		return output;
	}
	function item_input_object()
	{
		var output = {};

		output["require"] = false;
		output["value"] = '';
		output["name"] = '';
		output["des"] = '';

		return output;
	}
	function item_output_object()
	{
		var output = {};
		output["value"] = '';
		output["name"] = '';
		output["des"] = '';
		return output;
	}
	function item_calculate_object()
	{
		var output = {};
		output["type"] = '';
		output["from"] = '';
		output["para1"] = '';
		output["para2"] = '';
		output["to"] = '';
		return output;
	}
	function line_object()
	{
		var output = {};
		var config = {};
		
		output["id"] = '';
		output["type"] = '';
		
		config["target_side"] = '';
		config["source_side"] = '';
		config["target_item"] = '';
		config["source_item"] = '';
		config["idcounter"] = 0;
		config["linebox_left"] = 0;
		config["linebox_top"] = 0;
		config["linebox_long"] = 0;
		config["linebox_top_width"] = 0;
		config["linebox_bottom_width"] = 0;
		config["linebox_arrow_top"] = 0;
		config["linebox_arrow_left"] = 0;
		
		output["config"] = config;
		
		return output;
	}
	function start_object()
	{

		var output = {};
		//output["error_pass"] = false;
		//output["load_balance"] = false;
		//output["log"] = '';
		output["callable"] = false;
		output["subflow_id"] = '';
		output["input"] = [];
		output["output"] = [];		
		output["subflow_input"] = [];
		output["subflow_output"] = [];

		
		return output;
	}
	function end_object()
	{
		var output = {};
		output["output"] = [];	
		output["calculate"] = [];
		return output;
	}
	function python_object()
	{
		var output = {};
		output["autoinstall"] = false;
		output["error_pass"] = false;
		output["load_balance"] = false;
		output["log"] = true;
		output["input"] = [];
		output["output"] = [];	
		output["calculate"] = [];
		output["code"] = '';
		return output;
	}
	function subflow_object()
	{
		var output = {};
		output["error_pass"] = false;
		//output["load_balance"] = false;
		output["log"] = true;
		output["subflow_id"] = '';	
		output["subflow_input"] = [];
		output["subflow_output"] = [];
		return output;
	}
	function outflow_object()
	{
		var output = {};
		output["error_pass"] = false;
		//output["load_balance"] = false;
		output["log"] = true;
		output["app_name"] = '';	
		output["flow_name"] = '';	
		output["subflow_input"] = [];
		output["subflow_output"] = [];
		return output;
	}
	function inflow_object()
	{
		var output = {};
		output["error_pass"] = false;
		//output["load_balance"] = false;
		output["log"] = true;
		output["flow_name"] = '';	
		output["subflow_input"] = [];
		output["subflow_output"] = [];
		return output;
	}
	function switch_object()
	{
		var output = {};
		output["calculate"] = [];
		output["rules"] = []; //id,value1,value2m,rule
		output["log"] = true;
		return output;
	}
	function cform_object()
	{
		var output = {};
		output["calculate"] = [];
		output["input"] = [];
		output["input1"] = [];
		output["input2"] = [];
		output["action1"] = false;
		output["action1_text"] = '';
		output["action2"] = false;
		output["action2_text"] = '';
		output["output"] = [];	
		output["form_object"] = null;
		//output["form_setdata"] = [];
		output["subflow_id"] = '';	
		output["subflow_input"] = [];
		output["subflow_output"] = [];
		output["log"] = true;
		return output;
	}
	function setform_object()
	{
		var output = {};
		output["calculate"] = [];
		output["input"] = [];
		output["output"] = [];	
		output["log"] = true;
		return output;
	}
	function async_object()
	{
		var output = {};
		output["rules"] = [];
		output["log"] = true;
		return output;
	}
	function collection_object()
	{
		var output = {};
		output["main"] = '';
		output["rules"] = [];
		output["log"] = true;
		return output;
	}
	function sleep_object()
	{
		var output = {};
		output["msec"] = 5000;
		output["require"] = false;
		output["value"] = null;
		return output;
	}
	function org1_object()
	{
		var output = {};
		output["input"] = [{'require':true,'value':'','name':'role','des':'職務名稱'},{'require':true,'value':'','name':'user_no','des':'使用者編號'}];
		output["output"] = [{'value':'$(dept_no)','name':'','des':'部門編號'},{'value':'$(user_no)','name':'','des':'使用者編號'}];	
		return output;
	}
	function org2_object()
	{
		var output = {};
		output["input"] = [{'require':true,'value':'','name':'dept_no','des':'部門編號'},{'require':true,'value':'','name':'role_name','des':'職務名稱'}];
		output["output"] = [{'value':'$(dept_no)','name':'','des':'部門編號'},{'value':'$(user_no)','name':'','des':'使用者編號'}];		
		return output;
	}
	
	
	/**
	 * flow option maker for select2
	 * input: ul_id , form_include=true , value_include=true
	 * return: select's options in workflow output var 
	 */
	function chart_input_sortable_add(ul_id,form_include,value_include)
	{
		//org1_chart_modal  => check
		//org2_chart_modal
		
		//ul_id already have activeid and chart id
		var top_id = ul_id;
		var baseID = top_id.replace('_input_content','');
		var item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="2%"><span class="fa fa-arrows-v"></span></td>'
						+'<td width="8%" nowrap><input id="' + top_id + '_require__index_" type="checkbox" class="icheckbox_minimal-blue" ><label id="' + top_id + '_requirestyle__index_" for="' + top_id + '_require__index_"></label> '+gettext('必填')+'</td>'
						+'<td width="28%"><select id="' + top_id + '_value__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="28%"><input id="' + top_id + '_name__index_" type="text" class="form-control " placeholder="'+gettext('變數名稱')+'"></td>'
						+'<td width="30%"><input id="' + top_id + '_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'"></td>'
						+'<td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + top_id + '_li__index_"></i></td>'
						+'</tr></table>'
						+'</li>';
						
		if((ul_id.indexOf('org1_chart_modal') > 0)||(ul_id.indexOf('org2_chart_modal') > 0 ))
		{
			item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="2%"></td>'
						+'<td width="2%" nowrap><input id="' + top_id + '_require__index_" type="checkbox" class="icheckbox_minimal-blue" style="display:none">' + '</td>'
						+'<td width="31%"><select id="' + top_id + '_value__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="31%"><input id="' + top_id + '_name__index_" type="text" class="form-control " placeholder="'+gettext('變數名稱')+'" readonly></td>'
						+'<td width="30%"><input id="' + top_id + '_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
						+'<td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + top_id + '_li__index_" style="display:none"></i></td>'
						+'</tr></table>'
						+'</li>';
		}
						
		var newindex = 0;
		while($( '#' + top_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}
		
		$( '#' + top_id ).append(item_li_content.replace(/_index_/g,newindex));
		
		//read form field to select2
		var options = '';
		if(form_include)
		{
			options += select_option_form();
		}	
		if(value_include)
		{
			options += select_option_value();
		}
		$( '#' + top_id  + '_value_' + newindex).html( options );
		//select2 enable
		$( '#' + top_id  + '_value_' + newindex).select2({tags: true,placeholder: gettext('輸入資料'),allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
		$( '#' + top_id  + '_value_' + newindex).val(null).trigger('change');
		
		//remove event
		$('#remove_' + top_id + '_li_' + newindex ).click(function()
		{
			var get_li_id =  $( this ).attr('id').replace('remove_','');
			$('#' + get_li_id ).remove();
		});
		
		return newindex;
	}
	function chart_input_sortable_form_add(ul_id)
	{
		//ul_id already have activeid and chart id
		var top_id = ul_id;
		var item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="2%"><span class="fa fa-arrows-v"></span></td>'
						+'_require_input_'
						+'<td width="_require_td_%"><select id="' + top_id + '_value__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="28%"><select id="' + top_id + '_name__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="30%"><input id="' + top_id + '_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'"></td>'
						+'<td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + top_id + '_li__index_"></i></td>'
						+'</tr></table>'
						+'</li>';
						
		var require_checkbox = '<td width="8%" nowrap><input id="' + top_id + '_require__index_" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + top_id + '_require__index_"></label> '+gettext('必填')+'</td>';
		var newindex = 0;
		while($( '#' + top_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}
		
		if(top_id == baseID_FORM + '1_input_content')
		{
			item_li_content = item_li_content.replace(/_require_input_/g,'').replace(/_require_td_/g,'36%');
		}
		if(top_id == baseID_FORM + '2_input_content')
		{
			item_li_content = item_li_content.replace(/_require_input_/g,'').replace(/_require_td_/g,'36%');
		}
		else
		{
			item_li_content = item_li_content.replace(/_require_input_/g,require_checkbox).replace(/_require_td_/g,'28%');
			
		}
		
		$( '#' + top_id ).append(item_li_content.replace(/_index_/g,newindex));
		
		$( '#' + top_id  + '_value_' + newindex).html( select_option_value );
		$( '#' + top_id  + '_name_' + newindex).html( select_option_form );
		//select2 enable
		$( '#' + top_id  + '_value_' + newindex).select2({tags: true,placeholder: gettext('輸入資料'),allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
		$( '#' + top_id  + '_value_' + newindex).val(null).trigger('change');
		$( '#' + top_id  + '_name_' + newindex).select2({tags: false,placeholder: gettext('設定欄位'),allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
		$( '#' + top_id  + '_name_' + newindex).val(null).trigger('change');
		
		//remove event
		$('#remove_' + top_id + '_li_' + newindex ).click(function()
		{
			var get_li_id =  $( this ).attr('id').replace('remove_','');
			$('#' + get_li_id ).remove();
		});

		return newindex;
	}
	function chart_calculate_sortable_add(ul_id)
	{
		var top_id = ul_id;
		var availableTagsForm = select_option_form();
		var availableTagsValue = select_option_value();
		var availableTags = availableTagsForm + availableTagsValue;
		var baseID = top_id.replace('_calculate_content','');	
		var calculate_item = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
					+ '<table width="100%"><tr><td width="4%"><span class="fa fa-arrows-v"></span></td>'
					+'<td width="30%"><select id="' + top_id + '_type__index_" class="form-control select2" style="width:100%">'
					+'<option value="--">--</option>'
					+'<option value="upper">'+gettext('轉成大寫')+'</option>'
					+'<option value="lower">'+gettext('轉成小寫')+'</option>'
					+'<option value="replace">'+gettext('取代')+'</option>'
					+'<option value="len">'+gettext('取得長度')+'</option>'
					+'<option value="strip">'+gettext('去除前後空白')+'</option>'
					+'<option value="startwith">'+gettext('取開頭字元')+'</option>'
					+'<option value="endof">'+gettext('取後面字元')+'</option>'
					+'<option value="substring">'+gettext('擷取字元')+'</option>'
					+'<option value="string">'+gettext('轉成字串')+'</option>'
					+'<option value="add">'+gettext('字串相加')+'</option>'
					+'<option value="num+">'+gettext('數字相加')+'</option>'
					+'<option value="num-">'+gettext('數字相減')+'</option>'
					+'<option value="num*">'+gettext('數字相成')+'</option>'
					+'<option value="num/">'+gettext('數字相除')+'</option>'
					+'<option value="num_mod">'+gettext('數字取餘數')+'</option>'
					+'<option value="form_creater">'+gettext('開單人')+'</option>'
					+'<option value="form_creater_group">'+gettext('開單人群組')+'</option>'
					+'<option value="get_user_group">'+gettext('使用者所屬群組')+'</option>'
					+'<option value="get_user_name">'+gettext('使用者名稱')+'</option>'
					+'<option value="get_group_name">'+gettext('群組名稱')+'</option>'
					+'<option value="sys_parameter">'+gettext('系統參數')+'</option>'
					+'</select></td>'
					+'<td width="14%"><select id="' + top_id + '_from__index_" class="form-control select2" style="width:100%"></td>'
					+'<td width="16%"><select id="' + top_id + '_para1__index_" class="form-control select2" style="width:100%"></td>'
					+'<td width="16%"><select id="' + top_id + '_para2__index_" class="form-control select2" style="width:100%"></td>'
					+'<td width="16%"><select id="' + top_id + '_to__index_" class="form-control select2" style="width:100%"></td>'
					+'<td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + top_id + '_li__index_"></i></td>'
					+'</tr></table></li>';
		
		var newindex = 0;
		while($( '#' + top_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}
		
		$('#' + top_id ).append(calculate_item.replace(/_index_/g,newindex));
		$('#' + top_id + '_type_' + newindex).select2();
		$('#' + top_id + '_from_' + newindex).select2({tags: false,dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
		$('#' + top_id + '_from_' + newindex).attr('disabled', true);
		$('#' + top_id + '_from_' + newindex).html(availableTags); 
		$('#' + top_id + '_from_' + newindex).val(null).trigger('change');
		$('#' + top_id + '_para1_' + newindex).select2({tags: true,dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
		$('#' + top_id + '_para1_' + newindex).attr('disabled', true);
		$('#' + top_id + '_para1_' + newindex).html(availableTags); 
		$('#' + top_id + '_para1_' + newindex).val(null).trigger('change');
		$('#' + top_id + '_para2_' + newindex).select2({tags: true,dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
		$('#' + top_id + '_para2_' + newindex).attr('disabled', true);
		$('#' + top_id + '_para2_' + newindex).html(availableTags); 
		$('#' + top_id + '_para2_' + newindex).val(null).trigger('change');;
		$('#' + top_id + '_to_' + newindex).select2({tags: true,dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
		$('#' + top_id + '_to_' + newindex).attr('disabled', true);
		$('#' + top_id + '_to_' + newindex).html(availableTagsValue);
		$('#' + top_id + '_to_' + newindex).val(null).trigger('change');;

		//綁定option change 事件
		$('#' + top_id + '_type_' + newindex ).change(function()
		{
			
			//變動時，同時清空所選的值，更改placeholder 以及 disable (抓取ID動作)
			var changeID = this.id;
			var changeValue = $('#' + this.id).val();
			var object_from = $('#' + changeID.replace('_type_','_from_'));
			var object_para1 = $('#' + changeID.replace('_type_','_para1_'));
			var object_para2 = $('#' + changeID.replace('_type_','_para2_'));
			var object_to = $('#' + changeID.replace('_type_','_to_'));
			
			object_from.html(availableTags); 
			object_para1.html(availableTags);
			object_para2.html(availableTags);
			object_to.html(availableTagsValue);
			object_from.select2({placeholder : gettext("來源"),dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			object_to.select2({tags: true,placeholder : gettext("結果"),dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}},
								createTag: function(params) 
								{
									var term = $.trim(params.term);

									if (term == '') 
									{
									  return null;
									}
									
									if ((term.startsWith(gettext('變數:'))))
									{
										term = term.substring(3);
									}
									
									return {
									  id: '$(' + term + ')',
									  text: gettext('變數:') + term,
									  newTag: true // add additional parameters
									}
								}});
			object_from.val(null).trigger('change');
			object_to.val(null).trigger('change');
			object_para1.val(null).trigger('change');
			object_para2.val(null).trigger('change');
				
			if((changeValue == 'upper')||(changeValue == 'lower')||(changeValue == 'len')||(changeValue == 'strip')||(changeValue == 'number')||(changeValue == 'string')||(changeValue == '')||(changeValue == 'write'))
			{
				object_para1.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', true);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if(changeValue == 'form_creater')
			{
				object_para1.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', true);
				object_para1.attr('disabled', true);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if(changeValue == 'form_creater_group')
			{
				object_para1.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', true);
				object_para1.attr('disabled', true);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if((changeValue == 'get_user_group')||(changeValue == 'get_user_name')||(changeValue == 'get_group_name'))
			{
				object_para1.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', true);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if(changeValue == 'sys_parameter')
			{
				object_para1.select2({tags: true,placeholder : gettext("參數名"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', true);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if(changeValue == '--')
			{
				object_from.select2({placeholder : "",dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
				object_to.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para1.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', true);
				object_para1.attr('disabled', true);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', true);
			}
			else if(changeValue == 'replace')
			{
				object_para1.select2({tags: true,placeholder : gettext("尋找"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : gettext("換成"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', false);
				object_to.attr('disabled', false);
			}
			else if((changeValue == 'startwith')||(changeValue == 'endof'))
			{
				object_para1.select2({tags: true,placeholder : gettext("字數"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if(changeValue == 'substring')
			{
				object_para1.select2({tags: true,placeholder : gettext("第幾個字"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : gettext("取幾個字"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', false);
				object_to.attr('disabled', false);
			}
			else if((changeValue == 'add')||(changeValue == 'num+'))
			{
				object_para1.select2({tags: true,placeholder : gettext("加上"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if(changeValue == 'num-')
			{
				object_para1.select2({tags: true,placeholder : gettext("減去"), language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "", language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if(changeValue == 'num*')
			{
				object_para1.select2({tags: true,placeholder : gettext("乘上"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			else if((changeValue == 'num/')||(changeValue == 'num_mod'))
			{
				object_para1.select2({tags: true,placeholder : gettext("除以"),dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_para2.select2({tags: true,placeholder : "",dropdownAutoWidth: true,allowClear: true, language: {noResults: function (params) {return " ";}}});
				object_from.attr('disabled', false);
				object_para1.attr('disabled', false);
				object_para2.attr('disabled', true);
				object_to.attr('disabled', false);
			}
			
		});
		//綁定option change 事件 , update from and to options
		$('#' + top_id + '_to_' + newindex ).change(function()
		{
			var new_option = [];
			//開始掃描 TO (全部value)放入陣列
			$('[id^=' + top_id + '_to_]').each(function()
			{
				var item_value = $(this).val();
				if(new_option.indexOf(item_value) < 0)
				{
					if(item_value != null)
					{
						if(item_value.startsWith('$(') && item_value.endsWith(')')) //only value
						{
							new_option.push(item_value);
						}
					}
				}
			});
			new_option.forEach(function(item, item_index, array) 
			{
				var item_text = '';
				item_text = item.substring(2);
				item_text = item_text.substring(0,item_text.length -1);
				$('[id^=' + top_id + '_from_]').each(function()
				{
					select2_new_option( $(this).attr('id'),item,gettext('變數:') + item_text );
				});
				$('[id^=' + top_id + '_para1_]').each(function()
				{
					select2_new_option( $(this).attr('id'),item,gettext('變數:') + item_text );
				});
				$('[id^=' + top_id + '_para2_]').each(function()
				{
					select2_new_option( $(this).attr('id'),item,gettext('變數:') + item_text );
				});
				$('[id^=' + top_id + '_to_]').each(function()
				{
					select2_new_option( $(this).attr('id'),item,gettext('變數:') + item_text );
				});
				
				$('[id^="' + baseID + '_input_content_value_"]').each(function(i)
				{
					select2_new_option( $(this).attr('id'),item,gettext('變數:') + item_text );
				});
				$('[id^="' + baseID + '_rule_content_value1_"]').each(function(i)
				{
					select2_new_option( $(this).attr('id'),item,gettext('變數:') + item_text );
				});
				//_rule_content_value2_
				$('[id^="' + baseID + '_rule_content_value2_"]').each(function(i)
				{
					select2_new_option( $(this).attr('id'),item,gettext('變數:') + item_text );
				});
			});
		});
		//remove event
		$('#remove_' + top_id + '_li_' + newindex ).click(function()
		{
			var get_li_id =  $( this ).attr('id').replace('remove_','');
			$('#' + get_li_id ).remove();
		});
	}
	function chart_output_sortable_add(ul_id,form_include,value_include) 
	{
		//ul_id already have activeid and chart id
		var top_id = ul_id;
		var baseID = top_id.replace('_output_content','');
		var item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="4%"><span class="fa fa-arrows-v"></span></td>'
						+'<td width="32%"><select id="' + top_id + '_value__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="30%"><select id="' + top_id + '_name__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="30%"><input id="' + top_id + '_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'"></td>'
						+'<td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + top_id + '_li__index_"></i></td>'
						+'</tr></table>'
						+'</li>';
		
		if((ul_id.indexOf('org1_chart_modal') > 0)||(ul_id.indexOf('org2_chart_modal') > 0 ))
		{
			item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="4%"></span></td>'
						+'<td width="32%"><select id="' + top_id + '_value__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="30%"><select id="' + top_id + '_name__index_" class="form-control select2" style="width:100%"></select></td>'
						+'<td width="30%"><input id="' + top_id + '_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
						+'<td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + top_id + '_li__index_" style="display:none"></i></td>'
						+'</tr></table>'
						+'</li>';
						
		}

		var newindex = 0;
		while($( '#' + top_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}
		
		$( '#' + top_id ).append(item_li_content.replace(/_index_/g,newindex));
		
		if((ul_id.indexOf('org1_chart_modal') > 0)||(ul_id.indexOf('org2_chart_modal') > 0 ))
		{
			
			$( '#' + top_id  + '_value_' + newindex).select2({tags: false , placeholder: '',readonly: true , allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			$( '#' + top_id  + '_value_' + newindex).prop("disabled", true);
		}
		var options = '';
		if(form_include)
		{
			options += select_option_form();
		}	
		if(value_include)
		{
			options += select_option_value();
		}
		//read form field to select2
		$( '#' + top_id  + '_value_' + newindex).html(options);
		$( '#' + top_id  + '_name_' + newindex).html(select_option_value);
		//select2 enable
		$( '#' + top_id  + '_value_' + newindex).select2({tags: false , placeholder: gettext('輸入資料'), allowClear: true , dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
		$( '#' + top_id  + '_value_' + newindex).val(null).trigger('change');
		$( '#' + top_id  + '_name_' + newindex).select2({tags: true , placeholder: gettext('變數名稱'), allowClear: true , dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}, 
								createTag: function(params) 
								{
									var term = $.trim(params.term);

									if (term == '') 
									{
									  return null;
									}
									
									if ((term.startsWith(gettext('變數:'))))
									{
										term = term.substring(3);
									}
									
									return {
									  id: '$(' + term + ')',
									  text: gettext('變數:') + term,
									  newTag: true // add additional parameters
									}
								}});
		$( '#' + top_id  + '_name_' + newindex).val(null).trigger('change');
		//remove event
		$('#remove_' + top_id + '_li_' + newindex ).click(function()
		{
			var get_li_id =  $( this ).attr('id').replace('remove_','');
			$('#' + get_li_id ).remove();
		});
	}
	
	function chart_rule_sortable_add(ul_id)
	{
		var top_id = ul_id;

		var item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="25%"><input id="' + top_id + '_target__index_" type="text" class="form-control " placeholder="'+gettext('到')+'" readonly></td>'
						+'<td width="25%"><select id="' + top_id + '_value1__index_" class="form-control select2" placeholder="'+gettext('變數')+'" style="width:100%"></select></td>'
						+'<td width="25%"><select id="' + top_id + '_rule__index_" class="form-control select2" placeholder="'+gettext('條件')+'" style="width:100%"></select></td>'
						+'<td width="25%"><select id="' + top_id + '_value2__index_" class="form-control select2" placeholder="'+gettext('變數')+'" style="width:100%"></select></td>'
						+'</tr></table>'
						+'</li>';
						
		var newindex = 0;
		while($( '#' + top_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}

		$( '#' + top_id ).append(item_li_content.replace(/_index_/g,newindex));
		
		//read form field to select2
		$( '#' + top_id  + '_value1_' + newindex).html(select_option_form() + select_option_value());
		$( '#' + top_id  + '_value2_' + newindex).html(select_option_form() + select_option_value());
		$( '#' + top_id  + '_rule_' + newindex).html('<option value="=">'+gettext('相等')+'</option><option value="!=">'+gettext('不相等')+'</option><option value=">">'+gettext('大於')+'</option><option value="<">'+gettext('小於')+'</option>');
		//select2 enable
		$( '#' + top_id  + '_value1_' + newindex).select2({tags: true,placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
		$( '#' + top_id  + '_value2_' + newindex).select2({tags: true,placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});

	}
	function chart_rule_name_sortable_add(ul_id)
	{
		var top_id = ul_id;
		var item_li_content = '';
		if(top_id.startsWith(baseID_ASYNC))
		{
			item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="20%">'+gettext('前往:')+'</td>'
						+'<td width="80%"><input id="' + top_id + '_target__index_" type="text" class="form-control " placeholder="'+gettext('到')+'" readonly></td>'
						+'</tr></table>'
						+'</li>';
		}
		else if(top_id.startsWith(baseID_COLLECTION))
		{
			item_li_content = '<li id="' + top_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
						+'<table width="100%"><tr>'
						+'<td width="20%"><input id="' + top_id + '_targetR__index_" name="' + top_id + '_targetR' + '" type="radio" class="iradio_minimal-blue" value=""><label for="' + top_id + '_targetR__index_"></label>'+gettext('主線')+'</td>'
						+'<td width="20%">'+gettext('來自:')+'</td>'
						+'<td width="60%"><input id="' + top_id + '_target__index_" type="text" class="form-control " placeholder="'+gettext('到')+'" readonly></td>'
						+'</tr></table>'
						+'</li>';
		}
		
		var newindex = 0;
		while($( '#' + top_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}

		$( '#' + top_id ).append(item_li_content.replace(/_index_/g,newindex));
	}
	
	
	/**
	 * flow option maker for select2
	 * input: 
	 * return: select's options in workflow output var 
	 */
	function select_option_form()
	{
		var output = '';
		if(flowobject.form_object != null)
		{
			if(flowobject.form_object.items != null)
			{
				flowobject.form_object.items.forEach(function(item, index, array) 
				{
					if(item.type.startsWith('box'))
					{

					}
					else
					{
						if(item.type == 'h_group')
						{
							var option = '<option value="#G1(' + item.id + ')">'+gettext('欄位:') + item.config.group_title + '</option>'
										+ '<option value="#G2(' + item.id + ')">'+gettext('欄位:') + item.config.user_title + '</option>';
							output = output + option;
							
						}
						else
						{
							var option = '<option value="#(' + item.id + ')">'+gettext('欄位:') + item.config.title + '</option>';
							output = output + option;
						}
					}
				});
			}
		}
		
		return output;
	}
	/**
	 * flow option maker for select2
	 * input: baseID , if null , don't care caculate
	 * return: select's options in workflow output var 
	 */
	function select_option_value()
	{
		var output = '';
		flowobject.items.forEach(function(item, index)
		{
			if((item.type == 'start')) //start's input include
			{
				item.config.input.forEach(function(input_item, index)
				{

					var option = '<option value="$(' + input_item.name + ')">'+gettext('變數:')+ input_item.name + '</option>';
					if(output.indexOf(option) < 0)
					{
						output = output + option;
					}

				});
			}

			if('output' in item.config)
			{
				item.config.output.forEach(function(output_item, index)
				{
					var item_text = '';
					if(output_item.name != null)
					{
						if(output_item.name.startsWith('$('))
						{
							item_text = output_item.name.substring(2);
							item_text = item_text.substring(0,item_text.length -1);
						}
						else
						{
							item_text = output_item.name;
						}
						
						var option = '<option value="$(' + item_text + ')">'+gettext('變數:') + item_text + '</option>';
						if(output.indexOf(option) < 0)
						{
							output = output + option;
						}
					}
				});
			}
			if('subflow_output' in item.config)
			{
				item.config.subflow_output.forEach(function(output_item, index)
				{
					var item_text = '';
					if(output_item.name != null)
					{
						if(output_item.name.startsWith('$('))
						{
							item_text = output_item.name.substring(2);
							item_text = item_text.substring(0,item_text.length -1);
						}
						else
						{
							item_text = output_item.name;
						}
						
						var option = '<option value="$(' + item_text + ')">'+gettext('變數:')+ item_text + '</option>';
						if(output.indexOf(option) < 0)
						{
							output = output + option;
						}
					}
				});
			}
			
		});

		return output;
	}

	
	
	function select2_new_option(obj_id , item_value , item_text)
	{
		var tmp = $('#' + obj_id).val(); 
		//check exist
		if ($('#'+ obj_id).html().indexOf('value="' + item_value + '"') <= 0)
		{
			$('#' + obj_id).append(new Option(item_text , item_value , false , false));
		}
		$('#' + obj_id).val(tmp);
	}
	/**
	 * load All subflow name and id
	 * input: a ul content
	 * return: No Return 
	 */
	function subflow_load(ul_id)
	{
		$( '#' + ul_id ).html("");
		
		var subflow_item = '<li class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
					+'<table width="100%"><tr><td width="4%"><input type="radio" class="iradio_minimal-blue" id="_id_" value="_value_" name="' + ul_id + '_radio" value="_value_"><label for="_id_"></label></td>'
					+'<td width="40%">_name_</td>'
					+'<td width="56%">_des_</td>'
					+'</tr></table></li>';
					
		$( '#' + ul_id ).append(subflow_item.replace(/_value_/g,"0")
											.replace(/_id_/g, ul_id + '_radio_0')
											.replace(/_name_/g,gettext("不執行"))
											.replace(/_des_/g,gettext("說明"))
											);

		flowobject.subflow.forEach(function(flowobject_item, index)
		{
			$( '#' + ul_id ).append(subflow_item.replace(/_value_/g,flowobject_item.uid)
												.replace(/_id_/g, ul_id + '_radio_' + (index+1))
												.replace(/_name_/g,flowobject_item.name)
												.replace(/_des_/g,flowobject_item.description)
												);
		});
		
		$('input[type=radio][name=' + ul_id + '_radio' + ']').change(function() 
		{
			subflow_load_change_event(ul_id, new Number(this.value));

		});
		
	}
	function subflow_load_change_event(ul_id , select_value)
	{
		$( '#' + ul_id + '_input' ).html("");
		$( '#' + ul_id + '_output').html("");
		var item_li_input_content = '<li id="' + ul_id + '_input_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
					+'<table width="100%"><tr>'
					+'<td width="2%"><span class="fa fa-arrows-v"></span></td>'
					+'<td width="8%" nowrap><input id="' + ul_id + '_input_require__index_" type="checkbox" class="icheckbox_minimal-blue"><label for="' + ul_id + '_input_require__index_" readonly></label> '+gettext('必填')+'</td>'
					+'<td width="30%"><select id="' + ul_id + '_input_value__index_" class="form-control select2" placeholder="'+gettext('輸入資料')+'" style="width:100%"></select></td>'
					+'<td width="30%"><select id="' + ul_id + '_input_name__index_" type="text" class="form-control " placeholder="'+gettext('變數名稱')+'" style="width:100%" readonly></select></td>'
					+'<td width="30%"><input id="' + ul_id + '_input_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
					+'</tr></table>'
					+'</li>';
		var item_li_output_content = '<li id="' + ul_id + '_output_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
					+'<table width="100%"><tr>'
					+'<td width="4%"><span class="fa fa-arrows-v"></span></td>'
					+'<td width="32%"><select id="' + ul_id + '_output_value__index_" type="text" class="form-control " placeholder="'+gettext('輸出值')+'" style="width:100%" readonly></select></td>'
					+'<td width="32%"><select id="' + ul_id + '_output_name__index_" class="form-control select2" placeholder="'+gettext('輸出名稱')+'" style="width:100%"></select></td>'
					+'<td width="32%"><input id="' + ul_id + '_output_des__index_" type="text" class="form-control " placeholder="'+gettext('說明')+'" readonly></td>'
					+'</tr></table>'
					+'</li>';	
		
		if(select_value == 0) //no excute
		{
			
		}
		else
		{
			flowobject.subflow.forEach(function(sub_flowobject) 
			{
				if(sub_flowobject.uid == select_value)
				{
					sub_flowobject.items.forEach(function(flow_item) 
					{
						if(flow_item.type == 'start') //start it's input
						{
							flow_item.config.input.forEach(function(input_item, index)
							{
								$( '#' + ul_id + '_input' ).append(item_li_input_content.replace(/_index_/g,index));

								//read form field to select2
								$( '#' + ul_id + '_input_value_' + index ).html(select_option_value() + select_option_form());
								//select2 enable
								$( '#' + ul_id + '_input_value_' + index ).select2({tags: true , placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
								$( '#' + ul_id + '_input_name_' + index ).select2({tags: false , placeholder: '', readonly: true ,allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
								$( '#' + ul_id + '_input_name_' + index ).prop("disabled", true);
								
								//相同名稱自動帶入
								if($( '#' + ul_id + '_input_value_' + index ).html().indexOf('$(' + input_item.name + ')') > 0 )
								{
									$( '#' + ul_id + '_input_value_' + index ).val('$(' + input_item.name + ')').trigger('change');
								}
								else
								{
									$( '#' + ul_id + '_input_value_' + index ).val(null).trigger('change');
								}
								
								//寫設定值
								var item_text = '';
								if(input_item.name.startsWith('$('))
								{
									item_text = input_item.name.substring(2);
									item_text = item_text.substring(0,item_text.length -1);
								}
								else
								{
									item_text = input_item.name;
								}
								
								$( '#' + ul_id + '_input_name_' + index ).html('<option value="' + item_text + '">'+gettext('變數:') + item_text + '</option>');
								
								$( '#' + ul_id + '_input_des_' + index ).val(input_item.des);
							});
						}
						if(flow_item.type == 'end') //start it's input
						{
							flow_item.config.output.forEach(function(output_item, index)
							{
								$( '#' + ul_id + '_output' ).append(item_li_output_content.replace(/_index_/g,index));

								//read form field to select2
								$( '#' + ul_id + '_output_name_' + index ).html(select_option_value());
								//select2 enable
								$( '#' + ul_id + '_output_name_' + index ).select2({tags: true,placeholder : gettext("輸出變數"),dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}},
								createTag: function(params) 
								{
									var term = $.trim(params.term);

									if (term == '') 
									{
									  return null;
									}
									
									if ((term.startsWith(gettext('變數:'))))
									{
										term = term.substring(3);
									}
									
									return {
									  id: '$(' + term + ')',
									  text: gettext('變數:') + term,
									  newTag: true // add additional parameters
									}
								}});
								$( '#' + ul_id + '_output_value_' + index ).select2({tags: false , placeholder: '', readonly: true ,allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
								$( '#' + ul_id + '_output_value_' + index ).prop("disabled", true);
								//寫設定值
								var item_text = '';
								if(output_item.name.startsWith('$('))
								{
									item_text = output_item.name.substring(2);
									item_text = item_text.substring(0,item_text.length -1);
								}
								else
								{
									item_text = output_item.name;
								}
								$( '#' + ul_id + '_output_value_' + index ).html('<option value="' + item_text + '">'+gettext('變數:')+ item_text + '</option>');
								$( '#' + ul_id + '_output_des_' + index ).val(output_item.des);

								//相同名稱自動帶入
								if($( '#' + ul_id + '_output_name_' + index ).html().indexOf('$(' + output_item.name + ')') > 0 )
								{
									$( '#' + ul_id + '_output_name_' + index ).val('$(' + output_item.name + ')').trigger('change');;
								}
								else
								{
									$( '#' + ul_id + '_output_name_' + index ).val(null).trigger('change');
								}
							});
						}
					});
				}

			});
		}
	}

	/**
	 * remove item(object) in flow content
	 * input:flowobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_remove_by_id(flow_item_id)
	{
		var item_mark = [];
		flow_item_id = flow_item_id.replace('item_remove_','').replace(active_id + '_','');
		flowobject.items.forEach(function(item,index)
		{
			if(flow_item_id == item.id)
			{
				item_mark.push(item);
			}
			if(item.type == 'line')    
			{
				if((flow_item_id == item.config.target_item)||(flow_item_id == item.config.source_item))
				{
					item_mark.push(item);
				}
			}
			
		});
		
		item_mark.forEach(function(item)
		{
			item_remove(item);
		});

		flow_clean();
	}
	
	/**
	 * remove item in flow content for item_remove_by_id
	 * input:flowobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_remove(flow_item)
	{
		flowobject.items.forEach(function(item,index)
		{
			if(item.id == flow_item.id) 
			{
				if(item.type == 'line') //want delete line
				{
					var source_obj = flowobject_get(item.config.source_item);
					var target_obj = flowobject_get(item.config.target_item);
					if(source_obj != null)
					{
						if((source_obj.type == 'switch')||(source_obj.type == 'async')) //remove rule
						{
							source_obj.config.rules.forEach(function(rule,rule_index)
							{
								if(rule.target == item.config.target_item)
								{
									source_obj.config.rules.splice(rule_index,1);
								}
							});
						}
					}
					if(target_obj != null)
					{
						if(target_obj.type == 'collection') // remove rull
						{
							target_obj.config.rules.forEach(function(rule,rule_index)
							{
								if(rule.target == item.config.source_item)
								{
									if(rule.target == target_obj.config.main) //if delete main rule , clear that
									{
										target_obj.config.main = '';
									}
									target_obj.config.rules.splice(rule_index,1);
								}
							});
						}
					}
					
					flowobject.items.splice(index,1);
					$('#' + active_id + '_FLINE_' + flow_item.config.idcounter + 'A').remove();
					$('#' + active_id + '_FLINE_' + flow_item.config.idcounter + 'B').remove();
					$('#' + active_id + '_FLINE_' + flow_item.config.idcounter + 'C').remove();
					$('#' + active_id + '_' + flow_item.id).remove();
					//check source is switch
					
				}
				else //delete object
				{
					flowobject.items.splice(index,1);
					$('#' + active_id + '_' + flow_item.id).remove();
				}
			}
		});
	}
	
	/**
	 * item copy button click 
	 * input:flowobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_copy_by_id(flow_item_id) 
	{
		flow_item_id = flow_item_id.replace('item_copy_','').replace(active_id + '_','');
		flowobject.items.forEach(function(item,index)
		{
			if(flow_item_id == item.id)
			{				
				var new_item = new item_object();
				flowobject.flow_item_counter++;
				new_item.id = "FITEM_" + flowobject.flow_item_counter;
				new_item.type = item.type;
				new_item.text = item.text;
				if(new_item.type == 'switch')
				{
					new_item.config = new switch_object();
				}
				else if(new_item.type == 'async')
				{
					new_item.config = new async_object();
				}
				else if(new_item.type == 'collection')
				{
					new_item.config = new collection_object;
				}
				else
				{
					new_item.config = JSON.parse(JSON.stringify(item.config)) //deep clone object
				}
				//new_item.config = item.config;
				new_item.config.top = item.config.top + 25;
				new_item.config.left = item.config.left + 30;
				
				flowobject.items.push(new_item);
				item_create(new_item);
				item_select($('#' + active_id + '_' + 'chart_' + new_item.id) , false);
			}

		});
		
	}
	/**
	 * item config button click
	 * input:flowobject.items
	 * return: no return.
	 * author:Pen Lin 
	 */
	function item_config_by_id(flow_item_id)
	{
		flow_item_id = flow_item_id.replace(active_id + '_','').replace('item_config_','');
		flowobject.items.forEach(function(item,index)
		{
			if(flow_item_id == item.id)
			{
				action_item_for_modal = item;
			}
		});
		var show_id = '#' + active_id + '_' + action_item_for_modal.type + '_chart_modal';;
		switch(action_item_for_modal.type)
		{
			case 'start':
				//clean all things
				$('#' + baseID_START + '_config_text').val('');
				$('#' + baseID_START + '_config_callable').attr("checked", false);
						
				$('#' + baseID_START + '_input_content').html('');
				$('#' + baseID_START + '_subflow_content').html('');
				$('#' + baseID_START + '_subflow_content_input').html('');
				$('#' + baseID_START + '_subflow_content_output').html('');
				$('.nav-tabs a[href="#' + baseID_START + '_config"]').tab('show');

				//load object to real
				$('#' + baseID_START + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_START + '_config_callable').prop("checked", action_item_for_modal.config.callable);
				
				$('#' + baseID_START + '_id').html(action_item_for_modal.id);
				
				
				modal_load_input(baseID_START , action_item_for_modal);
				modal_load_subflow(baseID_START , action_item_for_modal);
				
				break;
			case 'end':
				//clean all things
				$('#' + baseID_END + '_config_text').val('');
				$('#' + baseID_END + '_output_content').html('');
				$('#' + baseID_END + '_calculate_content').html('');
				$('.nav-tabs a[href="#' + baseID_END + '_config"]').tab('show');
				
				//load object to real
				$('#' + baseID_END + '_config_text').val(action_item_for_modal.text);
				
				$('#' + baseID_END + '_id').html(action_item_for_modal.id);
				
				modal_load_calculate(baseID_END , action_item_for_modal);
				modal_load_output(baseID_END , action_item_for_modal);
				

				break;
			case 'python':
				//clean all things
				$('#' + baseID_PYTHON + '_config_text').val('');
				$('#' + baseID_PYTHON + '_config_error_pass').attr("checked", false);
				$('#' + baseID_PYTHON + '_config_load_balance').attr("checked", false);
				$('#' + baseID_PYTHON + '_config_log').attr("checked", false);
				
				$('#' + baseID_PYTHON + '_output_content').html('');
				$('#' + baseID_PYTHON + '_input_content').html('');
				$('#' + baseID_PYTHON + '_calculate_content').html('');
				$('.nav-tabs a[href="#' + baseID_PYTHON + '_config"]').tab('show');


				//load object to real
				$('#' + baseID_PYTHON + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_PYTHON + '_config_autoinstall').prop("checked", action_item_for_modal.config.autoinstall);
				$('#' + baseID_PYTHON + '_config_error_pass').prop("checked", action_item_for_modal.config.error_pass);
				$('#' + baseID_PYTHON + '_config_load_balance').prop("checked", action_item_for_modal.config.load_balance);
				$('#' + baseID_PYTHON + '_config_log').prop("checked", action_item_for_modal.config.log);
				
				//if (action_item_for_modal.config.code !='')
				//{
				//	myCodeMirror.setValue(action_item_for_modal.config.code);
				//}
				myCodeMirror.setValue(action_item_for_modal.config.code);
				
				$('#' + baseID_PYTHON + '_id').html(action_item_for_modal.id);
				
				modal_load_calculate(baseID_PYTHON , action_item_for_modal);
				modal_load_input(baseID_PYTHON , action_item_for_modal);
				modal_load_output(baseID_PYTHON , action_item_for_modal);


				break;
			case 'subflow':
				//clean all things
				$('#' + baseID_SUBFLOW + '_config_text').val('');
				$('#' + baseID_SUBFLOW + '_config_error_pass').attr("checked", false);
				$('#' + baseID_SUBFLOW + '_config_log').attr("checked", false);
				
				$('#' + baseID_SUBFLOW + '_subflow_content').html('');
				$('#' + baseID_SUBFLOW + '_subflow_content_input').html('');
				$('#' + baseID_SUBFLOW + '_subflow_content_output').html('');
				$('.nav-tabs a[href="#' + baseID_SUBFLOW + '_config"]').tab('show');

				//load object to real
				$('#' + baseID_SUBFLOW + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_SUBFLOW + '_config_error_pass').prop("checked", action_item_for_modal.config.error_pass);
				$('#' + baseID_SUBFLOW + '_config_log').prop("checked", action_item_for_modal.config.log);
				
				$('#' + baseID_SUBFLOW + '_id').html(action_item_for_modal.id);
				
				modal_load_subflow(baseID_SUBFLOW , action_item_for_modal);

				break;
			case 'outflow':
				//clean all things
				$('#' + baseID_OUTFLOW + '_config_text').val('');
				$('#' + baseID_OUTFLOW + '_config_error_pass').attr("checked", false);
				$('#' + baseID_OUTFLOW + '_config_log').attr("checked", false);
				
				$('#' + baseID_OUTFLOW + '_subflow_content_input').html('');
				$('#' + baseID_OUTFLOW + '_subflow_content_output').html('');
				$('.nav-tabs a[href="#' + baseID_OUTFLOW + '_config"]').tab('show');

				//load object to real
				$('#' + baseID_OUTFLOW + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_OUTFLOW + '_config_error_pass').prop("checked", action_item_for_modal.config.error_pass);
				$('#' + baseID_OUTFLOW + '_config_log').prop("checked", action_item_for_modal.config.log);
				
				$('#' + baseID_OUTFLOW + '_id').html(action_item_for_modal.id);
				
				$('#' + baseID_OUTFLOW + '_select_app').val(action_item_for_modal.config.app_name).trigger('change');
				$('#' + baseID_OUTFLOW + '_select_flow').val(action_item_for_modal.config.flow_name).trigger('change');
				modal_load_outflow(baseID_OUTFLOW , action_item_for_modal);

				break;
			case 'inflow':
				//clean all things
				$('#' + baseID_INFLOW + '_config_text').val('');
				$('#' + baseID_INFLOW + '_config_error_pass').attr("checked", false);
				$('#' + baseID_INFLOW + '_config_log').attr("checked", false);
				
				$('#' + baseID_INFLOW + '_subflow_content_input').html('');
				$('#' + baseID_INFLOW + '_subflow_content_output').html('');
				$('.nav-tabs a[href="#' + baseID_INFLOW + '_config"]').tab('show');

				//load object to real
				$('#' + baseID_INFLOW + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_INFLOW + '_config_error_pass').prop("checked", action_item_for_modal.config.error_pass);
				$('#' + baseID_INFLOW + '_config_log').prop("checked", action_item_for_modal.config.log);
				
				$('#' + baseID_INFLOW + '_id').html(action_item_for_modal.id);
				
				$('#' + baseID_INFLOW + '_select_flow').val(action_item_for_modal.config.flow_name).trigger('change');
				modal_load_outflow(baseID_INFLOW , action_item_for_modal);

				break;
			case 'form':
				//clean all things
				$('#' + baseID_FORM + '_config_text').val('');
				$('#' + baseID_FORM + '_config_log').attr("checked", false);
				$('#' + baseID_FORM + '_action1_text').val('');
				$('#' + baseID_FORM + '_action1').attr("checked", false);
				$('#' + baseID_FORM + '_action2_text').val('');
				$('#' + baseID_FORM + '_action2').attr("checked", false);
				
				$('#' + baseID_FORM + '_calculate_content').html('');
				$('#' + baseID_FORM + '_input_content').html('');		
				$('#' + baseID_FORM + '1_input_content').html('');	
				$('#' + baseID_FORM + '2_input_content').html('');	
				$('#' + baseID_FORM + '_subflow_content').html('');
				$('#' + baseID_FORM + '_subflow_content_input').html('');
				$('#' + baseID_FORM + '_subflow_content_output').html('');
				$('#' + baseID_FORM + '_output_content').html('');
				$('#' + baseID_FORM + '_myform_content').html('');
				$('.nav-tabs a[href="#' + baseID_FORM + '_config"]').tab('show');

				$('#' + baseID_FORM + '_id').html(action_item_for_modal.id);
				
				//load object to real
				$('#' + baseID_FORM + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_FORM + '_config_log').prop("checked", action_item_for_modal.config.log);
				$('#' + baseID_FORM + '_action1_text').val(action_item_for_modal.config.action1_text);
				$('#' + baseID_FORM + '_action1').prop("checked", action_item_for_modal.config.action1);
				$('#' + baseID_FORM + '_action2_text').val(action_item_for_modal.config.action2_text);
				$('#' + baseID_FORM + '_action2').prop("checked", action_item_for_modal.config.action2);
				
				modal_load_calculate(baseID_FORM , action_item_for_modal);
				modal_load_input(baseID_FORM , action_item_for_modal);
				modal_load_subflow(baseID_FORM , action_item_for_modal); //incloud content , input , output
				modal_load_output(baseID_FORM , action_item_for_modal);
				
				if(action_item_for_modal.config.form_object  == null)
				{
					$('#' + baseID_FORM + '_myform_button_new_box6').css('display','none');
					$('#' + baseID_FORM + '_myform_button_new_box12').css('display','none');
				}
				else
				{
					formobject_for_modal = new omformeng(baseID_FORM + '_myform_content');
					formobject_for_modal.init(true);
					//更新最大值給裡面的物件
					action_item_for_modal.config.form_object.form_item_counter = flowobject.form_object.form_item_counter;
					action_item_for_modal.config.form_object.form_box_counter = flowobject.form_object.form_box_counter;
					formobject_for_modal.event_group_list(event_get_group_list_callback);
					formobject_for_modal.event_user_list(event_get_user_list_callback);
					formobject_for_modal.load(JSON.stringify(action_item_for_modal.config.form_object));
					//formobject_for_modal.setData(action_item_for_modal.config.form_setdata);
					$('#' + baseID_FORM + '_myform_button_new_box6').css('display','');
					$('#' + baseID_FORM + '_myform_button_new_box12').css('display','');
				}
				

				break;
			case 'setform':
				//clean all things
				$('#' + baseID_SETFORM + '_config_text').val('');
				$('#' + baseID_SETFORM + '_config_log').attr("checked", false);
				
				$('#' + baseID_SETFORM + '_calculate_content').html('');
				$('#' + baseID_SETFORM + '_input_content').html('');				
				$('#' + baseID_SETFORM + '_output_content').html('');
				$('.nav-tabs a[href="#' + baseID_SETFORM + '_config"]').tab('show');

				$('#' + baseID_SETFORM + '_id').html(action_item_for_modal.id);
				
				//load object to real
				$('#' + baseID_SETFORM + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_SETFORM + '_config_log').prop("checked", action_item_for_modal.config.log);
				
				modal_load_calculate(baseID_SETFORM , action_item_for_modal);
				modal_load_input(baseID_SETFORM , action_item_for_modal);
				modal_load_output(baseID_SETFORM , action_item_for_modal);

				break;
			case 'switch':
				//clean all things
				$('#' + baseID_SWITCH + '_config_text').val('');
				$('#' + baseID_SWITCH + '_config_log').attr("checked", false);
				$('#' + baseID_SWITCH + '_rule_content').html('');
				$('#' + baseID_SWITCH + '_calculate_content').html('');
				$('.nav-tabs a[href="#' + baseID_SWITCH + '_calculate"]').tab('show');

				$('#' + baseID_SWITCH + '_id').html(action_item_for_modal.id);
				$('#' + baseID_SWITCH + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_SWITCH + '_config_log').prop("checked", action_item_for_modal.config.log);
				//load object to real
				modal_load_calculate(baseID_SWITCH , action_item_for_modal);
				modal_load_rule(baseID_SWITCH , action_item_for_modal);
				

				break;
			case 'async':
				//clean all things
				$('#' + baseID_ASYNC + '_config_text').val('');
				$('#' + baseID_ASYNC + '_config_log').attr("checked", false);
				$('#' + baseID_ASYNC + '_rule_content').html('');
				$('.nav-tabs a[href="#' + baseID_ASYNC + '_rule"]').tab('show');
				
				$('#' + baseID_ASYNC + '_id').html(action_item_for_modal.id);
				$('#' + baseID_ASYNC + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_ASYNC + '_config_log').prop("checked", action_item_for_modal.config.log);
				//load object to real
				modal_load_rule_name(baseID_ASYNC , action_item_for_modal);
				
				break;
			case 'collection':
				//clean all things
				$('#' + baseID_COLLECTION + '_rule_content').html('');
				$('#' + baseID_COLLECTION + '_config_log').attr("checked", false);
				$('#' + baseID_COLLECTION + '_rule_content').html('');
				$('.nav-tabs a[href="#' + baseID_COLLECTION + '_rule"]').tab('show');
				
				$('#' + baseID_COLLECTION + '_id').html(action_item_for_modal.id);
				$('#' + baseID_COLLECTION + '_config_text').val(action_item_for_modal.text);
				$('#' + baseID_COLLECTION + '_config_log').prop("checked", action_item_for_modal.config.log);
				//load object to real
				modal_load_rule_name(baseID_COLLECTION , action_item_for_modal);

				break;
			case 'sleep':
				//clean all things
				$('.nav-tabs a[href="#' + baseID_SLEEP + '_input"]').tab('show');
				var slider = $("#" + baseID_SLEEP + '_config_msec').data("ionRangeSlider");
				slider.update({from: action_item_for_modal.config.msec});
				$('#' + baseID_SLEEP + '_input_value').html(select_option_value());
				
				$('#' + baseID_SLEEP + '_id').html(action_item_for_modal.id);
				
				if(action_item_for_modal.config.value == null)
				{
					//相同名稱自動帶入
					if($('#' + baseID_SLEEP + '_input_value').html().indexOf('$(' + 'msec' + ')') > 0 )
					{
						$('#' + baseID_SLEEP + '_input_value').val('$(' + 'msec' + ')').trigger('change');
					}
					else
					{
						$( '#' + baseID_SLEEP + '_input_value' ).val(null).trigger('change');
					}
				}
				else
				{
					$('#' + baseID_SLEEP + '_input_value').val(action_item_for_modal.config.value);
				}
				
				
				break;
			case 'org1':
				//clean all things
				$('#' + baseID_ORG1 + '_config_text').val('');
				
				$('#' + baseID_ORG1 + '_output_content').html('');
				$('#' + baseID_ORG1 + '_input_content').html('');

				//load object to real
				$('#' + baseID_ORG1 + '_config_text').val(action_item_for_modal.text);

				$('#' + baseID_ORG1 + '_id').html(action_item_for_modal.id);
				
				modal_load_input(baseID_ORG1 , action_item_for_modal);
				modal_load_output(baseID_ORG1 , action_item_for_modal);

				break;
			case 'org2':
				//clean all things
				$('#' + baseID_ORG2 + '_config_text').val('');
				
				$('#' + baseID_ORG2 + '_output_content').html('');
				$('#' + baseID_ORG2 + '_input_content').html('');

				//load object to real
				$('#' + baseID_ORG2 + '_config_text').val(action_item_for_modal.text);

				$('#' + baseID_ORG2 + '_id').html(action_item_for_modal.id);
				
				modal_load_input(baseID_ORG2 , action_item_for_modal);
				modal_load_output(baseID_ORG2 , action_item_for_modal);

				break;
		}
		$(show_id).modal('show');
	}

	/**
	 * add new item in flow content
	 * input:flowobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_create(flow_item)
	{
		var content = '';
		var para = [];
		switch(flow_item.type)
		{
			case 'start':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_start});
				para.push({'key':'_icon_','value':'fa fa-play-circle'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'ff8176'});
				if(design_mode)
				{
					para.push({'key':'_button_','value':item_content_button_config});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				break;
			case 'end':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_end});
				para.push({'key':'_icon_','value':'fas fa-flag-checkered'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'ff8176'});
				if(design_mode)
				{
					para.push({'key':'_button_','value':item_content_button_config});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'python':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_process});
				para.push({'key':'_icon_','value':'fab fa-python'});
				para.push({'key':'_iconsize_','value':'40'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'c0e4eb'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
							
				break;
			case 'subflow':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_process});
				para.push({'key':'_icon_','value':'fa fa-play-circle-o'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'c0e4eb'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config + item_content_button_copy});	
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
						
				break;
			case 'outflow':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_outflow});
				para.push({'key':'_icon_','value':'far fa-share-square'});
				para.push({'key':'_iconsize_','value':'40'});
				para.push({'key':'_iconoffset_','value':'top:35px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'aaa'});
				if(design_mode)
				{
					para.push({'key':'_button_','value':item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'inflow':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_outflow});
				para.push({'key':'_icon_','value':'fas fa-share'});
				para.push({'key':'_iconsize_','value':'40'});
				para.push({'key':'_iconoffset_','value':'top:35px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'aaa'});
				if(design_mode)
				{
					para.push({'key':'_button_','value':item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'switch':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_select});
				para.push({'key':'_icon_','value':'fa fa-map-signs'});
				para.push({'key':'_iconsize_','value':'30'});
				para.push({'key':'_iconoffset_','value':'top:40px;left:45px;'});
				para.push({'key':'_iconcolor_','value':'e49d64'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'form':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_form});
				para.push({'key':'_icon_','value':'fa fa-pencil-square-o'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:35px;'});
				para.push({'key':'_iconcolor_','value':'c0e4eb'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'setform':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_form});
				para.push({'key':'_icon_','value':'fas fa-database'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:35px;'});
				para.push({'key':'_iconcolor_','value':'c0e4eb'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'async':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_async});
				para.push({'key':'_icon_','value':'fas fa-people-arrows'});
				para.push({'key':'_iconsize_','value':'30'});
				para.push({'key':'_iconoffset_','value':'top:40px;left:45px;'});
				para.push({'key':'_iconcolor_','value':'e49d64'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'collection':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_collection});
				para.push({'key':'_icon_','value':'fas fa-compress-arrows-alt'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'e49d64'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'sleep':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_process});
				para.push({'key':'_icon_','value':'far fa-clock'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:35px;'});
				para.push({'key':'_iconcolor_','value':'c0e4eb'});
				if(design_mode)
				{
					para.push({'key':'_button_','value':item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
				
				break;
			case 'org1':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_process});
				para.push({'key':'_icon_','value':'fas fa-user-tie'});
				para.push({'key':'_iconsize_','value':'40'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'c0e4eb'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
							
				break;
			case 'org2':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_process});
				para.push({'key':'_icon_','value':'fas fa-user-tag'});
				para.push({'key':'_iconsize_','value':'40'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'c0e4eb'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config + item_content_button_copy});
				}
				else
				{
					para.push({'key':'_button_','value':''});
				}
							
				break;
			
		}
		
		para.push({'key':'_pid_','value': flow_item.id});
		para.push({'key':'_top_','value':flow_item.config.top});
		para.push({'key':'_left_','value':flow_item.config.left});
		
		flowcontent.append(replacer(item_content,para));
		
		$('#' + active_id + '_itext_content_' + flow_item.id).html(flow_item.text);	
		
		if(design_mode)
		{
			$('#' + active_id + '_' + flow_item.id).draggable({
				grid: [ 30, 25 ],
				containment: "parent",
				scroll: true,
				drag: function (){
					flow_drag_item(this);
					},
				stop: function (){
					flow_drag_item(this);
					}
			});
		}

		$('#' + active_id + '_' + 'itext_' + flow_item.id).click(function()
		{
			flow_chart_item_click(this);

		});
		
		$('#' + active_id + '_' + 'itext_' + flow_item.id).mouseenter(function(){
			flow_chart_item_enter(this);
		});

		if ($('#' + active_id + '_' + 'item_remove_' + flow_item.id).length > 0) 
		{ 
			$('#' + active_id + '_' + 'item_remove_' + flow_item.id).click(function()
			{
				item_remove_by_id(this.id);
			});
		}
		if ($('#' + active_id + '_' + 'item_config_' + flow_item.id).length > 0) 
		{ 
			$('#' + active_id + '_' + 'item_config_' + flow_item.id).click(function()
			{
				item_config_by_id(this.id);
			});
		}
		if ($('#' + active_id + '_' + 'item_copy_' + flow_item.id).length > 0) 
		{ 
			$('#' + active_id + '_' + 'item_copy_' + flow_item.id).click(function()
			{
				item_copy_by_id(this.id);
			});
		}
	}
	/**
	* create line object
	* input: flowobject.items.config
	* return: no return.
	* author:Pen Lin
	*/
	function line_create(line_obj)
	{
		var line_config = line_obj.config;
		var para = [];
		var side = line_config.target_side + line_config.source_side;
		
		if((side == "leftleft")||(side == "rightright"))
		{
			para = [];
			para.push({'key':'_pid_','value':'MH' + line_config.idcounter});
			para.push({'key':'_top_','value':line_config.linebox_top});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':4});
			para.push({'key':'_height_','value':line_config.linebox_long});
			para.push({'key':'_direction_','value':'left'});
			flowcontent.append(replacer(line_content,para));
			para = [];
			para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
			para.push({'key':'_top_','value':line_config.linebox_top + line_config.linebox_long});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':line_config.linebox_bottom_width});
			para.push({'key':'_height_','value':4});
			para.push({'key':'_direction_','value':'top'});
			flowcontent.append(replacer(line_content,para));
			para = [];
			para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
			para.push({'key':'_top_','value':line_config.linebox_top});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':line_config.linebox_top_width});
			para.push({'key':'_height_','value':4});
			para.push({'key':'_direction_','value':'top'});
			flowcontent.append(replacer(line_content,para));
		}
		else if((side == "leftright")||(side == "rightleft"))
		{
			para = [];
			para.push({'key':'_pid_','value':"MH" + line_config.idcounter});
			para.push({'key':'_top_','value':line_config.linebox_top});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':4});
			para.push({'key':'_height_','value':line_config.linebox_long});
			para.push({'key':'_direction_','value':'left'});
			flowcontent.append(replacer(line_content,para));
			
			if(line_config.linebox_bottom_width > 0) //往右長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top+line_config.linebox_long});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':line_config.linebox_bottom_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top+line_config.linebox_long});
				para.push({'key':'_left_','value':line_config.linebox_left-line_config.linebox_bottom_width});
				para.push({'key':'_width_','value':line_config.linebox_bottom_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
			
			if(line_config.linebox_top_width > 0) //往右長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':line_config.linebox_top_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left-line_config.linebox_top_width});
				para.push({'key':'_width_','value':line_config.linebox_top_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
		}
		else if(side == "topbottom")
		{
			para = [];
			para.push({'key':'_pid_','value':"MW" + line_config.idcounter});
			para.push({'key':'_top_','value':line_config.linebox_top});
			para.push({'key':'_left_','value':line_config.linebox_left-line_config.linebox_long});
			para.push({'key':'_width_','value':line_config.linebox_long});
			para.push({'key':'_height_','value':4});
			para.push({'key':'_direction_','value':'top'});
			flowcontent.append(replacer(line_content,para));
			if(line_config.linebox_bottom_width > 0) //往下長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left+line_config.linebox_long});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top + line_config.linebox_top_width});
				para.push({'key':'_left_','value':line_config.linebox_left+line_config.linebox_long});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_top_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
			
			if(line_config.linebox_top_width > 0) //往下長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_top_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top + line_config.linebox_top_width});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_top_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
		
		}
		else if((side == "topright")||(side == "topleft"))
		{
			para = [];
			para.push({'key':'_pid_','value':"MW" + line_config.idcounter});
			para.push({'key':'_top_','value':line_config.linebox_top});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':4});
			para.push({'key':'_height_','value':4});
			para.push({'key':'_direction_','value':'top'});
			flowcontent.append(replacer(line_content,para));
			
			if(line_config.linebox_bottom_width > 0) //往下長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top + line_config.linebox_bottom_width});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
			
			if(line_config.linebox_top_width > 0) //往右長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':line_config.linebox_top_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left+line_config.linebox_top_width});
				para.push({'key':'_width_','value':line_config.linebox_top_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
		}
		else if((side == "rightbottom")||(side == "leftbottom"))
		{
			para = [];
			para.push({'key':'_pid_','value':"MH" + line_config.idcounter});
			para.push({'key':'_top_','value':line_config.linebox_top});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':4});
			para.push({'key':'_height_','value':4});
			para.push({'key':'_direction_','value':'top'});
			flowcontent.append(replacer(line_content,para));
			
			if(line_config.linebox_bottom_width > 0) //往下長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{               
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top + line_config.linebox_bottom_width});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				flowcontent.append(replacer(line_content,para));
			}
			
			if(line_config.linebox_top_width > 0) //往右長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':line_config.linebox_top_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
			else
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left+line_config.linebox_top_width});
				para.push({'key':'_width_','value':line_config.linebox_top_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				flowcontent.append(replacer(line_content,para));
			}
		}
		
		
		var arrow_side = '';
		switch(line_config.target_side)
		{
			case 'top':
					arrow_side = '45';
			break;
			case 'left':
					arrow_side = '-45';
			break;
			case 'right':
					arrow_side = '135';
			break;
		}
		para = [];
		para.push({'key':'_pid_','value':line_config.idcounter + 'C'});
		para.push({'key':'_top_','value':line_config.linebox_arrow_top});
		para.push({'key':'_left_','value':line_config.linebox_arrow_left});
		para.push({'key':'_direction_','value':arrow_side});
		flowcontent.append(replacer(arrow_content,para));
		
		//Dragable
		if(design_mode)
		{
			$('[id^="' + active_id + '_' + 'FLINE_MH"]').draggable({ grid: [ 5, 5 ],containment: "parent",scroll: true,axis: "x",drag: function (){flow_drag_item(this)},stop: function (){flow_drag_item(this)}});
			$('[id^="' + active_id + '_' + 'FLINE_MW"]').draggable({ grid: [ 5, 5 ],containment: "parent",scroll: true,axis: "y",drag: function (){flow_drag_item(this)},stop: function (){flow_drag_item(this)}});
		}

		//畫完之後
		var source_obj = flowobject_get(line_obj.config.source_item); //check asnyc / switch / collector , push id
		var target_obj = flowobject_get(line_obj.config.target_item);
		
		if((source_obj.type == 'switch')||(source_obj.type == 'async'))
		{
			var rule_found = false;
			source_obj.config.rules.forEach(function(item,index)
			{
				if(item.target == line_obj.config.target_item)
				{
					//exist remove
					rule_found = true;
				}
			});
			
			if(rule_found)
			{

			}
			else
			{
				//push new
				var rule_object = {};
				rule_object["target"] = line_obj.config.target_item;
				rule_object["value1"] = '';
				rule_object["value2"] = '';
				rule_object["rule"] = '=';
				source_obj.config.rules.push(rule_object);
			}
			
		}
		if(target_obj.type == 'collection')
		{
			var rule_found = false;
			target_obj.config.rules.forEach(function(item,index)
			{
				if(item.target == line_obj.config.source_item)
				{
					//exist remove
					rule_found = true;
				}
			});
			
			if(rule_found)
			{

			}
			else
			{
				//push new
				var rule_object = {};
				rule_object["target"] = line_obj.config.source_item;
				rule_object["value1"] = '';
				rule_object["value2"] = '';
				rule_object["rule"] = '=';
				target_obj.config.rules.push(rule_object);
			}
			
		}

	}

	
	
	//====================
	//===Event Handler
	//====================
	/**
	 * when item drag , clean ball and redraw things 
	 * input:none
	 * return: no return.
	 * author:Pen Lin
	 */
	function flow_drag_item(middle_line)
	{
		var drag_obj_id = middle_line.id.replace(active_id + '_' , '');
		flow_clean(drag_obj_id);

		if(drag_obj_id.indexOf('FITEM_') == 0) //drag object
		{
			//drag item
			flowobject.items.forEach(function(item,index)
			{
				if(item.id == drag_obj_id) //update object content
				{
					item.config.top = $('#' + active_id + '_' + drag_obj_id).css('top').replace('px','') * 1;
					item.config.left = $('#' + active_id + '_' + drag_obj_id).css('left').replace('px','') * 1;
				}
				
				if(item.type == 'line') //all line for connect this object
				{
					if((item.config.source_item == drag_obj_id)||(item.config.target_item == drag_obj_id))
					{
						line_calculator(item, false);
						line_renew(flowobject.items[index]);
					 
					}
				}
			});
			
		}
		else if(drag_obj_id.indexOf('FLINE_M') == 0) //drag middle line
		{
			//drag line
			flowobject.items.forEach(function(item,index)
			 {
				if(item.id == drag_obj_id)
				{
					item.config.linebox_top = $('#' + active_id + '_' + drag_obj_id).css('top').replace('px','');
					item.config.linebox_left = $('#' + active_id + '_' + drag_obj_id).css('left').replace('px','');
					line_calculator(item, true);
					line_renew(flowobject.items[index] );
				}
			 });
		}
	}
	
	function ball_mousedown(ball_id)
	{
		//if this ball aalready chkecked , delete all marked line 
		var item_delete = false;
		var ball_source_item = selected_source_chart_item.attr('id').replace('chart_','').replace(active_id + '_' , '');
		
		if(selected_ball == ball_id)
		{
			flowobject.items.forEach(function(item, index, array)
			{
				if(item.type == 'line')
				{
					//get ball side from end of id , left , bottom , right
					var side = ball_id.replace(active_id + '_ball_','');
					if((item.config.source_item == ball_source_item)&&(item.config.source_side == side)) //+ and side
					{  
						item_remove_by_id(item.id);
					}
				}
				
			});
		}
		else
		{
			selected_ball = ball_id;
			$('[id^="' + active_id + '_' + 'ball_"]').css('background-color','#fff');
			$('#' + ball_id).css('background-color','#00ff00');
			flowobject.items.forEach(function(item, index, array)
			{
				if(item.type == 'line')
				{
					if((item.config.source_item == ball_source_item)&(item.config.source_side == ball_id.replace('ball_','').replace(active_id + '_' , '')))
					{
						$('#' + active_id + '_' + item.id).css('border-color','#ff0000');
						$('#' + active_id + '_' + item.id).css('z-index','991');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'A').css('border-color','#ff0000');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'B').css('border-color','#ff0000');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'C').css('border-color','#ff0000');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'A').css('z-index','991');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'B').css('z-index','991');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'C').css('z-index','991');
					}
					else
					{
						$('#' + active_id + '_' +  item.id).css('border-color','#777');
						$('#' + active_id + '_' +  item.id).css('z-index','990');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'A').css('border-color','#777');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'B').css('border-color','#777');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'C').css('border-color','#777');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'A').css('z-index','990');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'B').css('z-index','990');
						$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'C').css('z-index','990');
					}
				}
				
			});
		}
		
		
	}

	function tball_mousedown(ball_id) 
	{	

		var items_line = line_object(); 
		items_line.type = "line";
		items_line.config.target_side = ball_id.replace('tball_','').replace(active_id + '_' , '');
		items_line.config.source_side = flow_get_source_ball().replace('ball_','').replace(active_id + '_' , '');
		items_line.config.target_item = selected_target_chart_item.attr('id').replace('chart_','').replace(active_id + '_' , '');
		items_line.config.source_item = selected_source_chart_item.attr('id').replace('chart_','').replace(active_id + '_' , '');
		
		var source_obj = flowobject_get(items_line.config.source_item);
		var target_obj = flowobject_get(items_line.config.target_item);
		
		var line_exist = false;
		
		flowobject.items.forEach(function(item, index, array)
		{
			if(item.type == 'line') 
			{
				if((item.config.source_item == items_line.config.source_item)
					&&(item.config.target_item == items_line.config.target_item)
					&&(item.config.target_side == items_line.config.target_side)
					&&(item.config.source_side == items_line.config.source_side))
				{
					//完全同一條線
					line_exist = true;
				}
			}
		});
		
		if(!line_exist)
		{
			if((source_obj.type != 'switch')&(source_obj.type != 'async'))
			{
				flowobject.items.forEach(function(item, index, array)
				{
					if(item.type == 'line')
					{
						if(item.config.source_item == items_line.config.source_item)
						{
							item_remove(item);
						}
					}
				});
			}

			flowobject.flow_line_counter++; //FIRST

			items_line.config.idcounter = flowobject.flow_line_counter;
			
			if(items_line.config.target_side == 'top')
			{
				items_line.id = "FLINE_MW" + items_line.config.idcounter;
			}
			else
			{
				items_line.id = "FLINE_MH" + items_line.config.idcounter;
			}
			
			
			flowobject.items.push(items_line);
			
			line_calculator(items_line, false);
			line_create(items_line);
			line_renew(items_line);
			flow_clean();
		}

	}

	/**
	 * check have source ball selected
	 * input:none
	 * return: ball id
	 * author:Pen Lin
	 */
	function flow_get_source_ball()
	{
		var output = '';
		$('[id^="' + active_id + '_' + 'ball_"]').each(function(i)
		{
			   if(($(this).css('background-color')=='#00ff00')||($(this).css('background-color')=='rgb(0, 255, 0)'))
			   {
					output = $(this).attr('id');
			   }
		});
		return output;
	}
	
	//====================
	//===common functions
	//====================
	/**
	 * flow chart click , selected or cancel this item
	 * input:selected chart items
	 * return: no return.
	 * author:Pen Lin
	 */
	function flow_chart_item_click(itext_obj)
	{
		var chart_obj = $('#' + active_id + '_' + 'chart_' + itext_obj.id.replace('itext_','').replace(active_id + '_' , ''));
		if(selected_source_chart_item == null) 
		{
			flow_clean();
			item_select(chart_obj , false);
		}
		else
		{
			if( chart_obj.attr('id') == selected_source_chart_item.attr('id') )
			{
				flow_clean();
			}
			else
			{
				flow_clean();
				item_select(chart_obj , false);
			}
		}
	}
	/**
	 * for flow_chart_item_click , for flow_chart_item_click
	 * input:selected chart items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_select(selected_item,move)
	{
		//flowcontent.scrollTop(10)
		selected_source_chart_item = selected_item;
		$('[id^="' + active_id + '_' + 'chart_FITEM_"]').each(function()
		{
			if($(this).attr('id') == selected_source_chart_item.attr('id'))
			{
				$(this).css('border','4px solid #eab126');
				
				var obj = flowobject_get($(this).attr('id').replace('chart_','').replace(active_id + '_' , ''));

				if(design_mode)
				{
					$('#' + active_id + '_display_' + $(this).attr('id').replace('chart_','').replace(active_id + '_' , '')).css('display','');
					if(obj.type != 'end')
					{
						$('#' + active_id + '_ball_left').css('display','');
						$('#' + active_id + '_ball_left').css('top',(obj.config.top + 45) + 'px');
						$('#' + active_id + '_ball_left').css('left',(obj.config.left - 10) + 'px');
						
						$('#' + active_id + '_ball_right').css('display','');
						$('#' + active_id + '_ball_right').css('top',(obj.config.top + 45) + 'px');
						$('#' + active_id + '_ball_right').css('left',(obj.config.left + 120) + 'px');
						
						$('#' + active_id + '_ball_bottom').css('display','');
						$('#' + active_id + '_ball_bottom').css('top',(obj.config.top + 80) + 'px');
						$('#' + active_id + '_ball_bottom').css('left',(obj.config.left + 55) + 'px');
					}
				}
				if(move)
				{
					flowcontent.scrollTop(10);
					if(obj.config.top > (flowcontent.height()/2))
					{
						flowcontent.scrollTop(obj.config.top - (flowcontent.height() /2)  );
					}
					if(obj.config.left > (flowcontent.width()/2))
					{
						flowcontent.scrollLeft(obj.config.left - (flowcontent.width() /2)  );
					}
				}
				if(event_chart_selected_callback != null)
				{
					event_chart_selected_callback(obj.id);
				}
			}
			else
			{
				$('#' + active_id + '_' + 'display_' + $(this).attr('id').replace('chart_','').replace(active_id + '_' , '')).css('display','none');
				$(this).css('border','0px solid #eab126');
			}
		});
	}
	/**
	 * find item in flowobject items array , 
	 * input:item id
	 * return: flowobject.items.
	 * author:Pen Lin
	 */
	function flowobject_get(item_id)
	{
		var output = null;
		flowobject.items.forEach(function(item, index, array)
		{
			if(item.id == item_id)
			{
				output = item;
			}
		});
		return output;
	}
	/**
	 * if ball selected , enter flow item , show the tball 
	 * input:item chart object
	 * return: no return.
	 * author:Pen Lin
	 */
	function flow_chart_item_enter(itext_obj)
	{
		var chart_obj = $('#' + active_id + '_' + 'chart_' + itext_obj.id.replace('itext_','').replace(active_id + '_' , ''));
		//ball must selected one
		if(selected_ball != '')
		{
			if(selected_source_chart_item != null) 
			{
				if((chart_obj.attr('id') != selected_source_chart_item.attr('id')))
				{
					selected_target_chart_item = chart_obj;
					var obj = flowobject_get(chart_obj.attr('id').replace('chart_','').replace(active_id + '_' , ''));
					if(obj.type != 'start')
					{
						$('#' + active_id + '_' + 'tball_left').css('display','');
						$('#' + active_id + '_' + 'tball_left').css('top',(obj.config.top + 45) + 'px');
						$('#' + active_id + '_' + 'tball_left').css('left',(obj.config.left - 10) + 'px');
						
						$('#' + active_id + '_' + 'tball_right').css('display','');
						$('#' + active_id + '_' + 'tball_right').css('top',(obj.config.top + 45) + 'px');
						$('#' + active_id + '_' + 'tball_right').css('left',(obj.config.left + 120) + 'px');
						
						$('#' + active_id + '_' + 'tball_top').css('display','');
						$('#' + active_id + '_' + 'tball_top').css('top',(obj.config.top + 10) + 'px');
						$('#' + active_id + '_' + 'tball_top').css('left',(obj.config.left + 55) + 'px');
					}
				}
			}
		}
	}
	/**
	 * unselect all flow object
	 * input:none
	 * return: no return.
	 * author:Pen Lin
	 */
	function flow_clean()
	{
		selected_source_chart_item = null;
		selected_target_chart_item = null;
		selected_ball = '';
		$('[id^="' + active_id + '_' + 'chart_FITEM_"]').each(function(i)
		{
			$(this).css('border','0px solid #eab126');
		});
		
		$('[id^="' + active_id + '_ball_"]').css('background-color','#fff');
		$('[id^="' + active_id + '_ball_"]').css('display','none');
		
		$('[id^="' + active_id + '_tball_"]').css('background-color','#fff');
		$('[id^="' + active_id + '_tball_"]').css('display','none');
		
		$('[id^="' + active_id + '_tball_"]').css('display','none');
		$('[id^="' + active_id + '_tball_"]').css('display','none');
		
		$('[id^="' + active_id + '_display_"]').css('display','none');
		
		flowobject.items.forEach(function(item, index, array)
		{
			if(item.type == 'line')
			{
				$('#' + active_id + '_' + item.id).css('border-color','#777');
				$('#' + item.id).css('z-index','990');
				$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'A').css('border-color','#777');
				$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'B').css('border-color','#777');
				$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'C').css('border-color','#777');
				$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'A').css('z-index','990');
				$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'B').css('z-index','990');
				$('#' + active_id + '_' + 'FLINE_' + item.config.idcounter + 'C').css('z-index','990');
			}
			
		});
	}

	/**
	 * move all line to new line_config object postion  
	 * input:line_config
	 * return: no return.
	 * author:Pen Lin
	 */
	function line_renew(line_obj)
	{
		var line_config = line_obj.config;

		if((line_config.target_side == 'left')&&(line_config.source_side == 'left'))
		{
			//畫中線
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('height',line_config.linebox_long + 'px');
			//畫下
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',((line_config.linebox_top * 1 )+(line_config.linebox_long * 1)) + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('width',line_config.linebox_bottom_width + 'px');
			//畫上
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',line_config.linebox_top_width + 'px');
			//箭頭
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('top',line_config.linebox_arrow_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('left',line_config.linebox_arrow_left + 'px');
			
		}
		if((line_config.target_side == 'right')&&(line_config.source_side == 'right'))
		{
			//畫中線
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('height',((line_config.linebox_long*1)+2) + 'px');
			//畫下
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',((line_config.linebox_top * 1 )+(line_config.linebox_long * 1)) + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',((line_config.linebox_left * 1 ) - (line_config.linebox_bottom_width * 1)) + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('width',line_config.linebox_bottom_width + 'px');
			//畫上
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',((line_config.linebox_left * 1) - (line_config.linebox_top_width * 1)) + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',line_config.linebox_top_width + 'px');
			//箭頭
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('top',line_config.linebox_arrow_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('left',line_config.linebox_arrow_left + 'px');

		}
		if(((line_config.target_side == 'left')&&(line_config.source_side == 'right'))||((line_config.target_side == 'right')&&(line_config.source_side == 'left')))
		{
			//畫中線
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('height',((line_config.linebox_long*1)+2) + 'px');
			//畫下
			if(line_config.linebox_bottom_width > 0 )
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',((line_config.linebox_top * 1 )+(line_config.linebox_long * 1)) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',((line_config.linebox_left * 1 )) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('width',line_config.linebox_bottom_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',((line_config.linebox_top * 1 )+(line_config.linebox_long * 1)) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',((line_config.linebox_left * 1 ) + (line_config.linebox_bottom_width * 1)) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('width',(line_config.linebox_bottom_width*-1) + 'px');
			}
			//畫上
			if(line_config.linebox_top_width > 0 )
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',((line_config.linebox_left * 1)) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',line_config.linebox_top_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',((line_config.linebox_left * 1) + (line_config.linebox_top_width * 1)) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',(line_config.linebox_top_width*-1) + 'px');
			}
			//箭頭
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('top',line_config.linebox_arrow_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('left',line_config.linebox_arrow_left + 'px');

		}
		if((line_config.target_side == 'top')&&(line_config.source_side == 'bottom'))
		{
			//畫中線
			$('#' + active_id + '_' + 'FLINE_MW' + line_config.idcounter).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_MW' + line_config.idcounter).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_MW' + line_config.idcounter).css('width',line_config.linebox_long + 'px');
			//畫左
			if(line_config.linebox_top_width > 0) //左邊往下長
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',line_config.linebox_left + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('height',line_config.linebox_top_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',(line_config.linebox_top*1 + line_config.linebox_top_width*1) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',line_config.linebox_left + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('height',line_config.linebox_top_width*-1 + 'px');
			}
			
			//畫右
			if(line_config.linebox_bottom_width > 0) //往下長
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',(line_config.linebox_left*1 + line_config.linebox_long*1) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('height',line_config.linebox_bottom_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',(line_config.linebox_top*1 + line_config.linebox_bottom_width*1) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',(line_config.linebox_left*1 + line_config.linebox_long*1)  + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('height',line_config.linebox_bottom_width*-1+2 + 'px');
			}
			//畫箭頭
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('top',line_config.linebox_arrow_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('left',line_config.linebox_arrow_left + 'px');
		}
		if((line_config.target_side == 'top')&&((line_config.source_side == 'left')||(line_config.source_side == 'right')))
		{
			
			//畫中線
			$('#' + active_id + '_' + 'FLINE_MW' + line_config.idcounter).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_MW' + line_config.idcounter).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_MW' + line_config.idcounter).css('width',line_config.linebox_long + 'px');
			
			//直線,由Middle往下畫 或 由source畫往中線
			if(line_config.linebox_bottom_width > 0) 
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',line_config.linebox_left + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('height',line_config.linebox_bottom_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',(line_config.linebox_top*1 + line_config.linebox_bottom_width*1) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',line_config.linebox_left  + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('height',line_config.linebox_bottom_width*-1+2 + 'px');
			}
			
			//橫線,由Middle往右畫 或 由source畫往中線
			if(line_config.linebox_top_width > 0)
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',line_config.linebox_left + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',line_config.linebox_top_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',(line_config.linebox_left*1 + line_config.linebox_top_width*1) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',line_config.linebox_top_width*-1+2 + 'px');
			}
			//畫箭頭
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('top',line_config.linebox_arrow_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('left',line_config.linebox_arrow_left + 'px');
		}
		if((line_config.source_side == 'bottom')&&((line_config.target_side == 'left')||(line_config.target_side == 'right')))
		{
			
			//畫中線
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('top',line_config.linebox_top + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('left',line_config.linebox_left + 'px');
			$('#' + active_id + '_' + 'FLINE_MH' + line_config.idcounter).css('width',line_config.linebox_long + 'px');
			
			//直線,由Middle往下畫 或 由source畫往中線
			if(line_config.linebox_bottom_width > 0) 
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',line_config.linebox_left + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('height',line_config.linebox_bottom_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('top',(line_config.linebox_top*1 + line_config.linebox_bottom_width*1) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('left',line_config.linebox_left  + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'A')).css('height',line_config.linebox_bottom_width*-1+2 + 'px');
			}
			
			//橫線,由Middle往右畫 或 由target畫往中線
			if(line_config.linebox_top_width > 0)
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',line_config.linebox_left + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',line_config.linebox_top_width + 'px');
			}
			else
			{
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('top',line_config.linebox_top + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('left',(line_config.linebox_left*1 + line_config.linebox_top_width*1) + 'px');
				$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'B')).css('width',line_config.linebox_top_width*-1+2 + 'px');
			}
			//畫箭頭
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('top',line_config.linebox_arrow_top + 'px');
			$('#' + active_id + '_' + 'FLINE_' + (line_config.idcounter + 'C')).css('left',line_config.linebox_arrow_left + 'px');
		}
	}

	/**
	 * calculat new line width , x , y 
	 * input:line item
	 * return: line item.
	 * author:Pen Lin
	 */
	function line_calculator(line_item , moveline)
	{
		var line_config = line_item.config;
		var target_object = flowobject_get(line_config.target_item);
		var source_object = flowobject_get(line_config.source_item);
		var target_y = target_object.config.top;
		var target_x = target_object.config.left;
		var source_y = source_object.config.top;
		var source_x = source_object.config.left;

		var base_space = 100;
		var item_width = 120;
		var item_height = 60;
		var item_header_height = 20;
		
		if((line_config.target_side == 'left')&&(line_config.source_side == 'left'))
		{
			if(moveline) // need recalculator?
			{
				if(line_config.linebox_left >= getMinNumber(target_x , source_x)) 
				{
					moveline = false; //線拉超過允許範圍 重新計算
				}
			}
		
			if(!moveline) //recalculator
			{
				line_config.linebox_top = getMinNumber(target_y , source_y) + item_header_height + (item_height/2); //線框上標
				line_config.linebox_left = getMinNumber(target_x , source_x) - base_space;                          //線框左標
				line_config.linebox_long = Math.abs(target_y - source_y);                                           //線框高
				if(line_config.linebox_left < 0)
				{
					line_config.linebox_left = 0;
				}
			}
			var linebar_width_longer = getMaxNumber(target_x , source_x) - line_config.linebox_left; //長線
			var linebar_width_shorter = getMinNumber(target_x , source_x) - line_config.linebox_left; //短線
																									
			line_config.linebox_arrow_top = target_y + item_header_height + (item_height/2) - 4;
			line_config.linebox_arrow_left = target_x - 10;
																			 
			if(target_y > source_y)
			{
				if(source_x - target_x > 0)
				{
					//long
					line_config.linebox_top_width = linebar_width_longer;
					line_config.linebox_bottom_width = linebar_width_shorter; 
				}
				else
				{
					//sort
					line_config.linebox_top_width = linebar_width_shorter;
					line_config.linebox_bottom_width = linebar_width_longer;
				}
			}
			else
			{
				if(target_x - source_x > 0)
				{
					//long
					line_config.linebox_top_width = linebar_width_longer;
					line_config.linebox_bottom_width = linebar_width_shorter; 
				}
				else
				{
					//sort
					line_config.linebox_top_width = linebar_width_shorter;
					line_config.linebox_bottom_width = linebar_width_longer;
				}
			}
			
			
		}
		if((line_config.target_side == 'right')&&(line_config.source_side == 'right'))
		{
			if(moveline) //need recalculator?
			{
				if(line_config.linebox_left < getMaxNumber(target_x , source_x)+item_width)
				{
					moveline = false;
				}
			}
		
			if(!moveline) //recalculator
			{
				line_config.linebox_top = getMinNumber(target_y , source_y) + item_header_height + (item_height/2);
				line_config.linebox_left = getMaxNumber(target_x , source_x) + item_width + base_space;
				line_config.linebox_long = Math.abs(target_y - source_y);
				if(line_config.linebox_left <= 0)
				{
					line_config.linebox_left = 0;
				}
			}
			var linebar_width_longer = line_config.linebox_left - getMinNumber(target_x , source_x) - item_width ;
			var linebar_width_shorter = line_config.linebox_left - getMaxNumber(target_x , source_x) - item_width ;
																									
			line_config.linebox_arrow_top = target_y + item_header_height + (item_height/2) - 4;
			line_config.linebox_arrow_left = target_x + item_width;
																			 
			if(target_y > source_y)
			{
				if(source_x - target_x > 0)
				{
					//long
					line_config.linebox_top_width = linebar_width_shorter;
					line_config.linebox_bottom_width = linebar_width_longer; 
				}
				else
				{
					//sort
					line_config.linebox_top_width = linebar_width_longer;
					line_config.linebox_bottom_width = linebar_width_shorter;
				}
			}
			else
			{
				if(target_x - source_x > 0)
				{
					//long
					line_config.linebox_top_width = linebar_width_shorter;
					line_config.linebox_bottom_width = linebar_width_longer; 
				}
				else
				{
					//sort
					line_config.linebox_top_width = linebar_width_longer;
					line_config.linebox_bottom_width = linebar_width_shorter;
				}
			}
		}
	   
		if((line_config.target_side == 'top')&&(line_config.source_side == 'bottom'))
		{
			var target_y_box = target_y + item_header_height;
			var source_y_box = source_y + item_height + item_header_height;
			var target_x_box = target_x + item_width / 2;
			var source_x_box = source_x + item_width / 2;
			
			if(moveline) //need recalculator
			{
				if((line_config.linebox_top < getMinNumber(target_y , source_y)+item_header_height+item_height)||(line_config.linebox_top > getMaxNumber(target_y, source_y)))
				{
					moveline = false;
				}
			}

			if(!moveline) //recalculator
			{
				line_config.linebox_top = (target_y_box + source_y_box ) /2;
				line_config.linebox_left = getMinNumber(target_x_box , source_x_box);
				line_config.linebox_long = Math.abs(target_x_box - source_x_box);
			}

			if(line_config.linebox_left == target_x_box)
			{
				line_config.linebox_top_width = target_y_box - line_config.linebox_top;
				line_config.linebox_bottom_width = source_y_box - line_config.linebox_top;
			}
			else
			{
				line_config.linebox_top_width = source_y_box - line_config.linebox_top;
				line_config.linebox_bottom_width = target_y_box - line_config.linebox_top;
			}

			line_config.linebox_arrow_top = target_y - 10 + item_header_height;
			line_config.linebox_arrow_left = (target_x + item_width / 2) - 4;
			
		}
		
		if((line_config.target_side == 'top')&&((line_config.source_side == 'left')||(line_config.source_side == 'right')))
		{
			var target_y_box = 0;
			var target_x_box = 0;
			var source_y_box = 0;
			var source_x_box = 0;
			
			if(line_config.source_side == 'left')
			{
				source_y_box = source_y + item_header_height + item_height/2;
				source_x_box = source_x ;
			}
			else
			{
				source_y_box = source_y + item_header_height + item_height/2;
				source_x_box = source_x + item_width;
			}
			var target_y_box = target_y + item_header_height;
			var target_x_box = target_x + item_width / 2;
			
			line_config.linebox_top = source_y_box;
			line_config.linebox_left = target_x_box;
			line_config.linebox_long = 0;
			line_config.linebox_top_width  = source_x_box - line_config.linebox_left;
			line_config.linebox_bottom_width = target_y_box - line_config.linebox_top;
			
			line_config.linebox_arrow_top = target_y - 10 + item_header_height;
			line_config.linebox_arrow_left = (target_x + item_width / 2) - 4;
		}
		if((line_config.source_side == 'bottom')&&((line_config.target_side == 'left')||(line_config.target_side == 'right'))) 
		{
			var target_y_box = 0;
			var target_x_box = 0;
			var source_y_box = 0;
			var source_x_box = 0;
			
			if(line_config.target_side == 'left')
			{
				target_y_box = target_y + item_header_height + item_height/2;
				target_x_box = target_x ;
				line_config.linebox_arrow_top = target_y + item_header_height + (item_height/2) - 4;
				line_config.linebox_arrow_left = target_x - 10;
			}
			else
			{
				target_y_box = target_y + item_header_height + item_height/2;
				target_x_box = target_x + item_width;
				line_config.linebox_arrow_top = target_y + item_header_height + (item_height/2) - 4;
				line_config.linebox_arrow_left = target_x + item_width;
			}
			var source_y_box = source_y + item_height + item_header_height;
			var source_x_box = source_x + item_width / 2;
			
			line_config.linebox_top = target_y_box;
			line_config.linebox_left = source_x_box;
			line_config.linebox_long = 0;
			line_config.linebox_top_width  = target_x_box - line_config.linebox_left;
			line_config.linebox_bottom_width = source_y_box - line_config.linebox_top;
			
		}

		if(((line_config.target_side == 'left')&&(line_config.source_side == 'right'))||((line_config.target_side == 'right')&&(line_config.source_side == 'left')))
		{
			if(moveline)
			{
				if((line_config.linebox_left < getMinNumber(target_x , source_x)+item_width)||(line_config.linebox_left > getMaxNumber(target_x , source_x)))
				{
					moveline = false;
				}
			}

			//get source and target box
			var target_y_box = 0;
			var source_y_box = 0;
			var target_x_box = 0;
			var source_x_box = 0;
			
			
			if(line_config.target_side == 'left')
			{
				target_y_box = target_y + item_header_height + item_height/2;
				source_y_box = source_y  + item_header_height + item_height/2;
				target_x_box = target_x;
				source_x_box = source_x + item_width;
			}
			if(line_config.target_side == 'right')
			{
				target_y_box = target_y + item_header_height + item_height/2;
				source_y_box = source_y  + item_header_height + item_height/2;
				target_x_box = target_x + item_width;
				source_x_box = source_x;
			}
			
			if(!moveline)
			{
				//MIDDLE LINE
				line_config.linebox_top = getMinNumber(target_y_box , source_y_box);
				line_config.linebox_left = (target_x_box + source_x_box ) /2;
				line_config.linebox_long = Math.abs(target_y_box - source_y_box);
			}
																			 
			if(line_config.linebox_top == target_y_box) //target at line top
			{
				line_config.linebox_top_width = target_x_box - line_config.linebox_left;
				line_config.linebox_bottom_width = source_x_box - line_config.linebox_left;
			}
			else
			{  //target at line bottom
				line_config.linebox_top_width = source_x_box - line_config.linebox_left;
				line_config.linebox_bottom_width = target_x_box - line_config.linebox_left;
			}
																			
																			
			line_config.linebox_arrow_top = target_y + item_header_height + (item_height/2) - 4;
			if(line_config.target_side == 'left')
			{
				line_config.linebox_arrow_left = target_x - 10;
			}
			else
			{
				line_config.linebox_arrow_left = target_x + item_width;
			}
		}
	}

	function getMaxNumber(num1 , num2)
	{
		if(num1 >= num2)
		{
			return num1;
		}
		else
		{
			return num2;
		}
	};
	function getMinNumber(num1 , num2)
	{
		if(num1 >= num2)
		{
			return num2;
		}
		else
		{
			return num1;
		}
	};
	/**
	 * replace paramter array to source content
	 * input: source , string content
	 * input: paramter , [key,value]
	 * return: content.
	 * author:Pen Lin
	 */
	function replacer(source , parameter)
	{
		var output = source;
		parameter.forEach(function(item, index, array)
		{
			output = output.replace(new RegExp(item.key,'g'),item.value);
		});
		return output;
	}
	/**
	 * for Select 2 , select item , if not exist , auto appent item
	 * input: item_id , select2 id
	 * input: value
	 * return: content.
	 * author:Pen Lin
	 */
	function select2_put_value(item_id , value)
	{
		if($('#'+ item_id).length <= 0 )
		{
		}
		else
		{
			if(value == null)
			{
				$('#'+ item_id).val(null).trigger('change');
			}
			else if(value == '')
			{
				$('#'+ item_id).val(null).trigger('change');
			}
			else
			{
				if ($('#'+ item_id).html().indexOf('value="' + value + '"') > 0)
				{
					$('#'+ item_id).val(value).trigger('change');
				} 
				else 
				{ 
					if(value.startsWith('$('))
					{
						item_text = value.substring(2);
						item_text = item_text.substring(0,item_text.length -1);
						select2_new_option(item_id , value , gettext('變數:') + item_text);
						$('#' + item_id ).val(value).trigger('change');
					}
					if(value.startsWith('#('))
					{
						item_text = value.substring(2);
						item_text = item_text.substring(0,item_text.length -1);
						select2_new_option(item_id , value , gettext('欄位:') + item_text);
						$('#' + item_id ).val(value).trigger('change');
					}
					else if(value.startsWith('#G'))
					{
						//暫時排除
					}
					else
					{
						select2_new_option(item_id , value , value);
						$('#' + item_id ).val(value).trigger('change');
					}
				} 
			}
		}
	}

}

/**
OMFLOW Form Desinger
input , div_id must equals object name
*/
var omformeng = function(div_id)
{
	//====================
	//===public variable==
	//====================
	var _self_ = this;
	//====================
	//===private variable==
	//====================
	var active_id = div_id;
	var formobject = null;
	var formcontent = null;
	var design_mode = false;
	var action_item_for_modal = null;
	var event_get_group_list_callback = null;
	var event_get_user_list_callback = null;
	var group_tree_data_uuid =[];
	//====================
	//===MODAL NAME ID==
	//====================
	var baseID_NEW = active_id + '_' + 'new_modal';
	var baseID_BOX = active_id + '_' + 'box_modal';
	
	var baseID_INPUT = active_id + '_' + 'input_modal';
	var baseID_AREA = active_id + '_' + 'area_modal';
	var baseID_LIST = active_id + '_' + 'list_modal'; 
	var baseID_CHECKBOX = active_id + '_' + 'checkbox_modal'; 
	var baseID_DATE = active_id + '_' + 'date_modal'; 
	var baseID_DATETIME = active_id + '_' + 'datetime_modal'; 
	
	var baseID_HTITLE = active_id + '_' + 'h_title_modal';
	var baseID_HLEVEL = active_id + '_' + 'h_level_modal';
	var baseID_HSTATUS = active_id + '_' + 'h_status_modal';
	var baseID_HGROUP = active_id + '_' + 'h_group_modal';
	
	
	
	//====================
	//===public method====
	//====================
	/**
	 * initialization  omformeng
	 * input:
	 * return: 
	 * author:Pen Lin
	 */
	_self_.init = function(mode)
	{
		design_mode = mode;
		formobject = form_object();
		
		$('#' + active_id).addClass('box-body');
		
		formcontent = $('#' + active_id);
		formcontent.html('');

		//====================
		//===MODAL CHART NEW
		//====================
		var box_add_modal = '<div class="modal fade" id="' + baseID_NEW + '">'
					+'<div class="modal-dialog modal-dialog-scrollable">'
					+'<div class="modal-content">'
					+'<div class="modal-header">'
					+'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
					+'<span aria-hidden="true">&times;</span></button>'
					+'<h4 class="modal-title"><i class="fa fa-trash-o"></i>&nbsp;&nbsp;'+gettext('新增項目')+'</h4>'
					+'</div>'
					+'<div class="modal-body">'
					+'<div class="form-group">'
					+'<label>'+gettext('選擇新增項目')+'</label>'
					+'<select id="' + baseID_NEW + '_item_select" class="form-control select2" style="width:100%">'
					+'</select>'
					+'</div>'
					+'</div>'
					+'<div class="modal-footer">'
					+'<button type="button" class="btn btn-default pull-left" id="' + baseID_NEW + '_close">'+gettext('取消')+'</button>'
					+'<button type="button" class="btn btn-primary" id="' + baseID_NEW + '_submit">'+gettext('確定')+'</button>'
					+'</div>'
					+'</div>'
					+'</div><!-- /.modal-content -->'
					+'</div>';
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_NEW).length == 0)
		{
			formcontent.append(box_add_modal);
			$( '#' + baseID_NEW + '_item_select').select2({tags: false , placeholder: '',allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			$('#' + baseID_NEW + '_submit').click(function() 
			{
				_self_.add_item($('#' + baseID_NEW + '_item_select').val() , action_item_for_modal.id);
				$('#' + baseID_NEW).modal('hide');
			});
			$('#' + baseID_NEW + '_close').click(function() 
			{
				$('#'+ baseID_NEW).modal('hide');
			});
		}
		//====================
		//===MODAL CHART BOX 
		//====================
		var box_config_modal = '<div class="modal fade" id="' + baseID_BOX + '">'
					+'<div class="modal-dialog modal-dialog-scrollable">'
					+'<div class="modal-content">'
					+'<div class="modal-header">'
					+'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
					+'<span aria-hidden="true">&times;</span></button>'
					+'<h4 class="modal-title"><i class="fa fa-trash-o"></i>&nbsp;&nbsp;'+gettext('區塊設定')+'</h4>'
					+'</div>'
					+'<div class="modal-body">'
					+'<div class="form-group">'
					+'<label>'+gettext('標題文字')+'</label>'
					+'<input id="' + baseID_BOX + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入標題文字')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'+gettext('標示顏色')+'</label>'
					+'<select id="' + baseID_BOX + '_item_color" class="form-control select2" style="width:100%">'
					+'<option value="box box-default">'+gettext('灰')+'</option>'
					+'<option value="box box-danger">'+gettext('紅')+'</option>'
					+'<option value="box box-warning">'+gettext('黃')+'</option>'
					+'<option value="box box-primary">'+gettext('藍')+'</option>'
					+'<option value="box box-info">'+gettext('水藍')+'</option>'
					+'<option value="box box-success">'+gettext('綠')+'</option>'
					+'<option value="box">'+gettext('無色區塊')+'</option>'
					+'</select>'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_BOX + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_BOX + '_item_hidden"></label>'
					+' '+gettext('隱藏')+''
					+'</label>'
					+'</div>'
					+'</div>'
					+'<div class="modal-footer">'
					+'<button type="button" class="btn btn-default pull-left" id="' + baseID_BOX + '_close">'+gettext('取消')+'</button>'
					+'<button type="button" class="btn btn-primary" id="' + baseID_BOX + '_submit">'+gettext('確定')+'</button>'
					+'</div>'
					+'</div>'
					+'</div><!-- /.modal-content -->'
					+'</div>';
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_BOX ).length == 0)
		{
			formcontent.append(box_config_modal);
			$( '#' + baseID_BOX + '_item_color').select2({tags: false , placeholder: '',allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			
			$('#' + baseID_BOX + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_BOX + '_close').click(function() 
			{
				$('#' + baseID_BOX ).modal('hide');
			});
		}
		//====================
		//===MODAL CHART INPUT 
		//====================
		var input_config_modal = '<div class="modal fade" id="' + baseID_INPUT + '">'
					+'<div class="modal-dialog modal-dialog-scrollable">'
					+'<div class="modal-content">'
					+'<div class="modal-header">'
					+'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
					+'<span aria-hidden="true">&times;</span></button>'
					+'<h4 class="modal-title"><i class="fa fa-trash-o"></i>&nbsp;&nbsp;'+gettext('輸入格設定')+'</h4>'
					+'</div>'
					+'<div class="modal-body">'
					+'<div class="form-group">'
					+'<label>'+gettext('欄位名稱')+'</label>'
					+'<input id="' + baseID_INPUT + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'+gettext('註解說明')+'</label>'
					+'<input id="' + baseID_INPUT + '_item_placeholder" type="text" class="form-control" placeholder="'+gettext('請輸入註解文字')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'+gettext('預設值')+'</label>'
					+'<input id="' + baseID_INPUT + '_item_value" type="text" class="form-control" placeholder="'+gettext('請輸入預設值')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'+gettext('類型')+'</label>'
					+'<select id="' + baseID_INPUT + '_item_type" class="form-control select2" style="width:100%">'
					+'<option value="text">'+gettext('文字')+'</option>'
					+'<option value="number">'+gettext('數字')+'</option>'
					+'<option value="password">'+gettext('密碼')+'</option>'
					+'<option value="email">'+gettext('電子郵件')+'</option>'
					+'<option value="url">'+gettext('網址')+'</option>'
					+'<option value="unique">'+gettext('唯一值')+'</option>'
					+'</select>'
					+'</div>'
					
					+'<div class="form-group">'
					+'<label>'+gettext('格式檢查(REGEX)')+'</label>'
					+'<input id="' + baseID_INPUT + '_item_regex" type="text" class="form-control" placeholder="'+gettext('請輸入regex語法')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_INPUT + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_INPUT + '_item_require"></label>'
					+' '+gettext('必填')+''
					+'</label>'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_INPUT + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_INPUT + '_item_readonly"></label>'
					+' '+gettext('唯讀')+''
					+'</label>'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_INPUT + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_INPUT + '_item_hidden"></label>'
					+' '+gettext('隱藏')+''
					+'</label>'
					+'</div>'
					
					+'</div>'
					+'<div class="modal-footer">'
					+'<button type="button" class="btn btn-default pull-left" id="' + baseID_INPUT + '_close">'+gettext('取消')+'</button>'
					+'<button type="button" class="btn btn-primary" id="' + baseID_INPUT + '_submit">'+gettext('確定')+'</button>'
					+'</div>'
					+'</div>'
					+'</div><!-- /.modal-content -->'
					+'</div>';
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_INPUT ).length == 0)
		{
			formcontent.append(input_config_modal);
			$( '#' + baseID_INPUT + '_item_type').select2({tags: false , placeholder: '',allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			
			$('#' + baseID_INPUT + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_INPUT + '_close').click(function() 
			{
				$('#' + baseID_INPUT ).modal('hide');
			});
		}
		//====================
		//===MODAL CHART AREA 
		//====================
		var area_config_modal = '<div class="modal fade" id="' + baseID_AREA + '">'
					+'<div class="modal-dialog modal-dialog-scrollable">'
					+'<div class="modal-content">'
					+'<div class="modal-header">'
					+'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
					+'<span aria-hidden="true">&times;</span></button>'
					+'<h4 class="modal-title"><i class="fa fa-trash-o"></i>&nbsp;&nbsp;'+gettext('多行輸入設定')+'</h4>'
					+'</div>'
					+'<div class="modal-body">'
					+'<div class="form-group">'
					+'<label>'+gettext('欄位名稱')+'</label>'
					+'<input id="' + baseID_AREA + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
					+'</div>'
					
					+'<div class="form-group">'
					+'<label>'+gettext('行數')+'</label>'
					+'<select id="' + baseID_AREA + '_item_rows" class="form-control select2" style="width:100%">'
					+'<option value="3">3</option>'
					+'<option value="4">4</option>'
					+'<option value="5">5</option>'
					+'<option value="6">6</option>'
					+'<option value="7">7</option>'
					+'<option value="8">8</option>'
					+'<option value="9">9</option>'
					+'</select>'
					+'</div>'
					
					+'<div class="form-group">'
					+'<label>'+gettext('格式檢查(REGEX)')+'</label>'
					+'<input id="' + baseID_AREA + '_item_regex" type="text" class="form-control" placeholder="'+gettext('請輸入regex語法')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_AREA + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_AREA + '_item_require"></label>'
					+' '+gettext('必填')+''
					+'</label>'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_AREA + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_AREA + '_item_readonly"></label>'
					+' '+gettext('唯讀')+''
					+'</label>'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_AREA + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_AREA + '_item_hidden"></label>'
					+' '+gettext('隱藏')+''
					+'</label>'
					+'</div>'
					
					+'</div>'
					+'<div class="modal-footer">'
					+'<button type="button" class="btn btn-default pull-left" id="' + baseID_AREA + '_close" >'+gettext('取消')+'</button>'
					+'<button type="button" class="btn btn-primary" id="' + baseID_AREA + '_submit">'+gettext('確定')+'</button>'
					+'</div>'
					+'</div>'
					+'</div><!-- /.modal-content -->'
					+'</div>';
		
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_AREA).length == 0)
		{
			formcontent.append(area_config_modal);
			$( '#' + baseID_AREA + '_item_rows').select2({tags: false , placeholder: '',allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			
			$('#' + baseID_AREA + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_AREA + '_close').click(function() 
			{
				$('#' + baseID_AREA ).modal('hide');
			});
		}
		//====================
		//===MODAL CHART H_TITLE 
		//====================
		var htitle_config_modal = '<div class="modal fade" id="' + baseID_HTITLE + '">'
					+'<div class="modal-dialog modal-dialog-scrollable">'
					+'<div class="modal-content">'
					+'<div class="modal-header">'
					+'<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
					+'<span aria-hidden="true">&times;</span></button>'
					+'<h4 class="modal-title"><i class="fa fa-trash-o"></i>&nbsp;&nbsp;'+gettext('標題設定')+'</h4>'
					+'</div>'
					+'<div class="modal-body">'
					
					+'<div class="form-group">'
					+'<label>'+gettext('欄位名稱')+'</label>'
					+'<input id="' + baseID_HTITLE + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
					+'</div>'
					
					+'<div class="form-group">'
					+'<label>'+gettext('註解說明')+'</label>'
					+'<input id="' + baseID_HTITLE + '_item_placeholder" type="text" class="form-control" placeholder="'+gettext('請輸入註解文字')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'+gettext('預設值')+'</label>'
					+'<input id="' + baseID_HTITLE + '_item_value" type="text" class="form-control" placeholder="'+gettext('請輸入預設值')+'">'
					+'</div>'
					
					+'<div class="form-group">'
					+'<label>'+gettext('格式檢查(REGEX)')+'</label>'
					+'<input id="' + baseID_HTITLE + '_item_regex" type="text" class="form-control" placeholder="'+gettext('請輸入regex語法')+'">'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_HTITLE + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HTITLE + '_item_require"></label>'
					+' '+gettext('必填')+''
					+'</label>'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_HTITLE + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HTITLE + '_item_readonly"></label>'
					+' '+gettext('唯讀')+''
					+'</label>'
					+'</div>'
					+'<div class="form-group">'
					+'<label>'
					+'<input id="' + baseID_HTITLE + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HTITLE + '_item_hidden"></label>'
					+' '+gettext('隱藏')+''
					+'</label>'
					+'</div>'
					
					+'</div>'
					+'<div class="modal-footer">'
					+'<button type="button" class="btn btn-default pull-left" id="' + baseID_HTITLE + '_close" >'+gettext('取消')+'</button>'
					+'<button type="button" class="btn btn-primary" id="' + baseID_HTITLE + '_submit">'+gettext('確定')+'</button>'
					+'</div>'
					+'</div>'
					+'</div><!-- /.modal-content -->'
					+'</div>';
		
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_HTITLE).length == 0)
		{
			formcontent.append(htitle_config_modal);
			
			$('#' + baseID_HTITLE + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_HTITLE + '_close').click(function() 
			{
				$('#' + baseID_HTITLE ).modal('hide');
			});
		}
		//====================
		//===MODAL CHART H_STATUS 
		//====================
		var hstatus_config_modal = '<div class="modal fade" id="' + baseID_HSTATUS + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('狀態欄位')+'</h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' +baseID_HSTATUS + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_HSTATUS + '_status" data-toggle="tab">'+gettext('選項')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_HSTATUS + '_config">'
						
						+'      <div class="form-group">'
						+'       <label>'+gettext('欄位名稱')+'</label>'
						+'       <input id="' + baseID_HSTATUS + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
						+'      </div>'
						
						+'      <div class="form-group">'
						+'       <label>'+gettext('預設值')+'</label>'
						+'       <input id="' + baseID_HSTATUS + '_item_value" type="text" class="form-control" placeholder="'+gettext('請輸入預設值')+'">'
						+'      </div>'			
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_HSTATUS + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HSTATUS + '_item_require"></label>'
						+'        '+gettext('必填')+''
						+'       </label>'
						+'      </div>'
						+'<div class="form-group">'
						+'<label>'
						+'<input id="' + baseID_HSTATUS + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HSTATUS + '_item_readonly"></label>'
						+' '+gettext('唯讀')+''
						+'</label>'
						+'</div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'        <input id="' + baseID_HSTATUS + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HSTATUS + '_item_hidden"></label>'
						+'        '+gettext('隱藏')+''
						+'       </label>'
						+'      </div>'						
						+'     </div>'
						
						+'     <div class="tab-pane " id="' + baseID_HSTATUS + '_status">'
						+'      <button id="' + baseID_HSTATUS + '_status_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_HSTATUS +  '_status_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						

						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_HSTATUS + '_close" >'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_HSTATUS + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';
		
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_HSTATUS).length == 0)
		{
			formcontent.append(hstatus_config_modal);
			
			$('#' + baseID_HSTATUS + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_HSTATUS + '_close').click(function() 
			{
				$('#' + baseID_HSTATUS ).modal('hide');
			});
			
			$( '#' + baseID_HSTATUS +  '_status_content' ).sortable();
			$( '#' + baseID_HSTATUS +  '_status_content' ).disableSelection();
			
			$('#'+ baseID_HSTATUS + '_status_content_add').click(function () 
			{
				dropdown_sortable_add(baseID_HSTATUS +  '_status_content'); 
			});
		}
		//====================
		//===MODAL CHART H_LEVEL 
		//====================
		var hlevel_config_modal = '<div class="modal fade" id="' + baseID_HLEVEL + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('燈號設定')+'</h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' +baseID_HLEVEL + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_HLEVEL + '_level" data-toggle="tab">'+gettext('選項')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_HLEVEL + '_config">'
						
						+'      <div class="form-group">'
						+'       <label>'+gettext('欄位名稱')+'</label>'
						+'       <input id="' + baseID_HLEVEL + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
						+'      </div>'
						
						+'      <div class="form-group">'
						+'       <label>'+gettext('預設值')+'</label>'
						+'       <input id="' + baseID_HLEVEL + '_item_value" type="text" class="form-control" placeholder="'+gettext('請輸入預設值')+'">'
						+'      </div>'			
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_HLEVEL + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HLEVEL + '_item_require"></label>'
						+'        '+gettext('必填')+''
						+'       </label>'
						+'      </div>'
						+'<div class="form-group">'
						+'<label>'
						+'<input id="' + baseID_HLEVEL + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HLEVEL + '_item_readonly"></label>'
						+' '+gettext('唯讀')+''
						+'</label>'
						+'</div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'        <input id="' + baseID_HLEVEL + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HLEVEL + '_item_hidden"></label>'
						+'        '+gettext('隱藏')+''
						+'       </label>'
						+'      </div>'						
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_HLEVEL + '_level">'
						+'      <ul id="' + baseID_HLEVEL +  '_level_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						

						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_HLEVEL + '_close" >'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_HLEVEL + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';
		
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_HLEVEL).length == 0)
		{
			formcontent.append(hlevel_config_modal);
			
			$('#' + baseID_HLEVEL + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_HLEVEL + '_close').click(function() 
			{
				$('#' + baseID_HLEVEL ).modal('hide');
			});

		}
		//====================
		//===MODAL CHART LIST 
		//====================
		var list_config_modal = '<div class="modal fade" id="' + baseID_LIST + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('下拉選單')+'</h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' +baseID_LIST + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_LIST + '_list" data-toggle="tab">'+gettext('選項')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_LIST + '_config">'
						
						+'      <div class="form-group">'
						+'       <label>'+gettext('欄位名稱')+'</label>'
						+'       <input id="' + baseID_LIST + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'+gettext('預設值')+'</label>'
						+'       <input id="' + baseID_LIST + '_item_value" type="text" class="form-control" placeholder="'+gettext('請輸入預設值')+'">'
						+'      </div>'			
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_LIST + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_LIST + '_item_require"></label>'
						+'        '+gettext('必填')+''
						+'       </label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'        <input id="' + baseID_LIST + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_LIST + '_item_readonly"></label>'
						+'        '+gettext('唯讀')+''
						+'       </label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'        <input id="' + baseID_LIST + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_LIST + '_item_hidden"></label>'
						+'        '+gettext('隱藏')+''
						+'       </label>'
						+'      </div>'						
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_LIST + '_list">'
						+'      <button id="' + baseID_LIST + '_list_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_LIST +  '_list_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						
						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_LIST + '_close" >'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_LIST + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';
		
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_LIST).length == 0)
		{
			formcontent.append(list_config_modal);
			
			$('#' + baseID_LIST + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_LIST + '_close').click(function() 
			{
				$('#' + baseID_LIST ).modal('hide');
			});
			
			$( '#' + baseID_LIST +  '_list_content' ).sortable();
			$( '#' + baseID_LIST +  '_list_content' ).disableSelection();
			
			$('#'+ baseID_LIST + '_list_content_add').click(function () 
			{
				dropdown_sortable_add(baseID_LIST +  '_list_content'); 
			});
		}
		//====================
		//===MODAL CHART CHECKBOX 
		//====================
		var checkbox_config_modal = '<div class="modal fade" id="' + baseID_CHECKBOX + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('勾選欄位')+'</h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' +baseID_CHECKBOX + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_CHECKBOX + '_checkbox" data-toggle="tab">'+gettext('選項')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_CHECKBOX + '_config">'
						
						+'      <div class="form-group">'
						+'       <label>'+gettext('欄位名稱')+'</label>'
						+'       <input id="' + baseID_CHECKBOX + '_item_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_CHECKBOX + '_item_multiple" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_CHECKBOX + '_item_multiple"></label>'
						+'        '+gettext('複選')+''
						+'       </label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'+gettext('預設值')+'</label>'
						+'       <input id="' + baseID_CHECKBOX + '_item_value" type="text" class="form-control" placeholder="'+gettext('預設值1,預設值2,預設值3')+'">'
						+'      </div>'			
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_CHECKBOX + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_CHECKBOX + '_item_require"></label>'
						+'        '+gettext('必填')+''
						+'       </label>'
						+'      </div>'
						+'<div class="form-group">'
						+'<label>'
						+'<input id="' + baseID_CHECKBOX + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_CHECKBOX + '_item_readonly"></label>'
						+' '+gettext('唯讀')+''
						+'</label>'
						+'</div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'        <input id="' + baseID_CHECKBOX + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_CHECKBOX + '_item_hidden"></label>'
						+'        '+gettext('隱藏')+''
						+'       </label>'
						+'      </div>'						
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_CHECKBOX + '_checkbox">'
						+'      <button id="' + baseID_CHECKBOX + '_checkbox_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_CHECKBOX +  '_checkbox_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						

						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_CHECKBOX + '_close" >'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_CHECKBOX + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';
		
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_CHECKBOX).length == 0)
		{
			formcontent.append(checkbox_config_modal);
			
			$('#' + baseID_CHECKBOX + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_CHECKBOX + '_close').click(function() 
			{
				$('#' + baseID_CHECKBOX ).modal('hide');
			});
			
			$( '#' + baseID_CHECKBOX +  '_checkbox_content' ).sortable();
			$( '#' + baseID_CHECKBOX +  '_checkbox_content' ).disableSelection();
			
			$('#'+ baseID_CHECKBOX + '_checkbox_content_add').click(function () 
			{
				dropdown_sortable_add(baseID_CHECKBOX +  '_checkbox_content'); 
			});
		}
		
		//====================
		//===MODAL CHART H_GROUP 
		//====================
		var hgroup_config_modal = '<div class="modal fade" id="' + baseID_HGROUP + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('受派人及組織')+'</h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' +baseID_HGROUP + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'     <li><a href="#' + baseID_HGROUP + '_group" data-toggle="tab">'+gettext('選項')+'</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'
						
						+'     <div class="tab-pane active" id="' +baseID_HGROUP + '_config">'
						
						+'      <div class="form-group">'
						+'       <label>'+gettext('組織欄位名稱')+'</label>'
						+'       <input id="' + baseID_HGROUP + '_item_group_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_HGROUP + '_item_user" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HGROUP + '_item_user"></label> '+gettext('包含受派人欄位')+''
						+'       </label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'+gettext('受派人欄位名稱')+'</label>'
						+'       <input id="' + baseID_HGROUP + '_item_user_title" type="text" class="form-control" placeholder="'+gettext('請輸入欄位名稱')+'">'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'+gettext('預設值')+'</label>'
						+'       <input id="' + baseID_HGROUP + '_item_value" type="text" class="form-control" placeholder="'+gettext('組織,受派人')+'">'
						+'      </div>'			
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_HGROUP + '_item_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HGROUP + '_item_require"></label> '+gettext('組織必填')+''
						+'       </label>'
						+'      </div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'       <input id="' + baseID_HGROUP + '_item_user_require" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HGROUP + '_item_user_require"></label> '+gettext('受派人必填')+''
						+'       </label>'
						+'      </div>'
						+'<div class="form-group">'
						+'<label>'
						+'<input id="' + baseID_HGROUP + '_item_readonly" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HGROUP + '_item_readonly"></label>'
						+' '+gettext('唯讀')+''
						+'</label>'
						+'</div>'
						+'      <div class="form-group">'
						+'       <label>'
						+'        <input id="' + baseID_HGROUP + '_item_hidden" type="checkbox" class="icheckbox_minimal-blue" ><label for="' + baseID_HGROUP + '_item_hidden"></label>'
						+'        '+gettext('隱藏')+''
						+'       </label>'
						+'      </div>'						
						+'     </div>'
						
						+'     <div class="tab-pane" id="' + baseID_HGROUP + '_group">'
						+'      <button id="' + baseID_HGROUP + '_group_content_add' + '" type="button" class="btn btn-default" style="margin:1px 0px;"><i class="fa fa-plus"></i> '+gettext('新增')+'</button>'
						+'      <ul id="' + baseID_HGROUP +  '_group_content' + '" style="list-style-type: none; margin: 0; padding: 0">'
						+'      </ul>'					
						+'     </div>'
						

						+'    </div>'
						
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_HGROUP + '_close" >'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_HGROUP + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';
		
		//====================
		//===MODAL INIT
		//====================
		if ($('#' + baseID_HGROUP).length == 0)
		{
			formcontent.append(hgroup_config_modal);
			
			$('#' + baseID_HGROUP + '_submit').click(function() 
			{
				modal_config_box_submit();
			});
			$('#' + baseID_HGROUP + '_close').click(function() 
			{
				$('#' + baseID_HGROUP ).modal('hide');
			});
			
			$( '#' + baseID_HGROUP +  '_group_content' ).sortable();
			$( '#' + baseID_HGROUP +  '_group_content' ).disableSelection();
			
			$('#'+ baseID_HGROUP + '_group_content_add').click(function () 
			{
				group_sortable_add(baseID_HGROUP +  '_group_content'); 
			});
		}
		
	}
	function group_sortable_add(ul_id)
	{	
		var group_item = '<li id="' + ul_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
					+ '<table width="100%"><tr>'
					+'  <td width="4%"><span class="fa fa-arrows-v"></span></td>'
					+'  <td width="46%"><select id="' + ul_id + '_value__index_" class="form-control select2" style="width:100%"></select></td>'
					+'  <td width="46%"><input id="' + ul_id + '_text__index_" class="form-control"  placeholder="'+gettext('顯示文字')+'"></td>'
					+'  <td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + ul_id + '_li__index_"></i></td>'
					+'</tr></table></li>';
		var newindex = 0;
		while($( '#' + ul_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}
		$( '#' + ul_id ).append(group_item.replace(/_index_/g,newindex));

		$('#' +  ul_id + '_value_' + newindex).html(dropdown_array_to_group(null,true));
		$('#' +  ul_id + '_value_' + newindex).select2ToTree({language: {noResults: function (params) {return " ";}}});	
		$('#' +  ul_id + '_value_' + newindex).val(null).trigger('change');
		$('#' +  ul_id + '_value_' + newindex).change(function()
		{
			var selected_value = $('#' + this.id).val();
			$('#' + this.id.replace('_value_','_text_')).val(selected_value);
		});
		$('#' +  ul_id + '_text_' + newindex).change(function()
		{
			var selected_value = $('#' + this.id).val();
			$('#' + this.id.replace('_text_','_value_')).val(selected_value).trigger('change');
		});
		//remove event
		$('#remove_' + ul_id + '_li_' + newindex ).click(function()
		{
			var get_li_id =  $( this ).attr('id').replace('remove_','');
			$('#' + get_li_id ).remove();
		});
		
		
	}
	
	function dropdown_sortable_add(ul_id)
	{	
		var dropdown_item = '<li id="' + ul_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
					+ '<table width="100%"><tr>'
					+'  <td width="4%"><span class="fa fa-arrows-v"></span></td>'
					+'  <td width="46%"><input id="' + ul_id + '_value__index_" class="form-control" placeholder="'+gettext('值')+'"></td>'
					+'  <td width="46%"><input id="' + ul_id + '_text__index_" class="form-control"  placeholder="'+gettext('顯示文字')+'"></td>'
					+'  <td width="4%" align="right" style="color:silver"><i class="far fa-trash-alt" id="remove_' + ul_id + '_li__index_"></i></td>'
					+'</tr></table></li>';
		var newindex = 0;
		while($( '#' + ul_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}
		$( '#' + ul_id ).append(dropdown_item.replace(/_index_/g,newindex));
		
		//remove event
		$('#remove_' + ul_id + '_li_' + newindex ).click(function()
		{
			var get_li_id =  $( this ).attr('id').replace('remove_','');
			$('#' + get_li_id ).remove();
		});
	}
	function dropdown_sortable_add_readonly(ul_id)
	{	
		var dropdown_item = '<li id="' + ul_id + '_li__index_" class="ui-state-default" style=" margin: 0 0 0 0;height:30px;">'
					+ '<table width="100%"><tr>'
					+'  <td width="4%"><span class="fa fa-arrows-v"></span></td>'
					+'  <td width="43%"><input id="' + ul_id + '_value__index_" class="form-control" placeholder="'+gettext('值')+'" readonly></td>'
					+'  <td width="43%"><input id="' + ul_id + '_text__index_" class="form-control"  placeholder="'+gettext('顯示文字')+'" readonly></td>'
					+'</tr></table></li>';
		var newindex = 0;
		while($( '#' + ul_id  + '_li_' + newindex).length !=0)
		{
			newindex = newindex + 1;
		}
		$( '#' + ul_id ).append(dropdown_item.replace(/_index_/g,newindex));
	}
	

	function dropdown_array_to_option(form_item)
	{
		var output = '';
		form_item.config.lists.forEach(function(item, index, array)
		{
			if(item.value == form_item.config.value)
			{
				output += '<option selected="selected" value="' + item.value + '">' + item.text + '</option>';
			}
			else
			{
				output += '<option value="' + item.value + '">' + item.text + '</option>';
			}
				
		});
		return output;
	}
	function dropdown_array_to_checkbox(form_item)
	{
		var output = '';
		var global_id = active_id + '_' + form_item.id;
		var multiple = form_item.config.multiple;
		if(form_item.config.readonly)
		{
			readonly = 'readonly';
		}
		
		form_item.config.lists.forEach(function(item, index, array)
		{
			if(multiple)
			{
				//checkbox
				output += '<div><input id="' + global_id + '_item_' + index + '" name="' + global_id + '_item[]" type="checkbox" class="icheckbox_minimal-blue" value="' + item.value + '" readonly><label for="' + global_id + '_item_' + index + '"></label> ' + item.text + '</div>'
			}
			else
			{
				//radio
				output += '<div><input id="' + global_id + '_item_' + index + '" type="radio" name="' + global_id + '_item" class="iradio_minimal-blue" value="' + item.value + '" readonly><label for="' + global_id + '_item_' + index + '"></label>' + item.text + '</div>'
			}
				
		});
		
		return output;
	}
	function dropdown_array_to_group(form_item , uuid_mode)
	{
		var output = '';
		var list_count = 0;
		if(form_item == null)
		{
			list_count = -1;
		}
		else
		{
			list_count = form_item.config.lists.length;
		}
		
		//get global
		if(group_tree_data_uuid.length <= 0 )
		{
			var group_tree_data_source = [];
			if(event_get_group_list_callback == null)
			{
				//no function assign
				group_tree_data_source = 
						[
							{id: 1, group_uuid: "06c83964-8628-468d-8412-56dbde09e35b", display_name: "凌群電腦", parent_group: null},
							{id: 2, group_uuid: "7f59287c-2f53-4a5b-8abf-b9f07d6ba317", display_name: "技術中心", parent_group: 1},
							{id: 7, group_uuid: "e57c9ed0-760b-45d2-a7dc-7129fe4859c2", display_name: "電信服務總處", parent_group: 2},
							{id: 3, group_uuid: "2580cc1b-3ba8-4acb-977a-c22e67c79697", display_name: "專業服務總處", parent_group: 2},
							{id: 6, group_uuid: "6ec027a7-6102-4101-8312-1ab3701832a7", display_name: "系統整合處", parent_group: 3},
							{id: 5, group_uuid: "fa822079-6b74-43d5-b44e-ed3e52c2ceda", display_name: "專業服務處", parent_group: 3},
							{id: 4, group_uuid: "f74106e7-8dd3-43b1-929e-9aedff9a87eb", display_name: "管理軟體服務處", parent_group: 3},
							{id: 9, group_uuid: "b26ea838-fbb9-4512-9d70-4582f3200b9c", display_name: "電信中南區服務處", parent_group: 7},
							{id: 8, group_uuid: "dbc29569-44b4-47bb-a0d7-f21c97cb41b5", display_name: "電信北區服務處", parent_group: 7}
						];
			}
			else
			{
				group_tree_data_source = event_get_group_list_callback();
			}
			
			group_tree_data_source.forEach(function(option_item)
			{
				if(option_item.parent_group == null)
				{
					group_tree_data_uuid.push({'id':option_item.id ,'value':option_item.group_uuid ,'text':option_item.display_name ,'parent_group':option_item.parent_group ,'parent':null,'level':1,'nonleaf':'non-leaf'});
				}
				else
				{
					var new_class = 0;
					var parent_uuid = '';
					group_tree_data_uuid.forEach(function(parent_item)
					{
						if(parent_item.id == option_item.parent_group)
						{
							new_class = parent_item.level + 1;
							parent_uuid = parent_item.value;
						}
					});
					//find child
					var nonleaf = '';
					group_tree_data_source.forEach(function(find_item)
					{
						if(find_item.parent_group == option_item.id)
						{
							nonleaf = 'non-leaf';
						}
					});
					group_tree_data_uuid.push({'id':option_item.id ,'value':option_item.group_uuid ,'text':option_item.display_name ,'parent_group':option_item.parent_group ,'parent':parent_uuid,'level':new_class,'nonleaf':nonleaf });
				}
			});
		}
		
		if(list_count <= 0)
		{
			//remake
			if(uuid_mode)
			{
				group_tree_data_uuid.forEach(function(group_item)
				{
					if (group_item.parent==null)
					{
						output += '<option value="' + group_item.value + '" class="l' + group_item.level + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.value + '-->';
					}
					else
					{
						output = output.replace('<!--' + group_item.parent + '-->','<option value="' + group_item.value + '" data-pup="' + group_item.parent + '" class="l' + group_item.level + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.value + '--><!--' + group_item.parent + '-->'); 
					}
				});
			}
			else
			{
				//convert to id
				group_tree_data_uuid.forEach(function(group_item)
				{
					if (group_item.parent==null)
					{
						output += '<option value="' + group_item.id + '" class="l' + group_item.level + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.id + '-->';
					}
					else
					{
						output = output.replace('<!--' + group_item.parent_group + '-->','<option value="' + group_item.id + '" data-pup="' + group_item.parent_group + '" class="l' + group_item.level + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.id + '--><!--' + group_item.parent_group + '-->'); 
					}
				});	
			}
		}
		else
		{
			if(uuid_mode)
			{
				group_tree_data_uuid.forEach(function(group_item)
				{
					if (group_item.parent==null)
					{
						output += '<option value="' + group_item.value + '" class="l' + group_item.level + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.value + '-->';
					}
					else
					{
						output = output.replace('<!--' + group_item.parent + '-->','<option value="' + group_item.value + '" data-pup="' + group_item.parent + '" class="l' + group_item.level + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.value + '--><!--' + group_item.parent + '-->'); 
					}
				});
			}
			else
			{
				//需支援多層次
				var output_multi = '';
				form_item.config.lists.forEach(function(list_item)
				{
					output = '';
					var root_id = 0;
					var tree_item = [];
					group_tree_data_uuid.forEach(function(group_item)
					{
						//循線往下長
						var root_level = 1;
						if (group_item.value == list_item.text)
						{
							output += '<option value="' + group_item.id + '" class="l' + '1' + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.id + '-->';
							root_level = group_item.level;
							tree_item.push(group_item.id);
						}
						else
						{
							if((tree_item.indexOf(group_item.id))||(tree_item.indexOf(group_item.parent_group)))
							{
								if(!(group_item.id in tree_item))
								{
									tree_item.push(group_item.id);
								}
								output = output.replace('<!--' + group_item.parent_group + '-->','<option value="' + group_item.id + '" data-pup="' + group_item.parent_group + '" class="l' + group_item.level + ' ' + group_item.nonleaf + '" >' + group_item.text + '</option><!--' + group_item.id + '--><!--' + group_item.parent_group + '-->'); 
							}
						}
					});	
					output_multi = output_multi + output;
					
				});
				output = output_multi;
			}
		}

		return output;
	}
	/**
	 * create a new form item  , from public level
	 * input: item type:
	 * return: 
	 * author:Pen Lin
	 */
	_self_.add_item = function(item_type , parent)
	{
		var item = new item_object();
		if(item_type.startsWith("box"))
		{
			formobject.form_box_counter++;
			item.id = "FORMBOX_" + formobject.form_box_counter;
		}
		else
		{
			formobject.form_item_counter++;
			item.id = "FORMITM_" + formobject.form_item_counter;
		}
		
		if(parent == null)
		{
			parent = 'public';
		}
		
		item.parent = parent;
		item.type = item_type;
		item.config = form_item_config_default(item_type);
		
		if(check_h_exist(item.type))
		{
			alert(item.type + ' already exist.');
		}
		else
		{
			formobject.items.push(item);
			item_create(item);
		}
		
	}
	/**
	 * get form design by string
	 * input:
	 * return: string
	 * author:Pen Lin
	 */
	_self_.toString = function()
	{
		return JSON.stringify(formobject);
	}
	/**
	 * return formobject
	 * input:
	 * return: flowobject
	 * author:Pen Lin
	 */
	_self_.getObject = function()
	{
		return formobject;
	}
	/**
	 * put form design by string
	 * input: string
	 * return: 
	 * author:Pen Lin
	 */
	_self_.load = function(form)
	{
		formobject = JSON.parse(form);
		if(formobject.items != null)
		{
			formobject.items.forEach(function(item, index, array)
			{
				item_create(item);
			});
		}
		_self_.setData(_self_.getDefaultData(formobject));
	}
	
	
	//====================
	//===object definition
	//====================

	/**
	 * inside object definition    -- start
	 * author:Pen Lin
	 */
	function form_object()
	{
		var output = {};
		output["form_item_counter"] = 0;
		output["form_box_counter"] = 0;
		output["user"] = [];
		output["group"] = [];
		output["level"] = [];
		output["title"] = false;
		output["status"] = [];
		output["op1"] = [];
		output["op2"] = [];
		output["items"] = [];
		return output;
	}
	function item_object()
	{
		var output = {};
		var config = {};
		output["id"] = '';
		output["type"] = '';
		output["parent"] = '';
		output["hidden"] = false;
		output["config"] = config;
		
		return output;
	}
	function box_object()
	{
		var output = {};
		output["idcounter"] = 0;
		output["color"] = '';
		output["title"] = '';
		
		return output;
	}
	function input_object()
	{
		var output = {};
		output["idcounter"] = 0;
		output["title"] = '';
		output["require"] = false;
		output["placeholder"] = '';
		output["type"] = ''; //email/password/text
		output["value"] = '';
		output["regex"] = '';
		output["readonly"] = false;
		
		return output;
	}
	function area_object()
	{
		var output = {};
		output["idcounter"] = 0;
		output["title"] = '';
		output["require"] = false;
		output["rows"] = 0;
		output["value"] = '';
		output["regex"] = '';
		output["readonly"] = false;
		
		return output;
	}
	function list_object()
	{
		var output = {};
		output["idcounter"] = '';
		output["title"] = '';
		output["lists"] = [];
		output["value"] = '';
		output["require"] = true;
		output["readonly"] = false;
		return output;
	}
	function checkbox_object()
	{
		var output = {};
		output["idcounter"] = '';
		output["title"] = '';
		output["lists"] = [];
		output["value"] = '';
		output["require"] = true;
		output["multiple"] = false;
		output["readonly"] = false;
		return output;
	}
	function h_title_object()
	{
		var output = {};
		output["idcounter"] = 0;
		output["title"] = '';
		output["require"] = false;
		output["placeholder"] = '';
		output["value"] = '';
		output["regex"] = '';
		output["readonly"] = false;
		return output;
	}
	function h_status_object()
	{
		var output = {};
		output["idcounter"] = '';
		output["title"] = '';
		output["lists"] = [];
		output["value"] = '';
		output["require"] = true;
		output["readonly"] = false;
		return output;
	}
	function h_level_object()
	{
		var output = {};
		output["idcounter"] = '';
		output["title"] = '';
		output["lists"] = [];
		output["value"] = '';
		output["require"] = true;
		output["readonly"] = false;
		
		return output;
	}

	function h_group_object()
	{
		var output = {};
		output["idcounter"] = '';
		output["group_title"] = '';
		output["lists"] = [];
		output["value"] = '';
		output["require"] = true;
		output["readonly"] = false;
		output["user"] = true;
		output["user_title"] = '';
		output["user_require"] = false;
		return output;
	}
	
	

	function check_h_exist(item_type)
	{
		var output = false;
		if(item_type.startsWith('h_'))
		{
			formobject.items.forEach(function(item, index, array)
			{
				if(item.type == item_type )
				{
					output = true;
				}
			});
		}
		return output;
	}
	function item_create(form_item)
	{
		/**
		 _p_id_
		 _item_type_
		 **/
		 
		var content = '';
		
		var drag = '';
		var drop = '';
		var config_button = '';
		var remove_button = '';
		var add_button = '';
		
		var hidden = '';
		var hidden_box = '';
		var readonly = '';
		var require = '';

		if(design_mode)
		{
			//var drag = ' draggable="true" ondragstart="' + active_id + '.boxdrag(event)" ondragover="' + active_id + '.boxAllowDrop(event) "';
			drag = ' draggable="true" ';
			//var drop = ' ondrop="' + active_id + '.boxdrop(event,this)" ';
			drop = ' ';
			config_button = '<button type="button" class="btn btn-box-tool pull-right" id="_pid__box_config_button" ><i class="fa fa-gear"></i></button>';
			remove_button = '<button type="button" class="btn btn-box-tool pull-right" id="_pid__box_remove_button" ><i class="fa fa-remove"></i></button>';
			add_button = '<button type="button" class="btn btn-box-tool pull-right"  id="_pid__box_add_button" ><i class="fa fa-plus"></i></button>';
		}
		else
		{
			//user mode
			
			if(form_item.hidden)
			{
				hidden = 'style="display:none"';
				hidden_box = 'hidden'
			}
		}
		
		if(form_item.config.readonly)
		{
			readonly = 'readonly';
		}

		if(form_item.config.require)
		{
			require = '<font color="red">*</font>';
		}

		
		switch(form_item.type)
		{
			case 'inputbox':
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
						+ remove_button + config_button
						+'<label id="_pid__title">' + form_item.config.title + require
						+'</label>'
						+'<input id="_pid__item" type="' + form_item.config.type + '" class="form-control" placeholder="' + form_item.config.placeholder + '" ' + readonly + '>'
						+'</div>';
				break;
			case 'areabox':
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
						+ remove_button + config_button
						+'<label id="_pid__title">' + form_item.config.title + require
						+'</label>'
						+'<textarea id="_pid__item" rows="' + form_item.config.rows + '" class="form-control" ' + readonly + '></textarea>'
						+'</div>';
				break;
			case 'list':
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
						+ remove_button + config_button
						+'<label id="_pid__title">' + form_item.config.title + require
						+'</label>'
						+'<select id="_pid__item" class="form-control select2" ' + readonly + ' style="width:100%">' + dropdown_array_to_option(form_item) + '</select>'
						+'</div>';
				break;
			case 'checkbox':
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
						+ remove_button + config_button
						+'<label id="_pid__title">' + form_item.config.title + require
						+'</label>'
						+'<div id="_pid__item">'
						+ dropdown_array_to_checkbox(form_item)
						+'</div>'
						+'</div>';
				break;
			case 'box6':
				content ='<div id="_pid_" class="col-md-6 ' + hidden_box + '"' + drag + ' ' + drop + '>'
						+'<div id="_pid__color" class="' + form_item.config.color + '" >'
						+'<div class="box-header with-border"><span id="_pid__title">' + form_item.config.title + '</span>'
						+ remove_button + config_button + add_button
						+'</div>'
						+'<div id="_pid__item" class="box-body"></div>'
						+'</div></div>';
				break;
			case 'box12':
				content ='<div id="_pid_" class="col-md-12 ' + hidden_box + '"' + drag + ' ' + drop + '>'
						+'<div id="_pid__color" class="' + form_item.config.color + '" >'
						+'<div class="box-header with-border"><span id="_pid__title">' + form_item.config.title + '</span>'
						+ remove_button + config_button + add_button
						+'</div>'
						+'<div id="_pid__item" class="box-body"></div>'
						+'</div></div>';
				break;
			case 'h_title':
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
						+ remove_button + config_button
						+'<label id="_pid__title">' + form_item.config.title + require
						+'</label>'
						+'<input id="_pid__item" type="text" class="form-control" placeholder="' + form_item.config.placeholder + '" ' + readonly + '>'
						+'</div>';
				break;
			case 'h_status':
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
						+ remove_button + config_button
						+'<label id="_pid__title">' + form_item.config.title + require
						+'</label>'
						+'<select id="_pid__item" class="form-control select2" ' + readonly + ' style="width:100%">' + dropdown_array_to_option(form_item) + '</select>'
						+'</div>';
				break;
			case 'h_level':
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
						+ remove_button + config_button
						+'<label id="_pid__title">' + form_item.config.title + require
						+'</label>'
						+'<select id="_pid__item" class="form-control select2" ' + readonly + ' style="width:100%">' + dropdown_array_to_option(form_item) + '</select>'
						+'</div>';
				break;
			case 'h_group':
				var display_none = '';
				var user_require = '';
				if(!form_item.config.user)
				{
					display_none = 'display:none;';
				}
				
				if(form_item.config.user_require)
				{
					user_require = '<font color="red">*</font>';
				}
				
				content = '<div id="_pid_" class="form-group "' + drag + ' ' + hidden + '>'
					+ remove_button + config_button
					+'<label id="_pid__group_title">' + form_item.config.group_title + require
					+'</label>'
					+'<select id="_pid__group_item" class="form-control select2" ' + readonly + ' style="width:100%">' + dropdown_array_to_group(form_item,false) + '</select>'
					+'<label id="_pid__user_title" style="' + display_none + '">' + form_item.config.user_title + user_require
					+'</label>'
					+'<select id="_pid__user_item" class="form-control select2" ' + readonly + ' style="width:100%;' + display_none + '"></select>'
					+'</div>';

				break;
		}
		
		//content = '<!--start _pid_-->' + content + '<!--end _pid_-->';
		content = content.replace(/_pid_/g,active_id + '_' + form_item.id);
		
		if(form_item.parent == 'public')
		{
			formcontent.append(content);
		}
		else
		{
			$('#'+ active_id + '_' + form_item.parent + '_item').append(content);
		}
		
		switch(form_item.type)
		{
			case 'list':
			case 'h_status':
			case 'h_level':
			//require , allowClear
				if(form_item.config.require)
				{
					$( '#' + active_id + '_' + form_item.id + '_item').select2({tags: false , placeholder: '',allowClear: false,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
				}
				else
				{
					$( '#' + active_id + '_' + form_item.id + '_item').select2({tags: false , placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
					$( '#' + active_id + '_' + form_item.id + '_item').val(null).trigger('change');
				}
				
				if(form_item.config.readonly)
				{
					$( '#' + active_id + '_' + form_item.id + '_item').select2({disabled:true});
				}
				break;
			case 'h_group':
				$( '#' + active_id + '_' + form_item.id + '_user_item').select2({tags: false , placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
				if(form_item.config.readonly)
				{
					$( '#' + active_id + '_' + form_item.id + '_group_item').select2({disabled:true});
					$( '#' + active_id + '_' + form_item.id + '_user_item').select2({disabled:true});
				}
				break;
			
			
		}
		
		
		document.getElementById(active_id + '_' + form_item.id).ondragstart = _self_.boxdrag;
		document.getElementById(active_id + '_' + form_item.id).ondragover = _self_.boxAllowDrop;

		
		if(form_item.type.startsWith('box'))
		{
			document.getElementById(active_id + '_' + form_item.id).ondrop = _self_.boxdrop;
		}
		
		
		$('#' + active_id + '_' + form_item.id + '_box_config_button').click(function() 
		{
			box_button_config_item(active_id + '_' + form_item.id);
		});
		$('#' + active_id + '_' + form_item.id + '_box_remove_button').click(function() 
		{
			box_button_remove_item(active_id + '_' + form_item.id);
		});
		$('#' + active_id + '_' + form_item.id + '_box_add_button').click(function() 
		{
			box_button_add_item(active_id + '_' + form_item.id);
		});
		
		//$('#' +  active_id + '_' + form_item.id + '_group_item').html(list_options);
		$('#' +  active_id + '_' + form_item.id + '_group_item').select2ToTree({language: {noResults: function (params) {return " ";}}});	
		$('#' +  active_id + '_' + form_item.id + '_group_item').val(null).trigger('change');
		$('#' +  active_id + '_' + form_item.id + '_group_item').change(function()
		{
			var selected_value = $('#' + this.id).val();
			var user_list = [];
			if(event_get_user_list_callback == null)
			{
				user_list = [{id: 1, nick_name: "林先生"},{id: 2,  nick_name: "黃小姐"}];
			}
			else
			{
				user_list = event_get_user_list_callback($(this).val());
			}
			
			if(selected_value != null)
			{
				var options = '';
				user_list.forEach(function(item, index, array)
				{
					options = options + '<option value="' + item.id + '">' + item.nick_name + '</option>'
				});
				$('#' +  active_id + '_' + form_item.id + '_user_item').html(options);
				$('#' +  active_id + '_' + form_item.id + '_user_item').select2({tags: false,placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});
			}
		});
	}
	
	function form_item_config_default(item_type)
	{
		var confitem = null;
		switch(item_type)
		{
			case 'inputbox':
				confitem = new input_object();
				confitem.title = gettext('輸入');
				confitem.idcounter = formobject.form_item_counter;
				confitem.require = false;
				confitem.placeholder = '';
				confitem.type = 'text';
				confitem.rows = 0;
				confitem.readonly = false;
				break;
			case 'areabox':
				confitem = new area_object();
				confitem.title = gettext('多行輸入');
				confitem.idcounter = formobject.form_item_counter;
				confitem.require = false;
				confitem.rows = 3;
				confitem.readonly = false;
				break;
			case 'list':
				confitem = new h_status_object();
				confitem.title = gettext('選單');
				confitem.idcounter = formobject.form_item_counter;
				confitem.require = true;
				confitem.readonly = false;
				break;
			case 'checkbox':
				confitem = new h_status_object();
				confitem.title = gettext('勾選');
				confitem.idcounter = formobject.form_item_counter;
				confitem.require = true;
				confitem.multiple = false;
				confitem.readonly = false;
				break;
			case 'box6':
			case 'box12':
				 confitem = new box_object();
				confitem.title = gettext('未命名');
				confitem.idcounter = formobject.form_box_counter;
				confitem.color = 'box box-primary';
				break;
			case 'h_title':
				confitem = new h_title_object();
				confitem.title = gettext('標題');
				confitem.idcounter = formobject.form_item_counter;
				confitem.require = false;
				confitem.placeholder = '';
				confitem.type = 'inputbox';
				confitem.readonly = false;
				break;
			case 'h_status':
				confitem = new h_status_object();
				confitem.title = gettext('狀態');
				confitem.idcounter = formobject.form_item_counter;
				confitem.require = true;
				confitem.readonly = false;
				break;
			case 'h_level':
				confitem = new h_level_object();
				confitem.title = gettext('燈號');
				confitem.idcounter = formobject.form_item_counter;
				confitem.require = true;
				confitem.lists = [];
				var level_list0 = {};
				level_list0['value'] = 'green';
				level_list0['text'] = gettext('綠燈');
				var level_list1 = {};
				level_list1['value'] = 'yellow';
				level_list1['text'] = gettext('黃燈');
				var level_list2 = {};
				level_list2['value'] = 'red';
				level_list2['text'] = gettext('紅燈');
				confitem.lists.push(level_list0);
				confitem.lists.push(level_list1);
				confitem.lists.push(level_list2);
				confitem.readonly = false;
				break;
			case 'h_group':
				confitem = new h_group_object();
				confitem.idcounter = formobject.form_item_counter;
				confitem.group_title = gettext('組織');
				confitem.lists = [];
				confitem.value = '';
				confitem.require = true;
				confitem.user = true;
				confitem.user_title = gettext('受派人');
				confitem.user_require = false;
				confitem.readonly = false;
				break;
		}
		return confitem;
	}
	
	function box_button_add_item(item_id)
	{
		item_id = item_id.replace(active_id + '_' , '');
		
		var deafult_option = '<option selected="selected" value="inputbox">'+gettext('輸入方塊')+'</option>'
							+'<option value="areabox">'+gettext('多行輸入')+'</option>'
							+'<option value="list">'+gettext('下拉選單')+'</option>'
							+'<option value="checkbox">'+gettext('單選/複選選單')+'</option>';
		var header_option = '';
		var addtion_option = '<option value="box6">'+gettext('半區塊')+'</option>';
		
		if(!check_h_exist('h_title'))
		{
			header_option = header_option + '<option value="h_title">'+gettext('*標題')+'</option>';
		}
		if(!check_h_exist('h_status'))
		{
			header_option = header_option + '<option value="h_status">'+gettext('*狀態')+'</option>';
		}
		if(!check_h_exist('h_level'))
		{
			header_option = header_option + '<option value="h_level">'+gettext('*燈號')+'</option>';
		}
		if(!check_h_exist('h_group'))
		{
			header_option = header_option + '<option value="h_group">'+gettext('*受派人及組織')+'</option>';
		}
		
		formobject.items.forEach(function(item, index, array)
		{
			if(item.id == item_id)
			{
				action_item_for_modal = item;
				if(item.type == 'box6')
				{
					$('#' + baseID_NEW + '_item_select').html(deafult_option + header_option);
				}
				else
				{
					$('#' + baseID_NEW + '_item_select').html(addtion_option + deafult_option + header_option);
				}
			}
		});

		$('#' + baseID_NEW).modal('show');
	}
	
	function box_button_config_item(item_id)
	{
		item_id = item_id.replace(active_id + '_' , '');
		
		formobject.items.forEach(function(item, index, array)
		{
			if(item.id == item_id)
			{
				if((item.type == 'box6')||(item.type == 'box12'))
				{
					$('#' + baseID_BOX + '_item_title').val(item.config.title);
					$('#' + baseID_BOX + '_item_color').val(item.config.color).trigger('change');
					$('#' + baseID_BOX + '_item_hidden').prop("checked", item.hidden);
					action_item_for_modal = item;
					$('#' + baseID_BOX).modal('show');
				}
				else if(item.type == 'inputbox')
				{
					$('#' + baseID_INPUT + '_item_title').val(item.config.title);
					$('#' + baseID_INPUT + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_INPUT + '_item_placeholder').val(item.config.placeholder);
					$('#' + baseID_INPUT + '_item_type').val(item.config.type).trigger('change');
					$('#' + baseID_INPUT + '_item_value').val(item.config.value);
					$('#' + baseID_INPUT + '_item_regex').val(item.config.regex);
					$('#' + baseID_INPUT + '_item_hidden').prop("checked", item.hidden);
					$('#' + baseID_INPUT + '_item_readonly').prop("checked", item.config.readonly);
					action_item_for_modal = item;
					$('#' + baseID_INPUT ).modal('show');
				}
				else if(item.type == 'areabox')
				{
					$('#' + baseID_AREA + '_item_title').val(item.config.title);
					$('#' + baseID_AREA + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_AREA + '_item_rows').val(item.config.rows);
					$('#' + baseID_AREA + '_item_value').val(item.config.value);
					$('#' + baseID_AREA + '_item_regex').val(item.config.regex);
					$('#' + baseID_AREA + '_item_hidden').prop("checked", item.hidden);
					$('#' + baseID_AREA + '_item_readonly').prop("checked", item.config.readonly);
					action_item_for_modal = item;
					$('#' + baseID_AREA ).modal('show');
					
				}
				else if(item.type == 'list')
				{
					$('#' + baseID_LIST + '_item_title').val(item.config.title);
					$('#' + baseID_LIST + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_LIST + '_item_value').val(item.config.value);
					$('#' + baseID_LIST + '_item_hidden').prop("checked", item.hidden);
					$('#' + baseID_LIST + '_item_readonly').prop("checked", item.config.readonly);
					//clean all things
					$('#' + baseID_LIST + '_list_content').html('');
					//load object to real
					modal_load_dropdown(baseID_LIST , item , 'list');
					
					action_item_for_modal = item;
					$('#' + baseID_LIST ).modal('show');
					
				}
				else if(item.type == 'checkbox')
				{
					$('#' + baseID_CHECKBOX + '_item_title').val(item.config.title);
					$('#' + baseID_CHECKBOX + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_CHECKBOX + '_item_value').val(item.config.value);
					$('#' + baseID_CHECKBOX + '_item_hidden').prop("checked", item.hidden);
					$('#' + baseID_CHECKBOX + '_item_readonly').prop("checked", item.config.readonly);
					$('#' + baseID_CHECKBOX + '_item_multiple').prop("checked",item.config.multiple);
					//clean all things
					$('#' + baseID_CHECKBOX + '_checkbox_content').html('');
					//load object to real
					modal_load_dropdown(baseID_CHECKBOX , item , 'checkbox');
					
					action_item_for_modal = item;
					$('#' + baseID_CHECKBOX ).modal('show');
				}
				else if(item.type == 'h_title')
				{
					
					$('#' + baseID_HTITLE + '_item_title').val(item.config.title);
					$('#' + baseID_HTITLE + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_HTITLE + '_item_placeholder').val(item.config.placeholder);
					$('#' + baseID_HTITLE + '_item_value').val(item.config.value);
					$('#' + baseID_HTITLE + '_item_regex').val(item.config.regex);
					$('#' + baseID_HTITLE + '_item_hidden').prop("checked",item.hidden);
					$('#' + baseID_HTITLE + '_item_readonly').prop("checked",item.config.readonly);
					action_item_for_modal = item;
					$('#' + baseID_HTITLE ).modal('show');
					
				}
				else if(item.type == 'h_status')
				{
					$('#' + baseID_HSTATUS + '_item_title').val(item.config.title);
					$('#' + baseID_HSTATUS + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_HSTATUS + '_item_value').val(item.config.value);
					$('#' + baseID_HSTATUS + '_item_hidden').prop("checked",item.hidden);
					$('#' + baseID_HSTATUS + '_item_readonly').prop("checked",item.config.readonly);
					//clean all things
					$('#' + baseID_HSTATUS + '_status_content').html('');
					//load object to real
					modal_load_dropdown(baseID_HSTATUS , item , 'status');
					
					action_item_for_modal = item;
					$('#' + baseID_HSTATUS ).modal('show');
					
				}
				else if(item.type == 'h_level')
				{
					$('#' + baseID_HLEVEL + '_item_title').val(item.config.title);
					$('#' + baseID_HLEVEL + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_HLEVEL + '_item_value').val(item.config.value);
					$('#' + baseID_HLEVEL + '_item_hidden').prop("checked",item.hidden);
					$('#' + baseID_HLEVEL + '_item_readonly').prop("checked",item.config.readonly);
					//clean all things
					$('#' + baseID_HLEVEL + '_level_content').html('');
					//load object to real
					modal_load_dropdown(baseID_HLEVEL , item , 'level');
					
					action_item_for_modal = item;
					$('#' + baseID_HLEVEL ).modal('show');
					
				}
				else if(item.type == 'h_group')
				{
					$('#' + baseID_HGROUP + '_item_group_title').val(item.config.group_title);
					$('#' + baseID_HGROUP + '_item_user_title').val(item.config.user_title);
					$('#' + baseID_HGROUP + '_item_require').prop("checked", item.config.require);
					$('#' + baseID_HGROUP + '_item_user').prop("checked", item.config.user);
					$('#' + baseID_HGROUP + '_item_user_require').prop("checked", item.config.user_require);
					$('#' + baseID_HGROUP + '_item_value').val(item.config.value);
					$('#' + baseID_HGROUP + '_item_hidden').prop("checked",item.hidden);
					$('#' + baseID_HGROUP + '_item_readonly').prop("checked",item.config.readonly);
					//clean all things
					$('#' + baseID_HGROUP + '_group_content').html('');
					//load object to real
					modal_load_group(baseID_HGROUP , item );
					
					action_item_for_modal = item;
					$('#' + baseID_HGROUP ).modal('show');
					
				}
			}
		});
		
	}
	function box_button_remove_item(item_id)
	{
		item_id = item_id.replace(active_id + '_' , '');
		var item_mark = [];
		var box_mark = [];
		var sub_box = [];
		sub_box.push(item_id);
		do
		{
			mark_id = sub_box[0];
			sub_box.shift();
				
			formobject.items.forEach(function(item, index, array)
			{
				if(item.id == mark_id)
				{
					if(item.type.startsWith("box"))
					{
						box_mark.push(item.id);
					}
					else
					{
						item_mark.push(item.id);
					}
					//formobject.items.splice(index,1);
					//$('#' + active_id + '_' + item.id).remove();
				}
				if(item.parent == mark_id)
				{
					if(item.type.startsWith("box"))
					{
						//have sub box
						box_mark.push(item.id);
						sub_box.push(item.id);
					}
					else
					{
						item_mark.push(item.id);
					}
					//box_button_remove_item(item.id);
				}
			});
		}while(sub_box.length > 0);
		
		//start 
		item_mark.forEach(function(remove_item)
		{
			formobject.items.forEach(function(item,index)
			{
				if(item.id == remove_item)
				{
					formobject.items.splice(index,1);
					$('#' + active_id + '_' + item.id).remove();
				}
			});
		});
		box_mark.forEach(function(remove_item)
		{
			formobject.items.forEach(function(item,index)
			{
				if(item.id == remove_item)
				{
					formobject.items.splice(index,1);
					$('#' + active_id + '_' + item.id).remove();
				}
			});
		});
		
		
	}
	function modal_load_dropdown(baseID , item , keyword)
	{
		item.config.lists.forEach(function(dropdown_item, index) 
		{
			if(keyword == 'level')
			{
				dropdown_sortable_add_readonly(baseID + '_' + keyword + '_content');
			}
			else
			{
				dropdown_sortable_add(baseID + '_' + keyword + '_content');
			}
			$('#' + baseID + '_' + keyword + '_content' + '_value_' + index).val(dropdown_item.value);
			$('#' + baseID + '_' + keyword + '_content' + '_text_' + index).val(dropdown_item.text);
		});
	}
	function modal_load_group(baseID , item)
	{
		item.config.lists.forEach(function(dropdown_item, index) 
		{
			group_sortable_add(baseID_HGROUP +  '_group_content'); 

			$('#' + baseID_HGROUP + '_group_content' + '_value_' + index).val(dropdown_item.value).trigger('change');
			$('#' + baseID_HGROUP + '_group_content' + '_text_' + index).val(dropdown_item.text);
		});
	}
	function modal_save_dropdown(baseID , item, keyword) 
	{
		item.config.lists = [];
		$('[id^=' + baseID + '_' + keyword + '_content' + '_li_]').each(function()
		{
			var my_id = $(this).attr('id');
			var item_list = {};
			item_list['value'] = $('#' + my_id.replace('_li_','_value_')).val();
			item_list['text'] = $('#' + my_id.replace('_li_','_text_')).val();
			item.config.lists.push(item_list);
		});
		
		if(item.type == 'checkbox')
		{
			$('#' + active_id + '_' + item.id + '_item' ).html(dropdown_array_to_checkbox(item));
		}
		else if(item.type == 'h_group')
		{
			$('#' + active_id + '_' + item.id + '_group_item' ).html(dropdown_array_to_group(item,false));
		}
		else
		{
			$('#' + active_id + '_' + item.id + '_item' ).html(dropdown_array_to_option(item));
		}
	}
	function modal_config_box_submit()
	{
		item = action_item_for_modal;

		if((item.type == 'box6')||(item.type == 'box12'))
		{
			//get modal data
			item.config.color = $('#' + baseID_BOX + '_item_color').val();
			item.config.title = $('#' + baseID_BOX + '_item_title').val();
			item.hidden = $('#' + baseID_BOX + '_item_hidden').prop("checked");
			//change ui object
			$('#' + active_id + '_' + item.id + '_color').attr('class',item.config.color) ;
			$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			$('#' + baseID_BOX ).modal('hide');
		}
		else if(item.type == 'inputbox')
		{
			//get modal data
			item.config.title = $('#' + baseID_INPUT + '_item_title').val();
			item.config.require = $('#' + baseID_INPUT + '_item_require').prop("checked");
			item.config.placeholder = $('#' + baseID_INPUT + '_item_placeholder').val();
			item.config.type = $('#' + baseID_INPUT + '_item_type').val();
			item.config.value = $('#' + baseID_INPUT + '_item_value').val();
			item.config.regex = $('#' + baseID_INPUT + '_item_regex').val();
			item.hidden = $('#' + baseID_INPUT + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_INPUT + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			}
			$('#' + active_id + '_' + item.id + '_item').attr('placeholder',item.config.placeholder);
			$('#' + active_id + '_' + item.id + '_item').prop('type',item.config.type);
			$('#' + active_id + '_' + item.id + '_item').prop('readonly',item.config.readonly);
			
			$('#' + baseID_INPUT ).modal('hide');
		}
		else if(item.type == 'areabox')
		{
			//get modal data
			item.config.title = $('#' + baseID_AREA + '_item_title').val();
			item.config.require = $('#' + baseID_AREA + '_item_require').prop("checked");
			item.config.rows = $('#' + baseID_AREA + '_item_rows').val();
			item.config.value = $('#' + baseID_AREA + '_item_value').val();
			item.config.regex = $('#' + baseID_AREA + '_item_regex').val();
			item.hidden = $('#' + baseID_AREA + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_AREA + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			}
			$('#' + active_id + '_' + item.id + '_item').prop('rows',item.config.rows);
			$('#' + active_id + '_' + item.id + '_item').prop('readonly',item.config.readonly);
			$('#' + baseID_AREA ).modal('hide');
		}
		else if(item.type == 'list')
		{
			//get modal data
			item.config.title = $('#' + baseID_LIST + '_item_title').val();
			item.config.require = $('#' + baseID_LIST + '_item_require').prop("checked");
			item.config.value = $('#' + baseID_LIST + '_item_value').val();
			item.hidden = $('#' + baseID_LIST + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_LIST + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			}
			
			if(item.config.readonly)
			{
				$('#' + active_id + '_' + item.id + '_item').select2({disabled:true});
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_item').select2({disabled:false});
			}
			
			modal_save_dropdown(baseID_LIST,item  , 'list');
			
			$('#' + baseID_LIST ).modal('hide');
		}
		else if(item.type == 'checkbox')
		{
			//get modal data
			item.config.title = $('#' + baseID_CHECKBOX + '_item_title').val();
			item.config.require = $('#' + baseID_CHECKBOX + '_item_require').prop("checked");
			item.config.multiple = $('#' + baseID_CHECKBOX + '_item_multiple').prop("checked");
			item.config.value = $('#' + baseID_CHECKBOX + '_item_value').val();
			item.hidden = $('#' + baseID_CHECKBOX + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_CHECKBOX + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			}
			
			modal_save_dropdown(baseID_CHECKBOX,item  , 'checkbox');
			
			$('#' + baseID_CHECKBOX ).modal('hide');
		}
		else if(item.type == 'h_title')
		{
			//get modal data
			item.config.title = $('#' + baseID_HTITLE + '_item_title').val();
			item.config.placeholder = $('#' + baseID_HTITLE + '_item_placeholder').val();
			item.config.require = $('#' + baseID_HTITLE + '_item_require').prop("checked");
			item.config.value = $('#' + baseID_HTITLE + '_item_value').val();
			item.config.regex = $('#' + baseID_HTITLE + '_item_regex').val();
			item.hidden = $('#' + baseID_HTITLE + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_HTITLE + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			}
			$('#' + active_id + '_' + item.id + '_item').attr('placeholder',item.config.placeholder);
			$('#' + active_id + '_' + item.id + '_item').prop('type',item.config.type);
			$('#' + active_id + '_' + item.id + '_item').prop('readonly',item.config.readonly);
			
			$('#' + baseID_HTITLE ).modal('hide');
		}
		else if(item.type == 'h_status')
		{
			//get modal data
			item.config.title = $('#' + baseID_HSTATUS + '_item_title').val();
			item.config.require = $('#' + baseID_HSTATUS + '_item_require').prop("checked");
			item.config.value = $('#' + baseID_HSTATUS + '_item_value').val();
			item.hidden = $('#' + baseID_HSTATUS + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_HSTATUS + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			}
			if(item.config.readonly)
			{
				$('#' + active_id + '_' + item.id + '_item').select2({disabled:true});
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_item').select2({disabled:false});
			}
			
			modal_save_dropdown(baseID_HSTATUS,item  , 'status');
			
			$('#' + baseID_HSTATUS ).modal('hide');
		}
		else if(item.type == 'h_level')
		{
			//get modal data
			item.config.title = $('#' + baseID_HLEVEL + '_item_title').val();
			item.config.require = $('#' + baseID_HLEVEL + '_item_require').prop("checked");
			item.config.value = $('#' + baseID_HLEVEL + '_item_value').val();
			item.hidden = $('#' + baseID_HLEVEL + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_HLEVEL + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_title').html(item.config.title) ;
			}
			if(item.config.readonly)
			{
				$('#' + active_id + '_' + item.id + '_item').select2({disabled:true});
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_item').select2({disabled:false});
			}
			
			modal_save_dropdown(baseID_HLEVEL,item , 'level');
			
			$('#' + baseID_HLEVEL ).modal('hide');
		}
		else if(item.type == 'h_group')
		{
			//get modal data
			item.config.group_title = $('#' + baseID_HGROUP + '_item_group_title').val();
			item.config.value = $('#' + baseID_HGROUP + '_item_value').val();
			item.config.require = $('#' + baseID_HGROUP + '_item_require').prop("checked");
			item.config.user = $('#' + baseID_HGROUP + '_item_user').prop("checked");
			item.config.user_title = $('#' + baseID_HGROUP + '_item_user_title').val();
			item.config.user_require = $('#' + baseID_HGROUP + '_item_user_require').prop("checked");
			item.hidden = $('#' + baseID_HGROUP + '_item_hidden').prop("checked");
			item.config.readonly = $('#' + baseID_HGROUP + '_item_readonly').prop("checked");
			//change ui object
			if(item.config.require)
			{
				$('#' + active_id + '_' + item.id + '_group_title').html(item.config.group_title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_group_title').html(item.config.group_title) ;
			}
			if(item.config.user_require)
			{
				$('#' + active_id + '_' + item.id + '_user_title').html(item.config.user_title + '<font color="red">*</font>') ;
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_user_title').html(item.config.user_title) ;
			}
			
			if(item.config.user)
			{
				$('#' + active_id + '_' + item.id + '_user_title').css('display','');
				$('#' + active_id + '_' + item.id + '_user_item').css('display','');
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_user_title').css('display','none');
				$('#' + active_id + '_' + item.id + '_user_item').css('display','none');
			}
			
			if(item.config.readonly)
			{
				$('#' + active_id + '_' + item.id + '_user_item').select2({disabled:true});
				$('#' + active_id + '_' + item.id + '_group_item').select2({disabled:true});
			}
			else
			{
				$('#' + active_id + '_' + item.id + '_user_item').select2({disabled:false});
				$('#' + active_id + '_' + item.id + '_group_item').select2({disabled:false});
			}


			modal_save_dropdown(baseID_HGROUP ,item  ,'group');
			
			
			$('#' + baseID_HGROUP ).modal('hide');
		}
		
	}		
		
	//===drop drag
	_self_.boxdrag = function(ev)
	{
		ev.dataTransfer.setData("text", ev.target.id.replace(active_id + '_' , ''));
	}
	_self_.boxdrop = function(ev)
	{
		ev.preventDefault();
		var target_id = ev.target.id;
		var source_id = ev.dataTransfer.getData("text");
		var move_record = [];
		target_id = target_id.replace('_item','').replace('_title','').replace('_color','').replace(active_id + '_' , '').replace('select2-','').replace('-container','');
		
		//fix target to box
		if(target_id.indexOf('FORMBOX') >= 0)
		{
			
		}
		else
		{
			formobject.items.forEach(function(item)
			{
				if(item.id == target_id)
				{
					target_id = item.parent;
				}
			});
		}
		
		
		//starting move
		if(source_id.indexOf('FORMBOX') >= 0)
		{
			//box move
			if((target_id != source_id)&&(target_id != ''))
			{	
				formobject.items.forEach(function(item1)
				{
					if(item1.id == source_id)
					{
						item1.parent = target_id;
						$('#' + active_id + '_' + source_id).remove();
						item_create(item1);
						move_record.push(item1.id);
						formobject.items.forEach(function(item2)
						{
							if(item2.parent == source_id)
							{
								$('#' + active_id + '_' + item2.id).remove();
								item_create(item2);
								move_record.push(item2.id);
								formobject.items.forEach(function(item3)
								{
									if(item3.parent == item2.id)
									{
										$('#' + active_id + '_' + item3.id).remove();
										item_create(item3);
										move_record.push(item3.id);
										formobject.items.forEach(function(item4)
										{
											if(item4.parent == item3.id)
											{
												$('#' + active_id + '_' + item4.id).remove();
												item_create(item4);
												move_record.push(item4.id);
											}
										});
									}
								});
							}
						});
					}
				});
			}
			
		}
		else
		{
			//item move
			if((target_id != source_id)&&(target_id != ''))
			{	
				formobject.items.forEach(function(item)
				{
					if(item.id == source_id)
					{
						item.parent = target_id;
						$('#' + active_id + '_' + source_id).remove();
						item_create(item);
						move_record.push(item.id);
					}
				});
			}
		}
		
		//reorder
		var tmp_item = null;
		move_record.forEach(function(item_id)
		{
			formobject.items.forEach(function(item,index)
			{
				if(item.id == item_id)
				{
					tmp_item = JSON.parse(JSON.stringify(item));
					formobject.items.splice(index,1);
					
				}
			});
			formobject.items.push(tmp_item);
		});
		
	};
	
	
	_self_.boxAllowDrop = function(ev)
	{
		ev.preventDefault();
	}
	
	_self_.event_group_list = function(function_name)
	{
		event_get_group_list_callback = function_name;
	}
	_self_.event_user_list = function(function_name)
	{
		event_get_user_list_callback = function_name;
	}
	/**
	 * put form data
	 * input: 
	 * return:[{id,value},...] 
	 * author:Pen Lin
	 */
	_self_.setData = function(data_values)
	{
		data_values.forEach(function(item, index, array)
		{
			switch(item.type)
			{
				case 'inputbox':
				case 'areabox':
				case 'h_title':
					$('#' + active_id + '_' + item.id + '_item').val(item.value);
					break;
				case 'h_status':
				case 'list':
				case 'h_level':
					$('#' + active_id + '_' + item.id + '_item').val(item.value).trigger('change');
					break;
				case 'h_group':
					$('#' + active_id + '_' + item.id + '_group_item').val(item.value.group).trigger('change');
					$('#' + active_id + '_' + item.id + '_user_item').val(item.value.user).trigger('change');
					break;
				case 'checkbox':
					$('input[name="' + active_id + '_' + item.id + '_item"][value="' + item.value[0] + '"]').prop("checked", true);
					$('input[name="' + active_id + '_' + item.id + '_item[]"]').each(function () 
					{
						$(this).prop("checked", ($.inArray($(this).val(), item.value) != -1));
					});
					break;
			}
		});
	}
	/**
	 * get form data from ui
	 * input: 
	 * return:[{id,value},...] 
	 * author:Pen Lin
	 */
	_self_.getData = function()
	{
		//必填欄位為空值時要處理(JOB)
		var data = {};
		data["checker"] = [];
		data["values"] =  [];
		var checker = [];
		formobject.items.forEach(function(item, index, array)
		{
			if(item.type.startsWith("box"))
			{
				//no
			}
			else
			{
				switch(item.type)
				{
					case 'inputbox':
					case 'areabox':
					case 'list':
						var obj  = $('#' + active_id + '_' + item.id + '_item');
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = obj.val();
						item_data['type'] = item.type;
						data.values.push(item_data);
						if(item.config.require)
						{
							if(item_data['value'] == null)
							{
								checker.push(item.id);
							}
							else
							{
								if(item_data['value'] == '')
								{
									checker.push(item.id);
								}
							}
						}
						break;
					case 'checkbox':
						var item_data = {};
						var values = [];
						item_data['id'] = item.id;
						item_data['type'] = item.type;
						item_data['value'] = [];
						if(item.config.multiple)
						{
							values= $('input[name="' + active_id + '_' + item.id + '_item[]"]:checked').map(function() { return $(this).val(); }).get();
						}
						else
						{
							values= [];
							if($('input[name="' + active_id + '_' + item.id + '_item"]:checked').length)
								values.push($('input[name="' + active_id + '_' + item.id + '_item"]:checked').val());
						}
						item_data['value'] = values;
						data.values.push(item_data);
						
						if(item.config.require)
						{
							if(item_data['value'].length == 0)
							{
								checker.push(item.id);
							}
						}
						break;
					case 'h_level':
						var obj  = $('#' + active_id + '_' + item.id + '_item');
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = obj.val();
						item_data['type'] = item.type;
						data.values.push(item_data);
						//
						var header_item_data = {};
						header_item_data['id'] = 'level';
						header_item_data['value'] = obj.val();
						header_item_data['type'] = 'header';
						data.values.push(header_item_data);
						if(item.config.require)
						{
							if(item_data['value'] == null)
							{
								checker.push(item.id);
							}
							else
							{
								if(item_data['value'] == '')
								{
									checker.push(item.id);
								}
							}
						}
						break;
					case 'h_title':
						var obj  = $('#' + active_id + '_' + item.id + '_item');
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = obj.val();
						item_data['type'] = item.type;
						data.values.push(item_data);
						//
						var header_item_data = {};
						header_item_data['id'] = 'title';
						header_item_data['value'] = obj.val();
						header_item_data['type'] = 'header';
						data.values.push(header_item_data);
						if(item.config.require)
						{
							if(item_data['value'] == null)
							{
								checker.push(item.id);
							}
							else
							{
								if(item_data['value'] == '')
								{
									checker.push(item.id);
								}
							}
						}
						break;
					case 'h_status':
						var obj  = $('#' + active_id + '_' + item.id + '_item');
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = obj.val();
						item_data['type'] = item.type;
						data.values.push(item_data);

						var header_item_data = {};
						header_item_data['id'] = 'status';
						header_item_data['value'] = '';
						item.config.lists.forEach(function(list_item)
						{
							if(list_item.value == item_data['value'])
							{
								header_item_data['value'] = list_item.text;
							}
						});
						
						header_item_data['type'] = 'header';
						data.values.push(header_item_data);
						if(item.config.require)
						{
							if(item_data['value'] == null)
							{
								checker.push(item.id);
							}
							else
							{
								if(item_data['value'] == '')
								{
									checker.push(item.id);
								}
							}
						}
						break;
					case 'h_group':
						var obj1  = $('#' + active_id + '_' + item.id + '_group_item');
						var obj2  = $('#' + active_id + '_' + item.id + '_user_item');
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = {'group':obj1.val(),'user':obj2.val()};
						item_data['type'] = item.type;
						data.values.push(item_data);
						var header_item_data = {};
						header_item_data['id'] = 'group';
						header_item_data['value'] = {'group':obj1.val(),'user':obj2.val()};
						header_item_data['type'] = 'header';
						data.values.push(header_item_data);
						var require_checker = false;
						
						if(item.config.user_require)
						{
							if(item_data['value'].user == null)
							{
								require_checker = true;
								checker.push(item.id);
							}
							else
							{
								if(item_data['value'].user == '')
								{
									require_checker = true;
									checker.push(item.id);
								}
							}
						}
						if(!require_checker)
						{
							if(item.config.require)
							{
								if(item_data['value'].group == null)
								{
									require_checker = true;
									checker.push(item.id);
								}
								else
								{
									if(item_data['value'].group == '')
									{
										require_checker = true;
										checker.push(item.id);
									}
								}
							}
						}
						break;
				}
			}
		});
		
		data.checker = checker;
		return data;
	}
	/**
	 * get form data from ui
	 * input: 
	 * return:[{id,value},...] 
	 * author:Pen Lin
	 */
	_self_.getDefaultData = function(obj)
	{
		var data = [];
		obj.items.forEach(function(item)
		{
			if(!item.type.startsWith("box"))
			{
				switch(item.type)
				{
					case 'inputbox':
					case 'areabox':
					case 'list':
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = item.config.value;
						item_data['type'] = item.type;
						data.push(item_data);
						break;
					case 'checkbox':
						var item_data = {};
						var values = [];
						item_data['id'] = item.id;
						item_data['type'] = item.type;
						item_data['value'] = item.config.value.split(',');
						data.push(item_data);
						break;
					case 'h_level':
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = item.config.value;
						item_data['type'] = item.type;
						data.push(item_data);
						//
						var header_item_data = {};
						header_item_data['id'] = 'level';
						header_item_data['value'] = item.config.value;
						header_item_data['type'] = 'header';
						data.push(header_item_data);
						break;
					case 'h_title':
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = item.config.value;
						item_data['type'] = item.type;
						data.push(item_data);
						//
						var header_item_data = {};
						header_item_data['id'] = 'title';
						header_item_data['value'] = item.config.value;
						header_item_data['type'] = 'header';
						data.push(header_item_data);
						break;
					case 'h_status':
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = item.config.value;
						item_data['type'] = item.type;
						data.push(item_data);
						//
						var header_item_data = {};
						header_item_data['id'] = 'status';
						header_item_data['value'] = item.config.value;
						header_item_data['type'] = 'header';
						data.push(header_item_data);
						break;
					case 'h_group':
						var obj1  = '';
						var obj2  = '';
						var obj =  item.config.value.split(',');
						if(obj.length >= 2)
						{
							obj1 = obj[0];
							obj2 = obj[1];
						}
						else
						{
							obj1 = obj[0];
						}
						var item_data = {};
						item_data['id'] = item.id;
						item_data['value'] = {'group':obj1,'user':obj2};
						item_data['type'] = item.type;
						data.push(item_data);
						var header_item_data = {};
						header_item_data['id'] = 'group';
						header_item_data['value'] = {'group':obj1,'user':obj2};
						header_item_data['type'] = 'header';
						data.push(header_item_data);
						break;
				}
			}
		});
		
		
		return data;
	}
}	



