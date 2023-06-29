const hide_friend_btn=document.getElementById('hide-friend-btn')
const show_friend_btn=document.getElementById('show-friend-btn')
const first_div=document.getElementById('first-div')
const sec_div=document.getElementById('second-div')


show_friend_btn.addEventListener('click',function(){
    sec_div.style['display']='none';
    first_div.style['width']='96%';
    first_div.style['display']='inline-block'
})

hide_friend_btn.addEventListener('click',function(){
    first_div.style['display']='none';
    sec_div.style['display']='inline-block';
})