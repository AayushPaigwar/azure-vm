from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import socket
import platform
import psutil
import os
from datetime import datetime
import sys

# Print current working directory to help with debugging
print(f"Current working directory: {os.getcwd()}")

# Check if the necessary directories exist
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")

if not os.path.exists(templates_dir):
    print(f"ERROR: Templates directory not found at {templates_dir}")
    print("Make sure you are running this command from the project root directory.")
    print("Try: cd /home/azure-admin/fastapi_vm_demo && uvicorn main:app --host 0.0.0.0 --port 8000")
    sys.exit(1)

if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"Created missing static directory at {static_dir}")

app = FastAPI(title="VM Info API", description="A simple API to expose VM information")

# Set up templates
templates = Jinja2Templates(directory=templates_dir)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

def get_host_info():
    """Get basic host information"""
    return {
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_system_info():
    """Get system resource information"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render HTML dashboard"""
    host_info = get_host_info()
    system_info = get_system_info()
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "host_info": host_info,
            "system_info": system_info
        }
    )

@app.get("/api/info")
async def get_info():
    """Return JSON with server information"""
    return {
        "host": get_host_info(),
        "system": get_system_info()
    }

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # This section is for development only
    import uvicorn
    # Run the server with host='0.0.0.0' to expose it on all network interfaces
    print("Starting server on http://0.0.0.0:8000")
    print("To access this server from your browser, use your VM's IP address")
    print("For example: http://your_vm_ip:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
else:
    # When imported by uvicorn, print helpful information
    print(f"FastAPI app loaded from {__file__}")
    print(f"Templates directory: {templates_dir}")
    print(f"Static directory: {static_dir}")
