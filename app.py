import streamlit as st
import pdfplumber
import docx
import re

# Login credentials
USERNAME = "Shreyash Kumar Sahoo"
PASSWORD = "Sk@2026"

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# Skills Database
SKILLS_DB = [
    "python", "java", "c", "c++", "javascript", "html", "css",
    "react", "nodejs", "mongodb", "mysql", "sql",
    "machine learning", "deep learning", "data science",
    "aws", "docker", "git", "github", "linux",
    "excel", "power bi", "communication", "leadership", "teamwork"
]

# Extract text from PDF
def extract_pdf_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Extract text from DOCX
def extract_docx_text(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Extract Email
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not Found"

# Extract Phone Number
def extract_phone(text):
    match = re.search(r'(\+91[\-\s]?)?[0-9]{10}', text)
    return match.group(0) if match else "Not Found"

# Extract Name (simple approach)
def extract_name(text):
    lines = text.split("\n")
    for line in lines[:5]:
        if len(line.split()) <= 4 and len(line.strip()) > 2:
            return line.strip()
    return "Not Found"

# Extract Skills
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))

# Extract Education
def extract_education(text):
    keywords = [
        "b.tech", "btech", "b.e", "be",
        "m.tech", "mtech", "mba",
        "bsc", "msc", "phd",
        "high school", "intermediate"
    ]

    found = []

    for keyword in keywords:
        if keyword.lower() in text.lower():
            found.append(keyword)

    return list(set(found))

# Streamlit UI
st.set_page_config(page_title="Resume Parser", page_icon="📄")
if not st.session_state.logged_in:
    login()
    st.stop()

st.sidebar.title("About")

st.sidebar.info(
    "This project extracts candidate information such as "
    "Name, Email, Phone Number, Skills and Education from resumes."
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("📄 AI Resume Parser")
st.markdown("### Extract candidate information from PDF and DOCX resumes")

st.write("Upload a PDF or DOCX resume to extract details.")

uploaded_file = st.file_uploader(
    "Choose Resume",
    type=["pdf", "docx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".pdf"):
        text = extract_pdf_text(uploaded_file)
    else:
        text = extract_docx_text(uploaded_file)

    st.success("Resume Uploaded Successfully!")

    st.subheader("Parsed Information")

    st.write("### 👤 Name")
    st.write(extract_name(text))

    st.write("### 📧 Email")
    st.write(extract_email(text))

    st.write("### 📱 Phone")
    st.write(extract_phone(text))
    st.write("### 💻 Skills")
    skills = extract_skills(text)

    if skills:
        for skill in skills:
            st.success(f"✅ {skill.title()}")
    else:
        st.warning("No skills detected")

    st.write("### 🎓 Education")
    education = extract_education(text)

    if education:
        for edu in education:
            st.info(f"🎓 {edu}")
    else:
        st.warning("No education details detected")

    with st.expander("📄 Resume Text"):
        st.write(text)