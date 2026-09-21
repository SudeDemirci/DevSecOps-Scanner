import subprocess
import json
import logging
import random

logger = logging.getLogger(__name__)

def run_trivy_scan(image_name: str):
    """
    Runs Trivy via Docker to scan an image.
    Returns a dictionary with parsed results.
    """
    try:
        # On Windows without socket mapping, we can scan public images.
        command = [
            "docker", "run", "--rm", 
            "-v", "trivy-cache:/root/.cache/",
            "-v", "/var/run/docker.sock:/var/run/docker.sock",
            "aquasec/trivy", "image", "--timeout", "30m", "-f", "json", "--quiet", image_name
        ]

        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=1800,
            encoding="utf-8"
        )
        
        data = json.loads(result.stdout)
        return _parse_trivy_json(data)
        
    except FileNotFoundError:
        # Docker is not installed or not in PATH
        return _get_mock_data(image_name)
    except subprocess.CalledProcessError as e:
        # Docker command failed (image not found, docker daemon not running, etc)
        logger.error(f"Trivy scan failed: {e.stderr}")
        return _get_mock_data(image_name, error=e.stderr)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return _get_mock_data(image_name, error=str(e))

def _parse_trivy_json(data):
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    vulnerabilities = []

    if "Results" in data:
        for result in data["Results"]:
            if "Vulnerabilities" in result:
                for vuln in result["Vulnerabilities"]:
                    severity = vuln.get("Severity", "UNKNOWN")
                    if severity in counts:
                        counts[severity] += 1
                    
                    vulnerabilities.append({
                        "id": vuln.get("VulnerabilityID"),
                        "pkg_name": vuln.get("PkgName"),
                        "installed_version": vuln.get("InstalledVersion"),
                        "severity": severity,
                        "title": vuln.get("Title", "")
                    })
    
    status = "FAIL" if counts["CRITICAL"] > 0 or counts["HIGH"] > 0 else "PASS"
    
    return {
        "status": status,
        "counts": counts,
        "vulnerabilities": vulnerabilities
    }

def _get_mock_data(image_name: str, error: str = None):
    """Fallback mock data for demo purposes if Docker is not available"""
    crit = random.randint(1, 5) if random.choice([True, False]) else 0
    high = random.randint(1, 10)
    
    # We always return some data to keep the UI functional for the demo
    mock_vulns = []
    if crit > 0:
        mock_vulns.append({
            "id": "CVE-MOCK-2026-001",
            "pkg_name": "openssl",
            "installed_version": "1.1.1t",
            "severity": "CRITICAL",
            "title": "Mock Critical Vulnerability (Docker/Trivy not running)"
        })
    if high > 0:
         mock_vulns.append({
            "id": "CVE-MOCK-2026-002",
            "pkg_name": "curl",
            "installed_version": "7.81.0",
            "severity": "HIGH",
            "title": "Mock High Vulnerability for demonstration"
        })

    return {
        "status": "FAIL" if crit > 0 or high > 0 else "PASS",
        "counts": {
            "CRITICAL": crit,
            "HIGH": high,
            "MEDIUM": random.randint(5, 20),
            "LOW": random.randint(10, 30)
        },
        "vulnerabilities": mock_vulns,
        "is_mock": True,
        "mock_reason": error
    }
