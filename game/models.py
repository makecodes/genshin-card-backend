# Genshin Impact Game Database Model
from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    vision = models.CharField(max_length=50, null=True, blank=True)
    weapon = models.CharField(max_length=50, null=True, blank=True)
    nation = models.CharField(max_length=100, null=True, blank=True)
    affiliation = models.CharField(max_length=100, null=True, blank=True)
    rarity = models.IntegerField(null=True, blank=True)
    constallation = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    vision_key = models.CharField(max_length=50, null=True, blank=True)
    weapon_type = models.CharField(max_length=50, null=True, blank=True)

    raw_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name or self.slug

    class Meta:
        db_table = "character"
        verbose_name = "Character"
        verbose_name_plural = "Characters"
        ordering = ["name"]


class Weapon(models.Model):
    name = models.CharField(max_length=50)
    weapon_type = models.CharField(max_length=50)
    rarity = models.IntegerField()
    base_attack = models.IntegerField()
    sub_stat = models.CharField(max_length=50)
    passive_name = models.CharField(max_length=100)
    passive_description = models.TextField()
    location = models.CharField(max_length=100)

    raw_data = models.JSONField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "weapon"
        verbose_name = "Weapon"
        verbose_name_plural = "Weapons"
        ordering = ["name"]
