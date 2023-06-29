from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import GroupChatRoom,GroupMessage
from notifications.models import Notification
import json


class GroupChatRoomConsumer(AsyncConsumer):
   async def websocket_connect(self, event):
      await self.user_active_status()
      group=self.scope['url_route']['kwargs']['room_name']
      self.groupchatroom=f"{group}"
      await self.channel_layer.group_add(
         self.groupchatroom,
         self.channel_name)
      await self.send({
         "type": "websocket.accept",
      })

   async def websocket_receive(self, event):   
      rtext=event.get('text',None)
      email='default'
      user=self.scope['user']
      if rtext is not None:
         data=json.loads(rtext)
         self.msg=data.get('message')
         if user.is_authenticated:
            email=user.email
            msg_id=await self.create_group_message(user=user)
            

         response={
            'message': self.msg,
            'user':email,
            'msg_id':msg_id
         }
         
         await self.channel_layer.group_send(
            self.groupchatroom,
            {
               "type": "chat_message",
               "text" : json.dumps(response)
            })

   async def chat_message(self,event): 
      await self.send({                  
         "type": "websocket.send",
         "text": event['text']})
   
   async def websocket_disconnect(self,event):
      await self.user_active_status()
      await self.channel_layer.group_discard(
         self.groupchatroom,
         self.channel_name )
      raise StopConsumer()

   @database_sync_to_async
   def user_active_status(self):
      self.scope['user'].save()




   
   @database_sync_to_async
   def create_group_message(self,user):
      user.save()
      try:
         room=GroupChatRoom.objects.get(id=self.groupchatroom)
      except:
         room=False
      if room:
         if user not in room.participants.all():
            room.participants.add(user)
            
            for participant in room.participants.all():
               if participant != user:
                  Notification.objects.create(
                     from_user=user,
                     for_user=participant,
                     room_group=room,
                     body="user joined group"    )
                     
            Notification.objects.create(
               from_user=room.host,
               for_user=user,
               room_group=room,
               body="you joind"    )
     
         mesg=GroupMessage.objects.create(
            body=self.msg,
            room=room,
            user=user )
         return mesg.id
