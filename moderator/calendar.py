
class Calendar:

    @staticmethod
    def getCalendar(self):
        text = "<table>"
        for x in range(1, 31):
            if x % 7 == 0:
                text += "<tr>"
            text += f'<td><a href="/date/2026-01-{x}">{x}</a></td>'
            if x % 7 == 0:
                text += "</tr>"
        text += "</table>"
        return text
