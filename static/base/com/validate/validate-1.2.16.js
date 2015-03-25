/**
 * error 主动提示的错误信息
 * errorinfo 非主动提示的错误信息
 * 
 * 
 * 
 * 
 * 
 * [description]
 * @param  {[type]} $         [description]
 * @param  {[type]} undefined [description]
 * @return {[type]}           [description]
 *
 *
 */
;(function($, undefined) {
	var Validate = function(el, option, errors, optionstring) {
		var _this = this, defaults = {
			errorInfoClass : 'errorInfo',
			errorContainerClass : 'errorContainer'
		};
		_this.option = $.extend(defaults, option);
		_this.$el = $(el);
		_this.options = _this.parseOptions(optionstring);

		//校验
		_this.check(errors);

	};

	Validate.prototype = {
		constructor : Validate,
		check : function(errors) {
			var _this = this, $el = _this.$el, option = _this.option, options = _this.options;

			//禁用
			if(typeof $el.attr('disabled') !== 'undefined')
				return errors;

			_this.errors = errors;

			//清空空格
			$el.val($.trim($el.val()));

			var type = options.type, required = false;
			_this.elerror = false;

			if (options.required == undefined)
				options.required = false;

			if (options.required == 'true') {
				if ($el.val() == '') {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'required'
					});
				}
				required = true;
			}

			// Check if we really have to go through all validation checks:

			if ((required || $el.val() != '') || options.type == 'group') {

				// Is this a valid email?
				if (options.type == 'email' && !$.fn.validate_emailCheck.call($el, $el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'email'
					});
				}

				// Is this a valid url (http:// or https://)?
				if (options.type == 'url' && !$.fn.validate_urlCheck.call($el, $el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'url'
					});
				}

				// Is this a valid date?
				if (options.type == 'date' && !$.fn.validate_dateCheck.call($el, $el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'date'
					});
				}

				// Is this date older than some other date?
				if (options.type == 'date' && (new Date($el.val()).getTime() <= new Date($(options.older).val()).getTime())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'older'
					});
				}

				// Is this date younger than some other date?
				if (options.type == 'date' && (new Date($el.val()).getTime() >= new Date($(options.younger).val()).getTime())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'younger'
					});
				}

				// Is this a valid time?
				if (options.type == 'time' && !$.fn.validate_timeCheck.call($el, $el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'time'
					});
				}

				// Is this a valid phone number?
				if (options.type == 'phone' && !$.fn.validate_phoneCheck.call($el, $el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'phone'
					});
				}

				// Is this a float?
				if (options.type == 'float' && isNaN($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'float'
					});
				}

				// Is this a int?
				if (options.type == 'int' && parseInt($el.val()) != $el.val()) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'int'
					});
				}

				// min (numeric)?
				if ((options.type == 'int' || options.type == 'float') && options.min != undefined && parseFloat($el.val()) < options.min && options.type != 'group') {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'min'
					});
				}

				// max (numeric)?
				if ((options.type == 'int' || options.type == 'float') && options.max != undefined && parseFloat($el.val()) > options.max && options.type != 'group') {

					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'max'
					});
				}

				// Is this bigger than x (numeric)?
				if ((options.type == 'int' || options.type == 'float') && options.bigger != undefined && parseFloat($el.val()) > $(options.bigger).val()) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'bigger'
					});
				}

				// Is this smaller than x (numeric)?
				if ((options.type == 'int' || options.type == 'float') && options.smaller != undefined && parseFloat($el.val()) < $(options.smaller).val()) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'smaller'
					});
				}

				// min (length)?
				if ((options.type != 'int' && options.type != 'float') && options.min != undefined && $el.val().length < options.min && options.type != 'group') {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'minlength'
					});
				}

				// max (length)?
				if ((options.type != 'int' && options.type != 'float') && options.max != undefined && $el.val().length > options.max && options.type != 'group') {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'maxlength'
					});
				}

				// Is the length of the entered string exactly the specified value?
				if (options.length != undefined && $el.val().length != options.length) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'length'
					});
				}

				// Is this longer than x (length)?
				if ((options.type != 'int' && options.type != 'float') && options.longer != undefined && $el.val().length > $(options.longer).val().length) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'longer'
					});
				}

				// Is this shorter than x (length)?
				if ((options.type != 'int' && options.type != 'float') && options.shorter != undefined && $el.val().length < $(options.shorter).val().length) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'shorter'
					});
				}

				//****** loginUsername
				if (options.type == 'loginUsername' && !$.fn.validate_loginUsername($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'loginUsername'
					});
				}
				//****** username
				if (options.type == 'username' && !$.fn.validate_usernameCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'username'
					});
				}
				//****** monitorname
				if (options.type == 'monitorname' && !$.fn.validate_monitornameCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'monitorname'
					});
				}

				//****** iphostname
				if (options.type == 'iphostname' && !$.fn.validate_iphostnameCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'iphostname'
					});
				}

				//****** ip
				if (options.type == 'ip' && !$.fn.validate_ipCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'ip'
					});
				}

				//****** taskplanname
				if (options.type == 'taskplanname' && !$.fn.validate_taskplannameCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'taskplanname'
					});
				}
				
				//****** communityname
				if (options.type == 'communityname' && !$.fn.validate_communitynameCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'communityname'
					});
				}

				//****** hostname
				if (options.type == 'hostname' && !$.fn.validate_hostnameCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'hostname'
					});
				}

				//****** realname
				if (options.type == 'realname' && !$.fn.validate_realnameCheck($el.val())) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'realname'
					});
				}

				// Check password strength (0=bad, 100=perfect)?
				if (options.strength != undefined && $.fn.validate_passwordStrength.call($el, $el.val()) < options.strength) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'strength'
					});
				}

				// Is this the same as x?
				if (options.same != undefined && $el.val() != $(options.same).val()) {
					_this.elerror = true;
					errors.push({
						'element' : $el,
						'info' : options.errorinfo || '',
						'type' : 'same'
					});
				}else if(options.same != undefined){
					var $validation = $(options.same).data('validation');
					if($validation && $validation && $validation.elerror)
						$validation['check']([]);
				}

				/*
				// Is this different as x?
				if (options.different != undefined){
					$.grep($(options.different), function(element, index){
						//排除options.different与$el是同一个元素
						if($el[0] != element){							
							if ($el.val() == $(element).val()) {
								_this.elerror = true;
								errors.push({
									'element' : $el,
									'info' : options.errorinfo || '',
									'type' : 'different'
								});
							}else{
								var $validation = $(element).data('validation');
								if($validation && $validation && $validation.elerror)
									$validation['check']([]);
							}
						}
					});		
				}
				*/
				// Is this different as x?
				if (options.different != undefined){
					var different = parseInt($(options.different).val()),$validation = $(options.different).data('validation'), checkOther = false;
					//若比较对象有 different 的错误类型，触发比较对象的校验
					if($validation && $validation.elerror){
						for(var i=0,l=$validation.errors.length;i<l;i++){
							if($validation.errors[i].type == 'different'){
								checkOther = true;
								break;
							}
						}
					}			
					if($el.val() >= different) {//若校验不通过，则增加错误
						_this.elerror = true;
						errors.push({
							'element' : $el,
							'info' : options.errorinfo || '',
							'type' : 'different'
						});
					}else if(checkOther){
						$validation['check']([]);
					}
				}

				if (options.smallerthan != undefined){
					var smallerthan = parseInt($(options.smallerthan).val());
					if(smallerthan >= 0 || smallerthan < 0 || smallerthan === 0 ){
						var $validation = $(options.smallerthan).data('validation'), checkOther = false;
						//若比较对象有与之相反 biggerthan 的错误类型，触发比较对象的校验
						if($validation && $validation.elerror){
							for(var i=0,l=$validation.errors.length;i<l;i++){
								if($validation.errors[i].type == 'biggerthan'){
									checkOther = true;
									break;
								}
							}
						}			
						if($el.val() >= smallerthan) {//若校验不通过，则增加错误
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'smallerthan'
							});
						}else if(checkOther){
							$validation['check']([]);
						}
					}
				}

				if (options.biggerthan != undefined){
					var biggerthan = parseInt($(options.biggerthan).val());
					if(biggerthan >= 0 || biggerthan < 0 || biggerthan === 0 ){
						var $validation = $(options.biggerthan).data('validation'), checkOther = false;
						//若比较对象有与之相反 smallerthan 的错误类型，触发比较对象的校验
						if($validation && $validation.elerror){
							for(var i=0,l=$validation.errors.length;i<l;i++){
								if($validation.errors[i].type == 'smallerthan'){
									checkOther = true;
									break;
								}
							}
						}						
						if($el.val() <= biggerthan) {//若校验不通过，则增加错误
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'biggerthan'
							});
						}else if(checkOther){
							$validation['check']([]);
						}
					}
				}

				if (options.unsmallerthan != undefined){
					var unsmallerthan = parseInt($(options.unsmallerthan).val());
					if(unsmallerthan >= 0 || unsmallerthan < 0 || unsmallerthan === 0 ){
						var $validation = $(options.unsmallerthan).data('validation'), checkOther = false;
						//若比较对象有与之相反 unsmallerthan 的错误类型，触发比较对象的校验
						if($validation && $validation.elerror){
							for(var i=0,l=$validation.errors.length;i<l;i++){
								if($validation.errors[i].type == 'unbiggerthan'){
									checkOther = true;
									break;
								}
							}
						}						
						if($el.val() < unsmallerthan) {//若校验不通过，则增加错误
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'unsmallerthan'
							});
						}else if(checkOther){
							$validation['check']([]);
						}
					}
				}

				if (options.unbiggerthan != undefined){
					var unbiggerthan = parseInt($(options.unbiggerthan).val());
					if(unbiggerthan >= 0 || unbiggerthan < 0 || unbiggerthan === 0 ){
						var $validation = $(options.unbiggerthan).data('validation'), checkOther = false;
						//若比较对象有与之相反unsmallerthan的错误类型，触发比较对象的校验
						if($validation && $validation.elerror){
							for(var i=0,l=$validation.errors.length;i<l;i++){
								if($validation.errors[i].type == 'unsmallerthan'){
									checkOther = true;
									break;
								}
							}
						}						
						if($el.val() > unbiggerthan) {//若校验不通过，则增加错误
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'unbiggerthan'
							});
						}else if(checkOther){
							$validation['check']([]);
						}
					}
				}

				// Has this file the correct extension?
				if (options.type == 'extension') {
					var opts = options.options.split(s.delimiter);
					var filesplit = $el.val().split('.');
					var ext = filesplit[filesplit.length - 1];
					if ($.inArray(ext, opts) == -1) {
						_this.elerror = true;
						errors.push({
							'element' : $el,
							'info' : options.errorinfo || '',
							'type' : 'ext'
						});
					}
				}

				// Is the correct amount of elements checked in this group?
				if (options.type == 'group') {
					if (options.min != undefined || options.max != undefined) {
						var checked = 0;
						$el.children('input[type=checkbox][checked]').each(function() {
							checked++;
						});
						if ((options.min != undefined && options.min > checked) || (options.max != undefined && checked > options.max)) {
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'group'
							});
						}
					} else {
						if ($el.find("input[name='" + options.name + "']:checked").val() == undefined) {
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'group'
							});
						}
					}
				}

				// Call a custom function that checks this field:
				if (options.type == 'custom' && options.customfn != undefined) {
					var fn = $.fn[options.customfn];
					if ( typeof fn === 'function') {
						var checkResult = fn.call(_this, $el, $el.val());
						if ( checkResult != true ) {
							options.errorInfoContainer = checkResult;
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'custom'
							});
						}
					} else {
						alert('未定义customfn');
					}
				}
				// 正则校验
				if (options.type == 'regex' && $el.attr('data-regex') != undefined) {
					var regex = $el.attr('data-regex');
					if ( regex ) {
                        var exp = new RegExp("^(" + regex + ")$");
                        var isvalid = exp.test($el.val());
						if ( !isvalid ) {
							_this.elerror = true;
							errors.push({
								'element' : $el,
								'info' : options.errorinfo || '',
								'type' : 'regex'
							});
						}
					} else {
						alert('未定义data-regex');
					}
				}

			};

			//清空错误提示
			if(options.tipped && options.tipped == 'true'){
				Tipped.remove($el);
			}else{
				$el.next('span.' + option.errorInfoClass).remove();
			}
			$el.removeClass(option.errorContainerClass);

			// Display and error if anything didn't validate correctly:

			if(typeof options.errorInfoContainer == 'boolean' || !options.errorInfoContainer)
				options.errorInfoContainer = $el;
			if (_this.elerror) {
				if (options.error) {
					if(options.tipped && options.tipped == 'true') {
						Tipped.create(options.errorInfoContainer, options.error, {
							skin : 'red',
							hook : 'topmiddle',
							hideOn : false
						}).show();
					}else if(options.title && options.title == 'true') {
						options.errorInfoContainer.attr('title', options.error);
					} else {
						$el.after('<span class="' + option.errorInfoClass + '">' + options.error + '</span>');
					};
				}
				$el.addClass(option.errorContainerClass);
			}else{//清除之前错误信息
				if(options.title && options.title == 'true')
					options.errorInfoContainer.attr('title', '');
			}

			return errors;

		},
		parseOptions : function(string) {

			var relsplit = string.split(':');
			var commandsplit = relsplit[0].split('.');

			var options = {
				'type' : $.trim(commandsplit[0])
			};

			if (commandsplit[1] !== undefined) {
				options['commandkey'] = commandsplit[1];
			}

			if (options.execute == undefined) {
				options.execute = 'always';
			}

			if (relsplit.length > 1) {
				var optionssplit = relsplit[1].split(';');

				$.each(optionssplit, function(key, value) {
					var optionssplit2 = value.split('=');
					options[$.trim(optionssplit2[0])] = $.trim(optionssplit2[1]);
				});
			}

			return options;

		}
	};

	// ### validate_emailCheck
	//
	// The **validate_emailCheck** plugin function is used by the validation command to check if an
	// email address is valid.

	$.fn.validate_emailCheck = function(string) {
		var filter = /^[a-z0-9\._-]+@([a-z0-9_-]+\.)+[a-z]{2,6}$/i;
		return filter.test(string);
	};

	// ### validate_urlCheck
	//
	// The **validate_urlCheck** plugin function is used by the validation command to check if an
	// url is valid.

	$.fn.validate_urlCheck = function(string) {
		var filter = /^(?:(ftp|http|https):\/\/)?(?:[\w\-]+\.)+[a-z]{2,6}$/i;
		return filter.test(string);
	};

	// ### validate_dateCheck
	//
	// The **validate_dateCheck** plugin function is used by the validation command to check if the
	// date string is valid.

	$.fn.validate_dateCheck = function(string) {

		return $.fn.validate_regexTests(string, [/^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$/i, // 01.01.12
		/^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2}$/i, // 1.1.12
		/^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}$/i, // 1.1.2012
		/^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$/i, // 01.01.2012
		/^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$/i, // 2012-01-01
		/^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$/i // 01/01/2012
		]);

	};

	// ### validate_timeCheck
	//
	// The **validate_timeCheck** plugin function is used by the validation command to check if the
	// time string is valid.

	$.fn.validate_timeCheck = function(string) {

		return $.fn.validate_regexTests(string, [/^[0-9]{1,2}\:[0-9]{2}$/i, // 1:59
		/^[0-9]{1,2}\:[0-9]{2}\:[0-9]{2}$/i // 1:59:59
		]);

	};

	// ### validate_phoneCheck
	//
	// The **validate_phoneCheck** plugin function is used by the validation command to check if the
	// phone string is valid.

	$.fn.validate_phoneCheck = function(string) {

		return $.fn.validate_regexTests(string, [/^(\+|0)([\d ])+(0|\(0\))+[\d ]+(-\d*)?\d$/, // +41 (0)76 123 45 67
		/^(\+|0)[\d ]+(-\d*)?\d$/, // +41 142-124-23
		/^((((\(\d{3}\))|(\d{3}-))\d{3}-\d{4})|(\+?\d{2}((-| )\d{1,8}){1,5}))(( x| ext)\d{1,5}){0,1}$/ // NAND and int formats
		]);

	};

	// ### validate_passwordStrength
	//
	// The **validate_passwordStrength** plugin function is used by the validation command to check if the
	// password strength is good enough. The function calculates a score from 0 to 100 based on various
	// checks.

	$.fn.validate_passwordStrength = function(passwd) {
		var intScore = 0

		if (passwd.length < 5) {
			intScore = intScore + 5;
		} else if (passwd.length > 4 && passwd.length < 8) {
			intScore = intScore + 15;
		} else if (passwd.length >= 8) {
			intScore = intScore + 30;
		}

		if (passwd.match(/[a-z]/))
			intScore = intScore + 5;
		if (passwd.match(/[A-Z]/))
			intScore = intScore + 10;
		if (passwd.match(/\d+/))
			intScore = intScore + 10;
		if (passwd.match(/(.*[0-9].*[0-9].*[0-9])/))
			intScore = intScore + 10;
		if (passwd.match(/.[!,@,#,$,%,^,&,*,?,_,~]/))
			intScore = intScore + 10;
		if (passwd.match(/(.*[!,@,#,$,%,^,&,*,?,_,~].*[!,@,#,$,%,^,&,*,?,_,~])/))
			intScore = intScore + 10;
		if (passwd.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/))
			intScore = intScore + 5;
		if (passwd.match(/([a-zA-Z])/) && passwd.match(/([0-9])/))
			intScore = intScore + 5;
		if (passwd.match(/([a-zA-Z0-9].*[!,@,#,$,%,^,&,*,?,_,~])|([!,@,#,$,%,^,&,*,?,_,~].*[a-zA-Z0-9])/))
			intScore = intScore + 5;

		return intScore;
	};

	// ### validate_regexTests
	//
	// The **validate_regexTests** plugin function is mainly used by the validation commands to test for different patterns.
	// The first argument is the string to test, the second contains an array of all patterns to test and the third is a boolean that can be set to true if
	// all patterns need to be found.

	$.fn.validate_regexTests = function(string, tests, checkall) {

		if (checkall === undefined)
			checkall = false;

		var matches = 0;

		for (var x in tests) {
			if (tests[x].test(string))
				matches++;
		}

		return (checkall && matches == tests.length) || (!checkall && matches > 0);

	};

	/***扩展校验规则**/

	// ### jKit_loginUsername
	$.fn.validate_loginUsername = function(string){
		var string = $.trim(string);
		if(string == '用户名'){
			return false;
		}else{
			var filter = /^[a-zA-Z0-9_\u4e00-\u9fa5]{1,30}$/i;
			return filter.test(string);
		}
	};
	// ### ip或url
	
	$.fn.validate_iphostnameCheck = function(string){
		//校验规则 http:// (可有可无) www.baidu.com|117.27.151.138:8899 (www与:8899可有可无) /login.jsp (不为空格)
        var url_filter = /^([a-zA-Z]+\:\/\/)?((((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))(:[0-9]{0,})?)|(www.|[a-zA-Z].)?[a-zA-Z0-9\-\.]+[^\.]\.(com|net|org|hk|cn|com.cn|net.cn|org.cn|gov.cn|biz|info|cc|tv|mobi|name|asia|tw|sh|ac|io|tm|travel|ws|us|sc|mn|ag|vc|la|bz|in|cm|co|tel|me|pro|com.hk|com.tw|pw))[^ ]*$/i;
        if(url_filter.test(string)){
			return true;
        }
	};

	// ### ip地址
	
	$.fn.validate_ipCheck = function(string){
		var filter = /^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$/i;
		return filter.test(string);
	};

	// ### 计划名称不为特殊字符，不超16个字
	
	$.fn.validate_taskplannameCheck = function(string){
		var filter = /^([^\^<>%_&',;=?$"':#@!~\]\[{}\/\`\|]){1,16}$/i;
		return filter.test(string);
	};
	
	$.fn.validate_communitynameCheck = function(string){
		var filter = /^([^\^<>%_&',;=?$"':#@!~\]\[{}\/\`\|]){1,32}$/i;
		return filter.test(string);
	};
	
	// ### jKit_hostnameCheck
	
	$.fn.validate_hostnameCheck = function(string){
		var filter = /^[a-zA-Z0-9-]{1,30}$/i;
		return filter.test(string);
	};


	// ### realname
	
	$.fn.validate_realnameCheck = function(string){
		var string = $.trim(string);
		var filter = /^[\u4E00-\uFA29\uE7C7-\uE7F3a-zA-Z _]{1,12}$/i;
		return filter.test(string);
	};

	// ### username
	
	$.fn.validate_usernameCheck = function(string){
		var string = $.trim(string);
		var filter = /^[a-zA-Z0-9\u4e00-\u9fa5]{1,30}$/i;
		return filter.test(string);
	};

	// ### monitorname
	
	$.fn.validate_monitornameCheck = function(string){
		var string = $.trim(string);
		var filter = /^[a-zA-Z#0-9\u4e00-\u9fa5]{1,30}$/i;
		return filter.test(string);
	};

	/***end***/

	$.fn.validate = function(option) {

		var errors = [];
		this.each(function() {
			var $this = $(this), data = $this.data('validation');
			//判断是否有初始化
			if (!data) {
				//获取参数
				var rel = $this.attr('rel'), data = $this.attr($.extend({dataAttribute:'data-validate'}, option).dataAttribute);

				if (data != undefined) {
					var start = data.indexOf('[');
					var end = data.indexOf(']');
					var optionstring = data.substring(start + 1, end);
				} else if(rel != undefined) {
					var start = rel.indexOf('[');
					var end = rel.indexOf(']');
					var optionstring = rel.substring(start + 1, end);
				}else if(option && option.validate){
					var start = option.validate.indexOf('[');
					var end = option.validate.indexOf(']');
					var optionstring = option.validate.substring(start + 1, end);
				}else{
					return;
				}
				$this.data('validation',(data = new Validate(this, option, errors, optionstring)));
			} else {
				//重新校验
				errors = data['check'](errors);
			}

			//绑定
			$this.on('blur', function() {
				data['check'](errors);
			}).on('keyup', function() {
				data['check'](errors);
			});

		});

		return errors;

	};

})(jQuery); 