from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import ApoliceLoja, Loja
from .forms import ApoliceLojaForm, LojaForm


class ApoliceListView(LoginRequiredMixin, ListView):
    model = ApoliceLoja
    template_name = "seguros/apolice_list.html"
    context_object_name = "apolices"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("loja", "loja__shopping")
        shopping_id = self.request.GET.get("shopping", "")
        tipo = self.request.GET.get("tipo", "")
        if shopping_id:
            try:
                qs = qs.filter(loja__shopping_id=int(shopping_id))
            except ValueError:
                pass
        if tipo:
            qs = qs.filter(tipo_seguro=tipo)
        return qs.order_by("-vigencia_fim")

    def get_context_data(self, **kwargs):
        from documentos.models import Shopping
        ctx = super().get_context_data(**kwargs)
        ctx["shopping_list"] = Shopping.objects.all().order_by("nome")
        ctx["tipo"] = self.request.GET.get("tipo", "")
        return ctx


class ApoliceCreateView(LoginRequiredMixin, CreateView):
    model = ApoliceLoja
    form_class = ApoliceLojaForm
    template_name = "seguros/apolice_form.html"
    success_url = reverse_lazy("seguros_apolice_list")


class LojaCreateView(LoginRequiredMixin, CreateView):
    model = Loja
    form_class = LojaForm
    template_name = "seguros/loja_form.html"
    success_url = reverse_lazy("seguros_apolice_list")
