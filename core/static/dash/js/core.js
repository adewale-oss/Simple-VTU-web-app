// DATA

$(document).ready(function(){
    data_fetchPlans();
    buy_data();
    data_fetchPhone();
    data_showpin();
    data_fetchtypes();


    function data_showpin(){
        $(document).on('input', '#data_b_number', function(){
            let b_number = $('#data_b_number').val();
            if (b_number !== ''){
                $('#data_pindiv').removeAttr('hidden', true);
            }else{
                $('#data_pindiv').removeAttr('hidden', 'hidden');
            }
        });
    }


    function data_fetchPhone(){
        $(document).on('change', '#data_plan', function(){
            let plan = $('#data_plan').val();

            if (plan !== ""){
                $('#data_phoneNo').removeAttr('hidden', true);
            }else{
                $('#data_phoneNo').attr('hidden', 'hidden');
            }

        });
    }


    function data_fetchtypes(){
        $(document).on('change', '#data_network', function(){
            let network  = $('#data_network').val();
            let csrfToken  = $("[name=csrfmiddlewaretoken]").val();
            if (network !== ""){
                $('#data_selectType').removeAttr('hidden', true);
            }else{
                $('#data_selectType').attr('hidden', 'hidden');
            }

           

            $('#data_type').html("<option value=''>Please select Plan type</option>");
            $.ajax({ 
                type: "POST",
                url: "/user/data/type/",  
                //data: JSON.stringify({network: network}),
                data: {network: network},
                headers : {'X-CSRFToken': csrfToken},
                cache: false,
                dataType: "JSON", 
                success: function(response){ 
                    console.log(response);
                    if(response.length !== 0){
                    for(let i=0; i < response.length; i++) {
                        
                        $('#data_type').append("<option value="+response[i].id+">"+response[i].name+"</option>");
                        //$('#data_selectType').removeAttr('hidden', true);
                    }
                    }else{
                        $('#data_type').append("<option value=''>Service currently unavailable</option>");
                    }
                },		
            });
        });

    }


    function data_fetchPlans(){
        $(document).on('change', '#data_type', function(){
            let network  = $('#data_network').val();
            let type  = $('#data_type').val();
            let csrfToken  = $("[name=csrfmiddlewaretoken]").val();
            if (type !== ""){
                $('#data_selectPlan').removeAttr('hidden', true);
            }else{
                $('#data_selectPlan').attr('hidden', 'hidden');
            }

           console.log(type)

            $('#data_plan').html("<option value=''>Please select</option>");
            $.ajax({ 
                type: "POST",
                url: "/user/data/plan/",  
                //data: JSON.stringify({network: network}),
                data: {network: network, type: type},
                headers : {'X-CSRFToken': csrfToken},
                cache: false,
                dataType: "JSON", 
                success: function(response){ 
                    //console.log(response);
                    if(response.dataplans.length !== 0){
                    for(let i=0; i < response.dataplans.length; i++) {
                        
                        $('#data_plan').append("<option value="+response.dataplans[i].id+">"+response.dataplans[i].plan+ ' - &#8358;' + response.dataplans[i].amount+"</option>");
                    }
                    }else{
                        $('#data_plan').append("<option value=''>Service currently unavailable</option>");
                    }
                },		
            });
        });

    }

    function buy_data(){
        $(document).on('click', '#data_submit', function(){
            let network = $("#data_network").val();
            let plan = $('#data_plan').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            let b_number = $('#data_b_number').val();
            let pin = $('#data_pin').val();
            

           
          
            if (b_number.length >= 11){
                $.ajax({
                    type : 'POST',
                    url: "/user/data/buy-data/",
                    data: {network:network, plan: plan, b_number:b_number, pin:pin},
                    headers : {'X-CSRFToken': csrftoken},
                    cache: false,
                    dataType: "JSON", 
                    success: function(response){
                        if(response !== "") {                                    
                            if(response.code == 200) {
                                window.location.href = "/user/transaction/detail/" + response.pk;
                            } else {
                                iziToast.error({
                                    title: 'Error',
                                    position: 'topRight', 
                                    message: response.error
                                    }); 
                                $('#data_submit').show();
                                $('#processing').attr('hidden', 'hidden');
                            }
                        } else{
                            iziToast.error({
                                title: 'Error',
                                position: 'topRight', // bottomRight, bottomLeft, topRight, topLeft, topCenter, bottomCenter
                                message: "Something went wrong"
                                });
                            $('#data_submit').show();
                            $('#processing').attr('hidden', 'hidden');
                        }
                        
                    },
                    beforeSend: function(){
                        $('#data_submit').hide();
                        $('#processing').removeAttr('hidden', true);
                    },
                    error :function(error){
                        //console.log('yuhbu');
                        
                    },
                });
            }else{
                iziToast.error({
                    title: 'Error',
                    position: 'topRight', 
                    message: 'Invalid Mobile Number'
                    });
            }

        });
    }

})



// AIRTIME

$(document).ready(function(){
    airtime_verify_number();
    airtime_fetch_type();
    airtime_amount();
    buy_airtime();
    airtime_showpin();


    function airtime_showpin(){
        $(document).on('input', '#airtime_amount', function(){
            let amount = $('#airtime_amount').val();
            if (amount !== ''){
                $('#airtime_pindiv').removeAttr('hidden', true);
            }else{
                $('#airtime_pindiv').removeAttr('hidden', 'hidden');
            }
        });
    }
        


    function airtime_verify_number(){
        $(document).on('input', '#airtime_b_number', function(){
            let b_number = $('#airtime_b_number').val();
            let network = $('#airtime_network').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();

            if (b_number.length >= 10){
                if (network !== null){
                    
                    $('#airtime_network_div').removeAttr('hidden', true);
                    $('#airtime_type_div').removeAttr('hidden', true);
                    $('#airtime_amount_div').removeAttr('hidden', true);
                } else{
                    
                    $('#airtime_network_div').attr('hidden', 'hidden');
                    $('#airtime_type_div').attr('hidden', 'hidden');
                    $('#airtime_amount_div').attr('hidden', 'hidden');
                }
            }
            //$('#network').html("<option value=''>Please select</option>");
            $('#airtime_type').html("<option value=''>Please select</option>");
            if (b_number.length >= 10){
                $.ajax({
                    type: 'POST',
                    url: "/user/verify-phone-no/",
                    data: {b_number:b_number},
                    headers : {'X-CSRFToken': csrftoken},
                    cache: false,
                    dataType: "JSON", 
                    success: function(response){
                        $('#airtime_network').val(response[0].network);
                        if(response.length !== 0){
                            for(let i=0; i < response.length; i++) {
                                
                                $('#airtime_type').append("<option value="+response[1][i].types+ ">"+  response[1][i].types+"</option>");                                
                                //console.log(response[i].default_price)
                            }
                               
                            } else {
                                $('#airtime_type').append("<option value=''>Service currently unavailable</option>");
                        }
                    },
                    error :function(response){},
                });
            };
        });
    }



    function airtime_fetch_type(){
        $(document).on('input', '#airtime_network', function(){
            let network = $('#airtime_network').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();

          
           
            $('#airtime_type').html("<option value=''>Please select</option>");
            if (network.length > 0){
                $.ajax({
                    type: 'POST',
                    url: "/user/airtime/type/",
                    data: {network:network},
                    headers : {'X-CSRFToken': csrftoken},
                    cache: false,
                    dataType: "JSON", 
                    success: function(response){
                        //$('#network').append("<option value="+response.network+">"+response.network+"</option>");
                        //$('#network').val(response.network);
                        if(response.length !== 0){
                            for(let i=0; i < response.length; i++) {
                                
                                $('#airtime_type').append("<option value="+response[i].types+ ">"+  response[i].types+"</option>");                                
                                //console.log(response[i].default_price)
                            }
                               
                            } else {
                                $('#airtime_type').append("<option value=''>Service currently unavailable</option>");
                        }
                    },
                    error :function(response){},
                });
            };
        });
    }


    
    function airtime_amount(){
        $(document).on('input', '#airtime_amount', function(){
            let amount = $('#airtime_amount').val();
            let network = $('#airtime_network').val();
            let type = $('#airtime_type').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();

            
           
            //$('#total_amount').html("<option value=''>Please select</option>");
            if (network.length > 0){
                if (amount >= 100){
                    if (type !== ''){
                        $.ajax({
                            type: 'POST',
                            url: "/user/airtime/amount/",
                            data: {amount:amount, network:network, type:type},
                            headers : {'X-CSRFToken': csrftoken},
                            cache: false,
                            dataType: "JSON",
                            success: function(response){
                                $('#airtime_total_amount').val(response.t_amount);
                                if (response.total_amount !== null){
                    
                                    $('#airtime_total_amount_div').removeAttr('hidden', true);
                                   
                                } else{
                                    
                                    $('#airtime_total_amount_div').attr('hidden', 'hidden');
                                  
                                }
                            },
                            error :function(response){},
                        });
     
                    }
                }
            };
        });
    }




    function buy_airtime(){
        $(document).on('click', '#airtime_submit', function(){
            let network = $('#airtime_network').val();
            let amount = $('#airtime_amount').val();
            let b_number = $('#airtime_b_number').val();
            let type = $('#airtime_type').val();
            let pin = $('#airtime_pin').val();

            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
           

            if (b_number.length >= 10){
                if (network !== ''){
                   if (type !== '' ){
                        if (amount >= 100){
                            $.ajax({
                                type: 'POST',
                                url: "/user/buy-airtime/",
                                data: {network:network, amount:amount, type:type, b_number:b_number, pin:pin},
                                headers : {'X-CSRFToken': csrftoken},
                                cache: false,
                                dataType: "JSON", 
                                success: function(response){
                                    if(response !== "") {                                    
                                        if(response.code == 200) {
                                            window.location.href = "/user/transaction/detail/" + response.pk;
                                        } else {
                                            iziToast.error({
                                                title: 'Error',
                                                position: 'topRight', 
                                                message: response.error
                                                }); 
                                            $('#airtime_submit').show();
                                            $('#processing').attr('hidden', 'hidden');
                                        }
                                    } else{
                                        iziToast.error({
                                            title: 'Error',
                                            position: 'topRight', // bottomRight, bottomLeft, topRight, topLeft, topCenter, bottomCenter
                                            message: "Something went wrong"
                                            });
                                        $('#airtime_submit').show();
                                        $('#processing').attr('hidden', 'hidden');
                                    }
                                    
                                },
                                beforeSend: function(){
                                    $('#airtime_submit').hide();
                                    $('#processing').removeAttr('hidden', true);
                                },
                                error :function(response){},
                            });
                        }else{
                            iziToast.error({
                                title: 'Error',
                                position: 'topRight', 
                                message: 'Please Enter A Valid Amount'
                                });
                        }
                   }else{
                    iziToast.error({
                        title: 'Error',
                        position: 'topRight', 
                        message: 'Type Cannot Be Empty'
                        });
                   }
                }else{
                    iziToast.error({
                        title: 'Error',
                        position: 'topRight', 
                        message: 'Please Select Network'
                        });
                }
            }else{
                iziToast.error({
                    title: 'Error',
                    position: 'topRight', 
                    message: 'Invalid Mobile Number'
                    });
            }

        });
    }
});



// BILL

$(document).ready(function(){

    disco_buyDisco();
    disco_fetch();
    disco_showpin();


    function disco_showpin(){
        $(document).on('input', '#disco_b_number', function(){
            let b_number = $('#disco_b_number').val();
            if (b_number !== ''){
                $('#disco_pindiv').removeAttr('hidden', true);
            }else{
                $('#disco_pindiv').removeAttr('hidden', 'hidden');
            }
        });
    }


    function disco_fetch(){
        $(document).on('change', '#disco_disco', function(){
           let disco = $('#disco_disco').val();
           
            if (disco !== ""){
               $('#disco_meterNo').removeAttr('hidden', true);
               $('#disco_discoAmount').removeAttr('hidden', true);
               $('#disco_phoneNo').removeAttr('hidden', true);
            }else{
                $('#disco_meterNo').attr('hidden', 'hidden');
                $('#disco_discoAmount').attr('hidden', 'hidden');
                $('#disco_phoneNo').attr('hidden', 'hidden');
            }
        });
    } 


    function disco_buyDisco(){
        $(document).on('click', '#disco_submit', function(){
            let disco = $('#disco_disco').val();
            let meter = $('#disco_meter').val();
            let amount = $('#disco_amount').val();
            let b_number = $('#disco_b_number').val();
            let pin = $('#disco_pin').val();
            let type = $('#disco_type').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            
            //console.log(disco);
            //console.log(meter);
            //console.log(amount);
            //console.log(b_number);

            if (disco !== ''){
                if (meter !== ''){
                    if (amount >= 1000){
                        if (b_number.length >= 11){
                            $.ajax({
                                type: 'POST',
                                url: "/user/buy-electricity/",
                                data: {disco:disco, meter:meter, amount:amount, b_number:b_number, type:type, pin:pin},
                                headers : {'X-CSRFToken': csrftoken},
                                cache: false,
                                dataType: "JSON", 
                                success: function(response){
                                    if(response !== "") {                                    
                                        if(response.code == 200) {
                                            window.location.href = "/user/transaction/detail/" + response.pk;
                                        } else {
                                            iziToast.error({
                                                title: 'Error',
                                                position: 'topRight', 
                                                message: response.error
                                                }); 
                                            $('#disco_submit').show();
                                            $('#processing').attr('hidden', 'hidden');
                                        }
                                    } else{
                                        iziToast.error({
                                            title: 'Error',
                                            position: 'topRight', 
                                            message: "Something went wrong"
                                            });
                                        $('#disco_submit').show();
                                        $('#processing').attr('hidden', 'hidden');
                                    }
                                    
                                },
                                beforeSend: function(){
                                    $('#disco_submit').hide();
                                    $('#processing').removeAttr('hidden', true);
                                },
                                error :function(response){},
                            });
                        }else{
                            iziToast.error({
                                title: 'Error',
                                position: 'topRight', 
                                message: 'Invalid Mobile Number'
                                });
                        }
                    }else{
                        iziToast.error({
                            title: 'Error',
                            position: 'topRight', 
                            message: 'Amount Must Be A Minimum Of 1000 Naira'
                            });
                    }
                }else{
                    iziToast.error({
                        title: 'Error',
                        position: 'topRight', 
                        message: 'Meter Number Cannot Be Empty'
                        });
                }
            }else{
                iziToast.error({
                    title: 'Error',
                    position: 'topRight', 
                    message: 'Please Select A Disco'
                    });
            }

        });
    }
});


// CABLE

$(document).ready(function(){
    cable_fetchPlans();
    cable_buyCable();
    cable_verifyDecoder();
    cable_changePlan();
    cable_showpin();


    function cable_showpin(){
        $(document).on('input', '#cable_b_number', function(){
            let b_number = $('#cable_b_number').val();
            if (b_number !== ''){
                $('#cable_pindiv').removeAttr('hidden', true);
            }else{
                $('#cable_pindiv').removeAttr('hidden', 'hidden');
            }
        });
    }
   

    function cable_verifyDecoder() {

        $(document).on('input', '#cable_card_no', function(){
            let card_no =$('#cable_card_no').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            let cable = $('#cable_decoder').val();
            
            if (card_no !== null){
                
                $('#cable_customerName_div').removeAttr('hidden', true);
                $('#cable_customerNumber').removeAttr('hidden', true);
            } else{
                
                $('#cable_customerName_div').attr('hidden', 'hidden');
                $('#cable_customerNumber').attr('hidden', 'hidden');
            }


            if (card_no.length >= 10) {

            $('#cable_b_name').html(' <input value=""/>')
            $.ajax({
                type : 'POST',
                url: "/user/cable/verify-cable/",
                data: {cable: cable, card_no:card_no},
                headers : {'X-CSRFToken': csrftoken},
                cache: false,
                dataType: "JSON", 
                success: function(response){
                    if (response.customerName !== null){ 
                        $('#cable_b_name').val(response.customerName);
                    //console.log(response.customerName)
                    }else{
                        $('#cable_b_name').val("Invalid number, please correct and retry");
                    }

                },
                
            });
        };
        });

    }


    function cable_buyCable() {

        $(document).on('click', '#cable_submit', function(){
            let decoder = $("#cable_decoder").val();
            let plan = $('#cable_plan').val();
            let amount = $('#cable_plan').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            let card_no = $('#cable_card_no').val();
            let b_name = $('#cable_b_name').val();
            let pin = $('#cable_pin').val();
            let b_number = $('#cable_b_number').val();
        

            $.ajax({
                type : 'POST',
                url: "/user/cable/buy-cable/",
                data: {decoder: decoder, plan: plan, card_no:card_no, b_number:b_number, b_name:b_name, pin:pin},
                headers : {'X-CSRFToken': csrftoken},
                cache: false,
                dataType: "JSON", 
                success: function(response){
                    if(response !== "") {                                    
                        if(response.code == 200) {
                            window.location.href = "/user/transaction/detail/" + response.pk;
                        } else {
                            iziToast.error({
                                title: 'Error',
                                position: 'topRight', 
                                message: response.error
                                }); 
                            $('#cable_submit').show();
                            $('#processing').attr('hidden', 'hidden');
                        }
                    } else{
                        iziToast.error({
                            title: 'Error',
                            position: 'topRight', 
                            message: "Something went wrong"
                            });
                        $('#cable_submit').show();
                        $('#processing').attr('hidden', 'hidden');
                    }
                    
                },
                beforeSend: function(){
                    $('#cable_submit').hide();
                    $('#processing').removeAttr('hidden', true);
                },
                error :function(response){
                },
            });


        });

    }

    function cable_changePlan(){
        $(document).on('change', '#cable_plan', function(){
            let plan = $("#plan").val();
            if (plan !== "") {
                $('#cable_iucNumber').removeAttr('hidden', true);
            } else {
                $('#cable_iucNumber').attr('hidden', 'hidden');
            }
        });
    }



    function cable_fetchPlans() {
        $(document).on('change', '#cable_decoder', function(){
            let decoder = $('#cable_decoder').val();
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            if (decoder !== ""){
                $('#cable_selectPlan_id').removeAttr('hidden', true);
            }else{
                $('#cable_selectPlan_id').attr('hidden', 'hidden');
            }

            $('#cable_plan').html("<option value=''>Please select</option>");
            $.ajax({
                type : 'POST',
                url: "/user/cable/plan/",
                data: {decoder: decoder},
                headers : {'X-CSRFToken': csrftoken},
                cache: false,
                dataType: "JSON", 
                success: function(response){ 
                        if(response.cableplans.length !== 0){
                        for(let i=0; i < response.cableplans.length; i++) {
                            
                            $('#cable_plan').append("<option value="+response.cableplans[i].id+ ">"+response.cableplans[i].plan+ ' - &#8358;' + response.cableplans[i].amount+"</option>");                                
                            // console.log(response.cableplans[i].end_user_price)
                        }
                        
                        } else {
                            $('#cable_plan').append("<option value=''>Service currently unavailable</option>");
                        }
                    },		
            });

        
        });
    }
});
