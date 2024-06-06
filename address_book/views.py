from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.contrib import messages
from .forms import UpdateContact, SignUpForm, UpdateUserForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Update User
def update_user(request):
	if request.user.is_authenticated:
		# Get current user
		current_user = User.objects.get(id=request.user.id)
		# Create our form
		user_form = UpdateUserForm(request.POST or None, instance=current_user)
	
		if user_form.is_valid():
			# Update and Save user info
			user_form.save()
			# Log user back in
			login(request, current_user)
			messages.success(request, "Your User Info Has Been Updated!")
			return redirect('home')
		return render(request, 'update_user.html', {'user_form':user_form})
	else:
		messages.success(request, "Must Be Logged In To View That Page...")
		return redirect('login')

# Update User Password
def update_password(request):
	if request.user.is_authenticated:
		#get the current user
		current_user = request.user
		
		# Did they post? Or are they viewing the page
		if request.method == "POST":
			# Define our form
			form = ChangePasswordForm(current_user, request.POST)
			# is form valid
			if form.is_valid():
				#save the form info
				form.save()
				# re-login the user
				login(request,current_user)
				# Success message
				messages.success(request, "Your Password Has Been Updated!")
				return redirect('update_user')
			else:
				# loop thru error messages
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			# Define our form
			form = ChangePasswordForm(current_user)
			return render(request, 'update_password.html', {"form":form})

	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

# Login
def login_user(request):
	if request.method == "POST":
		# They filled out the form, do something
		# Grab form info
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		# Is user correct?
		if user is not None:
			login(request,user)
			messages.success(request, "Login Succesful! Welcome!")
			return redirect('home')
		else:
			messages.success(request, "Whoops!  Looks Like There Was A Problem... Try Again!")
			return redirect('login')

		
	else:
		return render(request, 'login.html', {})

# Logout
def logout_user(request):
	# Log out user
	logout(request)
	messages.success(request, "Logout Succesful! Come Back Soon...")
	return redirect('home')


# Register
def register_user(request):
	# Grab the register form
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Log them in
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# Authenticate
			user = authenticate(username=username, password=password)
			# Log them in
			login(request, user)
			messages.success(request, "Login Succesful! Welcome!")
			return redirect('home')
		else:
			messages.success(request, "Whoops!  Looks Like There Was A Problem... Try Again!")
			return redirect('register')

	else:
		return render(request, 'register.html', {'form':form})


# Home page
def home(request):
	if request.user.is_authenticated:
		# Get all contacts
		#contacts = Contact.objects.all()
		# Get specific contacts for each user
		contacts = Contact.objects.filter(user=request.user)
		return render(request, 'home.html', {"contacts":contacts})
	else:
		return redirect('login')

# About Page
def about(request):
	return render(request, 'about.html', {})


# Individual Contact Page
@login_required()
def contact(request, pk):
	contact = get_object_or_404(Contact, id=pk)
	form = UpdateContact(request.POST or None, request.FILES or None, instance=contact)

	# Save Updated info
	if form.is_valid():
		# Check for correct user
		if request.user == contact.user:
			# Save the form
			form.save()
			# Success Message
			messages.success(request, "The Contact Has Been Updated!")
			# Redirect To Homepage
			return redirect('home')
		else:
			messages.success(request, "You Are Not Authorized To Edit That Contact")
			return redirect('home')
	else:
		return render(request, 'contact.html', {"contact":contact, "form":form})

	#return render(request, 'contact.html', {"contact":contact, "form":form})



# Delete a contact record
@login_required()
def delete_contact(request, pk):
	contact = get_object_or_404(Contact, id=pk)
	# delete contact
	names = f"{contact.first_name} {contact.last_name}"
	
	# Check for correct user
	if request.user == contact.user:
		# Delete Message
		contact.delete()
		# Message
		messages.success(request, f"{names} Has Been Deleted!")
		return redirect('home')
	else:
		messages.success(request, "You Are Not Authorized To Delete That Contact...")
		return redirect('home')


# Add A New Contact
def add_contact(request):
	form = UpdateContact(request.POST or None, request.FILES or None)
	# Check for filled out form
	if form.is_valid():
		# save the form
		saver = form.save(commit=False)
		# Add user ID to the form
		saver.user = request.user
		# Save the form for realz
		saver.save()	

		messages.success(request, "A New Contact Has Been Added!")
		return redirect('home')
	else:
		return render(request, 'add_contact.html', {"form":form})


	return render(request, 'add_contact.html', {"form":form})


