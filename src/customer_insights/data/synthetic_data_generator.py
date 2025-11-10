"""Generate synthetic customer insights data for BigQuery"""
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

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

REFERENCE_YEAR = 2025

TIME_PERIODS: Dict[str, Dict[str, datetime]] = {
    "2025-Q1": {"start": datetime(2025, 1, 1), "end": datetime(2025, 3, 31, 23, 59, 59)},
    "2025-Q2": {"start": datetime(2025, 4, 1), "end": datetime(2025, 6, 30, 23, 59, 59)},
    "2025-Q3": {"start": datetime(2025, 7, 1), "end": datetime(2025, 9, 30, 23, 59, 59)},
    "2025-Q4": {"start": datetime(2025, 10, 1), "end": datetime(2025, 12, 31, 23, 59, 59)},
}

DAYPART_HOURS: Dict[str, List[int]] = {
    "breakfast": list(range(6, 11)),
    "lunch": list(range(11, 15)),
    "afternoon": list(range(15, 18)),
    "dinner": list(range(18, 22)),
    "late-night": [22, 23, 0, 1, 2, 3, 4, 5],
}

DEFAULT_DAYPART_WEIGHTS = {
    "breakfast": 0.2,
    "lunch": 0.3,
    "afternoon": 0.15,
    "dinner": 0.2,
    "late-night": 0.15,
}

DEFAULT_TIME_PERIOD_WEIGHTS = {
    "2025-Q1": 0.3,
    "2025-Q2": 0.25,
    "2025-Q3": 0.25,
    "2025-Q4": 0.2,
}

DEFAULT_CHANNEL_WEIGHTS = {
    "app": 0.3,
    "web": 0.2,
    "in-store": 0.25,
    "drive-thru": 0.25,
}

DEFAULT_SEGMENT_WEIGHTS = {
    "value-driven-lunch-buyer": 0.2,
    "discount-hunter": 0.2,
    "loyal-repeater": 0.2,
    "convenience-driven": 0.2,
    "premium-seeker": 0.1,
    "weekend-splurger": 0.1,
}

GENERATION_CONFIGS = [
    {
        "name": "Gen Z",
        "weight": 0.32,
        "age_range": (18, 27),
        "segment_weights": {
            "value-driven-lunch-buyer": 0.28,
            "convenience-driven": 0.24,
            "discount-hunter": 0.18,
            "loyal-repeater": 0.16,
            "premium-seeker": 0.07,
            "weekend-splurger": 0.07,
        },
        "daypart_weights": {
            "breakfast": 0.42,
            "lunch": 0.33,
            "afternoon": 0.08,
            "dinner": 0.09,
            "late-night": 0.08,
        },
        "time_period_weights": {
            "2025-Q1": 0.55,
            "2025-Q2": 0.2,
            "2025-Q3": 0.15,
            "2025-Q4": 0.1,
        },
        "channel_weights": {
            "app": 0.5,
            "web": 0.18,
            "in-store": 0.17,
            "drive-thru": 0.15,
        },
    },
    {
        "name": "Millennial",
        "weight": 0.3,
        "age_range": (28, 43),
        "segment_weights": {
            "value-driven-lunch-buyer": 0.22,
            "discount-hunter": 0.22,
            "loyal-repeater": 0.2,
            "convenience-driven": 0.18,
            "premium-seeker": 0.1,
            "weekend-splurger": 0.08,
        },
        "daypart_weights": {
            "breakfast": 0.22,
            "lunch": 0.33,
            "afternoon": 0.16,
            "dinner": 0.22,
            "late-night": 0.07,
        },
        "time_period_weights": {
            "2025-Q1": 0.32,
            "2025-Q2": 0.26,
            "2025-Q3": 0.24,
            "2025-Q4": 0.18,
        },
        "channel_weights": {
            "app": 0.38,
            "web": 0.24,
            "in-store": 0.18,
            "drive-thru": 0.2,
        },
    },
    {
        "name": "Gen X",
        "weight": 0.22,
        "age_range": (44, 59),
        "segment_weights": {
            "loyal-repeater": 0.28,
            "discount-hunter": 0.22,
            "convenience-driven": 0.18,
            "premium-seeker": 0.14,
            "value-driven-lunch-buyer": 0.1,
            "weekend-splurger": 0.08,
        },
        "daypart_weights": {
            "breakfast": 0.18,
            "lunch": 0.28,
            "afternoon": 0.15,
            "dinner": 0.28,
            "late-night": 0.11,
        },
        "time_period_weights": {
            "2025-Q1": 0.25,
            "2025-Q2": 0.25,
            "2025-Q3": 0.25,
            "2025-Q4": 0.25,
        },
        "channel_weights": {
            "app": 0.28,
            "web": 0.22,
            "in-store": 0.2,
            "drive-thru": 0.3,
        },
    },
    {
        "name": "Boomer",
        "weight": 0.16,
        "age_range": (60, 75),
        "segment_weights": {
            "loyal-repeater": 0.3,
            "premium-seeker": 0.2,
            "discount-hunter": 0.18,
            "weekend-splurger": 0.14,
            "convenience-driven": 0.1,
            "value-driven-lunch-buyer": 0.08,
        },
        "daypart_weights": {
            "breakfast": 0.2,
            "lunch": 0.26,
            "afternoon": 0.2,
            "dinner": 0.24,
            "late-night": 0.1,
        },
        "time_period_weights": {
            "2025-Q1": 0.22,
            "2025-Q2": 0.28,
            "2025-Q3": 0.24,
            "2025-Q4": 0.26,
        },
        "channel_weights": {
            "app": 0.18,
            "web": 0.22,
            "in-store": 0.28,
            "drive-thru": 0.32,
        },
    },
]

GENERATION_LOOKUP = {config["name"]: config for config in GENERATION_CONFIGS}


def weighted_choice(options: List[str], weights: List[float]) -> str:
    if not options:
        raise ValueError("weighted_choice requires at least one option")
    if not weights or sum(weights) == 0:
        return random.choice(options)
    return random.choices(options, weights=weights, k=1)[0]


def weighted_choice_from_map(weight_map: Dict[str, float], defaults: Dict[str, float]) -> str:
    options = list(defaults.keys())
    weights = [weight_map.get(opt, defaults.get(opt, 0.0)) for opt in options]
    return weighted_choice(options, weights)


def sample_daypart(config: Dict[str, Any]) -> str:
    return weighted_choice_from_map(config.get("daypart_weights", {}), DEFAULT_DAYPART_WEIGHTS)


def sample_time_period(config: Dict[str, Any]) -> str:
    return weighted_choice_from_map(config.get("time_period_weights", {}), DEFAULT_TIME_PERIOD_WEIGHTS)


def sample_channel(config: Dict[str, Any]) -> str:
    return weighted_choice_from_map(config.get("channel_weights", {}), DEFAULT_CHANNEL_WEIGHTS)


def sample_segment(config: Dict[str, Any]) -> str:
    segment_weights = config.get("segment_weights", {})
    options = list(DEFAULT_SEGMENT_WEIGHTS.keys())
    weights = [segment_weights.get(opt, DEFAULT_SEGMENT_WEIGHTS[opt]) for opt in options]
    return weighted_choice(options, weights)


def sample_datetime(period_label: str, daypart: str) -> datetime:
    period = TIME_PERIODS[period_label]
    total_days = (period["end"].date() - period["start"].date()).days
    random_day = period["start"] + timedelta(days=random.randint(0, total_days))
    hour_choices = DAYPART_HOURS.get(daypart, list(range(24)))
    hour = random.choice(hour_choices)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    # Handle late-night hours that roll past midnight
    if hour >= 24:
        hour = hour % 24
    event_datetime = datetime(
        random_day.year,
        random_day.month,
        random_day.day,
        hour,
        minute,
        second,
    )
    # Ensure we stay within the quarter range
    if event_datetime < period["start"]:
        event_datetime = period["start"] + timedelta(
            hours=random.randint(0, 23), minutes=minute, seconds=second
        )
    if event_datetime > period["end"]:
        event_datetime = period["end"] - timedelta(
            hours=random.randint(0, 3), minutes=minute, seconds=second
        )
    return event_datetime


def determine_daypart_from_hour(hour: int) -> str:
    if 6 <= hour < 11:
        return "breakfast"
    if 11 <= hour < 15:
        return "lunch"
    if 15 <= hour < 18:
        return "afternoon"
    if 18 <= hour < 22:
        return "dinner"
    return "late-night"


def get_quarter_label(timestamp: datetime) -> str:
    month = timestamp.month
    if month <= 3:
        return "2025-Q1"
    if month <= 6:
        return "2025-Q2"
    if month <= 9:
        return "2025-Q3"
    return "2025-Q4"


def segment_visit_profile(segment: str) -> Tuple[int, float]:
    if segment == "value-driven-lunch-buyer":
        return random.randint(9, 16), round(random.uniform(8.0, 14.0), 2)
    if segment == "discount-hunter":
        return random.randint(12, 20), round(random.uniform(5.0, 10.0), 2)
    if segment == "loyal-repeater":
        return random.randint(15, 26), round(random.uniform(10.0, 16.0), 2)
    if segment == "convenience-driven":
        return random.randint(7, 13), round(random.uniform(9.0, 13.0), 2)
    if segment == "premium-seeker":
        return random.randint(5, 10), round(random.uniform(11.0, 18.0), 2)
    return random.randint(6, 12), round(random.uniform(7.0, 15.0), 2)


def generate_crm_data(num_customers: int = 1200) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Generate synthetic CRM and loyalty data with generation and time attributes."""
    crm_rows: List[Dict[str, Any]] = []
    customer_profiles: List[Dict[str, Any]] = []

    configs = GENERATION_CONFIGS
    config_weights = [cfg["weight"] for cfg in configs]

    for i in range(num_customers):
        generation_config = random.choices(configs, weights=config_weights, k=1)[0]
        generation = generation_config["name"]
        age = random.randint(*generation_config["age_range"])
        birth_year = REFERENCE_YEAR - age
        is_gen_z = generation == "Gen Z"

        segment = sample_segment(generation_config)
        avg_visits_per_month, avg_spend_per_visit = segment_visit_profile(segment)
        preferred_time = weighted_choice(list(DAYPART_HOURS.keys()), [generation_config.get("daypart_weights", {}).get(dp, DEFAULT_DAYPART_WEIGHTS[dp]) for dp in DAYPART_HOURS])

        customer_id = f"customer_{i+1:04d}"
        lifetime_visits = avg_visits_per_month * random.randint(18, 48)
        lifetime_spend = round(avg_spend_per_visit * lifetime_visits, 2)

        customer_profiles.append(
            {
                "customer_id": customer_id,
                "segment_id": segment,
                "generation": generation,
                "birth_year": birth_year,
                "age": age,
                "is_gen_z": is_gen_z,
                "preferred_time": preferred_time,
            }
        )

        annual_visits = avg_visits_per_month * 12
        num_visits = random.randint(int(annual_visits * 0.6), int(annual_visits * 1.1))

        for _ in range(num_visits):
            time_period = sample_time_period(generation_config)
            visit_daypart = sample_daypart(generation_config)
            visit_datetime = sample_datetime(time_period, visit_daypart)

            spend = round(random.uniform(avg_spend_per_visit * 0.7, avg_spend_per_visit * 1.3), 2)
            channel = sample_channel(generation_config)

            crm_rows.append(
                {
                    "customer_id": customer_id,
                    "segment_id": segment,
                    "visit_date": visit_datetime.isoformat(),
                    "spend": spend,
                    "channel": channel,
                    "preferred_time": preferred_time,
                    "total_lifetime_visits": lifetime_visits,
                    "total_lifetime_spend": lifetime_spend,
                    "birth_year": birth_year,
                    "age": age,
                    "generation": generation,
                    "is_gen_z": is_gen_z,
                    "time_period": time_period,
                    "visit_daypart": visit_daypart,
                }
            )

    return crm_rows, customer_profiles


def generate_redemption_logs(num_redemptions: int, customer_profiles: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generate synthetic redemption log data aligned to customer profiles."""
    data = []
    for i in range(num_redemptions):
        profile = customer_profiles.sample(1).iloc[0]
        generation = profile["generation"]
        generation_config = GENERATION_LOOKUP[generation]
        segment = profile["segment_id"]
        birth_year = int(profile["birth_year"])
        age = int(profile["age"])
        is_gen_z = bool(profile["is_gen_z"])

        offer_type = random.choice(OFFER_TYPES)

        base_lift = random.uniform(1.1, 1.8)
        if offer_type == "BOGO" and segment == "value-driven-lunch-buyer":
            base_lift = random.uniform(2.0, 2.8)
        elif offer_type == "Time-Boxed" and segment in {"convenience-driven", "value-driven-lunch-buyer"}:
            base_lift = random.uniform(1.8, 2.6)
        elif offer_type == "App Exclusive" and generation == "Gen Z":
            base_lift = random.uniform(2.0, 2.7)
        elif segment == "discount-hunter":
            base_lift = random.uniform(1.5, 2.2)

        channel = sample_channel(generation_config)
        time_period = sample_time_period(generation_config)
        daypart = sample_daypart(generation_config)
        redemption_dt = sample_datetime(time_period, daypart)

        is_time_boxed = offer_type == "Time-Boxed"
        is_app_exclusive = offer_type == "App Exclusive" or channel == "app"

        data.append(
            {
                "redemption_id": f"redemption_{i+1:05d}",
                "customer_id": profile["customer_id"],
                "segment_id": segment,
                "offer_type": offer_type,
                "redemption_date": redemption_dt.isoformat(),
                "channel": channel,
                "is_time_boxed": is_time_boxed,
                "is_app_exclusive": is_app_exclusive,
                "lift_multiplier": round(base_lift, 2),
                "redemption_value": round(random.uniform(5.0, 16.0), 2),
                "month": redemption_dt.strftime("%Y-%m"),
                "day_of_week": redemption_dt.strftime("%A"),
                "hour": redemption_dt.hour,
                "time_period": time_period,
                "daypart": daypart,
                "birth_year": birth_year,
                "age": age,
                "generation": generation,
                "is_gen_z": is_gen_z,
            }
        )
    return data


def generate_feedback_data(num_reviews: int, customer_profiles: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generate synthetic feedback and review data."""
    data = []
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

    for i in range(num_reviews):
        profile = customer_profiles.sample(1).iloc[0]
        generation_config = GENERATION_LOOKUP[profile["generation"]]
        segment = profile["segment_id"]
        time_period = sample_time_period(generation_config)
        daypart = sample_daypart(generation_config)
        feedback_dt = sample_datetime(time_period, daypart)

        offer_type = random.choice(OFFER_TYPES)
        phrases = segment_phrases.get(segment, ["good", "nice", "enjoyed"])
        selected_phrases = random.sample(phrases, k=min(len(phrases), random.randint(2, 4)))

        review_templates = [
            f"I {random.choice(['loved', 'appreciated', 'enjoyed'])} the {offer_type.lower()} offer. {random.choice(selected_phrases)}!",
            f"The {offer_type.lower()} was {selected_phrases[0]}. {selected_phrases[1] if len(selected_phrases) > 1 else 'Great experience!'}",
            f"Really {selected_phrases[0]} how {selected_phrases[1] if len(selected_phrases) > 1 else 'smooth'} the {offer_type.lower()} was.",
        ]
        review_text = random.choice(review_templates)
        if offer_type == "App Exclusive":
            review_text += " The app made it so easy!"
        if offer_type == "Time-Boxed" and daypart == "breakfast":
            review_text += " Perfect timing for my morning rush."

        sentiment_base = 0.88 if profile["generation"] == "Gen Z" and offer_type in {"App Exclusive", "Time-Boxed"} else 0.75
        sentiment_score = max(0.45, min(0.98, random.gauss(sentiment_base, 0.08)))

        data.append(
            {
                "feedback_id": f"feedback_{i+1:05d}",
                "customer_id": profile["customer_id"],
                "segment_id": segment,
                "offer_type": offer_type,
                "feedback_date": feedback_dt.isoformat(),
                "review_text": review_text,
                "sentiment_score": round(sentiment_score, 2),
                "key_phrases": selected_phrases,
                "channel": sample_channel(generation_config),
                "source": random.choice(["app_review", "campaign_feedback", "social_comment", "survey"]),
                "time_period": time_period,
                "daypart": daypart,
                "birth_year": int(profile["birth_year"]),
                "age": int(profile["age"]),
                "generation": profile["generation"],
                "is_gen_z": bool(profile["is_gen_z"]),
            }
        )
    return data


def generate_customer_transactions_raw(crm_df: pd.DataFrame, redemption_df: pd.DataFrame) -> pd.DataFrame:
    """Create raw transaction records derived from CRM visits."""
    transactions_df = crm_df.copy()
    transactions_df["transaction_date"] = pd.to_datetime(transactions_df["visit_date"])
    transactions_df["transaction_id"] = [f"txn_{i+1:07d}" for i in range(len(transactions_df))]
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
    transactions_df["payment_method"] = [random.choice(PAYMENT_METHODS) for _ in range(len(transactions_df))]
    transactions_df["items"] = [
        random.sample(MENU_ITEMS, k=random.randint(1, min(3, len(MENU_ITEMS))))
        for _ in range(len(transactions_df))
    ]

    transactions_df["visit_daypart"] = transactions_df["transaction_date"].dt.hour.apply(determine_daypart_from_hour)
    transactions_df["time_period"] = transactions_df["transaction_date"].apply(get_quarter_label)

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
            "birth_year",
            "age",
            "generation",
            "is_gen_z",
            "time_period",
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
            "time_period",
            "daypart",
            "birth_year",
            "age",
            "generation",
            "is_gen_z",
        ]
    ]


def generate_customer_segments(
    crm_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
    redemption_df: pd.DataFrame,
    feedback_df: pd.DataFrame,
    customer_profiles: pd.DataFrame,
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
        profile_segment = customer_profiles[customer_profiles["segment_id"] == segment]

        visits_per_customer = (
            crm_segment.groupby("customer_id")["visit_date"].count().mean()
            if not crm_segment.empty
            else 0
        )
        avg_spend = crm_segment["spend"].mean() if not crm_segment.empty else 0
        transaction_count = len(transactions_segment) or 1
        redemption_rate = len(redemption_segment) / transaction_count
        lift_estimate = (
            redemption_segment["lift_multiplier"].mean() if not redemption_segment.empty else 1.0
        )

        top_channels = crm_segment["channel"].value_counts().head(3).index.tolist()
        preferred_mechanics = (
            redemption_segment["offer_type"].value_counts().head(3).index.tolist()
            if not redemption_segment.empty
            else random.sample(OFFER_TYPES, k=3)
        )

        phrases = []
        if not feedback_segment.empty and "key_phrases" in feedback_segment:
            for value in feedback_segment["key_phrases"]:
                phrases.extend(value if isinstance(value, list) else [value])
        key_messaging_phrases = (
            pd.Series(phrases).value_counts().head(5).index.tolist() if phrases else []
        )

        generation_mix = (
            profile_segment["generation"].value_counts(normalize=True).round(3).to_dict()
            if not profile_segment.empty
            else {}
        )
        primary_generation = max(generation_mix, key=generation_mix.get) if generation_mix else None
        gen_z_share = generation_mix.get("Gen Z", 0.0)

        top_time_periods = crm_segment["time_period"].value_counts().head(3).index.tolist()
        dominant_dayparts = crm_segment["visit_daypart"].value_counts().head(3).index.tolist()

        description = (
            f"{segment.replace('-', ' ').title()} segment averaging ${avg_spend:0.2f} per visit "
            f"and {visits_per_customer:0.1f} visits per month."
        )

        empirical_metrics = {
            "avg_monthly_visits": round(visits_per_customer or 0, 1),
            "avg_spend": round(avg_spend or 0, 2),
            "segment_size": len(crm_segment["customer_id"].unique()),
            "top_channels": top_channels,
            "generation_mix": generation_mix,
            "top_time_periods": top_time_periods,
            "dominant_dayparts": dominant_dayparts,
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
                "primary_generation": primary_generation,
                "gen_z_share": round(float(gen_z_share), 3),
                "top_time_periods": top_time_periods,
                "dominant_dayparts": dominant_dayparts,
            }
        )

    return pd.DataFrame(segments)


def export_to_dataframes() -> Dict[str, pd.DataFrame]:
    """Generate all synthetic data and return as pandas DataFrames."""
    print("Generating synthetic CRM data...")
    crm_rows, customer_profile_rows = generate_crm_data(num_customers=1200)
    crm_df = pd.DataFrame(crm_rows)
    customer_profiles = pd.DataFrame(customer_profile_rows)

    print("Generating synthetic redemption logs...")
    redemption_data = generate_redemption_logs(num_redemptions=5500, customer_profiles=customer_profiles)
    redemption_df = pd.DataFrame(redemption_data)

    print("Generating synthetic feedback data...")
    feedback_data = generate_feedback_data(num_reviews=2200, customer_profiles=customer_profiles)
    feedback_df = pd.DataFrame(feedback_data)

    print("Deriving raw transaction records...")
    transactions_df = generate_customer_transactions_raw(crm_df, redemption_df)

    print("Deriving raw feedback verbatims...")
    feedback_raw_df = generate_customer_feedback_raw(feedback_df)

    print("Synthesizing baseline segment summaries...")
    segments_df = generate_customer_segments(
        crm_df, transactions_df, redemption_df, feedback_df, customer_profiles
    )

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
        print("\n  Sample data:")
        print(df.head(3).to_string())
