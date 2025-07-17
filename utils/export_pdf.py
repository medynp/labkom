from fpdf import FPDF
import tempfile

def export_riwayat_to_pdf(df_filtered):
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Riwayat Penggunaan Laboratorium", ln=True, align="C")
    pdf.ln(5)

    # Header dan kolom yang ingin ditampilkan
    headers = [
        "Laboratorium",
        "Guru Pendamping",
        "Tanggal Mulai",
        "Tanggal Selesai",
        "Kondisi Setelah",
        "Catatan"
    ]
    available_headers = [h for h in headers if h in df_filtered.columns]

    # Hitung lebar kolom otomatis
    col_widths = []
    for col in available_headers:
        max_len = max(df_filtered[col].astype(str).map(len).max(), len(col))
        col_widths.append(min(max_len * 2.5, 60))

    total_width = sum(col_widths)
    page_width = pdf.w - 2 * pdf.l_margin
    x_start = (page_width - total_width) / 2 + pdf.l_margin  # Tengah horizontal

    # Header
    pdf.set_font("Arial", "B", 10)
    pdf.set_x(x_start)
    for header, w in zip(available_headers, col_widths):
        pdf.cell(w, 10, header, border=1)
    pdf.ln()

    # Data rows
    pdf.set_font("Arial", "", 9)
    for _, row in df_filtered.iterrows():
        pdf.set_x(x_start)
        for header, w in zip(available_headers, col_widths):
            value = str(row.get(header, "-"))
            pdf.cell(w, 8, value, border=1)
        pdf.ln()

    # Simpan file sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name
