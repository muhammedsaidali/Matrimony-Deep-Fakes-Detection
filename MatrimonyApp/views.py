from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.db.models import Max, F
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from .models import *
import ast


# Create your views here.


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def signin(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        data = authenticate(username=email, password=passw)
        if data is not None:
            login(request, data)
            print("Data")
            if data.is_active:
                if data.userType == "User":
                    print("User")
                    id = data.id
                    request.session["uid"] = id
                    messages.success(request, "Login Success")
                    resp = '<script>alert("Login Success"); window.location.href = "/userHome";</script>'
                    return HttpResponse(resp)
                elif data.userType == "Admin":
                    print("Admin")
                    messages.success(request, "Login Success")
                    return redirect("/adminHome")
            else:
                print("Sorry You Are Not Approved")
                messages.error(request, "Sorry You are Not Approved")
                return redirect("/login")
        else:
            resp = '<script>alert("Sorry You Are Not Approved..😥");window.location.href="/login"</script>'
            return HttpResponse(resp)
    return render(request, "COMMON/login.html")

def register(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        gender = request.POST["gender"]
        city = request.POST["city"]
        age = request.POST["age"]
        password = request.POST["password"]
        image = request.FILES["imgfile"]

        if Login.objects.filter(username=email).exists():
            return HttpResponse('<script>alert("Email Already Exists");</script>')
        else:
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="User",
                viewPass=password,
                is_active=0,
            )
            logQry.save()
            regQry = Person.objects.create(
                name=name,
                email=email,
                phone=phone,
                loginid=logQry,
                image=image,
                gender=gender,
                age=age,
                city=city,
            )
            regQry.save()
            messages.success(request, "Registration Successfull")
            from django.urls import reverse
            return redirect(reverse('login'))  # ✅ this avoids 301 redirect issues


    return render(request, "COMMON/register.html")



def commonBase(request):
    return render(request, "COMMON/commonBase.html")

# -----------------------------------# ADMIN #-----------------------------------#
def adminHome(request):
    newData = Person.objects.filter(loginid__is_active=0)
    approvedData = Person.objects.filter(loginid__is_active=1)
    print(approvedData)
    if "sub" in request.POST:
        pname=request.POST["pname"]
        desc=request.POST["desc"]
        price=request.POST["price"]
        obj=Package.objects.create(name=pname,desc=desc,price=price)
        obj.save()
    packagedata=Package.objects.all()
    return render(
        request,
        "ADMIN/admin-dashboard.html",
        {"newData": newData, "approvedData": approvedData,"packagedata":packagedata},
    )


def approveUser(request):
    id = request.GET["id"]
    approve = Login.objects.filter(id=id).update(is_active=1)
    return HttpResponse(
        "<script>alert('Approved');window.location.href='/adminHome/'</script>"
    )


def rejectUser(request):
    id = request.GET["id"]
    reject = Login.objects.filter(id=id).update(is_active=0)
    return HttpResponse(
        "<script>alert('Rejected');window.location.href='/adminHome/'</script>"
    )


# -----------------------------------# USER #-----------------------------------#


def userHome(request):
    uid = request.session["uid"]
    print("Loginid", uid)
    mydata = Person.objects.get(loginid__id=uid)
    print(mydata)
    matchData = Person.objects.filter(~Q(gender=mydata.gender))
    print(matchData)
    pendingRequest = Intrests.objects.filter(
        Q(receiver__loginid=uid) & Q(status="Pending")
    )
    approvedRequest = Intrests.objects.filter(
        Q(receiver__loginid=uid) & Q(status="Approved")
    )
    rejectedRequest = Intrests.objects.filter(
        Q(receiver__loginid=uid) & Q(status="Rejected")
    )
    myRequests = Intrests.objects.filter(Q(sender__loginid=uid))
    print(pendingRequest)
    print(approvedRequest)
    print(rejectedRequest)
    print(myRequests)
    return render(
        request,
        "USER/user-dashboard.html",
        {
            "mydata": mydata,
            "matchData": matchData,
            "pendingRequest": pendingRequest,
            "approvedRequest": approvedRequest,
            "rejectedRequest": rejectedRequest,
            "myRequests": myRequests,
        },
    )


def profile(request):
    uid = request.session["uid"]
    mydata = Person.objects.get(loginid__id=uid)
    mem=Membership.objects.filter(user=mydata)
    memb=""
    if mem:
        memb=mem[0].pack.name
    return render(request, "USER/user-profile.html", {"mydata": mydata,"mem":memb})


@csrf_exempt
def uploadProfilePic(request):
    uid = request.session["uid"]
    if request.FILES:
        print("HIIII")
        image = request.FILES["file"]
        update = Person.objects.get(loginid__id=uid)
        update.image = image
        update.save()
        return redirect("/profile")


def editProfile(request):
    uid = request.session["uid"]
    mydata = Person.objects.get(loginid=uid)
    hobbies = [
        "Modelling",
        "Watching",
        "Movies",
        "Playing",
        "Volleyball",
        "Hangout with Family",
        "Adventure Travel",
        "Books Reading",
        "Music",
        "Cooking",
        "Yoga",
    ]
    hobbies_list = []
    if mydata.hobbies:
        try:
            hobbies_list = ast.literal_eval(mydata.hobbies)
        except (SyntaxError, ValueError) as e:
            print(f"Error evaluating string as Python literal: {e}")
    print(hobbies_list)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["pswd"]
        gender = request.POST["gender"]
        city = request.POST["city"]
        dob = request.POST["dob"]
        age = request.POST["age"]
        division = request.POST["division"]
        denomination = request.POST["denomination"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        fname = request.POST["fname"]
        mname = request.POST["mname"]
        address = request.POST["address"]
        jobtype = request.POST["jobtype"]
        cname = request.POST["cname"]
        education = request.POST["education"]
        about = request.POST["about"]
        hobbies = request.POST.getlist("hobbies")
        print("Hobbies", hobbies)

        # Updating Data

        userData = Person.objects.get(loginid=uid)
        userData.name = name
        userData.email = email
        userData.phone = phone
        userData.gender = gender
        userData.age = age
        userData.city = city
        userData.dob = dob
        userData.division = division
        userData.denomination = denomination
        userData.height = height
        userData.weight = weight
        userData.father = fname
        userData.mother = mname
        userData.address = address
        userData.jobtype = jobtype
        userData.company = cname
        userData.education = education
        userData.about = about
        userData.hobbies = hobbies
        userData.save()
        logData = Login.objects.get(id=uid)
        if password:
            logData.set_password(password)
        logData.username = email
        logData.save()
        return redirect("/editProfile")

    return render(
        request,
        "USER/user-profile-edit.html",
        {"mydata": mydata, "hobbies_list": hobbies_list, "hobbies": hobbies},
    )


def profileDetails(request):
    import deepfake4 as dp
    stat=""
    id = request.GET["id"]
    uid = request.session["uid"]
    profData = Person.objects.get(id=id)
    img="static/media/"+str(profData.image)
    result=dp.predict_fake(img)
    print(result)
    if profData.dob=="":
        stat="Fraud profile"
    if profData.age=="":
        stat="Fraud profile"
    if profData.father=="":
        stat="Fraud profile"
    if profData.mother=="":
        stat="Fraud profile"
    if profData.jobtype=="":
        stat="Fraud profile"

    case = request.GET.get("case")
    hobbies_list = []
    # like checking
    print("Check", uid, id)
    likeData = Likes.objects.filter(Q(liker__loginid=uid) & Q(liked=id))
    print(likeData, "Like Data")
    # like checking end
    if profData.hobbies:
        try:
            hobbies_list = ast.literal_eval(profData.hobbies)
        except (SyntaxError, ValueError) as e:
            print(f"Error evaluating string as Python literal: {e}")
    print(hobbies_list)

    chatData = Chat.objects.filter(
        (Q(sender__loginid=uid) & Q(receiver=id))
        | (Q(receiver__loginid=uid) & Q(sender=id))
    ).order_by("id")
    print(chatData)

    return render(
        request,
        "USER/profile-details.html",
        {
            "profData": profData,
            "hobbies_list": hobbies_list,
            "case": case,
            "chatData": chatData,
            "uid": uid,
            "likeData": likeData,"stat":stat,"result":result
        },
    )


def send_interest(request):
    rid = request.GET.get("id")
    uid = request.session["uid"]
    receiver_id = Person.objects.get(id=rid)  # receiver
    sender_id = Person.objects.get(loginid=uid)  # sender

    if Intrests.objects.filter(
        Q(sender_id=sender_id) & Q(receiver=receiver_id)
    ).exists():
        print("Already Sent")
        return HttpResponse(
            "<script>alert('Interest already sent');window.location.href='/profileDetails/?id={}'</script>".format(
                rid
            )
        )
    else:
        receiver_id.intrests += 1
        receiver_id.save()
        sendIntrest = Intrests.objects.create(sender=sender_id, receiver=receiver_id)
        sendIntrest.save()
    return redirect(f"/profileDetails/?id={rid}")


def approveIntrest(request):
    id = request.GET["id"]
    approveReq = Intrests.objects.filter(id=id).update(status="Approved")
    return HttpResponse(
        "<script>alert('Interest Accepted');window.location.href='/userHome';</script>"
    )


def rejectIntrest(request):
    id = request.GET["id"]
    approveReq = Intrests.objects.filter(id=id).update(status="Rejected")
    return HttpResponse(
        "<script>alert('Interest Rejected');window.location.href='/userHome';</script>"
    )


def chat(request):
    uid = request.session["uid"]
    time = datetime.now().time()
    date = datetime.now().date()
    formatted_time = time.strftime("%I:%M %p")
    formatted_date = date.strftime("%B %d")
    userId = Person.objects.get(loginid=uid)
    print("Hey")
    if request.method == "POST":
        print("Hiii")
        message = request.POST["chat_message"]
        rid = request.POST["rid"]
        receiverId = Person.objects.get(id=rid)
        print(message)
        print(rid)

        send_message = Chat.objects.create(
            sender=userId,
            receiver=receiverId,
            message=message,
            date=formatted_date,
            time=formatted_time,
            type="right",
        )
        send_message.save()
        return JsonResponse(
            {
                "status": "success",
                "message": "Message sent successfully",
                "newmsg": message,
            }
        )
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"})


# def chatList(request):
#     uid = request.session["uid"]
#     print("Loginid", uid)
#     mydata = Person.objects.get(loginid__id=uid)
#     print(mydata)
#     chatData = Chat.objects.filter(Q(sender__loginid=uid) | Q(receiver__loginid=uid))
#     print(chatData)

#     # Find users who have messaged you
#     users_messaged_you = (
#         Chat.objects.filter(receiver__loginid=uid)
#         .values_list("sender_id", "sender__name")
#         .distinct()
#     )

#     # Find users whom you have messaged
#     users_you_messaged = (
#         Chat.objects.filter(sender__loginid=uid)
#         .values_list("receiver_id", "receiver__name")
#         .distinct()
#     )

#     # Combine the results into a single list of unique users
#     unique_users = set(users_messaged_you) | set(users_you_messaged)

#     # Filter out the current user from the final list
#     unique_users = [
#         {"id": user[0], "name": user[1]} for user in unique_users if user[0] != uid
#     ]

#     print("Users who messaged you:", users_messaged_you)
#     print("Users whom you messaged:", users_you_messaged)
#     print("Combined unique users:", unique_users)
#     return render(
#         request, "USER/chat-list.html", {"mydata": mydata, "users": unique_users}
#     )


def chatList(request):
    uid = request.session["uid"]
    print("Loginid", uid)
    mydata = Person.objects.get(loginid__id=uid)
    print(mydata)

    # Get all relevant chat messages
    all_chats = (
        Chat.objects.filter(Q(sender__loginid=uid) | Q(receiver__loginid=uid))
        .values(
            "sender_id",
            "receiver_id",
            "message",
            "time",
            "timestamp",
            "sender__name",
            "receiver__name",
            "receiver__image",
        )
        .order_by("-timestamp")
    )

    # Process and group messages
    unique_users = {}
    for chat in all_chats:
        # print(chat)
        # Determine the other user's ID and name
        other_user_id = (
            chat["sender_id"] if chat["sender_id"] != uid else chat["receiver_id"]
        )
        other_user_name = (
            chat["sender__name"] if chat["sender_id"] != uid else chat["receiver__name"]
        )

        # Update the latest message for each user
        if (
            other_user_id not in unique_users
            or chat["timestamp"] > unique_users[other_user_id]["last_timestamp"]
        ):
            unique_users[other_user_id] = {
                "id": other_user_id,
                "name": other_user_name,
                "last_message": chat["message"],
                "last_time": chat["time"],
                "last_timestamp": chat["timestamp"],
                "image": chat["receiver__image"],
            }

    # Convert to list format
    unique_users_list = list(unique_users.values())
    print(unique_users_list)

    return render(
        request, "USER/chat-list.html", {"mydata": mydata, "users": unique_users_list}
    )


def like(request):
    uid = request.session["uid"]
    liker = Person.objects.get(loginid=uid)
    id = request.GET["id"]
    liked = Person.objects.get(id=id)
    if not Likes.objects.filter(Q(liker=liker) & Q(liked=liked)).exists():
        addLike = Likes.objects.create(liker=liker, liked=liked)
        addLike.save()
        liked.likes += 1
        liked.save()
    else:
        print("Hii")
    return redirect(f"/profileDetails?id={id}")


def dislike(request):
    uid = request.session["uid"]
    liker = Person.objects.get(loginid=uid)
    id = request.GET["id"]
    liked = Person.objects.get(id=id)

    disLike = Likes.objects.filter(Q(liker=liker) & Q(liked=liked)).delete()
    liked.likes -= 1
    liked.save()
    return redirect(f"/profileDetails?id={id}")


def allUsers(request):
    uid = request.session["uid"]
    print("Loginid", uid)
    mydata = Person.objects.get(loginid__id=uid)
    print(mydata)
    matchData = Person.objects.filter(~Q(gender=mydata.gender))
    print(matchData)
    if request.POST:
        keyword = request.POST["key"]
        matchData = Person.objects.filter(
            Q(name__icontains=keyword)
            | Q(denomination__contains=keyword)
            | Q(division__contains=keyword)
            | Q(city__contains=keyword)
            | Q(education__contains=keyword)
            | Q(age=keyword)
        )
        print(matchData, "Check")
    return render(
        request,
        "USER/allUsers.html",
        {"matchData": matchData, "mydata": mydata},
    )

def joinmembership(request):
    package=Package.objects.all()
    return render(request,"USER/Joinmembership.html",{"package":package})
def payment(request):
    uid = request.session["uid"]
    mydata = Person.objects.get(loginid__id=uid)
    id=request.GET["id"]
    package=Package.objects.get(id=id)
    obj=Membership.objects.create(user=mydata,pack=package,status='paid')
    obj.save()
    if request.POST:
        return redirect("/userHome/")
    return render(request,"USER/payment.html",{"package":package})