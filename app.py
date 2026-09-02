from flask import Flask, render_template, request, session
from pypdf import PdfReader
import json
import os

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

app.secret_key = "placement-navigator-secret-key"
PROGRESS_FILE = "progress.json"


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as file:
                return json.load(file)
        except:
            return []

    return []


def save_progress(completed):
    with open(PROGRESS_FILE, "w") as file:
        json.dump(completed, file)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# PREPARATION SETUP PAGE
# ==========================================

@app.route("/prepare")
def prepare():

    completed = load_progress()

    total_modules = 10

    readiness_score = int(
        (len(completed) / total_modules) * 100
    )

    return render_template(
        "prepare.html",
        readiness_score=readiness_score
    )

# ==========================================
# CREATE PERSONALIZED ROADMAP
# ==========================================

@app.route("/create-roadmap", methods=["POST"])
def create_roadmap():

    company = request.form.get("company")
    role = request.form.get("role")
    interview_date = request.form.get("interview_date")
    level = request.form.get("level")

    completed = session.get("completed_modules", [])

    total_modules = 10

    readiness_score = int(
        (len(completed) / total_modules) * 100
    )

    return render_template(
        "roadmap.html",
        company=company,
        role=role,
        interview_date=interview_date,
        level=level,
        readiness_score=readiness_score
    )

# ==========================================
# APTITUDE DASHBOARD
# ==========================================

@app.route("/aptitude")
def aptitude():
    return render_template("aptitude.html")

@app.route("/technical")
def technical():
    return render_template("technical.html") 

@app.route("/python")
def python():
    return render_template("python.html")


@app.route("/python-foundation")
def python_foundation():
    return render_template("python_foundation.html")


@app.route("/python-data-structures")
def python_data_structures():
    return render_template("python_data_structures.html")


@app.route("/python-functions")
def python_functions():
    return render_template("python_functions.html")


@app.route("/python-oop")
def python_oop():
    return render_template("python_oop.html")


@app.route("/python-control-flow")
def python_control_flow():
    return render_template("python_control_flow.html")


@app.route("/python-interview")
def python_interview():
    return render_template("python_interview.html")


@app.route("/sql")
def sql():
    return render_template("sql.html")

    
@app.route("/excel")
def excel():
    return render_template("excel.html")


@app.route("/excel-interview")
def excel_interview():
    return render_template("excel_interview.html")  

@app.route("/excel-topic")
def excel_topic():
    return render_template("excel_topic.html")

@app.route("/data-analysis")
def data_analysis():
    return render_template("data_analysis.html")

@app.route("/data-analysis-topic")
def data_analysis_topic():
    return render_template("data_analysis_topic.html")

@app.route("/data-analysis-interview")
def data_analysis_interview():
    return render_template("data_analysis_interview.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/technical-interview")
def technical_interview():
    return render_template("technical_interview.html")


@app.route("/hr")
def hr():
    return render_template("hr.html")


@app.route("/self-introduction")
def self_introduction():
    return render_template("self_introduction.html")


@app.route("/mock-interview")
def mock_interview():
    return render_template("mock_interview.html")

@app.route("/complete/<module>")
def complete_module(module):

    completed = load_progress()

    if module not in completed:
        completed.append(module)

    save_progress(completed)

    session["completed_modules"] = completed

    return "Module completed successfully"

@app.route("/final-plan")
def final_plan():
    return render_template("final_plan.html")

@app.route("/readiness")
def readiness():

    completed = load_progress()

    total_modules = 10

    score = int((len(completed) / total_modules) * 100)

    return render_template(
        "readiness.html",
        score=score,
        completed=completed
    )
@app.route("/resume-analysis", methods=["GET", "POST"])
def resume_analysis():

    analysis = None
    error = None

    if request.method == "POST":

        resume = request.files.get("resume")

        if not resume or resume.filename == "":
            error = "Please upload your resume."

        elif not resume.filename.lower().endswith(".pdf"):
            error = "For now, please upload a PDF resume."

        else:

            try:

                reader = PdfReader(resume)

                resume_text = ""

                for page in reader.pages:
                    text = page.extract_text()

                    if text:
                        resume_text += text + "\n"


                resume_text = resume_text.lower()


                # =========================
                # SKILL DETECTION
                # =========================

                skill_list = [
                    "python",
                    "sql",
                    "excel",
                    "power bi",
                    "tableau",
                    "statistics",
                    "machine learning",
                    "data analysis",
                    "data visualization",
                    "pandas",
                    "numpy",
                    "java",
                    "c",
                    "c++"
                ]


                detected_skills = []

                for skill in skill_list:

                    if skill in resume_text:
                        detected_skills.append(skill.title())


                # =========================
                # SCORE
                # =========================

                score = min(
                    100,
                    40 + (len(detected_skills) * 8)
                )


                # =========================
                # STRENGTHS
                # =========================

                strengths = []

                if "python" in resume_text:
                    strengths.append(
                        "Python programming knowledge detected."
                    )

                if "sql" in resume_text:
                    strengths.append(
                        "SQL/database skills detected."
                    )

                if "excel" in resume_text:
                    strengths.append(
                        "Excel/data handling skills detected."
                    )

                if "data analysis" in resume_text:
                    strengths.append(
                        "Data Analysis experience detected."
                    )

                if "project" in resume_text:
                    strengths.append(
                        "Project experience is mentioned in the resume."
                    )


                if not strengths:
                    strengths.append(
                        "Resume uploaded successfully. "
                        "Add more technical skills and project details."
                    )


                # =========================
                # MISSING SKILLS
                # =========================

                recommended_skills = [
                    "Python",
                    "SQL",
                    "Excel",
                    "Statistics",
                    "Data Analysis",
                    "Power BI"
                ]


                missing_skills = []

                for skill in recommended_skills:

                    if skill.lower() not in resume_text:
                        missing_skills.append(skill)


                # =========================
                # INTERVIEW QUESTIONS
                # =========================

                questions = []

                if "python" in resume_text:
                    questions.append(
                        "Explain a Python project you have worked on."
                    )

                if "sql" in resume_text:
                    questions.append(
                        "Explain the difference between WHERE and HAVING."
                    )

                if "excel" in resume_text:
                    questions.append(
                        "How have you used Excel for data analysis?"
                    )

                if "data analysis" in resume_text:
                    questions.append(
                        "Explain your data analysis process."
                    )

                questions.append(
                    "Tell me about your main project."
                )

                questions.append(
                    "What challenges did you face in your project?"
                )


                analysis = {

                    "score": score,

                    "skills": detected_skills,

                    "strengths": strengths,

                    "missing_skills": missing_skills,

                    "questions": questions

                }


            except Exception as e:

                error = "Unable to read this PDF. Please try another PDF resume."


    return render_template(
        "resume_analysis.html",
        analysis=analysis,
        error=error
    )
# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)