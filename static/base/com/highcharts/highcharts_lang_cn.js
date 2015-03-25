/*
 highcharts_lang_cn
*/
Highcharts.setOptions({
	lang: {
		decimalPoint: ".",
		downloadJPEG: "下载 JPEG 图像",
		downloadPDF: "下载 PDF 文档",
		downloadPNG: "下载 PNG 图像",
		downloadSVG: "下载 SVG 矢量图像",
		downloadCSV: "下载 CSV 表格",
		exportButtonTitle: "导出图像",
		loading: '加载中',
		months: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
		numericSymbols: ['k', 'M', 'G', 'T', 'P', 'E'],
		printButtonTitle: "打印图表",
		resetZoom: '复位',
		resetZoomTitle: '比例1:1',
		shortMonths: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
		thousandsSep: "",
		weekdays: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
	},
	exporting: {
		url: 'http://' + location.host + '/highcharts-export/'
	},
	//colors: "#4572A7,#AA4643,#89A54E,#80699B,#3D96AE,#DB843D,#92A8CD,#A47D7C,#B5CA92".split(","),
	colors: ['#4096B5', '#ED7054', '#47C6C9', '#E5A653', '#399960', '#CC4A5A', '#9BAD4E', '#DB4F82', '#7E58AF', '#CC5CB7'],
	style: {
		fontFamily: '"微软雅黑" , "宋体", "幼圆", Arial, Tahoma'
	},
	//版权声明
	credits: {
		enabled: false,
		text: 'Highcharts.com',
		href: 'http://www.highcharts.com',
		position: {
			align: 'right',
			x: -10,
			verticalAlign: 'bottom',
			y: -5
		},
		style: {
			cursor: 'pointer',
			color: '#909090',
			fontSize: '9px'
		}
	}
});