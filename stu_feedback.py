import streamlit as st
import csv
import re
import google.generativeai as genai

# Configure Google Gemini API
GOOGLE_API_KEY = "AIzaSyC8oElIjQQsSR3r0qG0KYwmboSIZ7gQvH4"
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini Feedback Prompt
def generate_feedback_prompt(name, score, total, student_answers):
    return f"""
    Student: {name}
    Score: {score}/{total}
    Short answers and MCQ selections: {student_answers}

    Based on the score and answers, provide a personalized 3-4 line performance feedback. 
    Highlight strengths, weaknesses, and one tip for improvement.
    """

# Generate Feedback Using Gemini
def generate_feedback(name, score, total, student_answers):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = generate_feedback_prompt(name, score, total, student_answers)
        response = model.generate_content(prompt)
        return response.text.strip() if response else "No feedback generated."
    except Exception as e:
        return f"⚠️ Error generating feedback: {e}"

st.set_page_config(page_title="Java Basics Test Platform", layout="centered")
st.title("🧠 Java Test Platform")

if "page" not in st.session_state:
    st.session_state.page = "info"

if st.session_state.page == "info":
    st.subheader("Enter Student Information")
    name = st.text_input("Student Name")
    reg_no = st.text_input("Registration Number")
    email = st.text_input("Email")

    if st.button("Next"):
        if not name.isalpha():
            st.warning("Name must contain only alphabets.")
        elif not re.match(r"^[a-zA-Z0-9]+$", reg_no):
            st.warning("Registration number must be alphanumeric.")
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            st.warning("Please enter a valid email address.")
        else:
            st.session_state.name = name
            st.session_state.reg_no = reg_no
            st.session_state.email = email
            st.session_state.page = "choose_set"

if st.session_state.page == "choose_set":
    st.subheader("Select the Test Type")
    test_type = st.radio(
        "Choose a set:",
        ("1. Basic Java (Core Concepts)", "2. Intermediate Java (OOP & Advanced Core Java)", "3. Advanced Java (Enterprise & Frameworks)")
    )
    if st.button("Start Test"):
        st.session_state.test_type = test_type
        st.session_state.page = "quiz"

if st.session_state.page == "quiz":
    st.subheader("Answer the following questions")

    selected_test = st.session_state.test_type

    short_questions, mcq_questions, correct_mcq_answers = [], [], []

    if "Basic" in selected_test:
        short_questions = [
            "Q1: What is a variable in Java?",
            "Q2: Explain how arrays are used in Java.",
            "Q3: What is the difference between a class and an object?"
        ]
        mcq_questions = [
            ("Q4: Which data type is used to create a variable that should store text?", ["--Select--", "string", "myString", "String", "Txt"]),
            ("Q5: Which loop is guaranteed to execute at least once?", ["--Select--", "for", "while", "do-while", "None"]),
            ("Q6: What is the size of an int in Java?", ["--Select--", "2 bytes", "4 bytes", "8 bytes", "Depends on system"]),
            ("Q7: What is the correct syntax to create a method in Java?", ["--Select--", "void myMethod()", "method myMethod()", "function myMethod()", "def myMethod()"]),
            ("Q8: Which of these is a correct OOP principle?", ["--Select--", "Inheritance", "Encapsulation", "Polymorphism", "All of the above"]),
            ("Q9: What is the output stream class in Java?", ["--Select--", "Scanner", "InputStream", "OutputStream", "PrintWriter"]),
            ("Q10: Which statement is used to handle exceptions?", ["--Select--", "catch", "throw", "try-catch", "final"]),
            ("Q11: Which of these is not a primitive data type?", ["--Select--", "int", "float", "String", "double"]),
            ("Q12: What does JVM stand for?", ["--Select--", "Java Variable Machine", "Java Virtual Machine", "Java Verified Machine", "None"]),
            ("Q13: How do you declare an array in Java?", ["--Select--", "int[] arr;", "int arr[];", "Both A and B", "None"]),
            ("Q14: Which keyword is used to define a class?", ["--Select--", "define", "class", "object", "struct"]),
            ("Q15: What does System.out.println do?", ["--Select--", "Print output", "Input line", "Scan data", "Display dialog"])
        ]
        correct_mcq_answers = [
            "String", "do-while", "4 bytes", "void myMethod()", "All of the above", 
            "OutputStream", "try-catch", "String", "Java Virtual Machine", 
            "Both A and B", "class", "Print output"
        ]
    elif "Intermediate" in selected_test:
        short_questions = [
            "Q1: What is abstraction in Java?",
            "Q2: Define a Java interface and its purpose.",
            "Q3: How does the Collection Framework benefit Java developers?"
        ]
        mcq_questions = [
            ("Q4: Which access modifier makes a member accessible only within its own package?", ["--Select--", "private", "protected", "default", "public"]),
            ("Q5: What is the super class of all classes in Java?", ["--Select--", "Object", "String", "Class", "Base"]),
            ("Q6: Which interface provides unique elements in a collection?", ["--Select--", "List", "Map", "Set", "Queue"]),
            ("Q7: What is autoboxing?", ["--Select--", "Converting object to primitive", "Converting primitive to object", "Wrapping data", "Unboxing class"]),
            ("Q8: Which thread method starts a thread execution?", ["--Select--", "run()", "execute()", "start()", "begin()"]),
            ("Q9: What is the use of the File class in Java?", ["--Select--", "To create and delete files", "To connect to a database", "To display UI", "None"]),
            ("Q10: What does the keyword 'abstract' mean?", ["--Select--", "Method with no body", "Class cannot be inherited", "Only interfaces", "All of the above"]),
            ("Q11: What is an Enum?", ["--Select--", "A final variable", "A type of interface", "A special class for constants", "None"]),
            ("Q12: Which collection maintains insertion order?", ["--Select--", "HashSet", "TreeSet", "LinkedHashSet", "Set"]),
            ("Q13: Which class is used to handle input from the console?", ["--Select--", "Scanner", "BufferedReader", "InputStreamReader", "All"]),
            ("Q14: What is the use of generics in Java?", ["--Select--", "Code reuse", "Type safety", "Both A and B", "None"]),
            ("Q15: Which method is used to create threads?", ["--Select--", "new Thread()", "start()", "init()", "run()"])
        ]
        correct_mcq_answers = [
            "default", "Object", "Set", "Converting primitive to object", "start()", 
            "To create and delete files", "Method with no body", "A special class for constants", 
            "LinkedHashSet", "Scanner", "Both A and B", "start()"
        ]
    else:
        short_questions = [
            "Q1: What is JDBC and how is it used in Java?",
            "Q2: Define a servlet and its use in web applications.",
            "Q3: What is the role of annotations in Spring Framework?"
        ]
        mcq_questions = [
            ("Q4: Which package is used for database connectivity in Java?", ["--Select--", "java.sql", "java.db", "javax.db", "java.jdbc"]),
            ("Q5: Which method is used to fetch data from a ResultSet?", ["--Select--", "get()", "fetch()", "next()", "retrieve()"]),
            ("Q6: Which library is used for building REST APIs in Spring?", ["--Select--", "Spring REST", "Spring Web", "Spring Boot", "SpringMVC"]),
            ("Q7: What does the @Autowired annotation do?", ["--Select--", "Injects dependencies", "Starts app", "Declares a class", "Configures DB"]),
            ("Q8: What is the purpose of Maven in Java projects?", ["--Select--", "Version control", "Dependency management", "Database connection", "None"]),
            ("Q9: Which keyword is used in Lambda expressions?", ["--Select--", "->", "=>", "::", "function"]),
            ("Q10: What is JUnit used for?", ["--Select--", "Logging", "Testing", "Debugging", "Packaging"]),
            ("Q11: What is the purpose of HttpServlet?", ["--Select--", "To manage HTTP requests", "To create GUI", "To read files", "None"]),
            ("Q12: Which Java GUI framework is lightweight?", ["--Select--", "Swing", "AWT", "JavaFX", "None"]),
            ("Q13: What does the stream API do in Java 8?", ["--Select--", "Handle files", "Parallel processing", "Functional style operations", "None"]),
            ("Q14: Which method is used to open a database connection?", ["--Select--", "getConnection()", "connectDB()", "open()", "startDB()"]),
            ("Q15: What is @RequestMapping used for in Spring?", ["--Select--", "Map HTTP requests", "Inject Beans", "Handle database", "Generate reports"])
        ]
        correct_mcq_answers = [
            "java.sql", "next()", "Spring Web", "@Autowired", "Dependency management", 
            "->", "Testing", "To manage HTTP requests", "Swing", 
            "Functional style operations", "getConnection()", "Map HTTP requests"
        ]

    short_answers = [st.text_input(q) for q in short_questions]
    mcq_answers = []
    all_answered = True

    for idx, (question, options) in enumerate(mcq_questions):
        answer = st.radio(question, options, key=f"q_{idx}")
        if answer == "--Select--":
            all_answered = False
        mcq_answers.append(answer)

    if st.button("Submit"):
        if not all(x.strip() for x in short_answers):
            st.warning("Please answer all short questions.")
        elif not all_answered:
            st.warning("Please select an answer for each MCQ.")
        else:
            score = 0
            incorrect_mcqs = []

            for i, (user_ans, correct_ans) in enumerate(zip(mcq_answers, correct_mcq_answers)):
                if "Basic" in selected_test and i >= 12:
                    break
                if "Intermediate" in selected_test and not (0 <= i < 12):
                    continue
                if "Advanced" in selected_test and i < 0:
                    continue
                if user_ans == correct_ans:
                    score += 1
                else:
                    incorrect_mcqs.append((mcq_questions[i][0], user_ans, correct_ans))

            try:
                with open("performance.csv", "a", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        st.session_state.name,
                        st.session_state.reg_no,
                        st.session_state.email,
                        st.session_state.test_type,
                        *short_answers,
                        *mcq_answers,
                        score
                    ])
            except Exception as e:
                st.error(f"Failed to save data: {e}")

            st.success("✅ Test submitted successfully!")
            st.subheader(f"📢 Feedback for {st.session_state.name}")
            st.write(f"Score: {score}/15")

            if "feedback_cache" not in st.session_state:
                st.session_state.feedback_cache = {}

            cache_key = (st.session_state.reg_no, score)

            if cache_key in st.session_state.feedback_cache:
                st.markdown(st.session_state.feedback_cache[cache_key])
            else:
                try:
                    feedback = generate_feedback(
                        name=st.session_state.name,
                        score=score,
                        total=15,
                        student_answers=short_answers + mcq_answers
                    )
                    st.session_state.feedback_cache[cache_key] = feedback
                    st.markdown(feedback)
                except Exception as e:
                    st.warning(f"⚠️ AI Feedback generation failed: {e}")

            if incorrect_mcqs:
                st.markdown("### ❌ Correct Answers for Your Mistakes:")
                for q, user_ans, correct_ans in incorrect_mcqs:
                    st.markdown(f"- **{q}**  \nYour answer: ❌ _{user_ans}_  \nCorrect answer: ✅ _{correct_ans}_")

            st.session_state.page = "info"
