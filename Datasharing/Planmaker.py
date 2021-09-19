import json

Subjects = ["Englisch", "Mathe", "Geschichte", "Geographie", "Informatik", "Politik", "Kunst", "WAT"]
Teachers = ["Berg", "Schiemenz", "Oertmann", "Muschert", "Wessner", "Schneider", "Berhorst", "Stoever"]
Rooms = ["B7", "B5", "C1", "C11", "A101", "A207", "A217", "A113"]
Classes = ["10A", "8L", "11", "9C", "10B", "12", "7C", "10B"]
Times = [('7:30-8:15', 'L'), ('8:15-8:30', 'R'), ('8:30-9:15', 'L'), ('9:15-9:25', 'R'), ('9:25-10:10', 'L'), ('10:10-10:30', 'R'),
		('10:30-11:15', 'L'), ('11:15-11:25', 'R'), ('11:25-12:10', 'L'), ('12:10-12:25', 'R'), ('12:25-13:10', 'L'), ('13:10-13:40', 'R')]

lesson_iter = 0
timebloc_iter = 0

Plan = {}
for Timebloc in Times:
	if Timebloc[1] == "L":
		Roomgrid = {}
		for i in range(len(Classes)):
			Roomgrid.update({f"{Rooms[i - lesson_iter]}": {"TEACHER": Teachers[i - lesson_iter], "SUBJECT": Subjects[i - lesson_iter], "CLASS": Classes[i]}})
			print({f"{Rooms[i - lesson_iter]}": {"Teacher": Teachers[i - lesson_iter], "Subject": Subjects[i - lesson_iter], "Class": Classes[i]}})
		lesson_iter += 1
	else:
		Roomgrid = None
	Plan.update({f"Bloc{timebloc_iter}": {"TIME": Timebloc[0], "TYPE": Timebloc[1], "ROOMGRID": Roomgrid}})
	timebloc_iter += 1

with open("../Helpfuls/ExamplePlan.json", "w") as f:
	json.dump(Plan, f)