import streamlit as st
import numpy as np

# --- 1. SHARED DATASETS (BTRP & RAWALJE) ---
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
    # Logic from your 2nd code: head-based discharge rates
    if head_diff > 3.0: return 0.17
    elif 2.0 <= head_diff <= 3.0: return 0.15
    elif 1.5 <= head_diff < 2.0: return 0.12
    elif head_diff > 0: return 0.08
    else: return 0.0

# --- 3. APP SETUP ---
st.set_page_config(page_title="BTRP-Rawalje Planner", layout="wide")
st.title("⚡ BTRP Dam & Rawalje PH Unified Tool")

# Sidebar for Current Readings
with st.sidebar:
    st.header("📍 Current Shift Levels")
    curr_u_rl = st.number_input("BTRP Level (m)", value=94.450, format="%.3f")
    curr_l_rl = st.number_input("Rawalje Level (m)", value=90.000, format="%.3f")
    st.divider()
    u_rate = 0.820  # MCM/MUS for BTRP
    l_rate = 9.360  # MCM/MUS for Rawalje

tab1, tab2 = st.tabs(["🎯 Planning (Generation Needed)", "🔮 Simulation (What-If?)"])

# --- TAB 1: PLANNING MODE ---
with tab1:
    st.subheader("Calculate Requirements to reach Targets")
    col1, col2 = st.columns(2)
    with col1:
        u_target_rl = st.number_input("BTRP Target RL (m)", value=94.500, format="%.3f")
    with col2:
        l_gen_target = st.number_input("Planned Rawalje Gen (MUS)", value=0.080, format="%.3f")

    if st.button("Calculate Plan"):
        # Initial Storage
        start_u_mcm = get_mcm(curr_u_rl, U_DATA)
        start_l_mcm = get_mcm(curr_l_rl, L_DATA)
        target_u_mcm = get_mcm(u_target_rl, U_DATA)
        
        # Rawalje Requirement
        demand_l = l_gen_target * l_rate
        floor_l_mcm = 3.290 # RL 90.000
        available_l = start_l_mcm - floor_l_mcm
        transfer_needed = max(0.0, demand_l - available_l)
        
        # BTRP Generation
        gen_for_level = (target_u_mcm - start_u_mcm) / u_rate
        gen_for_transfer = transfer_needed / u_rate
        total_btrp_gen = gen_for_level + gen_for_transfer
        
        st.divider()
        res1, res2 = st.columns(2)
        res1.metric("Total BTRP Gen Required", f"{total_btrp_gen:.3f} MUS")
        res1.write(f"For Target RL: {gen_for_level:.3f} MUS")
        res1.write(f"For Transfer: {gen_for_transfer:.3f} MUS")
        
        res2.metric("Volume to Transfer", f"{transfer_needed:.3f} MCM")
        st.info("Note: Use Tab 2 to find the exact gate hours based on this Volume.")

# --- TAB 2: SIMULATION MODE ---
with tab2:
    st.subheader("Predict levels based on specific Gen/Gate Hours")
    c1, c2, c3 = st.columns(3)
    with c1:
        sim_u_gen = st.number_input("BTRP Generation (MUS)", value=0.120, format="%.3f")
    with c2:
        sim_l_gen = st.number_input("Rawalje Generation (MUS)", value=0.050, format="%.3f")
    with c3:
        sim_hours = st.number_input("Gate Open Time (Hours)", value=6.0)

    if st.button("Run What-If Simulation"):
        u_mcm = get_mcm(curr_u_rl, U_DATA) + (sim_u_gen * u_rate)
        l_mcm = get_mcm(curr_l_rl, L_DATA) - (sim_l_gen * l_rate)
        
        total_moved = 0.0
        # 1-minute iterative loop
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
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("Final BTRP RL", f"{final_u_rl:.3f} m")
        col_r2.metric("Final Rawalje RL", f"{final_l_rl:.3f} m")
        col_r3.metric("Total Transferred", f"{total_moved:.3f} MCM")
