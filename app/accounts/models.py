
from datetime import datetime

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)

from app.core.models import CreationModificationDateAbstractModel
# from app.core.models import *
from app.core.utils.utils import *

# from core.models import CreationModificationDateAbstractModel
# from core.utils.utils import convert_date_to_jalali_date


# Create your models here.


class Province(
    CreationModificationDateAbstractModel):
    # title = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(
        allow_unicode=True, blank=True, null=True, unique=True
    )
    code = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class City(CreationModificationDateAbstractModel):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    slug = models.SlugField(
        allow_unicode=True, blank=True, null=True, unique=True
    )
    code = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    is_village = models.BooleanField(
        verbose_name="آیا روستا است؟",
        default=False,
    )
    unique_together = ["province", "title"]

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)


class UserManager(BaseUserManager["User"]):
    def create_user(
            self,
            phone_number,
            email=None,
            password=None,
            is_staff=False,
            is_active=True,
            **extra_fields,
    ):
        """Create a user instance with the given email and password."""
        if email:
            email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        # if is_telephone_number_invalid(phone_number):
        #     raise ValidationError("Phone number is not ok format.")

        user = self.model(
            email=email,
            phone_number=phone_number,
            is_active=is_active,
            is_staff=is_staff,
            **extra_fields,
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            phone_number,
            email=None,
            username=None,
            password=None,
            **extra_fields,
    ):
        user = self.create_user(
            phone_number,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            username=username,
            **extra_fields,
        )
        return user


class User(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    national_id = models.CharField(
        max_length=10, unique=True, blank=True, null=True
    )
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    # user_type = models.CharField(max_length=16, choices=UserType)
    avatar = models.ForeignKey("core.UploadFile", blank=True, null=True, on_delete=models.SET_NULL)

    birth_date = models.CharField(
        verbose_name="تاریخ تولد", max_length=255, null=True, blank=True
    )

    jalali_birth_date = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(
        verbose_name="جنسیت", max_length=3, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        is_new = self._state
        print(is_new)
        if self.sex == "M":
            self.sex = "مرد"
        elif self.sex == "F":
            self.sex = "زن"
        if self.birth_date:
            formatted_date = datetime.strptime(
                self.birth_date, "%Y-%m-%d"
            ).date()
            self.jalali_birth_date = convert_date_to_jalali_date(formatted_date)

        #        formatted_date = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        #        self.jalali_birth_date = convert_date_to_jalali_date(formatted_date)
        # super().save(*args, **kwargs)
        # Then, if the user is new, create and associate OtherPhoneNumber.
        # if is_new:
        #     other_phone = OtherPhoneNumbers.objects.create(
        #         main_phone_number=self.phone_number
        #     )

        # Add it to the user's 'other_phone_number' set.
        # self.other_phone_number.add(other_phone)
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.address.postCode == self.propertyownership.propertyPostCode and \
    #             self.propertyownership.bill_identities == self.address.main_bill_identities and \
    #             self.address.main_bill_identities.billTypeId == self.propertyownership.bill_identities.billTypeId and \
    #             self.address.main_bill_identities.billIdentity == self.propertyownership.bill_identities.billIdentity:
    #         pass
    #         # Address.objects.update_or_create(self.propertyownership)
    #     return super().save(*args, **kwargs)
