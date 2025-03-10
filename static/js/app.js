
document.addEventListener('DOMContentLoaded', function() {

    const diodeCircuitForm = document.getElementById('diodeCircuitForm');
    const systemSolverForm = document.getElementById('systemSolverForm');

    // Setup form submission handlers
    if (diodeCircuitForm) {
        diodeCircuitForm.addEventListener('submit', handleDiodeCircuitSubmit);
    }

    if (systemSolverForm) {
        systemSolverForm.addEventListener('submit', handleSystemSolverSubmit);
    }
});

// Handler for diode circuit form
async function handleDiodeCircuitSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const resultsContainer = document.getElementById('diodeCircuitResults');
    const formData = new FormData(form);

    try {
        // Set checkbox value explicitly (if not checked, it won't be included)
        if (!formData.has('historial')) {
            formData.append('historial', 'false');
        }

        // Submit form data to API
        const response = await fetch('/api/diode-circuit', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en el servidor');
        }

        const data = await response.json();
console.log("Response data:", data);
console.log("History data:", data.historial);
        // Display results
        document.getElementById('result-i1').textContent = data.i1.toExponential(6);
        document.getElementById('result-i2').textContent = data.i2.toExponential(6);
        document.getElementById('result-vd').textContent = data.vd.toFixed(6);
        document.getElementById('result-iterations').textContent = data.iterations;
        document.getElementById('result-converged').textContent = data.converged ? 'Sí' : 'No';

        // Show results container
        resultsContainer.classList.remove('d-none');

        // Display convergence chart if history data is available
        if (data.historial && data.historial.length > 0) {
            createConvergenceChart(data.historial);
        } else {
            // Si no hay historial, asegúrate de que la tabla esté oculta
            document.getElementById('iterationTableContainer').classList.add('d-none');
        }

    } catch (error) {
        alert('Error: ' + error.message);
        console.error('Error:', error);
    }
}

// Handler for system solver form
async function handleSystemSolverSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const resultsContainer = document.getElementById('systemSolverResults');
    const formData = new FormData(form);

    try {
        // Submit form data to API
        const response = await fetch('/api/system-solver', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en el servidor');
        }

        const data = await response.json();

        // Display results
        const solucionContainer = document.getElementById('result-solucion');
        solucionContainer.innerHTML = '';

        for (const [variable, valor] of Object.entries(data.solucion)) {
            const p = document.createElement('p');
            p.innerHTML = `<strong>${variable}:</strong> ${valor.toFixed(6)}`;
            solucionContainer.appendChild(p);
        }

        document.getElementById('result-system-iterations').textContent = data.iteraciones;
        document.getElementById('result-system-converged').textContent = data.convergencia ? 'Sí' : 'No';

        // Show results container
        resultsContainer.classList.remove('d-none');

        // Display convergence chart if history data is available
        if (data.historia && data.historia.length > 0) {
            createSystemConvergenceChart(data.historia, Object.keys(data.solucion));
        }

    } catch (error) {
        alert('Error: ' + error.message);
        console.error('Error:', error);
    }
}

// Function to create the convergence chart for diode circuit
function createConvergenceChart(historyData) {
    const ctx = document.getElementById('convergenceChart');

    // Prepare data for Chart.js
    const labels = historyData.map(item => `Iter ${item.iteracion}`);
    const i1Data = historyData.map(item => item.i1);
    const i2Data = historyData.map(item => item.i2);
    const vdData = historyData.map(item => item.vd);

    // Only include distance for non-zero iterations
    const distanceData = historyData
        .filter(item => item.iteracion > 0)
        .map(item => item.distancia);

    // Create chart
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'I1 (A)',
                    data: i1Data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    tension: 0.1
                },
                {
                    label: 'I2 (A)',
                    data: i2Data,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    tension: 0.1
                },
                {
                    label: 'Vd (V)',
                    data: vdData,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Create distance chart if we have distance data
    if (distanceData.length > 0) {
        // Create a second chart for distance
        const distanceCanvas = document.createElement('canvas');
        distanceCanvas.id = 'distanceChart';
        document.getElementById('convergenceChartContainer').appendChild(distanceCanvas);

        new Chart(distanceCanvas, {
            type: 'line',
            data: {
                labels: labels.slice(1), // Skip first label since no distance for iteration 0
                datasets: [{
                    label: 'Distance',
                    data: distanceData,
                    borderColor: 'rgba(153, 102, 255, 1)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        type: 'logarithmic',
                        title: {
                            display: true,
                            text: 'Distance (log scale)'
                        }
                    }
                }
            }
        });
    }

    // Display iteration history in table
    if (historyData && historyData.length > 0) {
        // Populate the table
        console.log("Table should be displayed, history data:", historyData);
        const tableBody = document.getElementById('iterationTableBody');
        tableBody.innerHTML = ''; // Clear any existing rows

        historyData.forEach(item => {
            const row = document.createElement('tr');

            // Create cells for each data point
            const iterCell = document.createElement('td');
            iterCell.textContent = item.iteracion;

            const i1Cell = document.createElement('td');
            i1Cell.textContent = item.i1.toExponential(6);

            const i2Cell = document.createElement('td');
            i2Cell.textContent = item.i2.toExponential(6);

            const vdCell = document.createElement('td');
            vdCell.textContent = item.vd.toFixed(6);

            // Distance might not be available for iteration 0
            const distCell = document.createElement('td');
            if ('distancia' in item) {
                distCell.textContent = item.distancia.toExponential(6);
            } else {
                distCell.textContent = '—';
            }

            // Add all cells to the row
            row.appendChild(iterCell);
            row.appendChild(i1Cell);
            row.appendChild(i2Cell);
            row.appendChild(vdCell);
            row.appendChild(distCell);

            // Add the row to the table
            tableBody.appendChild(row);
        });

        // Show the table container
        document.getElementById('iterationTableContainer').classList.remove('d-none');
    } else {
        // Hide the table container if no history data
        document.getElementById('iterationTableContainer').classList.add('d-none');
    }
}

// Function to create the convergence chart for general system solver
function createSystemConvergenceChart(historyData, variables) {
    const ctx = document.getElementById('systemConvergenceChart');

    // Prepare data for Chart.js
    const labels = historyData.map(item => `Iter ${item.iteracion}`);

    // Create datasets for each variable
    const datasets = variables.map((variable, index) => {
        // Choose a color based on index
        const colors = [
            'rgba(75, 192, 192, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(153, 102, 255, 1)'
        ];

        const color = colors[index % colors.length];

        return {
            label: variable,
            data: historyData.map(item => item[variable]),
            borderColor: color,
            tension: 0.1
        };
    });

    // Create chart
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Create distance chart if we have distance data
    const distanceData = historyData
        .filter(item => 'distancia' in item)
        .map(item => item.distancia);

    if (distanceData.length > 0) {
        // Create a second chart for distance
        const distanceCanvas = document.createElement('canvas');
        distanceCanvas.id = 'systemDistanceChart';
        document.getElementById('systemConvergenceChartContainer').appendChild(distanceCanvas);

        new Chart(distanceCanvas, {
            type: 'line',
            data: {
                labels: labels.slice(1), // Skip first label since no distance for iteration 0
                datasets: [{
                    label: 'Distance',
                    data: distanceData,
                    borderColor: 'rgba(153, 102, 255, 1)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        type: 'logarithmic',
                        title: {
                            display: true,
                            text: 'Distance (log scale)'
                        }
                    }
                }
            }
        });
    }
}