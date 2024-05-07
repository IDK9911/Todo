from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404,HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import datetime
from .seed import todos_data,subtask
from .models import Todo,SubTask,User
from .model_forms import ItemForm,AddTodoForm,FilterForm,EditProjectForm,UserInfoForm,UserLoginForm
from django.db.models import Q
import pytz
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView,CreateView
from django.views.generic.edit import FormView,UpdateView,DeleteView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pdb

# Create your views here.
"""
seed_data=[
    "Setup the project","Setup the urls","Send dynamic content to all urls","update info to the database"
]
#seed_dict={i+1:e for i,e in enumerate(seed_data)}

User table
user_id int , name txt, username txt

todo table
user_id int
task_id int
task_desc text
task_deadline YYYY/MM/DD
created_time YYYY/MM/DD HH:MM:SS
last_edited YYYY/MM/DD HH:MM:SS
status enum(1,0)
Tag enum(health,study,fitness,errands,mental_health,academic,professional)

subtask table

subtask_id int primary key
task_id int 
parent_id int
subtask_desc text
created_time YYYY:MM:DD HH:MM:SS

taskid range form 1 to 20, in this table we can have many subtask_id with the same task. 
and parent_id refers to the task_id


"""

def get_date(field):
    def myfunc(obj):
        return obj[field]
    return myfunc

def getAllTasks(user_id,field):
    tasks=getUserTasks(user_id)
    #created a factory func to sort the data baed on task_deadline.
    myfunc=get_date(field)
    tasks.sort(key=myfunc)
    return (tasks)



# class SignUp(CreateView):
#     model=User
#     form_class=UserInfoForm
#     template_name="tasks/signup.html"
#     success_url="/"
    

        
"""
def index(request):
    #identify user using user_id
    user_id=1
    #
    tasks=getAllTasks(user_id,'task_deadline')

    #two_weeks=datetime.date.today()+datetime.timedelta(weeks=2)
    ctime=datetime.date.today()

    try:
        return render(request,"tasks/index.html",{"tasks":tasks,"pg_name":"home","ctime":ctime});           
    except:
        raise Http404()
"""

def index(request):
    #identify user using user_id
    user_id=1
    #
    todos=Todo.objects.all()
    ctime=timezone.now()

    try:
        return render(request,"tasks/index.html",{"tasks":todos,"pg_name":"home","ctime":ctime});           
    except:
        raise Http404("Getting some error")

class IndexView(TemplateView):
    #class-level-variable
    template_name="tasks/index.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        #Database acess
        todos=Todo.objects.all().order_by('-last_edited','status')
        #Accessing libraries
        ctime=timezone.now()
        #initialization
        context["tasks"]=todos
        context["pg_name"]="class"
        context["ctime"]=ctime
        return context


"""
def recentPosts(request):
    #identify user using user_id
    user_id=1
    #
    tasks=getAllTasks(user_id,'last_edited')
    two_weeks=datetime.date.today()+datetime.timedelta(weeks=2)
    try:
        return render(request,"tasks/index.html",{"tasks":tasks[::-1],"pg_name":"home","two_weeks":two_weeks});           
    except:
        raise Http404()

"""

def recentPosts(request):
    #identify user using user_id
    user_id=1
    tasks=Todo.objects.filter(user=user_id).order_by("-last_edited")
    try:
        return render(request,"tasks/index.html",{"tasks":tasks,"pg_name":"home"});           
    except:
        raise Http404()

def getUserTasks(uuid):
    mylist=[]
    for e in todos_data:
        if e['user_id']==uuid:
            mylist.append(e)
    return mylist

def getSubTask(task_id):
    mylist=[]
    for e in subtask:
        if e['task_id']==task_id:
            mylist.append(e)
    return mylist

def getTaskInfo(task_id):
    for e in todos_data:
        if e['task_id']==task_id:
            return e
    return None

"""
def calcPercentage(start_time,deadline):

    if datetime.datetime.today()<deadline:
        #total duration
        duration=deadline - start_time
        duration=(duration.total_seconds()/3600)
        #time left
        time_used=datetime.datetime.today()-start_time
        time_used=(time_used.total_seconds()/3600)
        return round((time_used/duration)*100)
    else:
        return "100"
"""
def calcPercentage(start_time, deadline):
    today = timezone.now()
    
    if today < deadline:
        #total duration
        duration = deadline - start_time
        duration_hours = duration.total_seconds() / 3600
        #time used
        time_used = today - start_time
        time_used_hours = time_used.total_seconds() / 3600
        
        return round((time_used_hours / duration_hours) * 100,4)
    else:
        return 100
"""
def getTask(request,task_id):
    id=task_id
    task=getTaskInfo(id)
    subtasks=getSubTask(id)
    #two_weeks=datetime.date.today()+datetime.timedelta(weeks=2)
    percent=calcPercentage(task['created_time'],task['task_deadline'])
    ctime=datetime.date.today()
    try:
        #return HttpResponse(tasks)
        return render(request,"tasks/tasks.html",{"tasks":[task],"subtasks":subtasks,"pg_name":"home","percent":percent,"ctime":ctime});           
    except:
        raise Http404()    
    
"""
"""
def getTask(request,slug):
    #here slug is task id
    
    task=get_object_or_404(Todo,slug=slug)
    subtasks=SubTask.objects.filter(task_id=task.task_id)
    percent=calcPercentage(task.created_time,task.task_deadline)
    ctime=datetime.datetime.today()

    return render(request,"tasks/tasks.html",
    {"tasks":[task],"subtasks":subtasks,"pg_name":"home","percent":percent,"ctime":timezone.now(),"slug":slug});           


"""
def getTask(request,slug):
    #here slug is task id
    flag=False
    if request.method=='POST':
        form=ItemForm(request.POST)
        
        """
        task_desc=request.POST['task_desc']
        task_id=request.POST['task_id']
        print(task_desc,task_id) #working.
        """

        flag=True
        if form.is_valid():
            print(form.cleaned_data)
            task_desc = form.cleaned_data['task_desc']

            task_id=request.POST['task_id']
            todo = Todo.objects.get(pk=task_id)
            SubTask.objects.create(subtask_desc=task_desc, task_id=todo)
    else:
        pass
    # if the form is here because of post request. Send the post Req form and any possible errors
    if(not(flag)):
        form=ItemForm()

    task=get_object_or_404(Todo,slug=slug)
    subtasks=SubTask.objects.filter(task_id=task.task_id)
    percent=calcPercentage(task.created_time,task.task_deadline)
    ctime=datetime.datetime.today()
    return render(request,"tasks/tasks.html",
    {"tasks":task,"subtasks":subtasks,"pg_name":"home","percent":percent,"ctime":timezone.now(),"slug":slug,"form":form});           



#fix the timezone to the hour level. It is on UTC, to work on my local time. It's 5:30 min behind.
#The server is storing in utc. So they are 5:30 min behind. 
# def addTodo(request):
    
#     if request.method=='POST':
#         form=AddTodoForm(request.POST)
#         print('i AM IN')
#         if form.is_valid():
#             print("hello",form.cleaned_data['task_desc'],form.cleaned_data['task_deadline'])
# #            return HttpResponse("keep working")
#             form.save()
#             headline=1
#             #Headline tells the user that prev record was saved successfully. 
#         else:
#              headline=0
#     else:
#         headline=0
#         form=AddTodoForm()    
    
#     return render(request,"tasks/new.html",{"form":form,"headline":headline})


class AddTodo(View):
    template_name = 'tasks/new.html'
    form_class = AddTodoForm

    def get(self, request):
        form = self.form_class()
        headline = 0
        headline = 1 if request.GET.get(headline) else 0

        return render(request, self.template_name, {'form': form, 'headline': headline})

    def post(self, request):
        form = self.form_class(request.POST)
        headline = 0
        if form.is_valid():
            print("hello", form.cleaned_data['task_desc'], form.cleaned_data['task_deadline'])
            form.save()
            headline = 1
            # return redirect('/')  
            return render(request, self.template_name, {'form': form, 'headline': headline})    

        return render(request, self.template_name, {'form': form, 'headline': headline})


class SignUp(View):
    form_class=UserInfoForm
    template_name="tasks/signup.html"
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Save the user object without committing to the database
            username=form.cleaned_data['username']
            #User matching query does not exist.
            #use filter instead of get for even a single request
            if User.objects.filter(username=username).exists():
                form.add_error('username', "This username is already taken")
                #if username does exist keep him on the signup page
                return render(request,self.template_name,{'form':form})
            else:
                if(request.POST['password']==request.POST['password_2']):
                    user = form.save(commit=False)
                    # Hash the password before saving
                    print(request.POST)
                    print("clean_data if user doesn't exist \n",form.cleaned_data)
                    password = form.cleaned_data['password']
                    # user.password=make_password(user.password)
                    user.password=user.password

                    user.save()
                        # Redirect to the success URL after signup
                    #if username doesn't exist send him to login page.
                    return HttpResponseRedirect(reverse("login"))
                else:
                    form.add_error("passwords do not match")
                
            print('form is not valid')
            return render(request,self.template_name,{'form':form})

    
"""
class Login(View):
    form_class=UserLoginForm
    template_name="tasks/login.html"
    def get(self,request):
        print("i sent a get request to login form")
        form=self.form_class()
        return render(request,self.template_name,{'form':form,"pg_name":"login"})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            #Here i am getting an error of Already exists.
            #That is because the field Username is unique. 
            #We need to get pass that.
            print("am in the login form")
            #User.objects.get(username=request.POST.get('username'))
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['login_username']=username
                data=request.session.get('login_username')
                return redirect('/',{"data":data})  # Redirect to home page after successful login
            else:
                # Authentication failed
                messages.success(request,('There was an error logging in'))
                form.add_error(None, "Invalid username or password")
        else:
            print("form is not valid somehow?")
            messages.error(request, 'There was an error logging in')

            return render(request, self.template_name, {'form': form, "pg_name": "login"})

"""

class Login(View):
    form_class=UserLoginForm
    template_name="tasks/login.html"
    def get(self,request):
        print("i sent a get request to login form")
        form=self.form_class()
        return render(request,self.template_name,{'form':form,"pg_name":"login"})
    def post(self,request):
        form=self.form_class(request.POST)
        # if form.is_valid():
        """
        Here i am getting an error of Already exists.
        That is because the field Username is unique. 
        We need to get pass that.
        """
        print("am in the login form")
        #User.objects.get(username=request.POST.get('username'))
        username = request.POST['username']
        password = request.POST['password']
        print("is cleaned data working,",username,password)
        user = authenticate(request, username=username, password=password)  
        print(user)
        if user is not None:
            print("is user not none?")
            login(request, user)
            request.session['login_username']=username
            data=request.session.get('login_username')
            return redirect('/',{"data":data})  # Redirect to home page after successful login
        else:
            # Authentication failed
            messages.success(request,('There was an error logging in'))
            form.add_error(None, "Invalid username or password")
            return render(request,self.template_name,{"form":form})
       









def thank_you(req):
    return HttpResponse("Keep working")


# def subjectFilter(request):
#     #two form items based on tags and status
#     #GOTO model_forms.py
#     if request.method=='POST':
#         #if field1 and field2 and field3
#         #if field1 and field2
#         #if field2 and field3
#         #if field1 and field3
#         #if field1
#         #if field2
#         #if field3
#         form=FilterForm(request.POST)
#         operation=request.POST['operation']
#         if form.is_valid():
#             tag=request.POST['tag']
#             status=request.POST['status']
#             task_deadline=request.POST['task_deadline']
#             print(task_deadline)
#             if(operation=='AND'):
#                 op=andOperation(tag,status,task_deadline)
#             else:
#                 op=orOperation(tag,status,task_deadline)
#             return render(request,"tasks/filter.html",{"form":form,"tasks":op})
#     form=FilterForm()
#     return render(request,"tasks/filter.html",{"form":form})



class SubjectFilter(View):
    
    def post(self,request):
        #retrieving data
        form=FilterForm(request.POST)

        tag=request.POST.get('tag')
        status=request.POST.get('status')
        task_deadline=request.POST.get('task_deadline')
        operation=request.POST.get('operation')

        if(operation=='AND'):
            op=self.andOperation(tag,status,task_deadline)
        else:
            op=self.orOperation(tag,status,task_deadline)
        return render(request,"tasks/filter.html",{"form":form,"tasks":op})
    def get(self,request):
        form=FilterForm()
        return render(request,"tasks/filter.html",{"form":form})

    
    def orOperation(self,tag,status,task_deadline):
        #--- Converting my local timezone to utc to compare with server data.
        #if task_deadline:
        #   utc_datetime=localToUtc(task_deadline)
        #--
        today=timezone.now()
        filter_query = Q()

        # Add conditions for each field if it's not None
        if tag:
            filter_query |= Q(tag=tag)
        if status!='':
            filter_query |= Q(status=status)
        if task_deadline:
            filter_query &= Q(task_deadline__lt=task_deadline,task_deadline__gt=today)
        # print("hello-------------------",task_deadline)
        # Filter based on the constructed query
        #return Todo.objects.filter(Q(tag=tag)|Q(status=status)|Q(task_deadline__lt=task_deadline))    
        return Todo.objects.filter(filter_query)    

    def andOperation(self,tag,status,task_deadline):
        #arg1 is the tag
        #arg2 is the status
        #arg3 is the b from [a,b], where a is now +- 5h:30min
        today=timezone.now()
        if tag:
            obj=Todo.objects.filter(tag=tag)    
        if status!='':
            obj=obj.filter(status=status)
        if task_deadline:
            obj=obj.filter(task_deadline__lt=task_deadline,task_deadline__gt=today)
        return obj    


        

def localToUtc(task_deadline):
    # Assuming your datetime object is in local time
    local_datetime = task_deadline

    # Localize the datetime object to your local timezone
    local_timezone = pytz.timezone('Asia/Kolkata')
    localized_datetime = local_timezone.localize(local_datetime)

    # Convert the localized datetime object to UTC
    utc_datetime = localized_datetime.astimezone(pytz.utc)
    return utc_datetime

    

# def orOperation(tag,status,task_deadline):
#     #--- Converting my local timezone to utc to compare with server data.
#     #if task_deadline:
#      #   utc_datetime=localToUtc(task_deadline)
#     #--
#     today=timezone.now()

#     filter_query = Q()

#     # Add conditions for each field if it's not None
#     if tag:
#         filter_query &= Q(tag=tag)
#     if status!='':
#         filter_query &= Q(status=status)
#     #if task_deadline:
#      #   filter_query &= Q(task_deadline__lt=task_deadline,task_deadline__gt=today)
#     print("hello-------------------",task_deadline)
#     # Filter based on the constructed query
#     return Todo.objects.filter(Q(tag=tag)|Q(status=status)|Q(task_deadline__lt=task_deadline))



# def editProject(request,slug):
#     form=EditProjectForm()
#     if request.method=='POST':
#         existing_data=Todo.objects.get(slug=slug)
#         form=EditProjectForm(request.POST,instance=existing_data)

#         if form.is_valid():
#             form.save()
#             return render(request,"/")
#     else:
#         obj=Todo.objects.get(slug=slug)

#     return render(request,'tasks/edit.html',{"form":form,"obj":obj})

class EditProject(UpdateView):
    model = Todo
    form_class = EditProjectForm
    template_name = 'tasks/edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = '/'  

    def form_valid(self, form):
        # logic to execute after the form is successfully validated and saved
        return super().form_valid(form)

class DeleteProject(DeleteView):
    model = Todo
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url ='/'  # redirect URL after successful deletion



"""
def index(request):
    return render(request,"tasks/index.html",{"data":seed_data,"pg_name":"home"});   

def home(request):
    return render(request,"challenges/index.html",{"months":goals})

def index(request,month):
    try:
        text=goals[month]
    except:
        return HttpResponseNotFound('I got here first 404 not found')
    return render(request,"challenges/challenge.html",{"text":text,"pg_name":month})

def index_num(request,month):
    month=month%5
    months=list(goals.keys())
    redirect_month=months[month-1]
    op=reverse("contest",args=[redirect_month])
    return HttpResponseRedirect(op)



def home(request):
    response_data=""
    for months in goals.keys():
        link=reverse("contest",args=[months])    
        response_data+="<li><a href={l}>{m}</a></li><br>".format(m=months.capitalize(),l=link)
    response_data="<ul>{d}</ul>".format(d=response_data)
    return HttpResponse(response_data)
"""