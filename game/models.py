# Genshin Impact Game Database Model
from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=50)
    vision = models.CharField(max_length=50)
    weapon = models.CharField(max_length=50)
    nation = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100)
    rarity = models.IntegerField()
    constallation = models.CharField(max_length=100)
    birthday = models.DateField()
    description = models.TextField()
    vision_key = models.CharField(max_length=50)
    weapon_type = models.CharField(max_length=50)

    raw_data = models.JSONField()

    def __str__(self):
        return self.name

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
