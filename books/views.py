
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book,Cart
from .forms import BookForm
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import AddMoneyForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('book_list')  # Redirect to home page after signup
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('book_list')  # Redirect to the book list after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

#@login_required
# def buy_book(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     if book.stock > 0:
#         book.stock -= 1
#         book.save()
#         return redirect('book_list')
#     else:
#         return render(request, 'out_of_stock.html')
#from django.shortcuts import render, get_object_or_404, redirect
#from .models import Book, Cart

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.stock > 0:
        # Add the book to the user's cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
        if not created:
            cart_item.quantity += 1  # Increase quantity if the book is already in the cart
            cart_item.save()
        messages.success(request, f"'{book.title}' has been added to your cart.")
    else:
        messages.error(request, f"Sorry, '{book.title}' is out of stock.")
        return render(request, 'out_of_stock.html')
    return redirect('book_list')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)  # Get cart items for the logged-in user
    total_price = sum(item.book.price * item.quantity for item in cart_items)  # Calculate total price
    return render(request, 'books/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('view_cart')


# @login_required
# def checkout(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     for item in cart_items:
#         # Reduce the stock of each book in the cart
#         book = item.book
#         book.stock -= item.quantity
#         book.save()
#     # Clear the cart
#     cart_items.delete()
#     messages.success(request, "Thank you for your purchase!")
#     return redirect('book_list')
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.book.price * item.quantity for item in cart_items)  # Calculate total price

    # Get the user's profile
    profile = Profile.objects.get(user=request.user)

    # Check if the user has enough balance
    if profile.wallet_balance >= total_price:
        # Deduct the total price from the user's wallet
        profile.wallet_balance -= total_price
        profile.save()

        # Reduce the stock of each book in the cart
        for item in cart_items:
            book = item.book
            book.stock -= item.quantity
            book.save()

        # Clear the cart
        cart_items.delete()

        messages.success(request, "Thank you for your purchase!")
    else:
        messages.error(request, "Insufficient balance in your wallet.")

    return redirect('book_list')


@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'update_book.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    

#@login_required
# def add_money(request):
#     if request.method == 'POST':
#         form = AddMoneyForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             profile = Profile.objects.get(user=request.user)
#             profile.wallet_balance += amount
#             profile.save()
#             messages.success(request, f"${amount} added to your wallet.")
#             return redirect('book_list')
#     else:
#         form = AddMoneyForm()
#     return render(request, 'books/add_money.html', {'form': form})
@login_required
def add_money(request):
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            profile = request.user.profile
            profile.wallet_balance += amount
            profile.save()
            messages.success(request, f"${amount} added to your wallet.")
            return redirect('book_list')
    else:
        form = AddMoneyForm()
    return render(request, 'books/add_money.html', {'form': form})