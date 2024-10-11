var canvas = document.getElementById("draw");

var ctx = canvas.getContext("2d");

// initialize position as 0,0
var pos = { x: 0, y: 0 };
var lineWidth = 20;
ctx .strokeStyle = "#FFFFFF";

// new position from mouse events
function setPosition(e) {
    let rect = canvas.getBoundingClientRect();

    pos.x = e.clientX - rect.left;
    pos.y = e.clientY - rect.top;
}

function draw(e) {
  if (e.buttons !== 1) return; // if mouse is not clicked, do not go further

  ctx.beginPath(); // begin the drawing path

  ctx.lineWidth = lineWidth; // width of line
  ctx.lineCap = "round"; // rounded end cap
   // hex color of line

  ctx.moveTo(pos.x, pos.y); // from position
  setPosition(e);
  ctx.lineTo(pos.x, pos.y); // to position

  ctx.stroke(); // draw it!
}

canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mousedown", setPosition);
canvas.addEventListener("mousedown", draw);
canvas.addEventListener("mouseenter", setPosition);

canvas.addEventListener("touchstart", draw);
canvas.addEventListener("touchstart", setPosition);
canvas.addEventListener("touchmove", draw);
canvas.addEventListener("touchmove", setPosition);


function save() {
    if(isCanvasBlank(canvas)==false){
      document.getElementById('my_hidden').value = canvas.toDataURL('image/png');
      document.forms["canvasForm"].submit();
    }
}

function changeSize(size){
  lineWidth = size
}

function changeColor(colour){
  ctx.strokeStyle = colour;
}

function clearCanvas(){
  // changeSize(20)
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// thanks https://stackoverflow.com/questions/17386707/how-to-check-if-a-canvas-is-blank/17386803#17386803
function isCanvasBlank(canvas) {
  return !canvas.getContext('2d')
    .getImageData(0, 0, canvas.width, canvas.height).data
    .some(channel => channel !== 0);
}