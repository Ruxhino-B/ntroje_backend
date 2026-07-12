from django.db import models

from accounts.models import CustomUser
from agency.models import Agency
from properties.models import Property


# Create your models here.
class PropertyView(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    viewer_key = models.CharField(max_length=64, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property.title} - {self.viewer_key}"

    class Meta:
        indexes = [
            models.Index(fields=['property_id', 'viewer_key']),
            models.Index(fields=['viewed_at']),
        ]
        db_table = 'property_view'

class AgentView(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    viewer_key = models.CharField(max_length=64, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.agent.username} - {self.viewer_key}"
    class Meta:
        db_table = 'agent_view'

class AgencyView(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    viewer_key = models.CharField(max_length=64, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.agency.name} - {self.viewer_key}"

    class Meta:
        db_table = 'agency_view'

#Todo: make migrations and make view.py. Dont forget to add views_count +=1 for Agency, CustomUser, Property