from django.utils import timezone
import calendar


class Day:
    def __init__(self, number, past):
        self.number = number
        self.past = past


    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("일", "월", "화", "수", "목", "금", "토")
        self.months = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",)

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                now = timezone.now()
                today = now.day    # 11일
                month = now.month  # 8월
                past = False
                if month == self.month:
                    # 오늘은 예약못하게 오늘도 막음
                    if day <= today:
                        past = True
                new_day = Day(day, past)
                # print(new_day)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]
