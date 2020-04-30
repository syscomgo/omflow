function syscom_tag( selector ) {
	
	//功能說明
	/**
	 * 一.初始化
	 * 功能: var thisTAG = new syscom_tag( <selector物件> );
	 * 參數: 如 $("#thisDom")
	 * 
	 * 二.功能
	 * 1.add_value( <tag名稱>, <tag值> ) 新增tag
	 * 2.get_value() 取得tag陣列
	 */
	var ID = guid();
	var VALUE_LIST = [];
	var THIS_DIV = selector;
	
	init();

	function init() {
		var div_style = {
				padding : "0px" //須對超出範圍時，新增對應屬性
		};
		THIS_DIV.css(div_style);
		THIS_DIV.on('click','i',function(){ //不清除click事件，以同時維護複數VALUE_LIST
			if($(this).parent().data("id")==ID && $.inArray( $(this).parent().data("val").toString(), VALUE_LIST )>=0 ){
				VALUE_LIST.splice($.inArray( $(this).parent().data("val").toString(), VALUE_LIST ),1);
				$(this).parent().remove();
			}
		});
	}
	
	function add_value( name, val ){
		if($.inArray( val, VALUE_LIST )==-1){
			var tag_style = {
					background : "lightgray",
					margin : "5px 0px 5px 5px",
					padding : "1px 5px"
			};
	
			var btn_style = {
					cursor: "pointer"
			};
	
			var tag_btn = $('<label data-id='+ID+' data-val='+val+'>'+name+'<i class="fa fa-times"></i></label>');
			tag_btn.css(tag_style).find("i").css(btn_style);
			THIS_DIV.append(tag_btn);
			VALUE_LIST.push(val);
		}
	}
	
	// 隨機UUID
	function guid() {// UUID格式的隨機字串
		function s4() {
			return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
		}
		return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
	}
	
	return {
		get_value : function() {
			return VALUE_LIST;
		},
		add_value : function(p1,p2) {
			add_value(p1,p2.toString());
		}
	}
}