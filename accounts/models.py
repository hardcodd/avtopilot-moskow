from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser, Group)
from easy_thumbnails.fields import ThumbnailerImageField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    GENDERS = (('MALE', 'Мужской'), ('FEMALE', 'Женский'))
    # Account
    email = models.EmailField(max_length=255, unique=True)
    # Personal Info
    first_name = models.CharField(verbose_name='Имя', max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=True, null=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255, blank=True, null=True)
    born = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    gender = models.CharField(verbose_name='Пол', max_length=255, choices=GENDERS, blank=True, null=True)
    avatar = ThumbnailerImageField(verbose_name='Аватар', upload_to='avatars', blank=True, null=True)
    # Contacts
    phone = models.CharField(verbose_name='Телефон', max_length=255, blank=True, null=True)
    # Address
    country = models.CharField(verbose_name='Страна', max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name='Город', max_length=255, blank=True, null=True)
    street = models.CharField(verbose_name='Улица', max_length=255, blank=True, null=True)
    zip = models.PositiveIntegerField(verbose_name='Индекс', blank=True, null=True)
    house_num = models.PositiveIntegerField(verbose_name='Номер дома', blank=True, null=True)
    housing_num = models.PositiveIntegerField(verbose_name='Номер корпуса', blank=True, null=True)
    flat_num = models.PositiveIntegerField(verbose_name='Квартира', blank=True, null=True)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_full_name(self):
        if self.last_name and self.first_name:
            return '%s %s' % (self.last_name, self.first_name)
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email.split('@')[0]

    def get_polite_name(self):
        return '%s %s' % (self.first_name, self.middle_name)

    @property
    def get_complete_name(self):
        name = '%s %s %s' % (self.last_name or '', self.first_name or '', self.middle_name or '')
        return name.replace('  ', ' ')

    def get_short_name(self):
        return self.first_name

    @property
    def full_name(self):
        return self.get_full_name()


class UserGroup(Group):
    def __str__(self):
        return self.name
