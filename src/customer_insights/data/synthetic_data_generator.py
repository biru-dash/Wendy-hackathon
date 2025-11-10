"""Generate synthetic customer insights data for BigQuery"""
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

import pandas as pd

# Segment definitions
SEGMENTS = [
    "value-driven-lunch-buyer",
    "discount-hunter",
    "loyal-repeater",
    "convenience-driven",
    "premium-seeker",
    "weekend-splurger",
]

OFFER_TYPES = ["BOGO", "Percentage Off", "Free Item", "Bundle Deal", "Time-Boxed", "App Exclusive"]
CHANNELS = ["app", "web", "in-store", "drive-thru"]
MENU_ITEMS = ["Baconator", "Spicy Chicken Sandwich", "Frosty", "Fries", "Nuggets", "Salad"]
PAYMENT_METHODS = ["credit_card", "debit_card", "mobile_pay", "cash"]

def generate_crm_data(num_customers: int = 1000) -> List[Dict[str, Any]]:
    """Generate synthetic CRM and loyalty data"""
    data = []
    
    for i in range(num_customers):
        segment = random.choice(SEGMENTS)
        customer_id = f"customer_{i+1:04d}"
        
        # Generate visit patterns based on segment
        if segment == "value-driven-lunch-buyer":
            avg_visits_per_month = random.randint(8, 15)
            avg_spend_per_visit = round(random.uniform(8.00, 14.00), 2)
            preferred_time = "lunch"
        elif segment == "discount-hunter":
            avg_visits_per_month = random.randint(12, 20)
            avg_spend_per_visit = round(random.uniform(5.00, 10.00), 2)
            preferred_time = "any"
        elif segment == "loyal-repeater":
            avg_visits_per_month = random.randint(15, 25)
            avg_spend_per_visit = round(random.uniform(10.00, 16.00), 2)
            preferred_time = "dinner"
        elif segment == "convenience-driven":
            avg_visits_per_month = random.randint(6, 12)
            avg_spend_per_visit = round(random.uniform(9.00, 13.00), 2)
            preferred_time = "lunch"
        else:
            avg_visits_per_month = random.randint(5, 15)
            avg_spend_per_visit = round(random.uniform(7.00, 15.00), 2)
            preferred_time = random.choice(["lunch", "dinner", "breakfast"])
        
        # Generate last 3 months of visits
        base_date = datetime.now() - timedelta(days=90)
        for month_offset in range(3):
            month_start = base_date + timedelta(days=30 * month_offset)
            num_visits = random.randint(
                int(avg_visits_per_month * 0.7), 
                int(avg_visits_per_month * 1.3)
            )
            
            for visit_num in range(num_visits):
                visit_date = month_start + timedelta(
                    days=random.randint(0, 29),
                    hours=random.randint(8, 20)
                )
                
                data.append({
                    "customer_id": customer_id,
                    "segment_id": segment,
                    "visit_date": visit_date.isoformat(),
                    "spend": round(random.uniform(
                        avg_spend_per_visit * 0.7,
                        avg_spend_per_visit * 1.3
                    ), 2),
                    "channel": random.choice(CHANNELS),
                    "preferred_time": preferred_time,
                    "total_lifetime_visits": avg_visits_per_month * random.randint(6, 24),
                    "total_lifetime_spend": round(
                        avg_spend_per_visit * avg_visits_per_month * random.randint(6, 24),
                        2
                    ),
                })
    
    return data


def generate_redemption_logs(num_redemptions: int = 5000) -> List[Dict[str, Any]]:
    """Generate synthetic redemption log data"""
    data = []
    
    # Generate redemptions over last 6 months
    base_date = datetime.now() - timedelta(days=180)
    
    for i in range(num_redemptions):
        offer_type = random.choice(OFFER_TYPES)
        segment = random.choice(SEGMENTS)
        customer_id = f"customer_{random.randint(1, 1000):04d}"
        
        # Calculate lift based on offer type and segment
        base_lift = 1.0
        
        if offer_type == "BOGO" and segment == "value-driven-lunch-buyer":
            base_lift = random.uniform(2.0, 2.8)
        elif offer_type == "Time-Boxed" and segment == "convenience-driven":
            base_lift = random.uniform(1.8, 2.5)
        elif offer_type == "App Exclusive" and segment in ["value-driven-lunch-buyer", "convenience-driven"]:
            base_lift = random.uniform(1.9, 2.6)
        elif segment == "discount-hunter":
            base_lift = random.uniform(1.5, 2.2)
        else:
            base_lift = random.uniform(1.2, 1.8)
        
        # Channel preference
        if segment == "convenience-driven":
            channel = "app" if random.random() > 0.3 else random.choice(["web", "in-store"])
        elif segment == "value-driven-lunch-buyer":
            channel = "app" if random.random() > 0.2 else random.choice(["web", "drive-thru"])
        else:
            channel = random.choice(CHANNELS)
        
        redemption_date = base_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(8, 20)
        )
        
        # Time-boxed offers are more effective during specific hours
        is_time_boxed = offer_type == "Time-Boxed"
        if is_time_boxed:
            redemption_date = redemption_date.replace(
                hour=random.choice([11, 12, 13, 14])  # Lunch hours
            )
            base_lift *= 1.2  # Boost for time-boxed during lunch
        
        data.append({
            "redemption_id": f"redemption_{i+1:05d}",
            "customer_id": customer_id,
            "segment_id": segment,
            "offer_type": offer_type,
            "redemption_date": redemption_date.isoformat(),
            "channel": channel,
            "is_time_boxed": is_time_boxed,
            "is_app_exclusive": offer_type == "App Exclusive",
            "lift_multiplier": round(base_lift, 2),
            "redemption_value": round(random.uniform(5.00, 15.00), 2),
            "month": redemption_date.strftime("%Y-%m"),
            "day_of_week": redemption_date.strftime("%A"),
            "hour": redemption_date.hour,
        })
    
    return data


def generate_feedback_data(num_reviews: int = 2000) -> List[Dict[str, Any]]:
    """Generate synthetic feedback and review data"""
    data = []
    
    # Sentiment phrases by segment
    segment_phrases = {
        "value-driven-lunch-buyer": [
            "time-boxed", "app-exclusive", "quick redemption", "easy to use",
            "perfect for lunch break", "convenient", "no hassle"
        ],
        "discount-hunter": [
            "great deal", "saved money", "value", "worth it",
            "affordable", "discount", "budget-friendly"
        ],
        "convenience-driven": [
            "easy to use", "fast", "quick", "no hassle",
            "app makes it simple", "smooth process", "effortless"
        ],
        "loyal-repeater": [
            "always great", "consistent quality", "trustworthy",
            "reliable", "my go-to", "never disappoints"
        ],
    }
    
    offer_types = ["BOGO", "Percentage Off", "Free Item", "Time-Boxed", "App Exclusive"]
    base_date = datetime.now() - timedelta(days=90)
    
    for i in range(num_reviews):
        segment = random.choice(SEGMENTS)
        offer_type = random.choice(offer_types)
        customer_id = f"customer_{random.randint(1, 1000):04d}"
        
        # Generate sentiment score
        sentiment_score = random.uniform(0.6, 0.95)  # Mostly positive
        
        # Select relevant phrases
        phrases = segment_phrases.get(segment, ["good", "nice", "enjoyed"])
        selected_phrases = random.sample(phrases, k=min(len(phrases), random.randint(2, 4)))
        
        # Generate review text
        review_templates = [
            f"I {random.choice(['loved', 'appreciated', 'enjoyed'])} the {offer_type.lower()} offer. {random.choice(selected_phrases)}!",
            f"The {offer_type.lower()} was {selected_phrases[0]}. {selected_phrases[1] if len(selected_phrases) > 1 else 'Great experience!'}",
            f"Really {selected_phrases[0]} how {selected_phrases[1] if len(selected_phrases) > 1 else 'smooth'} the {offer_type.lower()} was.",
        ]
        
        review_text = random.choice(review_templates)
        
        # Add channel-specific feedback
        if offer_type == "App Exclusive":
            review_text += " The app made it so easy!"
        if offer_type == "Time-Boxed":
            review_text += " Perfect timing for my lunch break."
        
        feedback_date = base_date + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(8, 20)
        )
        
        data.append({
            "feedback_id": f"feedback_{i+1:05d}",
            "customer_id": customer_id,
            "segment_id": segment,
            "offer_type": offer_type,
            "feedback_date": feedback_date.isoformat(),
            "review_text": review_text,
            "sentiment_score": round(sentiment_score, 2),
            "key_phrases": selected_phrases,
            "channel": random.choice(CHANNELS),
            "source": random.choice(["app_review", "campaign_feedback", "social_comment", "survey"]),
        })
    
    return data


def generate_customer_transactions_raw(crm_df: pd.DataFrame, redemption_df: pd.DataFrame) -> pd.DataFrame:
    """Create raw transaction records derived from CRM visits."""
    transactions_df = crm_df.copy()
    transactions_df["transaction_date"] = pd.to_datetime(transactions_df["visit_date"])
    transactions_df["transaction_id"] = [
        f"txn_{i+1:07d}" for i in range(len(transactions_df))
    ]
    transactions_df["total_spend"] = transactions_df["spend"]

    offers_by_customer = redemption_df.groupby("customer_id")["offer_type"].apply(list).to_dict()

    def pick_offer(customer_id: str) -> str:
        offers = offers_by_customer.get(customer_id)
        if offers and random.random() < 0.65:
            return random.choice(offers)
        if random.random() < 0.25:
            return random.choice(OFFER_TYPES)
        return None

    transactions_df["redeemed_offer"] = transactions_df["customer_id"].apply(pick_offer)
    transactions_df["offer_type"] = transactions_df["redeemed_offer"].fillna(
        transactions_df["segment_id"].map(lambda _: random.choice(OFFER_TYPES))
    )
    transactions_df["payment_method"] = [
        random.choice(PAYMENT_METHODS) for _ in range(len(transactions_df))
    ]
    transactions_df["items"] = [
        random.sample(MENU_ITEMS, k=random.randint(1, min(3, len(MENU_ITEMS))))
        for _ in range(len(transactions_df))
    ]

    def determine_daypart(timestamp: pd.Timestamp) -> str:
        hour = timestamp.hour
        if 6 <= hour < 11:
            return "breakfast"
        if 11 <= hour < 15:
            return "lunch"
        if 15 <= hour < 18:
            return "afternoon"
        if 18 <= hour < 22:
            return "dinner"
        return "late-night"

    transactions_df["visit_daypart"] = transactions_df["transaction_date"].apply(determine_daypart)

    return transactions_df[
        [
            "transaction_id",
            "customer_id",
            "segment_id",
            "transaction_date",
            "total_spend",
            "channel",
            "redeemed_offer",
            "offer_type",
            "payment_method",
            "items",
            "visit_daypart",
        ]
    ]


def generate_customer_feedback_raw(feedback_df: pd.DataFrame) -> pd.DataFrame:
    """Create raw feedback verbatims with integer ratings."""
    feedback_raw = feedback_df.copy()
    feedback_raw["feedback_text"] = feedback_raw["review_text"]

    def derive_rating(sentiment_score: float) -> int:
        noisy_score = sentiment_score + random.uniform(-0.15, 0.15)
        rating = max(1, min(5, int(round(noisy_score * 5))))
        return rating

    feedback_raw["rating"] = feedback_raw["sentiment_score"].apply(derive_rating)

    return feedback_raw[
        [
            "feedback_id",
            "customer_id",
            "segment_id",
            "feedback_date",
            "rating",
            "feedback_text",
            "channel",
            "source",
        ]
    ]


def generate_customer_segments(
    crm_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
    redemption_df: pd.DataFrame,
    feedback_df: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate synthesized metrics by segment for initial seed data."""
    segments = []

    for segment in SEGMENTS:
        crm_segment = crm_df[crm_df["segment_id"] == segment]
        if crm_segment.empty:
            continue

        transactions_segment = transactions_df[transactions_df["segment_id"] == segment]
        redemption_segment = redemption_df[redemption_df["segment_id"] == segment]
        feedback_segment = feedback_df[feedback_df["segment_id"] == segment]

        visits_per_customer = (
            crm_segment.groupby("customer_id")["visit_date"].count().mean()
            if not crm_segment.empty
            else 0
        )
        avg_spend = crm_segment["spend"].mean() if not crm_segment.empty else 0
        transaction_count = len(transactions_segment) or 1
        redemption_rate = len(redemption_segment) / transaction_count
        lift_estimate = redemption_segment["lift_multiplier"].mean() if not redemption_segment.empty else 1.0

        top_channels = (
            crm_segment["channel"].value_counts().head(2).index.tolist()
            if "channel" in crm_segment
            else []
        )
        preferred_mechanics = (
            redemption_segment["offer_type"].value_counts().head(3).index.tolist()
            if not redemption_segment.empty
            else random.sample(OFFER_TYPES, k=3)
        )

        phrases = []
        if not feedback_segment.empty and "key_phrases" in feedback_segment:
            for value in feedback_segment["key_phrases"]:
                phrases.extend(value if isinstance(value, list) else [value])
        key_messaging_phrases = pd.Series(phrases).value_counts().head(5).index.tolist() if phrases else []

        description = (
            f"{segment.replace('-', ' ').title()} segment averaging ${avg_spend:0.2f} per visit "
            f"and {visits_per_customer:0.1f} visits per month."
        )

        empirical_metrics = {
            "avg_monthly_visits": round(visits_per_customer or 0, 1),
            "avg_spend": round(avg_spend or 0, 2),
            "segment_size": len(crm_segment["customer_id"].unique()),
            "top_channels": top_channels,
        }

        segments.append(
            {
                "segment_id": segment,
                "description": description,
                "preferred_mechanics": preferred_mechanics,
                "key_messaging_phrases": key_messaging_phrases,
                "redemption_rate": round(redemption_rate, 3),
                "lift_estimate": round(lift_estimate, 2),
                "empirical_metrics": json.dumps(empirical_metrics),
                "created_at": datetime.utcnow().isoformat(),
            }
        )

    return pd.DataFrame(segments)


def export_to_dataframes() -> Dict[str, pd.DataFrame]:
    """Generate all synthetic data and return as pandas DataFrames"""
    print("Generating synthetic CRM data...")
    crm_data = generate_crm_data(num_customers=1000)
    crm_df = pd.DataFrame(crm_data)
    
    print("Generating synthetic redemption logs...")
    redemption_data = generate_redemption_logs(num_redemptions=5000)
    redemption_df = pd.DataFrame(redemption_data)
    
    print("Generating synthetic feedback data...")
    feedback_data = generate_feedback_data(num_reviews=2000)
    feedback_df = pd.DataFrame(feedback_data)
    
    print("Deriving raw transaction records...")
    transactions_df = generate_customer_transactions_raw(crm_df, redemption_df)
    
    print("Deriving raw feedback verbatims...")
    feedback_raw_df = generate_customer_feedback_raw(feedback_df)
    
    print("Synthesizing baseline segment summaries...")
    segments_df = generate_customer_segments(crm_df, transactions_df, redemption_df, feedback_df)
    
    return {
        "crm_data": crm_df,
        "customer_transactions_raw": transactions_df,
        "redemption_logs": redemption_df,
        "feedback_data": feedback_df,
        "customer_feedback_raw": feedback_raw_df,
        "customer_segments": segments_df,
    }


if __name__ == "__main__":
    # Generate and preview data
    dataframes = export_to_dataframes()
    
    print("\n=== Data Summary ===")
    for name, df in dataframes.items():
        print(f"\n{name}:")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        print(f"\n  Sample data:")
        print(df.head(3).to_string())
