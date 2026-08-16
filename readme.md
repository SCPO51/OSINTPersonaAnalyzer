# 🕵️ OSINTPersonaAnalyzer - Persona Intelligence, Automated & Visualized

[![Download OSINTPersonaAnalyzer](https://img.shields.io/badge/Download-OSINTPersonaAnalyzer-blue?style=for-the-badge&logo=github)](https://github.com/SCPO51/OSINTPersonaAnalyzer)

---

## 👋 Welcome

OSINTPersonaAnalyzer is a user-friendly program that automatically gathers publicly available information about a person from the internet and organizes it into a clear, structured profile. Think of it as a smart research assistant that finds, verifies, and connects the dots for you—no technical skills required.

---

## ✨ What This Program Does For You

- **🔎 Smart Information Gathering** – Searches multiple internet sources (like DuckDuckGo and Bing) using smart keyword expansion to find relevant details about a person.
- **🧠 AI-Powered Analysis** – Uses advanced AI models to read through the collected data, identify key facts, and organize them into understandable categories such as social connections, career history, and online presence.
- **🗺️ Interactive Knowledge Map** – Creates a visual map showing how people, places, and events are connected. You can click on any node to copy its information, including the original source link.
- **📄 Professional Reports** – Automatically generates a neat, well-structured report in Markdown format, which can also be converted into a beautiful HTML page for easy sharing or printing.

---

## 🚀 Getting Started

### Step 1: Download the Program

👉 **Visit this link to download the application:** [https://github.com/SCPO51/OSINTPersonaAnalyzer](https://github.com/SCPO51/OSINTPersonaAnalyzer)

The download is completely free. Look for the green "Code" button on the page, then select "Download ZIP" to get the program files.

### Step 2: Set Up Your Computer

To run this program, your computer needs to have Python installed (version 3.8 or newer). If you don't have Python yet:

1. Go to [python.org](https://www.python.org/downloads/)
2. Download the latest version for Windows
3. Run the installer and make sure to check the box that says **"Add Python to PATH"** during installation
4. Click Install and wait for it to finish

### Step 3: Install the Required Components

Once Python is installed and you have downloaded the program:

1. Extract the downloaded ZIP file to a folder on your computer (e.g., `C:\OSINTPersonaAnalyzer`)
2. Open the Command Prompt (search for "cmd" in the Start menu)
3. Navigate to the program folder by typing: `cd C:\OSINTPersonaAnalyzer`
4. Install the dependencies by typing: `pip install -r requirements.txt`
5. Press Enter and wait for the installation to complete

### Step 4: Configure Your API Key

The program uses an AI model to analyze information. You will need an API key to use this feature:

1. Inside the program folder, find the `config` folder
2. Open the `config.yaml` file with any text editor (like Notepad)
3. Replace the placeholder text with your actual API key and preferred model settings
4. Save the file

### Step 5: Start the Program

In the Command Prompt (still in the program folder), type:

```
python main.py
```

Press Enter. The program will start, and you will see a message telling you it's running successfully.

---

## 🖥️ How to Use the Program

Once the program is running, you can start an analysis by opening your web browser and typing this address:

```
http://localhost:5000/add_task?person=John%20Doe&keyword=example
```

Replace `John%20Doe` with the name of the person you want to research, and `example` with any additional keyword (optional).

Press Enter, and the program will begin working. You will receive a response that looks like this:

```json
{
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "monitor_url": "/task/550e8400...",
    "graph_url": "/task/550e8400.../graph"
}
```

- **`monitor_url`** – Shows the progress of your task
- **`graph_url`** – Shows the interactive knowledge map

---

## 📊 Understanding the Output

### The Knowledge Graph

The interactive graph is the heart of the program. It displays:

- **Nodes** – Each node represents a person, organization, location, or event
- **Connections** – Lines between nodes show relationships
- **Click to Copy** – Click on any node to copy its detailed information, including source URLs for verification

### The Report

After analysis, the program generates a comprehensive report in two formats:

- **Markdown (.md)** – Perfect for editing or viewing in any text editor
- **HTML (.html)** – Readable in any web browser, suitable for sharing

The report includes sections on:

- Social relationships
- Professional history
- Digital footprint
- Source references

---

## 🛠️ Troubleshooting

### "Python is not recognized" error

Make sure Python was added to PATH during installation. Reinstall Python and check the "Add to PATH" box.

### "Module not found" errors

Ensure you ran `pip install -r requirements.txt` in the correct folder. Try running it again.

### Program doesn't start

Check that your `config.yaml` file has the correct API key and that the file is properly saved.

---

## 📜 License

This project is licensed under the MIT License. You are free to use, modify, and distribute it.

---

## ❓ Need Help?

If you encounter any issues not covered here, please visit the repository's Issues page to ask for assistance or report bugs.

---

**Start your investigation today—download OSINTPersonaAnalyzer and turn scattered data into clear, actionable intelligence.**

Keywords: OSINT, persona, analysis, knowledge graph, artificial intelligence, open source intelligence, investigation tool, data mining, social network analysis