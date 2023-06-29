var form=document.getElementById("form");
var allowSubmit=false;




form.addEventListener("submit", function(event){
    if(!allowSubmit){
        event.preventDefault()
        var name=document.getElementById("room_name").value.trim()
        var topic=document.getElementById("room_topic").value.trim()
        var des=document.getElementById("description").value.trim()

        if(name.length && topic.length && des.length){
            allowSubmit=true;
            form.submit();
            form.reset() }
        else{
            if(!name.length){
                alert('Room Name is required')
            }
            if(!topic.length){
                alert('Topic of room is required')
            }
            if(!des.length){
                alert('A short descripttion is required')
            }
        }
    
    }
})

