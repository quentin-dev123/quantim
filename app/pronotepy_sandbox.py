import pronotepy, datetime, colorist

from colorist import hex
client = pronotepy.Client(
        'https://pronote.fis.edu.hk/eleve.html',
        username=input("Username:"),
        password=input("Password:"),
    )
homeworks = client.homework(date_from=datetime.date(2025, 3, 1))
for i in homeworks:
    hex(f"{i.subject.name} :", i.background_color)
    print(f"\x1b[4m	Pour: {i.date}\x1b[24m")
    print(f"{i.description}")
    print()

pdf_link = client.generate_timetable_pdf(datetime.date(2025, 3, 2))
print(pdf_link)