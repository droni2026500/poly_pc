a=['9:00', '11:00','13:00','10:00','16:00']
print(a)

from datetime import datetime

sortedArray = sorted(
    a,
    key=lambda x: datetime.strptime(x, '%H:%M'), reverse=False
)
print(sortedArray)