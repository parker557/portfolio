# Project Portfolio

This folder collects selected academic, personal, and prototype projects by Zheng Jiang. The projects cover AI/VLM workflows, full-stack web applications, cybersecurity, databases, systems programming, data analysis, and Java/Python/C development.

## Featured Projects

### Qwen3-VL DuoImage Detector

Path: [Qwen3-VL-DuoImage-Detector](./Qwen3-VL-DuoImage-Detector/)

A multimodal vision-language batch inference tool for paired-image object matching. Given a reference image and a test image, the script asks Qwen3-VL to find matching objects, returns bounding boxes, and exports JSON, CSV/XLSX, and visualized results.

Tech: Python, PyTorch, Hugging Face Transformers, Qwen3-VL, Pillow, OpenPyXL, batch inference, VLM prompting.

### Property Management System

Path: [PropertyManagementSystem](./PropertyManagementSystem/)

A full-stack property management prototype with owner and staff dashboards, session-based login, issue reporting, chat workflows, and a DeepSeek/OpenAI-compatible API integration for AI-assisted responses.

Tech: Node.js, Express, Socket.IO, OpenAI SDK, DeepSeek API, HTML/CSS/JavaScript, server-side sessions.

### E2EE Chat Network Application

Path: [E2EE chat network application](./E2EE%20chat%20network%20application/)

A secure chat application focused on authentication, MFA/OTP, end-to-end message encryption, and TLS deployment. The project includes a report, demo video, Docker configuration, and web app implementation.

Tech: Flask, MySQL, Docker Compose, TLS certificates, OTP/MFA, E2EE design.

### E-Commerce Real Estate Website

Path: [E-commerce real estate website](./E-commerce%20real%20estate%20website/)

A React/Firebase real-estate web application with authentication, Firestore configuration, Material UI components, and payment-related integrations.

Tech: React, Firebase, Firestore, Material UI, Redux Toolkit, Stripe, Adyen.

### AI Finance Advisor

Path: [finance_advise](./finance_advise/)

A Python-based AI finance assistant that generates monthly and daily Markdown reports using DeepSeek API calls and local history/configuration files.

Tech: Python, DeepSeek API, Markdown report generation, local data storage, CLI workflow.

Note: This is a software/AI workflow demo, not financial advice.

## All Projects

| Project | Area | Main Stack | Summary |
| --- | --- | --- | --- |
| [Appointment Organizer](./Appointment%20Organizer/) | Systems / Scheduling | C | Command-line appointment scheduler supporting private time, meetings, group study, gatherings, scheduling exports, and rejected-appointment output. |
| [Data-Mining Heart Attack Analysis and Prediction](./Data-Mining%20Heart_Attack_Analysis_and_Prediction/) | Data Analysis / ML | Python, Jupyter, pandas, NumPy, seaborn | Exploratory analysis and prediction workflow for a heart-attack dataset, including feature description, visualization, and notebook-based modeling. |
| [E-commerce real estate website](./E-commerce%20real%20estate%20website/) | Full-Stack Web | React, Firebase, Firestore, Material UI, Stripe/Adyen | Real-estate commerce web app with modern React UI, Firebase backend services, and payment-related dependencies. |
| [E2EE chat network application](./E2EE%20chat%20network%20application/) | Cybersecurity / Web | Flask, MySQL, Docker, TLS, OTP | Secure chat application with authentication lifecycle management, MFA/OTP, TLS configuration, and end-to-end encryption design. |
| [finance_advise](./finance_advise/) | AI Application | Python, DeepSeek API, Markdown | AI-assisted investment-report workflow with local sessions, daily/monthly reports, and command-line utilities. |
| [Hashmapping](./Hashmapping/) | Java / Interpreter Design | Java, JUnit | Command-line interpreter project for a simple programming language, including expression definition, user manual, and Java implementation artifacts. |
| [Jupyter-Labs](./Jupyter-Labs/) | Teaching / Full-Stack Lab | Node.js, Express, PostgreSQL, Knex, HTML/CSS/JS | Task Management System lab materials, answer key, schema/seed SQL, screenshots, and guided full-stack teaching content. |
| [library Database System](./library%20Database%20System/) | Database Systems | Java, SQL, ER modeling | Library management system with user/admin workflows, ER design, relational schema work, SQL constraints, report, and user guide. |
| [Password Management System](./Password%20Management%20System/) | Security / Python | Python | Password evaluation and random password generation system with account/password storage concepts and project report. |
| [Product Information Management System](./Product%20Information%20Management%20System/) | Java / OOP | Java | Personal/product information manager using OOP design around contacts, events, tasks, plain text records, search, and update operations. |
| [PropertyManagementSystem](./PropertyManagementSystem/) | Full-Stack / AI App | Node.js, Express, Socket.IO, OpenAI SDK, DeepSeek | Property owner/staff dashboard with chat, issue reporting, AI-assisted response generation, and session handling. |
| [Qwen3-VL-DuoImage-Detector](./Qwen3-VL-DuoImage-Detector/) | GenAI / Computer Vision | Python, Qwen3-VL, PyTorch, Transformers | Batch VLM detector for paired image matching, bounding-box extraction, JSON/CSV/XLSX output, visualization, and benchmarking. |

## Repository Notes

- API keys and local configuration files should be provided through environment variables or local files that are not committed.
- Generated dependency folders such as `node_modules/`, Java build outputs, local cache files, and private configuration files are intentionally excluded from Git.
- Some projects include academic reports or demo assets; the source folders are the primary materials for code review.
- For a recruiter-facing portfolio, the strongest projects to pin are `Qwen3-VL-DuoImage-Detector`, `PropertyManagementSystem`, `E2EE chat network application`, and `E-commerce real estate website`.

## Suggested Next Improvements

1. Add screenshots or short GIFs to each major project README.
2. Replace default README templates with project-specific setup instructions.
3. Move large videos to a release asset, GitHub Pages page, or external media folder.
4. Add a top-level website page that links to these projects with screenshots and short case studies.
