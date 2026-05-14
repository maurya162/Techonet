from django.db import models
from django.contrib.auth.models import User


# LOST ITEM MODEL

class LostItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField()

    location = models.CharField(
        max_length=200
    )

    date_lost = models.DateField()

    contact = models.CharField(
        max_length=20
    )

    image = models.ImageField(
        upload_to='lost_items/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.item_name


# FOUND ITEM MODEL

class FoundItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField()

    location = models.CharField(
        max_length=200
    )

    date_found = models.DateField()

    contact = models.CharField(
        max_length=20
    )

    image = models.ImageField(
        upload_to='found_items/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.item_name


# CLAIM MODEL

class Claim(models.Model):

    item_name = models.CharField(
        max_length=200
    )

    claimant_name = models.CharField(
        max_length=200
    )

    claimant_email = models.EmailField()

    claimant_phone = models.CharField(
        max_length=20
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.claimant_name


# CHAT ROOM MODEL

class ChatRoom(models.Model):

    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_user1'
    )

    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_user2'
    )

    lost_item = models.ForeignKey(
        LostItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    found_item = models.ForeignKey(
        FoundItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user1} - {self.user2}"


# MESSAGE MODEL

class Message(models.Model):

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.sender.username