from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json

from documentos.models import RegistroDocumento, Shopping


class DashboardContratosView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard_contratos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtro_status = self.request.GET.get("status", "")
        filtro_shopping = self.request.GET.get("shopping", "")
        tipo = self.request.GET.get("tipo", "documento").lower()
        modo = self.request.GET.get("modo", "cards").lower()
        # Robustez: garantir valores válidos para tipo e janela
        if tipo not in ("documento", "contrato"):
            tipo = "documento"
        if modo not in ("cards", "lista"):
            modo = "cards"
        try:
            janela = int(self.request.GET.get("janela", "60"))
            if janela not in (30, 60, 90):
                janela = 60
        except (ValueError, TypeError):
            janela = 60
        hoje = date.today()
        limite_avencer = hoje + timedelta(days=janela)

        qs = RegistroDocumento.objects.all()
        qs = qs.filter(tipo__iexact=tipo)

        user = self.request.user
        shopping_list = []
        if user.groups.filter(name="Corporativo").exists() or user.is_superuser:
            shopping_list = list(Shopping.objects.all().order_by("nome"))
            if filtro_shopping:
                try:
                    qs = qs.filter(shopping_id=int(filtro_shopping))
                except ValueError:
                    pass
        else:
            shopping = getattr(getattr(user, "perfil", None), "shopping", None) or getattr(user, "shopping", None)
            if shopping:
                qs = qs.filter(shopping=shopping)
                shopping_list = [shopping]
            else:
                shopping_list = []

        if filtro_status in ["pendente", "aprovado"]:
            qs = qs.filter(status_aprovacao=filtro_status)

        total = qs.count()
        vencidos = qs.filter(data_vencimento__lt=hoje).count()
        a_vencer_qs = qs.filter(data_vencimento__gte=hoje, data_vencimento__lte=limite_avencer)
        a_vencer = a_vencer_qs.count()
        no_prazo = total - (vencidos + a_vencer)
        pendentes_aprovacao = qs.filter(status_aprovacao="pendente").count()
        aprovados = qs.filter(status_aprovacao="aprovado").count()

        status_counts = list(
            qs.values("status_aprovacao").annotate(total=Count("id")).order_by("status_aprovacao")
        )

        por_shopping_base = list(
            qs.values("shopping__nome").annotate(total=Count("id")).order_by("shopping__nome")
        )
        av_por_shopping = qs.filter(
            data_vencimento__gte=hoje, data_vencimento__lte=limite_avencer
        ).values("shopping__nome").annotate(a_vencer=Count("id"))
        vc_por_shopping = qs.filter(data_vencimento__lt=hoje).values("shopping__nome").annotate(vencidos=Count("id"))
        av_map = {r["shopping__nome"]: r["a_vencer"] for r in av_por_shopping}
        vc_map = {r["shopping__nome"]: r["vencidos"] for r in vc_por_shopping}
        por_shopping = []
        for r in por_shopping_base:
            nome = r["shopping__nome"]
            a_v = av_map.get(nome, 0)
            v = vc_map.get(nome, 0)
            por_shopping.append({
                "shopping__nome": nome,
                "total": r["total"],
                "a_vencer": a_v,
                "vencidos": v,
                "no_prazo": r["total"] - (a_v + v),
            })

        # Top 5 por vencidos e por a vencer
        top5_vencidos = sorted(por_shopping, key=lambda x: x["vencidos"], reverse=True)[:5]
        top5_avencer = sorted(por_shopping, key=lambda x: x["a_vencer"], reverse=True)[:5]

        # SLA de aprovação: tempo médio entre envio e aprovação (em dias)
        aprovados_qs = qs.filter(status_aprovacao="aprovado", data_aprovacao__isnull=False)
        durations_sec = []
        for d in aprovados_qs.only("data_envio", "data_aprovacao"):
            try:
                delta = d.data_aprovacao - d.data_envio
                durations_sec.append(delta.total_seconds())
            except Exception:
                continue
        sla_aprovacao_dias = round((sum(durations_sec) / len(durations_sec)) / 86400, 1) if durations_sec else None

        a_vencer_list = a_vencer_qs.select_related("shopping").order_by("data_vencimento")[:100]

        context.update({
            "title": "Dashboard",
            "hoje": hoje,
            "janela": janela,
            "tipo": tipo,
            "modo": modo,
            "filtro_status": filtro_status,
            "filtro_shopping": filtro_shopping,
            "shopping_list": shopping_list,
            "indicadores": {
                "total": total,
                "no_prazo": no_prazo,
                "a_vencer": a_vencer,
                "vencidos": vencidos,
                "pendentes_aprovacao": pendentes_aprovacao,
                "aprovados": aprovados,
                "sla_aprovacao_dias": sla_aprovacao_dias,
            },
            "status_counts": json.dumps(status_counts, cls=DjangoJSONEncoder),
            "por_shopping_list": por_shopping,
            "por_shopping_json": json.dumps(por_shopping, cls=DjangoJSONEncoder),
            "top5_vencidos_json": json.dumps(top5_vencidos, cls=DjangoJSONEncoder),
            "top5_avencer_json": json.dumps(top5_avencer, cls=DjangoJSONEncoder),
            "a_vencer_list": a_vencer_list,
        })
        return context