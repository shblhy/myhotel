	$(function() {
			//window.functions=functions;
			//functions.base.load_anchor();
			// //functions.base.set_all_aclick();
			// function addFavorite2() {
			    // var url = window.location;
			    // var title = document.title;
			    // var ua = navigator.userAgent.toLowerCase();
			    // if (ua.indexOf("360se") > -1) {
			        // alert("由于360浏览器功能限制，请按 Ctrl+D 手动收藏！");
			    // }
			    // else if (ua.indexOf("msie 8") > -1) {
			        // window.external.AddToFavoritesBar(url, title); //IE8
			    // }
			    // else if (document.all) {
			  // try{
			   // window.external.addFavorite(url, title);
			  // }catch(e){
			   // alert('您的浏览器不支持,请按 Ctrl+D 手动收藏!');
			  // }
			    // }
			    // else if (window.sidebar) {
			        // window.sidebar.addPanel(title, url, "");
			    // }
			    // else {
			  // alert('您的浏览器不支持,请按 Ctrl+D 手动收藏!');
			    // }
			// }
			$('#show-login-btn').click(function(){
                //alert("展示登录框");
                $("#pop-login-content").css({
                	'top': 100,
                	'left': 350,
                });
                $("#pop-login-content").show();
            });
			function show_loginon_label(username,backend){
				$("#pop-login-content").hide();
				$("#member-entrance").html("<label><a href='/member/center'>"+username+"</label>");
				if (backend){
					$("#member-entrance").append("|<label><a href='/admin'>后台</a></label>");
				}
				$("#member-entrance").append("|<label><a href='/member/logout'>注销</a></label>");
			}
			$('#login-submit-btn').click(function(){
				$("#pop-login-form1").ajaxForm({
					data : {},
					dataType : "json",
					success: function(data) {
						show_loginon_label(data.username,data.backend);
					},
					error: function(data){
                   		alert(data.responseText);
                   	}
				}).submit();
			});
			$('.login-cancel-btn').click(function(){
                $("#pop-login-content").hide();
            });
            $('.regist-cancel-btn').click(function(){
                $("#pop-regist-content").hide();
            });
			$('#show-regist-btn').click(function(){
                //alert("展示注册框");
                $("#pop-regist-content").css({
                	'top': 100,
                	'left': 350,
                });
                $("#pop-regist-content").show();
            });

			$('#regist-submit-btn').click(function(){
				if ($("#pop-regist-repeat-password").val()!=$("#pop-regist-password").val()){
					alert("两次输入的密码必须一致！")
					return false;
				}
				$("#pop-regist-form1").ajaxForm({
					data : {},
					dataType : "json",
					success: function(data) {
						alert("注册成功，请登录");
						window.location=location;
                   },
                   	error: function(data){
                   		alert(data.responseText);
                   	}
                }).submit();
			});
		});