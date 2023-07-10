import ssl

from cryptography.hazmat._oid import NameOID
from flask import Flask, render_template, request
import socket
import requests
from bs4 import BeautifulSoup
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    results = analyze_website(url)
    return render_template('scan_results.html', url=url, results=results)

def analyze_website(url):
    # Analisi dei certificati
    try:
        context = ssl.create_default_context()
        with socket.create_connection((url, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssl_sock:
                der_cert = ssl_sock.getpeercert(True)
                cert = x509.load_der_x509_certificate(der_cert, default_backend())
                subject = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
                issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
                cert_pem = cert.public_bytes(Encoding.PEM).decode('utf-8')
                cert_info = f"Subject: {subject}\nIssuer: {issuer}\n{cert_pem}"
    except Exception as e:
        cert_info = "Impossibile recuperare il certificato: " + str(e)

    # Analisi dei cookie
    try:
        response = requests.get("https://" + url)
        cookies = response.cookies.items()
    except Exception as e:
        cookies = []

    # Analisi delle porte attive
    common_ports = [80, 443, 21, 22, 25, 110, 143]  # Esempio di porte comuni
    open_ports = []
    try:
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((url, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
    except Exception as e:
        open_ports = "Errore durante l'analisi delle porte: " + str(e)

    # Analisi dei servizi
    service_names = {
        80: "HTTP",
        443: "HTTPS",
        21: "FTP",
        22: "SSH",
        25: "SMTP",
        110: "POP3",
        143: "IMAP"
    }
    service_info = []
    try:
        for port in open_ports:
            if port in service_names:
                service_info.append((port, service_names[port]))
    except Exception as e:
        service_info = "Errore durante l'analisi dei servizi: " + str(e)

    # Analisi degli script
    script_info = []
    try:
        response = requests.get("http://" + url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tags = soup.find_all('script')
            if script_tags:
                for script in script_tags:
                    script_src = script.get('src')
                    if script_src:
                        script_safe = check_script_safety(script_src)
                        script_info.append((script_src, script_safe))
                    else:
                        script_info.append(("Script incorporato", ""))
    except Exception as e:
        script_info = "Errore durante l'analisi degli script: " + str(e)

    return {
        'cert_info': cert_info,
        'cookies': cookies,
        'open_ports': open_ports,
        'service_info': service_info,
        'script_info': script_info
    }

def check_script_safety(script_url):
    try:
        response = requests.get(script_url)
        if response.status_code == 200:
            return "Sicuro"
        else:
            return "Non sicuro"
    except Exception as e:
        return "Errore: " + str(e)


if __name__ == '__main__':
    app.run()


