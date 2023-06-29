from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomsSerilizer,UsersSerilizer


from public_chat.models import GroupChatRoom
from accounts.models import User



@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api : endpoints_list',

        'GET /api/users : all_users_endpoint',
        'GET /api/user/<str:id> : each_user_detail_endpoint',
        
        'GET /api/rooms : rooms_list_endpoint',
        'GET /api/room/<str:id> : each_room_detail_endpoint'
    ]
    return Response(routes)

@api_view(['GET'])
def getAllUsers(request):
    users=User.objects.all()
    serializer=UsersSerilizer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request,pk):
    try:
        user=User.objects.get(id=pk)
    except:
        user=False
    if user:
        serializer=UsersSerilizer(user, many=False)
        return Response(serializer.data)
    else:
        routes=["Invalid Endpoint"]
        return Response(routes)
    

@api_view(['GET'])
def getAllRooms(request):
    users=GroupChatRoom.objects.all()
    serializer=RoomsSerilizer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    try:
        user=GroupChatRoom.objects.get(id=pk)
    except:
        user=False
    if user:
        serializer=RoomsSerilizer(user, many=False)
        return Response(serializer.data)
    else:
        routes=["Invalid Endpoint"]
        return Response(routes)