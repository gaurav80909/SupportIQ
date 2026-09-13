import json
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

GOLDEN_PATH = PROJECT_ROOT / "data" / "golden" / "golden_set.csv"
TAXONOMY_PATH = PROJECT_ROOT / "data" / "golden" / "taxonomy.json"

st.set_page_config(
    page_title="SupportIQ — Golden Set Annotation",
    page_icon="🏷️",
    layout="wide"
)

# --- Load Taxonomy ---
if not TAXONOMY_PATH.exists():
    st.error(f"Taxonomy file not found at {TAXONOMY_PATH}.")
    st.stop()

with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
    taxonomy_data = json.load(f)
taxonomy_intents = taxonomy_data.get("intents", [])

# --- Load Golden Dataset ---
if not GOLDEN_PATH.exists():
    st.error(f"Golden dataset template not found at {GOLDEN_PATH}. Run scripts/create_golden_template.py first.")
    st.stop()

if "df" not in st.session_state:
    df_loaded = pd.read_csv(GOLDEN_PATH, dtype={"tweet_id": str, "conversation_id": str})
    # Replace NaN with empty string across text columns
    for col in ["customer_message", "brand_response", "generated_reply", "intent", "expected_action", "notes"]:
        if col in df_loaded.columns:
            df_loaded[col] = df_loaded[col].fillna("").astype(str)
    st.session_state["df"] = df_loaded

if "current_idx" not in st.session_state:
    st.session_state["current_idx"] = 0

df = st.session_state["df"]
total_rows = len(df)


def save_dataset_to_disk():
    """Saves the current in-memory dataframe back to golden_set.csv preserving schema."""
    cols = [
        "tweet_id",
        "conversation_id",
        "customer_message",
        "brand_response",
        "generated_reply",
        "intent",
        "expected_action",
        "notes",
    ]
    # Ensure all required columns exist in proper order
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    save_df = df[cols].copy()
    save_df.to_csv(GOLDEN_PATH, index=False)


# --- Sidebar: Progress & Validation ---
st.sidebar.title("Annotation Tool")
st.sidebar.markdown(f"**Target File:** `data/golden/golden_set.csv`")
st.sidebar.markdown("---")

# Annotation Progress Calculation
completed_mask = (df["intent"].str.strip() != "") & (df["expected_action"].str.strip() != "")
completed_count = int(completed_mask.sum())
progress_ratio = completed_count / total_rows if total_rows > 0 else 0.0

st.sidebar.subheader("Progress")
st.sidebar.markdown(f"**Completed:** `{completed_count}` / `{total_rows}` ({progress_ratio:.1%})")
st.sidebar.progress(progress_ratio)

# Quick Jump to Next Unannotated
if st.sidebar.button("⏩ Jump to Next Unannotated", use_container_width=True):
    unannotated_indices = df[~completed_mask].index.tolist()
    if unannotated_indices:
        st.session_state["current_idx"] = unannotated_indices[0]
        st.rerun()
    else:
        st.sidebar.success("All examples have been annotated!")

st.sidebar.markdown("---")
st.sidebar.subheader("Navigation")

# Direct jump dropdown
jump_target = st.sidebar.selectbox(
    "Jump to Example #",
    options=list(range(1, total_rows + 1)),
    index=st.session_state["current_idx"],
)
if jump_target - 1 != st.session_state["current_idx"]:
    st.session_state["current_idx"] = jump_target - 1
    st.rerun()

st.sidebar.markdown("---")

# --- Validation Checker (Requirement 12) ---
st.sidebar.subheader("Validation Suite")
with st.sidebar.expander("Run Validation Checks", expanded=True):
    # Check 1: Exactly 200 rows
    row_check = len(df) == 200
    if row_check:
        st.markdown("✅ **Row Count:** Exactly 200 rows")
    else:
        st.markdown(f"❌ **Row Count:** Found {len(df)} rows (expected 200)")

    # Check 2: No duplicate tweet IDs
    dup_count = df["tweet_id"].duplicated().sum()
    if dup_count == 0:
        st.markdown("✅ **Unique IDs:** No duplicate tweet IDs")
    else:
        st.markdown(f"❌ **Duplicate IDs:** {dup_count} duplicates detected")

    # Check 3: Intent taxonomy adherence
    annotated_intents = df[df["intent"].str.strip() != ""]["intent"]
    invalid_intents = [i for i in annotated_intents if i not in taxonomy_intents]
    if not invalid_intents:
        st.markdown(f"✅ **Taxonomy Check:** All {len(annotated_intents)} labeled intents match taxonomy")
    else:
        st.markdown(f"❌ **Taxonomy Error:** {len(invalid_intents)} invalid intents found")

    # Check 4: Expected Action validity
    annotated_actions = df[df["expected_action"].str.strip() != ""]["expected_action"]
    invalid_actions = [a for a in annotated_actions if a not in ["AUTO_HANDLE", "ESCALATE"]]
    if not invalid_actions:
        st.markdown(f"✅ **Action Check:** All {len(annotated_actions)} labeled actions are valid")
    else:
        st.markdown(f"❌ **Action Error:** {len(invalid_actions)} invalid actions found")

    if completed_count == 200 and row_check and dup_count == 0 and not invalid_intents and not invalid_actions:
        st.success("🎉 Golden set is 100% annotated and fully valid!")


# --- Main Annotation View ---
st.title("SupportIQ — Golden Set Annotation")
st.caption("Human annotation workspace for the 200-example golden evaluation benchmark")
st.markdown("---")

current_idx = st.session_state["current_idx"]
row = df.iloc[current_idx]

# Header Row: Example Index and Status
col_meta1, col_meta2 = st.columns([3, 1])
with col_meta1:
    st.subheader(f"Example {current_idx + 1} of {total_rows} — Tweet ID: `{row['tweet_id']}`")
with col_meta2:
    is_completed = (row["intent"].strip() != "") and (row["expected_action"].strip() != "")
    if is_completed:
        st.success("Status: Completed")
    else:
        st.warning("Status: Pending Annotation")

# Display Customer Message
st.markdown("#### 👤 Customer Message")
st.info(row["customer_message"])

# Display Historical Brand Response
st.markdown("#### 🍎 Historical AppleSupport Response")
brand_reply_text = row["brand_response"] if row["brand_response"].strip() else "*[No response text recorded]*"
st.code(brand_reply_text, language="markdown")

st.markdown("---")
st.markdown("### ✍️ Label Assignment")

# Options setup
intent_options = ["-- Select Intent --"] + taxonomy_intents
current_intent = row["intent"].strip()
if current_intent in taxonomy_intents:
    intent_default_idx = intent_options.index(current_intent)
else:
    intent_default_idx = 0

action_options = ["-- Select Expected Action --", "AUTO_HANDLE", "ESCALATE"]
current_action = row["expected_action"].strip()
if current_action in ["AUTO_HANDLE", "ESCALATE"]:
    action_default_idx = action_options.index(current_action)
else:
    action_default_idx = 0

col_inp1, col_inp2 = st.columns(2)

with col_inp1:
    selected_intent = st.selectbox(
        "Intent (Required)",
        options=intent_options,
        index=intent_default_idx,
        key=f"intent_select_{current_idx}",
        help="Select the specific support problem class from the official 11-intent taxonomy."
    )

with col_inp2:
    selected_action = st.selectbox(
        "Expected Policy Action (Required)",
        options=action_options,
        index=action_default_idx,
        key=f"action_select_{current_idx}",
        help="AUTO_HANDLE: standard queries resolvable via safe RAG. ESCALATE: sensitive, ungrounded, or security/account issues."
    )

notes_val = st.text_input(
    "Notes (Optional rationale or edge-case context)",
    value=row.get("notes", ""),
    key=f"notes_input_{current_idx}",
    placeholder="e.g., Edge case: customer mentions cracked screen and AppleCare warranty",
)

st.markdown(" ")

# Button Controls
col_prev, col_save, col_next = st.columns([1, 2, 1])

with col_prev:
    prev_clicked = st.button("⬅️ Previous", use_container_width=True, disabled=(current_idx == 0))

with col_save:
    save_clicked = st.button("💾 Save & Next", type="primary", use_container_width=True)

with col_next:
    next_clicked = st.button("Next (Skip) ➡️", use_container_width=True, disabled=(current_idx == total_rows - 1))

# Handle Previous Button
if prev_clicked:
    if current_idx > 0:
        st.session_state["current_idx"] = current_idx - 1
        st.rerun()

# Handle Next (Skip) Button
if next_clicked:
    if current_idx < total_rows - 1:
        st.session_state["current_idx"] = current_idx + 1
        st.rerun()

# Handle Save & Next Button
if save_clicked:
    # Validation
    if selected_intent == "-- Select Intent --":
        st.error("Please select a valid Intent from the dropdown.")
    elif selected_action == "-- Select Expected Action --":
        st.error("Please select an Expected Action ('AUTO_HANDLE' or 'ESCALATE').")
    else:
        # Update in-memory state
        df.at[current_idx, "intent"] = selected_intent
        df.at[current_idx, "expected_action"] = selected_action
        df.at[current_idx, "notes"] = notes_val.strip()

        # Persist directly to disk
        save_dataset_to_disk()
        st.toast(f"Example {current_idx + 1} saved successfully!")

        # Advance to next example if available
        if current_idx < total_rows - 1:
            st.session_state["current_idx"] = current_idx + 1
        st.rerun()
