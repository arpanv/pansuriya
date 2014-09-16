jQuery(document).ready(function(){
	
	jQuery('#dob').datepicker();
	jQuery('#anniversary').datepicker();
	
	jQuery(".oe_signup_form").validate({
        rules: {
            name: "required",            
            prefix: "required",            
            lastname: "required",            
            gender: "required",            
            dob: "required",            
            login: {
				required: true,
                email: true
			},
			password: "required",
			confirm_password: {
				equalTo : '#password'
			},
			contact_no: {
				required:true,
				number:true
			},
			company_name: "required",            
			owner_name: "required",            
			company_address: "required",            
			city: "required",            
			state: "required",            
			country: "required",
			telephone: {
				required:true,
				number:true
			},
			zip: "required",            
			nature_of_business: "required",            
			broker: "required",            
			agent: "required",            
        },        
        messages: {
            name: "Please enter your first name",
            prefix: "Please select prefix",
            lastname: "Please enter your last name",
            gender: "Please select gender",
            dob: "Please enter date of birth",
            login: {
				required: "Please enter email address",
                email: "Please enter valid email address"
			},
			password: "Please enter password",    
			confirm_password: {
				equalTo : 'password does not match'
			},
			contact_no: {
				required:"Please enter contact number",
				number:"Please enter only number"
			},
			company_name: "Please enter company name",
			owner_name: "Please enter owner name",
			company_address: "Please enter company address",
			city: "Please enter city",
			state: "Please select state",
			country: "Please select country",
			telephone: {
				required: "Please enter telephone numner",
				number: "Please enter only number"
			},
			zip: "Please enter zip code",
			nature_of_business: "Please select nature of business",
			broker: "Please select broker",
			agent: "Please select agent",
        },        
        submitHandler: function(form) {			
            form.submit();
        }
    });
});
