$(function(){
    var $hint = $('#hint');  // 获取提示框
    var csrf = $('input[name=csrfmiddlewaretoken]').val();  // 获取csrf的值

    $('#btn').click(function(){  // 登录点击事件
        username = $('#username').val();
        password = $('#password').val();
        password = pidCrypt.SHA256(password);
        console.log(password);
        $.post('/login_check/', {'username':username,'password':password,'csrfmiddlewaretoken':csrf},function(data){
            // {'res': 结果 }  0不通过，1通过，2验证码错误
            if(data.res=='1'){
                location.href = '/index/'
            }
            else if(data.res=='2'){
                $hint.text('验证码错误').show();
            }
            else{
                $hint.text('帐号或密码不正确').show();
            }
        })
    });  // 登录点击事件


});