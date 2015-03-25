//扩展Raphael
Raphael.el.visible = function() {
    return (this.node.style.display !== "none");
}
Raphael.fn.connection = function(obj1, obj2) {
    var line;
    if (obj1.line && obj1.from && obj1.to) {
        line = obj1;
        obj1 = line.from;
        obj2 = line.to;
    }
    var bb1 = obj1.getBBox(),
        bb2 = obj2.getBBox(),
        p = [{
            x: bb1.x + bb1.width / 2,
            y: bb1.y - 1
        }, {
            x: bb1.x + bb1.width / 2,
            y: bb1.y + bb1.height + 1
        }, {
            x: bb1.x - 7,
            y: bb1.y + bb1.height / 2
        }, {
            x: bb1.x + bb1.width + 1,
            y: bb1.y + bb1.height / 2
        }, {
            x: bb2.x + bb2.width / 2,
            y: bb2.y - 1
        }, {
            x: bb2.x + bb2.width / 2,
            y: bb2.y + bb2.height + 1
        }, {
            x: bb2.x - 1,
            y: bb2.y + bb2.height / 2
        }, {
            x: bb2.x + bb2.width + 7,
            y: bb2.y + bb2.height / 2
        }],
        d = {}, dis = [];
    for (var i = 0; i < 4; i++) {
        for (var j = 4; j < 8; j++) {
            var dx = Math.abs(p[i].x - p[j].x),
                dy = Math.abs(p[i].y - p[j].y);
            if ((i == j - 4) || (((i != 3 && j != 6) || p[i].x < p[j].x) && ((i != 2 && j != 7) || p[i].x > p[j].x) && ((i != 0 && j != 5) || p[i].y > p[j].y) && ((i != 1 && j != 4) || p[i].y < p[j].y))) {
                dis.push(dx + dy);
                d[dis[dis.length - 1]] = [i, j];
            }
        }
    }
    if (dis.length == 0) {
        var res = [0, 4];
    } else {
        res = d[Math.min.apply(Math, dis)];
    }
    var x1 = p[res[0]].x,
        y1 = p[res[0]].y,
        x4 = p[res[1]].x,
        y4 = p[res[1]].y;
    dx = Math.max(Math.abs(x1 - x4) / 2, 10);
    dy = Math.max(Math.abs(y1 - y4) / 2, 10);
    var x2 = [x1, x1, x1 - dx, x1 + dx][res[0]].toFixed(3),
        y2 = [y1 - dy, y1 + dy, y1, y1][res[0]].toFixed(3),
        x3 = [0, 0, 0, 0, x4, x4, x4 - dx, x4 + dx][res[1]].toFixed(3),
        y3 = [0, 0, 0, 0, y1 + dy, y1 - dy, y4, y4][res[1]].toFixed(3);
    var path = ["M", x1.toFixed(3), y1.toFixed(3), "C", x2 - 70, y2, x3 + 70, y3, x4.toFixed(3), y4.toFixed(3), ].join(",");

    var size = 4;
    var angle = Math.atan2(x4 - x1, y1 - y1);
    angle = (angle / (2 * Math.PI)) * 360;
    path += ('M' + x1 + ' ' + y1 + ' L' + (x1 - size) + ' ' + (y1 - size) + ' L' + (x1 - size) + ' ' + (y1 + size) + ' L' + x1 + ' ' + y1);
    /*画箭头*
    var size = 3;
    var angle = Math.atan2(x4-x1,y1-y1);
    angle = (angle / (2 * Math.PI)) * 360;
    var arrowPath = this.path('M' + x1 + ' ' + y1 + ' L' + (x1 - size) + ' ' + (y1 - size) + ' L' + (x1 - size) + ' ' + (y1 + size) + ' L' + x1 + ' ' + y1 ).attr('fill','black').rotate((90+angle),x1,y1);
    */

    if (line && line.line) {
        line.bg && line.bg.attr({
            path: path
        });
        line.line.attr({
            path: path
        });
    } else {
        var rLine = {
            bg: this.path(path),
            line: this.path(path),
            from: obj1,
            to: obj2
        };
        rLine.bg.node.id = obj1.node.id + '_' + obj2.node.id;
        return rLine;
    }
};


/*
* 1.取消对点显示/隐藏操作
*
*
*坐标x轴保留百分比
*
*
*
*
*
*
*
*
*
后台：
    targets表示被测端，包含监测点与目标
    monitors表示探测端，只有监测点

前端：
    targets表示mid为空是目标，不为空是监测点
    monitors表示是监测点
    用户创建任务时，手动输入目标无tpid，从服务端请求数据时，目标带有tpid
    故，
    id组成规则【点：目标用 name ，监测点用 mid 线：name_mid】
    提交数据时，过滤掉前端动态生成的id
    connections用目标的name与监测点的mid进行连接
 */
;
(function($) {

    var ConceptMap = function(el, option) {
        var defaults = {
            draggable: false,//不可拖拽
            clickShow: false, //'show'画布只显示被点击元素 'hide'画布只隐藏被点击元素
            clickPoint: function(rNode, $click, x, y, nodeData) {
                this.pointClickShow(rNode);//单击点事件回调
            },
            dblclickPoint: function(rNode, $dbclick, x, y, nodeData) {
                //双击点事件回调
            },
            clickLine: function(rNode, $click, x, y, nodeData) {
                this.lineClickShow(rNode);//单击线事件回调
            },
            dblclickLine: function(rNode, $dbclick, x, y, nodeData) {
                //双击线事件回调
            },
            data: {
                targets: [],
                monitors: []
            },
            minHeight: 600,//画布最小高度
            containerPaddingTop: 80,//顶边距
            pointYRangPx: 42,//垂直间距
            pointXRangPer: 12,//x轴平分为12等份
            fontSize: 12,//文字大小
            imgPath: ''//监测点图片monitor.png的相对路径
        }
        var options = this.options = $.extend(true, defaults, option);
        //存储点
        this.points = {};
        //存储线
        this.lines = {};
        //颜色值
        this.color = {
            'none': 'gray',
            '3': 'red',
            '2': 'darkgoldenrod',
            '1': 'green',
            '0': 'gray'
        };
        //告警级别
        this.level = {
            'none': 'N/A',
            '3': '严重告警',
            '2': '告警',
            '1': '正常',
            '0': '未测试'
        };
        this.container = $(el);
        this.yMax = options.minHeight;
        this.init(options.data);

    };
    ConceptMap.prototype = {
        constructor: ConceptMap,
        init: function(data) {
            var options = this.options;

            //画布宽高
            //容器宽
            this.containerWidth = this.container.width();
            //容器高
            var maxPoint = options.data.targets.length > options.data.monitors.length ? options.data.targets.length : options.data.monitors.length;
            options.containerHeight = options.containerPaddingTop + options.pointYRangPx * maxPoint;
            if (this.options.minHeight > this.options.containerHeight) {
                this.options.containerHeight = this.options.minHeight;
            }
            //画布
            this.raphael = Raphael(this.container[0].id, this.containerWidth, this.options.containerHeight);

            //绘制点线
            this.draw(data);

            //重置画布高宽
            this.resize();
        },
        cleanData: function() {
            //清空数据
            this.points = {};
            this.lines = {};
        },
        redraw: function() {
            var options = this.options;
            //清空数据
            this.cleanData();
            //清空画布
            this.raphael.clear();
            //重绘
            this.draw(options.data);
        },
        setSize: function(width, height) {
            this.raphael.setSize(width, height);
        },
        resize: function() {
            this.containerWidth = this.container.width();
            this.raphael.setSize(this.containerWidth, this.yMax + 30);
        },
        setLineLevel: function(rLine, level, animate) {
            var that = this;
            if (!animate)
                rLine.line.attr({
                    stroke: that.color[level]
                });
            else {
                rLine.line.animate({
                    stroke: that.color[level]
                }, 200, 'linear');

                rLine.bg.animate({
                    stroke: that.color[level],
                    opacity: 1
                }, 200, 'linear', function() {
                    this.animate({
                        opacity: 0
                    }, 200, 'linear', function() {
                        this.animate({
                            opacity: 1
                        }, 400, 'linear', function() {
                            this.animate({
                                opacity: 0
                            }, 400, 'linear')
                        })
                    })
                });
            }

        },
        draw: function(data) {
            var points = this.points,
                lines = this.lines,
                level = this.level,
                width = this.containerWidth,
                R = this.raphael,
                that = this;
            options = this.options;
            //绘制点
            var leftX = width / this.options.pointXRangPer;
            var centerX = width / this.options.pointXRangPer * (this.options.pointXRangPer / 2 - 1);
            var rightX = width / this.options.pointXRangPer * (this.options.pointXRangPer - 1);

            //拖拽事件
            var start = function() {
                this.animate({
                    "fill-opacity": .5
                }, 500)
                //事件对象是text，不拖拽
                if (this.type == "text")
                    return;
                //读取各个元素原坐标
                for (i = 0; i < this.set.length; i++) {
                    this.set[i].ox = (this.set[i].type == "text" || this.set[i].type == "image") ? this.set[i].attr("x") : this.set[i].attr('cx');
                    this.set[i].oy = (this.set[i].type == "text" || this.set[i].type == "image") ? this.set[i].attr("y") : this.set[i].attr('cy');
                }
                //采集与此点连接的线
                this.connectLines = [];
                for (var index in lines)
                    if (lines[index].monitor_mid == this.node.id || lines[index].target_mid == this.node.id || lines[index].target_name == this.node.id)
                        this.connectLines.push(lines[index].rLine);
            },
                move = function(dx, dy) {
                    //事件对象是text，不拖拽
                    if (this.type == "text")
                        return;

                    //判断this.set的第一个元素坐标，限制元素在画布之内
                    var newX = this.set[0].ox + dx,
                        newY = this.set[0].oy + dy;
                    if (newX < 0 || newX > that.containerWidth - 30 || newY < 0 || newY > that.yMax - 38)
                        return;

                    //实时更新坐标
                    for (i = 0; i < this.set.length; i++) {


                        if (this.set[i].type == "text" || this.set[i].type == "image") {
                            this.set[i].attr({
                                x: this.set[i].ox + dx,
                                y: this.set[i].oy + dy
                            });
                        } else {
                            this.set[i].attr({
                                cx: this.set[i].ox + dx,
                                cy: this.set[i].oy + dy
                            });
                        }
                    }
                    for (var index in this.connectLines)
                        R.connection(this.connectLines[index]);
                },
                up = function() {
                    this.animate({
                        "fill-opacity": 1
                    }, 500);
                    //事件对象是text，不拖拽
                    if (this.type == "text")
                        return;
                    //保存当前坐标
                    for (i = 0; i < this.set.length; i++) {
                        this.set[i].ox = (this.set[i].type == "text" || this.set[i].type == "image") ? this.set[i].attr("x") : this.set[i].attr('cx');
                        this.set[i].oy = (this.set[i].type == "text" || this.set[i].type == "image") ? this.set[i].attr("y") : this.set[i].attr('cy');
                    }
                };

            var setHandler = function() {
                var set = R.set();
                for (var index in arguments) {
                    //元素放进集合
                    set.push(arguments[index]);
                    //集合保存在元素属性
                    arguments[index].set = set;
                }
                //绑定拖拽事件
                set.drag(move, start, up);
            }

            //tooltip
            var showTooltip = function(node, tooltip) {
                that.container.append($('<div style="display:none;" id="inline_' + node.id + '">' + tooltip + '</div>'));
                Tipped.create(node, 'inline_' + node.id, {
                    skin: 'white',
                    target: 'mouse',
                    hook: 'topmiddle',
                    stem: false,
                    inline: true,
                    offset: {
                        y: '-10'
                    }
                }).show();
            }
            var moniterTooltip = function() {
                var id = this.node.id,
                    tooltip = '';
                tooltip = '<span class="muted">监测点名称：</span><strong>' + points[id].name + '</strong>';

                showTooltip(this.node, tooltip);
            }
            var targetTooltip = function() {
                var id = this.node.id,
                    tooltip = '';
                tooltip = '<span class="muted">目标名称：</span><strong>' + points[id].name + '</strong><br>' + '<span class="muted">地址：</span>' + points[id].dest + '<br>' + '<span class="muted">分类：</span>' + points[id].web_type;

                showTooltip(this.node, tooltip);
            }
            var lineTooltip = function() {
                var id = this.node.id,
                    tooltip = '';
                tooltip = '<span class="muted">从 </span><strong>' + lines[id].monitor_name + '</strong><span class="muted"> 到 </span><strong>' + lines[id].target_name + '</strong>' + '<br>' + '<span class="muted">告警级别：</span><span class="text-info">' + level[lines[id].level] + '</span><br>' + '<span class="muted">包数：</span>' + lines[id].pack_cnt + '<br>' + '<span class="muted">包大小：</span>' + lines[id].pack_size + '<br>' + '<span class="muted">周期：</span>' + lines[id].period;

                for (var index in lines[id].tooltip) {
                    if (lines[id].tooltip[index].value && lines[id].tooltip[index].value != 'None')
                        tooltip += '<br><span class="muted">' + (lines[id].tooltip[index].name ? lines[id].tooltip[index].name + '：' : '') + '</span><strong">' + lines[id].tooltip[index].value + '</strong>' + (lines[id].tooltip[index].unit || '');
                }
                /*
                if(lines[id].tooltip && lines[id].tooltip.length && lines[id].tooltip.length == 1){//根据监测点monitor_mid更新线，监测点上线
                    tooltip += '<br><span class="muted">' + lines[id].tooltip[index].name + '</span>';
                }else{
                    if (lines[id].tooltip && lines[id].tooltip.length)
                        var status_cn = lines[id].tooltip[lines[id].tooltip.length - 1].value;//得到status_cn测试状态
                    if (status_cn != null) {//测试状态status_cn不为null，只显示id跟begin_time
                        for (var index in lines[id].tooltip) {
                            if (lines[id].tooltip[index].id == 'id' || lines[id].tooltip[index].id == 'begin_time') {
                                tooltip += '<br><span class="muted">' + lines[id].tooltip[index].name + '</span>：<strong">' + lines[id].tooltip[index].value + '</strong>' + lines[id].tooltip[index].unit;
                            }
                        }
                        tooltip += '<br><span class="muted">' + status_cn + '</span>';
                    } else {//测试状态status_cn为null，显示status_cn之外
                        for (var index in lines[id].tooltip) {
                            if (lines[id].tooltip[index].id != 'status_cn') {
                                tooltip += '<br><span class="muted">' + lines[id].tooltip[index].name + '</span>：<strong">' + lines[id].tooltip[index].value + '</strong>' + lines[id].tooltip[index].unit;
                            }
                        }
                    }
                }
                */
                showTooltip(this.node, tooltip);
            }
            var hideTooltip = function() {
                var id = this.node.id;
                if (id) {
                    Tipped.remove(this.node);
                    $('#inline_' + id).remove();
                }
            }
            //点的 显/隐 事件
            that.pointClickShow = function(rNode) {
                if (this.options.clickShow == 'show' && this.options.clickShow != false) {
                    var points = this.points,
                        lines = this.lines;
                    //隐藏所有
                    this.hideAllElements();
                    /**1**
                    //显示事件点
                    points[rNode.node.id].rPoint.show();
                    points[rNode.node.id].rName.show();
                    */
                    //显示事件 连接线    
                    for (var index in lines) {
                        //被测端id
                        var target_id = lines[index].target_mid != null ? lines[index].target_mid : lines[index].target_name;
                        if (lines[index].monitor_mid == rNode.node.id) { //点击的是探测端
                            /**1**
                            //显示被测端
                            points[target_id].rPoint.show();
                            points[target_id].rName.show();
                            */
                            //显示连接线
                            lines[index].rLine.line.show();
                            lines[index].rLine.bg.show();
                        } else if (target_id == rNode.node.id) { //点击的是被测端
                            /**1**
                            //显示被测端
                            points[lines[index].monitor_mid].rPoint.show();
                            points[lines[index].monitor_mid].rName.show();
                            */
                            //显示连接线
                            lines[index].rLine.line.show();
                            lines[index].rLine.bg.show();
                        }
                    }
                } else if (this.options.clickShow == 'hide' && this.options.clickShow != false) {
                    var points = this.points,
                        lines = this.lines;
                    /**1**
                    //显示事件点
                    points[rNode.node.id].rPoint.hide();
                    points[rNode.node.id].rName.hide();
                    */
                    //显示事件 连接线    
                    for (var index in lines) {
                        //被测端id
                        var target_id = lines[index].target_mid != null ? lines[index].target_mid : lines[index].target_name;
                        if (lines[index].monitor_mid == rNode.node.id) { //点击的是探测端
                            //显示连接线
                            lines[index].rLine.line.hide();
                            lines[index].rLine.bg.hide();
                        } else if (target_id == rNode.node.id) { //点击的是被测端
                            //显示连接线
                            lines[index].rLine.line.hide();
                            lines[index].rLine.bg.hide();
                        }
                    }
                }
            };
            //线的 显/隐 事件
            that.lineClickShow = function(rNode) {
                var points = this.points,
                    lines = this.lines;
                if (this.options.clickShow == 'show' && this.options.clickShow != false) {
                    //隐藏所有
                    this.hideAllElements();

                    //显示事件线
                    lines[rNode.node.id].rLine.line.show();
                    lines[rNode.node.id].rLine.bg.show();
                    /**1**
                    //被测端id
                    var target_id = lines[rNode.node.id].target_mid != null ? lines[rNode.node.id].target_mid : lines[rNode.node.id].target_name;
                    //显示事件线相关联点
                    points[target_id].rPoint.show();
                    points[target_id].rName.show();
                    points[lines[rNode.node.id].monitor_mid].rPoint.show();
                    points[lines[rNode.node.id].monitor_mid].rName.show();
                    */
                } else if (this.options.clickShow == 'hide' && this.options.clickShow != false) {

                    //显示事件线
                    lines[rNode.node.id].rLine.line.hide();
                    lines[rNode.node.id].rLine.bg.hide();
                }
            };

            //绘制监测点
            for (var i in data.monitors) {
                //生成操作id
                var id = data.monitors[i].mid;
                //判断点是否已经绘制过存在过
                if (points[id])
                    continue;
                //存储属性
                points[id] = {};
                points[id].mid = data.monitors[i].mid;
                points[id].name = data.monitors[i].name;
                points[id].x = data.monitors[i].x ? data.monitors[i].x % 100 / 100 * this.containerWidth : leftX;
                points[id].y = data.monitors[i].y || this.options.containerPaddingTop + this.options.pointYRangPx * parseInt(i - 1) + 20;
                //raphael对象  
                points[id].rPoint = R.image(this.options.imgPath + 'monitor.png', points[id].x, points[id].y, 24, 24).attr({
                    cursor: (options.draggable || options.clickPoint != null) ? "pointer" : "default"
                }).hover(moniterTooltip, hideTooltip);

                //事件绑定
                points[id].rPoint.click(function() {
                    options.clickPoint.call(that, this, arguments[0], arguments[1], arguments[2], points[this.node.id]);
                });
                points[id].rPoint.dblclick(function() {
                    options.dblclickPoint.call(that, this, arguments[0], arguments[1], arguments[2], points[this.node.id]);
                });

                //节点对象设置id
                points[id].rPoint.node.id = id;
                //名称
                points[id].rName = R.text(points[id].x + 10, 32 + points[id].y, data.monitors[i].name).attr({
                    fill: "#000",
                    "font-size": this.options.fontSize,
                    "font-family": '"微软雅黑" , "宋体", "幼圆", Arial, Tahoma',
                    cursor: "default"
                });

                //是否可拖拽
                if (options.draggable)
                    setHandler(points[id].rPoint, points[id].rName); //群组

                //更新y坐标最大值                 
                if (this.yMax < 46 + points[id].y) {
                    this.yMax = 46 + points[id].y;
                };
            }

            var monitor_index = 0,
                target_index = 0;
            for (var i in data.targets) {
                if (data.targets[i].mid != null) { //绘制监测点

                    //生成操作id
                    var id = data.targets[i].mid;
                    //判断点是否已经绘制过存在过
                    if (points[id])
                        continue;
                    //存储属性
                    points[id] = {};
                    points[id].mid = data.targets[i].mid;
                    points[id].name = data.targets[i].name;

                    points[id].x = data.targets[i].x % 100 / 100 * this.containerWidth || centerX;
                    points[id].y = data.targets[i].y || this.options.containerPaddingTop + this.options.pointYRangPx * parseInt(monitor_index - 1) + 20;
                    //监测点index加1
                    monitor_index += 1;
                    //raphael对象  
                    points[id].rPoint = R.image(this.options.imgPath + 'monitor.png', points[id].x, points[id].y, 24, 24).attr({
                        cursor: (options.draggable || options.clickPoint != null) ? "pointer" : "default"
                    }).hover(moniterTooltip, hideTooltip);

                    //事件绑定
                    points[id].rPoint.click(function() {
                        options.clickPoint.call(that, this, arguments[0], arguments[1], arguments[2], points[this.node.id]);
                    });
                    points[id].rPoint.dblclick(function() {
                        options.dblclickPoint.call(that, this, arguments[0], arguments[1], arguments[2], points[this.node.id]);
                    });

                    //节点对象设置id
                    points[id].rPoint.node.id = id;
                    //名称
                    points[id].rName = R.text(points[id].x + 10, 32 + points[id].y, data.targets[i].name).attr({
                        fill: "#000",
                        "font-size": this.options.fontSize,
                        "font-family": '"微软雅黑" , "宋体", "幼圆", Arial, Tahoma',
                        cursor: "default"
                    });
                    //更新y坐标最大值                                 
                    if (this.yMax < 46 + points[id].y) {
                        this.yMax = 46 + points[id].y;
                    };

                } else { //绘制目标

                    //生成操作id
                    var id = data.targets[i].name;
                    //判断点是否已经绘制过存在过
                    if (points[id])
                        continue;
                    //存储属性
                    points[id] = {};
                    points[id].tpid = data.targets[i].tpid;
                    points[id].mid = data.targets[i].mid;
                    points[id].name = data.targets[i].name;
                    points[id].dest = data.targets[i].dest;
                    points[id].web_type = data.targets[i].web_type;

                    points[id].x = data.targets[i].x % 100 / 100 * this.containerWidth || rightX;
                    points[id].y = data.targets[i].y || this.options.containerPaddingTop + this.options.pointYRangPx * parseInt(target_index - 1) + 20;
                    //监测点index加1
                    target_index += 1;
                    //raphael对象  
                    points[id].rPoint = R.circle(points[id].x, 10 + points[id].y, 5).attr({
                        fill: "#FFF",
                        stroke: "#0088CC",
                        "stroke-width": 3,
                        cursor: (options.draggable || options.clickPoint != null) ? "pointer" : "default"
                    }).hover(targetTooltip, hideTooltip);

                    //事件绑定
                    points[id].rPoint.click(function() {
                        options.clickPoint.call(that, this, arguments[0], arguments[1], arguments[2], points[this.node.id]);
                    });
                    points[id].rPoint.dblclick(function() {
                        options.dblclickPoint.call(that, this, arguments[0], arguments[1], arguments[2], points[this.node.id]);
                    });

                    //节点对象设置id
                    points[id].rPoint.node.id = id;
                    //名称
                    points[id].rName = R.text(points[id].x, 28 + points[id].y, data.targets[i].name).attr({
                        fill: "#000",
                        "font-size": this.options.fontSize,
                        "font-family": '"微软雅黑" , "宋体", "幼圆", Arial, Tahoma',
                        cursor: "default"
                    });
                    //更新y坐标最大值                    
                    if (this.yMax < 46 + points[id].y) {
                        this.yMax = 46 + points[id].y;
                    };
                }
                //是否可拖拽
                if (options.draggable)
                    setHandler(points[id].rPoint, points[id].rName); //群组
            }

            //绘制线
            for (var i in data.connections) {
                //target_mid为null，则被测端为目标，取target的name为组成线id的前缀
                var target_id = data.connections[i].target_mid == null ? data.connections[i].target_name : data.connections[i].target_mid;
                //生成操作id，目标name + 监测点mid
                var id = target_id + '_' + data.connections[i].monitor_mid;

                //是否已经绘制过
                if (id in lines == false) {
                    //绘制线
                    var rLine = R.connection(points[target_id].rPoint, points[data.connections[i].monitor_mid].rPoint);
                    //设置线颜色
                    if (typeof parseInt(data.connections[i].level) == 'number')
                        this.setLineLevel(rLine, data.connections[i].level);

                    //raphael线对象
                    lines[id] = {};
                    lines[id].rLine = rLine;
                    //存储ping参数
                    lines[id].target_tpid = data.connections[i].target_tpid || null;
                    lines[id].target_mid = data.connections[i].target_mid;
                    lines[id].target_name = data.connections[i].target_name;
                    lines[id].monitor_mid = data.connections[i].monitor_mid;
                    lines[id].monitor_name = data.connections[i].monitor_name;
                    lines[id].pack_cnt = data.connections[i].pack_cnt;
                    lines[id].pack_size = data.connections[i].pack_size;
                    lines[id].period = data.connections[i].period;
                    lines[id].level = data.connections[i].level;
                    lines[id].tooltip = data.connections[i].tooltip || null;

                    //线样式&&事件
                    rLine.bg.attr({
                        stroke: "#FFF",
                        fill: "none",
                        opacity: 0,
                        "stroke-width": 7,
                        cursor: options.clickLine != null ? "pointer" : "default"
                    }).hover(lineTooltip, hideTooltip);

                    //事件绑定
                    rLine.bg.click(function() {
                        options.clickLine.call(that, this, arguments[0], arguments[1], arguments[2], lines[this.node.id]);
                    });
                    rLine.bg.dblclick(function() {
                        options.dblclickLine.call(that, this, arguments[0], arguments[1], arguments[2], lines[this.node.id]);
                    });

                    rLine.line.attr({
                        fill: "none",
                        "stroke-width": .7
                    });

                    //节点对象设置id
                    rLine.bg.node.id = id;

                }
            }
            this.container.mouseup(function(e) {
                if (e.which == 3) {
                    that.container.triggerHandler('rightClick');
                }
            });

            //提示
            if (options.tips)
                R.text(40, this.yMax + 10, options.tips).attr({
                    fill: "gray",
                    "text-anchor": "start",
                    "font-size": "12px",
                    "font-family": '"微软雅黑" , "宋体", "幼圆", Arial, Tahoma'
                })
                //图例
            R.text(rightX - 74, this.yMax + 10, '监测点：').attr({
                fill: "gray",
                "font-size": "13px",
                "font-family": '"微软雅黑" , "宋体", "幼圆", Arial, Tahoma'
            })
            R.image(this.options.imgPath + 'monitor.png', rightX - 50, this.yMax + 2, 16, 16)

            R.text(rightX + 6, this.yMax + 10, '目标：').attr({
                fill: "gray",
                "font-size": "13px",
                "font-family": '"微软雅黑" , "宋体", "幼圆", Arial, Tahoma'
            })
            R.circle(rightX + 30, this.yMax + 10, 5).attr({
                fill: "#FFF",
                stroke: "#0088CC",
                "stroke-width": 3
            })
            //标题线
            R.path("M" + (leftX - 48) + "," + this.yMax + "L" + (this.containerWidth - leftX + 48) + "," + (this.yMax - 7)).attr({
                stroke: "gray",
                'stroke-dasharray': ["- "],
                'stroke-width': .5
            })
        },
        //隐藏全部
        hideAllElements: function() {
            var points = this.points,
                lines = this.lines;
            /**1**
            //显示所有点
            for (var i in points) {
                if (points[i].rPoint) {
                    points[i].rPoint.hide();
                    points[i].rName.hide();
                }
            }
            */
            //显示所有线
            for (var ii in lines) {
                lines[ii].rLine.line.hide();
                lines[ii].rLine.bg.hide();
            }
        },
        //显示全部
        showAllElements: function() {
            var points = this.points,
                lines = this.lines;
            /**1**
            //显示所有点
            for (var i in points) {
                if (points[i].rPoint) {
                    points[i].rPoint.show();
                    points[i].rName.show();
                }
            }
            */
            //显示所有线
            for (var ii in lines) {
                lines[ii].rLine.line.show();
                lines[ii].rLine.bg.show();
            }
        },
        changeLevel: function(level, checked) {
            var lines = this.lines;
            for (var i in lines) {
                if (lines[i].level == level) {
                    if (checked) {
                        //显示线
                        lines[i].rLine.line.show();
                        lines[i].rLine.bg.show();
                    } else {
                        //隐藏线
                        lines[i].rLine.line.hide();
                        lines[i].rLine.bg.hide();
                    }
                }
            }
        },
        destroy: function() {
            window.removed = function() {
                //画布销毁时触发
            }
            //销毁画布
            this.raphael.remove();
            //清空数据
            this.cleanData();
            //清除容器data数据
            this.container.removeData('conceptMap');
        },
        getCoordData: function() {
            var targets = this.options.data.targets,
                monitors = this.options.data.monitors,
                points = this.points;
            for (var index in targets) {
                if (targets[index].mid != null) { //监测点
                    targets[index].x = points[targets[index].mid].rPoint.attr("x") / this.containerWidth * 100;
                    targets[index].y = points[targets[index].mid].rPoint.attr("y");
                } else { //目标
                    targets[index].x = points[targets[index].name].rPoint.attr("cx") / this.containerWidth * 100;
                    targets[index].y = points[targets[index].name].rPoint.attr("cy") - 10; //目标圆圈y轴偏移10px
                }
            }
            for (var index in monitors) { //监测点
                monitors[index].x = points[monitors[index].mid].rPoint.attr("x") / this.containerWidth * 100;
                monitors[index].y = points[monitors[index].mid].rPoint.attr("y");
            }
            return {
                'targets': targets,
                'monitors': monitors
            }
        },
        updateConnections: function(data) {
            for (var index in data) {
                this.updateConnection(data[index]);
            }
        },
        updateConnection: function(data) {
            var id;
            if (data.target_mid != null)
                id = data.target_mid + '_' + data.monitor_mid;
            else
                id = data.target_name + '_' + data.monitor_mid;

            if(!this.lines[id]){
                console.log('推送data.target_tpid不存在的链路，具体：')
                console.dir(data)
            } 

            this.lines[id].tooltip = data.tooltip;
            //更新线颜色
            this.lines[id].level = data.level;
            this.setLineLevel(this.lines[id].rLine, data.level, true);

        },
        updateByMonitorMid: function(data) {
            for(var index in this.lines){
                if(data.mid == this.lines[index].monitor_mid){                    
                    this.lines[index].tooltip = data.tooltip;
                    //更新线颜色
                    this.lines[index].level = data.level;
                    this.setLineLevel(this.lines[index].rLine, data.level, true);
                }
            }
        }
    }

    $.fn.conceptMap = function(options, fnOption) {
        var $this = $(this),
            data = $this.data('conceptMap');
        //判断是否有初始化
        if (!data) {
            data = new ConceptMap(this, options);
            $this.data('conceptMap', data);
            return data;
        }
        //调用函数
        if (typeof options == 'string' && fnOption) {
            return data[options](fnOption);
        };
    }
})(jQuery);