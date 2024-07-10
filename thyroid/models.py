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
    
class Location(models.Model):
    latnum = models.FloatField()
    longnum = models.FloatField()

    def __str__(self):
        return f"Latitude: {self.latnum}, Longitude: {self.longnum}"
    

class PatientData(models.Model):
    patient_id = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    on_thyroxine = models.BooleanField()
    query_on_thyroxine = models.BooleanField()
    on_antithyroid_meds = models.BooleanField()
    sick = models.BooleanField()
    pregnant = models.BooleanField()
    thyroid_surgery = models.BooleanField()
    I131_treatment = models.BooleanField()
    query_hypothyroid = models.BooleanField()
    query_hyperthyroid = models.BooleanField()
    lithium = models.BooleanField()
    goitre = models.BooleanField()
    tumor = models.BooleanField()
    hypopituitary = models.FloatField(null=True, blank=True)  # Allow null values
    psych = models.BooleanField()
    TSH_measured = models.BooleanField()
    TSH = models.FloatField(null=True, blank=True)  # Allow null values
    T3_measured = models.BooleanField()
    T3 = models.FloatField(null=True, blank=True)  # Allow null values
    TT4_measured = models.BooleanField()
    TT4 = models.FloatField(null=True, blank=True)  # Allow null values
    T4U_measured = models.BooleanField()
    T4U = models.FloatField(null=True, blank=True)  # Allow null values
    FTI_measured = models.BooleanField()
    FTI = models.FloatField(null=True, blank=True)  # Allow null values
    TBG_measured = models.BooleanField()
    TBG = models.FloatField(null=True, blank=True)  # Allow null values
    referral_source = models.CharField(max_length=100)
    target = models.CharField(max_length=50)

    def __str__(self):
        return self.patient_id