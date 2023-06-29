const container=document.querySelector('.container')

const menuBtn = document.querySelector('.menu-btn');


let menuOpen = false;
menuBtn.addEventListener('click', () => {
  container.classList.toggle('height');
  if(!menuOpen) {
    menuBtn.classList.add('open');
    menuOpen = true;
  } else {
    menuBtn.classList.remove('open');
    menuOpen = false;
  }
});