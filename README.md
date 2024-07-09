# CSP_TimetableScheduling


Step 1: Understanding the Problem 

Before defining the variables, domains, and constraints, it's essential to understand the requirements and constraints of the university scheduling problem. Typically, this involves: 

Courses: Different subjects or classes. 

Professors: Who will be teaching these courses. 

Rooms: Where the classes will be held. 

Time Slots: When the classes will occur. 

Students: Who will attend these courses. 

Step 2: Define Variables 

Variables represent the elements that need to be assigned values. In the context of university scheduling, variables could be defined as follows: 

Course Assignments: Each course needs to be assigned a time slot and a room. 

Professor Assignments: Each professor needs to be assigned to a course. 

Student Assignments: Each student needs to be assigned to a course. 

Step 3: Define Domains 

Domains represent the possible values that the variables can take. In our case, the domains are implicitly defined by the range of indices for rooms and time slots. 

Step 4: Define Constraints 

Constraints are the rules that the assignments must satisfy. Typical constraints for a university scheduling problem include: 

Room Constraints: No two courses can be scheduled in the same room at the same time. 

Professor Constraints: A professor cannot teach more than one course at the same time. 

Time Slot Constraints: Courses cannot overlap in time for the same set of students. 

Lecture Hour Constraints: Adjusted to ensure proper distribution of timeslots based on lecture hours. 

 And so on
 ==============
 
 For small_Scheduling.py
 
 Code Explanation
 

Define Variables and Data:

	rooms, courses, course_lecture_hours, professors, batches, days, and hours.
	course_rooms assigns static rooms to courses
	
Variables:
	course_assignment[(course, day, hour)]: Boolean variable indicating if a course is scheduled at a specific day and hour.


Constraints:

	Room Constraints: Ensures no two courses are scheduled in the same room at the same time.
	Professor Constraints: Ensures professors do not teach more than one course simultaneously.
	Time Slot Constraints: Ensures courses do not overlap for the same batch of students.
	Lecture Hour Constraints: Adjusted to ensure proper distribution of timeslots based on lecture hours.


Solver:

	Create the solver and solve the model.
	Print the solution in a readable table format using PrettyTable.


Validation:
	Check room, professor, batch, and lecture hour constraints to ensure the solution's validity.
 
