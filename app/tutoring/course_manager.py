# Course Manager for Digital Electronics which defines the course structure and tracks student progress
DIGITAL_ELECTRONICS_COURSE = [
    "Boolean Algebra",
    "Logic Gates",
    "Karnaugh Maps",
    "Combinational Circuits",
    "Sequential Logic",
    "Flip-Flops",
    "Registers",
    "Counters",
    "Finite State Machines",
    "Memory Systems"
]

# Each student will have a progress index that starts at 0 and increments as they complete topics. The course manager provides functions to get the current topic, advance to the next topic, and check if the course is completed.

def get_current_topic(progress_index):

    if progress_index < len(DIGITAL_ELECTRONICS_COURSE):
        return DIGITAL_ELECTRONICS_COURSE[
            progress_index
        ]
    return None

# Returns True if the student has completed all topics in the course, False otherwise

def advance_topic(progress_index):
    return progress_index + 1

# Returns the total number of topics in the course, which can be used to check for completion

def get_course_length():

    return len(DIGITAL_ELECTRONICS_COURSE)