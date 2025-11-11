from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class Person(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    age = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    denomination = models.CharField(max_length=100, null=True, blank=True)
    division = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    hobbies = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    father = models.CharField(max_length=100, blank=True, null=True)
    mother = models.CharField(max_length=100, blank=True, null=True)
    likes = models.IntegerField(default=0)
    intrests = models.IntegerField(default=0)
    jobtype = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=400, null=True, blank=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Intrests(models.Model):
    sender = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="sent_interests"
    )
    receiver = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="received_interests"
    )
    date_time = models.DateTimeField(auto_now=True)
    status = models.CharField(default="Pending", max_length=100)

    def formatted_date_time(self):
        # Format the date and time as per your requirement
        return self.date_time.strftime("%I:%M %p, %d %B %Y")


class Chat(models.Model):
    sender = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="sent_user"
    )
    receiver = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="received_user"
    )
    message = models.CharField(max_length=300)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(
        null=True, auto_now=True
    )  # Stores both date and time

    def __str__(self):
        return self.message


class Likes(models.Model):
    liker = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="given_likes",  # Helps in querying likes given by the user
    )
    liked = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="received_likes",  # Helps in querying likes received by the user
    )
    datetime = models.DateTimeField(auto_now=True)
class Package(models.Model):
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=500)
    price=models.CharField(max_length=100)
class Membership(models.Model):
    user= models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="join_membership"
    )
    pack= models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="membershi_details"
    )
    date=models.DateField(auto_now=True)
    status=models.CharField(max_length=50)
class Payment(models.Model):
    
   
    mid=models.ForeignKey(
        Membership, on_delete=models.CASCADE, related_name="membershi_details"
    )
    date=models.DateField(auto_now=True)
    status=models.CharField(max_length=50)

