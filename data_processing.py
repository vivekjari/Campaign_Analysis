import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.metrics import mean_squared_error

# Function to detect column roles (for example, spending, impressions, etc.)
def detect_column_roles(df):
    columns = df.columns
    column_roles = {
        "spend": None,
        "impressions": None,
        "clicks": None,
        "conversions": None,
        "engagement": None,
        "ad_text": None,
        "date": None,
        "campaign_name": None,
        "ctr": None,  # Click-Through Rate
        "cvr": None   # Conversion Rate
    }
    
    for col in columns:
        if "spend" in col.lower():
            column_roles["spend"] = col
        elif "impressions" in col.lower():
            column_roles["impressions"] = col
        elif "clicks" in col.lower():
            column_roles["clicks"] = col
        elif "conversions" in col.lower():
            column_roles["conversions"] = col
        elif "engagement" in col.lower():
            column_roles["engagement"] = col
        elif "ad_text" in col.lower():
            column_roles["ad_text"] = col
        elif "date" in col.lower():
            column_roles["date"] = col
        elif "campaign" in col.lower():
            column_roles["campaign_name"] = col

    return column_roles

# Function to perform sentiment analysis on the ad text
def sentiment_analysis(df, ad_text_column):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []
    
    for text in df[ad_text_column]:
        score = analyzer.polarity_scores(str(text))["compound"]
        sentiment_scores.append(score)

    return sentiment_scores

# Function to calculate CTR and CVR
def calculate_ctr_and_cvr(df, col_roles):
    df["ctr"] = df[col_roles["clicks"]] / df[col_roles["impressions"]] * 100
    df["cvr"] = df[col_roles["conversions"]] / df[col_roles["clicks"]] * 100

    return df

# Function to generate insights based on the provided data
def generate_insights(df):
    column_roles = detect_column_roles(df)
    
    # Extracting necessary columns
    ad_text_column = column_roles["ad_text"]
    date_column = column_roles["date"]
    
    # Apply sentiment analysis
    sentiment_scores = sentiment_analysis(df, ad_text_column)
    df["sentiment"] = sentiment_scores

    # Calculate CTR and CVR
    df = calculate_ctr_and_cvr(df, column_roles)
    
    # Example analysis: Conversion Trend Analysis
    df[date_column] = pd.to_datetime(df[date_column])
    df_grouped = df.groupby(df[date_column].dt.date).agg({"conversions": "sum", "impressions": "sum"}).reset_index()
    df_grouped["conversion_rate"] = df_grouped["conversions"] / df_grouped["impressions"] * 100

    # Example regression analysis for predicting future trends
    model = LinearRegression()
    df_grouped["days_since_start"] = (df_grouped[date_column] - df_grouped[date_column].min()).dt.days
    X = df_grouped[["days_since_start"]]
    y = df_grouped["conversion_rate"]
    model.fit(X, y)
    predictions = model.predict(X)

    # Prepare the result
    insights = {
        "total_conversions": df["conversions"].sum(),
        "total_impressions": df["impressions"].sum(),
        "total_spend": df["spend"].sum(),
        "average_ctr": df["ctr"].mean(),
        "average_cvr": df["cvr"].mean(),
        "conversion_rate_trend": df_grouped[["date", "conversion_rate"]].to_dict(orient="records"),
        "predictions": predictions.tolist(),
        "model_coefficients": model.coef_.tolist(),
        "sentiment_distribution": df["sentiment"].describe().to_dict()
    }

    return insights

