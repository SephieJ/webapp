window.AgreementBuying =
{
	bInit	: false,
	sTitle	: 'Buying Agreement Modules',
	sDesc	: '',
	init	: function(aArg, cCb)
	{
		this.aWidgets.AgreementBuying.init(aArg, cCb);
	},
	aWidgets :
	{
		AgreementBuying :
		{
			iAgreementId : null,
			oForm		: null,
			bInit		: false,
			sModule	: 'AgreementBuying',
			sIndex	: 'iAgreementBuyingId',
			sItem		: 'AgreementBuying',
			oInterval : {},
			aDataTable: {
			sTable	: 'AgreementBuying',
			sModule	: 'AgreementBuying',
	    },
			init : function(aArg, cCb)
			{
        var oSelf = this;
        $("button[name='BuyerAcceptance']").click(function(){
            //oSelf.confirm(this.value);
						$("div[name='BuyingAgreements']").modal('show');
        });

				$("button[name='Confirm']").click(function(){
						oSelf.save();
				});

				if(reference_code){
					  $('input[name="booking_reference_code"]').val(reference_code);
						oRequest.apiCall(sUrl+"/get/resources/agreement/"+reference_code, 'GET'  , null , function(resp){
						 if(resp.agreement.status == "ACCEPTED"){
							 $('button[name="BuyerAcceptance"]').hide();
							 $('a[name="No"]').hide();
							 $('label.label-agreement').hide();
						 }
						 $('div[name="buying-agreement"]').html(resp.agreement.agreement_html);
						 $("div#divLoading").removeClass('show');
					 });
				}

			},
      confirm : function(aArg) {
				//$('button[name="No"]').attr("formaction", "/transactions/"+aArg+"/accept");
				//$('button[name="Yes"]').attr("formaction", "/transactions/"+aArg+"/gotoagreement");
        $("div[name='BuyingAgreements']").modal('show');
			},
      accept : function(aArg) {

			},
			form : function(aArg) {

			},

			save : function()
			{
				var agreement = {
						booking_reference_code :$("input[name='booking_reference_code']").val(),
						csrf_token : $("input[name='csrf_token']").val()
				};
				//console.log(agreement);
				oRequest.apiCall(sUrl+"/resources/agreement/accept", 'POST'  , agreement , function(resp){
					//console.log(resp);
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
					if(resp.status == 'success'){
						toastr.success('Agreement Accepted Successfully','Success!');
						location.reload();
					}else{
						toastr.error(resp.message,'Opps!');
					}

				});
			},

			template : function(aArg)
			{
			   var tRate = parseFloat(aArg.quantity) * parseFloat(aArg.resource.price);
				 var tSevenPercentRate = tRate * 1.07;
				 var temp = '';
				 var d = new Date();
				 var strDate = (d.getMonth()+1) + "/" +  d.getDate() + "/" + d.getFullYear();
				// temp += '      <p contenteditable="false" class="mceNonEditable"><strong>LEASE AGREEMENT</strong></p>';
				// temp += '				<p contenteditable="false">This Lease Agreement is made and executed on this <span contenteditable="true">____________</span> day of _____&nbsp;at</p>';
				// temp += '				<p>________________ by and between: Sri ________________ S/O D/O W/O ______________</p>';
				// temp += '				<p>aged about _______________ Occupation _______________ R/O _____________________</p>';
				// temp += '				<p>___________________________________________________________________________</p>';
				// temp += '				<p>Presented by his/her agent</p>';
				// temp += '				<p>Being minor represented by Father/Mother/Brother/Guardian</p>';
				// temp += '				<p>Sri ________________ S/o, D/o, W/o __________________&nbsp;Aged about _________________</p>';
				// temp += '				<p>years Occupation: ___________________Residing at under general / special power of attorney</p>';
				// temp += '				<p>dated: _____________________&nbsp;Registered as Document Number ______ of the year ______</p>';
				// temp += '				<p>Book- I/IV of RO/SRO__________.</p>';
				// temp += '				<p>&nbsp;</p>';
				// temp += '				<p>(Hereinafter called the Landlord or Lessor which term shall mean and include all ther heirs, legal, representatives, nominees and assigns etc.).</p>';
				// temp += '				<p>Sri ________________________ S/o D/o W/o _____________________ aged about</p>';
				// temp += '				<p>___________________ Occupation ___________________ R/o _______________________</p>';
				// temp += '				<p>___________________________________________________________________________</p>';
				// temp += '				<p>Being minor representatec by Father/Mother/Brother/Guardian</p>';
				// temp += '				<p>Sri ________________________ S/o D/o W/o _____________________ aged about</p>';
				// temp += '				<p>_____________________ years, Occupation: ______________________________________</p>';
				// temp += '				<p>Residing at _________________________________________________________________</p>';
				// temp += '				<p>&nbsp;</p>';
				// temp += '				<p>(Hereinafter called the Landlord or Lessee which term shall mean and include all ther heirs, legal, representatives, nominees and assigns etc.).</p>';
				// temp += '				<p>&nbsp;</p>';
				// temp += '				<p>Whereas the land lord herein is absolute owner of the house bearing No. ____________ in</p>';

				temp += ' <p><img src="'+(aArg.seller.company.image_url ? aArg.seller.company.image_url : '/static/assets/img/building.png')+'" height="60"/></p>';
				temp += ' <p><strong>'+aArg.seller.company.name.toUpperCase()+'</strong> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>AGREEMENT</strong></p>';
				//temp += ' <p>'+aArg.seller.company.company_info.toUpperCase()+' '+ aArg.seller.company.address.postal_code.toUpperCase()+'</p>';
				temp += ' <p>'+aArg.seller.company.address.block_street.toUpperCase()+' '+ aArg.seller.company.address.postal_code.toUpperCase()+'</p>';
				temp += ' <p></strong>'+aArg.seller.first_name.toUpperCase() +' '+ aArg.seller.last_name.toUpperCase() +'</strong></p>';
				temp += ' <p>&nbsp;</p>';
				temp += ' <p>To:</p>';
				temp += ' <p></strong>'+aArg.buyer.first_name.toUpperCase() +' '+ aArg.buyer.last_name.toUpperCase() +'</strong></p>';
				temp += ' <p>'+aArg.buyer.company.name.toUpperCase()+'</p>';
				//temp += ' <p>'+aArg.buyer.company.company_info.toUpperCase()+'</p>';
				temp += ' <p>'+aArg.buyer.company.address.block_street.toUpperCase()+' '+ aArg.seller.company.address.postal_code.toUpperCase()+'</p>';
				temp += ' <p>&nbsp;</p>';
				temp += ' <p>RE: Agreement</p>';
				temp += ' <p>This is an agreement made and executed on this day '+strDate+' <strong>'+aArg.seller.company.name.toUpperCase()+'</strong> and <strong>'+aArg.buyer.company.name.toUpperCase()+'</strong> regarding the sharing of resource <strong>'+aArg.resource.name.toUpperCase()+'</strong> as per the following details.&nbsp;</p>';
				temp += ' <p>Resource Item Description&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '+aArg.resource.description+'</p>';
				temp += ' <p>Unit of item or service&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '+aArg.quantity+ ' per ' +aArg.resource.resource_rate.toUpperCase() +' </p>';
				temp += ' <p>Agreed booking rates&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '+aArg.resource.price+'&nbsp;</p>';
				temp += ' <p>Total Rates (without GST) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = '+ tRate.toMonetaryString(2) +'</p>';
				temp += ' <p>Total Rates (With 7%. GST)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = '+tSevenPercentRate.toMonetaryString(2)+' (Please delete if you are not a GST registered company or if the rate above is inclusive of GST)</p>';
				temp += ' <p>Delivery Details&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Please add in how you will fulfill the booking</p>';
				temp += ' <p>Payment Terms &amp; Details&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; C.O.D/30 days/Deposit Required (Please delete where appropriate)</p>';
				temp += ' <p>Please make cheque payable to _________________</p>';
				temp += ' <p>Please make a bank transfer to ___________________</p>';
				temp += ' <p>&nbsp;</p>';
				temp += ' <p>Terms &amp; Conditions</p>';
				temp += ' <p>We agree to supply the resource based on the details above, provided that payment has been made.</p>';
				temp += ' <p>Resource should be returned in original condition. Any damages will be further assessed and could be subject to additional charges.</p>';
				temp += ' <p>You must reasonably co-operate with the company to allow us to establish and supply the resource to you safely and efficiently.</p>';
				temp += ' <p>In using the service or resource, you must comply with all laws, all directions by the Regulator and reasonable directions by the company.</p>';
				temp += ' <p>In using the resource (if storage space), you will only store items allowed by the owner and building approvals, which includes_please fill in or delete if not required_.</p>';
				temp += ' <p>In using the resource (if equipment), you will ensure that you have the right personnel to operate the equipment that would ensure safety of personnel.</p>';
				temp += ' <p>For other terms, please view the Terms of Use of the site for other member responsibilities</p>';
				temp += ' <p>Additional lines for users T&amp;Cs</p>';
				temp += ' <p>&nbsp;</p>';
				temp += ' <p>Agreement Template is provided by Resources to Share Pte Ltd.</p>';


				return temp;

			}
		}
	}
};
