var canvas = document.getElementById("draw");

var ctx = canvas.getContext("2d");
// resize();

// // resize canvas when window is resized
// function resize() {
//     let rect = canvas.getBoundingClientRect();
// //   ctx.canvas.width = window.innerWidth;
// //   ctx.canvas.height = window.innerHeight;
//     ctx.canvas.width = 720
//     ctx.canvas.height = 405
// }

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }
  

// initialize position as 0,0
var pos = { x: 0, y: 0 };

// new position from mouse events
function setPosition(e) {
    let rect = canvas.getBoundingClientRect();

    pos.x = e.clientX - rect.left;
    pos.y = e.clientY - rect.top;
}

function draw(e) {
  if (e.buttons !== 1) return; // if mouse is not clicked, do not go further

  var color = document.getElementById("hex").value;

  ctx.beginPath(); // begin the drawing path

  ctx.lineWidth = 20; // width of line
  ctx.lineCap = "round"; // rounded end cap
  ctx.strokeStyle = color; // hex color of line

  ctx.moveTo(pos.x, pos.y); // from position
  setPosition(e);
  ctx.lineTo(pos.x, pos.y); // to position

  ctx.stroke(); // draw it!
}


// add window event listener to trigger when window is resized
// window.addEventListener("resize", resize);

// add event listeners to trigger on different mouse events
document.addEventListener("mousemove", draw);
document.addEventListener("mousedown", setPosition);
document.addEventListener("mousedown", draw);
document.addEventListener("mouseenter", setPosition);

function save() {
    document.getElementById('my_hidden').value = canvas.toDataURL('image/png');
    document.forms["canvasForm"].submit();
}