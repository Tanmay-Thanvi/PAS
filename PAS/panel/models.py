from django.db import models

# Create your models here.
class Year_of_engineering(models.Model):
    year = models.CharField(max_length=100)
    abbrevation = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.abbrevation

class Semester(models.Model):
    sem = models.CharField(max_length=50)
    roman = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.sem 
    
class Division(models.Model):
    div = models.CharField(max_length=50)
    num = models.CharField(max_length=10) 

    def __str__(self) -> str:
        return self.div 
    
class Batch_Grp(models.Model):
    year = models.ForeignKey(Year_of_engineering,on_delete=models.CASCADE)
    Name = models.CharField(max_length=2)

    def __str__(self) -> str:
        return self.Name 
    
class Batch(models.Model):
    div = models.ForeignKey(Division,on_delete=models.CASCADE)
    batch_grp = models.ForeignKey(Batch_Grp,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return  self.batch_grp.Name + "" +  self.div.num

class Subject(models.Model):
    sub = models.CharField(max_length=100)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE)
    year = models.ForeignKey(Year_of_engineering,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.sub
    
class Lab(models.Model):
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    sub = models.ForeignKey(Subject,on_delete=models.CASCADE)
    faculty = models.CharField(max_length=100) 
    assistant = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.batch.batch_grp.Name + "" +  self.batch.div.num + " (" + self.sub.sub +") "

class Practical(models.Model):
    sub = models.ForeignKey(Subject,on_delete=models.CASCADE)
    practical_num = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.sub.sub + " - Pr " + str(self.practical_num)
    
class Student(models.Model):
    roll_no = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return str(self.roll_no)
    
class Assesment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    practical = models.ForeignKey(Practical,on_delete=models.CASCADE)
    date_of_performance = models.DateField()
    date_of_submission = models.DateField() 
    RPP = models.IntegerField(default=0)
    SPO = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.student.roll_no) + " - Pr " + str(self.practical.practical_num)