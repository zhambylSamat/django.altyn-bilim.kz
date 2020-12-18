
DEVELOPER_ROLE = "D"
SYSTEM_ROLE = 'SY'
STUDENT_ROLE = 'S'
ADMIN_ROLE = 'A'
SUPER_MODERATOR_ROLE = 'SM'
MODERATOR_ROLE = 'M'
TEACHER_ROLE = 'T'
PARENT_ROLE = 'P'
ROLE_CHOICES = (
    (ADMIN_ROLE, 'Admin'),
    (SUPER_MODERATOR_ROLE, 'Super Moderator'),
    (MODERATOR_ROLE, 'Moderator'),
    (STUDENT_ROLE, 'Student'),
    (TEACHER_ROLE, 'Teacher'),
    (SYSTEM_ROLE, 'System'),
    (DEVELOPER_ROLE, 'Developer'),
    (PARENT_ROLE, 'Parent')
)

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7
WEEK_DAY_CHOICES = (
    (MONDAY, "Понедельник"),
    (TUESDAY, "Вторник"),
    (WEDNESDAY, "Среда"),
    (THURSDAY, "Четверг"),
    (FRIDAY, "Пятница"),
    (SATURDAY, "Суббота"),
    (SUNDAY, "Воскресенье"),
)

WEEK_DAY_SHORT_NAME = (
    (1, 'ПН'),
    (2, 'ВТ'),
    (3, 'СР'),
    (4, 'ЧТ'),
    (5, 'ПТ'),
    (6, 'СБ'),
    (7, 'ВС'),
)

MON_TUE = 1
WED_THU = 2
FRI_SAT = 3

WEEK_DAY_SHORT_CHOICES = (
    (MON_TUE, "mon/tue"),
    (WED_THU, "wed/thu"),
    (FRI_SAT, "fri/sat")
)

WEEK_DAY_SHORT_CHOICES_LIST = (MON_TUE, WED_THU, FRI_SAT)

STAFF_POSITION = "staff"
GPH_POSITION = "gph"
CLIENT_POSITION = "client"

ROLES_INFO = (
    ("prefix", "level", "description", "position"),
    (DEVELOPER_ROLE, 10, "Разработчик", STAFF_POSITION),
    (ADMIN_ROLE, 20, "Руководитель", STAFF_POSITION),
    (SUPER_MODERATOR_ROLE, 30, "Администратор", STAFF_POSITION),
    (MODERATOR_ROLE, 40, "Менеджер", STAFF_POSITION),
    (TEACHER_ROLE, 50, "Мұғалім", GPH_POSITION),
    (STUDENT_ROLE, 0, "Оқушы", CLIENT_POSITION),
    (PARENT_ROLE, 0, "Ата-ана", CLIENT_POSITION)
)

FULL_STAFF_ROLES = (DEVELOPER_ROLE, ADMIN_ROLE, SUPER_MODERATOR_ROLE, MODERATOR_ROLE)


MALE = 'M'
FEMALE = 'F'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female')
)

FIELDS_FILLED_WRONG = "Username немесе құпия сөз қате енгізілген"

STUDENT_DEFAULT_PASSWORD = '1234567'
TEACHER_DEFAULT_PASSWORD = '12345678'
STAFF_DEFAULT_PASSWORD = '123456789'

NO_PAYMENT_STATUS_PK = 4

YOU_DON_NOT_HAVE_PERMISSION = "You do not have permission"