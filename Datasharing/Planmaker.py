import json

Subjects = ["Englisch", "Mathe", "Geschichte", "Geographie", "Informatik", "Politik", "Kunst", "WAT", "Spanisch"]
Teachers = ["Berg", "Schiemenz", "Oertmann", "Muschert", "Wessner", "Schneider", "Berhorst", "Stoever", "Jacob"]
Rooms = ["B7", "B5", "C1", "C11", "A101", "A207", "A217", "A113", "C3"]
Classes = ["10A", "8L", "11", "9C", "10B", "12", "7C", "10B"]
Times = [('7:30-8:15', 'L'), ('8:30-9:15', 'L'), ('9:25-10:10', 'L'), ('10:10-10:30', 'R'), ('10:30-11:15', 'L'), ('11:25-12:10', 'L'), ('12:25-13:10', 'L'), ('13:10-13:40', 'R'), ('13:40-14:25', 'L')]
# Times = [('17:20-17:21', 'L'), ('17:21-17:22', 'L'), ('17:22-17:23', 'L'), ('17:23-17:24', 'R'),
# 		('17:24-17:25', 'L'), ('17:25-17:26', 'L'), ('17:26-17:27', 'L'), ('17:27-17:28', 'R'), ('17:28-17:29', 'L')]

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
		Roomgrid = Rooms
	Plan.update({f"Bloc{timebloc_iter}": {"TIME": Timebloc[0], "KIND": Timebloc[1], "ROOMGRID": Roomgrid}})
	timebloc_iter += 1

with open("../Helpfuls/ExamplePlan.json", "w") as f:
	json.dump(Plan, f)