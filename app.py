import base64
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION & STYLING (OPACITY 0.50 & FIXED BG) ---
st.set_page_config(
    page_title="ECPL 2026 Auction Tracker", page_icon="🏏", layout="wide"
)


# Function to encode local image for background
def get_base64_of_bin_file(bin_file):
  with open(bin_file, "rb") as f:
    data = f.read()
  return base64.b64encode(data).decode()


try:
  bin_str = get_base64_of_bin_file("bg.jpeg")
  bg_css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.50), rgba(0, 0, 0, 0.50)), url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #ffffff;
    }}
    .stMetric {{
        background-color: rgba(22, 27, 34, 0.9);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }}
    .assignment-box {{
        background-color: rgba(22, 27, 34, 0.88);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #484f58;
        margin-bottom: 20px;
    }}
    </style>
    """
except Exception:
  bg_css = """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
    """

st.markdown(bg_css, unsafe_allow_html=True)

TOTAL_PURSE_CR = 100.0  # 100 Crores

# --- TEAMS LIST (PHANTOM BLUES FIRST) ---
team_list = [
    "Phantom Blues",
    "White Falcons",
    "Granite Gladiators",
    "Rising Champions",
    "Red Raptors",
    "Team Pirates",
    "Gold Gangsters",
    "Mighty Mavericks",
]

# --- CAPTAINS & VICE-CAPTAINS FOR ALL TEAMS ---
team_leadership = {
    "Phantom Blues": {"c": "Shreyash Jaiswal", "vc": "Aahana Kapse"},
    "White Falcons": {"c": "Vedant Karande", "vc": "Divya Tiwari"},
    "Granite Gladiators": {"c": "Paresh Dube", "vc": "Jhanvi Bhusare"},
    "Rising Champions": {"c": "Aziz Azad", "vc": "Sharvori Gawande"},
    "Red Raptors": {"c": "Swayam Tiwari", "vc": "Thalisha Godhani"},
    "Team Pirates": {"c": "Prasad Akle", "vc": "Jiya Kurjekar"},
    "Gold Gangsters": {"c": "Ansh Bisen", "vc": "Palak Jane"},
    "Mighty Mavericks": {"c": "Aarav Shukla", "vc": "Mahek Mishra"},
}

# --- INITIALIZE TEAMS ---
if "teams" not in st.session_state:
  st.session_state.teams = {}
  for t in team_list:
    c_name = team_leadership[t]["c"]
    vc_name = team_leadership[t]["vc"]
    st.session_state.teams[t] = {
        "captain": c_name,
        "vc": vc_name,
        "purse": TOTAL_PURSE_CR,
        "squad": [
            {"Name": f"{c_name} (C)", "Price": 0.0, "Role": "Captain"},
            {"Name": f"{vc_name} (VC)", "Price": 0.0, "Role": "VC"},
        ],
    }

# --- LOAD REGISTERED PLAYERS FROM EXCEL FILE ---
if "players" not in st.session_state:
  try:
    df_raw = pd.read_excel(
        "⚡ ECPL 2026 — Official Player Registration   (Responses).xlsx"
    )
    players_list = []
    for idx, row in df_raw.iterrows():
      players_list.append({
          "ID": idx + 1,
          "Name": str(row.get("Full Name", "")).strip(),
          "Year": str(row.get("Year of Study", "")).strip() + " Year",
          "Role": str(row.get("Player Primary Role", "")).strip(),
          "Select Team": "Available",
          "Price (Cr)": 0.0,
      })
    st.session_state.players = pd.DataFrame(players_list)
  except Exception as e:
    st.error(f"Error loading player registration file: {e}")
    st.session_state.players = pd.DataFrame(
        columns=["ID", "Name", "Year", "Role", "Select Team", "Price (Cr)"]
    )

# --- SIDEBAR CONTROLS ---
st.sidebar.title("⚙️ Controls")
with st.sidebar.expander("⚠️ Reset Database"):
  confirm = st.checkbox("Confirm Reset")
  if st.button("🔄 Reset All"):
    if confirm:
      st.session_state.clear()
      st.success("Reset successful!")
      st.rerun()

# --- MAIN HEADER ---
st.title("⚡ ECPL 2026 — Live Squad & Purse Tracker 🏏")
st.markdown(
    "Monitor live team budgets, manage player allocations, and track the"
    " auction seamlessly."
)
st.markdown("---")

# --- YOUR TEAM HIGHLIGHT (PHANTOM BLUES) ---
pb_data = st.session_state.teams["Phantom Blues"]
pb_spent = TOTAL_PURSE_CR - pb_data["purse"]
st.subheader("🔥 Your Team: Phantom Blues Dashboard")
c1, c2, c3 = st.columns(3)
c1.metric("Remaining Purse", f"₹ {pb_data['purse']:.2f} Cr")
c2.metric("Total Spent", f"₹ {pb_spent:.2f} Cr")
c3.metric("Squad Size", f"{len(pb_data['squad'])} Players")

with st.expander("🛡️️ View Phantom Blues Squad Details"):
  if pb_data["squad"]:
    for p in pb_data["squad"]:
      st.text(
          f"• {p['Name']} — Role: {p.get('Role', 'Player')} (Price: ₹"
          f" {p.get('Price', 0.0):.2f} Cr)"
      )
  else:
    st.text("No players assigned yet.")

st.markdown("---")

# --- SYSTEMATIC ASSIGNMENT SECTION ---
st.subheader("📝 Assign / Manage Team Squads (Quick Bidding Panel)")

st.markdown('<div class="assignment-box">', unsafe_allow_html=True)
col_asg1, col_asg2, col_asg3 = st.columns(3)

df = st.session_state.players
available_df = df[df["Select Team"] == "Available"]
available_players = available_df["Name"].tolist()

with col_asg1:
  selected_team = st.selectbox(
      "🛡️ Select Team to Update:", list(st.session_state.teams.keys())
  )

with col_asg2:
  if available_players:
    selected_player = st.selectbox(
        "👤 Select Available Player:", available_players
    )
  else:
    selected_player = None
    st.info("All players have been assigned!")

with col_asg3:
  player_price_cr = st.number_input(
      "💰 Final Sold Price (in Cr):",
      min_value=0.0,
      max_value=100.0,
      step=0.1,
      value=0.5,
      format="%.2f",
  )

st.markdown("<br>", unsafe_allow_html=True)

if selected_player:
  if st.button(
      "⚡ Confirm & Assign Player to Team", type="primary", use_container_width=True
  ):
    current_team_purse = st.session_state.teams[selected_team]["purse"]
    if current_team_purse >= player_price_cr:
      idx = df[df["Name"] == selected_player].index[0]
      st.session_state.players.at[idx, "Select Team"] = selected_team
      st.session_state.players.at[idx, "Price (Cr)"] = player_price_cr

      new_teams = {}
      for t in team_list:
        c_name = team_leadership[t]["c"]
        vc_name = team_leadership[t]["vc"]
        new_teams[t] = {
            "captain": c_name,
            "vc": vc_name,
            "purse": TOTAL_PURSE_CR,
            "squad": [
                {"Name": f"{c_name} (C)", "Price": 0.0, "Role": "Captain"},
                {"Name": f"{vc_name} (VC)", "Price": 0.0, "Role": "VC"},
            ],
        }

      for i, row in st.session_state.players.iterrows():
        assigned_t = row["Select Team"]
        p_price = float(row["Price (Cr)"])
        if assigned_t != "Available":
          new_teams[assigned_t]["purse"] -= p_price
          new_teams[assigned_t]["squad"].append({
              "Name": row["Name"],
              "Role": row["Role"],
              "Price": p_price,
          })

      st.session_state.teams = new_teams
      st.success(
          f"✅ {selected_player} successfully sold to {selected_team} for ₹"
          f" {player_price_cr:.2f} Cr!"
      )
      st.rerun()
    else:
      st.error(
          f"❌ {selected_team} does not have enough remaining purse (₹"
          f" {current_team_purse:.2f} Cr) for this bid!"
      )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# --- ALL TEAMS OVERVIEW ---
st.subheader("📊 All 8 Teams Status Overview")
t_names = list(st.session_state.teams.keys())
for i in range(0, len(t_names), 4):
  cols = st.columns(4)
  for j in range(4):
    if i + j < len(t_names):
      t = t_names[i + j]
      data = st.session_state.teams[t]
      spent = TOTAL_PURSE_CR - data["purse"]
      with cols[j]:
        st.markdown(f"### **{t}**")
        st.metric("Purse Left", f"₹ {data['purse']:.2f} Cr", f"-₹ {spent:.2f} Cr")
        st.write(f"👥 Squad: {len(data['squad'])} Players")
        with st.expander(f"View {t}"):
          if data["squad"]:
            for sp in data["squad"]:
              st.text(
                  f"- {sp['Name']}"
                  + (
                      f" (₹ {sp.get('Price', 0.0):.2f} Cr)"
                      if sp.get("Price", 0.0) > 0
                      else ""
                  )
              )
          else:
            st.text("Empty squad")
  st.markdown("---")

# --- MASTER PLAYER DIRECTORY & INLINE TABLE ---
st.subheader("📋 Master Player Directory & Inline Table")
st.info(
    "👉 You can also edit values directly in the table below and click"
    " **'💾 Update All Squads & Purses'**."
)

team_options = ["Available"] + team_list

edited_df = st.data_editor(
    st.session_state.players,
    column_config={
        "Select Team": st.column_config.SelectboxColumn(
            "Assign Team", options=team_options, required=True
        ),
        "Price (Cr)": st.column_config.NumberColumn(
            "Price (Cr)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f"
        ),
    },
    disabled=["ID", "Name", "Year", "Role"],
    hide_index=True,
    use_container_width=True,
)

if st.button("💾 Update All Squads & Purses"):
  new_teams = {}
  for t in team_list:
    c_name = team_leadership[t]["c"]
    vc_name = team_leadership[t]["vc"]
    new_teams[t] = {
        "captain": c_name,
        "vc": vc_name,
        "purse": TOTAL_PURSE_CR,
        "squad": [
            {"Name": f"{c_name} (C)", "Price": 0.0, "Role": "Captain"},
            {"Name": f"{vc_name} (VC)", "Price": 0.0, "Role": "VC"},
        ],
    }

  for idx, row in edited_df.iterrows():
    assigned_t = row["Select Team"]
    p_price = float(row["Price (Cr)"])
    if assigned_t != "Available":
      new_teams[assigned_t]["purse"] -= p_price
      new_teams[assigned_t]["squad"].append({
          "Name": row["Name"],
          "Role": row["Role"],
          "Price": p_price,
      })

  st.session_state.teams = new_teams
  st.session_state.players = edited_df
  st.success("🎉 All team squads and remaining purses updated successfully!")
  st.rerun()