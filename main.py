# main.py
import sys
import subprocess

def main():
    print("Starting TireSim Streamlit Dashboard...")
    
    # Programmatically runs 'streamlit run src/ui/app.py' using the active Python interpreter
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ui/app.py"], check=True)
    except KeyboardInterrupt:
        print("\nDashboard closed.")
    except Exception as e:
        print(f"Error launching dashboard: {e}")

if __name__ == "__main__":
    main()