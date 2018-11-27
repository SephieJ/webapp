window.AgreementSelling =
{
	bInit	: false,
	sTitle	: 'Selling Agreement Modules',
	sDesc	: '',
	selector: 'span',  // change this value according to your HTML
    keep_styles: true,
    paste_retain_style_properties: "font-size font-style",
	init	: function(aArg, cCb)
	{
		this.aWidgets.AgreementSelling.init(aArg, cCb);
	},
	aWidgets :
	{
		AgreementSelling :
		{
			iAgreementId : null,
			oForm		: null,
			bInit		: false,
			sModule	: 'AgreementSelling',
			sIndex	: 'iAgreementSellingId',
			sItem		: 'AgreementSelling',
			oInterval : {},
			aDataTable: {
			sTable	: 'AgreementSelling',
			sModule	: 'AgreementSelling',
	    },
			init : function(aArg, cCb)
			{
        var oSelf = this;
        $("button[name='AgreementTemplate']").click(function(){
            oSelf.confirm(this.value);
        });
				$("button[name='SendAgreement']").click(function(){
					if($(this).attr('edit_confirm')){
						$("div[name='ConfirmSendAgreement']").modal('show');
					}else{
						oSelf.save();
					}
						//
				});



				if(transaction_id){
						// var sRender ='';
						oRequest.apiCall(sUrl+"/agreements/"+transaction_id, 'GET'  , null , function(resp){
								 var sRender = (resp.agreements.status == 'success') ? resp.agreements.agreement.agreement_html :  oSelf.template(resp);
								 $('input[name="booking_reference_code"]').val((resp.agreements.status == 'success' ? resp.agreements.agreement.booking_reference_code : resp.reference_code ));
								 $('textarea[name="agreement_html"]').val(sRender);
								 tinymce.init({
 									selector: '#agreement_html',
 									height: 850,
 									theme: 'modern',
 									plugins: 'print preview fullpage searchreplace autolink directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount imagetools  contextmenu colorpicker textpattern help',
 									toolbar1: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent  | removeformat',
 									image_advtab: true,
 									branding : false,
									//readonly : 1
 								 });

								 if(resp.agreements.status == 'success'){
									 if(resp.agreements.agreement.status == "ACCEPTED"){
										 $('textarea[name="agreement_html"]').hide();
										 $('div[name="selling-agreement"]').html(resp.agreements.agreement.agreement_html);
										 $('button[name="SendAgreement"]').hide();
										 $('button[name="EditAgreement"]').hide();
										 $('label.label-agreement').hide();
										 tinymce.activeEditor.setMode('readonly');
									 }else{
										 tinymce.activeEditor.setMode('readonly');
										 $('textarea[name="agreement_html"]').show()
									 }

									 $('input[name="agreement_id"]').val(resp.agreements.agreement.id);
									 //$('button[name="SendAgreement"]').html("Edit Agreement");
								 }else{
									 $('button[name="EditAgreement"]').hide();
									 $('button[name="SendAgreement"]').show();
									 $('textarea[name="agreement_html"]').val(oSelf.template(resp));
									 $('textarea[name="agreement_html"]').show();
									 tinymce.activeEditor.setMode('design');
								 }


								 $("div#divLoading").removeClass('show');

								 $('button[name="EditAgreement"]').click(function(){
									 	tinymce.activeEditor.setMode('design');
										$('button[name="SendAgreement"]').show();
										//$('button[name="SendAgreement"]').attr("edit_confirm" , true);
								 });

						  });


				}
			},
      confirm : function(aArg) {
				$('button[name="No"]').attr("formaction", "/transactions/"+aArg+"/accept");
				$('button[name="Yes"]').attr("formaction", "/transactions/"+aArg+"/gotoagreement");
        $("div[name='AgreementSelling']").modal('show');
			},
      accept : function(aArg) {

			},
			form : function(aArg) {

			},

			save : function()
			{
				var agreement = {
						booking_reference_code : $("input[name='booking_reference_code']").val(),
						agreement_html 	: tinyMCE.activeEditor.getContent(),//$("textarea[name='agreement_html']").val(),
						csrf_token 			: $("input[name='csrf_token']").val()
				};
				var sRoute = $("input[name='agreement_id']").val() ? sUrl+"/resources/agreement/edit" : sUrl+"/resources/agreement/add";


				oRequest.apiCall(sRoute, 'POST'  , agreement , function(resp){
					toastr.options = {
					  "closeButton": false,
					  "debug": false,
					  "newestOnTop": false,
					  "progressBar": false,
					  "positionClass": "toast-bottom-left",
					  "preventDuplicates": false,
					  "onclick": null,
					  "showDuration": "300",
					  "hideDuration": "1000",
					  "timeOut": "5000",
					  "extendedTimeOut": "1000",
					  "showEasing": "swing",
					  "hideEasing": "linear",
					  "showMethod": "fadeIn",
					  "hideMethod": "fadeOut"
					};

					//if(resp.status == "success"){
						toastr.info(($("input[name='agreement_id']").val() ? 'Agreement Edited Successfully':'Agreement Send Successfully'),'Success!');
						setTimeout(function(){ location.reload(); }, 1000);
					//}
				});
			},

			template : function(aArg)
			{
			   var tRate = parseFloat(aArg.quantity) * parseFloat(aArg.resource.price);
				 var tSevenPercentRate = tRate * 1.07;
				 var temp = '';
				 var d = new Date();
				 var strDate = (d.getMonth()+1) + "/" +  d.getDate() + "/" + d.getFullYear();
					temp += '  <p><!--StartFragment--></p>';
					temp += '	<p style="text-align: center; line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;" align="center"><strong><span style="font-size: 18.0pt; color: black;">AGREEMENT</span></strong></p>';
					temp += '	<p style="text-align: center; line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;" align="center">&nbsp;</p>';
					temp += '<p style="text-align: center; line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;" align="center"><span style="position: absolute; z-index: -1; right: 0px; margin-right: 20px;  width: 155px; height: 80px;">'+(aArg.seller.company.image_url ? '<img src="'+ aArg.seller.company.image_url +'" height="60" />' : '') + '</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><strong><span style="font-size: 10.0pt; color: black;">'+(aArg.seller.company.name ? aArg.seller.company.name : '')+'</span></strong></p>';
					temp +=  (aArg.seller.company.address ? '<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">' + aArg.seller.company.address.block_street.toUpperCase() +'</span></p>' : '' );
					temp +=  (aArg.seller.company.address ? '<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">'  + aArg.seller.company.address.postal_code.toUpperCase() +'</span></p>' : '' );
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">To: <strong>'+(aArg.buyer.first_name ? aArg.buyer.first_name.toUpperCase() : '')+' '+ (aArg.buyer.last_name ? aArg.buyer.last_name.toUpperCase() : '')+'</strong></span></p>';
					temp += '	<table class="MsoTableGrid" style="border-collapse: collapse; border: none;margin-left:-8px;margin-top:-10px;" border="1" cellspacing="0" cellpadding="0" width="60%">';
					temp += '	<tbody>';
					temp += '	<tr style="height: 17.2pt;">';
					temp += '	<td style="width: 182.55pt; border: solid white 1.0pt; padding: 0cm 5.4pt 0cm 5.4pt; height: 17.2pt;" valign="top">';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;"> <strong>'+(aArg.buyer.company.name ? aArg.buyer.company.name.toUpperCase() : '')+'</strong></span></p>';
					temp += ' <p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">'+(aArg.buyer.company.address ? aArg.buyer.company.address.block_street.toUpperCase() : '')+'</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">'+(aArg.buyer.company.address ? aArg.buyer.company.address.postal_code.toUpperCase() : '')+'</span></p>';
					temp += '	</td>';
					temp += '	</tr>';
					temp += '	</tbody>';
					temp += '	</table>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;"><strong><span style="font-size: 10.0pt; color: black;">RE: Agreement</span></strong></p>';
					temp += '	<p style="line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">This is an agreement made and executed on this day 3/1/2018 between&nbsp;<strong>'+(aArg.seller.company.name ? aArg.seller.company.name.toUpperCase() : '')+'</strong>&nbsp;and&nbsp;<strong>'+(aArg.buyer.company.name ? aArg.buyer.company.name.toUpperCase() : '')+'</strong>&nbsp;regarding the sharing of resource:&nbsp;<strong>'+(aArg.resource.name ? aArg.resource.name.toUpperCase() :'')+'</strong>&nbsp;as per the following details.&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><strong><span style="font-size: 10.0pt; color: black;">Resource Description&nbsp;&nbsp;</span></strong><span style="font-size: 10.0pt; color: black;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">'+(aArg.resource.description ? aArg.resource.description : '')+'</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;">&nbsp;</p>';
					temp += '	<p style="line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;"><strong><span style="font-size: 10.0pt; color: black;">Other Details</span></strong></p>';
					temp += '	<table class="MsoTableGrid" style="border-collapse: collapse; border: none;" border="1" cellspacing="0" cellpadding="0">';
					temp += '	<tbody>';
					temp += '	<tr>';
					temp += '	<td style="width: 350.4pt; border: solid white 1.0pt; padding: 0cm 5.4pt 0cm 5.4pt;" valign="top" width="399">';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Date </span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">From:'+oPhp.date("d-m-Y",oPhp.strtotime(aArg.booking_start_date))+' - To:'+oPhp.date("d-m-Y",oPhp.strtotime(aArg.booking_end_date))+'</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Unit of item of Service</span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">'+aArg.quantity+ ' per ' +aArg.resource.resource_rate.toUpperCase() +'</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Agreed booking rates</span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">'+aArg.resource.price+'</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Total Rates (Excluding GST)</span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">'+ tRate.toMonetaryString(2) +'</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Total Rates (Including 7% GST)</span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;"> <span style="background: #F2F2F2;">'+tSevenPercentRate.toMonetaryString(2)+' (Please delete if you are not a GST registered</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;"><span style="background: #F2F2F2;">company or if the rate above is inclusive of GST)</span></p>';
					temp += '	</td>';
					temp += '	<td style="width: 200.4pt; border: solid white 1.0pt; border-left: none; background: #F2F2F2; padding: 0cm 5.4pt 0cm 5.4pt;" valign="top" width="399">';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;"><span style="text-decoration: none;">&nbsp;</p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Delivery Details</span></u></p>';
					//temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;"><input name="delevery_details" style="border:none;background: #F2F2F2;font-style: italic;" required placeholder="*Please fill this area"></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black; line-height: 1.2;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black; line-height: 1.2;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Payment Terms &amp; Details</span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black; line-height: 1.2;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black; line-height: 1.2;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Please make cheque payable to</span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black; line-height: 1.2;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black; line-height: 1.2;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><u><span style="font-size: 10.0pt; color: black;">Please make bank transfer to</span></u></p>';
					temp += '	<p style="margin: 0cm 0cm 0.0001pt; line-height: normal; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black; line-height: 1.2;">&nbsp;</span></p>';
					temp += '	</td>';
					temp += '	</tr>';
					temp += '	</tbody>';
					temp += '	</table>';
					temp += '	<p style="line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;"><strong><span style="font-size: 10.0pt; color: black;">Terms &amp; Conditions</span></strong></p>';
					temp += '<ul style="margin-bottom: 0cm; margin-top: 0px;line-height:18px;" type="disc">';
					temp += '<li style="color: black; line-height: normal; margin-top: 0cm; margin-right: 0cm; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt;">We agree to supply the resource based on the details above, provided that payment has been made.</span></li>';
					temp += '<li style="color: black; line-height: normal; margin-top: 0cm; margin-right: 0cm; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt;">Resource should be returned in original condition. Any damages will be further assessed and could be subject to additional charges.</span></li>';
					temp += '<li style="color: black; line-height: normal; margin-top: 0cm; margin-right: 0cm; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt;">We will aim to supply the resource safely and efficiently and expect reasonable co-operation for us to do so. </span></li>';
					temp += '<li style="color: black; line-height: normal; margin-top: 0cm; margin-right: 0cm; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt;">In using the service or resources, both companies have to comply with all prevailing laws and regulations including safety.</span></li>';
					temp += '<li style="color: black; line-height: normal; margin-top: 0cm; margin-right: 0cm; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt;">For other terms, please view the Terms of Use of this site for member responsibilities.</span></li>';
					temp += '<li style="color: black; line-height: normal; margin-top: 0cm; margin-right: 0cm; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt;"><span style="background: #F2F2F2;">Please add in or edit T&amp;Cs as per your requirements.</span></li>';
					temp += '</ul>';
					temp += '	<p style="line-height: normal; margin: 0cm 0cm 10pt; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; color: black;">&nbsp;</span></p>';
					temp += '	<p style="margin: 0cm 0cm 10pt; line-height: 115%; font-size: 11pt; font-family: Calibri, sans-serif;"><span style="font-size: 10.0pt; line-height: 115%;">&nbsp;</span></p>';
					temp += '	<p><!--EndFragment--></p>';
					return temp;
			}
		}
	}
};
