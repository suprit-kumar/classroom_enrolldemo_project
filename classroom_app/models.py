from django.db import models


# Create your models here.

class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    class Meta:
        db_table = "transactions"

    def __unicode__(self):
        return u'%s' % [self.id]


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    usercode = models.CharField(max_length=50, null=True, default="")
    teacher_name = models.CharField(max_length=50, null=True, default="")
    teacher_email = models.CharField(max_length=100, null=True, default="")
    created_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "teacher"

    def __unicode__(self):
        return u'%s' % [self.teacher_id]


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    usercode = models.CharField(max_length=50, null=True, default="")
    student_name = models.CharField(max_length=50, null=True, default="")
    student_email = models.CharField(max_length=100, null=True, default="")
    created_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "student"

    def __unicode__(self):
        return u'%s' % [self.student_id]


class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50, null=True, default="")
    class_subject = models.CharField(max_length=50, null=True, default="")
    class_date = models.CharField(max_length=50, null=True, default="")
    class_time = models.CharField(max_length=50, null=True, default="")
    number_of_students = models.CharField(max_length=50, null=True, default=0)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        db_table = "classes"

    def __unicode__(self):
        return u'%s' % [self.class_id]


class ClassStudentMapping(models.Model):
    cls_student_map_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "classroom"

    def __unicode__(self):
        return u'%s' % [self.class_id]


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, null=True, default="")
    role_status = models.CharField(max_length=50, null=True, default="")
    created_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "role"

    def __unicode__(self):
        return u'%s' % [self.role_id]


class Users(models.Model):
    u_id = models.AutoField(primary_key=True)
    user_code = models.CharField(max_length=50, null=True, default="")
    name = models.CharField(max_length=100, null=True, default="")
    useremail = models.CharField(max_length=100, null=True, default="")
    password = models.CharField(max_length=100, null=True, default="")
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, default="active")
    user_created_time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "users"

    def __unicode__(self):
        return u'%s' % [self.u_id]
