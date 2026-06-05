# Project Portfolio

This folder is an index of projects I can talk through in an interview. Some are academic assignments, some are prototypes, and a few are closer to real product work. I kept the notes practical: what the project does, the main stack, and what I would point to first.

## Start Here

### Qwen3-VL DuoImage Detector

Path: [Qwen3-VL-DuoImage-Detector](./Qwen3-VL-DuoImage-Detector/)

A Python tool for paired-image detection. It takes a reference image and a test image, asks Qwen3-VL to find matching objects, then writes bounding boxes to JSON, CSV or XLSX and saves rendered result images.

Good code to review: model loading, prompt construction, coordinate conversion, batch output handling, and timing runs.

Stack: Python, PyTorch, Hugging Face Transformers, Qwen3-VL, Pillow, OpenPyXL.

### Property Management System

Path: [PropertyManagementSystem](./PropertyManagementSystem/)

A full-stack property management prototype with owner and staff dashboards, issue reporting, chat, session login, and an AI-assisted response flow using an OpenAI-compatible API.

Good code to review: Express routes, Socket.IO chat flow, session handling, and the server-side AI request path.

Stack: Node.js, Express, Socket.IO, OpenAI SDK, DeepSeek API, HTML, CSS, JavaScript.

### E2EE Chat Network Application

Path: [E2EE chat network application](./E2EE%20chat%20network%20application/)

A secure chat application built around authentication, MFA with OTP, TLS deployment, and end-to-end encryption design. The folder includes implementation files, a report, Docker setup, and demo materials.

Good code to review: login flow, database use, Docker Compose setup, TLS configuration, and message-handling logic.

Stack: Flask, MySQL, Docker Compose, TLS, OTP, end-to-end encryption design.

### E-Commerce Real Estate Website

Path: [E-commerce real estate website](./E-commerce%20real%20estate%20website/)

A React and Firebase real-estate web app with authentication, Firestore-backed data, Material UI components, Redux state management, and payment-related integrations.

Good code to review: React component structure, Firebase integration, routing, and payment-provider wiring.

Stack: React, Firebase, Firestore, Material UI, Redux Toolkit, Stripe, Adyen.

### AI Finance Advisor

Path: [finance_advise](./finance_advise/)

A local Python reporting tool that calls a language model API and produces daily or monthly Markdown reports from local history and configuration files.

Good code to review: report generation, API-call structure, local file handling, and CLI flow.

Stack: Python, DeepSeek API, Markdown.

Note: this is a software and AI workflow demo, not financial advice.

## Full Index

| Project | Area | Main Stack | What To Look At |
| --- | --- | --- | --- |
| [Appointment Organizer](./Appointment%20Organizer/) | Systems and scheduling | C | Command-line scheduling, rejected appointment output, and file export logic. |
| [Data-Mining Heart Attack Analysis and Prediction](./Data-Mining%20Heart_Attack_Analysis_and_Prediction/) | Data analysis | Python, Jupyter, pandas, NumPy, seaborn | Notebook-based analysis, visualization, and basic prediction workflow. |
| [E-commerce real estate website](./E-commerce%20real%20estate%20website/) | Full-stack web | React, Firebase, Firestore, Material UI, Stripe, Adyen | React app structure, Firebase config pattern, and payment-related integration. |
| [E2EE chat network application](./E2EE%20chat%20network%20application/) | Security and web | Flask, MySQL, Docker, TLS, OTP | Authentication, MFA, TLS deployment, and encrypted-message design. |
| [finance_advise](./finance_advise/) | AI application | Python, DeepSeek API, Markdown | Local report generation and API-driven assistant workflow. |
| [Hashmapping](./Hashmapping/) | Java and interpreter design | Java, JUnit | Simple language interpreter, expression handling, and test artifacts. |
| [Jupyter-Labs](./Jupyter-Labs/) | Teaching and full-stack lab | Node.js, Express, PostgreSQL, Knex, HTML, CSS, JavaScript | Lab material, schema and seed files, screenshots, and answer key. |
| [library Database System](./library%20Database%20System/) | Database systems | Java, SQL, ER modeling | Relational schema, constraints, admin and user workflows, report and guide. |
| [Password Management System](./Password%20Management%20System/) | Security and Python | Python | Password evaluation, random password generation, and account storage concept. |
| [Product Information Management System](./Product%20Information%20Management%20System/) | Java and OOP | Java | Contact, event, task, search, and update logic around OOP design. |
| [PropertyManagementSystem](./PropertyManagementSystem/) | Full-stack AI app | Node.js, Express, Socket.IO, OpenAI SDK, DeepSeek API | Owner and staff dashboards, chat, issue reporting, and AI-assisted responses. |
| [Qwen3-VL-DuoImage-Detector](./Qwen3-VL-DuoImage-Detector/) | GenAI and computer vision | Python, Qwen3-VL, PyTorch, Transformers | Paired-image matching, bounding-box output, visualization, and timing tests. |

## Before Running

- API keys and private config values are expected through local environment variables or local files that are not committed.
- Dependency folders such as `node_modules/`, Java build outputs, caches, generated reports, and private config files are excluded.
- Large demo videos are not stored in Git. I would host them through GitHub Releases, Git LFS, Google Drive, or a portfolio site.
- A few folders started as coursework, so the report is sometimes cleaner than the code. For interviews, the best folders to open first are `Qwen3-VL-DuoImage-Detector`, `PropertyManagementSystem`, `E2EE chat network application`, and `E-commerce real estate website`.

## What I Would Improve Next

- Add one screenshot or short GIF to each featured project.
- Add project-specific setup steps where a folder still depends on old coursework instructions.
- Move large demo media to GitHub Releases or a small portfolio website.
- Add a simple GitHub Pages site with screenshots, short case studies, and links back to these folders.
