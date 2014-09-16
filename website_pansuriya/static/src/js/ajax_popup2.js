var jsonGridData = [];
// var jsonGridData=[];
var domainname = "http://"+parent.window.location.host;
var cart_url='http://'+parent.window.location.host;
                            var dataLength, loadData;
                            var filterParams;
                            var tempFlagFilterAttr = "";
                            var tempFlagFilterSort = 1;

                            var count_collection;

                            var compareFlagFilterAttr = "";
                            var compareFlagFilterSort = 1;

                            var jsonCompareData = [];
                            var compareCount = 0;

                            var firstTime = 1;

                            function getAuctionEndTime(current_time, auction_end_time)
                            {
                                var server_time = new Date(current_time);
                                var system_time = new Date();
                                var diff = minutesDiff(server_time, system_time);
                                var auction_end_date = new Date(auction_end_time);
                                return auction_end_date.setMinutes(auction_end_date.getMinutes() + diff);
                            }

                            function minutesDiff(system_time, server_time)
                            {
                                var minute = 1000 * 60;
                                return Math.ceil((server_time.getTime() - system_time.getTime()) / (minute));
                            }


                            jQuery(document).ready(function() {
                            	//alert('onready...');
                                /*
								 * $zopim(function() {
								 * $zopim.livechat.hideAll(); });
								 */
                                /*
								 * setTimeout(function() {
								 * jQuery('.zopim').remove(); },500);
								 * 
								 * 
								 */


//                                var auction_end_time = getAuctionEndTime('<?php echo $data['current_time']; ?>', '<?php echo $data['auction_end_time']; ?>');
//
//                                jQuery('.auction_timer_' + '<?php echo $data['entity_id']; ?>').countdown({
//                                    date: new Date(auction_end_time),
//                                    render: function(data) {
//                                        data.hours = data.hours + data.days * 24;
//                                        jQuery(this.el).html(data.hours + " : " + this.leadingZeros(data.min, 2) + " : " + this.leadingZeros(data.sec, 2));
//                                    },
//                                    onEnd: function() {
//                                        jQuery('#btnAddToCart').css({'background-color': '#66ccdd', 'color': 'black'}).attr('is_auction', 0);
//                                        jQuery('#bid_price').attr('disabled', 'disabled');
//                                        jQuery('#bid_price').attr('onclick', 'javascript:void(0)');
//                                    }
//                                });
                                if (jQuery('#btnAddToCart').attr('is_auction') == 1)
                                {
                                    jQuery('#btnAddToCart').css({'background-color': 'gray', 'color': 'white'});
                                }

                                //MagicMagnify.start();
// contact seller ajax start
//                                jQuery('.menu_send_button').click(function() {
//                                    jQuery('#addedoverlay').show();
//                                    showMessageCustom("Please wait...");
//                                    var url = '<?php echo $this->getUrl(); ?>ajaxmodule/ajax/sendsellercontactmail';
//                                    var manu_email = '<?php echo $data['manufacturer_email']; ?>';
//                                    var manu_name = '<?php echo $data['manufacturer']; ?>';
//                                    var sku = '<?php echo $data['sku']; ?>';
//                                    var cust_id = '<?php echo Mage::getSingleton('customer/session')->getCustomer()->getId(); ?>';
//                                    var contact_text = jQuery('#contact_text').val();
//                                    jQuery.ajax({
//                                        url: url,
//                                        type: 'POST',
//                                        data: {manufacturer_email: manu_email, manufacturer_name: manu_name, stone_sku: sku, customer_id: cust_id, seller_message: contact_text},
//                                        success: function(data) {
//                                            jQuery('#contact_text').val('');
//                                            var msg = data;
//                                            setTimeout(function() {
//                                                showMessageCustom(msg);
//                                                jQuery('#addedoverlay').hide();
//                                            }, 500);
//                                        }
//                                    });
//                                });

// contact seller end
//                                jQuery('#divLoginAlert, .login_required_redirect').click(function() {
//                                    var redirect_url = '<?php echo Mage::getUrl('customer/account/login'); ?>';
//                                    window.top.location = redirect_url;
//                                });

                                jQuery('.pop_na').click(function() {
                                    var attribute = jQuery(this).attr('attribute');
                                    var current_obj = jQuery(this);
                                    var entity_id = jQuery('#btnAddToWatchList').attr('data-id');
                                    if (customer_id == '')
                                    {
                                        jQuery('#divLoginAlert').click();
                                    }
                                    else if (current_obj.html() == 'ASK')
                                    {
                                        jQuery('.askpopup').fadeIn("slow");
                                        jQuery('.askpopup').css({display: "block", position: "absolute", 'top': 200, 'left': (window.innerWidth - 250) / 2});
                                    }
                                });
// ask popup send button
//                                jQuery('#askpopupsend').click(function() {
//                                    var stone_sku = jQuery('#stone_sku').val();
//                                    var customer_id = jQuery('#customer_id').val();
//                                    var txtarea = jQuery('#txtarea').val();
//                                    if (txtarea == null || txtarea == "")
//                                    {
//                                        alert("Please enter Message");
//                                        return false;
//                                    }
//                                    var ask_url = '<?php echo Mage::getUrl('ajaxmodule/ajax/sendaskmail'); ?>';
//                                    var tick_img_url = "<?php echo Mage::getBaseUrl(Mage_Core_Model_Store::URL_TYPE_SKIN); ?>themeforest/images/tick.png";
//                                    jQuery.ajax({
//                                        url: ask_url,
//                                        data: {msg: txtarea, customer_id: customer_id, stone_sku: stone_sku},
//                                        type: 'POST',
//                                        success: function(data) {
//                                            jQuery('.pop_na').html('<img src="' + tick_img_url + '" style="height: 18px;width: 18px;vertical-align: top;">');
//                                            jQuery('.askpopup').css({display: "none"});
//                                            alert('Email Sent');
//                                        }
//                                    });
//                                });
// click outer then hide code
                                jQuery(document).mouseup(function(e)
                                {
                                    var container = jQuery('.askpopup');

                                    if (container.has(e.target).length === 0)
                                    {
                                        container.fadeOut("slow");
                                    }
                                });



                                jQuery('#btnAddToCart').click(function(e) {
                                	var product_id = jQuery('#popup_stone_id').attr('data-oe-id');
//                                	var data = {product_id: product_id,line_id:false,add_qty:1};
//                                	openerp.jsonRpc("/shop/cart/update_json", 'call', {'data':data }  )
//                					.then(function (data) {			             
//                							alert(data);
//                			            });
                                	//parent.jQuery('#stone_addtocart_181').submit();                                	
                                	var loaderBckImg = domainname+"/website_pansuriya/static/src/images/loading.gif";
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
                                	jQuery.ajax({
                                      url: "/shop/cart/update",
                                      type: 'POST',
                                      data: {product_id: product_id},                                      
                                      success: function(data) {
                                    	  if(parent.jQuery('#top_menu').find('li').hasClass('hidden'))
                                		  {
                                    		  parent.jQuery('#top_menu').find('li').removeClass('hidden');
                                    		  parent.jQuery('.my_cart_quantity').html('1');
                                		  } else {
                                			  var old_qty = parent.jQuery('.my_cart_quantity').html();
                                			  var new_qty = parseInt(old_qty) + parseInt(1);
                                			  parent.jQuery('.my_cart_quantity').html(new_qty);                                			  
                                		  }
                                    	  window.parent.jQuery.prettyPhoto.close();
					parent.sendReq('search');
                                    	  //parent.window.location.reload();
                                      }
                                  });
                                	
                                	
                                    if (jQuery('#btnAddToCart').attr('is_auction') == 0)
                                    {
                                        e.preventDefault();
                                        //jQuery('.ajax-addtocart').click();
                                    }
                                });
//                                jQuery('#btnAddToWatchList').click(function() {
//                                    if (jQuery('#btnAddToWatchList').attr('status') == 'login')
//                                    {
//                                        var entity_id = jQuery('#btnAddToWatchList').attr('data-id');
//
//                                        jQuery('#addedoverlay').show();
//                                        showMessageCustom("Please wait...");
//                                        setTimeout(function() {
//
//                                            jQuery.ajax({
//                                                url: '<?php echo Mage::getUrl('ajaxmodule/ajax/setpricealert'); ?>product_id/' + entity_id,
//                                                success: function(data) {
//                                                }
//                                            });
//
//                                            jQuery('#addedoverlay').hide();
//                                            showMessageCustom("This Diamond Added to your Watchlist");
//                                        }, 500);
//                                    }
//                                    else
//                                    {
//                                        jQuery('#divLoginAlert').find('a').css('display', 'block');
//                                    }
//                                });
                            });


//                            function reInitTimer(entity_id, extend_time)
//                            {
//                                jQuery('.auction_timer_' + entity_id).data('countdown').update(+(new Date(extend_time))).start();
//// parent.jQuery('.modelauctiontimer_' +
//// entity_id).data('countdown').update(+(new Date(extend_time))).start();
//                                parent.reInitTimer(entity_id, extend_time);
//                            }
//
//                            function hasWhiteSpace(s) {
//                                return s.indexOf(' ') >= 0;
//                            }
//
//                            function UpdateTimerOrNot(data)
//                            {
//                                var arr = data.split(':');
//                                if (arr[0] <= 0 && arr[1] < 5)
//                                {
//                                    return true;
//                                }
//                                else
//                                {
//                                    return false;
//                                }
//                            }
//
//                            function saveBid(eid, curBid, bid_end_time)
//                            {
//                                if (jQuery('#btnAddToCart').attr('is_auction') == 1)
//                                {
//                                    curBid = parseFloat(curBid);
//                                    var bidamount = jQuery("#bid_price").val();
//// var productids = jsonGridData.map(function(product, index) { return
//// product.entity_id; });
//                                    if (!hasWhiteSpace(bidamount) && bidamount != "")
//                                    {
//                                        bidamount = parseFloat(bidamount);
//                                        if (bidamount > curBid && bidamount < 0)
//                                        {
//                                            if (confirm('Are your sure to make this bid?'))
//                                            {
//// add minute
//                                                var timerString = jQuery('.auction_timer_' + eid).html();
//                                                var is_extend_time = UpdateTimerOrNot(timerString);
//                                                jQuery.ajax({
//                                                    url: '<?php echo $this->getUrl("ajaxmodule/ajax/saveBid") ?>',
//                                                    type: 'POST',
//                                                    data: {product_id: eid, bid_amount: bidamount, is_extend_time: is_extend_time},
//                                                    async: false,
//                                                    success: function(data) {
//                                                        console.log('popup' + data);
//                                                        if (data != 'Error')
//                                                        {
//                                                            jQuery('.customer_bid_' + eid).html(bidamount);
//                                                            parent.jQuery('div[cust_id="customer_bid' + eid + '"] > span').html(bidamount);
//                                                        } else {
//                                                            alert('Bid amount invalid');
//                                                        }
//                                                    }
//                                                });
//                                            }
//                                        }
//                                        else
//                                        {
//                                            alert('Bid amount must be less then 0 and greater then current bid');
//                                        }
//                                    }
//                                    else
//                                    {
//                                        alert("Please enter bid price");
//                                    }
//                                }
//                            }


                            function showMessageCustom(message)
                            {
                                jQuery('body').append('<div class="ajax-message"></div>');
                                jQuery('.ajax-message').fadeIn(400);
                                jQuery('.ajax-message').html(message).append('<div id="ajax-close"></div>');
                                jQuery('#ajax-close').click(function() {
                                    jQuery('.ajax-message').fadeOut(400);
                                });
                                jQuery('.ajax-message').slideDown('400', function() {
                                    setTimeout(function() {
                                        jQuery('.ajax-message').slideUp('400', function() {
                                            jQuery(this).fadeOut(400, function() {
                                                jQuery(this).detach();
                                            })
                                        });
                                    }, 7000)
                                });
                            }

//                            function bulkAddToCart()
//                            {
//                                var products = [];
//                                if (jQuery('#btnAddToCart').attr('status') == 'login')
//                                {
//                                    jQuery('#addedoverlay').show();
//                                    showMessageCustom("Please wait...");
//                                    setTimeout(function() {
//                                        jQuery.each(jsonCompareData, function(index, key) {
//                                            products.push(jsonCompareData[index].entity_id);
//                                        });
//
//                                        var url = '<?php echo $this->getUrl("ajaxmodule/ajax/addtocart") ?>products/' + products + '/qty/1/';
//                                        jQuery.ajax({
//                                            url: url,
//                                            type: 'POST',
//                                            async: false,
//                                            success: function(data) {
//                                            }
//                                        });
//
//                                        jQuery('#addedoverlay').hide();
//                                        showMessageCustom("Diamonds added into cart successfully!!!");
//                                        window.location.href = '<?php echo $this->getUrl(); ?>';
//                                    }, 500);
//                                }
//                                else
//                                {
//                                    showMessageCustom("Login Required");
//                                }
//                            }
//
//                            function addToWishList(entity_id)
//                            {
//                                jQuery.ajax({
//                                    url: '<?php echo $this->getUrl("ajaxmodule/ajax/wishlist") ?>product/' + entity_id,
//                                    type: 'POST',
//                                    async: false,
//                                    success: function(data) {
//                                        window.location.href = '<?php echo $this->getUrl() ?>';
//                                    }
//                                });
//                            }
                            function refreshBidColumn(product_id, current_bid, product_bid_count)
                            {
                                jQuery('.current_bid_' + product_id).html(current_bid);
                                jQuery('.current_bid_' + product_id).css({'background': '#aa3c49', 'color': 'white'});
                                setTimeout(function() {
                                    jQuery('.current_bid_' + product_id).css({'background': '', 'color': ''});
                                }, 5000);

                                var minbidamount = parseFloat(current_bid) + parseFloat(0.11);
                                jQuery('.minbid_' + product_id).html('Enter ' + minbidamount.toFixed(2) + ' or Less');

                                parent.refreshBidColumn(product_id, current_bid, product_bid_count);
// model data refresh
                                /*
								 * parent.jQuery('.modelcurrentbid_'+product_id).html(current_bid).css('background','#aa3c49').css('color','white');
								 * setTimeout(function() {
								 * parent.jQuery('.modelcurrentbid_'+product_id).css('background','').css('color','');
								 * },5000);
								 */
                            }
