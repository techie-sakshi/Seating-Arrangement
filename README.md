# Exam Seating Plan Generator  

A Streamlit-based web application to automate the creation of seating plans and room vacancy reports for exams. This tool is designed to optimize room utilization and simplify the seating arrangement process for educational institutions.  

## Features  
- **Seating Plan Generation**: Automatically allocates students to rooms based on configurable parameters like room capacity, buffer size, and allocation mode (Dense/Sparse).  
- **Room Vacancy Reports**: Tracks room capacity and vacancy for each exam session.  
- **Configurable Options**:  
  - Buffer size per room.  
  - Dense or Sparse allocation modes.  
  - Optimized room locality allocation.  
- **User-Friendly Interface**: Upload files directly in the app and download the outputs in CSV and Excel formats.  

## How It Works  
1. **Upload Input Files**:  
   - `inp1.csv`: Student and course details.  
   - `inp2.csv`: Exam timetable.  
   - `inp3.csv`: Room data (capacity, block, etc.).  

2. **Configure Parameters**:  
   - Set buffer size, allocation mode, and locality optimization preferences.  

3. **Download Outputs**:  
   - `output1.csv` / `output1.xlsx`: Seating plan.  
   - `output2.csv` / `output2.xlsx`: Room capacity and vacancy report.  

## Installation  
1. Clone the repository:  
   ``git clone https://github.com/techie-sakshi/Seating-Arrangement.git`` 

2. Install dependencies:  
   ``pip install -r requirements.txt`` 

## Run the Application  
Run the Streamlit app with:  
```bash
streamlit run exam_seating_plan.py
```  
Access the app at `http://localhost:8501` in your browser.  

## File Format Details  
- **inp1.csv**:  
  | rollno | course_code |  
  |--------|-------------|  
  | R001   | CS101       |  

- **inp2.csv**:  
  | Date       | Day  | Morning       | Evening       |  
  |------------|------|---------------|---------------|  
  | 2024-12-20 | Fri  | CS101;PH102   | NO EXAM       |  

- **inp3.csv**:  
  | Room No. | Exam Capacity | Block |  
  |----------|---------------|-------|  
  | R101     | 30            | Block A |  

## Technologies Used  
- **Python**: Backend logic using Pandas for data processing.  
- **Streamlit**: Interactive front-end for user uploads and downloads.  
- **Excel/CSV Handling**: Managed with Pandas and `openpyxl`.  
