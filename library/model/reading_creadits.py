from collections import defaultdict
from library.model.genre import Genre


reading_credits = defaultdict(int)
reading_credits[Genre.HISTORY] = 1
reading_credits[Genre.MEDICINE] = 2
reading_credits[Genre.SOCIOLOGY] = 2
