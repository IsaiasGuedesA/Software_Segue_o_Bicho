import subprocess

def execute_scripts():
    script1_process = subprocess.Popen(['python', r'Serve_Flask\\main.py'])
    script2_process = subprocess.Popen(['python', r'Serve_Mqtt\\main.py'])

    
if __name__ == "__main__":
    execute_scripts()