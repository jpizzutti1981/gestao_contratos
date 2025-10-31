from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Perfil  # ✅ Importa Perfil certo

@receiver(post_save, sender=Usuario)
def criar_perfil_automaticamente(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name='Gestor').exists():
            Perfil.objects.get_or_create(  # ✅ Usa get_or_create para evitar duplicidade
                usuario=instance,
                defaults={'shopping': instance.shopping}
            )
