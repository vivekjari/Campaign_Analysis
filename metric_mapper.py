def infer_metrics(df):
    mapping = {}
    event_col = None

    for col in df.columns:
        col_l = col.lower()

        if any(k in col_l for k in ["click"]):
            mapping["Clicks"] = col
        elif any(k in col_l for k in ["impression", "view"]):
            mapping["Impressions"] = col
        elif any(k in col_l for k in ["spend", "cost", "budget"]):
            mapping["Spend"] = col
        elif "campaign" in col_l:
            mapping["Campaign"] = col

        if any(k in col_l for k in ["event", "action", "type"]):
            event_col = col

    if event_col:
        df["derived_clicks"] = df[event_col].apply(lambda x: 1 if "click" in str(x).lower() else 0)
        df["derived_impressions"] = df[event_col].apply(lambda x: 1 if "impression" in str(x).lower() else 0)
        mapping.setdefault("Clicks", "derived_clicks")
        mapping.setdefault("Impressions", "derived_impressions")

    return mapping, df