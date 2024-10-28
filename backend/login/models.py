from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        if not id:
            raise ValueError("아이디를 입력해야 합니다.")
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=50, unique=True, primary_key=True)  # primary_key=True 설정
    blood_sugar_target = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'  # 'id'를 사용자명 필드로 사용
    REQUIRED_FIELDS = []  # 추가 필드가 필요 없다면 빈 리스트

    def __str__(self):
        return self.id