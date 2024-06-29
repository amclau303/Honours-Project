# thyroid/models.py

from django.db import models

class Thyroid(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    YES = 'yes'
    NO = 'no'
    DONT_KNOW = "don't know"
    STATUS_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No'),
        (DONT_KNOW, "Don't Know"),
    ]
    
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    year = models.PositiveIntegerField()
    treatment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="N/A")
    thyroid_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Don't Know")
    
    def __str__(self):
        return f"{self.gender}, {self.year}, {self.treatment_status}, {self.thyroid_status}"
