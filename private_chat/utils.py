from .models import ChatRoom
from accounts.models import User

def create_or_get_chatroom(request,pk):
    p1=request.user
    p2=User.objects.get(id=pk)
  
    if ChatRoom.objects.filter(participant1=p1,participant2=p2).exists():
        return ChatRoom.objects.get(participant1=p1,participant2=p2).id
    elif ChatRoom.objects.filter(participant1=p2,participant2=p1).exists():
        return ChatRoom.objects.get(participant1=p2,participant2=p1).id
    else:
        chat_room = ChatRoom.objects.create(participant1=p1,participant2=p2)
        return chat_room.id
    




def chatroom_or_false(request,pk):
    p1=request.user
    p2=User.objects.get(id=pk)
  
    if ChatRoom.objects.filter(participant1=p1,participant2=p2).exists():
        return ChatRoom.objects.get(participant1=p1,participant2=p2).id
    elif ChatRoom.objects.filter(participant1=p2,participant2=p1).exists():
        return ChatRoom.objects.get(participant1=p2,participant2=p1).id
    else:
        return False
    