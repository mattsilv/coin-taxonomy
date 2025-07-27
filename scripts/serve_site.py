#!/usr/bin/env python3
"""
Local development server for GitHub Pages site
"""
import http.server
import socketserver
import os
import sys
import subprocess
import signal
from pathlib import Path

def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socketserver.TCPServer(("", port), None) as test_server:
                return port
        except OSError:
            continue
    return None

def kill_processes_on_port(port):
    """Kill any processes using the specified port"""
    try:
        # Find processes using the port
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"🔄 Killed process {pid} on port {port}")
                except (ProcessLookupError, ValueError):
                    pass
            return True
        return False
    except FileNotFoundError:
        # lsof not available, skip cleanup
        return False

def serve_site(port=8000, auto_port=True, kill_existing=False):
    """Serve the GitHub Pages site locally"""
    # Change to docs directory
    docs_dir = Path(__file__).parent.parent / "docs"
    
    if not docs_dir.exists():
        print("❌ docs/ directory not found")
        sys.exit(1)
        
    os.chdir(docs_dir)
    
    # Handle port conflicts
    if kill_existing:
        killed = kill_processes_on_port(port)
        if killed:
            print(f"🔄 Cleaned up existing processes on port {port}")
    
    if auto_port:
        available_port = find_available_port(port)
        if available_port is None:
            print(f"❌ No available ports found in range {port}-{port+9}")
            sys.exit(1)
        port = available_port
    
    # Start server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🌐 Serving GitHub Pages site at http://localhost:{port}")
            print(f"📁 Serving from: {docs_dir}")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} still in use after cleanup")
            if not auto_port:
                print("💡 Try using --auto-port or --kill-existing flags")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Serve GitHub Pages site locally")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000)")
    parser.add_argument("--no-auto-port", action="store_true", help="Don't automatically find available port")
    parser.add_argument("--kill-existing", action="store_true", help="Kill existing processes on port")
    args = parser.parse_args()
    
    serve_site(args.port, auto_port=not args.no_auto_port, kill_existing=args.kill_existing)