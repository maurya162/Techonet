from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    LostItem,
    FoundItem,
    Claim,
    ChatRoom,
    Message
)


# HOME PAGE

def index(request):

    return render(request, 'index.html')


# REGISTER

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'register.html',
                {
                    'error':
                    'Username already exists'
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(
            request,
            "Registration Successful!"
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# LOGIN

def login_user(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        role = request.POST.get(
            'role'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # =========================
            # ADMIN LOGIN
            # =========================

            if role == "admin":

                if user.is_superuser:

                    login(request, user)

                    messages.success(
                        request,
                        "Admin Login Successful!"
                    )

                    return redirect(
                        '/admin/'
                    )

                else:

                    return render(
                        request,
                        'login.html',
                        {
                            'error':
                            'You are not admin'
                        }
                    )

            # =========================
            # USER LOGIN
            # =========================

            else:

                login(request, user)

                messages.success(
                    request,
                    "Login Successful!"
                )

                # REDIRECT TO SAME PAGE

                next_url = request.GET.get(
                    'next'
                )

                if next_url:

                    return redirect(
                        next_url
                    )

                # DEFAULT REDIRECT

                return redirect(
                    'dashboard'
                )

        # =========================
        # INVALID LOGIN
        # =========================

        else:

            return render(
                request,
                'login.html',
                {
                    'error':
                    'Invalid Username or Password'
                }
            )

    # =========================
    # GET REQUEST
    # =========================

    return render(
        request,
        'login.html'
    )


# DASHBOARD

@login_required(login_url='login')
def dashboard(request):

    # CHAT NOTIFICATIONS

    chat_rooms = (
        ChatRoom.objects.filter(
            user1=request.user
        ) |
        ChatRoom.objects.filter(
            user2=request.user
        )
    ).exclude(
        user1=request.user,
        user2=request.user
    )
    message_count = Message.objects.exclude(
    sender=request.user
    ).count()

    context = {

        'chat_rooms': chat_rooms,
        'message_count': message_count,

    }

    return render(
        request,
        'dashboard.html',
        context
    )
from .models import Message


# LOGOUT

def logout_user(request):

    logout(request)

    return redirect('index')


# REPORT LOST ITEM

@login_required(login_url='login')
def report_lost(request):

    if request.method == 'POST':

        item_name = request.POST.get('item_name')

        category = request.POST.get('category')

        description = request.POST.get('description')

        location = request.POST.get('location')

        date_lost = request.POST.get('date_lost')

        contact = request.POST.get('contact')

        image = request.FILES.get('image')

        LostItem.objects.create(
            user=request.user,
            item_name=item_name,
            category=category,
            description=description,
            location=location,
            date_lost=date_lost,
            contact=contact,
            image=image
        )

        return redirect('lost_items')

    return render(
        request,
        'report_lost.html'
    )


# LOST ITEMS

@login_required(login_url='login')
def lost_items(request):

    items = LostItem.objects.all().order_by('-id')

    return render(
        request,
        'lost_items.html',
        {
            'items': items
        }
    )


# REPORT FOUND ITEM

@login_required(login_url='login')
def report_found(request):

    if request.method == 'POST':

        item_name = request.POST.get('item_name')

        category = request.POST.get('category')

        description = request.POST.get('description')

        location = request.POST.get('location')

        date_found = request.POST.get('date_found')

        contact = request.POST.get('contact')

        image = request.FILES.get('image')

        FoundItem.objects.create(
            user=request.user,
            item_name=item_name,
            category=category,
            description=description,
            location=location,
            date_found=date_found,
            contact=contact,
            image=image
        )

        return redirect('found_items')

    return render(
        request,
        'report_found.html'
    )


# FOUND ITEMS

@login_required(login_url='login')
def found_items(request):

    items = FoundItem.objects.all().order_by('-id')

    return render(
        request,
        'found_items.html',
        {
            'items': items
        }
    )


# ALL ITEMS

@login_required(login_url='login')
def all_items(request):

    lost_items = LostItem.objects.all().order_by('-id')

    found_items = FoundItem.objects.all().order_by('-id')

    context = {

        'lost_items': lost_items,

        'found_items': found_items,

    }

    return render(
        request,
        'all_items.html',
        context
    )


# LOST ITEM DETAIL

@login_required(login_url='login')
def lost_item_detail(request, id):

    item = get_object_or_404(
        LostItem,
        id=id
    )

    return render(
        request,
        'lost_item_detail.html',
        {
            'item': item
        }
    )


# FOUND ITEM DETAIL

@login_required(login_url='login')
def found_item_detail(request, id):

    item = get_object_or_404(
        FoundItem,
        id=id
    )

    return render(
        request,
        'found_item_detail.html',
        {
            'item': item
        }
    )


# EDIT LOST ITEM

@login_required(login_url='login')
def edit_lost_item(request, id):

    item = get_object_or_404(
        LostItem,
        id=id
    )

    if request.method == 'POST':

        item.item_name = request.POST.get(
            'item_name'
        )

        item.category = request.POST.get(
            'category'
        )

        item.description = request.POST.get(
            'description'
        )

        item.location = request.POST.get(
            'location'
        )

        item.contact = request.POST.get(
            'contact'
        )

        if request.FILES.get('image'):

            item.image = request.FILES.get(
                'image'
            )

        item.save()

        return redirect(
            'lost_item_detail',
            id=item.id
        )

    return render(
        request,
        'edit_lost_item.html',
        {
            'item': item
        }
    )


# DELETE LOST ITEM

@login_required(login_url='login')
def delete_lost_item(request, id):

    item = get_object_or_404(
        LostItem,
        id=id
    )

    item.delete()

    return redirect('lost_items')


# EDIT FOUND ITEM

@login_required(login_url='login')
def edit_found_item(request, id):

    item = get_object_or_404(
        FoundItem,
        id=id
    )

    if request.method == 'POST':

        item.item_name = request.POST.get(
            'item_name'
        )

        item.category = request.POST.get(
            'category'
        )

        item.description = request.POST.get(
            'description'
        )

        item.location = request.POST.get(
            'location'
        )

        item.contact = request.POST.get(
            'contact'
        )

        if request.FILES.get('image'):

            item.image = request.FILES.get(
                'image'
            )

        item.save()

        return redirect(
            'found_item_detail',
            id=item.id
        )

    return render(
        request,
        'edit_found_item.html',
        {
            'item': item
        }
    )


# DELETE FOUND ITEM

@login_required(login_url='login')
def delete_found_item(request, id):

    item = get_object_or_404(
        FoundItem,
        id=id
    )

    item.delete()

    return redirect('found_items')


# CLAIM ITEM

@login_required(login_url='login')
def claim_item(request, item_name):

    if request.method == 'POST':

        claimant_name = request.POST.get(
            'name'
        )

        claimant_email = request.POST.get(
            'email'
        )

        claimant_phone = request.POST.get(
            'phone'
        )

        message = request.POST.get(
            'message'
        )

        Claim.objects.create(
            item_name=item_name,
            claimant_name=claimant_name,
            claimant_email=claimant_email,
            claimant_phone=claimant_phone,
            message=message
        )

        return render(
            request,
            'claim_success.html'
        )

    return render(
        request,
        'claim_item.html',
        {
            'item_name': item_name
        }
    )


# PROFILE PAGE

@login_required(login_url='login')
def profile(request):

    # TOTAL COUNTS

    lost_count = LostItem.objects.filter(
        user=request.user
    ).count()

    found_count = FoundItem.objects.filter(
        user=request.user
    ).count()

    # USER ITEMS

    lost_items = LostItem.objects.filter(
        user=request.user
    ).order_by('-id')

    found_items = FoundItem.objects.filter(
        user=request.user
    ).order_by('-id')

    # RECENT ITEMS

    recent_lost = LostItem.objects.filter(
        user=request.user
    ).order_by('-id')[:3]

    recent_found = FoundItem.objects.filter(
        user=request.user
    ).order_by('-id')[:3]

    # CHAT ROOMS
    # SELF CHAT REMOVE

    chat_rooms = (
        ChatRoom.objects.filter(
            user1=request.user
        ) |
        ChatRoom.objects.filter(
            user2=request.user
        )
    ).exclude(
        user1=request.user,
        user2=request.user
    )

    # CONTEXT

    context = {

        'lost_count': lost_count,

        'found_count': found_count,

        'lost_items': lost_items,

        'found_items': found_items,

        'recent_lost': recent_lost,

        'recent_found': recent_found,

        'chat_rooms': chat_rooms,
    }

    return render(
        request,
        'profile.html',
        context
    )

    # CHAT ROOM

@login_required(login_url='login')
def chat_room(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    # FIND ROOM

    room = ChatRoom.objects.filter(
        user1=request.user,
        user2=other_user
    ).first()

    if not room:

        room = ChatRoom.objects.filter(
            user1=other_user,
            user2=request.user
        ).first()

    # CREATE ROOM

    if not room:

        room = ChatRoom.objects.create(
            user1=request.user,
            user2=other_user
        )

    # SEND MESSAGE

    if request.method == 'POST':

        msg = request.POST.get('message')

        if msg:

            Message.objects.create(
                room=room,
                sender=request.user,
                message=msg
            )

    # ALL MESSAGES

    messages_list = Message.objects.filter(
        room=room
    ).order_by('created_at')

    return render(
        request,
        'chat_room.html',
        {
            'room': room,
            'messages_list': messages_list,
            'other_user': other_user
        }
    )