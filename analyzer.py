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
        "What is the best performing campaign?",
        "Which campaign has the highest click-through rate (CTR)?",
        "Show campaigns with the lowest conversion rate.",
        "What is the average cost per click (CPC)?",
        "Compare performance across platforms.",
        "Which campaign had the most impressions?",
        "What is the overall ROI?",
        "List underperforming campaigns.",
        "What is the total ad spend?",
        "Break down performance by device type.",
        "Which day had the highest engagement?",
        "Show trends over time.",
        "What are the top 5 campaigns by revenue?",
        "Compare engagement between genders (if available).",
        "Which regions performed best?"
    ]
