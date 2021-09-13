from django import forms
from django.contrib import admin

from .models import Registration, CourseRegistration


class RegistrationStudentForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('status', 'user')


class RegistrationSubjectInLine(admin.TabularInline):
    model = CourseRegistration
    extra = 1 #количество форм при добавлении нового заказа (по умолчанию было 3)


class TotalSumFilter(admin.SimpleListFilter):
    subject_name = 'Фильтрация по количеству кредитов'
    parameter_name = 'total_sum'

    def lookups(self, request, model_admin): #как в choices
        return (
            ('0to3', 'от 0 до 3'),
            ('4to7', 'от 4 до 7'),
            ('8to10', 'от 8 до 10'),
            ('from10', 'от 10 и выше'),
        )

    def queryset(self, request, queryset): #список в листинге
        if self.value() == '0to3':
            return queryset.filter(total_sum__lte=4)
        elif self.value() == '4to7':
            return queryset.filter(total_sum__range=[4, 8])
        elif self.value() == '8to10':
            return queryset.filter(total_sum__range=[8, 10])
        elif self.value() == 'from10':
            return queryset.filter(total_sum__gte=10)
        else:
            return queryset


class RegisterStudent(admin.ModelAdmin):
    inlines = [
        RegistrationSubjectInLine
    ]
    exclude = ('course', )
    form = RegistrationStudentForm
    readonly_fields = ['user', 'total', 'created_at']
    list_display = ['id', 'status', 'total', 'created_at']
    list_filter = ['status', TotalSumFilter]
    search_fields = ['course']
    list_display_links = ['id', 'status']

    def save_model(self, request, obj, form, change): #change - change - true, create - false
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        total = 0
        for inline_form in formset:
            if inline_form.cleaned_data:
                subject = inline_form.cleaned_data['subject'].price
                quantity = inline_form.cleaned_data['quantity']
                total += subject * quantity
        form.instance.total_sum = total
        form.instance.save()
        formset.save()


admin.site.register(Registration, RegisterStudent)
admin.site.register(CourseRegistration)

