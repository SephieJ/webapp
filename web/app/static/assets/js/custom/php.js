window.oPhp = {
	date : function(format, timestamp) {
		var that = this;
		var jsdate,
		    f;
		var txt_words = ['Sun', 'Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		var formatChr = /\\?(.?)/gi;
		var formatChrCb = function(t, s) {
			return f[t] ? f[t]() : s;
		};
		var _pad = function(n, c) {
			n = String(n);
			while (n.length < c) {
				n = '0' + n;
			}
			return n;
		};
		f = {
			d : function() {
				return _pad(f.j(), 2);
			},
			D : function() {
				return f.l().slice(0, 3);
			},
			j : function() {
				return jsdate.getDate();
			},
			l : function() {
				return txt_words[f.w()] + 'day';
			},
			N : function() {
				return f.w() || 7;
			},
			S : function() {
				var j = f.j();
				var i = j % 10;
				if (i <= 3 && parseInt((j % 100) / 10, 10) == 1) {
					i = 0;
				}
				return ['st', 'nd', 'rd'][i - 1] || 'th';
			},
			w : function() {
				return jsdate.getDay();
			},
			z : function() {
				var a = new Date(f.Y(), f.n() - 1, f.j());
				var b = new Date(f.Y(), 0, 1);
				return Math.round((a - b) / 864e5);
			},

			W : function() {
				var a = new Date(f.Y(), f.n() - 1, f.j() - f.N() + 3);
				var b = new Date(a.getFullYear(), 0, 4);
				return _pad(1 + Math.round((a - b) / 864e5 / 7), 2);
			},

			F : function() {
				return txt_words[6 + f.n()];
			},
			m : function() {
				return _pad(f.n(), 2);
			},
			M : function() {
				return f.F().slice(0, 3);
			},
			n : function() {
				return jsdate.getMonth() + 1;
			},
			t : function() {
				return (new Date(f.Y(), f.n(), 0)).getDate();
			},

			L : function() {
				var j = f.Y();
				return j % 4 === 0 & j % 100 !== 0 | j % 400 === 0;
			},
			o : function() {
				var n = f.n();
				var W = f.W();
				var Y = f.Y();
				return Y + (n === 12 && W < 9 ? 1 : n === 1 && W > 9 ? -1 : 0);
			},
			Y : function() {
				return jsdate.getFullYear();
			},
			y : function() {
				return f.Y().toString().slice(-2);
			},

			a : function() {
				return jsdate.getHours() > 11 ? 'pm' : 'am';
			},
			A : function() {
				return f.a().toUpperCase();
			},
			B : function() {
				var H = jsdate.getUTCHours() * 36e2;
				var i = jsdate.getUTCMinutes() * 60;
				var s = jsdate.getUTCSeconds();
				return _pad(Math.floor((H + i + s + 36e2) / 86.4) % 1e3, 3);
			},
			g : function() {
				return f.G() % 12 || 12;
			},
			G : function() {
				return jsdate.getHours();
			},
			h : function() {
				return _pad(f.g(), 2);
			},
			H : function() {
				return _pad(f.G(), 2);
			},
			i : function() {
				return _pad(jsdate.getMinutes(), 2);
			},
			s : function() {
				return _pad(jsdate.getSeconds(), 2);
			},
			u : function() {
				return _pad(jsdate.getMilliseconds() * 1000, 6);
			},

			e : function() {
				throw 'Not supported (see source code of date() for timezone on how to add support)';
			},
			I : function() {
				var a = new Date(f.Y(), 0);
				var c = Date.UTC(f.Y(), 0);
				var b = new Date(f.Y(), 6);
				var d = Date.UTC(f.Y(), 6);
				return ((a - c) !== (b - d)) ? 1 : 0;
			},
			O : function() {
				var tzo = jsdate.getTimezoneOffset();
				var a = Math.abs(tzo);
				return (tzo > 0 ? '-' : '+') + _pad(Math.floor(a / 60) * 100 + a % 60, 4);
			},
			P : function() {
				var O = f.O();
				return (O.substr(0, 3) + ':' + O.substr(3, 2));
			},
			T : function() {
				return 'UTC';
			},
			Z : function() {
				return -jsdate.getTimezoneOffset() * 60;
			},

			c : function() {
				return 'Y-m-d\\TH:i:sP'.replace(formatChr, formatChrCb);
			},
			r : function() {
				return 'D, d M Y H:i:s O'.replace(formatChr, formatChrCb);
			},
			U : function() {
				return jsdate / 1000 | 0;
			}
		};
		this.date = function(format, timestamp) {
			that = this;
			jsdate = (timestamp === undefined ? new Date() : ( timestamp instanceof Date) ? new Date(timestamp) : new Date(timestamp * 1000)
			);
			return format.replace(formatChr, formatChrCb);
		};
		return this.date(format, timestamp);
	},

	array_intersect_key : function(arr1) {
		var retArr = {},
		    argl = arguments.length,
		    arglm1 = argl - 1,
		    k1 = '',
		    arr = {},
		    i = 0,
		    k = ''; arr1keys:
		for (k1 in arr1) { arrs:
			for ( i = 1; i < argl; i++) {
				arr = arguments[i];
				for (k in arr) {
					if (k === k1) {
						if (i === arglm1) {
							retArr[k1] = arr1[k1];
						}
						continue arrs;
					}
				}
				continue arr1keys;
			}
		}

		return retArr;
	},

	array_merge : function() {
		var args = Array.prototype.slice.call(arguments),
		    argl = args.length,
		    arg,
		    retObj = {},
		    k = '',
		    argil = 0,
		    j = 0,
		    i = 0,
		    ct = 0,
		    toStr = Object.prototype.toString,
		    retArr = true;

		for ( i = 0; i < argl; i++) {
			if (toStr.call(args[i]) !== '[object Array]') {
				retArr = false;
				break;
			}
		}

		if (retArr) {
			retArr = [];
			for ( i = 0; i < argl; i++) {
				retArr = retArr.concat(args[i]);
			}
			return retArr;
		}

		for ( i = 0,
		ct = 0; i < argl; i++) {
			arg = args[i];
			if (toStr.call(arg) === '[object Array]') {
				for ( j = 0,
				argil = arg.length; j < argil; j++) {
					retObj[ct++] = arg[j];
				}
			} else {
				for (k in arg) {
					if (arg.hasOwnProperty(k)) {
						if (parseInt(k, 10) + '' === k) {
							retObj[ct++] = arg[k];
						} else {
							retObj[k] = arg[k];
						}
					}
				}
			}
		}
		return retObj;
	},

	htmlentities : function(string, quote_style, charset, double_encode) {
		var hash_map = this.get_html_translation_table('HTML_ENTITIES', quote_style),
		    symbol = '';
		string = string == null ? '' : string + '';

		if (!hash_map) {
			return false;
		}

		if (quote_style && quote_style === 'ENT_QUOTES') {
			hash_map["'"] = '&#039;';
		}

		if (!!double_encode || double_encode == null) {
			for (symbol in hash_map) {
				if (hash_map.hasOwnProperty(symbol)) {
					string = string.split(symbol).join(hash_map[symbol]);
				}
			}
		} else {
			string = string.replace(/([\s\S]*?)(&(?:#\d+|#x[\da-f]+|[a-zA-Z][\da-z]*);|$)/g, function(ignore, text, entity) {
				for (symbol in hash_map) {
					if (hash_map.hasOwnProperty(symbol)) {
						text = text.split(symbol).join(hash_map[symbol]);
					}
				}

				return text + entity;
			});
		}
		return string;
	},

	number_format : function(number, decimals, dec_point, thousands_sep) {
		var n = !isFinite(+number) ? 0 : +number,
		    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
		    sep = ( typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
		    dec = ( typeof dec_point === 'undefined') ? '.' : dec_point,
		    s = '',
		    toFixedFix = function(n, prec) {
			var k = Math.pow(10, prec);
			return '' + Math.round(n * k) / k;
		};
		s = ( prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
		if (s[0].length > 3) {
			s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
		}
		if ((s[1] || '').length < prec) {
			s[1] = s[1] || '';
			s[1] += new Array(prec - s[1].length + 1).join('0');
		}
		return s.join(dec);
	},

	in_array : function(needle, haystack, argStrict) {
		var key = '',
		    strict = !!argStrict;
		if (strict) {
			for (key in haystack) {
				if (haystack[key] === needle) {
					return true;
				}
			}
		} else {
			for (key in haystack) {
				if (haystack[key] == needle) {
					return true;
				}
			}
		}
		return false;
	},

	range : function(low, high, step) {
		var matrix = [];
		var inival,
		    endval,
		    plus;
		var walker = step || 1;
		var chars = false;

		if (!isNaN(low) && !isNaN(high)) {
			inival = low;
			endval = high;
		} else if (isNaN(low) && isNaN(high)) {
			chars = true;
			inival = low.charCodeAt(0);
			endval = high.charCodeAt(0);
		} else {
			inival = (isNaN(low) ? 0 : low);
			endval = (isNaN(high) ? 0 : high);
		}

		plus = ((inival > endval) ? false : true);
		if (plus) {
			while (inival <= endval) {
				matrix.push(((chars) ? String.fromCharCode(inival) : inival));
				inival += walker;
			}
		} else {
			while (inival >= endval) {
				matrix.push(((chars) ? String.fromCharCode(inival) : inival));
				inival -= walker;
			}
		}

		return matrix;
	},

	sha1 : function(str) {
		var rotate_left = function(n, s) {
			var t4 = (n << s) | (n >>> (32 - s));
			return t4;
		};

		var cvt_hex = function(val) {
			var str = '';
			var i;
			var v;

			for ( i = 7; i >= 0; i--) {
				v = (val >>> (i * 4)) & 0x0f;
				str += v.toString(16);
			}
			return str;
		};

		var blockstart;
		var i,
		    j;
		var W = new Array(80);
		var H0 = 0x67452301;
		var H1 = 0xEFCDAB89;
		var H2 = 0x98BADCFE;
		var H3 = 0x10325476;
		var H4 = 0xC3D2E1F0;
		var A,
		    B,
		    C,
		    D,
		    E;
		var temp;

		str = this.utf8_encode(str);
		var str_len = str.length;

		var word_array = [];
		for ( i = 0; i < str_len - 3; i += 4) {
			j = str.charCodeAt(i) << 24 | str.charCodeAt(i + 1) << 16 | str.charCodeAt(i + 2) << 8 | str.charCodeAt(i + 3);
			word_array.push(j);
		}

		switch (str_len % 4) {
		case 0:
			i = 0x080000000;
			break;
		case 1:
			i = str.charCodeAt(str_len - 1) << 24 | 0x0800000;
			break;
		case 2:
			i = str.charCodeAt(str_len - 2) << 24 | str.charCodeAt(str_len - 1) << 16 | 0x08000;
			break;
		case 3:
			i = str.charCodeAt(str_len - 3) << 24 | str.charCodeAt(str_len - 2) << 16 | str.charCodeAt(str_len - 1) << 8 | 0x80;
			break;
		}

		word_array.push(i);

		while ((word_array.length % 16) != 14) {
			word_array.push(0);
		}

		word_array.push(str_len >>> 29);
		word_array.push((str_len << 3) & 0x0ffffffff);

		for ( blockstart = 0; blockstart < word_array.length; blockstart += 16) {
			for ( i = 0; i < 16; i++) {
				W[i] = word_array[blockstart + i];
			}
			for ( i = 16; i <= 79; i++) {
				W[i] = rotate_left(W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16], 1);
			}

			A = H0;
			B = H1;
			C = H2;
			D = H3;
			E = H4;

			for ( i = 0; i <= 19; i++) {
				temp = (rotate_left(A, 5) + ((B & C) | (~B & D)) + E + W[i] + 0x5A827999) & 0x0ffffffff;
				E = D;
				D = C;
				C = rotate_left(B, 30);
				B = A;
				A = temp;
			}

			for ( i = 20; i <= 39; i++) {
				temp = (rotate_left(A, 5) + (B ^ C ^ D) + E + W[i] + 0x6ED9EBA1) & 0x0ffffffff;
				E = D;
				D = C;
				C = rotate_left(B, 30);
				B = A;
				A = temp;
			}

			for ( i = 40; i <= 59; i++) {
				temp = (rotate_left(A, 5) + ((B & C) | (B & D) | (C & D)) + E + W[i] + 0x8F1BBCDC) & 0x0ffffffff;
				E = D;
				D = C;
				C = rotate_left(B, 30);
				B = A;
				A = temp;
			}

			for ( i = 60; i <= 79; i++) {
				temp = (rotate_left(A, 5) + (B ^ C ^ D) + E + W[i] + 0xCA62C1D6) & 0x0ffffffff;
				E = D;
				D = C;
				C = rotate_left(B, 30);
				B = A;
				A = temp;
			}

			H0 = (H0 + A) & 0x0ffffffff;
			H1 = (H1 + B) & 0x0ffffffff;
			H2 = (H2 + C) & 0x0ffffffff;
			H3 = (H3 + D) & 0x0ffffffff;
			H4 = (H4 + E) & 0x0ffffffff;
		}

		temp = cvt_hex(H0) + cvt_hex(H1) + cvt_hex(H2) + cvt_hex(H3) + cvt_hex(H4);
		return temp.toLowerCase();
	},

	utf8_decode : function(str_data) {
		var tmp_arr = [],
		    i = 0,
		    ac = 0,
		    c1 = 0,
		    c2 = 0,
		    c3 = 0,
		    c4 = 0;

		str_data += '';

		while (i < str_data.length) {
			c1 = str_data.charCodeAt(i);
			if (c1 <= 191) {
				tmp_arr[ac++] = String.fromCharCode(c1);
				i++;
			} else if (c1 <= 223) {
				c2 = str_data.charCodeAt(i + 1);
				tmp_arr[ac++] = String.fromCharCode(((c1 & 31) << 6) | (c2 & 63));
				i += 2;
			} else if (c1 <= 239) {
				c2 = str_data.charCodeAt(i + 1);
				c3 = str_data.charCodeAt(i + 2);
				tmp_arr[ac++] = String.fromCharCode(((c1 & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			} else {
				c2 = str_data.charCodeAt(i + 1);
				c3 = str_data.charCodeAt(i + 2);
				c4 = str_data.charCodeAt(i + 3);
				c1 = ((c1 & 7) << 18) | ((c2 & 63) << 12) | ((c3 & 63) << 6) | (c4 & 63);
				c1 -= 0x10000;
				tmp_arr[ac++] = String.fromCharCode(0xD800 | ((c1 >> 10) & 0x3FF));
				tmp_arr[ac++] = String.fromCharCode(0xDC00 | (c1 & 0x3FF));
				i += 4;
			}
		}

		return tmp_arr.join('');
	},

	utf8_encode : function(argString) {
		if (argString === null || typeof argString === 'undefined') {
			return '';
		}

		var string = (argString + '');
		var utftext = '',
		    start,
		    end,
		    stringl = 0;

		start = end = 0;
		stringl = string.length;
		for (var n = 0; n < stringl; n++) {
			var c1 = string.charCodeAt(n);
			var enc = null;

			if (c1 < 128) {
				end++;
			} else if (c1 > 127 && c1 < 2048) {
				enc = String.fromCharCode((c1 >> 6) | 192, (c1 & 63) | 128);
			} else if ((c1 & 0xF800) != 0xD800) {
				enc = String.fromCharCode((c1 >> 12) | 224, ((c1 >> 6) & 63) | 128, (c1 & 63) | 128);
			} else {
				if ((c1 & 0xFC00) != 0xD800) {
					throw new RangeError('Unmatched trail surrogate at ' + n);
				}
				var c2 = string.charCodeAt(++n);
				if ((c2 & 0xFC00) != 0xDC00) {
					throw new RangeError('Unmatched lead surrogate at ' + (n - 1));
				}
				c1 = ((c1 & 0x3FF) << 10) + (c2 & 0x3FF) + 0x10000;
				enc = String.fromCharCode((c1 >> 18) | 240, ((c1 >> 12) & 63) | 128, ((c1 >> 6) & 63) | 128, (c1 & 63) | 128);
			}
			if (enc !== null) {
				if (end > start) {
					utftext += string.slice(start, end);
				}
				utftext += enc;
				start = end = n + 1;
			}
		}

		if (end > start) {
			utftext += string.slice(start, stringl);
		}

		return utftext;
	},

	str_pad	: function  (input, padLength, padString, padType)
	{
		var half = '';
		var padToGo;
		var _strPadRepeater = function (s, len) {
			var collect = '';
			
			while (collect.length < len) {
				collect += s;
			}
			collect = collect.substr(0, len);
			
			return collect;
		};
		
		input += '';
		padString = padString !== undefined ? padString : ' ';
		
		if (padType !== 'STR_PAD_LEFT' && padType !== 'STR_PAD_RIGHT' && padType !== 'STR_PAD_BOTH') {
			padType = 'STR_PAD_RIGHT';
		}
		if ((padToGo = padLength - input.length) > 0) {
			if (padType === 'STR_PAD_LEFT') {
				input = _strPadRepeater(padString, padToGo) + input;
			} else if (padType === 'STR_PAD_RIGHT') {
				input = input + _strPadRepeater(padString, padToGo);
			} else if (padType === 'STR_PAD_BOTH') {
				half = _strPadRepeater(padString, Math.ceil(padToGo / 2));
				input = half + input + half;
				input = input.substr(0, padLength);
			}
		}
		
		return input;
	},

	strtotime : function(text, now) {
		var parsed,
		    match,
		    today,
		    year,
		    date,
		    days,
		    ranges,
		    len,
		    times,
		    regex,
		    i,
		    fail = false;

		if (!text) {
			return fail;
		}

		text = text.replace(/^\s+|\s+$/g, '').replace(/\s{2,}/g, ' ').replace(/[\t\r\n]/g, '').toLowerCase();

		match = text.match(/^(\d{1,4})([\-\.\/\:])(\d{1,2})([\-\.\/\:])(\d{1,4})(?:\s(\d{1,2}):(\d{2})?:?(\d{2})?)?(?:\s([A-Z]+)?)?$/);

		if (match && match[2] === match[4]) {
			if (match[1] > 1901) {
				switch (match[2]) {
				case '-': {
					if (match[3] > 12 || match[5] > 31) {
						return fail;
					}

					return new Date(match[1], parseInt(match[3], 10) - 1, match[5], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
				}
				case '.': {
					return fail;
				}
				case '/': {
					if (match[3] > 12 || match[5] > 31) {
						return fail;
					}

					return new Date(match[1], parseInt(match[3], 10) - 1, match[5], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
				}
				}
			} else if (match[5] > 1901) {
				switch (match[2]) {
				case '-': {
					if (match[3] > 12 || match[1] > 31) {
						return fail;
					}

					return new Date(match[5], parseInt(match[3], 10) - 1, match[1], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
				}
				case '.': {
					if (match[3] > 12 || match[1] > 31) {
						return fail;
					}

					return new Date(match[5], parseInt(match[3], 10) - 1, match[1], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
				}
				case '/': {
					if (match[1] > 12 || match[3] > 31) {
						return fail;
					}

					return new Date(match[5], parseInt(match[1], 10) - 1, match[3], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
				}
				}
			} else {
				switch (match[2]) {
				case '-': {
					if (match[3] > 12 || match[5] > 31 || (match[1] < 70 && match[1] > 38)) {
						return fail;
					}

					year = match[1] >= 0 && match[1] <= 38 ? +match[1] + 2000 : match[1];
					return new Date(year, parseInt(match[3], 10) - 1, match[5], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
				}
				case '.': {
					if (match[5] >= 70) {
						if (match[3] > 12 || match[1] > 31) {
							return fail;
						}

						return new Date(match[5], parseInt(match[3], 10) - 1, match[1], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
					}
					if (match[5] < 60 && !match[6]) {
						if (match[1] > 23 || match[3] > 59) {
							return fail;
						}

						today = new Date();
						return new Date(today.getFullYear(), today.getMonth(), today.getDate(), match[1] || 0, match[3] || 0, match[5] || 0, match[9] || 0) / 1000;
					}

					return fail;
				}
				case '/': {
					if (match[1] > 12 || match[3] > 31 || (match[5] < 70 && match[5] > 38)) {
						return fail;
					}

					year = match[5] >= 0 && match[5] <= 38 ? +match[5] + 2000 : match[5];
					return new Date(year, parseInt(match[1], 10) - 1, match[3], match[6] || 0, match[7] || 0, match[8] || 0, match[9] || 0) / 1000;
				}
				case ':': {
					if (match[1] > 23 || match[3] > 59 || match[5] > 59) {
						return fail;
					}

					today = new Date();
					return new Date(today.getFullYear(), today.getMonth(), today.getDate(), match[1] || 0, match[3] || 0, match[5] || 0) / 1000;
				}
				}
			}
		}

		if (text === 'now') {
			return now === null || isNaN(now) ? new Date().getTime() / 1000 | 0 : now | 0;
		}
		if (!isNaN( parsed = Date.parse(text))) {
			return parsed / 1000 | 0;
		}

		date = now ? new Date(now * 1000) : new Date();
		days = {
			'sun' : 0,
			'mon' : 1,
			'tue' : 2,
			'wed' : 3,
			'thu' : 4,
			'fri' : 5,
			'sat' : 6
		};
		ranges = {
			'yea' : 'FullYear',
			'mon' : 'Month',
			'day' : 'Date',
			'hou' : 'Hours',
			'min' : 'Minutes',
			'sec' : 'Seconds'
		};

		function lastNext(type, range, modifier) {
			var diff,
			    day = days[range];

			if ( typeof day !== 'undefined') {
				diff = day - date.getDay();

				if (diff === 0) {
					diff = 7 * modifier;
				} else if (diff > 0 && type === 'last') {
					diff -= 7;
				} else if (diff < 0 && type === 'next') {
					diff += 7;
				}

				date.setDate(date.getDate() + diff);
			}
		}

		function process(val) {
			var splt = val.split(' '),
			    type = splt[0],
			    range = splt[1].substring(0, 3),
			    typeIsNumber = /\d+/.test(type),
			    ago = splt[2] === 'ago',
			    num = (type === 'last' ? -1 : 1) * ( ago ? -1 : 1);

			if (typeIsNumber) {
				num *= parseInt(type, 10);
			}

			if (ranges.hasOwnProperty(range) && !splt[1].match(/^mon(day|\.)?$/i)) {
				return date['set' + ranges[range]](date['get' + ranges[range]]() + num);
			}

			if (range === 'wee') {
				return date.setDate(date.getDate() + (num * 7));
			}

			if (type === 'next' || type === 'last') {
				lastNext(type, range, num);
			} else if (!typeIsNumber) {
				return false;
			}

			return true;
		}

		times = '(years?|months?|weeks?|days?|hours?|minutes?|min|seconds?|sec' + '|sunday|sun\\.?|monday|mon\\.?|tuesday|tue\\.?|wednesday|wed\\.?' + '|thursday|thu\\.?|friday|fri\\.?|saturday|sat\\.?)';
		regex = '([+-]?\\d+\\s' + times + '|' + '(last|next)\\s' + times + ')(\\sago)?';

		match = text.match(new RegExp(regex, 'gi'));
		if (!match) {
			return fail;
		}

		for ( i = 0,
		len = match.length; i < len; i++) {
			if (!process(match[i])) {
				return fail;
			}
		}

		return (date.getTime() / 1000);
	},

	trim : function(str, charlist) {
		var whitespace,
		    l = 0,
		    i = 0;
		str += '';

		if (!charlist) {
			whitespace = ' \n\r\t\f\x0b\xa0\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u200b\u2028\u2029\u3000';
		} else {
			charlist += '';
			whitespace = charlist.replace(/([\[\]\(\)\.\?\/\*\{\}\+\$\^\:])/g, '$1');
		}

		l = str.length;
		for ( i = 0; i < l; i++) {
			if (whitespace.indexOf(str.charAt(i)) === -1) {
				str = str.substring(i);
				break;
			}
		}

		l = str.length;
		for ( i = l - 1; i >= 0; i--) {
			if (whitespace.indexOf(str.charAt(i)) === -1) {
				str = str.substring(0, i + 1);
				break;
			}
		}

		return whitespace.indexOf(str.charAt(0)) === -1 ? str : '';
	}
}; 