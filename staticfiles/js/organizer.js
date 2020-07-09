/**
 * SYSCOM OMFLOW FLOW ENGINE
 * for Organizer diagram design ui 
 * 2020/5/21 beta
 * author:Pen Lin
 * ------------------
 */
var organizer = function(div_id)
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
	var orgobject = null;
	var orgcontent = $('#' + div_id);
	var action_item_for_modal = null;
	var event_get_group_list_callback = null;
	var event_get_role_list_callback = null;
	var event_get_user_list_callback = null;
	var group_tree_data_uuid =[];
	
	var selected_source_chart_item = null;
	var selected_target_chart_item = null;
	var selected_ball = '';
	var event_chart_selected_callback = null;
	
	
	var design_mode = false;

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
	var item_content_button_copy = '<button id="' + active_id + '_item_copy__pid_" class="btn btn-box-tool pull-left"><i class="fa fa-plus"></i></button>';
	

	var item_content_style_dept = 'left:0px;width: 120px;height: 60px;background-color: #19B3B1;border-radius: 5px;margin: 0px auto 0;';
	var item_content_style_role = 'left:0px;width: 120px;height: 60px;background-color: #BC5F6A;border-radius: 5px;margin: 0px auto 0;';
	var item_content_style_people = 'left:0px;width: 120px;height: 60px;background-color: #E3A6A1;border-radius: 5px;margin: 0px auto 0;';

	
	//====================
	//===MODAL NAME ID==
	//====================
	var baseID_NEW = active_id + '_' + 'add_chart_modal';
	var baseID_DEPT = active_id + '_' + 'dept_chart_modal';
	var baseID_ROLE = active_id + '_' + 'role_chart_modal';
	var baseID_PEOPLE = active_id + '_' + 'people_chart_modal';

	
	//====================
	//===public method====
	//====================
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
		orgobject = org_object();
		orgobject.uid = uid;
		orgcontent.css('overflow','scroll');
		orgcontent.css('position','relative');
		//orgcontent.css('background','blue');
		if ($('#' + active_id + '_ball_left').length == 0)
		{
			orgcontent.append(box_ball_content);
			
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
						+'   <h4 class="modal-title"> ' + gettext('新增項目') + '</h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_NEW + '_item" data-toggle="tab">' + gettext('項目') + '</a></li>'
						+'    </ul>'
						
						+'    <div class="tab-content">'

						+'     <div class="tab-pane active" id="' + baseID_NEW + '_item">'

						+'      <div class="table-responsive" style="z-index:1001">'
						+'      <table class="table no-margin">'
						+'      <thead><tr><th>' + gettext('項目') + '</th><th>' + gettext('說明') + '</th></tr></thead>'
						+'      <tbody>'
						+'      <tr>'
						+'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_dept" class="iradio_minimal-blue" value="dept" checked><label for="' + baseID_NEW + '_dept"></label><b>  <i class="fas fa-share"></i>  '+gettext('部門組織')+'</b></td>'
						+'      <td>'+gettext('建立新的組織部門。')+'</td>'
						+'      </tr>'						
						+'      <tr>'
						+'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_role" class="iradio_minimal-blue" value="role"><label for="' + baseID_NEW + '_role"></label><b>  <i class="fa fa-play-circle-o"></i>  '+gettext('職務')+'</b></td>'
						+'      <td>'+gettext('建立新的職務。')+'</td>'
						+'      </tr>'	
						+'      <tr>'
						+'      <td><input type="radio" name="' + baseID_NEW + '_options" id="' + baseID_NEW + '_people" class="iradio_minimal-blue" value="people"><label for="' + baseID_NEW + '_people"></label><b>  <i class="fab fa-python"></i>  '+gettext('人員')+'</b></td>'
						+'      <td>'+gettext('新增人員。')+'</td>'
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
			orgcontent.append(modal_add_item);
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
		//===MODAL CHART DEPT
		//====================
		if ($('#' + baseID_DEPT).length == 0)
		{
			var modal_DEPT = '<div class="modal fade" id="' + baseID_DEPT + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('部門組織-')+'<span id="' + baseID_DEPT + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_DEPT + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'    </ul>'
						+'    <div class="tab-content">'
						+'     <div class="tab-pane active" id="' + baseID_DEPT + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('部門組織')+'</label>'
						+'       <select id="' + baseID_DEPT + '_config_value" class="form-control select2" placeholder="'+gettext('輸入資料')+'" style="width:100%"></select>'
						+'      </div>'
						+'     </div>'
						+'    </div>'
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_DEPT + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_DEPT + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			orgcontent.append(modal_DEPT);
			//====================
			//===MODAL INIT
			//====================
			
			$('#' +  baseID_DEPT + '_config_value').html(dropdown_array_to_group(null,true));
            $('#' +  baseID_DEPT + '_config_value').select2ToTree({language: {noResults: function (params) {return " ";}}});


			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_DEPT + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_DEPT + '_config_value').select2('data')[0].text;
                item.config.noid = $('#' + baseID_DEPT + '_config_value').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);		
				$('#' + baseID_DEPT).modal('hide');
			});
			$('#' +  baseID_DEPT + '_close').click(function ()
			{
				$('#' + baseID_DEPT).modal('hide');
			});
		}
		//====================
		//===MODAL CHART ROLE
		//====================
		if ($('#' + baseID_ROLE).length == 0)
		{
			var modal_ROLE = '<div class="modal fade" id="' + baseID_ROLE + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('職務-')+'<span id="' + baseID_ROLE + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_ROLE + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'    </ul>'
						+'    <div class="tab-content">'
						+'     <div class="tab-pane active" id="' + baseID_ROLE + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('職務')+'</label>'
						+'       <select id="' + baseID_ROLE + '_config_value" class="form-control select2" placeholder="'+gettext('輸入資料')+'" style="width:100%"></select>'
						+'      </div>'
						+'     </div>'
						+'    </div>'
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_ROLE + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_ROLE + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			orgcontent.append(modal_ROLE);
			//====================
			//===MODAL INIT
			//====================
			var role_data_source = [];
			var role_option = '';
			if(event_get_role_list_callback == null)
			{
				//no function assign
				role_data_source = 
						[
							{id: 1, display_name: "預算主管"},
							{id: 2, display_name: "主管"},
							{id: 7, display_name: "工程師"},
							{id: 3, display_name: "一般員工"},
							{id: 6, display_name: "經理"},
							{id: 5, display_name: "處長"}
						];
			}
			else
			{
				role_data_source = event_get_role_list_callback();
			}
			role_data_source.forEach(function(option_item)
			{
				role_option = role_option + '<option value="' + option_item.id + '">' + option_item.display_name + '</option>'
			});
			$('#' +  baseID_ROLE + '_config_value').html(role_option);
            $('#' +  baseID_ROLE + '_config_value').select2({tags: false , placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});

			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_ROLE + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_ROLE + '_config_value').select2('data')[0].text;
                item.config.noid = $('#' + baseID_ROLE + '_config_value').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);		
				$('#' + baseID_ROLE).modal('hide');
			});
			$('#' +  baseID_ROLE + '_close').click(function ()
			{
				$('#' + baseID_ROLE).modal('hide');
			});
		}
		//====================
		//===MODAL CHART PEOPLE
		//====================
		if ($('#' + baseID_PEOPLE).length == 0)
		{
			var modal_PEOPLE = '<div class="modal fade" id="' + baseID_PEOPLE + '">'
						+'<div class="modal-dialog modal-lg modal-dialog-scrollable">'
						+' <div class="modal-content">'
						+'  <div class="modal-header">'
						+'   <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
						+'   <h4 class="modal-title"> '+gettext('人員-')+'<span id="' + baseID_PEOPLE + '_id"></span></h4>'
						+'  </div>'
						+'  <div class="modal-body">'
						+'   <div class="nav-tabs-custom">'
						+'    <ul class="nav nav-tabs">'
						+'     <li class="active"><a href="#' + baseID_PEOPLE + '_config" data-toggle="tab">'+gettext('設定')+'</a></li>'
						+'    </ul>'
						+'    <div class="tab-content">'
						+'     <div class="tab-pane active" id="' + baseID_PEOPLE + '_config">'
						+'      <div class="form-group has-warning" >'
						+'       <label> '+gettext('人員')+'</label>'
						+'       <select id="' + baseID_PEOPLE + '_config_value" class="form-control select2" placeholder="'+gettext('輸入資料')+'" style="width:100%"></select>'
						+'      </div>'
						+'     </div>'
						+'    </div>'
						+'   </div>'
						+'  </div>'
						+'  <div class="modal-footer">'
						+'   <button type="button" class="btn btn-default pull-left" id="' + baseID_PEOPLE + '_close">'+gettext('取消')+'</button>'
						+'   <button type="button" class="btn btn-primary"  id="' + baseID_PEOPLE + '_submit">'+gettext('確定')+'</button>'
						+'  </div>'
						+' </div>'
						+'</div>'
						+'</div>';

			orgcontent.append(modal_PEOPLE);
			//====================
			//===MODAL INIT
			//====================
			var user_data_source = [];
			var user_option = '';
			if(event_get_user_list_callback == null)
			{
				//no function assign
				user_data_source = 
						[
							{id: 1, nick_name: "林先生"},
							{id: 2, nick_name: "李先生"},
							{id: 7, nick_name: "張小姐"},
							{id: 3, nick_name: "王先生"},
							{id: 6, nick_name: "徐先生"},
							{id: 5, nick_name: "池先生"}
						];
			}
			else
			{
				user_data_source = event_get_user_list_callback();
			}
			user_data_source.forEach(function(option_item)
			{
				user_option = user_option + '<option value="' + option_item.id + '">' + option_item.nick_name + '</option>'
			});
			$('#' +  baseID_PEOPLE + '_config_value').html(user_option);
            $('#' +  baseID_PEOPLE + '_config_value').select2({tags: false , placeholder: '',allowClear: true,dropdownAutoWidth: true, language: {noResults: function (params) {return " ";}}});

			//====================
			//===MODAL EVENT SAVE 
			//====================
			$('#' +  baseID_PEOPLE + '_submit').click(function ()
			{
				item = action_item_for_modal;
				//save real to object
				item.text = $('#' + baseID_PEOPLE + '_config_value').select2('data')[0].text;
                item.config.noid = $('#' + baseID_PEOPLE + '_config_value').val();
				$('#' + active_id + '_itext_content_' + item.id).html(item.text);		
				$('#' + baseID_PEOPLE).modal('hide');
			});
			$('#' +  baseID_PEOPLE + '_close').click(function ()
			{
				$('#' + baseID_PEOPLE).modal('hide');
			});
		}
//    _self_.load('{"version":16777216,"flow_item_counter":6,"flow_line_counter":5,"max_dept_noid":0,"max_role_noid":0,"max_people_noid":0,"uid":1590119080512,"form_object":{"items":[]},"is_sub":false,"subflow":[],"items":[{"id":"FITEM_1","type":"dept","text":"凌群電腦","left":0,"top":0,"config":{"top":25,"left":270}},{"id":"FITEM_2","type":"dept","text":"技術中心","left":0,"top":0,"config":{"top":150,"left":120}},{"id":"FITEM_3","type":"role","text":"主管","left":0,"top":0,"config":{"top":250,"left":30}},{"id":"FITEM_4","type":"role","text":"工程師","left":0,"top":0,"config":{"top":250,"left":210}},{"id":"FITEM_5","type":"people","text":"張小姐","left":0,"top":0,"config":{"top":350,"left":30}},{"id":"FLINE_MW1","type":"line","config":{"target_side":"top","source_side":"bottom","target_item":"FITEM_5","source_item":"FITEM_3","idcounter":1,"linebox_left":90,"linebox_top":350,"linebox_long":0,"linebox_top_width":20,"linebox_bottom_width":-20,"linebox_arrow_top":360,"linebox_arrow_left":86}},{"id":"FITEM_6","type":"people","text":"王先生","left":0,"top":0,"config":{"top":350,"left":210}},{"id":"FLINE_MW2","type":"line","config":{"target_side":"top","source_side":"bottom","target_item":"FITEM_6","source_item":"FITEM_4","idcounter":2,"linebox_left":270,"linebox_top":350,"linebox_long":0,"linebox_top_width":20,"linebox_bottom_width":-20,"linebox_arrow_top":360,"linebox_arrow_left":266}},{"id":"FLINE_MW3","type":"line","config":{"target_side":"top","source_side":"bottom","target_item":"FITEM_3","source_item":"FITEM_2","idcounter":3,"linebox_left":90,"linebox_top":250,"linebox_long":90,"linebox_top_width":20,"linebox_bottom_width":-20,"linebox_arrow_top":260,"linebox_arrow_left":86}},{"id":"FLINE_MW4","type":"line","config":{"target_side":"top","source_side":"bottom","target_item":"FITEM_4","source_item":"FITEM_2","idcounter":4,"linebox_left":180,"linebox_top":250,"linebox_long":90,"linebox_top_width":-20,"linebox_bottom_width":20,"linebox_arrow_top":260,"linebox_arrow_left":266}},{"id":"FLINE_MW5","type":"line","config":{"target_side":"top","source_side":"bottom","target_item":"FITEM_2","source_item":"FITEM_1","idcounter":5,"linebox_left":180,"linebox_top":137.5,"linebox_long":150,"linebox_top_width":32.5,"linebox_bottom_width":-32.5,"linebox_arrow_top":160,"linebox_arrow_left":176}}]}');
        
	}
	
	
	
	_self_.setFocus = function(obj_id)
	{
		
		item_select($('#' + active_id + '_' + 'chart_' + obj_id) , true);
	}
	_self_.event_group_list = function(function_name)
	{
		event_get_group_list_callback = function_name;
	}
	_self_.event_role_list = function(function_name)
	{
		event_get_role_list_callback = function_name;
	}
	_self_.event_user_list = function(function_name)
	{
		event_get_user_list_callback = function_name;
	}
	
	/**
	 * create a new workflow item 
	 * input: item type:start , end , process , outside , select , async , collection
	 * return: 
	 * author:Pen Lin
	 */
	_self_.getName = function()
	{
		return orgobject.name;
	}
	_self_.setName = function(new_name)
	{
		orgobject.name = new_name;
	}
	_self_.getDes = function()
	{
		return orgobject.description;
	}
	_self_.setDes = function(new_des)
	{
		orgobject.description = new_des;
	}
	_self_.getUID = function()
	{
		return orgobject.uid;
	}
	_self_.setUID = function(new_uid)
	{
		orgobject.uid = new_uid;
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
		orgobject.flow_item_counter++;
		item.id = "FITEM_" + orgobject.flow_item_counter;
		item.text = '';
		item.type = item_type;
		item.top = 0;
		item.left = 0;
		switch(item.type)
		{
			case 'dept':
				item.text = gettext('新組織');
				item.config = new dept_object();
				break;
			case 'role':
				item.text = gettext('新職務');
				item.config = new role_object();
				break;
			case 'people':
				item.text = gettext('新人員');
				item.config = new people_object();		
				break;

		}
		orgobject.items.push(item);
		item_create(item);
	}

	/**
	 * get flow design by string
	 * input:
	 * return: string
	 * author:Pen Lin
	 */
	_self_.toString = function()
	{
		if(orgobject.is_sub == true)
		{
			var obj = JSON.parse(JSON.stringify(orgobject));
			obj.subflow = [];
			obj.form_object = {};
			return JSON.stringify(obj);
		}
		else
		{
			return JSON.stringify(orgobject);
		}
		
	}

	 /**
	 * return orgobject
	 * input:
	 * return: orgobject
	 * author:Pen Lin
	 */
	_self_.getObject = function()
	{
		if(orgobject.is_sub == true)
		{
			var obj = JSON.parse(JSON.stringify(orgobject));
			obj.subflow = [];
			obj.form_object = {};
			return obj;
		}
		else
		{
			return JSON.parse(JSON.stringify(orgobject));
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
		orgobject = JSON.parse(flow);
		//check and compare version
		if(!orgobject["version"])
		{
			orgobject["version"] = 000100000000;
		}
		
		
		orgobject.items.forEach(function(item, index, array)
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
	
	//====================
	//===object definition
	//====================

	/**
	 * inside object definition    -- start
	 * author:Pen Lin
	 */
	function org_object()
	{
		var output = {};
		output["version"] = 000100000000;
		output["flow_item_counter"] = 0;
		output["flow_line_counter"] = 0;
		output["max_dept_noid"] = 0;
		output["max_role_noid"] = 0;
		output["max_people_noid"] = 0;
		output["uid"] = 0;
		output["form_object"] = {};
		output.form_object.items = [];
		output["is_sub"] = false;
		output["subflow"] = []; //orgobject
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
	function dept_object()
	{
		var output = {};
		output["noid"] = 0;
		return output;
	}
	function role_object()
	{
		var output = {};
		output["noid"] = 0;
		return output;
	}
	function people_object()
	{
		var output = {};
		output["noid"] = 0;
		return output;
	}
	
	
	/**
	 * remove item(object) in flow content
	 * input:orgobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_remove_by_id(flow_item_id)
	{
		var item_mark = [];
		flow_item_id = flow_item_id.replace('item_remove_','').replace(active_id + '_','');
		orgobject.items.forEach(function(item,index)
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
	 * input:orgobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_remove(flow_item)
	{
		orgobject.items.forEach(function(item,index)
		{
			if(item.id == flow_item.id) 
			{
				if(item.type == 'line') //want delete line
				{
					var source_obj = orgobject_get(item.config.source_item);
					var target_obj = orgobject_get(item.config.target_item);

					orgobject.items.splice(index,1);
					$('#' + active_id + '_FLINE_' + flow_item.config.idcounter + 'A').remove();
					$('#' + active_id + '_FLINE_' + flow_item.config.idcounter + 'B').remove();
					$('#' + active_id + '_FLINE_' + flow_item.config.idcounter + 'C').remove();
					$('#' + active_id + '_' + flow_item.id).remove();
					
				}
				else 
				{
					orgobject.items.splice(index,1);
					$('#' + active_id + '_' + flow_item.id).remove();
				}
			}
		});
	}
	
	/**
	 * item copy button click 
	 * input:orgobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_make_by_id(flow_item_id)
	{
		flow_item_id = flow_item_id.replace('item_copy_','').replace(active_id + '_','');
		orgobject.items.forEach(function(item,index)
		{
			if(flow_item_id == item.id)
			{				
				var new_item = new item_object();
				orgobject.flow_item_counter++;
				new_item.id = "FITEM_" + orgobject.flow_item_counter;
                if(item.type == 'dept')
                {
                                 new_item.type = 'role';
                                 new_item.text = '選擇職務';
                                 new_item.config = new role_object();
                }
                if(item.type == 'role')
                {
                                 new_item.type = 'people';
                                 new_item.text = '選擇人';
                                 new_item.config = new people_object();
                }
                if(item.type == 'people')
                {
                                 new_item.type = 'people';
                                 new_item.text = '選擇人';
                                 new_item.config = new people_object();
                }
				
				//new_item.config = item.config;
				new_item.config.top = item.config.top + 25;
				new_item.config.left = item.config.left + 30;
				
				orgobject.items.push(new_item);
				item_create(new_item);
				item_select($('#' + active_id + '_' + 'chart_' + new_item.id) , false);
			}

		});
		
	}
	/**
	 * item config button click
	 * input:orgobject.items
	 * return: no return.
	 * author:Pen Lin 
	 */
	function item_config_by_id(flow_item_id)
	{
		flow_item_id = flow_item_id.replace(active_id + '_','').replace('item_config_','');
		orgobject.items.forEach(function(item,index)
		{
			if(flow_item_id == item.id)
			{
				action_item_for_modal = item;
			}
		});
		var show_id = '#' + active_id + '_' + action_item_for_modal.type + '_chart_modal';;
		switch(action_item_for_modal.type)
		{
			case 'dept':
				//clean all things
				$('#' + baseID_DEPT + '_config_value').val(null).trigger('change');

				//load object to real
				$('#' + baseID_DEPT + '_config_value').val(action_item_for_modal.config.noid).trigger('change');

				break;
			case 'role':
				//clean all things
				$('#' + baseID_ROLE + '_config_value').val(null).trigger('change');

				//load object to real
				$('#' + baseID_ROLE + '_config_value').val(action_item_for_modal.config.noid).trigger('change');

				break;
			case 'people':
				//clean all things
				$('#' + baseID_PEOPLE + '_config_value').val(null).trigger('change');

				//load object to real
				$('#' + baseID_PEOPLE + '_config_value').val(action_item_for_modal.config.noid).trigger('change');

				break;
		}
		$(show_id).modal('show');
	}

	/**
	 * add new item in flow content
	 * input:orgobject.items
	 * return: no return.
	 * author:Pen Lin
	 */
	function item_create(flow_item)
	{
		var content = '';
		var para = [];
		switch(flow_item.type)
		{
			case 'dept':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_dept});
				para.push({'key':'_icon_','value':'far fa-building'});
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
			case 'role':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_role});
				para.push({'key':'_icon_','value':'fas fa-briefcase'});
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
			case 'people':
				para.push({'key':'_des_','value':''});
				para.push({'key':'_style_','value':item_content_style_people});
				para.push({'key':'_icon_','value':'fas fa-user-tie'});
				para.push({'key':'_iconsize_','value':'45'});
				para.push({'key':'_iconoffset_','value':'top:32px;left:40px;'});
				para.push({'key':'_iconcolor_','value':'A39A81'});
				if(design_mode)
				{
					para.push({'key':'_button_','value': item_content_button_remove + item_content_button_config });
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
		
		orgcontent.append(replacer(item_content,para));
		
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
				item_make_by_id(this.id);
			});
		}
	}
	/**
	* create line object
	* input: orgobject.items.config
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
			orgcontent.append(replacer(line_content,para));
			para = [];
			para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
			para.push({'key':'_top_','value':line_config.linebox_top + line_config.linebox_long});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':line_config.linebox_bottom_width});
			para.push({'key':'_height_','value':4});
			para.push({'key':'_direction_','value':'top'});
			orgcontent.append(replacer(line_content,para));
			para = [];
			para.push({'key':'_pid_','value':line_config.idcounter + 'B'});
			para.push({'key':'_top_','value':line_config.linebox_top});
			para.push({'key':'_left_','value':line_config.linebox_left});
			para.push({'key':'_width_','value':line_config.linebox_top_width});
			para.push({'key':'_height_','value':4});
			para.push({'key':'_direction_','value':'top'});
			orgcontent.append(replacer(line_content,para));
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
			orgcontent.append(replacer(line_content,para));
			
			if(line_config.linebox_bottom_width > 0) //往右長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top+line_config.linebox_long});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':line_config.linebox_bottom_width});
				para.push({'key':'_height_','value':4});
				para.push({'key':'_direction_','value':'top'});
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
			orgcontent.append(replacer(line_content,para));
			if(line_config.linebox_bottom_width > 0) //往下長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left+line_config.linebox_long});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
			orgcontent.append(replacer(line_content,para));
			
			if(line_config.linebox_bottom_width > 0) //往下長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
			orgcontent.append(replacer(line_content,para));
			
			if(line_config.linebox_bottom_width > 0) //往下長
			{
				para = [];
				para.push({'key':'_pid_','value':line_config.idcounter + 'A'});
				para.push({'key':'_top_','value':line_config.linebox_top});
				para.push({'key':'_left_','value':line_config.linebox_left});
				para.push({'key':'_width_','value':4});
				para.push({'key':'_height_','value':line_config.linebox_bottom_width});
				para.push({'key':'_direction_','value':'left'});
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
				orgcontent.append(replacer(line_content,para));
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
		orgcontent.append(replacer(arrow_content,para));
		
		//Dragable
		if(design_mode)
		{
			$('[id^="' + active_id + '_' + 'FLINE_MH"]').draggable({ grid: [ 5, 5 ],containment: "parent",scroll: true,axis: "x",drag: function (){flow_drag_item(this)},stop: function (){flow_drag_item(this)}});
			$('[id^="' + active_id + '_' + 'FLINE_MW"]').draggable({ grid: [ 5, 5 ],containment: "parent",scroll: true,axis: "y",drag: function (){flow_drag_item(this)},stop: function (){flow_drag_item(this)}});
		}

		//畫完之後
		var source_obj = orgobject_get(line_obj.config.source_item); //check asnyc / switch / collector , push id
		var target_obj = orgobject_get(line_obj.config.target_item);
		
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
			orgobject.items.forEach(function(item,index)
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
						line_renew(orgobject.items[index]);
					 
					}
				}
			});
			
		}
		else if(drag_obj_id.indexOf('FLINE_M') == 0) //drag middle line
		{
			//drag line
			orgobject.items.forEach(function(item,index)
			 {
				if(item.id == drag_obj_id)
				{
					item.config.linebox_top = $('#' + active_id + '_' + drag_obj_id).css('top').replace('px','');
					item.config.linebox_left = $('#' + active_id + '_' + drag_obj_id).css('left').replace('px','');
					line_calculator(item, true);
					line_renew(orgobject.items[index] );
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
			orgobject.items.forEach(function(item, index, array)
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
			orgobject.items.forEach(function(item, index, array)
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
		
		var source_obj = orgobject_get(items_line.config.source_item);
		var target_obj = orgobject_get(items_line.config.target_item);
		
		var line_exist = false;
		
		orgobject.items.forEach(function(item, index, array)
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
			
			orgobject.flow_line_counter++; //FIRST

			items_line.config.idcounter = orgobject.flow_line_counter;
			
			if(items_line.config.target_side == 'top')
			{
				items_line.id = "FLINE_MW" + items_line.config.idcounter;
			}
			else
			{
				items_line.id = "FLINE_MH" + items_line.config.idcounter;
			}
			
			
			orgobject.items.push(items_line);
			
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
		//orgcontent.scrollTop(10)
		selected_source_chart_item = selected_item;
		$('[id^="' + active_id + '_' + 'chart_FITEM_"]').each(function()
		{
			if($(this).attr('id') == selected_source_chart_item.attr('id'))
			{
				$(this).css('border','4px solid #eab126');
				
				var obj = orgobject_get($(this).attr('id').replace('chart_','').replace(active_id + '_' , ''));

				if(design_mode)
				{
					$('#' + active_id + '_display_' + $(this).attr('id').replace('chart_','').replace(active_id + '_' , '')).css('display','');
					if(obj.type != 'people')
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
					orgcontent.scrollTop(10);
					if(obj.config.top > (orgcontent.height()/2))
					{
						orgcontent.scrollTop(obj.config.top - (orgcontent.height() /2)  );
					}
					if(obj.config.left > (orgcontent.width()/2))
					{
						orgcontent.scrollLeft(obj.config.left - (orgcontent.width() /2)  );
					}
					
					if(event_chart_selected_callback != null)
					{
						event_chart_selected_callback(obj.id);
					}
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
	 * find item in orgobject items array , 
	 * input:item id
	 * return: orgobject.items.
	 * author:Pen Lin
	 */
	function orgobject_get(item_id)
	{
		var output = null;
		orgobject.items.forEach(function(item, index, array)
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
					var obj = orgobject_get(chart_obj.attr('id').replace('chart_','').replace(active_id + '_' , ''));
					var source_obj = orgobject_get(selected_source_chart_item.attr('id').replace('chart_','').replace(active_id + '_' , ''));
					var show_point = false;
					
					if(source_obj.type == 'dept')
					{
						if((obj.type == 'dept')||(obj.type == 'role'))
						{
							show_point = true;
						}
					}
					else if(source_obj.type == 'role')
					{
						if(obj.type == 'people')
						{
							show_point = true;
						}
					}
					
					//使用者都不能連
					
					if(show_point)
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
		
		orgobject.items.forEach(function(item, index, array)
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
		var target_object = orgobject_get(line_config.target_item);
		var source_object = orgobject_get(line_config.source_item);
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
					group_tree_data_uuid.push({'id':option_item.id ,'value':option_item.id ,'text':option_item.display_name ,'parent_group':option_item.parent_group ,'parent':null,'level':1,'nonleaf':'non-leaf'});
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
					group_tree_data_uuid.push({'id':option_item.id ,'value':option_item.id ,'text':option_item.display_name ,'parent_group':option_item.parent_group ,'parent':parent_uuid,'level':new_class,'nonleaf':nonleaf });
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
	
}


