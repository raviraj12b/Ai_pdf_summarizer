# 🚀 Easy Setup Guide
## Smart AI PDF Summarizer - Step-by-Step Installation

---

## 📋 Before You Start

### System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| **Operating System** | Windows 10, macOS 10.15, Ubuntu 20.04 | Latest versions |
| **RAM** | 8GB | 16GB |
| **Free Disk Space** | 10GB | 20GB |
| **Python** | 3.8 | 3.10+ |
| **Internet** | Required for setup | Not needed after |

### Time Required
- **First-time setup:** 15-20 minutes
- **Subsequent runs:** 2 minutes

---

## 🎯 Installation Path

Choose your path based on experience:

### 🟢 Beginner (Recommended)
Follow detailed step-by-step instructions below

### 🟡 Intermediate
Skip to [Quick Install](#-quick-install-for-intermediate-users)

### 🔴 Advanced
See [Advanced Setup](#-advanced-setup)

---

## 📦 Step-by-Step Installation (Beginners)

### Step 1: Install Python

#### Windows
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.10 or later
3. **IMPORTANT:** Check ✅ "Add Python to PATH" during installation
4. Click "Install Now"
5. Wait for installation to complete

**Verify Installation:**
```bash
# Open Command Prompt (Windows Key + R, type "cmd")
python --version
```

Should show: `Python 3.10.x` or higher

#### macOS
```bash
# Install using Homebrew (recommended)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.10
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv
```

---

### Step 2: Install Ollama

Ollama runs AI models on your computer.

#### Windows
1. Visit [ollama.ai/download](https://ollama.ai/download)
2. Click "Download for Windows"
3. Run the downloaded `.exe` file
4. Ollama will start automatically
5. Look for Ollama icon in system tray (bottom-right)

#### macOS
**Option A: Using Installer**
1. Visit [ollama.ai/download](https://ollama.ai/download)
2. Download macOS installer
3. Open `.dmg` file
4. Drag Ollama to Applications

**Option B: Using Terminal**
```bash
curl https://ollama.ai/install.sh | sh
```

#### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

**Verify Ollama Installation:**
```bash
ollama --version
```

Should show version number like `ollama version 0.x.x`

---

### Step 3: Download AI Model

Choose ONE model to start (you can add more later):

#### Option 1: Llama 2 (Recommended - Balanced)
```bash
ollama pull llama2
```

#### Option 2: Mistral (Best Quality)
```bash
ollama pull mistral
```

#### Option 3: Phi (Fastest)
```bash
ollama pull phi
```

**Wait for download to complete** (3-5 minutes depending on internet)

**Verify Model Downloaded:**
```bash
ollama list
```

Should show your downloaded model.

---

### Step 4: Download Project Files

#### Option A: Download ZIP (Easiest)
1. Go to project GitHub page
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract ZIP to a folder (e.g., `C:\Projects\smart-ai-pdf-summarizer`)

#### Option B: Using Git
```bash
git clone https://github.com/raviraj12b/Ai_pdf_summarizer.git
cd smart-ai-pdf-summarizer
```

---

### Step 5: Open Project Folder

#### Windows
1. Open File Explorer
2. Navigate to project folder
3. Right-click inside folder
4. Select "Open in Terminal" or "Open PowerShell here"

#### macOS/Linux
```bash
cd /path/to/smart-ai-pdf-summarizer
```

---

### Step 6: Create Virtual Environment

**What is a virtual environment?**  
A clean space for your project's Python packages (recommended but optional).

```bash
# Create virtual environment
python -m venv venv
```

**Activate it:**

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

**You should see `(venv)` at the start of your command line.**

---

### Step 7: Install Python Packages

```bash
pip install -r requirements.txt
```

**Wait 2-3 minutes for installation.**

**Troubleshooting:**
If you get an error, try:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 8: Start Ollama Server

**Keep this terminal open!**

```bash
ollama serve
```

You should see:
```
Ollama server is running on http://localhost:11434
```

**Leave this running and open a NEW terminal for next step.**

---

### Step 9: Run the Application

**In a NEW terminal (with virtual environment activated):**

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Your browser will open automatically!** 🎉

---

### Step 10: Use the App

1. **Upload PDF:**
   - Click "Browse files"
   - Select your PDF document

2. **Configure:**
   - Select Model: Choose your installed model
   - Summary Type: Try "Abstractive" first
   - Length: Choose "Medium"

3. **Generate:**
   - Click "Generate AI Summary"
   - Wait 15-60 seconds

4. **Download:**
   - Click "Download as TXT" or "Download as PDF"

---

## ⚡ Quick Install (For Intermediate Users)

```bash
# 1. Install Ollama
curl https://ollama.ai/install.sh | sh  # macOS/Linux
# Or download from ollama.ai for Windows

# 2. Pull AI model
ollama pull llama2

# 3. Clone project
git clone https://github.com/raviraj12b/Ai_pdf_summarizer.git
cd smart-ai-pdf-summarizer

# 4. Setup Python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 5. Run (in separate terminals)
# Terminal 1:
ollama serve

# Terminal 2:
streamlit run app.py
```

---

## 🔧 Advanced Setup

### Custom Ollama Host

If running Ollama on different port or server:

Edit `backend/ollama_client.py`:
```python
def __init__(self, base_url="http://localhost:11434"):
    # Change to your URL
    self.base_url = "http://your-server:port"
```

### Docker Installation (Advanced)

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Copy project
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Pull model
RUN ollama pull llama2

# Expose ports
EXPOSE 8501 11434

# Run
CMD ollama serve & streamlit run app.py
```

### Custom Model Configuration

Create `config.yaml`:
```yaml
ollama:
  host: localhost
  port: 11434
  default_model: llama2
  
summarization:
  default_type: abstractive
  default_length: medium
  max_context: 8000
```

---

## 🐛 Troubleshooting

### Problem: "python: command not found"

**Solution:**
```bash
# Try python3 instead
python3 --version

# Or reinstall Python with PATH option checked
```

### Problem: "pip: command not found"

**Solution:**
```bash
python -m ensurepip --upgrade
```

### Problem: "Ollama connection refused"

**Solution:**
1. Check if Ollama is running:
   ```bash
   ollama list
   ```
2. Start Ollama:
   ```bash
   ollama serve
   ```
3. Verify port 11434 is available

### Problem: "No module named 'streamlit'"

**Solution:**
```bash
# Ensure virtual environment is activated
# Look for (venv) in terminal

# Reinstall packages
pip install -r requirements.txt
```

### Problem: "Port 8501 already in use"

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Problem: "Model not found"

**Solution:**
```bash
# List installed models
ollama list

# Pull the model
ollama pull llama2
```

### Problem: "Out of memory"

**Solutions:**
1. Close other applications
2. Use smaller model:
   ```bash
   ollama pull phi
   ```
3. Restart computer
4. Upgrade RAM

---

## 🔄 Daily Usage

### Starting the App (After Initial Setup)

1. **Open terminal in project folder**

2. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Start Ollama (Terminal 1):**
   ```bash
   ollama serve
   ```

4. **Run app (Terminal 2):**
   ```bash
   streamlit run app.py
   ```

### Stopping the App

1. Press `Ctrl+C` in both terminals
2. Type `deactivate` to exit virtual environment

---

## 📊 System Check Script

Create `check_system.py`:
```python
#!/usr/bin/env python3
import sys
import subprocess

def check_python():
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 8

def check_ollama():
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True)
        print(f"✓ Ollama installed")
        return True
    except:
        print("✗ Ollama not found")
        return False

def check_models():
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True)
        models = result.stdout
        print(f"✓ Models: {models}")
        return 'llama2' in models or 'mistral' in models
    except:
        print("✗ No models found")
        return False

if __name__ == "__main__":
    print("System Check for Smart AI PDF Summarizer\n")
    
    checks = [
        ("Python 3.8+", check_python()),
        ("Ollama", check_ollama()),
        ("AI Models", check_models())
    ]
    
    all_passed = all(check[1] for check in checks)
    
    if all_passed:
        print("\n✅ All checks passed! You're ready to go.")
    else:
        print("\n❌ Some checks failed. Please review setup instructions.")
```

Run: `python check_system.py`

---


---

## 📝 Checklist

### Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Python added to PATH
- [ ] Ollama installed
- [ ] At least one AI model downloaded
- [ ] Project files downloaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Can run `ollama serve`
- [ ] Can run `streamlit run app.py`
- [ ] App opens in browser

### First Run Checklist

- [ ] Ollama server running
- [ ] App started successfully
- [ ] Can upload PDF
- [ ] Model list showing
- [ ] Can generate summary
- [ ] Can download results

---

## 🆘 Getting Help

### If You're Stuck

1. **Check this guide again** - Most issues covered here
2. **Read error messages** - They usually tell you what's wrong
3. **Check main README.md** - Additional troubleshooting
4. **Search GitHub Issues** - Someone may have had same problem
5. **Ask for help** - Open a GitHub issue with:
   - Your operating system
   - Python version (`python --version`)
   - Ollama version (`ollama --version`)
   - Error message (full text)
   - What you were trying to do

### Useful Commands for Debugging

```bash
# Check Python
python --version

# Check pip
pip --version

# Check Ollama
ollama --version
ollama list

# Check installed packages
pip list

# Test Ollama API
curl http://localhost:11434/api/tags
```

---

## 🎯 Quick Reference

### Essential Commands

| Command | Purpose |
|---------|---------|
| `ollama serve` | Start Ollama server |
| `streamlit run app.py` | Start application |
| `ollama list` | Show installed models |
| `ollama pull llama2` | Download model |
| `pip install -r requirements.txt` | Install dependencies |
| `deactivate` | Exit virtual environment |

### Default URLs

| Service | URL |
|---------|-----|
| Application | http://localhost:8501 |
| Ollama API | http://localhost:11434 |

---

## 🔗 Additional Resources

- [Main README](README.md) - Complete documentation
- [Backend README](backend/README.md) - Backend API docs
- [Frontend README](frontend/README.md) - UI customization
- [Ollama Documentation](https://github.com/ollama/ollama) - Ollama help
- [Streamlit Documentation](https://docs.streamlit.io) - Streamlit help

---

## ✅ Success!

If you've reached this point and the app is running:

**🎉 Congratulations! You're ready to start summarizing PDFs with AI!**

Try these first PDFs:
1. A short news article (2-3 pages)
2. A research paper abstract
3. A technical document

Experiment with different:
- Models (Llama 2 vs Mistral vs Phi)
- Summary types (Extractive vs Abstractive)
- Lengths (Short vs Medium vs Long)

---

**Questions?** Check the [Troubleshooting](#-troubleshooting) section or open an issue!

**Last Updated:** January 2026  
**Version:** 1.0.0
