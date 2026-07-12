from django.conf import settings
from django.db import models
from django.utils.text import slugify

AGENCY_MEMBER_ROLE_AGENT = 'agent'

AGENCY_MEMBER_ROLE = (
('admin', 'Admin'),
('manager', 'Manager'),
('agent', 'Agent'),
)

class Agency(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_agency'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='agencies/logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='agencies/covers/', blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='Albania')

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agencies'
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'
        ordering = ['-date_created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AgencyMember(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agency_memberships'
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agency_members'
        verbose_name = 'Agency Member'
        verbose_name_plural = 'Agency Members'
        unique_together = ('agency', 'user')
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.user.email} - {self.agency.name} ({self.user.role})'