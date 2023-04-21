from django.shortcuts import render, redirect
from django.http import HttpResponse
# Importar formularios UserCreationForm - AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Guaradr usuarios
from django.contrib.auth.models import User
# Cookies del user
from django.contrib.auth import login, logout, authenticate
# Manejar excepciones
from django.db import IntegrityError
# Formulario creado para Task
from .forms import TaskForm
# Listar Tareas
from .models import Task
#404 Errores
from django.shortcuts import get_object_or_404
# Fechas
from django.utils import timezone
# validar rutas que algun usuario no puede entrar
from django.contrib.auth.decorators import login_required


# Create your views here.

# Home


def home(request):
    return render(request, 'home.html')


# Vista que envio un formulario
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crear User y cifrar pr django
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                # Guardar
                user.save()
                # Guardar session en cookies
                login(request, user)
                # retornar exito
                # return HttpResponse('User created successfully')
                # Redireccionar a la vista
                return redirect('tasks')
            except IntegrityError:  # Considerar excepciones con IntegrityError
                # return HttpResponse('User name already exist')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })

# Tareas pendientes
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) 
    return render(request, 'tasks.html', {
        'tasks' : tasks
    })

#Tareas completas
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks' : tasks
    })



# Crear tareas
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form' : TaskForm
        })
    else:
        try:
            # print(request.POST)
            form = TaskForm(request.POST)        
            new_task = form.save(commit=False)
            new_task.user = request.user
            # print(new_task)
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form' : TaskForm,
                'error' : 'Please provide valida data'
            })



# Detalle tarea
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # task = Task.objects.get(id=task_id) # puede ser ID o PK igual funcionan
        # task = Task.objects.get(pk=task_id, user=request.user)
        #Listo las tareas pertenecientes al usuario conectado
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task' : task,
            'form' : form
        })
    else:
        try:
            # print(request.POST)
            #Obtengo los datos del form, y valido que solo los creados por el user se puedan acutalizar
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # Toma los nuevos datos actualizados del formulario
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{
                'task' : task,
                'form' : form,
                'error' : 'Error updating task'
            })
    

# Completar tarea
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


#Eliminar tarea
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


# Cerrar sesion

@login_required
def signout(request):
    logout(request)
    return redirect('home')


# login
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # print(request.POST)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error' : 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
