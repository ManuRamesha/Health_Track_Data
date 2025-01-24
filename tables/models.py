from django.db import models

# Create your models here.

class Role(models.Model):
    role_id = models.CharField(max_length=3, primary_key=True,editable=False)
    name = models.CharField(max_length=50, unique=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.role_id:  # Only generate role_id for new objects
            last_role = Role.objects.order_by('-id').first()
            next_number = 1 if not last_role else int(last_role.role_id[1:]) + 1
            self.role_id = f"R{next_number:02}"  # Format as Rxx with zero-padding
        super().save(*args, **kwargs)
        


    def __str__(self):
        return self.name
    

class Gender(models.Model):
    gender_id = models.CharField(max_length=3, primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.gender_id:  # Only generate gender_id for new objects
            last_gender = Gender.objects.order_by('-id').first()
            next_number = 1 if not last_gender else int(last_gender.gender_id[1:]) + 1
            self.gender_id = f"G{next_number:02}"  # Format as Gxx with zero-padding
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name