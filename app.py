import streamlit as st
import numpy as np

# --- 1. DATASETS (BTRP & RAWALJE) ---
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
    # Note: interp expects x-coordinates to be increasing. 
    # Since MCM increases with Level, this works perfectly.
    return np.interp(mcm, vals, keys)

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Water Management System", layout="wide")
st.title("Water Level & Pumping Control")

tab1, tab2 = st.tabs(["📊 Simulation Mode", "⚡ Pumping Mode"])

# --- TAB 1: SIMULATION MODE ---
with tab1:
    st.header("Rawalje Simulation")
    
    col1, col2 = st.columns(2)
    with col1:
        current_rl_r = st.number_input("Current Rawalje Level (m)", value=91.000, format="%.3f")
        reduction_mcm = st.number_input("Enter Reduction (MCM)", value=0.000, format="%.3f")
    
    # Logic
    start_mcm = get_mcm(current_rl_r, L_DATA)
    final_mcm = start_mcm - reduction_mcm
    final_rl_r = get_rl(final_mcm, L_DATA)
    
    st.divider()
    
    # Calculation Summary
    st.subheader("Calculation Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Initial Storage", f"{start_mcm:.3f} MCM")
    c2.metric("Target Reduction", f"{reduction_mcm:.3f} MCM")
    c3.metric("Final Projected Level", f"{final_rl_r:.3f} m")
    
    # Alert for Rawalje
    if final_rl_r < 90.000:
        st.error(f"⚠️ **CRITICAL ALERT:** Final Rawalje level ({final_rl_r:.3f}m) falls below the minimum limit of 90.00m!")

# --- TAB 2: PUMPING MODE ---
with tab2:
    st.header("BTRP Pumping Operations")
    
    btrp_rl = st.number_input("Current BTRP Level (m)", value=94.000, format="%.3f")
    op_hours = st.number_input("Enter Planned Pumping Hours", min_value=0.0, step=0.5, value=1.0)
    
    st.divider()
    
    # Alert for BTRP
    if btrp_rl < 93.850:
        st.error(f"🚫 **PUMPING HALTED:** BTRP level is {btrp_rl:.3f}m.")
        st.warning(f"Pumping cannot possible for **{op_hours}** hours.")
    else:
        st.success(f"✅ BTRP Level is sufficient ({btrp_rl:.3f}m). Pumping is possible for the requested {op_hours} hours.")
        
    # Show corresponding MCM for reference
    btrp_mcm = get_mcm(btrp_rl, U_DATA)
    st.info(f"Equivalent BTRP Storage: {btrp_mcm:.3f} MCM")
