from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

import json


class NotificationConsumer(AsyncConsumer):
   
   async def websocket_connect(self, event):   
      user=self.scope['user']
      self.notification=f"{user.username}"
      await self.channel_layer.group_add(
         self.notification,
         self.channel_name)
      await self.send({
         "type": "websocket.accept",
      })

   async def websocket_receive(self, event):
      print("=========================",event)
      body=event['body']
      from_user=event['from_user']
      for_user=event['for_user']

      if "room_id" in event.keys() :
         room_id=event["room_id"]
      else:
         room_id=False
      if "room_name" in event.keys():
         room_name=event["room_name"]
      else:
         room_name=False

      if "host_username" in event.keys():
         host_username=event["host_username"]
      else:
         host_username=False

      if "roomname" in event.keys():
         roomname=event["roomname"]
      else:
         roomname=False

      response={
            "body": body,
            "from_user": from_user,
            "for_user": for_user,
            "room_id" : room_id,
            "room_name" : room_name,
            "host_username" : host_username,
            "roomname" : roomname
         }
         
      await self.channel_layer.group_send(
         self.notification,
         {
            "type": "send_notification",
            "text" : json.dumps(response)
         })

   async def send_notification(self,event): 
   
      await self.send({                  
         "type": "websocket.send",
         "text": event['text']
         })
   
   async def websocket_disconnect(self,event):
      await self.channel_layer.group_discard(
         self.notification,
         self.channel_name )
      raise StopConsumer()
