/* Add To Cart */
jQuery(function (jQuery) {
	
	function showQuickView(url, id){
		url += '?iframe=true&width=800&height=410';
		jQuery.prettyPhoto.open(url);
	}
	
    function ajaxAddToCart(url, id){
        url = url.replace("checkout/cart","ajax/index");
		url += 'isAjax/1';
        var msgHtml;
        var productImg = jQuery('#item-id-' + id + ' .product-image').html();

		jQuery('body').append('<div id="addedoverlay" style="display:none"></div>');
		jQuery('body').append('<div id="added" style="display:none"><div id="added-internal"><div id="added-content"></div></div></div>');
        var windowOver = jQuery('#addedoverlay');
        var windowBox = jQuery('#added');
		var windowContent = jQuery('#added-content');
        windowOver.show();
		windowBox.show();
		windowContent.css({
        	backgroundImage: "url('"+loaderBckImg+"')"
		});
        try {
        	jQuery.ajax({
            	url : url,
                dataType : 'json',
				beforeSubmit: function(){    
					//jQuery('#ajax_loader').show();                   
				},
                success : function(data) {
					//jQuery('#ajax_loader').hide();
					parent.jQuery.prettyPhoto.close();
					parent.setAjaxData(data,loaderBckImg, successMsg, continueMsg, cartUrl, cartMsg, errorMsg);                                        
/*
					if(data.status == 'SUCCESS'){
						
						if(jQuery('.block-cart')){
							jQuery('.block-cart').replaceWith(data.sidebar);
						}
						if(jQuery('.header .cart-header')){
							jQuery('.header .cart-header').replaceWith(data.topcart);
						}
						if(window.parent.jQuery('.header .cart-header')){
							window.parent.jQuery('.header .cart-header').replaceWith(data.topcart);
						}
						msgHtml = '<div style="float:left;">' + productImg + '</div>' + data.message + '<div style="clear:both;"></div><a id="hidewindow" onclick="window.parent.jQuery.prettyPhoto.close()" href="javascript:void(0);">' + continueMsg + '</a>&nbsp;<a onclick="returnCart()" href="javascript:void(0)">' + cartMsg + '</a>';
					}else{
						msgHtml = '<p class="error-msg" style="margin-bottom:15px;">' + data.message + '</p><a id="hidewindow" href="javascript:void(0);" onclick="window.parent.jQuery.prettyPhoto.close()">' + continueMsg + '</a>&nbsp;<a onclick="returnCart()" href="javascript:void(0)">' + cartMsg + '</a>';
					}            
					
					windowContent.css({
						backgroundImage: 'none'
					});
					
					windowContent.html(msgHtml);
												
					windowOver.on('click',function(){
						hidewindow(windowBox,windowOver);                    
					});	       
											 
					jQuery('#hidewindow').click(function(){
						hidewindow(windowBox,windowOver);                    
					});
*/
             	}
         	});
        } catch (e) {
        }
	}
			
	jQuery('.ajax-addtocart').click(function (e) {            
		e.preventDefault();        
        ajaxAddToCart(jQuery(this).attr('href'), jQuery(this).attr('data-id'));        
    });
	
	jQuery('.btn-quickview').click(function (e) {
		e.preventDefault();
        showQuickView(jQuery(this).attr('href'), jQuery(this).attr('data-id'));
    });
	
});

function hidewindow(windowBox,windowOver){        	
	windowOver.fadeOut(400, function(){ jQuery(this).remove(); });
	windowBox.fadeOut(400, function(){ jQuery(this).remove(); });
	sendReq('search');
}

function setAjaxData(data,loaderBckImg, successMsg, continueMsg, cartUrl, cartMsg, errorMsg) {
	var msgHtml;
	jQuery('body').append('<div id="addedoverlay" style="display:none"></div>');
	jQuery('body').append('<div id="added" style="display:none"><div id="added-internal"><div id="added-content"></div></div></div>');
    var windowOver = jQuery('#addedoverlay');
    var windowBox = jQuery('#added');
	var windowContent = jQuery('#added-content');
    windowOver.show();
	windowBox.show();
		
	if(jQuery('.block-cart')){
		jQuery('.block-cart').replaceWith(data.sidebar);
	}
	if(jQuery('.header .cart-header')){
		jQuery('.header .cart-header').replaceWith(data.topcart);
	}	
	if(window.parent.jQuery('.header .cart-header'))
	{
		window.parent.jQuery('.header .cart-header').replaceWith(data.topcart);
	}
	msgHtml = data.message + '<div style="clear:both; height: 10px;"></div><a id="hidewindow" href="javascript:void(0);">' + continueMsg + '</a>&nbsp;<a href="' + cartUrl + '">' + cartMsg + '</a>';
	windowContent.html(msgHtml);					   

	windowOver.on('click',function(){                            
		hidewindow(windowBox,windowOver);                    
	});	       

	jQuery('#hidewindow').click(function(){                      
		hidewindow(windowBox,windowOver); 
	});

}

function returnCart()
{
	window.top.location = cartUrl;
}
