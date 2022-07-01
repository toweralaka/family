from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from.models import ParentName, ChildName
from .forms import ParentForm, ChildForm
# Create your views here.


def index(request):
    # initialise empty form for parent model child model
    # parent form uses prefix to help identify which one belongs 
    # to parent since they have similar fields
    pform = ParentForm(prefix='parent')
    cform = ChildForm()
    # check if form has been submitted
    if request.method == "POST":
        # get forms with submitted data
        pform = ParentForm(request.POST, prefix='parent')
        cform = ChildForm(request.POST)
        # check if child form has data
        if cform.data.get('first_name', False):
            # check if appropriate data was submitted in forms
            if pform.is_valid() and cform.is_valid():
                # save parent to database
                new_parent = pform.save()
                # check if data was entered for child form
                if cform.data['first_name'] and cform.data['dob']:
                    # save child form that was created using django
                    # but dont store to database because a required 
                    # field(parent) has not been included
                    a_child = cform.save(commit=False)
                    # attach the parent to the saved child then commit to database
                    a_child.parent = new_parent
                    a_child.save()
                # filter through other subitted data to get the cloned forms 
                # and store in child list
                child_list = {}
                for key, value in request.POST.items():
                    try:
                        # since cloned forms were separated by appending 
                        # numbers ('-0', '-1') to them, each submitted item will be 
                        # checked for whichever has appended number
                        field_name_and_number_label = key.split('-')
                        field_name = field_name_and_number_label[0]
                        number_label = field_name_and_number_label[1]
                        try:
                            # try to check if number label is integer
                            int(number_label)
                            try:
                                # try to retrieve a child dictionary whose key is the above integer
                                child = child_list[number_label]
                                child[field_name] = value
                            except KeyError:
                                # create a child dictionary
                                child_list[number_label] = {field_name:value}
                        except Exception:
                            # ignore if there is no integer
                            pass
                    except Exception:
                        # ignore if any error exists
                        pass
                # from each child data stored in child_list, 
                # create a child model object and add the parent
                # then save to database
                for index, child in child_list.items():
                    new_child = ChildName(**child,
                                parent = new_parent
                                )
                    new_child.save()
                # redirect to same view
                return HttpResponseRedirect('/')
        elif pform.is_valid():
            pform.save()
            return HttpResponseRedirect('/')
    return render(request, 'parent/index.html', {'pform': pform, 'cform': cform})



# base View is used since there is more than one 
# form and submitted forms require custom actions
class HomePageView(View):

    template_name = "parent/home.html"

    def get(self, request, *args, **kwargs):
        # initialise empty form for parent model child model
        # parent form uses prefix to help identify which one belongs 
        # to parent since they have similar fields
        pform = ParentForm(prefix='parent')
        cform = ChildForm()
        return render(request, self.template_name, {'pform': pform, 'cform': cform})
    
    def post(self, request, *args, **kwargs):
        # get forms with submitted data
        pform = ParentForm(request.POST, prefix='parent')
        cform = ChildForm(request.POST)
        # check if child form has data
        if cform.data.get('first_name', False):
            # check if appropriate data was submitted in forms
            if pform.is_valid() and cform.is_valid():
                # save parent to database
                new_parent = pform.save()
                # check if data was entered for child form
                if cform.data['first_name'] and cform.data['dob']:
                    # save child form that was created using django
                    # but dont store to database because a required 
                    # field(parent) has not been included
                    a_child = cform.save(commit=False)
                    # attach the parent to the saved child then commit to database
                    a_child.parent = new_parent
                    a_child.save()
                # filter through other subitted data to get the cloned forms 
                # and store in child list
                child_list = {}
                for key, value in request.POST.items():
                    try:
                        # since cloned forms were separated by appending 
                        # numbers ('-0', '-1') to them, each submitted item will be 
                        # checked for whichever has appended number
                        field_name_and_number_label = key.split('-')
                        field_name = field_name_and_number_label[0]
                        number_label = field_name_and_number_label[1]
                        try:
                            # try to check if number label is integer
                            int(number_label)
                            try:
                                # try to retrieve a child dictionary whose key is the above integer
                                child = child_list[number_label]
                                child[field_name] = value
                            except KeyError:
                                # create a child dictionary
                                child_list[number_label] = {field_name:value}
                        except Exception:
                            # ignore if there is no integer
                            pass
                    except Exception:
                        # ignore if any error exists
                        pass
                # from each child data stored in child_list, 
                # create a child model object and add the parent
                # then save to database
                for index, child in child_list.items():
                    new_child = ChildName(**child,
                                parent = new_parent
                                )
                    new_child.save()
                # redirect to same view
                return HttpResponseRedirect('/home/')
        elif pform.is_valid():
            pform.save()
            return HttpResponseRedirect('/home/')
        return render(request, self.template_name, {'pform': pform, 'cform': cform})



            
def pdf_view(request):
    import weasyprint
    # the_url = request
    pdf = weasyprint.HTML('http://www.google.com').write_pdf()
    open('google.pdf', 'wb').write(pdf)
    return HttpResponse()
        
