# from auditor_module import audit_and_fix_code

# if __name__ == "__main__":
#     audit_and_fix_code("vulnerable_app.py")
import os
import subprocess
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini Client
client = genai.Client()

def run_bandit_scan(filepath):
    print(f"[*] Running Bandit security scan on {filepath}...")
    result = subprocess.run(["bandit", "-r", filepath, "-f", "json"], capture_output=True, text=True)
    return result.stdout

def audit_and_fix_code(file_path):
    with open(file_path, 'r') as f:
        code_content = f.read()

    bandit_report = run_bandit_scan(file_path)
    print("[*] Sending code and security report to Gemini Agent for fixing...")

    prompt = f"""
    You are an expert Autonomous Cybersecurity Code Auditor and Senior Developer.
    Analyze the following Python code and the Bandit security report.
    Rewrite the code to fix all vulnerabilities (such as SQL injections, hardcoded secrets, command injections) 
    while preserving its original functionality.
    
    CRITICAL INSTRUCTION: Only modify the specific lines of code that are flagged as vulnerabilities 
    by the Bandit report; do not change any other parts of the code.

    Return ONLY the fully refactored, secure Python code inside a standard python code block (```python ... ```). 
    Do not add extra conversational filler.

    --- ORIGINAL CODE ---
    {code_content}

    --- BANDIT SECURITY REPORT ---
    {bandit_report}
    """

    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )

    ai_output = response.text
    print("[*] Gemini has generated the secured code.")

    if "```python" in ai_output:
        fixed_code = ai_output.split("```python")[1].split("```")[0].strip()
    elif "```" in ai_output:
        fixed_code = ai_output.split("```")[1].split("```")[0].strip()
    else:
        fixed_code = ai_output.strip()

    output_filename = "fixed_app.py"
    with open(output_filename, 'w') as f:
        f.write(fixed_code)

    print(f"[+] Success! Secured code saved to {output_filename}")

if __name__ == "__main__":
    audit_and_fix_code("vulnerable_app.py")