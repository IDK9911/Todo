#import path to map for which url to run which index func
from django.urls import path
#import views function in this script
from . import views

urlpatterns=[
    path("",views.IndexView.as_view(),name='home'), #shows the recent tag(created/updated)
    # path("login",views.login), #signup is same as login page but w/o # constraints on passwd match.
    path("signup",views.SignUp.as_view(),name="signup"),
    path("login",views.Login.as_view(),name="login"),
    path("filter/",views.SubjectFilter.as_view(),name='filter'), #This will filter todo items based on their tag.
    path('<slug:slug>/edit',views.EditProject.as_view(),name="editProject"),#include the delete btn in update as well.
    path('<slug:slug>/delete',views.DeleteProject.as_view(),name="delProject"),
     path("<slug:slug>/",views.getTask,name='task_pg'),   #shows the content for a specific tag suchs as subtasks.
     path('tasks/new',views.AddTodo.as_view(),name="addTodo"),
     path("recents",views.recentPosts,name='recents'), #This will give u post that were updated recently.
     path("thankyou",views.thank_you)
     
]
"""
urlpatterns=[
    path("",views.index,name='home'), #shows the recent tag(created/updated)
     path("<int:task_id>/",views.getTask,name='task_pg'),   #shows the content for a specific tag suchs as subtasks.
     path("tag/<subject>",views.subjectFilter), #This will filter todo items based on their tag.
     path("recents",views.recentPosts,name='recents') #This will give u post that were updated recently.
]


"""
# some errors like reverse ones would occur if the slug field is empty
# make a page which would give u some statistics on the database. 
# to look at consistency.