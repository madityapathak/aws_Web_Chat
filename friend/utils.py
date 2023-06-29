from .models import Friend_request

def get_friend_req_or_false(sender,reciever):
    try:
        if len(Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=True))>1:
            Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=True).exclude(pk=Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=True).last().pk).delete()
        if len(Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=False))>1:
            Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=False).exclude(pk=Friend_request.objects.filter(sender=sender,reciever=reciever,is_active=False).last().pk).delete()
        return Friend_request.objects.get(sender=sender,reciever=reciever,is_active=True)
    except Friend_request.DoesNotExist:
        return False




