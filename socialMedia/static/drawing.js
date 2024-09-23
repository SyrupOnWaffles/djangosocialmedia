var canvas = document.getElementById("draw");

var ctx = canvas.getContext("2d");

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }
  

// initialize position as 0,0
var pos = { x: 0, y: 0 };
var lineWidth = 20;
var color = "#FFFFFF";

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
  ctx.strokeStyle = color; // hex color of line

  ctx.moveTo(pos.x, pos.y); // from position
  setPosition(e);
  ctx.lineTo(pos.x, pos.y); // to position

  ctx.stroke(); // draw it!
}

document.addEventListener("mousemove", draw);
document.addEventListener("mousedown", setPosition);
document.addEventListener("mousedown", draw);
document.addEventListener("mouseenter", setPosition);

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
  color = colour
}

function clearCanvas(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// thanks https://stackoverflow.com/questions/17386707/how-to-check-if-a-canvas-is-blank/17386803#17386803
function isCanvasBlank(canvas) {
  return !canvas.getContext('2d')
    .getImageData(0, 0, canvas.width, canvas.height).data
    .some(channel => channel !== 0);
}