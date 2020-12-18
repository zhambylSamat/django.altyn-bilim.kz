TWO_DAY_ABS = "2DA"
RE_RETAKE_QUIZ = "RRQ"
THREE_TIMES_UP_TRIAL_TEST = "3UTT"
MAX_TRIAL_TEST = "MTT"
MAX_QUIZ = "MQ"
EXCELLENT_QUIZ = "EQ"
NO_HOME_WORK = "NHW"

NOTIFICATION_TYPE = (
    (TWO_DAY_ABS, '2 рет қатарынан сабаққа келмеді'),
    (RE_RETAKE_QUIZ, 'Пересдачадан құлады'),
    (NO_HOME_WORK, 'Үй жұмысы жоқ'),
    (THREE_TIMES_UP_TRIAL_TEST, '3 рет баллын көтерді'),
    (MAX_TRIAL_TEST, 'Пробный тесттен макс. жинады'),
    (MAX_QUIZ, 'Аралық бақылаудан макс. жинады'),
    (EXCELLENT_QUIZ, 'Аралық бақылауды жақсы жазды'),
)

NOTIFICATION_TYPE_COUNT = (
    (TWO_DAY_ABS, 2),
    (RE_RETAKE_QUIZ, 2),
    (NO_HOME_WORK, 1),
    (THREE_TIMES_UP_TRIAL_TEST, 3),
    (MAX_TRIAL_TEST, 1),
    (MAX_QUIZ, 1),
    (EXCELLENT_QUIZ, 1),
)


def notification_type_count(notification_type):
    return dict(NOTIFICATION_TYPE_COUNT)[notification_type]


SUCCESS_CLASS = "S"
WARNING_CLASS = "W"
DANGER_CLASS = "D"

NOTIFICATION_CLASS = (
    (SUCCESS_CLASS, 'success'),
    (WARNING_CLASS, 'warning'),
    (DANGER_CLASS, 'danger'),
)
