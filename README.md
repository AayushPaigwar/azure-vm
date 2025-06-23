# FastAPI VM Information Dashboard

This is a simple FastAPI application that displays information about the VM it's running on and exposes system information through a web interface and API.

## Installation

!! This commands are for Azure VM

1. Clone this repository or navigate to the project directory:

```bash
cd /home/azure-admin/fastapi_vm_demo
```

2. Make the start service script executable:

[change modify file permission (chmod) & (+x) executable]

```bash
chmod +x start_service.sh
```

## Running the Application

The easiest way to run the application is to use the provided script:

```bash
./start_service.sh
```

This script will:
- Create and activate a virtual environment if it doesn't exist
- Install all required dependencies
- Verify that FastAPI is properly installed
- Check for and create any missing directories
- Find an available port if the default port (8000) is already in use
- Start the application and display the URL to access it

## Accessing the Application

After starting the application, you can access it at:
- `http://YOUR_VM_IP:8000/` (or another port if 8000 is in use)

The IP address will be displayed in the console when you start the application.

## Exposing Your VM to the Internet

To expose your VM to the internet, you need to ensure that:
- The VM's public IP address is accessible
1. Inbound rules in your cloud provider's security group allow traffic on the port you are using (default is 8000).
2. Your VM's firewall allows incoming connections on that port.

## API Endpoints

- `/` - HTML dashboard showing VM information
- `/api/info` - JSON endpoint with all VM information
- `/health` - Health check endpoint
- `/docs` - Interactive API documentation

## Notes on Security

1. Be cautious when exposing VM information publicly
2. Consider adding authentication for sensitive endpoints
3. Limit the information exposed in production environments
4. Always keep your system and packages updated


## Vercel Deploy Check from VM 🚀 