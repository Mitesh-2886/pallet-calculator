import streamlit as st
import pandas as pd
from fpdf import FPDF

# ---------- પેજ સેટિંગ ----------
st.set_page_config(page_title="પેલેટ બોક્સ કેલ્ક્યુલેટર", page_icon="📦", layout="wide")

st.title("📦 પેલેટ બોક્સ કેલ્ક્યુલેટર")

# ---------- પ્રોડક્ટ ડેટા ----------
product_data = [
    {"code": "BTRBP06", "name": "Amul Butter 15 Kg Bulk Pack", "pallet": 55},
    {"code": "BTRCP01", "name": "Amul Butter 150x100 Gm", "pallet": 54},
    {"code": "BTRCP02", "name": "Amul Butter 30x500 Gm CP", "pallet": 60},
    {"code": "BTRCP03", "name": "Amul Butter 36x400 Gm Tin", "pallet": 36},
    {"code": "BTRCP04", "name": "Amul Butter 10x125x8g Institutional Pack", "pallet": 33},
    {"code": "BTRCP16", "name": "Amul Butter 16x50x20 gm", "pallet": 52},
    {"code": "BTRCP17", "name": "Amul Butter 100x10x10 g", "pallet": 36},
    {"code": "BTRCP18", "name": "Amul Butter School Pack 60x10x10 Gm", "pallet": 36},
    {"code": "BTRCP19", "name": "Amul Butter 36x400 Gm Tin (Civil)", "pallet": 40},
    {"code": "BTRCP20", "name": "Amul Butter 8x8x200 Gm Tub", "pallet": 36},
    {"code": "BTRIP05", "name": "AMUL BUTTER 40X500 GM IP", "pallet": 44},
    {"code": "EXBTRCP08", "name": "Amul Butter Salted 100x100 Gm", "pallet": 78},
    {"code": "EXBTRCP09", "name": "Amul Butter Salted 20 x 500 Gm", "pallet": 88},
    {"code": "EXBTRCP11", "name": "Amul Butter Unsalted 100 x 100 Gm", "pallet": 78},
    {"code": "EXBTRCP12", "name": "Amul Butter Unsalted 20 x 500 Gm", "pallet": 88},
    {"code": "EXBTRCP17", "name": "Amul Butter Salted 10 x 100 x 10 Gm", "pallet": 36},
    {"code": "EXBTRCP18", "name": "Amul Butter School Pack 60x10x10 Gm", "pallet": 30},
    {"code": "EXPLWBCP02", "name": "Amul Lactic Butter 500 gm", "pallet": 88},
    {"code": "EXPUSBATRCP11", "name": "AMUL WATER BUFFALO&COW MILK PAST.UNSBUT1-100*100", "pallet": 78},
    {"code": "EXPUSBATRCP12", "name": "AMUL WATER BUFFALO&COW MILK PAST.UNSBUT5-20*500gm", "pallet": 88},
    {"code": "EXPUSBATRCP13", "name": "AMUL WATER BUFFALO&COW MILK PAST.BUTTER1-100*100gm", "pallet": 78},
    {"code": "EXPUSBATRCP14", "name": "AMUL WATER BUFFALO&COW MILK PAST.BUTTER5-20*500gm", "pallet": 88},
    {"code": "EXPUSBATRCP18", "name": "AMUL WATER BUFFALO&COW MILK PAST.BUTTER60-10*10gm", "pallet": 36},
    {"code": "EXPALWBCP02", "name": "AMUL PAST.WATER BUFFALO MILK LACT BUTTERS", "pallet": 88},
    {"code": "LWBCP01", "name": "Amul Safed Makhkhan 150x100g", "pallet": 54},
    {"code": "LWBCP02", "name": "Amul Safed Makhkhan 30x500g", "pallet": 60},
    {"code": "WBTBP01", "name": "White Butter 15 Kg Carton", "pallet": 55},
    {"code": "WBTBP05", "name": "Cow Butter 15 Kg Carton", "pallet": 55},
]

product_names = [f"{p['code']} - {p['name']}" for p in product_data]

# ---------- Session State ----------
if "products" not in st.session_state:
    st.session_state.products = []

# ---------- PDF બનાવવાનું ફંક્શન ----------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Arial ફોન્ટ (Windows માં હંમેશા હોય છે)
    try:
        pdf.add_font("Arial", "", "C:/Windows/Fonts/arial.ttf", uni=True)
        pdf.set_font("Arial", size=14)
    except Exception:
        pdf.set_font("Helvetica", size=14)
    
    # ટાઈટલ
    pdf.set_font_size(18)
    pdf.cell(0, 12, "Pallet Box Calculator", ln=True, align="C")
    pdf.ln(5)
    
    # ટેબલ હેડર
    pdf.set_font_size(11)
    pdf.set_fill_color(26, 35, 126)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(15, 10, "Sr", 1, 0, "C", True)
    pdf.cell(90, 10, "Product Name", 1, 0, "C", True)
    pdf.cell(30, 10, "Pallet", 1, 0, "C", True)
    pdf.cell(25, 10, "Box", 1, 1, "C", True)
    
    pdf.set_text_color(0, 0, 0)
    
    counter = 1
    grand_target = 0
    grand_filled = 0
    
    for product in st.session_state.products:
        pdf.set_font_size(11)
        pdf.set_fill_color(230, 235, 255)
        pdf.cell(0, 10, f"{product['code']} - {product['name'][:40]}  (Target: {product['target']})",
                 1, 1, "L", True)
        
        pdf.set_font_size(10)
        section_total = 0
        for row in product["rows"]:
            pdf.cell(15, 8, str(counter), 1, 0, "C")
            pdf.cell(90, 8, product["name"][:50], 1, 0, "L")
            pdf.cell(30, 8, str(product["pallet"]), 1, 0, "C")
            pdf.cell(25, 8, str(row["box"]), 1, 1, "C")
            section_total += row["box"]
            counter += 1
        
        pdf.set_font_size(11)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(135, 8, "Product Total:", 1, 0, "R", True)
        pdf.cell(25, 8, str(section_total), 1, 1, "C", True)
        pdf.ln(3)
        
        grand_target += product["target"]
        grand_filled += section_total
    
    # ગ્રાન્ડ ટોટલ
    pdf.ln(5)
    pdf.set_font_size(13)
    pdf.set_fill_color(255, 235, 59)
    remaining = grand_target - grand_filled
    pdf.cell(0, 10,
             f"Grand Target: {grand_target}  |  Filled: {grand_filled}  |  Remaining: {remaining}",
             1, 1, "C", True)
    
    return bytes(pdf.output())

# ---------- પ્રોડક્ટ ઉમેરવાનું ફોર્મ ----------
st.subheader("➕ નવી પ્રોડક્ટ ઉમેરો")

col1, col2 = st.columns([3, 1])
with col1:
    selected = st.selectbox("પ્રોડક્ટ પસંદ કરો", ["-- પ્રોડક્ટ પસંદ કરો --"] + product_names)

with col2:
    st.write("")
    st.write("")
    if st.button("પ્રોડક્ટ ઉમેરો", use_container_width=True):
        if selected != "-- પ્રોડક્ટ પસંદ કરો --":
            idx = product_names.index(selected)
            new_product = {
                "name": product_data[idx]["name"],
                "code": product_data[idx]["code"],
                "pallet": product_data[idx]["pallet"],
                "target": 600,
                "rows": [{"box": 0}]
            }
            st.session_state.products.append(new_product)
            st.rerun()
        else:
            st.warning("કૃપા કરીને પ્રોડક્ટ પસંદ કરો!")

st.divider()

# ---------- દરેક પ્રોડક્ટનું સેક્શન ----------
grand_target = 0
grand_filled = 0

for p_idx, product in enumerate(st.session_state.products):
    with st.container(border=True):
        head_col1, head_col2 = st.columns([3, 1])
        with head_col1:
            st.markdown(f"### 📋 {product['code']} - {product['name']}")
        with head_col2:
            new_target = st.number_input(
                "🎯 ટાર્ગેટ:",
                min_value=1,
                value=product["target"],
                key=f"target_{p_idx}",
                step=1
            )
            product["target"] = new_target

        h1, h2, h3, h4, h5 = st.columns([0.5, 3, 1, 1, 1.5])
        h1.markdown("**ક્રમ**")
        h2.markdown("**પ્રોડક્ટ નામ**")
        h3.markdown("**પેલેટ પ્રતિ બોક્સ**")
        h4.markdown("**બોક્સ**")
        h5.markdown("**ક્રિયા**")

        rows_to_delete = []
        for r_idx, row in enumerate(product["rows"]):
            c1, c2, c3, c4, c5 = st.columns([0.5, 3, 1, 1, 1.5])
            c1.write(f"{r_idx + 1}")
            c2.write(product["name"])
            c3.write(f"{product['pallet']}")
            box_val = c4.number_input(
                "બોક્સ",
                min_value=0,
                value=row["box"],
                key=f"box_{p_idx}_{r_idx}",
                label_visibility="collapsed"
            )
            product["rows"][r_idx]["box"] = box_val

            b1, b2 = c5.columns(2)
            if b1.button("➕", key=f"add_{p_idx}_{r_idx}", help="આ જ પ્રોડક્ટની નવી લાઈન ઉમેરો"):
                product["rows"].append({"box": 0})
                st.rerun()
            if b2.button("✕", key=f"del_{p_idx}_{r_idx}", help="લાઈન ડિલીટ કરો"):
                rows_to_delete.append(r_idx)

        if rows_to_delete:
            for idx in sorted(rows_to_delete, reverse=True):
                del product["rows"][idx]
            st.rerun()

        section_total = sum(r["box"] for r in product["rows"])
        grand_target += product["target"]
        grand_filled += section_total

        st.markdown("---")
        tot_col1, tot_col2 = st.columns([3, 1])
        with tot_col2:
            if section_total > product["target"]:
                st.error(f"**પ્રોડક્ટ સરવાળો: {section_total}** ⚠️ ટાર્ગેટ કરતાં વધુ!")
            else:
                st.success(f"**પ્રોડક્ટ સરવાળો: {section_total}**")

# ---------- ગ્રાન્ડ ટોટલ ----------
st.divider()
st.subheader("📊 ગ્રાન્ડ ટોટલ")

g1, g2, g3 = st.columns(3)
g1.metric("કુલ ટાર્ગેટ", grand_target)
g2.metric("કુલ ભરેલા બોક્સ", grand_filled)
remaining = grand_target - grand_filled
g3.metric("બાકી", remaining)

# ---------- CSV ડાઉનલોડ ----------
if st.session_state.products:
    csv_rows = []
    counter = 1
    for product in st.session_state.products:
        for row in product["rows"]:
            csv_rows.append({
                "ક્રમ": counter,
                "પ્રોડક્ટ કોડ": product["code"],
                "પ્રોડક્ટ નામ": product["name"],
                "પેલેટ પ્રતિ બોક્સ": product["pallet"],
                "બોક્સ": row["box"],
                "પ્રોડક્ટ ટાર્ગેટ": product["target"]
            })
            counter += 1

    df = pd.DataFrame(csv_rows)
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📊 CSV ડાઉનલોડ કરો",
        data=csv,
        file_name="pallet_data.csv",
        mime="text/csv"
    )

# ---------- PDF ડાઉનલોડ ----------
if st.session_state.products:
    try:
        pdf_bytes = generate_pdf()
        st.download_button(
            label="📄 PDF ડાઉનલોડ કરો (પ્રિન્ટ માટે)",
            data=pdf_bytes,
            file_name="pallet_report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"PDF error: {e}")

# ---------- રીસેટ બટન ----------
if st.button("🔄 રીસેટ કરો"):
    st.session_state.products = []
    st.rerun()