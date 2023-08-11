from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

from django.http import JsonResponse

Year_of_engineerings = []
Semesters = []
Divisions = []

Batch_ = {
    '0': [],
}

final_selected = {}

def initialization():
    if Year_of_engineerings == []:
        for i in Year_of_engineering.objects.all():
            Year_of_engineerings.append(i.year)

    if Semesters == []:
        for i in Semester.objects.all():
            Semesters.append(i.sem + " ("+i.roman+")")
    
    if Divisions == []:
        for i in Division.objects.all():
            Divisions.append(i.div + " ("+i.num+")")

    if Batch_ == {'0': [],}:
        for i in Year_of_engineering.objects.all():
            batches = []
            for j in Batch_Grp.objects.all():
                if j.year == i:
                    batches.append(j.Name)
            Batch_[i.year] = batches

# Batch = {
#     '0': [],
#     'Second Year (2nd)' : ['E','F','G','H'],
#     'Third Year (3rd)' : ['K','L','M','N'],
#     'Fourth Year (4th)' : ['P','Q','R','S'],
# }

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        initialization()
    Batches = []
    selected = {
        'yr_of_engg': '0',
        'sem': '0',
        'div': '0',
        'batch': '0',
    }
    if request.method == "POST" and request.POST['select_batch'] == "1":
        yr = request.POST['Year_of_engineering']
        div = request.POST['Division']
        sem = request.POST['Semester']
        selected['yr_of_engg'] = yr
        selected['sem'] = sem
        selected['div'] = div
        for i in Batch_[yr]:
            Batches.append(i+str(Divisions.index(div)+1))
        select_batch = 0
    else:
        if request.method == "POST":
            yr = request.POST['Year_of_engineering']
            div = request.POST['Division']
            sem = request.POST['Semester']
            batch = request.POST['Batch']
            # selected['yr_of_engg'] = yr
            # selected['sem'] = sem
            # selected['div'] = div
            # selected['batch'] = batch
            final_selected['yr_of_engg'] = yr
            final_selected['sem'] = sem
            final_selected['div'] = div
            final_selected['batch'] = batch
            selected = {
                'yr_of_engg': '0',
                'sem': '0',
                'div': '0',
                'batch': '0',
            }
            return redirect(select_batch_fn)
        select_batch = 1
    context = {'title': "Panel", 'Year_of_engineering': Year_of_engineerings, 'Semester': Semesters,
               'Division': Divisions, 'Batch': Batches, 'select_batch': select_batch, 'selected': selected}
    return render(request, 'home.html', context)


def select_batch_fn(request):
    if final_selected == {}:
        messages.warning(request,'Please select the field again')
        return redirect(home)
    
    if Batch.objects.filter(div=Division.objects.get(div=final_selected['div'].split(" ")[0]),batch_grp=Batch_Grp.objects.get(Name=final_selected['batch'][0])).exists():
        batch = Batch.objects.get(div=Division.objects.get(div=final_selected['div'].split(" ")[0]),batch_grp=Batch_Grp.objects.get(Name=final_selected['batch'][0]))
    else:
        messages.error(request,str(final_selected)+' : Batch does not exist')
        return redirect(home)
    
    batches = Lab.objects.filter(batch=batch)
    sub = Subject.objects.filter(sem = Semester.objects.get(sem=final_selected['sem'].split(" ")[0]))
    final_batches = []
    for i in batches:
        if i.sub in sub:
            final_batches.append(i)
    context = {'batches':final_batches,'final_selected':final_selected,'title':'Select Batch'}
    return render(request,'select_batch.html',context)

def assesment(request, pk,pk_1):
    if request.method == 'POST':
        practical = Practical.objects.get(id=pk_1)
        if Assesment.objects.filter(practical=practical,student=Student.objects.get(roll_no=request.POST['roll_no'])).exists():
            assesment = Assesment.objects.get(practical=practical,student=Student.objects.get(roll_no=request.POST['roll_no']))
            assesment.date_of_performance = request.POST['dop']
            assesment.date_of_submission = request.POST['dos']
            assesment.RPP = request.POST['RPP']
            assesment.SPO = request.POST['SPO']
            assesment.save()
        else:
            assesment = Assesment.objects.create(practical=practical,student=Student.objects.get(roll_no=request.POST['roll_no']),date_of_performance=request.POST['dop'],date_of_submission=request.POST['dos'],RPP=request.POST['RPP'],SPO=request.POST['SPO'])
            assesment.save()
        messages.success(request,'Data Updated Successfully')
    if pk_1 != '0':
        practical = Practical.objects.get(id=pk_1)
    else:
        practical = 0
    lab = Lab.objects.get(id=pk)
    # print(batch)
    practicals = []
    for i in Practical.objects.filter(sub=lab.sub):
        practicals.append(i)
    assesment = Assesment.objects.filter(practical=practical)
    # print(assesment)
    students = Student.objects.filter(batch=lab.batch)
    # print(students)
    assesment_students = []
    for i in assesment:
        if i.student in students:
            assesment_students.append(i.student)
    # print(assesment_students)
    context = {'title':'Assesment','lab':lab,'practicals':practicals,'practical':practical,'assesment':assesment,'students':students,'intersection': (assesment_students)}
    return render(request,'assesment.html',context)

def get_info(request):
    roll_no = request.GET['roll_no']
    student_data = Student.objects.get(roll_no=roll_no)
    subject = Practical.objects.get(id=request.GET['practical']).sub
    practicals = Practical.objects.filter(sub=Subject.objects.get(sub=subject))
    assesments = Assesment.objects.filter(student=student_data)
    Final = dict()
    for i in practicals:
        for j in assesments:
            if i == j.practical:
                    Final[i.practical_num] = True
                    break
            else:
                    Final[i.practical_num] = False
    student_info = {
        'roll no':student_data.roll_no,
        'Name' : student_data.Name,
        'Batch' : {
            'div' : {
                'div': student_data.batch.div.div,
                'num':student_data.batch.div.num,
            },
            'batch_grp' : {
                'year': {
                    'year':student_data.batch.batch_grp.year.year,
                    'abbrevation':student_data.batch.batch_grp.year.abbrevation,
                },
                'Name': student_data.batch.batch_grp.Name,
            }
        }
    }
    return JsonResponse({'student_info':student_info,'Assesment':Final})