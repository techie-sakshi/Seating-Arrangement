import pandas as pd
import streamlit as st
from io import BytesIO

# Streamlit app
st.title("Exam Seating Plan Generator")

# Input file upload
st.header("Upload Input Files")
input1_file = st.file_uploader("Upload inp1.csv (Student and Course Details)", type="csv")
input2_file = st.file_uploader("Upload inp2.csv (Exam Timetable)", type="csv")
input3_file = st.file_uploader("Upload inp3.csv (Room Data)", type="csv")

# Configuration parameters
st.header("Configuration")
buffer_per_room = st.number_input("Buffer per Room (0 for no buffer)", min_value=0, value=0)
allocation_mode = st.selectbox("Allocation Mode", ["Dense", "Sparse"])
optimize_locality = st.checkbox("Optimize Locality", value=True)

# Generate outputs if files are uploaded
if input1_file and input2_file and input3_file:
    st.write("Processing...")

    # Read input files
    inp1 = pd.read_csv(input1_file)
    inp2 = pd.read_csv(input2_file)
    inp3 = pd.read_csv(input3_file)

    # Validate inp2
    required_columns_inp2 = {"Date", "Day", "Morning", "Evening"}
    if not required_columns_inp2.issubset(inp2.columns):
        st.error(f"Input file inp2.csv is missing one or more required columns: {required_columns_inp2}")
        st.stop()

    # Validate inp1
    required_columns_inp1 = {"rollno", "course_code"}
    if not required_columns_inp1.issubset(inp1.columns):
        st.error(f"Input file inp1.csv is missing one or more required columns: {required_columns_inp1}")
        st.stop()

    # Validate inp3
    required_columns_inp3 = {"Room No.", "Exam Capacity", "Block"}
    if not required_columns_inp3.issubset(inp3.columns):
        st.error(f"Input file inp3.csv is missing one or more required columns: {required_columns_inp3}")
        st.stop()

    # Prepare room data
    room_df = inp3.copy()
    room_df["Vacant"] = room_df["Exam Capacity"].copy()
    room_df = room_df.sort_values(by=["Block", "Room No."], ascending=[True, True])

    # Initialize outputs
    seating_plan = []
    vacancy_per_day = []

    # Process each exam session
    for _, exam in inp2.iterrows():
        date, day = exam["Date"], exam["Day"]
        daily_vacancy = room_df.copy()
        daily_vacancy["Date"] = date

        for session in ["Morning", "Evening"]:
            if exam[session] != "NO EXAM":
                courses = [course.strip() for course in exam[session].split(";")]
                courses.sort(key=lambda x: len(inp1[inp1["course_code"] == x]), reverse=True)
                for course in courses:
                    student_rolls = inp1[inp1["course_code"] == course]["rollno"].tolist()
                    room_index = 0
                    while student_rolls:
                        room = room_df.iloc[room_index]
                        room_capacity = room["Exam Capacity"]
                        capacity_with_buffer = room_capacity - buffer_per_room if buffer_per_room > 0 else room_capacity

                        if allocation_mode == "Sparse":
                            half_capacity = room_capacity // 2
                            allocated_students = student_rolls[:half_capacity]
                            remaining_vacant = room_capacity - len(allocated_students)
                            room_df.at[room_index, "Vacant"] = remaining_vacant
                        else:
                            allocated_students = student_rolls[:capacity_with_buffer]
                            remaining_vacant = room_capacity - len(allocated_students)
                            room_df.at[room_index, "Vacant"] = remaining_vacant

                        seating_plan.append({
                            "Date": date,
                            "Day": day,
                            "course_code": course,
                            "Room": room["Room No."],
                            "Allocated_students_count": len(allocated_students),
                            "Roll_list (semicolon separated_)": ";".join(allocated_students),
                        })

                        student_rolls = student_rolls[len(allocated_students):]
                        room_index += 1
                        if room_index >= len(room_df):
                            break

        daily_vacancy["Vacant"] = daily_vacancy["Exam Capacity"] - room_df["Vacant"]
        daily_vacancy["Capacity"] = daily_vacancy["Exam Capacity"]
        daily_vacancy["Block"] = daily_vacancy["Block"]
        vacancy_per_day.append(daily_vacancy[["Date", "Room No.", "Capacity", "Vacant", "Block"]])

    vacancy_df = pd.concat(vacancy_per_day, ignore_index=True)
    seating_df = pd.DataFrame(seating_plan)

    # Allow downloading of output files
    st.header("Download Output Files")
    seating_csv = seating_df.to_csv(index=False).encode('utf-8')
    vacancy_csv = vacancy_df.to_csv(index=False).encode('utf-8')

    seating_excel_buffer = BytesIO()
    seating_df.to_excel(seating_excel_buffer, index=False, engine='openpyxl')
    seating_excel_buffer.seek(0)

    vacancy_excel_buffer = BytesIO()
    vacancy_df.to_excel(vacancy_excel_buffer, index=False, engine='openpyxl')
    vacancy_excel_buffer.seek(0)

    st.download_button("Download Seating Plan (output1.csv)", seating_csv, "output1.csv", "text/csv")
    st.download_button("Download Room Capacity and Vacancy (output2.csv)", vacancy_csv, "output2.csv", "text/csv")
    st.download_button("Download Seating Plan (output1.xlsx)", seating_excel_buffer, "output1.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("Download Room Capacity and Vacancy (output2.xlsx)", vacancy_excel_buffer, "output2.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.warning("Please upload all input files to proceed.")
