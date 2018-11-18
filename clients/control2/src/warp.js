const reticle = $('#Reticle')[0];
const centerPiece = $('#Centerpiece_Frame')[0];

function rotate(n, x) {
  n.style['transform'] = `rotate(${x}deg)`;
}

function wobble() {
  if (Math.random() > 0.8) {
    const x = Math.random() * 360;
    rotate(reticle, x);
  }

  if (Math.random() > 0.7) {
    const x = Math.random() * 360;
    rotate(centerPiece, x);
  }
}
$(function() {
    setInterval(wobble, 1000);
});