from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
      name=models.CharField(max_length=200)
      address=models.CharField(max_length=200)
      user=models.ForeignKey(User,on_delete=models.CASCADE)
      created_date=models.DateTimeField(auto_now=True)

      class Meta:
        ordering=['-created_date']

      def __str__(self):
            return self.name

class Service(models.Model):
    name=models.CharField(max_length=255)
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    names=models.CharField(max_length=225)
    tel=models.CharField(max_length=255,default="078064")
    email=models.CharField(max_length=255,default="tee@")
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.names

class Patient(models.Model):
    names=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.names


class RequestAppointment(models.Model):
    STATUS = (("approved", "Approved"), ("pending", "Pending"),("canceled", "Canceled"), ("rejected", "Rejected"))
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    transfer=models.ImageField(default="avatar.jpg")
    status = models.CharField(max_length=123, choices=STATUS, default="pending")
    created_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.patient.names

class ApprovedAppointment(models.Model):
    request=models.ForeignKey(RequestAppointment,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    created_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.request.patient.names
