from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom,Message
import json
from datetime import datetime
import pytz


class ChatRoomConsumer(AsyncConsumer):
   async def websocket_connect(self, event):
      
      await self.user_active_status()
      room=self.scope['url_route']['kwargs']['room_name']
      self.chatroom=f"{room}"
      await self.channel_layer.group_add(
         self.chatroom,
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
            msg_id=await self.create_message(user=user)

         response={
            'message': self.msg,
            'user':email,
            'msg_id':msg_id
         }
         
         await self.channel_layer.group_send(
            self.chatroom,
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
         self.chatroom,
         self.channel_name )
      raise StopConsumer()

   @database_sync_to_async
   def user_active_status(self):
      self.scope['user'].save()
      
   @database_sync_to_async
   def create_message(self,user):
      user.save()
      try:
         room=ChatRoom.objects.get(id=self.chatroom)
      except:
         room=False
      if room:
         msg=Message.objects.create(
            body=self.msg,
            room=room,
            user=user )
         msg.visible_to.add(room.participant1,room.participant2)
         return msg.id
      
   