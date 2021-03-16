/**
 * SYSCOM OMFLOW JS Lib
 * author:Pen Lin
 * ------------------
 */

/**
 * search document name is start with omflow then send post to omflow server
 * when ajax post success , omflowAjax will put data parameter to callback  function 
 * input:formid,target form id ; url,omflow api url ; callback, callback function name
 * return: no return.
 * author:Pen Lin
 */
function omflowAjax(formid,url,callback)
{	
	$('*').blur();
	var $inputs = $('#' + formid + ' :input');
	if ($('#' + formid).attr('enctype') == 'multipart/form-data')
	{	
		var file_data = $('#attachment').prop('files');
		var form_data = new FormData(); 
		for (var i = 0; i < file_data.length; i++) {
		    form_data.append('attachment[]', file_data[i]);
		}
		$inputs.each(function() {
			if(this.name == 'csrfmiddlewaretoken')
			{
				form_data.append(this.name,$(this).val());
			}
			else
			{
				form_data.append(this.name,$(this).val());
			}
		});
		$.ajax({
			url: url,
			type: 'post',
	        data: form_data,
	        cache:false,
	        processData: false,
	        contentType: false,
	        dataType: 'json',
	        xhr : function () {
	        	var myXhr = $.ajaxSettings.xhr();
	        	if(myXhr.upload)
	        	{
	        		myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
	        		return myXhr;
	        	}
	      	},
	        success: function (data) {
	            callback(data);
	        },
	        error: function(req, status, err) {
				$('#modal_error').modal('show');
	        	console.log('Something went wrong', status, err);
	    	}
		});
	}
	else
	{
		console.log("form");
		var values = {};
		$inputs.each(function() {
			if(this.name == 'csrfmiddlewaretoken')
			{
	        	values[this.name] = $(this).val();
			}
			else if(this.type == 'checkbox')
			{
				if($(this).prop('checked'))
				{
					values[this.name] = 'True';
				}
				else
				{
					values[this.name] = 'False';
				}
			}
			else
			{
				//values[this.name.substring(3)] = $(this).val();
				values[this.name] = $(this).val();
			}
		});
		$.ajax({
			url: url,
			type: 'post',
	        data: values,
	        dataType: 'json',
	        success: function (data) {
	            callback(data);
	        },
	        error: function(req, status, err) {
				$('#modal_error').modal('show');
	        	console.log('Something went wrong', status, err);
	    	}
		});
	}
}

function progressHandlingFunction(event) {
//	if (event.lengthComputable && event.total >= 10) 
//	{
		$('#modal-progress').modal('show');
		var value = (event.loaded / event.total * 100 | 0);
		var strProgress = value + "%";
	    $(".progress-bar").css({"width": strProgress});
	    $(".progress-bar").text(strProgress);
//	}
//	else
//	{
//		omflowAlert('black')
//	}
}

/**
 * send post to omflow server
 * when ajax post success , omflowAjax will put data parameter to callback  function 
 * input:postbody,json name ; url,omflow api url ; callback, callback function name
 * return: no return.
 * author:Arthur
 */
function omflowJsonAjax(postbody,url,callback){
	var postbody = arguments[0]? arguments[0]: {};
	var url = arguments[1];
	var callback = arguments[2];
	$.ajax({
		url: url,
		type: 'POST',
		headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: JSON.stringify(postbody),
        dataType: 'json',
        success: function (data) {
            callback(data);
        },
        error: function(req, status, err) {
			$('#modal_error').modal('show');
        	console.log('Something went wrong', status, err);
    	}
	});
	
	postbody = undefined;
	url = undefined;
	//callback = undefined;
}
/**
 * Show Alert Dialogue
 * input: color, msg, callback, callbackdata
 * author:Arthur
 */
function omflowAlert(){
	
	var color = arguments[0];
	var msg = "";
	var callback = arguments[2];
	var callbackdata = arguments[3];
	
	switch(color){
		case "red":
			msg = __const_systemError__;
			break;
		case "yellow":
			msg = __const_actionError__;
			break;
		case "green":
			msg = __const_actionDone__;
			break;
		case "black":
			break;
		default:
			color = "blue";
			msg = __const_actionDone__;
	}
	
	msg = arguments[1]? arguments[1]: msg ;
	$('#modal_'+color+'_text').html('<p>' + msg + '</p>');
	$('#modal_'+color).modal('show');
	if(callback){
		$('#modal_'+color+' button:eq(1)').off("click").click(function(){
			$(this).modal('hide');
			callback( callbackdata );
		});
	}else{
	    $('#modal_'+color+' button:eq(1)').off("click").click(function(){
	  		$(this).modal('hide');
	  	});
	}
	
	color = undefined;
	msg = undefined;
	//callback = undefined;
	//callbackdata = undefined;
}

/**
 * Show Confirm Dialogue
 * input: color, msg, callback, callbackdata
 * author:Arthur
 */
function omflowConfirm(){
	
	var color = arguments[0];
	var msg = arguments[1];
	var callback = arguments[2];
	var callbackdata = arguments[3];
	
	switch(color){
		case "red":
		case "yellow":
		case "green":
			break;
		default:
			color = "blue";
	}
	
	msg = arguments[1]? arguments[1]: __const_noMessage__ ;
	$('#modal_'+color+'_text').html('<p>' + msg + '</p>');
	$('#modal_'+color).modal('show');
	$('#modal_'+color+' button:eq(1)').off("click").click(function(){
		$('#modal_'+color).modal('hide');
		callback( callbackdata );
	});
	
	color = undefined;
	msg = undefined;
	//callback = undefined;
	//callbackdata = undefined;
}

/**
 * Show Confirm Dialogue
 * input: type, title, callback, callbackdata
 * author: Arthur
 */
function omflowConfirmDialogue(){
	var icon = arguments[0];
	var title = arguments[1];
	var content = arguments[2];
	var callback = arguments[3];
	var thisDialoge = $("#modal-default-confirm");
	
	thisDialoge.find('.modal-title i').removeClass().addClass(icon);
	thisDialoge.find('.modal-title span').text(title);
	thisDialoge.find('.modal-body').text(content);
	thisDialoge.find('.btn-primary').off('click').on('click',function(){
		callback();
	});
	thisDialoge.modal('show');
}


/**
 * Show List Dialogue
 * input: type, title, callback, callbackdata
 * author: Arthur
 */
function omflowListDialogue(){

	var tag_i = "";
	var type = arguments[0];
	var title = arguments[1];
	var callback = arguments[2];
	var callbackdata = arguments[3];
	var table = arguments[4]? $(arguments[4]): $('.table');
	
	switch(type){
	case "enable":
		tag_i = '<i class="fa fa-play"></i>&nbsp;&nbsp;';
		break;
	case "disable":
		tag_i = '<i class="fa fa-stop"></i>&nbsp;&nbsp;';
		break;
	case "delete":
		tag_i = '<i class="fa fa-trash-o"></i>&nbsp;&nbsp;';
		break;
	case "undeploy":
		tag_i = '<i class="fa fa-ban"></i>&nbsp;&nbsp;';
		break;
	case "output":
		tag_i = '<i class="fa fa-upload"></i>&nbsp;&nbsp;';
		break;
	case "input":
		tag_i = '<i class="fa fa-download"></i>&nbsp;&nbsp;';
		break;
	case "relation":
		tag_i = '<i class="fas fa-link"></i>&nbsp;&nbsp;';
		break;
	case "remove":
		tag_i = '<i class="far fa-calendar-minus"></i>&nbsp;&nbsp;';
		break;
	}
	
  	
  	$('#modal-default-list').find('.modal-body').empty().append(
  		'<ul class="list-group list-group-unbordered" id="modal-default-list-text"></ul>'	
  	);
	$('#modal-default-list-title').empty();
	$('#modal-default-list-title').append(tag_i+title);
	var this_check = '';
	$.each( table.find('input:checkbox:checked'), function(){
		this_check = $(this).data('value');
		if (this_check == null )
		{
			return;
		}
		var status = $(this).closest('tr').find('.label:eq(0)').parent().html();
		if (status)
		{
			$('#modal-default-list-text').prepend('<li class="list-group-item"><i class="fa fa-circle"></i>&nbsp;&nbsp;<b class="text-light-blue">'+this_check+'</b> <a class="pull-right">'+status+'</li>');
		}
		else
		{
			$('#modal-default-list-text').prepend('<li class="list-group-item"><i class="fa fa-circle"></i>&nbsp;&nbsp;<b class="text-light-blue">'+this_check+'</b></li>');
		}
	});
	$('#modal-default-list').modal('show');
	$('#modal-default-list button:eq(2)').off("click").on("click",function(){
		$('#modal-default-list').modal('hide');
		callback(callbackdata);
	});
	
	tag_i = undefined;
	type = undefined;
	title = undefined;
	//callback = undefined;
	//callbackdata = undefined;
}

/**
 * Change the file size unit
 * input: size (Integer in Bytes)
 * return: size (String with unit)
 * author: Pei lin
 */

function omflowSizeUnit(size){
	if (size < 1024)
		{size = size+' Byte'}
	else if (size < Math.pow(2,20))
	 	{size = (size/Math.pow(2,10)).toFixed(2)+' KB'}
	else if (size < Math.pow(2,30))
	 	{size = (size/Math.pow(2,20)).toFixed(2)+' MB'}
	else if (size < Math.pow(2,40))
		{size = (size/Math.pow(2,30)).toFixed(2)+' GB'}
	else 
		{size = (size/Math.pow(2,40)).toFixed(2)+' TB'}
	return size;
}

/**
 * trans numder to serial number => "00000001"
 * input: String
 * return: String
 * author: Pei lin
 */

function paddingLeft(str,lenght){
	if(str.length >= lenght)
	return str;
	else
	return paddingLeft("0" +str,lenght);
}


/**
 * show B modal until A hided
 * input: A modal,B modal
 * return: none
 * author: Arthur
 */
function BindSwitchModal(thisModal,nextModal){
	thisModal = $(thisModal);
	nextModal = $(nextModal);
	thisModal.off('hidden.bs.modal');
	thisModal.on('hidden.bs.modal', function () {
		thisModal.off('hidden.bs.modal');
	    nextModal.modal('show');
	});
}

/**
 * prevent bodyscroll show until A modal hided
 * input: A modal
 * return: none
 * author: Arthur
 */
function HideBodyScrollModal(thisModal){
	$('body').css('overflow','hidden');
	thisModal = $(thisModal);
	thisModal.modal('show');
	thisModal.off('hidden.bs.modal');
	thisModal.on('hidden.bs.modal', function () {
		thisModal.off('hidden.bs.modal');
	    	$('body').css('overflow','auto');
	});
}

/**
 * trans string 'aaaa' to '****'
 * input: String
 * return: String
 * author: Pei lin
 */

function paddingMark(str){
	var newstr = ''
	for (var i=0; i < str.length; i++)
		newstr += '*'
	return newstr;
}

/**
 * Check all checkbox in current page
 * input: none
 * return: none
 * author: Pei lin
 */

function omflowCheckAll(){
	$('.checkbox-toggle').off('click').on('click',function () {
		thistable = $(this).closest('table').attr('id');
		if($('#'+ thistable +' input:checkbox:checked').length == 0)
			{$('#'+ thistable +' input[type="checkbox"]').prop('checked',true);}
		else
			{$('#'+ thistable +' input[type="checkbox"]').prop('checked',false);}
		enablebtt();
	});	
}
 
/**
 * Filter dialog 
 * input: none
 * return: none
 * author: Pei lin
 */

function omflowFilter(){
	var filter_item = arguments[0];
	var callback = arguments[1];
	var callbackdata = arguments[2];
	
	var filter_search = '<li class="list-group-item" name="filter_search">'+
      					'<div class="input-group">'+
      					'<span class="input-group-addon"><i class="fa fa-search"></i></span>'+
      					'<input type="text" id="search" name="search" class="form-control" placeholder=" ' + gettext('搜尋') + '..." autofocus />'+
      					'</div>'+
      					'</li>';
	
	var filter_type = 	'<li class="list-group-item" name="filter_type">'+
						'<div class="form-group" style="margin:0px;">'+
						'<label class="text-light-blue">' + gettext('屬性') + '：</label>'+
						'<br>'+
           				'<input type="checkbox" class="icheckbox_minimal-blue" name="filter_type" data-value="lib" id="filter_lib" checked><label for="filter_lib"></label>&nbsp;&nbsp;&nbsp;lib&nbsp;&nbsp;&nbsp;'+
           				'<input type="checkbox" class="icheckbox_minimal-blue" name="filter_type" data-value="sys" id="filter_sys" checked><label for="filter_sys"></label>&nbsp;&nbsp;&nbsp;sys&nbsp;&nbsp;&nbsp;'+
           				'<input type="checkbox" class="icheckbox_minimal-blue" name="filter_type" data-value="user" id="filter_user" checked><label for="filter_user"></label>&nbsp;&nbsp;&nbsp;user&nbsp;&nbsp;&nbsp;'+
           				'<input type="checkbox" class="icheckbox_minimal-blue" name="filter_type" data-value="cloud" id="filter_cloud" checked><label for="filter_cloud"></label>&nbsp;&nbsp;&nbsp;cloud&nbsp;&nbsp;&nbsp;'+
           				'</div>'+
           				'</li>';
	
	var filter_utype = 	'<li class="list-group-item" name="filter_utype">'+
						'<div class="form-group" style="margin:0px;">'+
						'<label class="text-light-blue">' + gettext('類別') + '：</label>'+
						'<br>'+
						'<input type="checkbox" class="icheckbox_minimal-blue" name="filter_utype" data-value="1" id="filter_type_1" checked><label for="filter_type_1"></label>&nbsp;&nbsp;&nbsp;' + gettext('外部') + '&nbsp;&nbsp;&nbsp;'+
			            '<input type="checkbox" class="icheckbox_minimal-blue" name="filter_utype" data-value="0" id="filter_type_0" checked><label for="filter_type_0"></label>&nbsp;&nbsp;&nbsp;' + gettext('系統') + '&nbsp;&nbsp;&nbsp;'+
						'</div>'+
						'</li>';
	
	var filter_status = '<li class="list-group-item" name="filter_status">'+
						'<div class="form-group" style="margin:0px;">'+
						'<label class="text-light-blue">' + gettext('狀態') + '：</label>'+
						'<br>'+
			            '<input type="checkbox" class="icheckbox_minimal-blue" name="filter_status" data-value="1" id="filter_status_1" checked><label for="filter_status_1"></label>&nbsp;&nbsp;&nbsp;' + gettext('啟用') + '&nbsp;&nbsp;&nbsp;'+
			            '<input type="checkbox" class="icheckbox_minimal-blue" name="filter_status" data-value="0" id="filter_status_0" checked><label for="filter_status_0"></label>&nbsp;&nbsp;&nbsp;' + gettext('停用') + '&nbsp;&nbsp;&nbsp;'+
			          	'</div>'+
			            '</li>';
	
	var filter_closed = '<li class="list-group-item" name="filter_closed">'+
						'<div class="form-group" style="margin:0px;">'+
						'<label class="text-light-blue">' + gettext('已關單') + '/' + gettext('未關單') + '：</label>'+
						'<br>'+
					    '<input type="checkbox" class="icheckbox_minimal-blue" name="filter_closed" data-value="1" id="filter_closed_1"><label for="filter_closed_1"></label>&nbsp;&nbsp;&nbsp;' + gettext('已關單') + '&nbsp;&nbsp;&nbsp;'+
					    '<input type="checkbox" class="icheckbox_minimal-blue" name="filter_closed" data-value="0" id="filter_closed_0" checked><label for="filter_closed_0"></label>&nbsp;&nbsp;&nbsp;' + gettext('未關單') + '&nbsp;&nbsp;&nbsp;'+
					  	'</div>'+
					    '</li>';

	var filter_length = '<li class="list-group-item" name="filter_length">'+
						'<div class="form-group" style="margin:0px;">'+
		            	'<label class="text-light-blue">' + gettext('每頁顯示筆數 ') + ':</label>'+
		            	'<br>'+
						'<select id="page_length" class="form-control">'+
					  	'	<option value="10">10</option>'+
					  	'	<option value="25">25</option>'+
					  	'	<option value="50">50</option>'+
					  	'	<option value="100">100</option>'+	                  		
						'</select>'+
						'</div>'+
						'</li>';
	
	var filter_date =	'<li class="list-group-item" name="filter_date">'+
						'<div class="form-group" style="margin:0px;">'+
						'<label class="text-light-blue">' + gettext('選擇檔案日期範圍') + ':</label>'+
						'<br>'+
						'<button type="button" class="btn btn-default" id="daterange">'+
						'<span>'+
						'<i class="fa fa-calendar"></i> ' + gettext('選擇日期') + 
						'</span>'+
						'<i class="fa fa-caret-down"></i>'+
						'</button>'+
						'</div>'+
						'</li>';
	
	var filter_drange = '<li class="list-group-item" name="filter_date">'+
						'<div class="form-group" style="margin:0px;">'+
					    '<label class="text-light-blue">' + gettext('選擇日期範圍') + ':</label>(測試中)'+
					    '<div class="input-group">'+
					    '<button type="button" class="btn btn-default pull-right" id="daterange-btn">'+
					    '<span><i class="fa fa-calendar"></i> ' + gettext('選擇日期範圍') + '</span>'+
					    '<i class="fa fa-caret-down"></i>'+
					    '</button>'+
					    '</div>'+
					    '</div>'+
					    '</li>'
	
	var filter_flow = 	'<li class="list-group-item" name="filter_flow">'+
						'<div class="form-group" style="margin:0px;">'+
						'<label class="text-light-blue">' + gettext('查詢特定流程') + ' :</label>'+
						'<br>'+
						'<select id="select_flow_uuid" class="form-control" style="width:100%; margin-bottom:10px;">'+                  		
						'</select>'+
						'</div>'+
						'</li>';
	
	var filter_tag ={ 
		  				'filter_search'	: filter_search , 
						'filter_flow'	: filter_flow,
						'filter_type'	: filter_type,
						'filter_utype'	: filter_utype,
						'filter_status'	: filter_status, 
						'filter_closed' : filter_closed,
						'filter_length'	: filter_length, 
						'filter_date'	: filter_date,
						'filter_drange' : filter_drange
		}
	$('#modal-default-filter .list-group-unbordered').empty();
	$.each(filter_tag, function(index, value){
		if (filter_item.indexOf(index) >= 0){
			$('#modal-default-filter .list-group-unbordered').append(value);
		}
	});
	
	if (filter_item.indexOf('filter_date')　>= 0){
		//Date range as a button
		var ranges = {};
		ranges[gettext('顯示所有檔案')] = [moment().toDate()];
		ranges[gettext('30  天') + '&nbsp;&nbsp;&nbsp;' + gettext('前所有檔案')] = [moment().subtract(30, 'days')];
		ranges[gettext('60  天') + '&nbsp;&nbsp;&nbsp;' + gettext('前所有檔案')] = [moment().subtract(60, 'days')];
		ranges[gettext('120  天')+ '&nbsp;' + gettext('前所有檔案')] = [moment().subtract(120, 'days')];
		ranges[gettext('6 個月') + '&nbsp;' + gettext('前所有檔案')] = [moment().subtract(6, 'month')];
		ranges[gettext('一年')  + '&nbsp;&nbsp;&nbsp;&nbsp;' + gettext('前所有檔案')] =[moment().subtract(1, 'year')];
	    $('#daterange').daterangepicker(
			{
				ranges   : ranges,
				startDate: moment().subtract(29, 'days'),
			},
			function (start) {
				$('#daterange'+' span').html(start.format('Y-MM-DD') + gettext('前所有檔案 '));
		      	select_time = start.add(1,'days').format('Y-MM-DD');
			}
		);
	}
	
	if(filter_item.indexOf('filter_drange')　>= 0){
		var ranges = {};
		ranges[gettext('今天')]     = [moment(), moment()];
		ranges[gettext('昨天')]     = [moment().subtract(1, 'days'), moment().subtract(1, 'days')];
		ranges[gettext('最近一周')]  = [moment().subtract(6, 'days'), moment()];
		ranges[gettext('最近30天')]  = [moment().subtract(29, 'days'), moment()];
		ranges[gettext('本月')]     = [moment().startOf('month'), moment().endOf('month')];
		ranges[gettext('上個月')]    = [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')];
		$('#daterange-btn').daterangepicker(
			{
				ranges   : ranges,
				startDate: moment().subtract(29, 'days'),
				endDate  : moment()
			},
			function (start, end) {
				$('#daterange-btn span').html(start.format('Y-MM-DD') + ' - ' + end.format('Y-MM-DD') + ' ')
				select_range = start.format('Y-MM-DD') + ',' + end.format('Y-MM-DD');
			}
	    );
	}
	
	$('#modal-default-filter').on('shown.bs.modal', function () {
	    $('#modal-default-filter #search').focus();
	})
	$('#modal-default-filter').modal('show');
}

/**
 * Cookie handler getCookie/setCookie
 * input: 			name   / name, value, days
 * return:			value  / set cookie time 
 * author: Pei lin
 */

function getCookie(name) {
    var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}

function setCookie(name, value, days) {
    var d = new Date;
    d.setTime(d.getTime() + 24*60*60*1000*days);
    document.cookie = name + "=" + value + ";SameSite=Strict;path=/;expires=" + d.toGMTString();
}

/**
 * Datatable compare data form backend
 * Need announce variable data_tmp, data_len, data_page in front of all script first,
 * and overwrite variable out of the function.
 * input:	data:{draw, recordsTotal, recordsFilter, recordsNum, data}
 * return:	data.data, data_tmp, data_len, data_page
 * author: Pei lin
 */
function dataCompare(data,data_tmp,data_len,data_page,table){
	if ([403,404,500].indexOf(data.status) >= 0)		//check data return status
	{
		actions(data);
	}
	else
	{		//If first time load datatable draw = 1,and if page changed pass full data to datatable. 
			//Store data.data 		--> data_tmp, 
			//		data.recordsNum --> data_len, 
			//		data.page,page()--> data_page 
		if (data.draw == 1 | table.page.info().page !== data_page)
		{
			data_tmp 	= data.data;
			data_len 	= data.recordsNum;
			data_page 	= table.page.info().page;
		}
		else
		{		
			if (data_len == data.recordsNum && data.data == 'same')		//If show data length not change and data.data == 'same' do nothing 
			{
				
			}
			else if (data.data == 'page_null')
			{
				table.page('previous').draw();
			}
			else if (data_len <= data.recordsNum)		//If data_len <= data.recordsNum overwrite data_tmp from data.data by row
			{
				$.each(data.data, function(i,v){		//overwrite data_tmp
					if (!$.isEmptyObject(v))
					{	
						data_tmp[i] = v
					}
				});
			}		
			else if (data_len > data.recordsNum)		//If data_len > data.recordsNum overwrite data_tmp from data.data by row and delete unnecessary row
			{
				$.each(data.data, function(i,v){
					if (!$.isEmptyObject(v))
					{	
						data_tmp[i] = v					//overwrite data_tmp
					}
				});
				data_tmp.length = data.recordsNum;		//delete unnecessary row
			}
			data_len = data.recordsNum;					//overwrite data_len
			data.data = data_tmp;
		}
		return {'data.data': escapeHtml(data.data), 'data_len': data_len, 'data_page':　data_page, 'data_tmp': data_tmp};
	}
}

/**
 * uuid_function
 * author: Arthur
 */
function guid() {
	function s4() {
		return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
	}
	return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}

/**
 * common_function
 * author: Arthur
 */
(function($) {
    $.fn.invisible = function() {
        return this.each(function() {
            $(this).css("visibility", "hidden");
        });
    };
    $.fn.visible = function() {
        return this.each(function() {
            $(this).css("visibility", "visible");
        });
    };
    $.fn.hasName = function(name) {
        return this.name == name;
    };
}(jQuery));

if (!String.prototype.startsWith) {
    String.prototype.startsWith = function(searchString, position){
      position = position || 0;
      return this.substr(position, searchString.length) === searchString;
  };
}


function escapeHtml(text) {
	var map = 
	{
//		'&': '&amp;',
		'<': '&lt;',
		'>': '&gt;',
		'"': '&quot;',
		"'": '&#039;'
	};
	if (typeof text == 'object')
		{
			$.each(text, function(I, V){
				text[I] = escapeHtml(V);
			});
			return text;
		}
	else if (typeof text == 'string' )
		{
			return text.replace(/[<>"']/g, function(m) { return map[m]; });
		}
	else
		{
			return text;
		}
}

function unescapeHtml(text) {
	var map = 
	{
//		'&amp;': '&',
		'&lt;': '<',
		'&gt;': '>',
		'&quot;': '"',
		"&#039;": "'"
	};
	if (typeof text == 'object')
		{
			$.each(text, function(I, V){
				text[I] = escapeHtml(V);
			});
			return text;
		}
	else if (typeof text == 'string' )
		{
			return text.replace(/&#039;|&quot;|&gt;|&lt;/g, function(m) { return map[m]; });
		}
	else
		{
			return text;
		}
}

function checkPattern(obj){
	var pattern = obj.attr('pattern')
	var re = new RegExp(pattern);
    if (re.test(obj.val())) {
        return true;
    } else {
        return false;
    }
}