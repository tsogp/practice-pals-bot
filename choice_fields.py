'''

Definition for multiple choice labels for several columns.

'''

import enum

class SpokenLanguages(enum.Enum):
    russian = 'Russian'
    english = 'English'

class ProgrammingLanguages(enum.Enum):
    cpp = 'C++'
    python = 'Python'
    javascript = 'JavaScript'

class PreferedAge(enum.Enum):
    sexteentoeighteen = (16, 18)
    nineteentotwentyone = (19, 22)
    twentythreetotwentyfive = (23, 25)