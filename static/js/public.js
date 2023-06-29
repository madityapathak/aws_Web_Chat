show_room=document.getElementById('view-your-rooms')
back_btn=document.getElementById('back-btn')
second_div=document.querySelector(".second-div")
first_div=document.querySelector(".first-div")



show_room.addEventListener('click',function(){
    second_div.style['display']='none';
    first_div.style['width']='97%';
    first_div.style['display']='block';
})







back_btn.addEventListener('click',function(){
    first_div.style['display']='none';
    second_div.style['width']='97%';
    second_div.style['display']='block';  
})