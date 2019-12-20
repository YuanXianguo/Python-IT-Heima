var width = 500,
    height = 250,
    margin = {left:50, top:30, right:20, bottom:20},
    g_width = width - margin.left - margin.right,
    g_height = height - margin.top - margin.bottom;

// 添加svg元素
d3.select("#container")
    .append("svg")
// 设置宽高
    .attr("width", width)
    .attr("height", height)

// 添加g元素
var g = d3.select("svg")
    .append("g")
// 设置偏移
    .attr("transform","translate(" + margin.left + "," + margin.top + ")")

// 定义数据
var data = [1,3,5,7,8,4,3,7]

// 定义x方向缩放
var scale_x = d3.scale.linear()
    .domain([0, data.length-1]) // 设置输入范围

    .range([0, g_width]) // 设置输出范围
// 定义y方向缩放
var scale_y = d3.scale.linear()
    .domain([0, d3.max(data)])
    .range([g_height, 0]) // 浏览器与数学坐标轴方向相反

// 定义生成曲线的函数
var line_generator = d3.svg.line()
    .x(function (d, i) {
        return scale_x(i);  // 对数组下标进行缩放
    })
    .y(function (d) {
        return scale_y(d); // 对数组值进行缩放
    })
    .interpolate("cardinal")  // 指定拟合方式

// 添加线元素：两种方式，d3.select("g").append(),或用变量名g.append()
// d3.selectAll("g")，给多个g元素同时添加元素
d3.select("g")
    .append("path")
    .attr("d",line_generator(data)) //<path d="M0,1L1,3L2,5L3,7L4,8L5,4L6,3L7,7"></path>

// 添加坐标轴，x轴向下偏移，y轴朝向左
var x_axis = d3.svg.axis().scale(scale_x),
    y_axis = d3.svg.axis().scale(scale_y).orient("left");

g.append("g")
.call(x_axis)
.attr("transform", "translate(0," + g_height + ")")

g.append("g")
.call(y_axis)
.append("text")
.text("Price($)")  // 设置标签文字
.attr("transform", "rotate(-90)")  // 旋转-90度
.attr("text-anchor", "end")  // 与坐标轴末尾对齐
.attr("dy", "1em")  // 沿自身y轴偏移1em
