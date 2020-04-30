//功能：遮蔽內容
(function($) {
    $.fn.block = function() {
        return this.each(function() {
        	var THIS_DOM = $(this);
        	var THIS_BLOCK = $('<div class="omflow-block-board"><div class="omflow-block-text">處理中...</div></div>');

        	if(THIS_DOM.css("position") == "static") {
        		THIS_DOM.addClass("omflow-block-parent");
    		}
    		THIS_DOM.append(THIS_BLOCK);
        	THIS_DOM = undefined;
        	THIS_BLOCK = undefined;
        });
    };
    $.fn.unblock = function() {
        return this.each(function() {
        	var THIS_DOM = $(this);
        	if(THIS_DOM.hasClass("omflow-block-parent")){
        		THIS_DOM.removeClass("omflow-block-parent");	
        	}
        	THIS_DOM.find(".omflow-block-board").remove();
        	THIS_DOM = undefined;
        });
    };
}(jQuery));