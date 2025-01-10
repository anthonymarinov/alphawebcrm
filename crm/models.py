from django.db import models

# client record
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    # return string representation
    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
    
# client project
class Project(models.Model):
    client_record = models.ForeignKey(Record, related_name="projects", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    estimate_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # string representation
    def __str__(self):
        return(f"{self.address}, {self.city}")