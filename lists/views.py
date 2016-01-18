from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView
from django.views.generic.detail import SingleObjectMixin

from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List
import logging

User = get_user_model()


class HomePageView(FormView):
    template_name = "home.html"
    form_class = ItemForm


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, "list.html", {
        "list": list_,
        "form": form
    })


class NewListView(CreateView, HomePageView):

    def form_valid(self, form):
        list_ = List.objects.create()
        Item.objects.create(text=form.cleaned_data["text"], list=list_)
        return redirect(list_)


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})


class ViewAndAddToList(CreateView, SingleObjectMixin):
    model = List
    template_name = "list.html"
    form_class = ExistingListItemForm

    def get_form(self, form_class):
        self.object = self.get_object()
        return form_class(for_list=self.object, data=self.request.POST)


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {"owner": owner})


def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if "email" in request.POST:
        list_.shared_with.add(request.POST["email"])
    return redirect(list_)
