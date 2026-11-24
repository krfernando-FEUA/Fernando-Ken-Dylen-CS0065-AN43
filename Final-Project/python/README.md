# Python source

[Download the Python source ZIP](LoopGuard-Python-Source.zip), extract it, and open
the `loopguard-python` directory. It includes the Streamlit application, rule
engine, scenarios, assets, requirements, tests, and KNIME integration.

Use Python 3.12. From the extracted project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open http://127.0.0.1:8501/. The extracted README contains the complete setup,
command-line audit, and test instructions.
