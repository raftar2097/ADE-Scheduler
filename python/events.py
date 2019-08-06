import re
from enum import Enum
from static_data import COURSE_REGEX
from datetime import datetime, timedelta
from ics import Event


class EventType(Enum):
    CM = 1
    TP = 2
    E = 3  # Exams
    Other = 4  # For other events


# Information extraction functions
def extractCode(course):
    s = re.search(COURSE_REGEX, course, re.IGNORECASE)
    if s:
        return s.group(1)
    else:
        return None


def extractType(course):
    if re.search(COURSE_REGEX + "_", course, re.IGNORECASE):
        return EventType.CM
    elif re.search(COURSE_REGEX + "-", course, re.IGNORECASE):
        return EventType.TP
    elif re.search(COURSE_REGEX + "=E", course, re.IGNORECASE):
        return EventType.E
    else:
        return EventType.Other


def extractDateTime(date, time, delta):
    t0 = datetime.strptime(date + '-' + time, '%d/%m/%Y-%Hh%M')
    h, m = [0 if x is '' else int(x) for x in delta.split('h')]
    dt = timedelta(hours=h, minutes=m)
    t1 = t0 + dt
    return t0, t1, dt


# EVENT CLASSES (FOR ICS FORMAT)
class EventCM(Event):
    def __init__(self, start, end, code, name, professor, loc):
        name = 'Cours Magistral\n' + code + ' : ' + name
        super().__init__(name=name, begin=start, end=end, description=str(professor), location=loc)


class EventTP(Event):
    def __init__(self, start, end, code, name, professor, loc):
        name = 'Séance de TP\n' + code + ' : ' + name
        super().__init__(name=name, begin=start, end=end, description=str(professor), location=loc)


class EventEXAMEN(Event):
    def __init__(self, start, end, code, name, professor, loc):
        name = 'EXAMEN\n' + code + ' : ' + name
        super().__init__(name=name, begin=start, end=end, description=str(professor), location=loc)


class EventOTHER(Event):
    def __init__(self, start, end, code, name, professor, loc):
        name = 'Other\n' + code + ' : ' + name
        super().__init__(name=name, begin=start, end=end, description=str(professor), location=loc)


# class Course:
#     def __init__(self, name, professor, CM=None, TP=None, E=None, Other=None):
#         self.name = name
#         self.professor = professor
#         self.CM = CM
#         self.TP = TP
#         self.E = E
#         self.Other = Other