#!/usr/bin/env python3
"""
Launch script for the Interactive Decision Space Viewer
Starts a local web server and opens the interactive application
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path
import subprocess

def main():
    """Main launch function"""
    port = 8080

    # Get the absolute path to the decision space viewer
    viewer_path = Path(__file__).parent / "decision_space_viewer.html"

    if not viewer_path.exists():
        print(f"❌ Error: Decision Space Viewer not found at {viewer_path}")
        print("Make sure decision_space_viewer.html exists in the current directory.")
        return 1

    print("🚀 Starting Interactive Decision Space Viewer...")
    print(f"📁 Serving from: {Path.cwd()}")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"📊 Viewer URL: http://localhost:{port}/decision_space_viewer.html")
    print("\n" + "="*60)

    # Try to open in default browser
    try:
        webbrowser.open(f"http://localhost:{port}/decision_space_viewer.html")
        print("✅ Browser opened automatically")
    except Exception as e:
        print(f"ℹ️  Please open http://localhost:{port}/decision_space_viewer.html in your browser")
        print(f"   (Browser auto-open failed: {e})")

    print("\n" + "="*60)
    print("🎯 Decision Space Viewer Features:")
    print("• Add projects and create constraints interactively")
    print("• View real-time decision space visualization")
    print("• Analyze constraint impacts on portfolio options")
    print("• Test constraint feasibility and sensitivity")
    print("• Export projects and constraints for further analysis")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60)

    # Start HTTP server
    try:
        with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return 1

    return 0

def launch_with_alternate_method():
    """Alternative launcher using Python's built-in server differently"""
    port = 8080

    try:
        print("🌍 Starting server with built-in Python HTTP server...")
        print(f"📊 Open http://localhost:{port}/decision_space_viewer.html in your browser")

        # Use subprocess to run the server
        cmd = [sys.executable, "-m", "http.server", str(port)]
        subprocess.run(cmd)

    except FileNotFoundError:
        print("❌ Python executable not found. Please run with: python -m http.server")
        return 1
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
