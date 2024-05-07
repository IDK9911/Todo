from django import forms
from .models import Todo,SubTask,User


#Subtask form
class ItemForm(forms.Form):
    task_desc=forms.CharField(label="Add Task",max_length=65,error_messages={
        "required":"Task items can't be empty",
        "max-length":"65 character or less"
    })

"""
Todo Form
todo table
user_id int #temporarily hard-coded
task_id int
task_desc text  #?
task_deadline YYYY/MM/DD #?
created_time YYYY/MM/DD HH:MM:SS
last_edited YYYY/MM/DD HH:MM:SS 
status enum(1,0) #?
Tag enum(health,study,fitness,errands,mental_health,academic,professional) #?
"""

class AddTodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['task_desc','status','tag','task_deadline']
        labels={
            'task_desc':'Todo item',
            'status':'Status',
            'tag':'Choose a Tag',
            'task_deadline':'Deadline'
        }
        error_messages={
            "task_desc":{
                "required":"Todo item must have name",
                "min-length":"Todo must have lenght >=3",
                "max-length":"Todo must have lenght <=65"
            },
            'tag':{
                "required":"set a status",   
            },
            'task_deadline':{
                "required":"Datetime field can't be empty"
            }
        }
        widgets = {
            'task_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class FilterForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['status','tag','task_deadline']
        labels={
            'task_desc':'Todo item',
            'status':'Status',
            'tag':'Choose a Tag',
            'task_deadline':'deadline'
        }
        error_messages={
            "task_desc":{
                "required":"Todo item must have name",
                "min-length":"Todo must have lenght >=3",
                "max-length":"Todo must have lenght <=65"
            },
            'tag':{
                "required":"set a status",   
            },
            'task_deadline':{
                "required":"Datetime field can't be empty"
            }
        }
        widgets = {
            'task_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class EditProjectForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['task_desc','status','tag','task_deadline']
        labels={
            'task_desc':'Edit Todo item',
            'status':'Status',
            'tag':'Choose a Tag',
            'task_deadline':'deadline'
        }
        error_messages={
            "task_desc":{
                "required":"Todo item must have name",
                "min-length":"Todo must have lenght >=3",
                "max-length":"Todo must have lenght <=65"
            },
            'tag':{
                "required":"set a status",   
            },
            'task_deadline':{
                "required":"Datetime field can't be empty"
            }
        }
        widgets = {
            'task_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class UserLoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        exclude=['name']
        labels={
            'username':'email',
            'password':'password'
        }
        error_messages={
            'username':{"required":"Invalid email"},
            'password':{
                "required":"Password can't be Empty",
                "minlength":"password must be 8 character long."
            }

        }
        widgets = {
        'password': forms.PasswordInput(),
         }

class UserInfoForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['name','username','password']
        labels={
            'name':"what's your name?",
            'username':'email id',
            'password':'password'
        }
        error_messages={
            'name':{"required":"Name cant be empty"},
            'username':{"required":"Invalid email"},
            'password':{
                "required":"Password can't be Empty",
                "minlength":"password must be 8 character long."
            }

        }
        widgets = {
        'password': forms.PasswordInput(),
         }
    def clean_password(self):
        password = self.cleaned_data.get('password')
        print(password,len(password))
        if len(password) <= 7:  
            raise forms.ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):  # Check for at least one digit
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in password):  # Check for at least one alphabetic character
            raise forms.ValidationError("Password must contain at least one letter.")
        return password
        
#ValueError: dictionary update sequence element #0 has length 1; 2 is required, it comes when u not 
#format it well.


         