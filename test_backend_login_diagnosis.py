#!/usr/bin/env python3
"""
Diagnóstico de login y endpoints críticos del backend en Render
"""

import requests
import time
from datetime import datetime

BACKEND_URL = "https://zurich-claims-api.onrender.com"
LOGIN_URL = f"{BACKEND_URL}/api/analyst/auth/login"
STATS_URL = f"{BACKEND_URL}/api/analyst/dashboard/stats"
CLAIMS_URL = f"{BACKEND_URL}/api/analyst/claims"

LOGIN_DATA = {
    "email": "analyst@zurich-demo.com",
    "password": "demo123"
}

MAX_RETRIES = 5
DELAY = 3

def print_response(resp):
    print(f"Status: {resp.status_code}")
    try:
        print("JSON:", resp.json())
    except Exception:
        print("Text:", resp.text)

def test_login():
    print("\n=== TEST LOGIN ===")
    for i in range(MAX_RETRIES):
        print(f"\nIntento {i+1}/{MAX_RETRIES} - {datetime.now()}")
        try:
            resp = requests.post(LOGIN_URL, data=LOGIN_DATA, timeout=15)
            print_response(resp)
            if resp.status_code == 200:
                print("✅ Login exitoso")
                return True
            else:
                print("❌ Login fallido")
        except Exception as e:
            print(f"❌ Excepción en login: {e}")
        time.sleep(DELAY)
    print("❌ Todos los intentos de login fallaron")
    return False

def test_stats():
    print("\n=== TEST DASHBOARD STATS ===")
    try:
        resp = requests.get(STATS_URL, timeout=15)
        print_response(resp)
    except Exception as e:
        print(f"❌ Excepción en stats: {e}")

def test_claims():
    print("\n=== TEST CLAIMS ENDPOINT ===")
    try:
        resp = requests.get(CLAIMS_URL, timeout=15)
        print_response(resp)
    except Exception as e:
        print(f"❌ Excepción en claims: {e}")

def main():
    print(f"\n🚀 Diagnóstico backend Render - {datetime.now()}\n")
    test_stats()
    test_claims()
    test_login()
    print("\n💡 Revisa los mensajes de error y status para identificar el problema exacto.")

if __name__ == "__main__":
    main() 