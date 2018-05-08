$(function(){
    $('#login').click(function(e) {
        var username = $('#login_username').val();
        var password = $('#login_password').val();
        console.log(username + " " + password);
        
        $.ajax({
            'url': '/ajax/verifyUser',
            'data': { 'username': username, 'password': password},
            'dataType': 'json',
            'success' : function(data) {
                if (data.success){
                    // $.cookie("RRID",data.data.UserID,{expires : 1});
                    document.cookie = "RRID="+data.data.UserID+";";
                    document.cookie = "RRName="+data.data.UserDisplayName+";";
                    window.location.reload();
                }else{
                    $('#error').html(data.error);    
                    $('#error').show();
                }
            }

        });
        
    });
});
