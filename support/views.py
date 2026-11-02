import json
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST
from orders.models import Order
from support.agents import run_support_agent
from support.models import Conversation, Message


def chat(request,order_id):
    if request.method=="POST":
        data= json.loads(request.body)
        user_message=data.get("message")
        if not user_message:
            return JsonResponse({"error":"Empty Message Set"},status=HTTP_400_BAD_REQUEST)
        order=get_object_or_404(Order,id=order_id,user=request.user)
        conversation,created=Conversation.objects.get_or_create(user=request.user,order=order)
        Message.objects.create(conversation=conversation,role="user",content=user_message)

        #send user message and conversation too LLM
        reply=run_support_agent(user_message,conversation.id,order.id,request.user.id)

        #save the LLM Answers
        Message.objects.create(conversation=conversation,role="assistant",content=reply)
    return JsonResponse({"reply":reply})