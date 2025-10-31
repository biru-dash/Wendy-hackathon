# BigQuery Dataset: wendys_hackathon_data - Table Summary

## Overview
The `wendys_hackathon_data` dataset contains **13 tables** with existing data that the Customer Insights agents can now leverage.

## Tables Used by Customer Insights Agents

### BehavioralAnalysisAgent (Quant Specialist)

**Primary Tables:**
1. **crm_data** (37,513 rows) ✓ Using
   - Customer visit history with segments, spend, channels
   - Fields: customer_id, segment_id, visit_date, spend, channel, preferred_time, lifetime metrics
   - **Status**: Fully integrated

2. **customer_transactions_raw** (2,000 rows) ✓ Now Integrated
   - Raw transaction data with offer redemptions
   - Fields: transaction_id, customer_id, visit_date, total_spend, redeemed_offer, channel
   - **Use Case**: Analyzing which specific offers were redeemed
   - **Status**: Auto-selected when queries mention "transaction" or "redeemed_offer"

3. **redemption_logs** (5,000 rows) ✓ Using
   - Detailed redemption history with lift metrics
   - Fields: redemption_id, offer_type, lift_multiplier, channel, segment_id, temporal data
   - **Status**: Fully integrated

### SentimentAnalysisAgent (Qual Specialist)

**Primary Tables:**
1. **feedback_data** (2,000 rows) ✓ Using
   - Structured feedback with sentiment scores and key phrases
   - Fields: feedback_id, segment_id, offer_type, review_text, sentiment_score, key_phrases[], channel, source
   - **Status**: Fully integrated

2. **customer_feedback_raw** (1,000 rows) ✓ Now Integrated
   - Raw feedback text with ratings
   - Fields: feedback_id, customer_id, feedback_date, rating, feedback_text
   - **Use Case**: Analyzing raw text without pre-processed sentiment
   - **Status**: Auto-selected when queries mention "rating" or "raw"

### ProfileSynthesizerAgent (Strategist)

**Output Table:**
1. **customer_segments** (0 rows - empty, ready for use) ✓ Now Integrated
   - Schema matches the output format perfectly
   - Fields: segment_id, description, preferred_mechanics[], key_messaging_phrases[], redemption_rate, lift_estimate, empirical_metrics
   - **Use Case**: Save synthesized customer insights for persistence and retrieval
   - **Status**: `save_customer_segments_tool` now available to write results

## Integration Details

### Smart Table Selection
The database tools now intelligently select which table to query based on query content:

**crm_database_tool:**
- Queries `customer_transactions_raw` if query mentions "transaction" or "redeemed_offer"
- Queries `crm_data` if query mentions "segment", "lifetime", or "visit"
- Default: `crm_data`

**feedback_database_tool:**
- Queries `customer_feedback_raw` if query mentions "rating" or "raw"
- Queries `feedback_data` if query mentions "sentiment", "key_phrases", or "segment"
- Default: `feedback_data`

### Other Tables (Not Used by Customer Insights, but Available)

- **competitor_intel_raw** (1,000 rows): Competitor offer observations
- **competitor_landscape** (0 rows): Structured competitor data
- **market_trends** (0 rows): Processed market trends
- **market_trends_raw** (1,500 rows): Raw trend data sources
- **offer_concepts** (0 rows): Generated offer concepts
- **whitespace_opportunities** (0 rows): Market whitespace analysis
- **agent_runs** (0 rows): Agent execution logs

## Benefits of Using Existing Data

1. **More Data Sources**: Agents can now query both structured and raw data
2. **Better Coverage**: 2K additional transactions + 1K raw feedback entries
3. **Flexibility**: Tools auto-select the best table based on query intent
4. **Persistence**: Can save results to `customer_segments` for later use

## Next Steps

The Customer Insights agents are now fully integrated with existing BigQuery data:

- ✅ Can query `crm_data` + `customer_transactions_raw` for behavioral analysis
- ✅ Can query `redemption_logs` for lift calculations  
- ✅ Can query `feedback_data` + `customer_feedback_raw` for sentiment analysis
- ✅ Can save results to `customer_segments` table

All tools are ready to use with the existing dataset!
