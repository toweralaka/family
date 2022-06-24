from django.shortcuts import render
from.models import ParentName, ChildName
from .forms import ParentForm, ChildForm
# Create your views here.


def index(request):
    if request.method == "POST":
        child_list = {}
        pform = ParentForm(request.POST, prefix='parent')
        new_parent = pform.save()
        cform = ChildForm(request.POST)
        a_child = cform.save(commit=False)
        a_child.parent = new_parent
        a_child.save()
        for key, value in request.POST.items():
            try:
                info = key.split('-')
                info0 = info[0]
                info1 = info[1]
                try:
                    int(info1)
                    try:
                        child = child_list[info1]
                        child[info0] = value
                    except KeyError:
                        child_list[info1] = {info0:value}
                except Exception as e:
                    pass
            except Exception as e:
                pass
        for index, child in child_list.items():
            new_child = ChildName(**child,
                        parent = new_parent
                        )
            # new_child.save(commit=False)
            # new_child.parent = new_parent
            new_child.save()
            print(new_child.first_name)
    pform = ParentForm(prefix='parent')
    cform = ChildForm()
    return render(request, 'parent/index.html', {'pform': pform, 'cform': cform})