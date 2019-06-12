from django.db import models

# Create your models here. 所有你需要的模块都放在这里
'''
主要就是一下几个模块:(models)
1. DroneCategory 
2.Drone 
3.Pilot 
4.Competition

- `Meta` 定义了ordering attribute
- `__str__`方法返回每个model返回的名字
- `ForeignKey`提供了many-to one relationship to `DroneCategory` model.
- 因为希望在一个数据删除之后,对应的内容都删除,所以声明`models.CASCADE`在`on_delete` 参数定义时
'''


class DroneCategory(models.Model):
    name = models.CharField(max_length=250, unique=True)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class Drone(models.Model):
    name = models.CharField(max_length=250, unique=True)
    drone_category = models.ForeignKey(
        DroneCategory,
        related_name='drones',
        on_delete=models.CASCADE)
    manufacturing_date = models.DateTimeField()
    has_it_competed = models.BooleanField(default=False)
    inserted_timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Pilot(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length=150, blank=False, unique=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    races_count = models.IntegerField()
    inserted_timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class Competition(models.Model):
    pilot = models.ForeignKey(
        Pilot,
        related_name='competitions',
        on_delete=models.CASCADE)
    drone = models.ForeignKey(
        Drone,
        on_delete=models.CASCADE)
    distance_in_feet = models.IntegerField()
    distance_achievement_date = models.DateTimeField()
    
    class Meta:
        # Order by distance in descending order
        ordering = ('-distance_in_feet',)