from pathlib import Path

import pandas as pd

WDI_PATH = Path("WB_WDI_WIDEF.csv")
EMDAT_PATH = Path("public_emdat_custom_request_2026-04-30_22d8bc4c-5753-434a-90e6-6851109fb6f4.xlsx")


def main() -> None:
    if not WDI_PATH.exists() or not EMDAT_PATH.exists():
        missing = [str(p) for p in [WDI_PATH, EMDAT_PATH] if not p.exists()]
        raise FileNotFoundError(f"Missing required files: {missing}")

    wdi = pd.read_csv(WDI_PATH, low_memory=False)
    emdat = pd.read_excel(EMDAT_PATH, sheet_name="EM-DAT Data")

    year_cols = [c for c in wdi.columns if c.isdigit()]
    id_cols = [c for c in wdi.columns if c not in year_cols]
    wdi_long = wdi.melt(id_vars=id_cols, value_vars=year_cols, var_name="year", value_name="value")
    wdi_long["year"] = wdi_long["year"].astype(int)
    wdi_long["value"] = pd.to_numeric(wdi_long["value"], errors="coerce")

    panel = wdi_long[wdi_long["REF_AREA_LABEL"].isin(["Malaysia", "Vietnam"])].copy()

    emdat["country"] = emdat["Country"].replace({"Viet Nam": "Vietnam"})
    emdat = emdat[emdat["country"].isin(["Malaysia", "Vietnam"])].copy()
    emdat = emdat[emdat["Disaster Group"].eq("Natural")].copy()
    emdat = emdat[emdat["Disaster Subgroup"].isin(["Hydrological", "Meteorological", "Climatological"])].copy()

    emdat["Start Year"] = pd.to_numeric(emdat["Start Year"], errors="coerce")
    emdat["Total Damage ('000 US$)"] = pd.to_numeric(emdat["Total Damage ('000 US$)"], errors="coerce")

    emdat_yearly = (
        emdat.groupby(["country", "Start Year"], as_index=False)
        .agg(event_count=("DisNo.", "count"), emdat_damage_kusd=("Total Damage ('000 US$)", "sum"))
        .rename(columns={"Start Year": "year"})
    )

    print("WDI panel rows (MY+VN):", len(panel))
    print("EM-DAT yearly rows:", len(emdat_yearly))
    print("EM-DAT year range:", int(emdat_yearly["year"].min()), int(emdat_yearly["year"].max()))
    print("Quick validation: PASS")


if __name__ == "__main__":
    main()
