import math
import pywebio
from pywebio.input import input, FLOAT, checkbox, radio
from pywebio.output import put_text, put_markdown, clear, put_html, put_buttons, put_row, put_column
from pywebio import start_server
import webview

def add_custom_styles():
    """添加自定義 CSS 樣式"""
    custom_css = """
    <style>
    /* 全局樣式 */
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Microsoft JhengHei', 'Arial', sans-serif;
        margin: 0;
        padding: 20px;
    }
    
    /* 主容器樣式 */
    .pywebio-container {
        max-width: 800px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        padding: 30px;
        backdrop-filter: blur(10px);
    }
    
    /* 標題樣式 */
    h1, h2, h3 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 25px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    h1 {
        font-size: 2.2em;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 30px;
    }
    
    /* 輸入框組樣式 */
    .form-group {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .form-group:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* 輸入框樣式 */
    .form-control {
        border-radius: 12px !important;
        border: 2px solid #e1e8ed !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        background: #fafbfc !important;
    }
    
    .form-control:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background: white !important;
        transform: translateY(-1px);
    }
    
    /* 標籤樣式 */
    label {
        font-weight: 600 !important;
        color: #34495e !important;
        margin-bottom: 8px !important;
        font-size: 14px !important;
    }
    
    /* 按鈕樣式 */
    .btn {
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 8px !important;
    }
    
    .btn-primary {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    .btn-success {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(86, 171, 47, 0.4) !important;
    }
    
    .btn-success:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(86, 171, 47, 0.6) !important;
    }
    
    .btn-warning {
        background: linear-gradient(45deg, #f093fb, #f5576c) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4) !important;
    }
    
    .btn-warning:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.6) !important;
    }
    
    /* 複選框樣式 */
    .checkbox {
        margin: 15px 0 !important;
    }
    
    .checkbox input[type="checkbox"] {
        transform: scale(1.2);
        margin-right: 10px;
        accent-color: #667eea;
    }
    
    .checkbox label {
        font-size: 16px !important;
        color: #2c3e50 !important;
    }
    
    /* 結果區域樣式 */
    .result-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 25px;
        margin-top: 25px;
        border-left: 5px solid #667eea;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }
    
    .result-text {
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        line-height: 1.6;
        color: #2c3e50;
        background: white;
        padding: 20px;
        border-radius: 12px;
        white-space: pre-wrap;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    /* 卡片樣式 */
    .info-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        .pywebio-container {
            margin: 10px;
            padding: 20px;
            border-radius: 15px;
        }
        
        .form-group {
            padding: 20px;
        }
        
        h1 {
            font-size: 1.8em;
        }
    }
    
    /* 載入動畫 */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* 高亮樣式 */
    .highlight {
        background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
        padding: 2px 6px;
        border-radius: 6px;
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* 分隔線樣式 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        margin: 30px 0;
        border-radius: 2px;
    }
    </style>
    """
    put_html(custom_css)

def create_header():
    """創建頁面標題"""
    put_html("""
    <div class="pywebio-container">
        <h1>🔧 MOSFET 計算器 (VESC FOC)</h1>
        <div style="text-align: center; margin-bottom: 30px;">
            <p style="color: #7f8c8d; font-size: 16px; margin: 0;">
                專業級電機控制器 MOSFET 選型工具
            </p>
        </div>
    </div>
    """)

def mosfet_calculator():
    # 清空輸出並添加樣式
    clear()
    add_custom_styles()
    create_header()
    
    # 使用自定義樣式的輸入表單
    put_html('<div class="form-group">')
    
    # 輸入表單
    data = pywebio.input.input_group("📊 輸入參數", [
        input("電機功率 (W)", name="max_power", type=FLOAT, value=2700, 
              help_text="電機的最大功率輸出"),
        input("KV (RPM/V)", name="motor_kv", type=FLOAT, value=190,
              help_text="電機的KV值，每伏特對應的轉速"),
        input("每相 RMS 電流 (A)", name="max_current", type=FLOAT, value=75,
              help_text="電機每相的有效值電流"),
        input("最大電壓 (V)", name="v_max", type=FLOAT, value=60,
              help_text="系統的最大工作電壓"),
        checkbox("控制選項", name="foc", options=[
            {'label': '🎯 使用 FOC 控制', 'value': True, 'selected': True}
        ], help_text="FOC控制具有更高的效率和更低的噪音")
    ])
    
    put_html('</div>')
    
    # 提取輸入
    max_power = data["max_power"]
    motor_kv = data["motor_kv"]
    max_current = data["max_current"]
    v_max = data["v_max"]
    foc = data["foc"][0] if data["foc"] else False
    
    # 顯示載入動畫
    put_html("""
    <div style="text-align: center; margin: 20px 0;">
        <div class="loading"></div>
        <p style="color: #7f8c8d; margin-top: 10px;">正在計算中...</p>
    </div>
    """)
    
    # 固定參數（針對 VESC FOC）
    n_parallel = 2
    k_margin = 1.5
    k_derate = 1.3
    D = 0.8
    f_sw = 30000
    t_r_f = 100e-9
    Qg = 100e-9
    Vgs = 10
    Rds_on_assumed = 0.0015
    eta = 0.95 if foc else 0.90
    Pd_max = 50
    
    # 計算電池側直流電流
    I_phase_rms = max_current
    I_cont = I_phase_rms * math.sqrt(3) / (math.sqrt(2) * eta)
    
    # 驗證功率
    I_cont_power = max_power / (v_max * eta)
    
    # 每個 MOSFET 電流
    I_mos_rms = I_phase_rms / n_parallel
    I_mos_peak = (I_phase_rms * math.sqrt(2)) / n_parallel
    I_mos_min = I_mos_rms * k_derate
    
    # 電壓規格（考慮 BEMF）
    max_rpm = motor_kv * v_max
    bemf_voltage = max_rpm / motor_kv * 0.9
    Vds_min = max(v_max, bemf_voltage) * k_margin
    
    # 最大 Rds(on)
    Rds_on_max = (Pd_max / (I_mos_rms**2 * D)) * 1000
    
    # 功率損耗
    P_cond = I_mos_rms**2 * Rds_on_assumed * D
    P_sw = (v_max * I_mos_peak * t_r_f * f_sw) / 2 + (Qg * Vgs * f_sw)
    P_total = P_cond + P_sw
    
    # 散熱建議
    cooling = "標準散熱器" if P_total < 30 else "強制風冷"
    
    # 清除載入動畫
    clear()
    add_custom_styles()
    create_header()
    
    # 顯示結果
    control_type = "FOC" if foc else "BLDC"
    
    # 輸入參數卡片
    put_html('<div class="info-card">')
    put_markdown(f"""
### 📋 輸入參數
- **電機功率**: {max_power}W
- **KV**: {motor_kv} RPM/V  
- **每相 RMS 電流**: {max_current}A
- **最大電壓**: {v_max}V
- **控制模式**: {control_type}
""")
    put_html('</div>')
    
    # 電流分析卡片
    put_html('<div class="info-card">')
    put_markdown(f"""
### ⚡ 電流分析
- **電池電流**: <span class="highlight">{round(I_cont, 1)}A</span> (功率推算: {round(I_cont_power, 1)}A)
- **每相 RMS 電流**: <span class="highlight">{round(I_phase_rms, 1)}A</span>
- **每個 MOSFET RMS 電流**: <span class="highlight">{round(I_mos_rms, 1)}A</span>
""")
    put_html('</div>')
    
    # BEMF 分析卡片
    put_html('<div class="info-card">')
    put_markdown(f"""
### 🔄 BEMF 分析
- **最大轉速**: <span class="highlight">{round(max_rpm, 0)} RPM</span>
- **反電動勢**: <span class="highlight">{round(bemf_voltage, 1)}V</span>
""")
    put_html('</div>')
    
    # MOSFET 規格要求卡片
    put_html('<div class="info-card">')
    put_markdown(f"""
### 🔧 MOSFET 規格要求
1. **Vds** > <span class="highlight">{round(Vds_min, 1)}V</span>
2. **Id** > <span class="highlight">{round(I_mos_min, 1)}A</span>  
3. **Rds(on)** < <span class="highlight">{round(Rds_on_max, 2)}mΩ</span>
""")
    put_html('</div>')
    
    # 功率損耗分析卡片
    put_html('<div class="info-card">')
    put_markdown(f"""
### 🔥 功率損耗分析
- **每個 MOSFET 功率損耗**: <span class="highlight">{round(P_total, 2)}W</span>
  - 導通損耗: {round(P_cond, 2)}W
  - 開關損耗: {round(P_sw, 2)}W
- **總熱量 (12個MOSFET)**: <span class="highlight">{round(P_total * 12, 2)}W</span>
- **散熱建議**: <span class="highlight">{cooling}</span>
""")
    put_html('</div>')
    
    # 按鈕區域
    put_html('<hr>')
    
    def show_engineering_data():
        # 工程用數據（含 20% 裕度）
        Vds_eng = Vds_min * 1.2
        Id_eng = I_mos_min * 1.2
        Rds_on_eng = Rds_on_max * 0.8
        
        put_html('<div class="info-card" style="border-left: 5px solid #e74c3c;">')
        put_markdown(f"""
### 🛠️ 工程用數據（含 20% 裕度）
#### 保守設計規格:
1. **Vds** > <span class="highlight">{round(Vds_eng, 1)}V</span>
2. **Id** > <span class="highlight">{round(Id_eng, 1)}A</span>
3. **Rds(on)** < <span class="highlight">{round(Rds_on_eng, 2)}mΩ</span>

#### 散熱設計建議:
- 選擇熱阻 < **0.5°C/W** 的散熱器
- 建議尺寸約 **20cm × 10cm × 5cm**  
- 考慮使用導熱膠或導熱墊
- 確保良好的空氣流通

#### 注意事項:
- ✅ 以上數據已包含 20% 安全裕度
- ✅ 適用於 VESC {control_type} 控制模式
- ⚠️ 建議在實際應用前進行熱測試
""")
        put_html('</div>')
    
    def restart_calculator():
        mosfet_calculator()
    
    # 操作按鈕
    put_row([
        put_column([
            put_buttons([
                {'label': '🛠️ 顯示工程用數據', 'value': 'eng', 'color': 'success'}
            ], onclick=lambda _: show_engineering_data())
        ]),
        put_column([
            put_buttons([
                {'label': '🔄 重新計算', 'value': 'restart', 'color': 'primary'}
            ], onclick=lambda _: restart_calculator())
        ]),
        put_column([
            put_buttons([
                {'label': '❌ 清除', 'value': 'clear', 'color': 'warning'}
            ], onclick=lambda _: clear())
        ])
    ])
    
    # 頁尾
    put_html("""
    <div style="text-align: center; margin-top: 40px; padding: 20px; color: #7f8c8d;">
        <hr>
        <p>🚀 MOSFET Calculator v2.0 | Powered by PyWebIO</p>
        <p style="font-size: 12px;">專業級電機控制器設計工具</p>
    </div>
    </div>
    """)

def run_desktop_app():
    # 啟動 PyWebIO 伺服器（後台運行）
    pywebio.start_server(mosfet_calculator, port=8080, auto_open_webbrowser=False)
    # 使用 PyWebView 創建桌面視窗
    webview.create_window("🔧 MOSFET 計算器 (VESC FOC)", "http://localhost:8080", 
                         width=900, height=800, resizable=True, 
                         min_size=(700, 600))
    webview.start()

if __name__ == "__main__":
    run_desktop_app()