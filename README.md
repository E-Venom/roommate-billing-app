# 🏠 Roommate Billing App

A Python-based application that calculates how roommates should split shared bills proportionally based on how long each person stayed in the house.

The application generates a clean, professionally formatted PDF report and optionally uploads it to the cloud for easy sharing.

---

## 🚀 Features

- 📊 Proportional bill splitting based on occupancy duration  
- 🧠 Object-Oriented Design (`Bill`, `Roommate`, `PDFReport`, `FileSharer`)  
- 🧾 Automatically generated, formatted PDF reports  
- ☁️ Optional cloud upload via Filestack (returns a shareable link)  
- 📁 Clean project structure with separation of concerns  
- 🔐 Secure API key handling using `.env`  

---

## 🧠 How It Works

Each roommate pays a share of the bill based on:
share = (days stayed / total days) * bill amount

## 🖥️ Example Output

- John pays: $53.33
- Mary pays: $66.67
- PDF generated at: generated_pdf_reports/Report.pdf
Shareable link: https://cdn.filestackcontent.com/
...
## ⚙️ Installation

## ▶️ How to Run
```bash
python main.py
```
## ‍💻 Author

Michael Bryant
M.S. Computer Science — Colorado School of Mines