import subprocess
import sys
from pathlib import Path


def main():
    """Launch the Streamlit RAG application"""
    
    # Get the path to the rag_app.py file
    app_path = Path(__file__).parent / "src" / "rag_app.py"
    
    if not app_path.exists():
        print(f"❌ Error: Could not find {app_path}")
        sys.exit(1)
    
    print("🚀 Starting RAG Question Answering System...")
    print(f"📂 Loading app from: {app_path}")
    print("🌐 Opening browser at http://localhost:8501")
    print("\n⏹️  Press Ctrl+C to stop the server\n")
    
    # Run streamlit with the app file
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    