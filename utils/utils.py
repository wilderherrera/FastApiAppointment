from datetime import datetime


class Utils:
    def format_date(self, raw_date):
        return datetime.fromisoformat(str(raw_date)).strftime('%A, %d de %B de %Y a las %I:%M %p')
