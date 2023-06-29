show_rest_btn=document.querySelector('.show-restricted-user-btn')
show_part_btn=document.querySelector('.show-participants-btn')
block_back_btn=document.querySelector('.block-back-btn')
participant_back_btn=document.querySelector('.participants-back-btn')
restricted_user_btn=document.querySelector('.restricted-users-btn')
participant_btn=document.querySelector('.participants-btn')
block_list_div=document.querySelector('.block-list-div')
chat_box=document.querySelector('.chat-box-div')
participants_div=document.querySelector('.participants-div')



restricted_user_btn.addEventListener('click',function(){
    chat_box.style['display']='none';
    block_list_div.setAttribute('style','display: block !important;')
    block_list_div.style['width']='97%';
})

participant_btn.addEventListener('click',function(){
    chat_box.style['display']='none';
    participants_div.setAttribute('style','display: block !important;')
    participants_div.style['width']='97%';
})
show_rest_btn.addEventListener('click',function(){
    participants_div.style['display']='none';
    block_list_div.style['display']='block';
    block_list_div.style['width']='29%';
})
show_part_btn.addEventListener('click',function(){
    block_list_div.style['display']='none';
    participants_div.style['display']='block';
    participants_div.style['width']='29%';
})

participant_back_btn.addEventListener('click',function(){
    participants_div.style['display']='none'
    chat_box.style['display']='block'
})
block_back_btn.addEventListener('click',function(){
    block_list_div.style['display']='none'
    chat_box.style['display']='block'
})
