from django.db import models

# Course model
class Course(models.Model):
    id=models.IntegerField(primary_key=True)
    id_curso = models.CharField(max_length=255, unique=True)  # Use CharField for the text ID
    nombre = models.TextField()

    def __str__(self):
        return self.nombre


# Objective model
class Objective(models.Model):
    id=models.IntegerField(primary_key=True)
    id_objetivo = models.CharField(max_length=255)  # Use CharField for the text ID
    id_curso = models.TextField()  # Assuming this links to the Course model
    nombre = models.TextField()
    objetivo = models.TextField()

    def __str__(self):
        return self.nombre


# Requirement model
class Requirement(models.Model):
    id=models.IntegerField(primary_key=True)
    id_curso = models.CharField(max_length=255)  # Use CharField for the text ID
    id_requisito = models.TextField()  # Optional self-reference

    def __str__(self):
        return f"Requirement {self.id}"

# RA Link model
class RALink(models.Model):
    id = models.IntegerField(primary_key=True)
    
    # ForeignKey to Requirement (id_curso)
    id_curso = models.TextField()
    
    # ForeignKey to Objective
    id_objetivo = models.TextField()  # ForeignKey to Objective
    
    importancia = models.TextField()  # Use TextField for "importancia" if it's not a number
    
    # ForeignKey to Requirement (id_prerequisito)
    id_prerequisito = models.TextField()  # ForeignKey to Requirement
    
    # ForeignKey to Objective (id_objetivo_prerequisito)
    id_objetivo_prerequisito = models.TextField()  # ForeignKey to Objective

    def __str__(self):
        return f"Link {self.id}"

