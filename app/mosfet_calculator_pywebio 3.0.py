import math
import pywebio
from pywebio.input import input, FLOAT, checkbox
from pywebio.output import put_html, clear, put_buttons, put_row, put_column, put_error, put_text
from pywebio import start_server
import webview
import socket
import sys
import webbrowser
import threading
import time

# Constants for MOSFET calculations
DEFAULT_PARAMETERS = {
    "max_power": 2700.0,  # Motor power in Watts
    "motor_kv": 190.0,    # Motor KV (RPM/V)
    "max_current": 75.0,  # Phase RMS current in Amps
    "v_max": 60.0,        # Maximum voltage in Volts
    "foc": True,          # Default to FOC control
    "n_parallel": 2,      # Number of parallel MOSFETs
    "k_margin": 1.5,      # Voltage margin factor
    "k_derate": 1.3,      # Current derating factor
    "D": 0.8,             # Duty cycle
    "f_sw": 30000,        # Switching frequency in Hz
    "t_r_f": 100e-9,     # Rise/fall time in seconds
    "Qg": 100e-9,         # Gate charge in Coulombs
    "Vgs": 10,            # Gate-source voltage in Volts
    "Rds_on_assumed": 0.0015,  # Assumed Rds(on) in Ohms
    "Pd_max": 50          # Maximum power dissipation in Watts
}

# CSS Styles
CUSTOM_CSS = """
<style>
    /* Global styles - Dark mode optimized */
    body {
        background: #1a1a1a;
        font-family: 'Microsoft JhengHei', 'Segoe UI', sans-serif;
        margin: 0;
        padding: 16px;
        color: #ffffff;
    }

    /* Main container */
    .pywebio-container {
        max-width: 900px;
        margin: 0 auto;
        background: #2d2d2d;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        padding: 24px;
        border: 1px solid #404040;
    }

    /* Headings */
    h1 {
        color: #ffffff;
        text-align: center;
        margin: 0 0 8px 0;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #ffffff;
        margin: 0 0 12px 0;
        font-size: 20px;
        font-weight: 600;
    }

    h3 {
        color: #ffffff;
        margin: 0 0 12px 0;
        font-size: 16px;
        font-weight: 600;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #b0b0b0;
        font-size: 14px;
        margin: 0 0 24px 0;
        font-weight: 400;
    }

    /* Form group */
    .form-group {
        background: #2d2d2d;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #404040;
    }

    /* Input fields */
    .form-control {
        border-radius: 6px !important;
        border: 1px solid #505050 !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        transition: border-color 0.2s ease !important;
        background: #3a3a3a !important;
        color: #ffffff !important;
    }

    .form-control:focus {
        border-color: #2196F3 !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
        background: #3a3a3a !important;
        outline: none !important;
    }

    /* Labels */
    label {
        font-weight: 500 !important;
        color: #ffffff !important;
        margin-bottom: 6px !important;
        font-size: 14px !important;
        display: block !important;
    }

    /* Help text */
    .form-text {
        color: #b0b0b0 !important;
        font-size: 12px !important;
        margin-top: 4px !important;
    }

    /* Buttons */
    .btn {
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin: 4px !important;
        min-width: 120px;
    }

    .btn-primary {
        background: #2196F3 !important;
        color: #ffffff !important;
    }

    .btn-primary:hover {
        background: #1976D2 !important;
        transform: translateY(-1px);
    }

    .btn-success {
        background: #4CAF50 !important;
        color: #ffffff !important;
    }

    .btn-success:hover {
        background: #388E3C !important;
        transform: translateY(-1px);
    }

    .btn-warning {
        background: #FF9800 !important;
        color: #ffffff !important;
    }

    .btn-warning:hover {
        background: #F57C00 !important;
        transform: translateY(-1px);
    }

    /* Checkbox */
    .checkbox {
        margin: 12px 0 !important;
    }

    .checkbox input[type="checkbox"] {
        transform: scale(1.1);
        margin-right: 8px;
        accent-color: #2196F3;
    }

    .checkbox label {
        font-size: 14px !important;
        color: #ffffff !important;
        font-weight: 400 !important;
    }

    /* Info card */
    .info-card {
        background: #2d2d2d;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        border: 1px solid #404040;
        position: relative;
    }

    .info-card-header {
        background: #2196F3;
        color: #ffffff;
        padding: 12px 16px;
        border-radius: 12px; /* Fully rounded corners */
        font-weight: 600;
        font-size: 14px;
    }

    /* Highlight */
    .highlight {
        background: #2196F3;
        color: #ffffff;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 13px;
    }

    /* Data grid */
    .data-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 12px 0;
    }

    .data-item {
        background: #3a3a3a;
        padding: 12px;
        border-radius: 6px;
        border-left: 3px solid #2196F3;
    }

    .data-label {
        color: #b0b0b0;
        font-size: 12px;
        margin-bottom: 4px;
        font-weight: 400;
    }

    .data-value {
        color: #ffffff;
        font-size: 16px;
        font-weight: 600;
        margin: 0;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #404040;
        margin: 24px 0;
    }

    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #404040;
        border-radius: 50%;
        border-top-color: #2196F3;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 32px;
        padding: 16px;
        color: #808080;
        border-top: 1px solid #404040;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .pywebio-container {
            margin: 8px;
            padding: 16px;
        }

        .data-grid {
            grid-template-columns: 1fr;
            gap: 8px;
        }

        h1 {
            font-size: 24px;
        }

        .btn {
            min-width: 100px;
            padding: 8px 16px !important;
        }
    }

    /* Fix PyWebIO default styles */
    .form-group .form-group {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 16px !important;
    }

    /* Markdown content */
    .markdown-body {
        color: #ffffff !important;
        background: transparent !important;
    }

    .markdown-body p {
        color: #ffffff !important;
        line-height: 1.5;
        margin: 8px 0;
    }

    .markdown-body ul {
        margin: 8px 0;
        padding-left: 20px;
    }

    .markdown-body li {
        color: #ffffff !important;
        margin: 4px 0;
        line-height: 1.4;
    }

    .markdown-body strong {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* White text areas */
    .white-text {
        color: #ffffff !important;
    }

    .data-item-white {
        background: #ffffff;
        padding: 12px;
        border-radius: 6px;
        border-left: 3px solid #2196F3;
        color: #000000 !important;
    }

    .data-item-white .data-label {
        color: #666666 !important;
    }

    .data-item-white .data-value {
        color: #000000 !important;
    }

    .data-item-white p {
        color: #000000 !important;
    }
</style>
"""

def add_custom_styles():
    """Apply custom CSS styles for dark mode and UI consistency."""
    put_html(CUSTOM_CSS)

def create_header():
    """Create the page header with title and subtitle."""
    put_html("""
        <h1>🔧 MOSFET Calculator</h1>
        <div class="subtitle">Professional-grade MOSFET selection tool for VESC FOC</div>
    """)

def validate_inputs(data):
    """Validate user inputs to ensure they are positive and reasonable."""
    for key in ["max_power", "motor_kv", "max_current", "v_max"]:
        if data[key] <= 0:
            raise ValueError(f"{key.replace('_', ' ').title()} must be positive.")
    return data

def calculate_mosfet_params(data, params):
    """Perform MOSFET calculations based on input data and fixed parameters."""
    max_power = data["max_power"]
    motor_kv = data["motor_kv"]
    max_current = data["max_current"]
    v_max = data["v_max"]
    foc = data["foc"][0] if data["foc"] else False

    # Efficiency based on control type
    eta = 0.95 if foc else 0.90

    # Battery-side DC current
    I_phase_rms = max_current
    I_cont = I_phase_rms * math.sqrt(3) / (math.sqrt(2) * eta)
    I_cont_power = max_power / (v_max * eta)

    # Per-MOSFET current
    I_mos_rms = I_phase_rms / params["n_parallel"]
    I_mos_peak = (I_phase_rms * math.sqrt(2)) / params["n_parallel"]
    I_mos_min = I_mos_rms * params["k_derate"]

    # Voltage requirements (considering BEMF)
    max_rpm = motor_kv * v_max
    bemf_voltage = max_rpm / motor_kv * 0.9
    Vds_min = max(v_max, bemf_voltage) * params["k_margin"]

    # Maximum Rds(on)
    Rds_on_max = (params["Pd_max"] / (I_mos_rms**2 * params["D"])) * 1000

    # Power dissipation
    P_cond = I_mos_rms**2 * params["Rds_on_assumed"] * params["D"]
    P_sw = (v_max * I_mos_peak * params["t_r_f"] * params["f_sw"]) / 2 + (params["Qg"] * params["Vgs"] * params["f_sw"])
    P_total = P_cond + P_sw

    # Cooling recommendation
    cooling = "Standard heatsink" if P_total < 30 else "Forced air cooling"

    return {
        "I_cont": I_cont,
        "I_cont_power": I_cont_power,
        "I_phase_rms": I_phase_rms,
        "I_mos_rms": I_mos_rms,
        "I_mos_peak": I_mos_peak,
        "I_mos_min": I_mos_min,
        "max_rpm": max_rpm,
        "bemf_voltage": bemf_voltage,
        "Vds_min": Vds_min,
        "Rds_on_max": Rds_on_max,
        "P_total": P_total,
        "P_cond": P_cond,
        "P_sw": P_sw,
        "cooling": cooling,
        "control_type": "FOC" if foc else "BLDC",
        "eta": eta
    }

def display_results(data, results):
    """Display calculation results in organized cards."""
    # Input parameters card
    put_html('<div class="info-card">')
    put_html('<div class="info-card-header">📋 Input Parameters</div>')
    put_html(f'''
    <div class="data-grid">
        <div class="data-item">
            <div class="data-label">Motor Power</div>
            <div class="data-value">{data["max_power"]} W</div>
        </div>
        <div class="data-item">
            <div class="data-label">KV Value</div>
            <div class="data-value">{data["motor_kv"]} RPM/V</div>
        </div>
        <div class="data-item">
            <div class="data-label">Phase RMS Current</div>
            <div class="data-value">{data["max_current"]} A</div>
        </div>
        <div class="data-item">
            <div class="data-label">Maximum Voltage</div>
            <div class="data-value">{data["v_max"]} V</div>
        </div>
    </div>
    <p style="margin: 8px 0 0 0; color: #b0b0b0; font-size: 13px;">Control Mode: {results["control_type"]}</p>
    ''')
    put_html('</div>')

    # Current analysis card
    put_html('<div class="info-card">')
    put_html('<div class="info-card-header">⚡ Current Analysis</div>')
    put_html(f'''
    <div class="data-grid">
        <div class="data-item">
            <div class="data-label">Battery Current</div>
            <div class="data-value">{round(results["I_cont"], 1)} A</div>
        </div>
        <div class="data-item">
            <div class="data-label">Power-Derived Current</div>
            <div class="data-value">{round(results["I_cont_power"], 1)} A</div>
        </div>
        <div class="data-item">
            <div class="data-label">Phase RMS Current</div>
            <div class="data-value">{round(results["I_phase_rms"], 1)} A</div>
        </div>
        <div class="data-item">
            <div class="data-label">Per-MOSFET RMS Current</div>
            <div class="data-value">{round(results["I_mos_rms"], 1)} A</div>
        </div>
    </div>
    ''')
    put_html('</div>')

    # Additional current calculations card
    put_html('<div class="info-card">')
    put_html('<div class="info-card-header">🔍 Additional Current Calculations</div>')
    put_html(f'''
    <div class="data-grid">
        <div class="data-item">
            <div class="data-label">Per-MOSFET Peak Current</div>
            <div class="data-value">{round(results["I_mos_peak"], 1)} A</div>
        </div>
        <div class="data-item">
            <div class="data-label">Per-MOSFET Minimum Current (Derated)</div>
            <div class="data-value">{round(results["I_mos_min"], 1)} A</div>
        </div>
        <div class="data-item">
            <div class="data-label">System Efficiency</div>
            <div class="data-value">{round(results["eta"] * 100, 1)} %</div>
        </div>
    </div>
    ''')
    put_html('</div>')

    # BEMF analysis card
    put_html('<div class="info-card">')
    put_html('<div class="info-card-header">🔄 BEMF Analysis</div>')
    put_html(f'''
    <div class="data-grid">
        <div class="data-item">
            <div class="data-label">Maximum RPM</div>
            <div class="data-value">{round(results["max_rpm"], 0)} RPM</div>
        </div>
        <div class="data-item">
            <div class="data-label">Back EMF</div>
            <div class="data-value">{round(results["bemf_voltage"], 1)} V</div>
        </div>
    </div>
    ''')
    put_html('</div>')

    # MOSFET specifications card
    put_html('<div class="info-card">')
    put_html('<div class="info-card-header">🔧 MOSFET Specifications</div>')
    put_html(f'''
    <div style="margin: 12px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px 12px; background: #3a3a3a; border-radius: 6px;" class="white-text">
            <span style="color: #ffffff;">Vds Rating</span>
            <span class="highlight">> {round(results["Vds_min"], 1)} V</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px 12px; background: #3a3a3a; border-radius: 6px;" class="white-text">
            <span style="color: #ffffff;">Id Current</span>
            <span class="highlight">> {round(results["I_mos_rms"] * DEFAULT_PARAMETERS["k_derate"], 1)} A</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px 12px; background: #3a3a3a; border-radius: 6px;" class="white-text">
            <span style="color: #ffffff;">Rds(on) Resistance</span>
            <span class="highlight">< {round(results["Rds_on_max"], 2)} mΩ</span>
        </div>
    </div>
    ''')
    put_html('</div>')

    # Power dissipation analysis card
    put_html('<div class="info-card">')
    put_html('<div class="info-card-header">🔥 Power Dissipation Analysis</div>')
    put_html(f'''
    <div class="data-grid">
        <div class="data-item">
            <div class="data-label">Single MOSFET Power</div>
            <div class="data-value">{round(results["P_total"], 2)} W</div>
        </div>
        <div class="data-item">
            <div class="data-label">Total Heat (12 MOSFETs)</div>
            <div class="data-value">{round(results["P_total"] * 12, 2)} W</div>
        </div>
        <div class="data-item">
            <div class="data-label">Conduction Loss</div>
            <div class="data-value">{round(results["P_cond"], 2)} W</div>
        </div>
        <div class="data-item">
            <div class="data-label">Switching Loss</div>
            <div class="data-value">{round(results["P_sw"], 2)} W</div>
        </div>
    </div>
    <p style="margin: 12px 0 0 0; color: #b0b0b0; font-size: 13px;">Cooling Recommendation: {results["cooling"]}</p>
    ''')
    put_html('</div>')

def display_engineering_data(results):
    """Display engineering data with 20% margin."""
    Vds_eng = results["Vds_min"] * 1.2
    Id_eng = results["I_mos_rms"] * DEFAULT_PARAMETERS["k_derate"] * 1.2
    Rds_on_eng = results["Rds_on_max"] * 0.8

    put_html('<div class="info-card engineering-data" style="border: 1px solid #FF9800;">')
    put_html('<div class="info-card-header" style="background: #FF9800;">🛠️ Engineering Data (20% Margin)</div>')
    put_html(f'''
    <div style="margin: 16px 0;">
        <h4 style="color: #ffffff; margin: 0 0 12px 0; font-size: 15px;">Conservative Design Specifications:</h4>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px 12px; background: #3a3a3a; border-radius: 6px;">
            <span style="color: #b0b0b0;">Vds Rating</span>
            <span class="highlight">> {round(Vds_eng, 1)} V</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px 12px; background: #3a3a3a; border-radius: 6px;">
            <span style="color: #b0b0b0;">Id Current</span>
            <span class="highlight">> {round(Id_eng, 1)} A</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0; padding: 8px 12px; background: #3a3a3a; border-radius: 6px;">
            <span style="color: #b0b0b0;">Rds(on) Resistance</span>
            <span class="highlight">< {round(Rds_on_eng, 2)} mΩ</span>
        </div>
    </div>
    <div style="margin: 16px 0;">
        <h4 style="color: #ffffff; margin: 0 0 12px 0; font-size: 15px;">Cooling Design Recommendations:</h4>
        <div style="background: #3a3a3a; padding: 12px; border-radius: 6px; margin: 8px 0;">
            <p style="margin: 4px 0; color: #ffffff; font-size: 13px;">• Select heatsink with thermal resistance < 0.5°C/W</p>
            <p style="margin: 4px 0; color: #ffffff; font-size: 13px;">• Recommended size: ~20cm × 10cm × 5cm</p>
            <p style="margin: 4px 0; color: #ffffff; font-size: 13px;">• Consider thermal adhesive or pads</p>
            <p style="margin: 4px 0; color: #ffffff; font-size: 13px;">• Ensure adequate airflow</p>
        </div>
    </div>
    <div style="margin: 16px 0;">
        <h4 style="color: #ffffff; margin: 0 0 12px 0; font-size: 15px;">Notes:</h4>
        <div class="data-item-white">
            <p style="margin: 4px 0; color: #2E7D32; font-size: 13px;">✅ Data includes 20% safety margin</p>
            <p style="margin: 4px 0; color: #2E7D32; font-size: 13px;">✅ Suitable for VESC {results["control_type"]} mode</p>
            <p style="margin: 4px 0; color: #E65100; font-size: 13px;">⚠️ Perform thermal testing before deployment</p>
        </div>
    </div>
    ''')
    put_html('</div>')

def find_free_port(start_port=8080):
    """Find an available port starting from the given port."""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                port += 1

def mosfet_calculator():
    """Main function to run the MOSFET calculator application."""
    engineering_data_visible = False

    def toggle_engineering_data():
        nonlocal engineering_data_visible
        if engineering_data_visible:
            put_html('<script>document.querySelectorAll(".engineering-data").forEach(el => el.remove());</script>')
            engineering_data_visible = False
        else:
            display_engineering_data(results)
            engineering_data_visible = True

    def restart_calculator():
        mosfet_calculator()

    try:
        clear()
        add_custom_styles()
        create_header()

        # Input form (no outer form-group to avoid overlap with header)
        data = pywebio.input.input_group("", [
            input("Motor Power (W)", name="max_power", type=FLOAT, value=DEFAULT_PARAMETERS["max_power"],
                  help_text="Maximum motor power output"),
            input("KV (RPM/V)", name="motor_kv", type=FLOAT, value=DEFAULT_PARAMETERS["motor_kv"],
                  help_text="Motor KV value, RPM per Volt"),
            input("Phase RMS Current (A)", name="max_current", type=FLOAT, value=DEFAULT_PARAMETERS["max_current"],
                  help_text="Effective RMS current per motor phase"),
            input("Maximum Voltage (V)", name="v_max", type=FLOAT, value=DEFAULT_PARAMETERS["v_max"],
                  help_text="Maximum system operating voltage"),
            checkbox("Control Options", name="foc", options=[
                {'label': '🎯 Use FOC Control', 'value': True, 'selected': DEFAULT_PARAMETERS["foc"]}
            ], help_text="FOC control offers higher efficiency and lower noise")
        ])

        # Validate inputs
        try:
            validate_inputs(data)
        except ValueError as e:
            put_error(str(e))
            return

        # Show loading animation
        put_html("""
        <div style="text-align: center; margin: 20px 0;">
            <div class="loading"></div>
            <p style="color: #b0b0b0; margin-top: 10px; font-size: 14px;">Calculating...</p>
        </div>
        """)

        # Perform calculations
        results = calculate_mosfet_params(data, DEFAULT_PARAMETERS)

        # Clear loading animation and display results
        clear()
        add_custom_styles()
        create_header()
        display_results(data, results)

        # Operation buttons
        put_html('<hr>')
        put_row([
            put_column([
                put_buttons([
                    {'label': '🛠️ Engineering Data', 'value': 'eng', 'color': 'success'}
                ], onclick=lambda _: toggle_engineering_data())
            ]),
            put_column([
                put_buttons([
                    {'label': '🔄 Recalculate', 'value': 'restart', 'color': 'primary'}
                ], onclick=lambda _: restart_calculator())
            ]),
            put_column([
                put_buttons([
                    {'label': '🗑️ Clear', 'value': 'clear', 'color': 'warning'}
                ], onclick=lambda _: clear())
            ])
        ])

        # Footer
        put_html("""
        <div class="footer">
            <p style="margin: 0; font-size: 14px; font-weight: 500;">🚀 MOSFET Calculator v2.0</p>
            <p style="margin: 4px 0 0 0; font-size: 12px;">Professional motor controller design tool | Powered by PyWebIO</p>
        </div>
        """)

    except Exception as e:
        put_error(f"An error occurred: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)

def run_desktop_app():
    """Run the MOSFET calculator as a desktop application using PyWebIO and PyWebView."""
    try:
        port = find_free_port(8080)
        print(f"Starting PyWebIO server on http://localhost:{port}")

        # Start PyWebIO server in a separate thread
        server_thread = threading.Thread(target=start_server, args=(mosfet_calculator,), kwargs={'port': port, 'debug': True})
        server_thread.daemon = True
        server_thread.start()

        # Wait a moment for the server to start
        time.sleep(2)

        try:
            webview.create_window("🔧 MOSFET Calculator (VESC FOC)", f"http://localhost:{port}",
                                 width=900, height=800, resizable=True, min_size=(700, 600))
            webview.start()
        except Exception as e:
            print(f"PyWebView failed: {str(e)}. Falling back to browser mode.", file=sys.stderr)
            webbrowser.open(f"http://localhost:{port}")
    except Exception as e:
        print(f"Failed to start application: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_desktop_app()