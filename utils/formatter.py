import pandas as pd
from datetime import datetime

# Fallback nama bulan manual
bulan_id = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

def format_tanggal_indo(tanggal_iso):
    try:
        dt = pd.to_datetime(tanggal_iso)
        return f"{dt.day} {bulan_id[dt.month]} {dt.year}"
    except:
        return "-"
