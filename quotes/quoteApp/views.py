from django.contrib import messages
from django.shortcuts import redirect, render
from quoteApp.models import User, Quote, Like
import bcrypt


def index(request):
    print('*'*30)
    print('index route')
    context = {
    }
    if 'user' not in request.session: 
        #If user exists, send to quote
        messages.error(request, 'You are NOT logged')
        return render(request,'quotes/index.html')
    
    return redirect('/quotes') 

def register(request):
    print('*'*30)
    print('Register')

    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        print("Post register ",request.POST)
        
        errors = User.objects.reg_validation(request.POST)
        print(errors)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        else:
            encrypted_pwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()

            user = User.objects.create(
            first_name = request.POST['fname'],
            last_name = request.POST['lname'],
            email = request.POST['email'].lower(),
            password = encrypted_pwd
            )

            session_user = {
                'id': user.id,
                'name' : user.first_name + ' ' + user.last_name,
                'email' : user.email.lower()
            }
            
            print(session_user)
            request.session['user'] = session_user
            return redirect('/quotes') 

def login(request):
    print('*'*30)
    print('log in')
    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        print("Post register ",request.POST)
        errors = User.objects.log_validation(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        else:
            user = User.objects.get(email = request.POST['email'].lower())
            session_user = {
                'id' : user.id,
                'name' : user.first_name + ' ' + user.last_name,
                'email' : user.email.lower()
            }
            print(session_user)
            request.session['user'] = session_user
            return redirect('/quotes')

def logout(request):
    print('*'*30)
    print('Clean session')
    
    if 'user' not in request.session: 
        messages.error(request, 'You are NOT logged')
    else:
        del request.session['user']
    return redirect('/')   

def quotes(request):
    print('*'*30)
    print('The quote path')
    print(request.session['user'])
    #Access when there is a session opens
    if 'user' not in request.session:
        return redirect('/')
    
    if request.method == "GET":
        context = {
            'name': request.session['user']['name'],
            'quotes' : Quote.objects.all().order_by('-created_at'),
            'likes' : Like.objects.all()
        }
        print(context)    
        return render(request,'quotes/quotes.html', context)
        
    if request.method == "POST":
        print("Post register ",request.POST)
        errors = Quote.objects.quote_validation(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/quotes')
        else:
            new_quote = Quote.objects.create(
                quote = request.POST['quote'],
                author = request.POST['author'],
                posted_by = User.objects.get(id=request.session['user']['id'])
                )
            return redirect('/quotes')


def edit(request, id_user):
    if request.method == "GET":
        context = {
            'user' : User.objects.get(id=id_user)
        }
        return render(request,'quotes/edit.html', context)

    if request.method == "POST":
        print("Edit register ",request.POST)
        errors = User.objects.edit_validation(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/myaccount/{id_user}')
        else:
            #validate unique mail
            user_mail = User.objects.get(id=id_user)
            if request.POST['email'].lower() != user_mail.email:
                if User.objects.exclude().filter(email = request.POST['email'].lower()).exists():
                    message_error = "Email already exists."
                    messages.error(request, message_error)
                    return redirect(f'/myaccount/{id_user}')
                else:
                    new_user = User.objects.get(id=id_user)
                    new_user.first_name = request.POST['fname']
                    new_user.last_name = request.POST['lname']
                    new_user.email = request.POST['email'].lower()
                    new_user.save()

                    session_user = {
                        'id' : new_user.id,
                        'name' : new_user.first_name + ' ' + new_user.last_name,
                        'email' : new_user.email.lower()
                    }
                    request.session['user'] = session_user
                    return redirect('/quotes')
            else:
                new_user = User.objects.get(id=id_user)
                new_user.first_name = request.POST['fname']
                new_user.last_name = request.POST['lname']
                new_user.save()

                session_user = {
                    'id' : new_user.id,
                    'name' : new_user.first_name + ' ' + new_user.last_name,
                    'email' : new_user.email.lower()
                }
                request.session['user'] = session_user
                return redirect('/quotes')


def user(request, id_user):
    user_id = User.objects.get(id=id_user)
    context = {
        'name' : user_id.first_name + ' ' + user_id.last_name,
        'user_quotes' : user_id.user_quoted.all()
    }
    print(context)
    return render(request, 'quotes/user.html', context)

def delete_quote(request, quote_id):
    print('*'*30)
    print('delete quote')
    quote_del = Quote.objects.get(id=quote_id)
    quote_del.delete()
    return redirect('/quotes')

def update_quote(request, quote_id):
    print('*'*30)
    print('update quote')

    if len(Like.objects.filter(user__id=request.session['user']['id']).filter(quote__id=quote_id)) == 0:
        quote_create =  Like.objects.create(
            user =  User.objects.get(id=request.session['user']['id']),
            quote = Quote.objects.get(id=quote_id))
        
    update_quote = Quote.objects.get(id=quote_id)
    n_likes = Like.objects.filter(quote=update_quote).count()
    update_quote.likes = n_likes
    update_quote.save()
    return redirect('/quotes')