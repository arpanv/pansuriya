// Take All CSS and JS from website.
// neeed to change all class name of the css.
// Take care for all classes and ID which are used into js.
// Identify all the json request for the data from database.
	
	//var domainname = "http://192.168.1.14:8069/website-test/";
var domainname = "http://"+window.location.host+"/website-pansuriya/";

	var jsonGridData = [];
    var jsonBidData = [];
    var customer_bid = '';

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
        

    jQuery(document).ready(function() {
    	  //alert('ready');
          /*openerp.jsonRpc("/website-test/submit_json", 'call', {
              'data': {'field1':'data1','field2':'data2'} })
              .then(function (data) {
            	 alert(data); 
              });*/
    	  
//	      jQuery.ajax({
//	      url: 'http://localhost:8069/website-test/submit',
//	      type: 'POST',
//	      data: {'field1':'data1','field2':'data2'},
//	      success: function(data) {
//	
//	          alert(data);
//	      }
//	  });
    	
    //});
    
    console.log('on ready call...');
		jQuery(document).mouseup(function (e)
		{
			var container = jQuery(".bidModelDiv");
			if (!container.is(e.target) // if the target of the click isn't the container...
				&& container.has(e.target).length === 0) // ... nor a descendant of the container
			{
				jQuery('#overlay').fadeOut()
			}			
		});
		
		jQuery('.closemodel').click(function(){			
			jQuery('#overlay').fadeOut();
		});		
		
		jQuery('#grid3').click(function() {
			//alert('mb');
			var active_tab_name = "mybid";
			//jQuery(".DivMyBidInnerData").html('<img style="padding-left:350px" src="<?php echo Mage::getBaseUrl(Mage_Core_Model_Store::URL_TYPE_SKIN); ?>themeforest/images/ajax-loader.gif" alt="Please wait" />');
			jQuery.ajax({
				url: '',
				success: function(data) {
					var objGridData = jsonBidData = JSON.parse(data);
					jQuery(".DivMyBidInnerData").html('');
					jQuery.each(objGridData, function(index, key) {
						if (objGridData[index].booked == 1)
						{
							bg_color = 'background-color:#D0282D;';
							color = 'color:white;';
						}
						else
						{
							bg_color = '';
							color = '';
						}
						if (index % 2 == 0) {
							tempClassType = "even";
						} else {
							tempClassType = "odd";
						}
						var imgProd;
						if (objGridData[index].imgStatus == 1) {
							imgProd = "camera_blue.png";
						} else {
							imgProd = "camera_gray.png";
						}

						/*
						 * 						var tempGridJsonData = '<div class="gridrow '+tempClassType+'" onmouseover="showPopDiv(this,1,'+objGridData[index].entity_id+')" onmouseout="showPopDiv(this,0)" class='+tempDivclass+'>'+
						 */

						var tempCheckBoxClass = "chkCompare" + index;
						var tempDivclass = "DivImg" + index;

						var tooltip_html = '';
						var bid_column = ''; 

						if(objGridData[index].is_auction == 1) { 				
							
							bid_column = '<div class="gridcolumn21 makebid" cust_id="customer_bid' + objGridData[index].entity_id + '">'+
									'<span>' + objGridData[index].customer_bid_amount + '</span>'+
									'<button class="makebid_button makebid_button_' + objGridData[index].entity_id + '" id="makebid_button_' + objGridData[index].entity_id + '" type="button">Make Bid</button>'+
									'<div id="makebid_button_'+ objGridData[index].entity_id +'_div" class="makebid_div makebid_button_'+ objGridData[index].entity_id +'_div">'+
									'<form><input placeholder="Price" type="text" class="input-text mybid_price_'+ objGridData[index].entity_id +'" name="bid_price" id="bid_price_'+ objGridData[index].entity_id +'" />'+
									'<br/> <button onclick="saveBid('+ objGridData[index].entity_id + ',' + objGridData[index].back_percentage +',' + new Date(objGridData[index].auction_end_time).getTime() + ',1)" type="button">'+
									' Place Bid </button> <button onclick="closeBidDiv('+ objGridData[index].entity_id + ')" type="button">'+
									'Close</button> </form> </div> </div>';
						} else {
							tooltip_html = '';
							bid_column = '<div class="gridcolumn21" cust_id="customer_bid' + objGridData[index].entity_id + '"><span>' + objGridData[index].customer_bid_amount + '</span> </div>';
						}
						var tempGridJsonData = '<div id="gridrow_'+ objGridData[index].entity_id +'" class="gridrow_'+ objGridData[index].entity_id+' gridrow ' + tempClassType +' '+tempDivclass +'" style=' + bg_color + color + '>' +                   
												'<div class="gridcolumn1" onClick="showFullPopDiv(' + objGridData[index].entity_id + ', ' + objGridData[index].imgStatus + ')" style="cursor:pointer;color:#29A1B5;">' + objGridData[index].sku + '</div>' +
												'<div class="gridcolumn2">' + objGridData[index].shape + '</div>' +
												'<div class="gridcolumn3">' + objGridData[index].carat + '</div>' +
												'<div class="gridcolumn4">' + objGridData[index].color + '</div>' +
												'<div class="gridcolumn5">' + objGridData[index].clarity + '</div>' +
												'<div class="gridcolumn6">' + objGridData[index].cut + '</div>' +
												'<div class="gridcolumn7">' + objGridData[index].polish + '</div>' +
												'<div class="gridcolumn8">' + objGridData[index].symmetry + '</div>' +
												'<div class="gridcolumn9">' + objGridData[index].florescence + '</div>' +
												'<div class="gridcolumn11">' + objGridData[index].table + '</div>' +
												'<div class="gridcolumn12">' + objGridData[index].m1 +' * '+ objGridData[index].m2 + ' * '+ objGridData[index].m3 +'</div>' +                    
												'<div class="gridcolumn20"><a target="_blank" href="' + objGridData[index].certificate_link + '">' + objGridData[index].lab + '</a></div>' +
												'<div class="gridcolumn17">' + objGridData[index].rapnet_price + '</div>' +
												'<div class="gridcolumn18">' + objGridData[index].carat_price + '</div>' +                    
												'<div class="gridcolumn19">' + objGridData[index].price + '</div>' +
												'<div class="gridcolumn0"><a style="cursor:pointer"  onClick="showFullPopDiv(' + objGridData[index].entity_id + ', ' + objGridData[index].imgStatus + ', ' + index + ')"><img src="/website_pansuriya/static/src/images/' + imgProd + '"></div></a>' +
												'<div class="gridcolumn16 makebid'+objGridData[index].entity_id+'">' + objGridData[index].back_percentage + '</div>' +                    
												bid_column +                    
												'<div class="gridcolumn22 auction_timer_'+objGridData[index].entity_id+'" id="auction_timer_'+objGridData[index].entity_id+'">'+ objGridData[index].auction_time +'</div>' +
												'<div class="gridcolumn15"><a href="javascript:void(0);" class="imgChk' + objGridData[index].entity_id + '" onClick="chkClickEvent(this,' + objGridData[index].entity_id + ')"><img class="imgChk" alt="check" src="/website_pansuriya/static/src/images/uncheck_box.png" /></a></div>' +                    
												'</div>' +
												'<div class="responsive_data" id="responsive_' + objGridData[index].entity_id + '"><div class="responsive_data_col_1" id="responsive_' + objGridData[index].entity_id + '_1"></div><div class="responsive_data_col_2" id="responsive_' + objGridData[index].entity_id + '_2"></div></div>';
						jQuery(".DivMyBidInnerData").append(tempGridJsonData);

						if(objGridData[index].is_auction == 1) {
														
							jQuery('.gridrow_'+ objGridData[index].entity_id).find('.gridcolumn15 > a').attr('onclick','javascript:void(0)');

							objGridData[index].auction_end_time = getAuctionEndTime(objGridData[index].current_time,objGridData[index].auction_end_time);
							
							jQuery('.auction_timer_' + objGridData[index].entity_id).countdown({
							  date: new Date(objGridData[index].auction_end_time),
							  render: function(data) {
								 data.hours = data.hours + data.days * 24;
								jQuery(this.el).html( data.hours + " : " + this.leadingZeros(data.min, 2) + " : " + this.leadingZeros(data.sec, 2));
							  },
							  onEnd: function(){
									jQuery('.makebid_button_'+objGridData[index].entity_id).remove();
									jQuery('.auction_timer_' + objGridData[index].entity_id).html('-');
								}
								});
						}
						else if(objGridData[index].is_auction == 0)
						{
							jQuery('.auction_timer_' + objGridData[index].entity_id).html('-');				
						}
					});
					
					jQuery('.makebid').hover(function() {
						jQuery(this).children('.makebid_button').show(200);
					});
					jQuery('.makebid').mouseleave(function() {
						jQuery(this).children('.makebid_button').hide(500);			
					});
					
					jQuery('.makebid_button').click(function(){
					jQuery('.makebid_div').hide(100);
					var makebidbuttonid = jQuery(this).attr('id');
					jQuery("." + makebidbuttonid + "_div").show(200);		
				}); 
				}
			});
		});

		/*window.setInterval(function() {
			refreshBidColumn();
		}, 25000);*/
		
        jQuery('#search_tab_1 input, #search_tab_1 select').keypress(function(e) {
            if (e.which == 13) {
                jQuery('#btnSearch').click();
            }
        });
        
//        jQuery('.DivGridInnerData').scroll(function()
//        {
//            var objGridData;
//			var bg_color = '';
//			var color = '';
//			var active_tab_name = "homegrid";
//            var scrollHeight = (dataLength * 30) - jQuery('.DivGridInnerData').height();
//            if (jQuery('.DivGridInnerData').scrollTop() == scrollHeight)
//            {
//
//                if (firstTime == 1)
//                {
//                    jQuery('#divNoMoreProduct').css('display', 'block');
//                    return false;
//                }
//
//                if (count_collection == dataLength)
//                {
//                    jQuery('#divNoMoreProduct').css('display', 'block');
//                    return false;
//                }
//
//                jQuery('#divMoreProductLoad').css('display', 'block');
//
//                loadData = dataLength;
//                filterParams['loadData'] = loadData;
//
//                jQuery.ajax({
//                    url: '',
//                    data: filterParams,
//                    success: function(data) {
//                        objGridData = JSON.parse(data);
//
//                        jQuery.each(objGridData, function(index, key) {
//                            var gridIndex = loadData + index;
//							if (objGridData[index].booked == 1)
//							{
//								bg_color = 'background-color:#D0282D;';
//								color = 'color:white;';
//							}
//							else
//							{
//								bg_color = '';
//								color = '';
//							}
//                            jsonGridData.push(objGridData[index]);
//                            if (index % 2 == 0) {
//                                tempClassType = "even";
//                            } else {
//                                tempClassType = "odd";
//                            }
//                            var imgProd;
//                            if (objGridData[index].imgStatus == 1) {
//                                imgProd = "camera_blue.png";
//                            } else {
//                                imgProd = "camera_gray.png";
//                            }
//
//                            var tempCheckBoxClass = "chkCompare" + index;
//                            var tempDivclass = "DivImg" + index;
//                            
//                            var tooltip_html = '';
//							var bid_column = ''; 
//							if(objGridData[index].is_auction == 1) { 				
//								bid_column = '<div class="gridcolumn21 makebid" cust_id="customer_bid' + objGridData[index].entity_id + '">'+
//										'<span>' + objGridData[index].customer_bid_amount + '</span>'+
//										'<button class="makebid_button makebid_button_'+objGridData[index].entity_id+'" id="makebid_button_' + objGridData[index].entity_id + '" type="button">Make Bid</button>'+
//										'<div id="makebid_button_'+ objGridData[index].entity_id +'_div" class="makebid_div">'+
//										'<form><input placeholder="Price" type="text" class="input-text" name="bid_price" id="bid_price_'+ objGridData[index].entity_id +'" />'+
//										'<br/> <button onclick="saveBid('+ objGridData[index].entity_id + ',' + objGridData[index].back_percentage +',' + new Date(objGridData[index].auction_end_time).getTime() + ',0)" type="button">'+
//										' Place Bid </button> <button onclick="closeBidDiv('+ objGridData[index].entity_id + ')" type="button">'+
//										'Close</button> </form> </div> </div>';
//							} else {
//								tooltip_html = '';
//								bid_column = '<div class="gridcolumn21" cust_id="customer_bid' + objGridData[index].entity_id + '"><span>' + objGridData[index].customer_bid_amount + '</span> </div>';
//							}   
//							                         
//							var tempGridJsonData = '<div id="gridrow_'+ objGridData[index].entity_id +'" class="gridrow_'+ objGridData[index].entity_id +' gridrow ' + tempClassType +' '+tempDivclass +'" style=' + bg_color + color + '>' +                   
//										'<div class="gridcolumn1" onClick="showFullPopDiv(' + objGridData[index].entity_id + ', ' + objGridData[index].imgStatus + ')" style="cursor:pointer;color:#29A1B5;">' + objGridData[index].sku + '</div>' +
//										'<div class="gridcolumn2">' + objGridData[index].shape + '</div>' +
//										'<div class="gridcolumn3">' + objGridData[index].carat + '</div>' +
//										'<div class="gridcolumn4">' + objGridData[index].color + '</div>' +
//										'<div class="gridcolumn5">' + objGridData[index].clarity + '</div>' +
//										'<div class="gridcolumn6">' + objGridData[index].cut + '</div>' +
//										'<div class="gridcolumn7">' + objGridData[index].polish + '</div>' +
//										'<div class="gridcolumn8">' + objGridData[index].symmetry + '</div>' +
//										'<div class="gridcolumn9">' + objGridData[index].florescence + '</div>' +
//										'<div class="gridcolumn11">' + objGridData[index].table + '</div>' +
//										'<div class="gridcolumn12">' + objGridData[index].m1 +' * '+ objGridData[index].m2 + ' * '+ objGridData[index].m3 +'</div>' +                    
//										'<div class="gridcolumn20"><a target="_blank" href="' + objGridData[index].certificate_link + '">' + objGridData[index].lab + '</a></div>' +
//										'<div class="gridcolumn17">' + objGridData[index].rapnet_price + '</div>' +
//										'<div class="gridcolumn18">' + objGridData[index].carat_price + '</div>' +                    
//										'<div class="gridcolumn19">' + objGridData[index].price + '</div>' +
//										'<div class="gridcolumn0"><a style="cursor:pointer"  onClick="showFullPopDiv(' + objGridData[index].entity_id + ', ' + objGridData[index].imgStatus + ', ' + index + ')"><img  src="/website_pansuriya/static/src/images' + imgProd + '"></div></a>' +
//										'<div class="gridcolumn16 makebid'+objGridData[index].entity_id+'" id="makebid' + objGridData[index].entity_id + '">' + objGridData[index].back_percentage + '</div>' +                    
//										bid_column +                    
//										'<div class="gridcolumn22 auction_timer_'+objGridData[index].entity_id+'" id="auction_timer_'+objGridData[index].entity_id+'">'+ objGridData[index].auction_time +'</div>' +                                        
//										'<div class="gridcolumn15"><a href="javascript:void(0);" class="imgChk' + objGridData[index].entity_id + '" onClick="chkClickEvent(this,' + objGridData[index].entity_id + ')"><img class="imgChk" alt="check" src="/website_pansuriya/static/src/images/uncheck_box.png" /></a></div>' +                    
//										'</div>' +
//										'<div class="responsive_data" id="responsive_' + objGridData[index].entity_id + '"><div class="responsive_data_col_1" id="responsive_' + objGridData[index].entity_id + '_1"></div><div class="responsive_data_col_2" id="responsive_' + objGridData[index].entity_id + '_2"></div></div>';
//							jQuery(".DivGridInnerData").append(tempGridJsonData);
//							if(objGridData[index].is_auction == 1) {
//
//								//desable compare functionality
//								jQuery('.gridrow_'+ objGridData[index].entity_id).find('.gridcolumn15 > a').attr('onclick','javascript:void(0)');
//								
//								objGridData[index].auction_end_time = getAuctionEndTime(objGridData[index].current_time,objGridData[index].auction_end_time);
//								
//								jQuery('.auction_timer_' + objGridData[index].entity_id).countdown({
//								  date: new Date(objGridData[index].auction_end_time),
//								  render: function(data) {
//									 data.hours = data.hours + data.days * 24;
//									jQuery(this.el).html( data.hours + " : " + this.leadingZeros(data.min, 2) + " : " + this.leadingZeros(data.sec, 2));
//								  },
//								  onEnd: function(){
//										jQuery('.makebid_button_'+objGridData[index].entity_id).remove();
//										jQuery('.auction_timer_' + objGridData[index].entity_id).html('-');
//									}
//								});
//							}
//							else if(objGridData[index].is_auction == 0)
//							{
//								jQuery('.auction_timer_' + objGridData[index].entity_id).html('-');
//							}
//							if (objGridData[index].booked == 1)
//							{
//								rowDisabled('#gridrow_'+ objGridData[index].entity_id);
//							}
//							if (objGridData[index].imgStatus == 1)
//							{
//								var url = '<?php echo $this->getUrl("ajaxmodule/ajax/ajaxpopup") ?>id/' + objGridData[index].entity_id + '?iframe=true&width=855&height=530';
//							}
//							else
//							{
//								var url = '<?php echo $this->getUrl("ajaxmodule/ajax/ajaxpopup") ?>id/' + objGridData[index].entity_id + '?iframe=true&width=855&height=500';
//							}                       
//							jQuery("#prettyPhotoLinks").append('<a class="aPrettyPhoto" id="prettyPhoto_' + objGridData[index].entity_id + '" href="' + url + '" rel="prettyPhoto[iframe]">abc</a>');
//                        });
//                        
//						dataLength = jsonGridData.length;
//						jQuery('.aPrettyPhoto').prettyPhoto({
//							overlay_gallery: false,
//							social_tools: '',
//							animation_speed: 'fast',
//							slideshow: 10000,
//							deeplinking: false,
//							hideflash: true
//						});
//												
//						
//                        jQuery('#divMoreProductLoad').css('display', 'none');
//                        dataLength = jsonGridData.length;
//                        
//                        jQuery('.gridrow').hover(function() {
//							jQuery(this).children('.makebid').children('.makebid_button').show(200);
//						});
//						jQuery('.gridrow').mouseleave(function() {
//							jQuery(this).children('.makebid').children('.makebid_button').hide(500);			
//						});
//                    }
//                });
//            }
//            else
//            {
//                jQuery('#divNoMoreProduct').css('display', 'none');
//                return false;
//            }
//        });
        
/*
        jQuery('.nav-tabs .with_icon').find('a').click(function() {
            var href = jQuery(this).attr('href').charAt(jQuery(this).attr('href').length - 1);
            jQuery('#grid' + href).trigger('click');
        });
*/

        jQuery('.clear_filters').click(function()
        {
            jQuery("#shape").val(""); //.next().find("span").html("Round");
            jQuery("#color,#color_to,#clarity,#clarity_to,#cut,#cut_to,#polish,#polish_to,#symmetry,#symmetry_to,#fluorescence,#fluorescence_to,#lab,#girdle_from,#girdle_to,#culet_size,#culet_condition").val(""); //.next().find("span").html("Any");
            jQuery("#carat,#carat_to,#table,#table_to,#carat_price,#carat_price_to,#price,#price_to,#back,#back_to,#m1,#m1_to,#m2,#m2_to,#m3,#m3_to").val("");

            setTimeout(function() {
                sendReq('clear');
            }, 250);
        });

        jQuery('#headingAdvanceSearch').click(function() {
            jQuery("#carat_price,#carat_price_to,#price,#price_to,#back,#back_to,#m1,#m1_to,#m2,#m2_to,#m3,#m3_to").val('');

            jQuery(this).find('img').toggle();

            jQuery('#divAdvanceSearch').slideToggle('slow');
        });

        jQuery('.compareProd').html('compare & checkout(' + compareCount + ')');

        jQuery(".signin").click(function(e) {
            e.preventDefault();
            jQuery("fieldset#signin_menu").toggle();
            jQuery(".signin").toggleClass("menu-open");
        });

        jQuery("fieldset#signin_menu").mouseup(function() {
            return false
        });
        jQuery(document).mouseup(function(e) {
            if (jQuery(e.target).parent("a.signin").length == 0) {
                jQuery(".signin").removeClass("menu-open");
                jQuery("fieldset#signin_menu").hide();
            }
        });

        sendReq('home');

        jQuery('.DivGridInnerData,.CompareGridInnerData').slimscroll({
            color: '#666',
            background: '#666',
            size: '0px',
            wheelStep: 30
        });

        jQuery('#selLocation').slimscroll({
            color: '#666',
            background: '#666',
            size: '0px',
            wheelStep: 3
        });

        /*     
         jQuery("#location").focus();
         jQuery("#location option:eq(0)").prop('selected', true);
         
         jQuery('.select').click(function(e) {
         alert('test');
         });
         */
        jQuery('#btnAddToCart, #btnAddToWishList').click(function() {
        	alert('tess');
//            if (jQuery('#btnAddToCart').attr('status') == 'login')
//            {
//                jQuery.fancybox.close();
//            }
//            else
//            {
//                jQuery('#divLoginAlert').css('display', 'block');
//            }
        });

        jQuery('#btnAddToWatchList').click(function() {

            if (jQuery('#btnAddToWatchList').attr('status') == 'login')
            {
                var entity_id = jQuery('#btnAddToWatchList').attr('data-id');

                jQuery.fancybox.close();
                jQuery('#addedoverlay').show();
                showMessageCustom("Please wait...");
                setTimeout(function() {

                    jQuery.ajax({
                        url: '',
                        success: function(data) {
                        }
                    });

                    jQuery('#addedoverlay').hide();
                    showMessageCustom("This Diamond Added to your Watchlist");
                }, 500);
            }
            else
            {
                jQuery('#divLoginAlert').css('display', 'block');
            }
        });
             
    });
    
    function minutesDiff(system_time, server_time) 
 	{ 
 		var minute=1000*60; 
 		return Math.ceil((server_time.getTime()-system_time.getTime())/(minute)); 
 	} 

    function computeCompareData()
    {
        var carat = [];
        var carat_price = [];
        var discount = [];
        if (jsonCompareData.length > 0)
        {
            jsonCompareData.forEach(function(value, index, ar) {
                carat.push(parseFloat(value.carat));
                carat_price.push(parseInt(value.carat_price));
                if (value.back_percentage != '' && value.back_percentage != null)
                {
                    discount.push(parseInt(value.back_percentage));
                }
            });
            var total_carat = carat.reduce(function(previousValue, currentValue, index, array) {
                return previousValue + currentValue;
            });
            var total_carat_price = carat_price.reduce(function(previousValue, currentValue, index, array) {
                return previousValue + currentValue;
            });

            var total_discount = discount.reduce(function(previousValue, currentValue, index, array) {
                return previousValue + currentValue;
            });
            var avg_carat_price = total_carat_price / jsonCompareData.length;
            var avg_discount = total_discount / discount.length;
            jQuery('.productsummary > #carat').html('Carat : ' + total_carat.toFixed(2));
            jQuery('.productsummary > #carat_price').html('$/Carat : ' + avg_carat_price.toFixed(2));
            jQuery('.productsummary > #discount').html('Back (%) : ' + avg_discount.toFixed(2));
        }
        if (jsonCompareData.length == 0)
        {
            jQuery('.productsummary > #carat').html('');
            jQuery('.productsummary > #carat_price').html('');
            jQuery('.productsummary > #discount').html('');
        }

    }
    
    function refreshBidColumn(product_id,current_bid,product_bid_count)
    {
		
		jsonGridData = jsonGridData.map(function(collection, index) {						
			if(product_id == collection.entity_id)
			{				
				collection.back_percentage = current_bid;
				collection.product_bid_count = product_bid_count;			
			}		
			return collection;						
		});		
		
		jQuery('.makebid'+product_id).html(current_bid).css('background','#aa3c49').css('color','white');		
		setTimeout(function() {
			jQuery('.makebid'+product_id).css('background','').css('color','');			
		},5000);
		
		//model data refresh
		jQuery('.modelcurrentbid_'+product_id).html(current_bid).css('background','#aa3c49').css('color','white');		
		setTimeout(function() {
			jQuery('.modelcurrentbid_'+product_id).css('background','').css('color','');			
		},5000);
		var minbidamount = parseFloat(current_bid) + parseFloat(0.11);
		jQuery('.minbid_'+product_id).html('Enter '+minbidamount.toFixed(2)+' or Less');
		jQuery('.product_bid_count_'+product_id).html(product_bid_count+' Bids');
		if(jQuery('.bidModelDiv').attr('product_id') == product_id)
		{
			//reOpenModel(product_id);
		}		
	}
	/*function refreshBidColumn()
	{
		var productids = jsonGridData.map(function(product, index) { return product.entity_id; });
		var backgroundcolor_elements = color_elements = [];
		try {
			jQuery.ajax({
				url: '<?php echo $this->getUrl("ajaxmodule/ajax/refreshBidColumn") ?>',
				type: 'POST',
				data: {product_ids: productids},
				async: false,
				success: function(data) {
					var bidColumn = JSON.parse(data);
					jsonGridData = jsonGridData.map(function(product, index) {
						var bid = bidColumn.filter(function(bid){ 
							if(bid.entity_id == product.entity_id) { 
								return bid; 
							} 
						});
						
						if(product.back_percentage != bid[0].back_percentage) {
							backgroundcolor_elements.push('#makebid'+product.entity_id);
							color_elements.push('#makebid'+product.entity_id+' > span');
						}
						
						product.back_percentage = bid[0].back_percentage;
						product.customer_bid_amount = bid[0].customer_bid_amount;
						jQuery('#makebid'+product.entity_id).html(product.back_percentage);
						jQuery('div[cust_id="customer_bid'+product.entity_id+'"] > span').html(product.customer_bid_amount);
						return product;
					});
				}
			});
			
			if(jQuery('#featured_news_tab_4').attr('class').search('active') > 0) {
				var bid_productids = jsonBidData.map(function(product, index) { return product.entity_id; });

				jQuery.ajax({
					url: '<?php echo $this->getUrl("ajaxmodule/ajax/refreshBidColumn") ?>',
					type: 'POST',
					data: {product_ids: bid_productids},
					async: false,
					success: function(data) {
						var bidColumn = JSON.parse(data);
						jsonBidData = jsonBidData.map(function(product, index) {
							var bid = bidColumn.filter(function(bid){ 
								if(bid.entity_id == product.entity_id) { 
									return bid; 
								} 
							});
							if(product.back_percentage != bid[0].back_percentage) {
								backgroundcolor_elements.push('#bidgrid_makebid'+product.entity_id);
								color_elements.push('#bidgrid_makebid'+product.entity_id+' > span');
							}
							
							product.back_percentage = bid[0].back_percentage;
							product.customer_bid_amount = bid[0].customer_bid_amount;
							jQuery('#bidgrid_makebid'+product.entity_id+' > span').html(product.back_percentage);
							jQuery('#bidgrid_customer_bid'+product.entity_id+' > span').html(product.customer_bid_amount);
							return product;
						});
						
					}
				});
			}
		} catch(err) {
			
		}
		
		jQuery(backgroundcolor_elements.join()).css('background','#aa3c49');
		jQuery(color_elements.join()).css('color','white');
		//jQuery('.gridcolumn16').children('span').css('color','white');
		setTimeout(function() {
			jQuery(backgroundcolor_elements.join()).css('background','');
			jQuery(color_elements.join()).css('color','');
		},5000);
	}*/

    /*function setRangeAttribute(from, to, name)
    {
        var from_label, to_label, options;
        var flag = false;
        var result = "";
        if (from == '')
        {
            return '';
        }

        jQuery.ajax({
            url: '',
            async: false,
            data: {name: name},
            success: function(data) {
                options = JSON.parse(data);
            }
        });

        jQuery.each(options, function(index, key) {
            if (options[index].value == from)
            {
                from_label = options[index].label;
            }
            if (options[index].value == to)
            {
                to_label = options[index].label;
            }
        });

        jQuery.each(options, function(index, key) {

            if (options[index].label == from_label)
            {
                flag = true;
            }
            if (flag == true)
            {
                result += options[index].value + ',';
            }
            if (options[index].label == to_label)
            {
                flag = false;
            }
        });
        //jQuery("html, body").animate({scrollTop: jQuery("#featured_news").offset().top },2000);
        return result.substring(0, result.length - 1);
    }*/
//
    function sendReq(type)
    {    	
    	var isfirstreq = 0;
//        var url = 'http://localhost:8069/website-test/submit_json';
        var shape, carat, carat_to, color, colorto, clarity, cut, polish, symmetry, fluorescence, lab, table, table_to, location, girdle_from, girdle_to;
        var culet_size, culet_condition, m1, m1_to, m2, m2_to, m3, m3_to, carat_price, carat_price_to, price, price_to, back, back_to, report_no, reference_no;
        if (type == "click")
        {
        	
            if (jQuery('#carat').val() == '')
            {
                jQuery('#carat, #carat_to').css('background-color', '#f9d7cf').css('border', '#f9d7cf');
                jQuery('#carat').focus();
                return;
            }
            

            //jQuery("html, body").animate({scrollTop: jQuery("#featured_news").offset().top },2000);
			
            jQuery('#carat, #carat_to').css('background-color', '').css('border', '');
            shape = document.getElementById('shape').value;
            carat = document.getElementById('carat').value;
            carat_to = document.getElementById('carat_to').value;

            /*color = setRangeAttribute(document.getElementById('color').value, document.getElementById('color_to').value, 'color');
            clarity = setRangeAttribute(document.getElementById('clarity').value, document.getElementById('clarity_to').value, 'clarity');
            cut = setRangeAttribute(document.getElementById('cut').value, document.getElementById('cut_to').value, 'cut');
            polish = setRangeAttribute(document.getElementById('polish').value, document.getElementById('polish_to').value, 'polish');
            symmetry = setRangeAttribute(document.getElementById('symmetry').value, document.getElementById('symmetry_to').value, 'symmetry');
            fluorescence = setRangeAttribute(document.getElementById('fluorescence').value, document.getElementById('fluorescence_to').value, 'fluorescence');*/
            
            color = $( "#color" ).val();
            color_to = $( "#color_to" ).val();
            clarity = $( "#clarity" ).val();
            clarity_to = $( "#clarity_to" ).val();
            cut = $( "#cut" ).val();
            cut_to = $( "#cut_to" ).val();
            polish = $( "#polish" ).val();
            polish_to = $( "#polish_to" ).val();
            symmetry = $( "#symmetry" ).val();
            symmetry_to = $( "#symmetry_to" ).val();
            fluorescence = $( "#fluorescence" ).val();
            fluorescence_to =$( "#fluorescence_to" ).val();

            lab = document.getElementById('lab').value;
            table = document.getElementById('table').value;
            table_to = document.getElementById('table_to').value;

            // advance search criteria

            girdle_from = document.getElementById('girdle_from').value;
            girdle_to = document.getElementById('girdle_to').value;

            culet_size = jQuery('#culet_size').val();
            culet_condition = jQuery('#culet_condition').val();
            location = jQuery('#selLocation').val();
			if(location != null && location[0].length == 0) {
				location = null;
			}
            m1 = document.getElementById('m1').value;
            m1_to = document.getElementById('m1_to').value;
            m2 = document.getElementById('m2').value;
            m2_to = document.getElementById('m2_to').value;
            m3 = document.getElementById('m3').value;
            m3_to = document.getElementById('m3_to').value;
            carat_price = document.getElementById('carat_price').value;
            carat_price_to = document.getElementById('carat_price_to').value;
            price = document.getElementById('price').value;
            price_to = document.getElementById('price_to').value;
            back = document.getElementById('back').value;
            back_to = document.getElementById('back_to').value;
            report_no = document.getElementById('report_no').value;
            reference_no = document.getElementById('reference_no').value;

            firstTime = 0;
        }
        else if(type == 'search')
        {
        	
			jQuery('#carat, #carat_to').css('background-color', '').css('border', '');
            shape = document.getElementById('shape').value;
            carat = document.getElementById('carat').value;
            carat_to = document.getElementById('carat_to').value;

            /*color = setRangeAttribute(document.getElementById('color').value, document.getElementById('color_to').value, 'color');
            clarity = setRangeAttribute(document.getElementById('clarity').value, document.getElementById('clarity_to').value, 'clarity');
            cut = setRangeAttribute(document.getElementById('cut').value, document.getElementById('cut_to').value, 'cut');
            polish = setRangeAttribute(document.getElementById('polish').value, document.getElementById('polish_to').value, 'polish');
            symmetry = setRangeAttribute(document.getElementById('symmetry').value, document.getElementById('symmetry_to').value, 'symmetry');
            fluorescence = setRangeAttribute(document.getElementById('fluorescence').value, document.getElementById('fluorescence_to').value, 'fluorescence');
             */
            color = $( "#color" ).val();
            color_to = $( "#color_to" ).val();
            clarity = $( "#clarity" ).val();
            clarity_to = $( "#clarity_to" ).val();
            cut = $( "#cut" ).val();
            cut_to = $( "#cut_to" ).val();
            polish = $( "#polish" ).val();
            polish_to = $( "#polish_to" ).val();
            symmetry = $( "#symmetry" ).val();
            symmetry_to = $( "#symmetry_to" ).val();
            fluorescence = $( "#fluorescence" ).val();
            fluorescence_to =$( "#fluorescence_to" ).val();
            
            lab = document.getElementById('lab').value;
            table = document.getElementById('table').value;
            table_to = document.getElementById('table_to').value;

            // advance search criteria

            girdle_from = document.getElementById('girdle_from').value;
            girdle_to = document.getElementById('girdle_to').value;

            culet_size = jQuery('#culet_size').val();
            culet_condition = jQuery('#culet_condition').val();
            location = jQuery('#selLocation').val();
			if(location != null && location[0].length == 0) {
				location = null;
			}
            m1 = document.getElementById('m1').value;
            m1_to = document.getElementById('m1_to').value;
            m2 = document.getElementById('m2').value;
            m2_to = document.getElementById('m2_to').value;
            m3 = document.getElementById('m3').value;
            m3_to = document.getElementById('m3_to').value;
            carat_price = document.getElementById('carat_price').value;
            carat_price_to = document.getElementById('carat_price_to').value;
            price = document.getElementById('price').value;
            price_to = document.getElementById('price_to').value;
            back = document.getElementById('back').value;
            back_to = document.getElementById('back_to').value;
            report_no = document.getElementById('report_no').value;
            reference_no = document.getElementById('reference_no').value;

            firstTime = 0;
		}
        else
        {
            shape = document.getElementById('shape').value;
        	//shape = 37;
            cut_to = "";
            color_to = "";
            clarity_to ="";
            carat_to="";
            polish_to="";
            symmetry_to="";
            fluorescence_to ="";
            table_to="";
            carat_price_to="";
            price_to="";
            back_to="";
            girdle_to="";
            m1_to="";
            m2_to="";
            m3_to="";           
            
            isfirstreq = 1;
        }
        
        jQuery('#divNoMoreProduct').css('display', 'none');

        if(type != 'search')
		{
			jQuery(".DivGridInnerData").html('');        
			jQuery(".DivGridInnerData").html('<img style="padding-left:350px" src="/website_pansuriya/static/src/images/ajax-loader.gif" alt="Please wait" />');
		}

        loadData = 0;
        
        
                
        filterParams = {shape: shape, cut: cut, cut_to:cut_to, color: color, color_to: color_to, clarity: clarity, clarity_to: clarity_to, carat: carat, 
        		carat_to: carat_to, polish: polish, polish_to: polish_to, symmetry: symmetry,symmetry_to: symmetry_to,
            lab: lab, fluorescence: fluorescence, fluorescence_to: fluorescence_to, table: table, table_to: table_to, carat_price: carat_price, carat_price_to: carat_price_to,
            price: price, price_to: price_to, back: back, back_to: back_to, girdle_from: girdle_from, girdle_to: girdle_to,
            culet_size: culet_size, culet_condition: culet_condition, m1: m1, m1_to: m1_to, m2: m2, m2_to: m2_to, m3: m3, m3_to: m3_to,
            report_no: report_no, reference_no: reference_no, loadData: loadData, location: location, isfirstreq: isfirstreq};
        
        //return;
        
        /*jQuery.ajax({
            url: 'http://localhost:8069/',
            type: 'POST',
            data: filterParams,
            success: function(data) {

                jsonGridData = JSON.parse(data);
                if (type == "click")
                {
                    jQuery("html, body").animate({scrollTop: jQuery("#featured_news").offset().top}, 2000);
                }
                if (jsonGridData.length > 0) {
                    count_collection = jsonGridData[0].count_collection;

                    dataLength = jsonGridData.length;
                    if (jsonGridData.length <= 0) {
                        jQuery(".DivGridInnerData").html('<div class="gridrow even">No diamond found with specified criteria, please modify criteria and try again.</div>');
                    } else {
                        loadGridData(jsonGridData);
                    }
                }
                else {
                    jQuery(".DivGridInnerData").html('<div class="gridrow even">No diamond found with specified criteria, please modify criteria and try again.</div>');
                }
            }
        });*/
        //console.log(JSON.stringify(filterParams));
        openerp.jsonRpc("/website-pansuriya/submit_json", 'call', {
            'data': filterParams})
            .then(function (data) {
             
             jsonGridData = data;
             if (type == "click")
             {
                 jQuery("html, body").animate({scrollTop: jQuery("#featured_news").offset().top}, 2000);
             }
             if (jsonGridData.length > 0) {
                 count_collection = jsonGridData[0].count_collection;

                 dataLength = jsonGridData.length;
                 if (jsonGridData.length <= 0) {
                     jQuery(".DivGridInnerData").html('<div class="gridrow even">No diamond found with specified criteria, please modify criteria and try again.</div>');
                 } else {
                     loadGridData(jsonGridData);
                 }
             }
             else {
                 jQuery(".DivGridInnerData").html('<div class="gridrow even">No diamond found with specified criteria, please modify criteria and try again.</div>');
             }
          	 
            });
    }
//
    var tempClassType = "";

    function gridSortData(gridFilterattr)
    {
        var imgId = ".div" + gridFilterattr;
        var tempGridFilterAttr = gridFilterattr;
        //var tempFilterGridData = sortJSON(jsonGridData,tempGridFilterAttr);
        var tempFilterGridData = "";

        var rmImgId = ".div" + tempFlagFilterAttr;


        jQuery(rmImgId).attr('src', '/website_pansuriya/static/src/images/arrow_up_down.png');
        jQuery(rmImgId).attr('style', '');

        if (tempFlagFilterAttr == tempGridFilterAttr) {
            if (tempFlagFilterSort == 1) {
                tempFlagFilterSort = 0;
            } else {
                tempFlagFilterSort = 1;
            }
        } else {
            tempFlagFilterSort = 1;
        }

        if (tempFlagFilterSort == 1) {

            jQuery(imgId).removeAttr("style");
            jQuery(imgId).attr('src', '/website_pansuriya/static/src/images/arrow_up.png');
            jQuery(imgId).attr('style', '');
            jQuery(imgId).css('height', '4px');
            jQuery(imgId).css('width', '7px');

        } else {

            jQuery(imgId).removeAttr("style");
            jQuery(imgId).attr('src', '/website_pansuriya/static/src/images/arrow_down.png');
            jQuery(imgId).attr('style', '');
            jQuery(imgId).css('height', '4px');
            jQuery(imgId).css('width', '7px');
        }

        if (gridFilterattr == "sku" || gridFilterattr == "shape" || gridFilterattr == "date" || gridFilterattr == "color" || gridFilterattr == "polish" || gridFilterattr == "symmetry" || gridFilterattr == "clarity" || gridFilterattr == "florescence")
        {
            tempFilterGridData = jsonGridData.sort(sort_by(gridFilterattr, tempFlagFilterSort, function(a) {
                return a.toString().toUpperCase()
            }));
        }
        else
        {
            tempFilterGridData = jsonGridData.sort(sort_by(gridFilterattr, tempFlagFilterSort, parseFloat));
        }
        loadGridData(tempFilterGridData);
        tempFlagFilterAttr = tempGridFilterAttr;
    }

    function compareSortData(gridFilterattr)
    {
        var imgId = "#comparediv" + gridFilterattr;
        var tempGridFilterAttr = gridFilterattr;

        var tempFilterGridData = "";

        var rmImgId = "#comparediv" + compareFlagFilterAttr;

        jQuery(rmImgId).attr('src', '/website_pansuriya/static/src/images/arrow_up_down.png');
        jQuery(rmImgId).attr('style', '');

        if (compareFlagFilterAttr == tempGridFilterAttr) {
            if (compareFlagFilterSort == 1) {
                compareFlagFilterSort = 0;
            } else {
                compareFlagFilterSort = 1;
            }
        } else {
            compareFlagFilterSort = 1;
        }

        if (compareFlagFilterSort == 1) {

            jQuery(imgId).removeAttr("style");
            jQuery(imgId).attr('src', '/website_pansuriya/static/src/images/arrow_up.png');
            jQuery(imgId).attr('style', '');
            jQuery(imgId).css('height', '4px');
            jQuery(imgId).css('width', '7px');
        } else {
            jQuery(imgId).removeAttr("style");
            jQuery(imgId).attr('src', '/website_pansuriya/static/src/images/arrow_down.png');
            jQuery(imgId).attr('style', '');
            jQuery(imgId).css('height', '4px');
            jQuery(imgId).css('width', '7px');
        }

        if (gridFilterattr == "shape" || gridFilterattr == "date" || gridFilterattr == "color" || gridFilterattr == "polish" || gridFilterattr == "symmetry" || gridFilterattr == "clarity" || gridFilterattr == "florescence")
        {
            tempFilterGridData = jsonCompareData.sort(sort_by(gridFilterattr, compareFlagFilterSort, function(a) {
                return a.toString().toUpperCase()
            }));
        }
        else
        {
            tempFilterGridData = jsonCompareData.sort(sort_by(gridFilterattr, compareFlagFilterSort, parseFloat));
        }
        loadCompareGridData(tempFilterGridData);
        compareFlagFilterAttr = tempGridFilterAttr;
    }

    var sort_by = function(field, reverse, primer) {

        var key = function(x) {
            return primer ? primer(x[field]) : x[field]
        };

        return function(a, b) {
            var A = key(a), B = key(b);
            return ((A < B) ? -1 : (A > B) ? +1 : 0) * [-1, 1][+!!reverse];
        }
    }
    function chkClickEvent(objBtn, entity_id)
    {
        if (jQuery(objBtn).find("img").attr('alt') == "check")
        {
            jQuery(objBtn).html('<img class="imgChk" alt="uncheck" src="/website_pansuriya/static/src/images/check_box.png" />');
            loadCompareGridData(entity_id, 'add');
        }
        else if (jQuery(objBtn).find("img").attr('alt') == "uncheck")
        {
            jQuery(objBtn).html('<img class="imgChk" alt="check" src="/website_pansuriya/static/src/images/uncheck_box.png" />');
            //jQuery('.gridhead > .gridcolumn15').html('<a href="javascript:void(0);" class="chkHead" onClick="chkClickAll(this)"><img class="imgChk" alt="check" src="images/uncheck_box.png" /></a>');

            removeCompareRow(entity_id, objBtn);
        }

    }
    function chkClickAll(objBtn)
    {
        if (jQuery(objBtn).find("img").attr('alt') == "check")
        {
            jQuery(objBtn).find('img').attr('alt', 'uncheck').attr('src', '/website_pansuriya/static/src/images/check_box.png');
            jQuery('.gridrow > .gridcolumn15').find('img').attr('src', '/website_pansuriya/static/src/images/check_box.png').attr('alt', 'uncheck');
            compareCount = dataLength;
            jsonCompareData = jsonGridData;
            setCompareGrid();
        }
        else if (jQuery(objBtn).find("img").attr('alt') == "uncheck")
        {
            jQuery(objBtn).find('img').attr('alt', 'check').attr('src', '/website_pansuriya/static/src/images/uncheck_box.png');
            jQuery('.gridrow > .gridcolumn15').find('img').attr('src', '/website_pansuriya/static/src/images/uncheck_box.png').attr('alt', 'check');

            jsonCompareData = [];
            setCompareGrid();
            compareCount = 0;
        }
        jQuery('.compareProd').html('compare & checkout(' + compareCount + ')');
    }

    function setCompareGrid()
    {
        jQuery(".CompareGridInnerData").html("");
        jQuery('.compareProd').html('compare & checkout(' + compareCount + ')');

        jQuery.each(jsonCompareData, function(index, key) {

            if (index % 2 == 0) {
                tempClassType = "even";
            } else {
                tempClassType = "odd";
            }

            var imgProd;
            if (jsonCompareData[index].imgStatus == 1) {
                imgProd = "camera_blue.png";
            } else {
                imgProd = "camera_gray.png";
            }

            var tempCheckBoxClass = "chkCompare" + index;
            var tempDivclass = "DivImg" + index;
            var bid_column = ''; 
            
			if(jsonCompareData[index].is_auction == 1) { 				
				
				bid_column = '<div class="gridcolumn21 makebid" cust_id="customer_bid' + jsonCompareData[index].entity_id + '">'+
						'<span>' + jsonCompareData[index].customer_bid_amount + '</span>'+
						'<button class="makebid_button makebid_button_' + jsonCompareData[index].entity_id + '" id="makebid_button_' + jsonCompareData[index].entity_id + '" type="button">Make Bid</button>'+
						'<div id="makebid_button_'+ jsonCompareData[index].entity_id +'_div" class="makebid_div makebid_button_'+ jsonCompareData[index].entity_id +'_div">'+
						'<form><input placeholder="Price" type="text" class="input-text" name="bid_price" id="bid_price_'+ jsonCompareData[index].entity_id +'" />'+
						'<br/> <button onclick="saveBid('+ jsonCompareData[index].entity_id + ',' + jsonCompareData[index].back_percentage +',' + new Date(jsonCompareData[index].auction_end_time).getTime() + ',home)" type="button">'+
						' Place Bid </button> <button onclick="closeBidDiv('+ jsonCompareData[index].entity_id + ')" type="button">'+
						'Close</button> </form> </div> </div>';
			} else {				
				bid_column = '<div class="gridcolumn21" cust_id="customer_bid' + jsonCompareData[index].entity_id + '"><span>' + jsonCompareData[index].customer_bid_amount + '</span> </div>';
			}						
            var tempGridJsonData = '<div class="gridrow entity' + jsonCompareData[index].entity_id + ' ' + tempClassType + '" class=' + tempDivclass + '>' +
                    '<div class="gridcolumn1" onClick="showFullPopDiv(' + jsonCompareData[index].entity_id + ', ' + jsonCompareData[index].imgStatus + ')" style="cursor:pointer;color:#29A1B5;">' + jsonCompareData[index].sku + '</div>' +
                    '<div class="gridcolumn2">' + jsonCompareData[index].shape + '</div>' +
                    '<div class="gridcolumn3">' + jsonCompareData[index].carat + '</div>' +
                    '<div class="gridcolumn4">' + jsonCompareData[index].color + '</div>' +
                    '<div class="gridcolumn5">' + jsonCompareData[index].clarity + '</div>' +
                    '<div class="gridcolumn6">' + jsonCompareData[index].cut + '</div>' +
                    '<div class="gridcolumn7">' + jsonCompareData[index].polish + '</div>' +
                    '<div class="gridcolumn8">' + jsonCompareData[index].symmetry + '</div>' +
                    '<div class="gridcolumn9">' + jsonCompareData[index].florescence + '</div>' +
                    '<div class="gridcolumn11">' + jsonCompareData[index].table + '</div>' +
                    '<div class="gridcolumn12">' + jsonCompareData[index].m1 +' * '+ jsonCompareData[index].m2 + ' * '+ jsonCompareData[index].m3 +'</div>' +                    
                    '<div class="gridcolumn20"><a target="_blank" href="' + jsonCompareData[index].certificate_link + '">' + jsonCompareData[index].lab + '</a></div>' +
                    '<div class="gridcolumn17">' + jsonCompareData[index].rapnet_price + '</div>' +
                    '<div class="gridcolumn18">' + jsonCompareData[index].carat_price + '</div>' +                    
                    '<div class="gridcolumn19">' + jsonCompareData[index].price + '</div>' +
                    '<div class="gridcolumn0"><a style="cursor:pointer"  onClick="showFullPopDiv(' + jsonCompareData[index].entity_id + ', ' + jsonCompareData[index].imgStatus + ', ' + index + ')"><img  src="/website_pansuriya/static/src/images/' + imgProd + '"></div></a>' +
                    '<div class="gridcolumn16 makebid'+jsonCompareData[index].entity_id+'" id="makebid' + jsonCompareData[index].entity_id + '">' + jsonCompareData[index].back_percentage + '</div>' +                    
                    bid_column +                    
                    '<div class="gridcolumn22 auction_timer_'+jsonCompareData[index].entity_id+'" id="auction_timer_'+jsonCompareData[index].entity_id+'">'+ jsonCompareData[index].auction_time +'</div>' +                                        
                    '<div class="gridcolumn15"><a href="javascript:void(0);" onClick="removeCompareRow(' + jsonCompareData[index].entity_id + ',/main/)"><img src="/website_pansuriya/static/src/images/removeCompare.gif" /></a></div>' +
                    '</div>' +
                    '<div class="responsive_data" id="responsive_' + jsonCompareData[index].entity_id + '"><div class="responsive_data_col_1" id="responsive_' + jsonCompareData[index].entity_id + '_1"></div><div class="responsive_data_col_2" id="responsive_' + jsonCompareData[index].entity_id + '_2"></div></div>';                    
					jQuery(".CompareGridInnerData").append(tempGridJsonData);					
                    if(jsonCompareData[index].is_auction == 1) {
						jsonCompareData[index].auction_end_time = getAuctionEndTime(jsonCompareData[index].current_time,jsonCompareData[index].auction_end_time);						
						jQuery('.auction_timer_' + jsonCompareData[index].entity_id).countdown({
							date: new Date(jsonCompareData[index].auction_end_time),
							render: function(data) {
							data.hours = data.hours + data.days * 24;
							jQuery(this.el).html( data.hours + " : " + this.leadingZeros(data.min, 2) + " : " + this.leadingZeros(data.sec, 2));
						  },
						  onEnd: function(){
								jQuery('.makebid_button_'+jsonCompareData[index].entity_id).remove();
								jQuery('.auction_timer_' + jsonCompareData[index].entity_id).html('-');
							}
						});
					}
					else if(jsonCompareData[index].is_auction == 0)
					{						
						jQuery('.auction_timer_'+jsonCompareData[index].entity_id).html('-');
					}
        });
        //grid row hover code
		jQuery('.gridrow').hover(function() {			
			jQuery(this).children('.makebid').children('.makebid_button').show(200);
		});
		jQuery('.gridrow').mouseleave(function() {
			jQuery(this).children('.makebid').children('.makebid_button').hide(500);			
		});
		
		jQuery('.makebid_button').click(function(){
			jQuery('.makebid_div').hide(100);
			var makebidbuttonid = jQuery(this).attr('id');			
			jQuery("." + makebidbuttonid + "_div").show(200);		
		}); 
        if (jsonCompareData.length >= 1)
        {
            jQuery('#divBulkAddToCart').css('display', 'block');
        }
        else
        {
            jQuery('#divBulkAddToCart').css('display', 'none');
        }
        computeCompareData();              

    }

    function loadCompareGridData(entity_id, operation)
    {
        jQuery.each(jsonGridData, function(index, key) {
            if (jsonGridData[index].entity_id == entity_id)
            {
                if (operation == "add") {
                    jsonCompareData.push(jsonGridData[index]);
                    compareCount++;
                }
                return;
            }
        });
        setCompareGrid();
    }

    function removeCompareRow(entity_id, objChk)
    {
        var tempMain = new String(objChk).replace(/\//gi, '');

        if (tempMain != "main") {
            jQuery(objChk).html('<img class="imgChk" alt="check" src="/website_pansuriya/static/src/images/uncheck_box.png" />');
        } else {
            jQuery('.imgChk' + entity_id).html('<img class="imgChk" alt="check" src="/website_pansuriya/static/src/images/uncheck_box.png" />');
        }
        var loopflag = false;
        var indextobedelete = 0;
        //jQuery('.CompareGridInnerData > .entity'+entity_id).css('display','none');

        jQuery.each(jsonCompareData, function(index, key) {
            if (jsonCompareData[index].entity_id == entity_id && loopflag == false)
            {
                jsonCompareData.splice(index, 1);

                loopflag = true;
                compareCount--;
                setCompareGrid();
                jQuery('.compareProd').html('compare & checkout(' + jsonCompareData.length + ')');

                return;
            }
        });
        //setCompareGrid();
    }

    function bulkAddToCart()
    {
        var products = [];
        jQuery('#addedoverlay').show();
        showMessageCustom("Please wait...");
               
        setTimeout(function() {
            jQuery.each(jsonCompareData, function(index, key) {
				jQuery.ajax({
                    url: "/shop/cart/update",
                    type: 'POST', 
					async: false,
                    data: {product_id:jsonCompareData[index].entity_id},
                    success: function(data) {
                    }
                });
                //products.push(jsonCompareData[index].entity_id);
            });
            //alert(products);
            /*for(var i=0;i<products.length;i++)
        	{          
            	var p_id= products[i];
            	jQuery.ajax({
                    url: "/shop/cart/update",
                    type: 'POST', 
					async: false,
                    data: {product_id:p_id},
                    success: function(data) {
                    }
                });
        	}*/
            jQuery('#addedoverlay').hide();
            showMessageCustom("Diamonds added into cart successfully!!!");
            window.location.reload();
        }, 500);        
    }

	function getAuctionEndTime(current_time,auction_end_time)
	{		
		var server_time = new Date(current_time);
		var system_time = new Date();
		var diff = minutesDiff(server_time,system_time);		
		var auction_end_date = new Date(auction_end_time);		
		return auction_end_date.setMinutes(auction_end_date.getMinutes()+diff);
	}	

    function loadGridData(data)
    {
        var bg_color = '';
        var color = '';
        jQuery(".DivGridInnerData, #prettyPhotoLinks").html("");
        var objGridData = data;
		var active_tab_name = "homegrid";
        jQuery.each(objGridData, function(index, key) {
            if (objGridData[index].booked == 1)
            {
                bg_color = 'background-color:#D0282D;';
                color = 'color:white;';
            }
            else
            {
                bg_color = '';
                color = '';
            }
            if (index % 2 == 0) {
                tempClassType = "even";
            } else {
                tempClassType = "odd";
            }
            var imgProd;
            if (objGridData[index].imgStatus == 1) {
                imgProd = "camera_blue.png";
            } else {
                imgProd = "camera_gray.png";
            }

            /*
             * 	var tempGridJsonData = '<div class="gridrow '+tempClassType+'" onmouseover="showPopDiv(this,1,'+objGridData[index].entity_id+')" onmouseout="showPopDiv(this,0)" class='+tempDivclass+'>'+
             */
            var tempCheckBoxClass = "chkCompare" + index;
            var tempDivclass = "DivImg" + index;
			var tooltip_html = '';
			var bid_column = ''; 
			
			if(objGridData[index].is_auction == 1) {
				bid_column = '<div class="gridcolumn21 makebid" cust_id="customer_bid' + objGridData[index].entity_id + '">'+
						'<span>' + objGridData[index].customer_bid_amount + '</span>'+
						'<button class="makebid_button makebid_button_'+objGridData[index].entity_id+'" id="makebid_button_' + objGridData[index].entity_id + '" product_index="'+index+'">Make Bid</button>'+
						'<div id="makebid_button_'+ objGridData[index].entity_id +'_div" class="makebid_div">'+
						'<form><input placeholder="Price" type="text" class="input-text" name="bid_price" id="bid_price_'+ objGridData[index].entity_id +'" />'+
						'<br/> <button onclick="saveBid('+ objGridData[index].entity_id + ',' + objGridData[index].back_percentage +',' + new Date(objGridData[index].auction_end_time).getTime() + ',0)" type="button">'+
						' Place Bid </button> <button onclick="closeBidDiv('+ objGridData[index].entity_id + ')" type="button">'+
						'Close</button> </form> </div> </div>';
			} else {
				tooltip_html = '';
				bid_column = '<div class="gridcolumn21" cust_id="customer_bid' + objGridData[index].entity_id + '"><span>' + objGridData[index].customer_bid_amount + '</span> </div>';
			}
			
            var tempGridJsonData = '<div id="gridrow_'+ objGridData[index].entity_id +'" class="gridrow_'+ objGridData[index].entity_id +' gridrow ' + tempClassType +' '+tempDivclass +'" style=' + bg_color + color + '>' +                   
                    '<div class="gridcolumn1" onClick="showFullPopDiv(' + objGridData[index].entity_id + ', ' + objGridData[index].imgStatus + ')" style="cursor:pointer;color:#29A1B5;">' + objGridData[index].sku + '</div>' +
                    '<div class="gridcolumn2">' + objGridData[index].shape + '</div>' +
                    '<div class="gridcolumn3">' + objGridData[index].carat + '</div>' +
                    '<div class="gridcolumn4">' + objGridData[index].color + '</div>' +
                    '<div class="gridcolumn5">' + objGridData[index].clarity + '</div>' +
                    '<div class="gridcolumn6">' + objGridData[index].cut + '</div>' +
                    '<div class="gridcolumn7">' + objGridData[index].polish + '</div>' +
                    '<div class="gridcolumn8">' + objGridData[index].symmetry + '</div>' +
                    '<div class="gridcolumn9">' + objGridData[index].florescence + '</div>' +
                    '<div class="gridcolumn11">' + objGridData[index].table + '</div>' +
                    '<div class="gridcolumn12">' + objGridData[index].m1 +' * '+ objGridData[index].m2 + ' * '+ objGridData[index].m3 +'</div>' +                    
                    '<div class="gridcolumn20"><a target="_blank" href="' + objGridData[index].certificate_link + '">' + objGridData[index].lab + '</a></div>' +
                    '<div class="gridcolumn17">' + objGridData[index].rapnet_price + '</div>' +
                    '<div class="gridcolumn18">' + objGridData[index].carat_price + '</div>' +                    
                    '<div class="gridcolumn19">' + objGridData[index].price + '</div>' +
                    '<div class="gridcolumn0"><a style="cursor:pointer"  onClick="showFullPopDiv(' + objGridData[index].entity_id + ', ' + objGridData[index].imgStatus + ', ' + index + ')"><img  src="/website_pansuriya/static/src/images/' + imgProd + '"></div></a>' +
                    '<div class="gridcolumn16 makebid'+objGridData[index].entity_id+'" id="makebid' + objGridData[index].entity_id + '">' + objGridData[index].back_percentage + '</div>' +                    
                    bid_column +                    
                    '<div class="gridcolumn22 auction_timer_'+objGridData[index].entity_id+'" id="auction_timer_'+objGridData[index].entity_id+'">'+ objGridData[index].auction_time +'</div>' +
                    '<div class="gridcolumn15"><a href="javascript:void(0);" class="imgChk' + objGridData[index].entity_id + '" onClick="chkClickEvent(this,' + objGridData[index].entity_id + ')"><img class="imgChk" alt="check" src="/website_pansuriya/static/src/images/uncheck_box.png" /></a></div>' +                    
                    '</div>' +
                    '<div class="responsive_data" id="responsive_' + objGridData[index].entity_id + '"><div class="responsive_data_col_1" id="responsive_' + objGridData[index].entity_id + '_1"></div><div class="responsive_data_col_2" id="responsive_' + objGridData[index].entity_id + '_2"></div></div>';
                                
            jQuery(".DivGridInnerData").append(tempGridJsonData); 			
            if(objGridData[index].is_auction == 1) {            	
				//desable compare functionality
				jQuery('.gridrow_'+ objGridData[index].entity_id).find('.gridcolumn15 > a').attr('onclick','javascript:void(0)');				
				
				objGridData[index].auction_end_time = getAuctionEndTime(objGridData[index].current_time,objGridData[index].auction_end_time);															
//				jQuery('.auction_timer_' + objGridData[index].entity_id).countdown({
//					  date: new Date('Jul 19,2014 21:00:00'),
//					  render: function(data) {
//						 data.hours = data.hours + data.days * 24;
//						jQuery(this.el).html( data.hours + " : " + this.leadingZeros(data.min, 2) + " : " + this.leadingZeros(data.sec, 2));
//					  },
//					  onEnd: function(){
//							jQuery('.makebid_button_'+ objGridData[index].entity_id).remove();
//							jQuery('.auction_timer_' + objGridData[index].entity_id).html('-');						
//						}
//					});
				jQuery('.auction_timer_' + objGridData[index].entity_id).countdown({
				  date: new Date(objGridData[index].auction_end_time),
				  render: function(data) {
					 data.hours = data.hours + data.days * 24;
					jQuery(this.el).html( data.hours + " : " + this.leadingZeros(data.min, 2) + " : " + this.leadingZeros(data.sec, 2));
				  },
				  onEnd: function(){
						jQuery('.makebid_button_'+ objGridData[index].entity_id).remove();
						jQuery('.auction_timer_' + objGridData[index].entity_id).html('-');						
					}
				});
			}
            else
            {
				jQuery('.auction_timer_' + objGridData[index].entity_id).html('-');
			}
			
            if (objGridData[index].booked == 1)
            {
                rowDisabled('#gridrow_'+ objGridData[index].entity_id);
            }
            if (objGridData[index].imgStatus == 1)
            {
                //var url = '<?php echo $this->getUrl("ajaxmodule/ajax/ajaxpopup") ?>id/' + objGridData[index].entity_id + '?iframe=true&width=855&height=530';
            	//var url = '/website-test/ajaxpopup' + '?id='+objGridData[index].entity_id+'&iframe=true&width=855&height=530';
            	var url = domainname+'ajaxpopup?id='+objGridData[index].entity_id+'&iframe=true&width=855&height=530';
            }
            else
            {
                //var url = '<?php echo $this->getUrl("ajaxmodule/ajax/ajaxpopup") ?>id/' + objGridData[index].entity_id + '?iframe=true&width=855&height=500';
            	//var url = '/website-test/ajaxpopup' + '?id='+objGridData[index].entity_id+'&iframe=true&width=855&height=500';
            	var url = domainname+'ajaxpopup?id='+objGridData[index].entity_id+'&iframe=true&width=855&height=500';
            }
            jQuery("#prettyPhotoLinks").append('<a class="aPrettyPhoto" id="prettyPhoto_' + objGridData[index].entity_id + '" href="' + url + '" rel="prettyPhoto[iframe]">abc</a>');
        });
        dataLength = jsonGridData.length;
        jQuery('.aPrettyPhoto').prettyPhoto({
            overlay_gallery: false,
            social_tools: '',
            animation_speed: 'fast',
            slideshow: 10000,
            deeplinking: false,
            hideflash: true
        });
        
        /*jQuery('.bidModel').prettyPhoto({
            overlay_gallery: false,
            social_tools: '',
            animation_speed: 'fast',
            slideshow: 10000,
            deeplinking: false,
            hideflash: true
        });*/
        
		//grid row hover code
		jQuery('.gridrow').hover(function() {			
			jQuery(this).children('.makebid').children('.makebid_button').show(200);
		});
		jQuery('.gridrow').mouseleave(function() {
			jQuery(this).children('.makebid').children('.makebid_button').hide(500);			
		});
		
		jQuery('.makebid_button').click(function(){
			//jQuery('.makebid_div').hide(100);			
			var p_index = jQuery(this).attr('product_index');
			setModelBoxData(p_index,objGridData);								
		//jQuery('.bidModel').click();
			/*var makebidbuttonid = jQuery(this).attr('id');			
			jQuery("#" + makebidbuttonid + "_div").show(200);*/	
			//jQuery(this).next('.makebid_div').show(200);
		});  
    }	
	function hideOverlay()
	{
		jQuery('#overlay').hide();
	}
	function reOpenModel(entity_id)
	{
		jQuery('.makebid_button_'+entity_id).click();
	}	
	function setModelBoxData(p_index,objGridData)
	{		
		var minbidamount = parseFloat(jsonGridData[p_index].back_percentage) + parseFloat(0.11);
		var h = '<i class="icon-remove fr closemodel" onclick="hideOverlay()"></i>'+
		'<div class="bidModelContent">'+
			'<div class="modelrow txt-center" style="padding-bottom:10px;"><span class="reflabel">Ref: </span><span class="ref">'+jsonGridData[p_index].sku+'</span></div>'+			
			'<div class="modelrow txt-center">'+
				'<span class="model_label">Time left : </span><span class="modeltimer modelauctiontimer_'+jsonGridData[p_index].entity_id+'"></span>'+
				'<span class="gmt_timer" id="gmt_timer"></span>'+
			'</div>'+
			'<div class="model_bid_data">'+
				'<div class="modelrow" style="padding:0 0px 40px 25px;">'+
					'<div class="model_change_data">'+
						'<span class="model_label" style="text-transform:none;color:#424242;font-weight:bold;">Current Bid : </span><span class="modelprice">$'+objGridData[p_index].price+'</span><span class="model_current_bid modelcurrentbid_'+jsonGridData[p_index].entity_id+'">'+jsonGridData[p_index].back_percentage+'</span>'+
						'<span class="modelbidamountmainspan">'+
							'<input type="text" id="modelbidamount" class="modelbidamount" placeholder="Bid amount"/>'+
							'<span class="minbid minbid_'+jsonGridData[p_index].entity_id+'">Enter '+minbidamount.toFixed(2)+' or Less</span>'+
						'</span>'+
						'<div class="product_bid_count product_bid_count_'+jsonGridData[p_index].entity_id+'">'+jsonGridData[p_index].product_bid_count+' Bids</div>'+
					'</div>'+
					'<div class="placebidbuttonmaindiv">'+
						'<button class="placebidbutton" onclick="confirmDialog('+p_index+')">Place Bid</button>'+
					'</div>'+
					'<div class="modelbacklink">'+
						'<a href="javascript:void(0)" class="confirmreturn" onclick="returnBidData();">Back</a>'+
					'</div>'+
				'</div>'+
				'<span class="bidamount_error"></span>'+
				'<span class="confirminfo">By clicking Confirm, you commit to buy this stone, if you are wining bidder.</span>'+
			'</div>';
		
		jQuery('.bidModelDiv').attr('product_id',jsonGridData[p_index].entity_id)
		jQuery('.bidModelDiv').html(h);
		jQuery('.gmt_timer').jClocksGMT({offset: '0',digital: true, analog:false});		
		jQuery('.modelauctiontimer_'+jsonGridData[p_index].entity_id).countdown({
				  date: new Date(objGridData[p_index].auction_end_time),
				  render: function(data) {
					 data.hours = data.hours + data.days * 24;
					jQuery(this.el).html( data.hours + " : " + this.leadingZeros(data.min, 2) + " : " + this.leadingZeros(data.sec, 2));
				  },
				  onEnd: function(){
						jQuery('#overlay').hide('fast');					
					}
		});
		jQuery('#overlay').fadeIn('fast');			
		jQuery('#bidModelDiv').css('position','absolute');
		jQuery('#bidModelDiv').css("left", jQuery(window).width()/2-jQuery('#bidModelDiv').width()/2);
		jQuery('#bidModelDiv').css("top", jQuery(window).height()/2-jQuery('#bidModelDiv').height()/2);				
		jQuery('.bidModelDiv').attr('product_id',jsonGridData[p_index].entity_id);		
		//jQuery('.product_bid_count').html(jsonGridData[p_index].product_bid_count);		
		jQuery('.modelprice').addClass('modelprice_'+jsonGridData[p_index].entity_id);
		jQuery('.minbid').addClass('minbid_'+jsonGridData[p_index].entity_id);
		jQuery('.product_bid_count').addClass('product_bid_count_'+jsonGridData[p_index].entity_id);
		jQuery('.modelprice_'+jsonGridData[p_index].entity_id).html('$'+objGridData[p_index].price);
		jQuery('.raise_modelprice').html('($'+objGridData[p_index].price+')');
		jQuery('.modelcurrentbidmainspan').addClass('modelcurrentbid_'+jsonGridData[p_index].entity_id);
		jQuery('.modelcurrentbid_'+jsonGridData[p_index].entity_id).html(jsonGridData[p_index].back_percentage);				
		jQuery('.raisebidbutton').attr('onclick',
		'saveBid('+ jsonGridData[p_index].entity_id + ',' + jsonGridData[p_index].back_percentage +',' + new Date(jsonGridData[p_index].auction_end_time).getTime() + ',3)');
	}
	
	function confirmDialog(p_index)
	{
		var _value = jQuery(".modelbidamount").val();
		var min_bid = parseFloat(jsonGridData[p_index].back_percentage) + parseFloat(0.11);		
		if(hasWhiteSpace(_value) || _value=="")
		{
			jQuery(".modelbidamount").css('border','1px solid red');
			jQuery(".bidamount_error").html('Please enter bid amount');			
		}		
		else if(parseFloat(_value) < min_bid || parseFloat(_value) > 0)
		{
			jQuery(".modelbidamount").css('border','1px solid red');
			jQuery(".bidamount_error").html('Bid amount must be less then 0 and greater then '+min_bid);
		}
		else
		{				
			jQuery('.bidamount_error').html('');			
			jQuery('.hidden_modelbidamount').html(jQuery(".modelbidamount").val());
			jQuery('.hidden_bid_data').html(jQuery('.model_change_data').html());
			jQuery('.model_change_data').fadeOut('fast');
			jQuery('.hidden_placebid_button').html(jQuery('.placebidbuttonmaindiv > .placebidbutton').attr('onclick'));
			jQuery('.placebidbuttonmaindiv > .placebidbutton').html('Confirm');
			jQuery('.placebidbuttonmaindiv > .placebidbutton').attr('onclick',
			'saveBid('+ jsonGridData[p_index].entity_id + ',' + jsonGridData[p_index].back_percentage +',' + new Date(jsonGridData[p_index].auction_end_time).getTime() + ',2)');
			var confirm_html = '<h3 style="display:inline-block;">'+
			'Your bid <span class="confirm_bid_amount">'+jQuery(".modelbidamount").val()+'</span>'+
			'</h3>'+
			'<span class="confirmprice">($ '+jsonGridData[p_index].price+')</span>'+
			'<div style="text-align:center;display:block;" class="product_bid_count product_bid_count_'+jsonGridData[p_index].entity_id+'">'+jsonGridData[p_index].product_bid_count+' bids</div>'		
			;			
			jQuery('.model_change_data').addClass('change_data_class');		
			jQuery('.model_change_data').html(confirm_html);		
			jQuery('.model_change_data,.modelbacklink,.confirminfo').fadeIn('fast');			
		}		
	}
	
	function returnBidData()
	{
		if(jQuery.trim(jQuery('.hidden_bid_data').html()).length!=0)
		{	
			jQuery('.placebidbutton').html('Place Bid');
			jQuery('.placebidbutton').attr('onclick',jQuery('.hidden_placebid_button').html());
			jQuery('.modelbacklink,.confirminfo').hide();
			jQuery('.model_change_data').removeClass('change_data_class');		
			jQuery(".modelbidamount").css('border','');
			jQuery('.model_change_data').html(jQuery('.hidden_bid_data').html());
		}		
	}
	
	function UpdateTimerOrNot(data)
	{			
		var arr = data.split(':');
		if(arr[0] <= 0 && arr[1] < 5)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	
	function saveBid(eid,curBid,bid_end_time,type)
	{		
		curBid = parseFloat(curBid);		
		
		var bidamount="";
		if(type == 0)
		{
			bidamount = jQuery("#bid_price_"+eid).val();
		}
		else if(type == 1)
		{
			bidamount = jQuery('.mybid_price_'+eid).val();
		}
		else if(type == 2)
		{			
			bidamount = jQuery('.hidden_modelbidamount').html();
		}
		else if(type == 3)
		{
			bidamount = jQuery('.raisebidamount').val();
			var _value = jQuery(".raisebidamount").val();
			var min_bid = curBid + parseFloat(0.11);		
			if(hasWhiteSpace(_value) || _value=="")
			{
				jQuery(".raisebidamount").css('border','1px solid red');
				jQuery(".bidamount_error").html('Please enter bid amount');
				return false;			
			}		
			else if(parseFloat(_value) < min_bid || parseFloat(_value) > 0)
			{
				jQuery(".raisebidamount").css('border','1px solid red');
				jQuery(".bidamount_error").html('Bid amount must be less then 0 and greater then '+min_bid);
				return false;
			}
		}
			
		
		//var productids = jsonGridData.map(function(product, index) { return product.entity_id; });
					
			bidamount = parseFloat(bidamount);
			if(type==3)//if(bidamount > curBid && bidamount < 0)
			{
				if(confirm('Are your sure to make this bid?'))
				{
					var timerString = jQuery('#auction_timer_' + eid).html();
					var is_extend_time = UpdateTimerOrNot(timerString);
					args_data = {product_id: eid, bid_amount: bidamount};
					openerp.jsonRpc("/savebid", 'call', {'data': args_data}  )
					.then(function (data) {			             
							if(data!='Error')
							{							
								jQuery('div[cust_id="customer_bid'+eid+'"] > span').html(bidamount);
							} else {								
								//alert('Bid amount invalid');
								reOpenModel(eid);				
								jQuery('.bidamount_error').html('Invalid Bid Please re-enter Bid').show();				
								return;								
							}						
							closeBidDiv(eid);
							customer_bid = bidamount;
							if(type==2)
							{
								jQuery('.bidModelContent').html(jQuery('.raisebidmodel').html());													
							}
							if(type==3)
							{
								jQuery('#overlay').hide()
							}		          	 
			            });
					
					/*jQuery.ajax({
						url: '<?php echo $this->getUrl("ajaxmodule/ajax/saveBid") ?>',
						type: 'POST',
						data: {product_id: eid, bid_amount: bidamount,is_extend_time: is_extend_time},
						async: false,
						success: function(data) {						
							if(data!='Error')
							{							
								jQuery('div[cust_id="customer_bid'+eid+'"] > span').html(bidamount);
							} else {								
								//alert('Bid amount invalid');
								reOpenModel(eid);				
								jQuery('.bidamount_error').html('Invalid Bid Please re-enter Bid').show();				
								return;								
							}						
							closeBidDiv(eid);
							customer_bid = bidamount;
							if(type==2)
							{
								jQuery('.bidModelContent').html(jQuery('.raisebidmodel').html());													
							}
							if(type==3)
							{
								jQuery('#overlay').hide()
							}
							},
						error: function(a1,a2,a3)
						{
							alert('error');
						}
						
					});*/
				}
			}
			else
			{
				var timerString = jQuery('#auction_timer_' + eid).html();
				var is_extend_time = UpdateTimerOrNot(timerString);
				
				args_data = {product_id: eid, bid_amount: bidamount};
				openerp.jsonRpc("/savebid", 'call', {'data': args_data}  )
				.then(function (data) {			             
						closeBidDiv(eid);
						customer_bid = bidamount;
						if(data!='Error')
						{													
							jQuery('div[cust_id="customer_bid'+eid+'"] > span').html(bidamount);
						} else {							
							//alert('Bid amount invalid');
							reOpenModel(eid);							
							jQuery('.bidamount_error').html('Invalid Bid Please re-enter Bid').show();
							return;							
						}														
						if(type==2)
						{
							jQuery('.bidModelContent').html(jQuery('.raisebidmodel').html());													
						}
						if(type==3)
						{
							jQuery('#overlay').hide()
						}
		            });
				
				/*jQuery.ajax({
					url: '<?php echo $this->getUrl("ajaxmodule/ajax/saveBid") ?>',
					type: 'POST',
					data: {product_id: eid, bid_amount: bidamount,is_extend_time: is_extend_time},
					async: false,
					success: function(data) {							
						closeBidDiv(eid);
						customer_bid = bidamount;
						if(data!='Error')
						{													
							jQuery('div[cust_id="customer_bid'+eid+'"] > span').html(bidamount);
						} else {							
							//alert('Bid amount invalid');
							reOpenModel(eid);							
							jQuery('.bidamount_error').html('Invalid Bid Please re-enter Bid').show();
							return;							
						}														
						if(type==2)
						{
							jQuery('.bidModelContent').html(jQuery('.raisebidmodel').html());													
						}
						if(type==3)
						{
							jQuery('#overlay').hide()
						}
					}
				});*/
				//alert('Bid amount must be less then 0 and greater then current bid');
			}
		
	}
	
	function reInitTimer(entity_id,extend_time,current_time)
	{	
		var extend_time_local_var = getAuctionEndTime(current_time,extend_time);		
		jQuery('.auction_timer_' + entity_id).data('countdown').update(+(new Date(extend_time_local_var))).start();
		if(jQuery('.bidModelDiv').attr('product_id') == product_id) {
			jQuery('.modelauctiontimer_' + entity_id).data('countdown').update(+(new Date(extend_time_local_var))).start();
		}
	}
	
	function hasWhiteSpace(s) {
		return s.indexOf(' ') >= 0;
	}
	
	function closeBidDiv(eid)
	{
		jQuery('.makebid_div').hide(100);		
	}
	

    function rowDisabled(rowId)
    {		
		jQuery(rowId).find('.gridcolumn21 > .makebid_button').remove();
        jQuery(rowId).find('.gridcolumn1').attr('onclick','javascript:void(0)');
        jQuery(rowId).find('.gridcolumn20 > a').attr('href','javascript:void(0)');               
        jQuery(rowId).find('.gridcolumn20 > a').attr('target','');
        jQuery(rowId).find('.gridcolumn0 > a').attr('onclick','javascript:void(0)');
        jQuery(rowId).find('.gridcolumn15 > a').attr('onclick','javascript:void(0)');
    }
    function showPopDiv(ImgDivClass, optValue, entity_id)
    {
        var innerPopover;
        var tempDisplayPop = "." + ImgDivClass.className;
        if (optValue == 1)
        {
            var tempData = jsonGridData;

            jQuery.each(tempData, function(index, key)
            {
                if (tempData[index].entity_id == entity_id)
                {
                    innerPopover =
                            '<div class="arrow"></div>' +
                            '<div style="background-color: #29A1B5;padding-left: 5px;font-size: 15px;color: white;">Report : ' + tempData[index].report_no + '</div>' +
                            '<div style="width: 200px;float: left;padding-left: 10px;">' +
                            '<div class="popDivRow"><div class="popTitle">Lab:</div><div class="popContent">' + tempData[index].lab + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Laser Inscription:</div><div class="popContent">' + tempData[index].laser_inscription + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Girdle Thin:</div><div class="popContent">' + tempData[index].girdle_thin + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Girdle Thick:</div><div class="popContent">' + tempData[index].girdle_thick + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Girdle %:</div><div class="popContent">' + tempData[index].girdle_percentage + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Girdle Cond.:</div><div class="popContent">' + tempData[index].girdle_condition + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Culet Size:</div><div class="popContent">' + tempData[index].culet_size + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Culet Condition:</div><div class="popContent">' + tempData[index].culet_condition + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Crown Height:</div><div class="popContent">' + tempData[index].crown_height + '</div></div></div>' +
                            '<div style="width: 200px;float: left;padding-left: 10px;">' +
                            '<div class="popDivRow"><div class="popTitle">Crown Angle:</div><div class="popContent">' + tempData[index].crown_angle + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Pavilion Depth:</div><div class="popContent">' + tempData[index].pavilion_depth + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Pavilion Angle:</div><div class="popContent">' + tempData[index].pavilion_angle + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Fancy Color:</div><div class="popContent">' + tempData[index].fancy_color + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Fancy Color Overtone:</div><div class="popContent">' + tempData[index].fancy_color_overtone + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Fancy Color Intensity:</div><div class="popContent">' + tempData[index].fancy_color_intensity + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Milky:</div><div class="popContent">' + tempData[index].milky + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Shade:</div><div class="popContent">' + tempData[index].shade + '</div></div>' +
                            '<div class="popDivRow"><div class="popTitle">Tinge:</div><div class="popContent">' + tempData[index].tinge + '<div></div></div>';
                }
            });

            var tempTop = jQuery(ImgDivClass).offset();
            jQuery(".custompopover").html(innerPopover);
            jQuery(".custompopover").css("top", tempTop.top - 449).css("left", tempTop.left + 90);
            jQuery(".popTitle").css("width", "auto").css("", "bold");
            jQuery(".custompopover").toggle();
        }
        else
        {
            jQuery('.custompopover').css("display", "none");
        }
    }

    function addToWishList(entity_id)
    {
        jQuery.ajax({
            url: '',
            type: 'POST',
            async: false,
            success: function(data) {
                window.location.href = '<?php echo $this->getUrl() ?>';
            }
        });
    }


    function showFullPopDiv(entity_id, imgStatus)
    {
    	//alert(entity_id+' - '+imgStatus);
    	
        if (window.innerWidth > 480)
        {
            jQuery('#prettyPhoto_' + entity_id).click();
            return;
        }
    	
        var PopData;
        
        openerp.jsonRpc("/website-pansuriya/popup", 'call', {
            'data': {entity_id: entity_id} 
            })
            .then(function (data) {
            	//alert(JSON.stringify(data));
            });
        
        /*jQuery.ajax({
            url: '',
            type: 'POST',
            async: false,
            data: {entity_id: entity_id},
            success: function(data) {


                PopData = JSON.parse(data);

                var sku = PopData[0].sku;

                var shape = PopData[0].shape == null ? "-" : PopData[0].shape;
                var carat = PopData[0].carat == null ? "-" : PopData[0].carat;
                var color = PopData[0].color == null ? "-" : PopData[0].color;
                var clarity = PopData[0].clarity == null ? "-" : PopData[0].clarity;
                var cut = PopData[0].cut == null ? "-" : PopData[0].cut;
                var polish = PopData[0].polish == null ? "-" : PopData[0].polish;
                var symmetry = PopData[0].symmetry == null ? "-" : PopData[0].symmetry;
                var florescence = PopData[0].florescence == null ? "-" : PopData[0].florescence;

                var table = PopData[0].table == null ? "-" : PopData[0].table;
                var m1 = PopData[0].m1 == null ? "-" : PopData[0].m1;
                var m2 = PopData[0].m2 == null ? "-" : PopData[0].m2;
                var m3 = PopData[0].m3 == null ? "-" : PopData[0].m3;
                var crown_height = PopData[0].crown_height == null ? "-" : PopData[0].crown_height;
                var crown_angle = PopData[0].crown_angle == null ? "-" : PopData[0].crown_angle;
                var culet_condition = PopData[0].culet_condition == null ? "-" : PopData[0].culet_condition;
                var culet_size = PopData[0].culet_size == null ? "-" : PopData[0].culet_size;
                var fancy_color = PopData[0].fancy_color == null ? "-" : PopData[0].fancy_color;
                var fancy_color_intensity = PopData[0].fancy_color_intensity == null ? "-" : PopData[0].fancy_color_intensity;
                var fancy_color_overtone = PopData[0].fancy_color_overtone == null ? "-" : PopData[0].fancy_color_overtone;
                var girdle = PopData[0].girdle == null ? "-" : PopData[0].girdle;
                var girdle_condition = PopData[0].girdle_condition == null ? "-" : PopData[0].girdle_condition;
                var girdle_percentage = PopData[0].girdle_percentage == null ? "-" : PopData[0].girdle_percentage;
                var girdle_thick = PopData[0].girdle_thick == null ? "-" : PopData[0].girdle_thick;
                var girdle_thin = PopData[0].girdle_thin == null ? "-" : PopData[0].girdle_thin;
                var hna = PopData[0].hna == null ? "-" : PopData[0].hna;

                var lower_half = PopData[0].lower_half == null ? "-" : PopData[0].lower_half;
                var measurements = PopData[0].measurements == null ? "-" : PopData[0].measurements;
                var pavilion_angle = PopData[0].pavilion_angle == null ? "-" : PopData[0].pavilion_angle;
                var pavilion_depth = PopData[0].pavilion_depth == null ? "-" : PopData[0].pavilion_depth;
                var report_no = PopData[0].report_no == null ? "-" : PopData[0].report_no;
                var shade = PopData[0].shade == null ? "-" : PopData[0].shade;
                var star_length = PopData[0].star_length == null ? "-" : PopData[0].star_length;
                var tinge = PopData[0].tinge == null ? "-" : PopData[0].tinge;
                var natts = PopData[0].natts == null ? "-" : PopData[0].natts;
                var laser_inscription = PopData[0].laser_inscription == null ? "-" : PopData[0].laser_inscription;
                var browness = PopData[0].browness == null ? "-" : PopData[0].browness;
                var milky = PopData[0].milky == null ? "-" : PopData[0].milky;
                var short_description = PopData[0].short_description == null ? "-" : PopData[0].short_description;
                var rapnet_price = PopData[0].rapnet_price == null ? "-" : PopData[0].rapnet_price;
                var eye_clean = PopData[0].eye_clean == null ? "-" : PopData[0].eye_clean;
                var imgProd = PopData[0].imgProd == null ? "-" : PopData[0].imgProd;
                var back_percentage = PopData[0].back_percentage == null ? "-" : PopData[0].back_percentage;
                var lab = PopData[0].lab == null ? "-" : PopData[0].lab;
                var report_link = PopData[0].report_link == null ? "-" : PopData[0].report_link;
                var certificate_link = PopData[0].certificate_link == null ? "-" : PopData[0].certificate_link;
                var manufacturer = PopData[0].manufacturer == null ? "-" : PopData[0].manufacturer;

                //jQuery('#product_addtocart_id').val(entity_id);
                if (jQuery('#btnAddToCart').attr('status') == 'login')
                {
                    jQuery('#btnAddToCart').attr('data-id', entity_id);
                    jQuery('#btnAddToCart').attr('href', '');
                    jQuery('#btnAddToWishList').attr('href', '');
                    jQuery('#btnAddToWatchList').attr('data-id', entity_id);
                }

                if (PopData[0].price != null)
                {
                    jQuery('#popRapnetPrice').html('<strong>Rapnet Price: </strong>$' + PopData[0].rapnet_price);
                    jQuery('#popRapnetPrice').css('text-align', 'left').css('margin-top', '10px').css('float', 'left').css('padding-right', '40px');

                    jQuery('#popBackPercentage').html('<strong>Back (%): </strong>' + PopData[0].back_percentage);
                    jQuery('#popBackPercentage').css('text-align', 'left').css('margin-top', '10px');

                    jQuery('#popCaratPrice').html('<strong>Price Per Carat: </strong>$' + PopData[0].carat_price);
                    jQuery('#popCaratPrice').css('text-align', 'left').css('margin-top', '10px').css('float', 'left').css('padding-right', '24px');

                    jQuery('#popPrice').html('<strong>Total Price: </strong>$' + PopData[0].price);
                    jQuery('#popPrice').css('text-align', 'left').css('margin-top', '10px');

                    jQuery('#popManufacturer').html('<strong>Seller: </strong><a href="javascript:void(0)">' + manufacturer + '</a>');
                    jQuery('#popManufacturer').css('text-align', 'left').css('margin-top', '10px');
                }

                jQuery('#report_link').html('<strong>Report No: </strong>' + report_no);
                jQuery('#report_link').attr('href', report_link);

                jQuery('#certificate_link').attr('href', certificate_link);

                jQuery('.popShape').html('<strong>Shape : </strong>' + shape);
                jQuery('.popColor').html('<strong>Color : </strong>' + color);
                jQuery('.popClarity').html('<strong>Clarity : </strong>' + clarity);
                jQuery('.popCarat').html('<strong>Carat : </strong>' + carat);
                jQuery('.popCut').html('<strong>cut : </strong>' + cut);
                jQuery('.popPolish').html('<strong>Polish : </strong>' + polish);
                jQuery('.popSymentry').html('<strong>Symentry : </strong>' + symmetry);
                jQuery('.popEyeClean').html('<strong>Eye Clean : </strong>' + eye_clean);
                jQuery('.popFlourecense').html('<strong>Flourecense : </strong>' + florescence);
                jQuery('.popGradedBy').html('<strong>Graded By : </strong>' + lab);



                jQuery('.popTable').html('<strong>Table : </strong>' + table);
                jQuery('.popHnA').html('<strong>HnA : </strong>' + hna);
                jQuery('.popGirdle').html('<strong>Girdle : </strong>' + girdle);
                jQuery('.popCrHeight').html('<strong>Cr Height : </strong>' + crown_height);
                jQuery('.popPawDepth').html('<strong>Paw Depth : </strong>' + pavilion_depth);
                jQuery('.popCrAng').html('<strong>Cr Ang : </strong>' + crown_angle);
                jQuery('.popGirdlePer').html('<strong>Girdle Per : </strong>' + girdle_percentage);
                jQuery('.popPawAngle').html('<strong>Paw Angle : </strong>' + pavilion_angle);
                jQuery('.popLaser').html('<strong>Laser : </strong>' + laser_inscription);
                jQuery('.popGirdleCondition').html('<strong>Girdle Cond. : </strong>' + girdle_condition);
                jQuery('.popStarLength').html('<strong>Star Length : </strong>' + star_length);
                jQuery('.popLowerHalf').html('<strong>Lower Half : </strong>' + lower_half);
                jQuery('.popComment').html('<strong>Comment : </strong>' + short_description);
                jQuery('.popRapRat').html('<strong>Rap Rat : </strong>' + rapnet_price);
                jQuery('.popBack').html('<strong>Back (%) : </strong>' + back_percentage);
                jQuery('.popNatts').html('<strong>Natts : </strong>' + natts);
                jQuery('.popTableInc').html('<strong>Table Inc : </strong> ');
                jQuery('.popBrowness').html('<strong>Browness : </strong>' + browness);
                jQuery('.popMilky').html('<strong>Milky : </strong>' + milky);

                jQuery('.four_images').addClass(' MagicScroll ');
                jQuery('.MagicMagnify').attr('id', 'diamond' + entity_id).attr('rel', 'group:diamond' + entity_id);
                jQuery('.MagicScroll').html('');
                jQuery('.MagicScroll').attr('id', 'scroll' + entity_id);

                jQuery('.item_main > h3').html('Reference: ' + sku);

                jQuery('.overlayed_custom').find('img').attr('src', '');

                jQuery('.overlayed_small_custom').html('');

                jQuery('.four_images').css('padding-top', '17px');

                if (PopData[0].imgProd != null)
                {
                    jQuery('.overlayed_custom').css('display', 'block');
                    jQuery('#no_image').css('display', 'none');
                    var j = 0;
                    while (j <= PopData[0].imgProd.length - 1)
                    {

                        if (j == 0)
                        {
                            jQuery('.overlayed_custom').find('img').attr('src', PopData[0].imgProd[j]).css('height', '300px').css('width', '300px');

                            jQuery('.overlayed_custom').find('a').attr('href', PopData[0].imgProd[j]);

                            jQuery('.cartPopImage').attr('id', 'item-id-' + entity_id);
                            jQuery('.product-image').find('img').attr('src', PopData[0].imgProd[j]);
                        }
                        jQuery('.four_images').append('<a  href="' + PopData[0].imgProd[j] + '" rev="' + PopData[0].imgProd[j] + '" rel="magnifier-id:diamond' + entity_id + '" class="overlayed_small_custom"><img src="' + PopData[0].imgProd[j] + '" style="height:65px; width:65px" /></a>');
                        j++;
                    }
                    if (jQuery('.overlayed_small_custom').find('img').attr('src') == '')
                    {
                        jQuery(this).remove();
                    }
                }
                else
                {
                    jQuery('.overlayed_custom').css('display', 'none');
                    jQuery('.four_images').removeClass(' MagicScroll ');
                    jQuery('#no_image').css('display', 'block');
                }


                if (window.innerWidth > 480)
                {
                    //jQuery.colorbox.close();
                }
                else if (window.innerWidth <= 480)
                {
                    if (jQuery('#responsive_' + entity_id + '_1').html() == '' && jQuery('#responsive_' + entity_id + '_2').html() == '')
                    {
						jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Shape : </strong>' + shape + '</div>');
						jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Color : </strong>' + color + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Clarity : </strong>' + clarity + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Carat : </strong>' + carat + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>cut : </strong>' + cut + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Polish : </strong>' + polish + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Symentry : </strong>' + symmetry + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Eye Clean : </strong>' + eye_clean + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Flourecense : </strong>' + florescence + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Graded By : </strong>' + lab + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Table : </strong>' + table + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>HnA : </strong>' + hna + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Girdle : </strong>' + girdle + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Cr Height : </strong>' + crown_height + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Paw Depth : </strong>' + pavilion_depth + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Cr Ang : </strong>' + crown_angle + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Girdle Per : </strong>' + girdle_percentage + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Paw Angle : </strong>' + pavilion_angle + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Laser : </strong>' + laser_inscription + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Girdle Cond.: </strong>' + girdle_condition + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Star Length : </strong>' + star_length + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Lower Half : </strong>' + lower_half + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Rap Rat : </strong>' + rapnet_price + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Back (%) : </strong>' + back_percentage + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Natts : </strong>' + natts + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Table Inc : </strong> ' + '</div>');
                        jQuery('#responsive_' + entity_id + '_2').append('<div class="responsive_div"><strong>Browness : </strong>' + browness + '</div>');
                        jQuery('#responsive_' + entity_id + '_1').append('<div class="responsive_div"><strong>Milky : </strong>' + milky + '</div>');
                        jQuery('#responsive_' + entity_id).append('<div class="responsive_comment"><strong>Comment : </strong>' + short_description + '</div>');
                    }
                    jQuery('.responsive_div').css('background-color', 'aliceblue'); 
                    
                    jQuery('.responsive_data:not(#responsive_'+ entity_id+')').slideUp('slow');	
					jQuery('#responsive_' + entity_id).slideToggle('slow');                    
                                       
                }
            }
        });*/
    }
    
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
            }, 70000)
        });
    }

