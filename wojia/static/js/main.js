$(function(){  
    $(".form_datetime").datetimepicker({  // 日期控件用
    format: "yyyy-mm-dd",
    autoclose: true,
    todayBtn: true,
    todayHighlight: true,
    showMeridian: true,
    pickerPosition: "bottom-left",
    language: 'zh-CN',//中文，需要引用zh-CN.js包
    startView: 2,//月视图
    minView: 2//日期时间选择器所能够提供的最精确的时间选择视图
    }); 

    // 获取窗口的宽度
    var iNum = $(document).width(),
    $li = $('.wid li'),
    $btn = $('.margin_top button');  // 获取中间的button按钮
    var csrf = $('input[name=csrfmiddlewaretoken]').val();  // 获取csrf的值

    // 窗口的宽/2给顶部的2个导航条
    $li.css('width',iNum/2-10);

    $(window).scroll(function(){  // 窗口滚动的时候要重新调整尺寸;
        iNum = $(window).width();
        $li.css('width',iNum/2-1);
    });

    $('.filter').click(function(){  // 筛选内容
        $('.margin_top').slideToggle();  // 切换收起或展开
        $content = $('.filter').children().children();  // 获取文本内容
        if($content.text()=='点此展开筛选框'){$content.text('点此收起筛选框')}
        else($content.text('点此展开筛选框'));
    });  // 切换展示内容

    $btn.click(function(){  // 对btn按钮设置点击事件
        $input = $(this).parent().parent().children('input');  // 获取旁边的input按钮
        if($input.prop('disabled')){$input.removeAttr('disabled')}  // 如果是禁用状态，就移除
        else{$input.attr("disabled",true)}  // 否则就禁用
    });  // btn按钮点击事件

    var $head = $('.header');  // 获取主要内容页
    $li.click(function(){  // 标签页的点击事件
        $(this).addClass('active').siblings().removeClass('active');
        iIndex = $(this).index();  // 获取下标
        $head.eq(iIndex).siblings('.header').fadeOut(function(){
        $head.eq(iIndex).fadeIn();
        });  // 自己出现，其他隐藏
    });  // 标签页的点击事件


    $('#add_new').click(function(){  // 绑定添加事件
        $success = $('.add .success');
        $danger = $('.add .danger');
        new_date = $('#new_date').val();  // 读取日期,字符串
        new_con = $('#new_content').val();  // 读取内容
        new_ps = $('#new_ps').val();  // 读取备注
        new_mon = $('#new_money').val();  // 读取金额
        aDict = {
            'date':new_date,
            'content':new_con,
            'ps':new_ps,
            'money':new_mon,
            'csrfmiddlewaretoken':csrf
        };  // 定义要传送数据的字典
        $.post('/add_new/',aDict, function(data){
            // {'res': 结果} 0为不成功，1为成功
            if(data.res=='1'){
                $success.fadeIn(function(){
                    $success.fadeOut(5000);
                })
            }  // 出现成功提示，5秒后消失
            else{
                $danger.fadeIn(function(){
                    $danger.fadeOut(5000);
                })
            }  // 出现失败提示，5秒后消失
        });  // ajax的括号
    });  // 添加事件的括号


    $('#find_all').click(function(){  // 查询所有的点击事件
        $.get('/find_all/',function(data){
            // {'res':数组,'sum':和} [[date,content,ps,money], ...]
            $('#find_body').html('');  // 清空内容
            aList = data.res;  // 获取返回结果
            for(var i=0;i<aList.length;i++){
                var $res = $('<div class="row content_body"><div class="col-xs-3">'+aList[i][0]+'</div><div class="col-xs-3">'+aList[i][1]+'</div><div class="col-xs-3">'+aList[i][2]+'</div><div class="col-xs-3">'+aList[i][3]+'</div></div>');
                console.log($res);
                $('#find_body').append($res);  // 插入数据
            }  // 循环读出数据
            $('#sum_money').text(data.sum);  // 总和加上
            $('.margin_top').slideUp();  // 收起
        })


    })
            

});
