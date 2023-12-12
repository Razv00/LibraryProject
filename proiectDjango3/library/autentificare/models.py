from django.db import models
from django.contrib.auth.models import User


class Carte(models.Model):
    titlu = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    descriere = models.TextField()
    disponibil = models.BooleanField(default=True)
    utilizator_imprumutat = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()


    def imprumutaCarte(self, utilizator):
        if self.disponibil:
            self.disponibil = False
            self.utilizator_imprumutat = utilizator
            self.save()

    def returneazaCarte(self):
        if not self.disponibil:
            self.disponibil = True
            self.utilizator_imprumutat = None
            self.save()

    def __str__(self):
        return self.titlu

    @classmethod
    def createCarte(cls, titlu, autor, descriere, disponibil=True, utilizator_imprumutat=None):
        return cls.objects.bjects.create(
            titlu=titlu,
            autor=autor,
            descriere=descriere,
            disponibil=disponibil,
            utilizator_imprumutat=utilizator_imprumutat
        )

    @classmethod
    def getCarteById(cls, carte_id):
        return cls.objects.get(id=carte_id)

    @classmethod
    def getCarti(cls):
        return cls.objects.all()
        # Funcție pentru a actualiza informațiile unei cărți

    @classmethod
    def updateCarte(cls,carte_id, **kwargs):
        carte = cls.objects.get(id=carte_id)
        for key, value in kwargs.items():
            setattr(carte, key, value)
        carte.save()

    @classmethod
    def delete_carte(cls,carte_id):
        carte = cls.objects.get(id=carte_id)
        carte.delete()

