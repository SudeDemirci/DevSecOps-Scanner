const API_BASE = "http://127.0.0.1:8000/api";

document.addEventListener("DOMContentLoaded", () => {
    const scanBtn = document.getElementById("scan-btn");
    const imageInput = document.getElementById("image-input");
    
    const loadingState = document.getElementById("loading-state");
    const errorState = document.getElementById("error-state");
    const errorMessage = document.getElementById("error-message");
    const resultsDashboard = document.getElementById("results-dashboard");
    
    // Stats
    const gateStatus = document.getElementById("gate-status");
    const countCritical = document.getElementById("count-critical");
    const countHigh = document.getElementById("count-high");
    const countMedium = document.getElementById("count-medium");
    const mockWarning = document.getElementById("mock-warning");
    
    // Table
    const vulnTableBody = document.getElementById("vuln-table-body");
    const noVulnMsg = document.getElementById("no-vuln-msg");
    const tableResponsive = document.querySelector(".table-responsive");

    scanBtn.addEventListener("click", async () => {
        const image = imageInput.value.trim();
        if (!image) {
            alert("Please enter a Docker image name.");
            return;
        }

        // UI Reset
        resultsDashboard.classList.add("hidden");
        errorState.classList.add("hidden");
        loadingState.classList.remove("hidden");
        scanBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE}/scan?image_name=${encodeURIComponent(image)}`, {
                method: "POST"
            });

            if (!response.ok) {
                throw new Error("API request failed: " + response.statusText);
            }

            const data = await response.json();
            
            // Populate data
            populateDashboard(data);
            
            loadingState.classList.add("hidden");
            resultsDashboard.classList.remove("hidden");

        } catch (err) {
            console.error(err);
            errorMessage.textContent = err.message;
            loadingState.classList.add("hidden");
            errorState.classList.remove("hidden");
        } finally {
            scanBtn.disabled = false;
        }
    });

    function populateDashboard(data) {
        // Status Gate
        if (data.status === "PASS") {
            gateStatus.innerHTML = `<div class="status-pass-badge"><i class="fa-solid fa-check-circle"></i> PASSED</div>`;
            gateStatus.className = "status-indicator status-pass";
        } else {
            gateStatus.innerHTML = `<div class="status-fail-badge"><i class="fa-solid fa-ban"></i> FAILED</div>`;
            gateStatus.className = "status-indicator status-fail";
        }

        // Counts
        countCritical.textContent = data.counts.CRITICAL || 0;
        countHigh.textContent = data.counts.HIGH || 0;
        countMedium.textContent = data.counts.MEDIUM || 0;

        // Mock Warning
        if (data.is_mock) {
            mockWarning.classList.remove("hidden");
        } else {
            mockWarning.classList.add("hidden");
        }

        // Table
        vulnTableBody.innerHTML = "";
        if (!data.vulnerabilities || data.vulnerabilities.length === 0) {
            tableResponsive.classList.add("hidden");
            noVulnMsg.classList.remove("hidden");
        } else {
            tableResponsive.classList.remove("hidden");
            noVulnMsg.classList.add("hidden");

            data.vulnerabilities.forEach(vuln => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td class="cve-id"><a href="https://nvd.nist.gov/vuln/detail/${vuln.id}" target="_blank" style="color: #64b5f6; text-decoration: underline;">${vuln.id}</a></td>
                    <td><span class="badge badge-${vuln.severity.toLowerCase()}">${vuln.severity}</span></td>
                    <td class="pkg-name">${vuln.pkg_name}</td>
                    <td>${vuln.installed_version}</td>
                    <td style="max-width: 400px; word-wrap: break-word; white-space: normal;">${vuln.title || '-'}</td>
                `;
                vulnTableBody.appendChild(tr);
            });
        }
    }
});
