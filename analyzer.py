from metric_mapper import infer_metrics

def analyze_dataset(df):
    mapping, df = infer_metrics(df)
    insights = []

    try:
        clicks = df[mapping["Clicks"]]
        impressions = df[mapping["Impressions"]]
        df["CTR"] = clicks / impressions.replace(0, 1)
        insights.append(f"CTR: {df['CTR'].mean():.2%}")
    except: pass

    try:
        spend = df[mapping["Spend"]]
        df["CPC"] = spend / df[mapping["Clicks"]].replace(0, 1)
        insights.append(f"CPC: ₹{df['CPC'].mean():.2f}")
    except: pass

    try:
        df["CPM"] = df[mapping["Spend"]] / df[mapping["Impressions"]].replace(0, 1) * 1000
        insights.append(f"CPM: ₹{df['CPM'].mean():.2f}")
    except: pass

    if "CTR" in df:
        insights.append(f"Top CTR Campaigns: {df.sort_values('CTR', ascending=False).head(3)[mapping['Campaign']]}")
    
    return insights, [
        "Which platform or audience group is converting the best?",
        "Are there signs of ad fatigue based on date trends?",
        "What should I do to reduce my CPC or increase ROI?"
    ]