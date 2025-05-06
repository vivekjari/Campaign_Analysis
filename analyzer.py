from metric_mapper import infer_metrics

def analyze_dataset(df):
    # Attempt to infer the column mappings dynamically
    mapping, df = infer_metrics(df)
    insights = []

    try:
        # Clicks and Impressions (Check if they exist in the inferred mapping)
        clicks = df[mapping.get("Clicks", "clicks")]
        impressions = df[mapping.get("Impressions", "impressions")]
        df["CTR"] = clicks / impressions.replace(0, 1)
        insights.append(f"CTR: {df['CTR'].mean():.2%}")
    except KeyError:
        insights.append("CTR could not be calculated because 'Clicks' or 'Impressions' columns are missing.")

    try:
        # Spend and CPC (Check if columns exist for Spend and Clicks)
        spend = df[mapping.get("Spend", "spend")]
        df["CPC"] = spend / df[mapping.get("Clicks", "clicks")].replace(0, 1)
        insights.append(f"CPC: ₹{df['CPC'].mean():.2f}")
    except KeyError:
        insights.append("CPC could not be calculated because 'Spend' or 'Clicks' columns are missing.")

    try:
        # CPM (Cost per 1000 Impressions)
        df["CPM"] = df[mapping.get("Spend", "spend")] / df[mapping.get("Impressions", "impressions")].replace(0, 1) * 1000
        insights.append(f"CPM: ₹{df['CPM'].mean():.2f}")
    except KeyError:
        insights.append("CPM could not be calculated because 'Spend' or 'Impressions' columns are missing.")

    # Dynamic Campaign Column Handling (Check if 'ad_grp_name' or 'campaign' exists)
    campaign_column = mapping.get("Campaign", None)
    if not campaign_column:
        if 'ad_grp_name' in df.columns:
            campaign_column = 'ad_grp_name'
        elif 'campaign' in df.columns:
            campaign_column = 'campaign'

    if campaign_column:
        try:
            insights.append(f"Top CTR Campaigns: {df.sort_values('CTR', ascending=False).head(3)[campaign_column]}")
        except KeyError:
            insights.append("Top CTR Campaigns could not be listed due to missing data.")
    else:
        insights.append("No valid campaign column found to display top CTR campaigns.")

    return insights, [
        "Which platform or audience group is converting the best?",
        "Are there signs of ad fatigue based on date trends?",
        "What should I do to reduce my CPC or increase ROI?"
    ]
