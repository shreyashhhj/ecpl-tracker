import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ECPL 2026 Team Squad & Purse Tracker",
    page_icon="🏏",
    layout="wide",
)

TOTAL_PURSE_CR = 100.0  # 100 Crores

# --- INITIALIZE TEAMS, CAPTAINS & VCs ---
if "teams" not in st.session_state:
  st.session_state.teams = {
      "White Falcons": {
          "captain": "Vedant Karande",
          "vc": "Divya Tiwari",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Vedant Karande (C)", "Price": 0.0, "Role": "Captain"},
              {
                  "Name": "Divya Tiwari (VC)",
                  "Price": 0.0,
                  "Role": "Vice-Captain",
              },
          ],
      },
      "Granite Gladiators": {
          "captain": "Paresh Dube",
          "vc": "Jhanvi Bhusare",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Paresh Dube (C)", "Price": 0.0, "Role": "Captain"},
              {
                  "Name": "Jhanvi Bhusare (VC)",
                  "Price": 0.0,
                  "Role": "Vice-Captain",
              },
          ],
      },
      "Rising Champions": {
          "captain": "Aziz Azad",
          "vc": "Sharwari Gawande",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Aziz Azad (C)", "Price": 0.0, "Role": "Captain"},
              {
                  "Name": "Sharwari Gawande (VC)",
                  "Price": 0.0,
                  "Role": "Vice-Captain",
              },
          ],
      },
      "Red Raptors": {
          "captain": "Swayam Tiwari",
          "vc": "Thalisha Godhani",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Swayam Tiwari (C)", "Price": 0.0, "Role": "Captain"},
              {
                  "Name": "Thalisha Godhani (VC)",
                  "Price": 0.0,
                  "Role": "Vice-Captain",
              },
          ],
      },
      "Phantom Blues": {
          "captain": "Shreyash Jaiswal",
          "vc": "Ahana Kapse",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Shreyash Jaiswal (C)", "Price": 0.0, "Role": "Captain"},
              {
                  "Name": "Ahana Kapse (VC)",
                  "Price": 0.0,
                  "Role": "Vice-Captain",
              },
          ],
      },
      "Team Pirates": {
          "captain": "Prasad Akle",
          "vc": "Jiya Kurjekar",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Prasad Akle (C)", "Price": 0.0, "Role": "Captain"},
              {
                  "Name": "Jiya Kurjekar (VC)",
                  "Price": 0.0,
                  "Role": "Vice-Captain",
              },
          ],
      },
      "Gold Gangsters": {
          "captain": "Ansh Bisen",
          "vc": "Palak Jane",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Ansh Bisen (C)", "Price": 0.0, "Role": "Captain"},
              {"Name": "Palak Jane (VC)", "Price": 0.0, "Role": "Vice-Captain"},
          ],
      },
      "Mighty Mavericks": {
          "captain": "Aarav Shukla",
          "vc": "Mahek Mishra",
          "purse": TOTAL_PURSE_CR,
          "squad": [
              {"Name": "Aarav Shukla (C)", "Price": 0.0, "Role": "Captain"},
              {
                  "Name": "Mahek Mishra (VC)",
                  "Price": 0.0,
                  "Role": "Vice-Captain",
              },
          ],
      },
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
          "Status": "Available",
          "Assigned Team": "-",
          "Purchase Price (Cr)": 0.0,
      })
    st.session_state.players = pd.DataFrame(players_list)
  except Exception as e:
    st.error(f"Error loading player registration file: {e}")
    st.session_state.players = pd.DataFrame(
        columns=[
            "ID",
            "Name",
            "Year",
            "Role",
            "Status",
            "Assigned Team",
            "Purchase Price (Cr)",
        ]
    )

# --- SIDEBAR CONTROLS WITH SAFE RESET ---
st.sidebar.title("⚙️ Database Management")

# Safe reset logic using expander or confirmation checkbox
with st.sidebar.expander("⚠️ Danger Zone (Reset)"):
  confirm_reset = st.checkbox("I want to reset all data")
  if st.button("🔄 Confirm Reset All Data", type="primary"):
    if confirm_reset:
      st.session_state.clear()
      st.success("Data reset successfully!")
      st.rerun()
    else:
      st.warning("Please check the confirmation box above first!")

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Instructions:**\n1. Select a team below to assign players and"
    " enter price in Crores (Cr).\n2. View squads and remaining purse live!"
)

# --- MAIN HEADER ---
st.title("⚡ ECPL 2026 — Team Squad & Purse Tracker (Cr) 🏏")
st.markdown(
    "Monitor team budgets, squad compositions, and player distribution in"
    " Crores."
)
st.markdown("---")

# --- HIGHLIGHT YOUR TEAM (PHANTOM BLUES) ---
st.subheader("🔥 Your Team Dashboard (Phantom Blues)")
pb_data = st.session_state.teams["Phantom Blues"]
pb_spent = TOTAL_PURSE_CR - pb_data["purse"]
pb_c1, pb_c2, pb_c3 = st.columns(3)
pb_c1.metric("Remaining Purse", f"₹ {pb_data['purse']:.2f} Cr")
pb_c2.metric("Total Spent", f"₹ {pb_spent:.2f} Cr")
pb_c3.metric("Squad Size", f"{len(pb_data['squad'])} Players")

with st.expander("🛡️ View Phantom Blues Squad Details"):
  for p in pb_data["squad"]:
    st.text(
        f"• {p['Name']} — Role: {p.get('Role', 'Player')} (Price: ₹"
        f" {p['Price']:.2f} Cr)"
    )

st.markdown("---")

# --- ASSIGNMENT SECTION (MANAGE TEAMS) ---
st.subheader("📝 Assign / Manage Team Squads")

col_asg1, col_asg2, col_asg3 = st.columns(3)

df = st.session_state.players
available_df = df[df["Status"] == "Available"]
available_players = available_df["Name"].tolist()

with col_asg1:
  selected_team = st.selectbox(
      "Select Team to Update:", list(st.session_state.teams.keys())
  )

with col_asg2:
  if available_players:
    selected_player = st.selectbox(
        "Select Available Player:", available_players
    )
  else:
    selected_player = None
    st.info("All players assigned!")

with col_asg3:
  player_price_cr = st.number_input(
      "Player Cost / Price (in Cr):",
      min_value=0.0,
      step=0.1,
      value=0.5,
      format="%.2f",
  )

if selected_player:
  if st.button("➕ Assign Player to Team", type="primary"):
    if st.session_state.teams[selected_team]["purse"] >= player_price_cr:
      # Deduct from team purse
      st.session_state.teams[selected_team]["purse"] -= player_price_cr
      # Add to team squad
      st.session_state.teams[selected_team]["squad"].append({
          "Name": selected_player,
          "Price": player_price_cr,
          "Role": df[df["Name"] == selected_player]["Role"].values[0],
      })
      # Update main dataframe
      idx = df[df["Name"] == selected_player].index[0]
      st.session_state.players.at[idx, "Status"] = "Assigned"
      st.session_state.players.at[idx, "Assigned Team"] = selected_team
      st.session_state.players.at[idx, "Purchase Price (Cr)"] = player_price_cr

      st.success(
          f"✅ {selected_player} successfully added to {selected_team} for ₹"
          f" {player_price_cr:.2f} Cr!"
      )
      st.rerun()
    else:
      st.error(
          f"❌ {selected_team} does not have enough remaining purse for this"
          " amount!"
      )

st.markdown("---")

# --- OVERALL TEAMS OVERVIEW GRID ---
st.subheader("📊 All 8 Teams Overview & Squads")

team_names = list(st.session_state.teams.keys())
for i in range(0, len(team_names), 4):
  cols = st.columns(4)
  for j in range(4):
    if i + j < len(team_names):
      t_name = team_names[i + j]
      data = st.session_state.teams[t_name]
      with cols[j]:
        spent = TOTAL_PURSE_CR - data["purse"]
        st.markdown(f"### **{t_name}**")
        st.write(f"👑 **C:** {data['captain']}")
        st.write(f"🛡️ **VC:** {data['vc']}")
        st.metric(
            label="Remaining Purse",
            value=f"₹ {data['purse']:.2f} Cr",
            delta=f"-₹ {spent:.2f} Cr",
        )
        st.write(f"👥 **Squad:** {len(data['squad'])} Players")
        with st.expander(f"Inspect {t_name}"):
          for p in data["squad"]:
            st.text(
                f"- {p['Name']}"
                + (f" (₹ {p['Price']:.2f} Cr)" if p["Price"] > 0 else "")
            )
  st.markdown("---")

# --- MASTER PLAYER DIRECTORY TABLE ---
st.subheader("📋 Master Player Directory (All 113 Registered Players)")

search_q = st.text_input(
    "Search Player by Name or Role:",
    placeholder="Type name to search...",
)
if search_q:
  display_df = df[
      df["Name"].str.contains(search_q, case=False, na=False)
      | df["Role"].str.contains(search_q, case=False, na=False)
  ]
else:
  display_df = df

st.dataframe(display_df, use_container_width=True, hide_index=True)