from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = ((1, "Начальник"), (2, "Персонал"), (3, "Студент"))
    user_type = models.CharField(
        "тип пользователя", default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    """Модель Начальник"""

    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name="пользователь")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    """Модель Персонал"""

    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    address = models.TextField("адрес")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class Courses(models.Model):
    """Модель Курс"""

    course_name = models.CharField("название курса", max_length=255)
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class Subjects(models.Model):
    """Модель Урок"""

    subject_name = models.CharField("имя урока", max_length=255)
    course_id = models.ForeignKey(
        Courses, on_delete=models.CASCADE, default=1, verbose_name='название курса')
    staff_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class Students(models.Model):
    """Модель Студенты"""

    admin = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name="пользователь")
    gender = models.CharField(max_length=255, verbose_name="пол")
    profile_pic = models.FileField()
    address = models.TextField("адрес")
    course_id = models.ForeignKey(
        Courses, on_delete=models.DO_NOTHING, verbose_name='название курса')
    session_start_year = models.DateField("начало учебного года")
    session_end_year = models.DateField("конец учебного года")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    """Модель Посещаемость"""

    subject_id = models.ForeignKey(
        Subjects, on_delete=models.DO_NOTHING, verbose_name="урок")
    attendance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    """Модель Отчет о посещении"""

    student_id = models.ForeignKey(
        Students, on_delete=models.DO_NOTHING, verbose_name="студент")
    attendance_id = models.ForeignKey(
        Attendance, on_delete=models.CASCADE, verbose_name="посещаемость")
    status = models.BooleanField("присутствие", default=False)
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    """Модель Отчисленный Студент"""

    student_id = models.ForeignKey(
        Students, on_delete=models.CASCADE, verbose_name="студент")
    leave_date = models.CharField("дата отчисления", max_length=255)
    leave_message = models.TextField("сообщение")
    leave_status = models.BooleanField("статус", default=False)
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    """Модель Уволенный Персонал"""

    staff_id = models.ForeignKey(
        Staffs, on_delete=models.CASCADE, verbose_name="персонал")
    leave_date = models.CharField("дата увольнения", max_length=255)
    leave_message = models.TextField("сообщение")
    leave_status = models.BooleanField("статус", default=False)
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    """Обратная Связь Студента"""

    student_id = models.ForeignKey(
        Students, on_delete=models.CASCADE, verbose_name='студент')
    feedback = models.TextField("текст уведомления")
    feedback_reply = models.TextField("ответ на обратную связь")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    """Обратная Связь Персонала"""

    staff_id = models.ForeignKey(
        Staffs, on_delete=models.CASCADE, verbose_name="персонал")
    feedback = models.TextField("текст уведомления")
    feedback_reply = models.TextField("ответ на обратную связь")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    """Модель Уведомления Студента"""

    student_id = models.ForeignKey(
        Students, on_delete=models.CASCADE, verbose_name="студент")
    message = models.TextField("текст уведомления")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    """Модель Уведомления Персонала"""

    staff_id = models.ForeignKey(
        Staffs, on_delete=models.CASCADE, verbose_name="персонал")
    message = models.TextField("текст уведомления")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)
    objects = models.Manager()
