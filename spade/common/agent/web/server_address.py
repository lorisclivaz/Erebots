import os

WEB_SERVER_PUBLIC_IP = os.environ.get("WEB_SERVER_PUBLIC_IP", "localhost")
"""The public IP of DoctorAgent web server"""

WEB_SERVER_PUBLIC_PORT = os.environ.get("WEB_SERVER_PUBLIC_PORT", 10000)
"""The public port at which the DoctorAgent page is served"""

WEB_SERVER_INTERNAL_IP = os.environ.get("WEB_SERVER_INTERNAL_IP", WEB_SERVER_PUBLIC_IP)
"""The internal IP of DoctorAgent web server"""

WEB_SERVER_INTERNAL_PORT = os.environ.get("WEB_SERVER_INTERNAL_PORT", WEB_SERVER_PUBLIC_PORT)
"""The internal port at which the DoctorAgent page is served"""
