var canvas,pen;
canvas = document.getElementById('myCanvas');
pen = canvas.getContext('2d');

pen.lineWidth = 1;
pen.strokeStyle = "blue";

var mousePress = false;  //判断鼠标是否按下
var last = null;  //记录最后一个点，即下一次起始点

// 获得鼠标按下的点，即下一次终止点
function pos(event){
	var x,y;
	x = event.clientX;
	y = event.clientY;
	return{
		x,y
	}
}

function start(event){
	mousePress = true;
}

function draw(event){
	if(!mousePress) return;
	var next = pos(event);
	if(last != null){
		pen.beginPath();
		pen.moveTo(last.x,last.y);
		pen.lineTo(next.x,next.y);
		pen.stroke();
	}
	last = next;
}

function finish(event){
	mousePress = false;
	last = null;
}

canvas.onmousedown = start;
canvas.onmousemove = draw;
canvas.onmouseup = finish;