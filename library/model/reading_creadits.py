from collections import defaultdict
from library.model.genre import Genre


ReadingCreditsPerGenre = defaultdict(int)
ReadingCreditsPerGenre[Genre.HISTORY] = 1
ReadingCreditsPerGenre[Genre.MEDICINE] = 2
ReadingCreditsPerGenre[Genre.SOCIOLOGY] = 2
