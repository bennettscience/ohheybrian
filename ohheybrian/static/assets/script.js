// TODO: clean up mouse tracking animation
let constrain = 20;
let mouseOverContainer = document.querySelector(`#cover`);
let el = document.querySelector(`.face`);

function transforms(x, y, el) {
  let box = el.getBoundingClientRect();
  let calcX = -(y - box.y - (box.height / 2)) / constrain;
  let calcY = (x - box.x - (box.width / 2)) / constrain;
  
  return "perspective(100px) "
    + "   rotateX("+ calcX +"deg) "
    + "   rotateY("+ calcY +"deg) ";
}

function transformElement(el, xyEl) {
  el.style.transform  = transforms.apply(null, xyEl);
}

mouseOverContainer.onmousemove = function(e) {
  let xy = [e.clientX, e.clientY];
  let position = xy.concat([el]);

  window.requestAnimationFrame(function(){
    transformElement(el, position);
  });
};

mouseOverContainer.onmouseleave = function(e) {
  el.style.transform = 'initial';
}
