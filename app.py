import streamlit as st
import numpy as np

# --- 1. DATASETS (BTRP, RAWALJE, & FLOW) ---
U_DATA = { # BTRP DAM
    90.000: 4.336, 90.025: 4.354, 90.050: 4.371, 90.075: 4.389, 90.100: 4.406,
    90.125: 4.424, 90.150: 4.441, 90.175: 4.459, 90.200: 4.476, 90.225: 4.494,
    90.250: 4.511, 90.275: 4.529, 90.300: 4.546, 90.325: 4.564, 90.350: 4.581,
    90.375: 4.599, 90.400: 4.616, 90.425: 4.634, 90.450: 4.651, 90.475: 4.669,
    90.500: 4.686, 90.525: 4.704, 90.550: 4.721, 90.575: 4.739, 90.600: 4.756,
    90.625: 4.774, 90.650: 4.791, 90.675: 4.809, 90.700: 4.826, 90.725: 4.844,
    90.750: 4.861, 90.775: 4.879, 90.800: 4.896, 90.825: 4.914, 90.850: 4.931,
    90.875: 4.949, 90.900: 4.966, 90.925: 4.984, 90.950: 5.001, 90.975: 5.019,
    91.000: 5.036, 91.025: 5.054, 91.125: 5.124, 91.250: 5.211, 91.375: 5.299,
    91.500: 5.386, 91.625: 5.474, 91.750: 5.561, 91.875: 5.649, 92.000: 5.736,
    92.250: 5.936, 92.500: 6.137, 92.750: 6.338, 93.000: 6.539, 93.250: 6.739,
    93.500: 6.940, 93.750: 7.141, 94.000: 7.342, 94.250: 7.535, 94.400: 7.862,
    94.500: 8.067, 94.750: 8.579, 95.000: 9.081
}

L_DATA = { # RAWALJE FOREBAY
    89.000: 2.870, 89.250: 2.975, 89.500: 3.080, 89.750: 3.185, 90.000: 3.290,
    90.250: 3.345, 90.500: 3.400, 90.750: 3.520, 91.000: 3.640, 91.250: 3.765,
    91.500: 3.890, 91.750: 3.955, 92.000: 4.020, 92.250: 4.135, 92.500: 4.250,
    92.750: 4.365, 93.000: 4.480, 93.250: 4.570, 93.500: 4.660, 93.750: 4.750,
    94.000: 4.840, 94.250: 4.945, 94.500: 5.050, 94.750: 5.495, 95.000: 5.940
}

FLOW_DATA = { # Diff(m): Flow(m3/s)
    0.000: 0.00, 0.063: 2.50, 0.125: 5.00, 0.188: 7.50, 0.250: 10.00,
    0.313: 12.50, 0.375: 15.00, 0.438: 17.50, 0.500: 20.00, 0.563: 20.75,
    0.625: 21.50, 0.688: 22.25, 0.750: 23.00, 0.813: 23.75, 0.875: 24.50,
    0.938: 25.25, 1.000: 26.00, 1.125: 27.50, 1.250: 29.00, 1.375: 30.50,
    1.500: 32.00, 1.625: 33.50, 1.750: 35.00, 1.875: 36.50, 2.000: 38.00,
    2.125: 39.13, 2.250: 40.25, 2.375: 41.38, 2.500: 42.50, 2.625: 43.63,
    2.750: 44.75, 2.875: 45.88, 3.000: 47.00, 3.125: 48.00, 3.250: 49.00,
    3.375: 50.00, 3.500: 51.00, 3.625: 52.00, 3.750: 53.00, 3.875: 54.00,
    4.000: 55.00, 4.125: 56.00, 4.250: 57.00, 4.375: 58.00, 4.500: 59.00,
    4.625: 60.00, 4.750: 61.00, 4.875: 62.00, 5.000: 63.00
}

# --- 2. CORE FUNCTIONS ---
def get_mcm(level, data_dict):
    keys = np.array(list(data_dict.keys()))
    vals = np.array(list(data_dict.values()))
    return np.interp(level, keys, vals)

def get_rl(mcm, data_dict):
    keys = np.array(list(data_dict.keys()))
    vals = np.array(list(data_dict.values()))
    return np.interp(mcm, vals, keys)

def get_flow_mcm_hr(head_diff):
    if head_diff <= 0: return 0.0
    diffs = np.array(list(FLOW_DATA.keys()))
    flows = np.array(list(FLOW_DATA.values()))
    flow_m3_sec = np.interp(head_diff, diffs, flows)
    return (flow_m3_sec * 3600) / 1000000 # Convert to MCM/hr

# --- 3. APP SETUP & MOBILE DARK MODE ---
st.set_page_config(page_title="BTRP-Rawalje Planner", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    div[data-baseweb="input"] { background-color: #1A1C24 !important; border: 1px solid #4B5563 !important; }
    input { color: #00FFC2 !important; font-weight: bold !important; }
    div[data-testid="stMetric"] { background-color: #1F2937; border: 2px solid #374151; border-radius: 12px; padding: 15px; }
    div[data-testid="stMetricValue"] { color: #00D1FF !important; }
    div[data-testid="stMetricLabel"] { color: #E5E7EB !important; font-size: 1.1rem !important; }
    .stButton>button { width: 100%; background-color: #3B82F6; color: white; font-weight: bold; border-radius: 10px; height: 3.5em; border: none; }
    h1 { color: #60A5FA; text-shadow: 2px 2px #000; text-align: center; }
    h2, h3 { color: #FB923C; }
    .danger-alert { color: #FF3131; font-weight: bold; border: 2px solid #FF3131; padding: 10px; border-radius: 5px; background: #2D0000; margin-bottom: 15px; }
    .warning-alert { color: #FFAC1C; font-weight: bold; border: 2px solid #FFAC1C; padding: 10px; border-radius: 5px; background: #2D1B00; margin-bottom: 15px; }
    .time-card { background-color: #064E3B; border: 2px solid #10B981; color: #D1FAE5; padding: 15px; border-radius: 12px; font-size: 1.2rem; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ BTRP & Rawalje Dispatch Planner")

# --- 4. TOP SECTION: CURRENT READINGS ---
st.header("📍 Current Shift Data")
col_curr1, col_curr2 = st.columns(2)
with col_curr1:
    curr_u_rl = st.number_input("Current BTRP RL (m)", value=94.450, format="%.3f")
with col_curr2:
    curr_l_rl = st.number_input("Current Rawalje RL (m)", value=90.000, format="%.3f")

u_rate = 0.820  # MCM/MUS for BTRP Generation
l_rate = 9.360  # MCM/MUS for Rawalje Generation
pump_rate = 0.211 # MCM/hr

st.divider()

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(["🎯 PLANNING MODE", "🔮 SIMULATION MODE", "🚜 PUMPING & BHIRA"])

# --- TAB 1: PLANNING MODE ---
with tab1:
    st.subheader("Plan Generation & Gate Opening Time")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        u_target_rl = st.number_input("Target BTRP RL (m)", value=94.500, format="%.3f")
    with p_col2:
        l_gen_target = st.number_input("Rawalje Generation Plan (MUS)", value=0.080, format="%.3f")

    if st.button("Calculate Shift Plan & Gate Time"):
        start_u_mcm = get_mcm(curr_u_rl, U_DATA)
        start_l_mcm = get_mcm(curr_l_rl, L_DATA)
        target_u_mcm = get_mcm(u_target_rl, U_DATA)
        
        demand_l = l_gen_target * l_rate
        available_l = start_l_mcm - 3.290 
        transfer_needed = max(0.0, demand_l - available_l)
        
        gen_for_level = (target_u_mcm - start_u_mcm) / u_rate
        gen_for_transfer = transfer_needed / u_rate
        total_gen_required = gen_for_level + gen_for_transfer
        
        u_temp_mcm = start_u_mcm + (total_gen_required * u_rate)
        l_temp_mcm = start_l_mcm - (l_gen_target * l_rate)
        
        minutes_required = 0
        total_transferred = 0.0
        
        while total_transferred < transfer_needed:
            u_rl_now = get_rl(u_temp_mcm, U_DATA)
            l_rl_now = get_rl(l_temp_mcm, L_DATA)
            h_diff = u_rl_now - l_rl_now
            if h_diff <= 0: break
            flow_min = get_flow_mcm_hr(h_diff) / 60
            u_temp_mcm -= flow_min
            l_temp_mcm += flow_min
            total_transferred += flow_min
            minutes_required += 1
            if minutes_required > 1440: break

        hrs = minutes_required // 60
        mins = minutes_required % 60
        st.divider()
        st.metric("Total generation required", f"{total_gen_required:.3f} Mus")
        if transfer_needed > 0:
            st.markdown(f'<div class="time-card">⏱️ INTAKE GATES MUST BE OPEN FOR: {hrs} Hours and {mins} Minutes</div>', unsafe_allow_html=True)

# --- TAB 2: SIMULATION MODE ---
with tab2:
    st.subheader("Predictive 'What-If' Simulation")
    gate_status = st.toggle("Interconnecting Gate Open?", value=False, key="sim_gate")
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        sim_u_gen = st.number_input("BTRP Total generation (Mus)", value=0.120, format="%.3f")
    with s_col2:
        sim_l_gen = st.number_input("Rawalje PH Generation (Mus)", value=0.050, format="%.3f")
    with s_col3:
        sim_hours = st.number_input("Gate Open Time (Hrs)", value=6.0 if gate_status else 0.0, disabled=not gate_status, key="sim_time")

    if st.button("Start Simulation"):
        u_mcm = get_mcm(curr_u_rl, U_DATA) + (sim_u_gen * u_rate)
        l_mcm = get_mcm(curr_l_rl, L_DATA) - (sim_l_gen * l_rate)
        total_moved = 0.0
        if gate_status and sim_hours > 0:
            for m in range(int(sim_hours * 60)):
                u_rl_now = get_rl(u_mcm, U_DATA)
                l_rl_now = get_rl(l_mcm, L_DATA)
                h_diff = u_rl_now - l_rl_now
                if h_diff <= 0: break
                flow_min = get_flow_mcm_hr(h_diff) / 60
                u_mcm -= flow_min
                l_mcm += flow_min
                total_moved += flow_min
        
        final_u_rl = get_rl(u_mcm, U_DATA)
        final_l_rl = get_rl(l_mcm, L_DATA)
        st.divider()
        
        st.info(f"""
        **Calculation Summary:**
        * Water added from BTRP Gen: **{(sim_u_gen * u_rate):.3f} MCM**
        * Water used by Rawalje Gen: **{(sim_l_gen * l_rate):.3f} MCM**
        * Water transferred via Gates: **{total_moved:.3f} MCM**
        """)

        if final_l_rl < 90.000:
            st.markdown(f'<div class="danger-alert">⚠️ ALERT: Final Rawalje level ({final_l_rl:.3f}m) falls below 90.00m!</div>', unsafe_allow_html=True)

        col_res1, col_res2 = st.columns(2)
        with col_res1: st.metric("Final BTRP RL", f"{final_u_rl:.3f} m")
        with col_res2: st.metric("Final Rawalje RL", f"{final_l_rl:.3f} m")

# --- TAB 3: PUMPING & BHIRA OPERATION ---
with tab3:
    st.subheader("BTRP Pumping & Bhira Generation Analysis")
    
    if curr_u_rl >= 94.480:
        st.success(f"✅ BTRP RL is {curr_u_rl:.3f}m. Pumping is POSSIBLE.")
    else:
        st.markdown(f'<div class="warning-alert">⚠️ BTRP RL is {curr_u_rl:.3f}m (Below 94.48m). Pumping NOT RECOMMENDED.</div>', unsafe_allow_html=True)

    st.info(f"Pumping Rate Fixed at: {pump_rate} MCM/hr (Discharged Out)")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        pump_hrs = st.number_input("Pumping Duration (Hrs)", min_value=0.0, value=3.0, step=0.5)
    with col_p2:
        bhira_gen = st.number_input("Bhira Generation (Mus)", min_value=0.0, value=0.0, format="%.3f")
    with col_p3:
        p_gate_status = st.toggle("Interconnecting Gate Open?", value=False, key="pump_gate")

    if st.button("Analyze Pumping Effect"):
        u_mcm = get_mcm(curr_u_rl, U_DATA)
        l_mcm = get_mcm(curr_l_rl, L_DATA)
        
        net_btrp_change = (bhira_gen * u_rate) - (pump_hrs * pump_rate)
        u_mcm += net_btrp_change
        
        total_moved = 0.0
        if p_gate_status:
            for m in range(int(pump_hrs * 60)):
                u_rl_now = get_rl(u_mcm, U_DATA)
                l_rl_now = get_rl(l_mcm, L_DATA)
                h_diff = u_rl_now - l_rl_now
                if h_diff <= 0: break
                flow_min = get_flow_mcm_hr(h_diff) / 60
                u_mcm -= flow_min
                l_mcm += flow_min
                total_moved += flow_min

        final_u_rl = get_rl(u_mcm, U_DATA)
        final_l_rl = get_rl(l_mcm, L_DATA)
        st.divider()
        
        if final_u_rl < 93.850:
            st.markdown(f'<div class="danger-alert">❌ ALERT: Pumping cannot be possible for {pump_hrs} hours. Final BTRP level ({final_u_rl:.3f}m) drops below 93.85m!</div>', unsafe_allow_html=True)

        st.write(f"Total Water Pumped Out: **{pump_hrs * pump_rate:.3f} MCM**")
        if bhira_gen > 0:
            st.write(f"Total Water Inflow from Bhira: **{bhira_gen * u_rate:.3f} MCM**")
            
        p_res1, p_res2 = st.columns(2)
        with p_res1: st.metric("New BTRP RL", f"{final_u_rl:.3f} m")
        with p_res2: st.metric("New Rawalje RL", f"{final_l_rl:.3f} m")
