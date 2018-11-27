$(document).ready(


	function()
	{
		oMain.init();



	}
);
window.oMain = {
  init : function(){

		oLazyLoad.init();
		Tickets.init({aCustom : { iUserId : 1 , iStatus : 1 }});
		$('#ticketsModal').on('hidden.bs.modal', function () {
			 Tickets.init({aCustom : { iUserId : 1 , iStatus : 1 }});
		});
		oPusher.init('support_requests' , 'update_ticket',function(aResp){
			 toastr.info(aResp, 'Tickets Updated');
			 Tickets.init();
		});
		$("input[name='chat_message']").keypress(function(e) {
	    if (e.which == 13) {
				 e.preventDefault();
				 if($("input[name='chat_message']").val()){
					 aModules.oChat.send();
				 }else{
					  toastr.error("Chat messege required", 'Opps Something went wrong');
				 }
	    }
		});

		$("button[name='chatBtn']").click(function(){
			if($("input[name='chat_message']").val()){
				aModules.oChat.send();
			}else{
				 toastr.error("Chat messege required", 'Opps Something went wrong');
			}
		});
		oNum.init();
  }
};

// Lazy loading Images
window.oLazyLoad = {
  init : function() {
		var $q = function(q, res){
				if (document.querySelectorAll) {
					res = document.querySelectorAll(q);
				} else {
					var d=document
						, a=d.styleSheets[0] || d.createStyleSheet();
					a.addRule(q,'f:b');
					for(var l=d.all,b=0,c=[],f=l.length;b<f;b++)
						l[b].currentStyle.f && c.push(l[b]);

					a.removeRule(0);
					res = c;
				}
				return res;
			}
		, addEventListener = function(evt, fn){
				window.addEventListener
					? this.addEventListener(evt, fn, false)
					: (window.attachEvent)
						? this.attachEvent('on' + evt, fn)
						: this['on' + evt] = fn;
			}
		, _has = function(obj, key) {
				return Object.prototype.hasOwnProperty.call(obj, key);
			}
		;

	function loadImage (el, fn) {
		var img = new Image()
			, src = el.getAttribute('data-src');
		img.onload = function() {
			if (!! el.parent)
				el.parent.replaceChild(img, el)
			else
				el.src = src;

			fn? fn() : null;
		}
		img.src = src;
	}

	function elementInViewport(el) {
		var rect = el.getBoundingClientRect()

		return (
			 rect.top    >= 0
		&& rect.left   >= 0
		&& rect.top <= (window.innerHeight || document.documentElement.clientHeight)
		)
	}

		var images = new Array()
			, query = $q('img.lazy')
			, processScroll = function(){
					for (var i = 0; i < images.length; i++) {
						if (elementInViewport(images[i])) {
							loadImage(images[i], function () {
								images.splice(i, i);
							});
						}
					};
				}
			;
		// Array.prototype.slice.call is not callable under our lovely IE8
		for (var i = 0; i < query.length; i++) {
			images.push(query[i]);
		};

		processScroll();
		addEventListener('scroll',processScroll);
  }
};

// Tickets Module
window.Tickets =
{
	bInit	: false,
	sTitle	: 'Tickets Tickets',
	sDesc	: '',
	init	: function(aArg, cCb)
	{
		this.aWidgets.Tickets.init(aArg, cCb);
	},
	aWidgets :
	{
		Tickets :
		{
			oForm		: null,
			bInit		: false,
			sModule	: 'Tickets',
			sIndex	: 'iTicketsId',
			sItem		: 'tickets',
			oInterval : {},
			aDataTable: {
			sId			: '#TicketsDataTable',
			sTable	: 'Tickets',
			sModule	: 'Tickets',
      aColumns	: [{
				sTitle		: 'Reference Code',
				mData		  : 'reference_code',
				sWidth		: 10,
				render : function(data, type, row){
					return '<a href="javascript:Tickets.aWidgets.Tickets.form(\'' + row.reference_code + '\')">'+data+'</a>'
				}
			},{
				sTitle		: 'Subject ',
				mData			: 'subject',
				sWidth		: 20,

			},{
				sTitle		: 'Message ',
				mData			: 'message',
				sWidth		: 20,
			},{
				sTitle		: 'Date started',
				mData			: 'support_date_started',
				render 		: function(data, type, row){
					  return data ? moment(data).format('DD-MM-YYYY HH:mm:ss') : '';
				},
				sWidth		: 10,
			},{
				sTitle		: 'Actions',
				sWidth		: 30,
				mData			: 'bActive ',
				render  	: function(data, type, row){
						return row.status;
					}
				}]
	    },
			init : function(aArg, cCb)
			{
				var oSelf = this;
				oRequest.apiCall(sUrl+"/client/supportrequests", 'GET'  , null , function(resp){
					resp.unread_support_requests ? $('span[name="SupportBadge"]').attr('class','badge') : '';
					$('span[name="SupportBadge"]').html(resp.unread_support_requests ? resp.unread_support_requests : '');
					oTables.render([{
							sTableId : oSelf.aDataTable.sId ,
							aData    : resp.support_requests,
							aColumns : oSelf.aDataTable.aColumns
						}]);
				});
			},
			form : function(aArg) {
					if(aArg){
						var oSelf = this;
						oRequest.apiCall(sUrl+"/client/supportrequests/"+aArg, 'GET'  , null , function(aResp){
							$('.addForm').hide();
							$('.btnAdd').hide();
							$('.sSubject').html(aResp.support_requests.subject);
							$('.sTicketNo').html(aResp.support_requests.reference_code);
							$('.sDescription').html(aResp.support_requests.message);
							$('.ViewConversation').show();
							$("#ticketsModal").modal("show");
							$("input[name='message']").val('')
							$("input[name='reference_code']").val(aResp.support_requests.reference_code);
							if(aResp.support_requests.conversations){
								aModules.oChat.render(aResp.support_requests.conversations);
							}
							if(aResp.support_requests.status == "ONGOING"){
								  $("input[name='chat_message']").removeAttr("disabled");
									$("a#sendBtn").attr("href","javascript:aModules.oChat.send()");
							}else{
								  $("input[name='chat_message']").attr("disabled","disabled");
									$("a#sendBtn").removeAttr("href");
							}
							 oScroll.scrollToBottom();
							 oPusher.init('support_requests',aResp.support_requests.reference_code ,function(resp){
								 oRequest.apiCall(sUrl+"/client/supportrequests/"+aResp.support_requests.reference_code, 'GET'  , null , function(resp){
									 if(resp.support_requests.conversations){
 										aModules.oChat.render(resp.support_requests.conversations,resp.support_requests.reference_code);
										oScroll.scrollToBottom();
 									}
								 });
							 });
							 $('.direct-chat-messages').attr("Reference",aResp.support_requests.reference_code);
						});
					}else{
						$('.addForm').show();
						$('.btnAdd').show();
						$('.ViewConversation').hide();
						$('#ticketsModal').modal('show');
					}
			},

			filterTable : function(sArg)
			{
				oTable = $('#TicketsDataTable').dataTable();
				var Filtered = oTable.fnFilter( sArg );
		    return Filtered;
			},

			ramdom : function(){
				var text = "";
				 var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
				 for (var i = 0; i < 15; i++)
					 text += possible.charAt(Math.floor(Math.random() * possible.length));
				 return text;
			},

			save : function(oNode, aArg)
			{
				var oSelf = this;
				oRequest.apiCall(sUrl+"/client/supportrequests", 'POST'  , {
						subject :$("input[name='subject']").val(),
						message : $("textarea[name='message']").val(),
						csrf_token : $("input[name='csrf_token']").val()
				} , function(resp){
					toastr.success('Success!', 'Tickets Created Successfully');
					$("#ticketsModal").modal('hide');
					$("input[name='message']").val('');
					$("input[name='subject']").val('');
					Tickets.init();
				});

			}
		}
	}
};


window.oTables = {
	sId : null,
  render :  function(aArg){
		var oTable = $(aArg[0].sTableId);
		this.sId = oTable;
		if(oTable){
			if ( $.fn.DataTable.fnIsDataTable(oTable) ) {
				oTable.DataTable().clear().draw();
				oTable.DataTable().rows.add(aArg[0].aData);
				oTable.DataTable().columns.adjust().draw();
			}else{
				oTable.DataTable({
					data 	  : aArg[0].aData,
					columns : aArg[0].aColumns,
					order: [[ 3, "desc" ]],
					aoColumnDefs: [{ "sType": "date-uk", "aTargets": [3] }],
					fnRowCallback: function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
						if(aData.has_unread_messages){
							 $('td', nRow).css('background-color', '#f2f2f2');
						}
					 }
				});
			}
		}
	}
};

//Tickets
window.aModules = {
	oChat : {
		send : function() {
			var oSelf = this;
			var reference_code = $("input[name='reference_code']").val();
			oRequest.apiCall(sUrl+"/client/supportrequests/"+reference_code, 'POST'  , {
					message : $("input[name='chat_message']").val(),
					csrf_token : $("input[name='csrf_token']").val()
			} , function(resp){
				aModules.oChat.render(resp.support_requests.conversations);
				$("input[name='chat_message']").val('');
			});
		},
		render : function(aArg,reference_code){
				var Msgs = '';
				$.each(aArg, function( index, value ) {
					Msgs  += '<div class="direct-chat-msg '+ ( value.sender_type =='Admin' ? '' : 'right') +'">'+
						'<div class="direct-chat-info clearfix">'+
							'<span class="direct-chat-name pull-left">'+value.sender_name+'</span>'+
							'<span class="direct-chat-timestamp pull-right">'+value.date_submitted+'</span>'+
						'</div>'+
						'<img class="direct-chat-img" src="https://adminlte.io/themes/AdminLTE/dist/img/user1-128x128.jpg" alt="message user image">'+
						'<div class="direct-chat-text">'+
							value.message+
						'</div>'+
					'</div>';
				});
				if(reference_code){
					$('div[reference="'+reference_code+'"]').html(Msgs);
				}else{
					$('.direct-chat-messages').html(Msgs);
				}
		}
	},
};

window.oRequest = {
  call : function(aArg,cCb){
    $.ajax({
      url			: 'http://localhost/acl/openapi/',
      type		: 'POST',
      dataType	: 'text',
      processData	: false,
      data		: window.btoa(JSON.stringify(aArg)),
      success		: function(sResp)
      {
        cCb(jQuery.parseJSON(sResp));
      },

      complete : function(oXhr, sStatus)
      {
        $('#cover').fadeOut(300);
      },
      error : function(oXhr, sStatus, Ticketsg)
      {
        $('#cover').fadeOut(300);
      }
    });
  },
	apiCall : function(sUrl, type  , aArg , cCb){
		$("button[name='chatBtn']").attr("disabled","disabled");
		$("button[name='chatBtn']").html("Sending...");
		$("input[name='chat_message']").attr("disabled","disabled");
		$.ajaxSetup({
				headers: {
						'X-CSRF-Token': $("input[name='csrf_token']").val()
				}
		});

    $.ajax({
      url			: sUrl,
      type		: type,
      dataType	: 'json',
			//contentType: "application/json; charset=utf-8",
      data			: aArg ? aArg : null,
      success		: function(sResp)
      {
				$("button[name='chatBtn']").removeAttr('disabled');
				$("button[name='chatBtn']").html("Send");
				$("input[name='chat_message']").removeAttr("disabled");
        cCb(sResp);
      },

      complete : function(oXhr, sStatus)
      {
        $('#cover').fadeOut(300);
      },

      error : function(sResp)
      {
        cCb(sResp);
      }
    });
  }
};

window.oPusher = {
	init : function (sChannel,sEvent,cCb){
		Pusher.logToConsole = false;
		var pusher = new Pusher(sKey, {
			cluster: 'ap1',
			encrypted: true
		});
		var channel = pusher.subscribe(sChannel);
		channel.bind(sEvent, function(aResp) {
			cCb(aResp);
		});
	}
};

window.oScroll = {
	scrollToBottom : function () {
		var div = $(".direct-chat-messages");
	  div.scrollTop(div.prop('scrollHeight'));
	},
};

window.oNum = {

  init: function () {


      Number.prototype.toMonetaryString = function (iDecimals) {
          return this.toFixed(iDecimals).replace(/(\d)(?=(\d{3})+\b)/g, '$1,');
      };

      String.prototype.fromMonetarySting = function () {
          return +this.replace(/[^\d\.\+-]+/g, '');
      };
  },

  parseToDecimal: function (iDecimals) {
      var currency = iDecimals;
      return Number(currency.replace(/[^0-9\.]+/g,""));
  },

  getKey: function (oEvent) {
      if (window.event)
          return window.event.keyCode;
      else if (oEvent)
          return oEvent.which;
      else
          return null;
  },

  checkInput: function (oNode, oEvent) {
      return (
         /^\d*\.?\d*$/.test(oNode.value + String.fromCharCode(this.getKey(oEvent))) ||
         $.inArray(this.getKey(oEvent), [8, 0]) > -1
      );
  },

  onPriceBlur: function (oNode) {
      oNode.value !== '' && (
          oNode.value = parseFloat(oNode.value).toMonetaryString(2)
      );
  },

  onPriceFocus: function (oNode) {
      oNode.value !== '' && (
          oNode.value = String(oNode.value).fromMonetarySting()
      );
  },

	tempData : {}
};

$.extend(jQuery.fn.dataTableExt.oSort, {
    "date-uk-pre": function (a) {
    var x;
    try {
    var dateA = a.replace(/ /g, '').split("-");
    var day = parseInt(dateA[0], 10);
    var month = parseInt(dateA[1], 10);
    var year = parseInt(dateA[2], 10);
    var date = new Date(year, month - 1, day)
    x = date.getTime();
    }
    catch (err) {
    x = new Date().getTime();
    }

    return x;
    },

    "date-uk-asc": function (a, b) {
    return a - b;
    },

    "date-uk-desc": function (a, b) {
    return b - a;
    }
});
