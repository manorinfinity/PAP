from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, first_name=None, last_name=None, links=None, bio=None, role=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError('Users must have an email address')
		if not password:
			raise ValueError('Users must have a password')

		user_obj = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
			links=links,
			bio=bio,
			role=role
		)
		user_obj.set_password(password)
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, first_name=None, last_name=None, links=None, bio=None, role=None, password=None):
		user = self.create_user(
			email,
			password=password,
			first_name=first_name,
			last_name=last_name,
			links=links,
			bio=bio,
			role=role
		)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password, first_name=None, last_name=None, links=None, bio=None, role=None):
		user = self.create_user(
			email,
			password=password,
			first_name=first_name,
			last_name=last_name,
			links=links,
			bio=bio,
			role=role
		)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email 	= models.EmailField(max_length=255, unique=True)
	#username = models.CharField(max_length=30, unique=True)
	active  = models.BooleanField(default=True)
	staff   = models.BooleanField(default=False)
	admin   = models.BooleanField(default=False)
	first_name = models.CharField(max_length=100,blank=True,null=True)
	last_name = models.CharField(max_length=100,blank=True,null=True)
	links   = models.URLField(blank=True,null=True)
	bio     = models.CharField(max_length=200,blank=True,null=True)
	role    = models.CharField(max_length=10,blank=True,null=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['role']

	objects=UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active
