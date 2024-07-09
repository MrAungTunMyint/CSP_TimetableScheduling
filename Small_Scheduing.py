from ortools.sat.python import cp_model
from prettytable import PrettyTable




# Create the model
model = cp_model.CpModel()

# Define the data
rooms = ['201', '202', '203', '204', '205']
courses = ['Physics', 'Math', 'Programming', 'Chemistry', 'Biology']
course_lecture_hours = {'Physics': 5, 'Math': 4, 'Programming': 3, 'Chemistry': 7, 'Biology': 2}
professors = ['John', 'Mike', 'Alice', 'Bob', 'Carol']
batches = ['2017', '2018', '2019']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
hours = {
    'Monday': list(range(10, 17)),  # 10 AM to 4 PM
    'Tuesday': list(range(9, 17)),  # 9 AM to 5 PM
    'Wednesday': list(range(9, 17)),
    'Thursday': list(range(9, 17)),
    'Friday': list(range(10, 17)),  # 10 AM to 4 PM
}

# Assign courses to static rooms
course_rooms = {
    'Physics': '201',
    'Math': '202',
    'Programming': '203',
    'Chemistry': '204',
    'Biology': '205'
}

num_courses = len(courses)
num_rooms = len(rooms)
num_days = len(days)
num_hours = 17 - 9  # 9 AM to 5 PM

# Map course names to indices
course_indices = {course: index for index, course in enumerate(courses)}

# Variables: course_assignment[course][day][hour] is True if course is assigned at the given day and hour
course_assignment = {}
for course in range(num_courses):
    for day in range(num_days):
        for hour in hours[days[day]]:
            course_assignment[(course, day, hour)] = model.NewBoolVar(
                f'course_assignment_{courses[course]}_{days[day]}_{hour}')

# Room constraints: No two courses can be in the same room at the same time
for room in range(num_rooms):
    for day in range(num_days):
        for hour in hours[days[day]]:
            room_courses = [course for course, room_num in course_rooms.items() if room_num == rooms[room]]
            model.Add(sum(course_assignment[(course_indices[course], day, hour)] for course in room_courses) <= 1)

# Professor constraints: A professor cannot teach more than one course at the same time
professor_courses = {
    'John': ['Physics'],
    'Mike': ['Math'],
    'Alice': ['Programming'],
    'Bob': ['Chemistry'],
    'Carol': ['Biology']
}

for professor, prof_courses in professor_courses.items():
    for day in range(num_days):
        for hour in hours[days[day]]:
            model.Add(sum(course_assignment[(course_indices[course], day, hour)] for course in prof_courses) <= 1)

# Time slot constraints: Courses cannot overlap in time for the same batch of students
batch_courses = {
    '2017': ['Physics', 'Math'],
    '2018': ['Programming', 'Chemistry'],
    '2019': ['Biology', 'Physics']
}

for batch, batch_courses_list in batch_courses.items():
    for day in range(num_days):
        for hour in hours[days[day]]:
            model.Add(sum(course_assignment[(course_indices[course], day, hour)] for course in batch_courses_list) <= 1)

# Lecture hour constraints
for course, lecture_hours in course_lecture_hours.items():
    course_idx = course_indices[course]
    if lecture_hours <= 5:
        for day in range(num_days):
            model.Add(sum(course_assignment[(course_idx, day, hour)] for hour in hours[days[day]]) <= 1)
        model.Add(sum(course_assignment[(course_idx, day, hour)] for day in range(num_days) for hour in
                      hours[days[day]]) == lecture_hours)
    else:
        two_timeslot_days = lecture_hours - 5
        single_timeslot_days = 5 - two_timeslot_days

        for day in range(two_timeslot_days):
            model.Add(sum(course_assignment[(course_idx, day, hour)] for hour in hours[days[day]]) == 2)

        for day in range(two_timeslot_days, 5):
            model.Add(sum(course_assignment[(course_idx, day, hour)] for hour in hours[days[day]]) == 1)

# Create the solver and solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Check the solution
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print('Feasible solution found')


    # Helper function to format hours in 12-hour AM/PM format
    def format_hour(hour):
        period = 'AM' if hour < 12 else 'PM'
        formatted_hour = hour if hour <= 12 else hour - 12
        return f'{formatted_hour} {period}'


    # Timetable for batches
    batch_timetable = {batch: {day: {hour: '' for hour in hours[day]} for day in days} for batch in batches}
    for course in range(num_courses):
        for day in range(num_days):
            for hour in hours[days[day]]:
                if solver.Value(course_assignment[(course, day, hour)]):
                    for batch, batch_courses_list in batch_courses.items():
                        if courses[course] in batch_courses_list:
                            batch_timetable[batch][days[day]][
                                hour] = f'{courses[course]} (Room {course_rooms[courses[course]]})'

    for batch, schedule in batch_timetable.items():
        print(f'Timetable for Batch {batch}:')
        table = PrettyTable()
        table.field_names = ["Hour"] + days
        for hour in range(9, 17):
            row = [format_hour(hour)]
            for day in days:
                if hour in hours[day]:
                    row.append(schedule[day][hour])
                else:
                    row.append("")
            table.add_row(row)
        print(table)

    # Timetable for professors
    professor_timetable = {prof: {day: {hour: '' for hour in hours[day]} for day in days} for prof in professors}
    for course in range(num_courses):
        for day in range(num_days):
            for hour in hours[days[day]]:
                if solver.Value(course_assignment[(course, day, hour)]):
                    for professor, prof_courses in professor_courses.items():
                        if courses[course] in prof_courses:
                            professor_timetable[professor][days[day]][
                                hour] = f'{courses[course]} (Room {course_rooms[courses[course]]})'

    for professor, schedule in professor_timetable.items():
        print(f'Timetable for Professor {professor}:')
        table = PrettyTable()
        table.field_names = ["Hour"] + days
        for hour in range(9, 17):
            row = [format_hour(hour)]
            for day in days:
                if hour in hours[day]:
                    row.append(schedule[day][hour])
                else:
                    row.append("")
            table.add_row(row)
        print(table)

    # Validation
    valid = True

    # Validate room constraints
    for room in range(num_rooms):
        for day in range(num_days):
            for hour in hours[days[day]]:
                room_courses = [course for course, room_num in course_rooms.items() if room_num == rooms[room]]
                if sum(solver.Value(course_assignment[(course_indices[course], day, hour)]) for course in room_courses) > 1:
                    print(f'Room conflict in Room {rooms[room]} on {days[day]} at {format_hour(hour)}')
                    valid = False

    # Validate professor constraints
    for professor, prof_courses in professor_courses.items():
        for day in range(num_days):
            for hour in hours[days[day]]:
                if sum(solver.Value(course_assignment[(course_indices[course], day, hour)]) for course in prof_courses) > 1:
                    print(f'Professor conflict for {professor} on {days[day]} at {format_hour(hour)}')
                    valid = False

    # Validate batch constraints
    for batch, batch_courses_list in batch_courses.items():
        for day in range(num_days):
            for hour in hours[days[day]]:
                if sum(solver.Value(course_assignment[(course_indices[course], day, hour)]) for course in batch_courses_list) > 1:
                    print(f'Batch conflict for Batch {batch} on {days[day]} at {format_hour(hour)}')
                    valid = False

    # Validate lecture hour constraints
    for course, lecture_hours in course_lecture_hours.items():
        course_idx = course_indices[course]
        assigned_hours = sum(
        solver.Value(course_assignment[(course_idx, day, hour)]) for day in range(num_days) for hour in
        hours[days[day]])
        if assigned_hours != lecture_hours:
            print(f'Lecture hours mismatch for {course}: expected {lecture_hours}, got {assigned_hours}')
            valid = False

    if valid:
        print("The solution is valid.")
    else:
        print("The solution has conflicts.")
else:
    print('No feasible solution found')
