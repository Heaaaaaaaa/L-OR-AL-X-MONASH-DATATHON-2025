# dashboard.py - Save this as a separate file
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="CommentSense Dashboard", layout="wide")

DATA_CANDIDATES = ["/Users/hea/Library/CloudStorage/OneDrive-Heriot-WattUniversity/HW/L’Oréal/Final/your_processed_data(En).csv", "/Users/hea/Library/CloudStorage/OneDrive-Heriot-WattUniversity/HW/L’Oréal/your_processed_data(En).csv"]

def _pick_data_path(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("CSV not found in: " + ", ".join(paths))

DATA_PATH = _pick_data_path(DATA_CANDIDATES)

@st.cache_data(show_spinner=False)
def load_data(path: str, mtime: float, size: int):
    # mtime & size are part of the cache key → auto-bust when file changes
    return pd.read_csv(path)

stat = os.stat(DATA_PATH)
df = load_data(DATA_PATH, stat.st_mtime, stat.st_size)

# Sidebar: force-refresh button
if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()

# (File info caption hidden)

# Sidebar filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect("Category", df['category_final'].unique())
sentiment_filter = st.sidebar.multiselect("Sentiment", df['sent_label'].unique())
# New: Relevance filter (if column exists)
relevance_options = df['relevance_label'].unique() if 'relevance_label' in df.columns else []
relevance_filter = st.sidebar.multiselect("Relevance", relevance_options) if len(relevance_options) else []

# Apply filters (handle empty selections)
if not category_filter:
    category_filter = df['category_final'].unique()
if not sentiment_filter:
    sentiment_filter = df['sent_label'].unique()
if 'relevance_label' in df.columns and not relevance_filter:
    relevance_filter = df['relevance_label'].unique().tolist()

mask = (
    df['category_final'].isin(category_filter)
    & df['sent_label'].isin(sentiment_filter)
)
if 'relevance_label' in df.columns:
    mask = mask & df['relevance_label'].isin(relevance_filter)

filtered_df = df[mask]

# Main dashboard
st.title("🎯 CommentSense Analytics Dashboard")

# KPI cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Comments", f"{len(filtered_df):,}")
with col2:
    quality_ratio = (filtered_df['is_spam'] == False).mean()
    st.metric("Quality Ratio", f"{quality_ratio:.1%}")
with col3:
    positive_ratio = (filtered_df['sent_label'] == 'positive').mean()
    st.metric("Positive Sentiment", f"{positive_ratio:.1%}")
with col4:
    relevant_ratio = (filtered_df['relevance_label'] == 'relevant').mean()
    st.metric("Relevance Ratio", f"{relevant_ratio:.1%}")

# Charts
col1, col2 = st.columns(2)

with col1:
    # Category distribution
    cat_counts = filtered_df['category_final'].value_counts()
    fig = px.pie(values=cat_counts.values, names=cat_counts.index, title="Comments by Category")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Stacked bars: X = categories, Y = count, stacks = sentiments
    if len(filtered_df):
        cats = sorted(filtered_df['category_final'].dropna().unique())
        # Stack order: bottom -> top
        order = ['positive','neutral','negative']

        counts = (
            filtered_df
            .groupby(['category_final','sent_label'])
            .size()
            .unstack(fill_value=0)
            .reindex(index=cats, columns=order, fill_value=0)
        )
        # Sort categories by total height (descending)
        totals = counts.sum(axis=1)
        counts = counts.loc[totals.sort_values(ascending=False).index]
        totals = counts.sum(axis=1).replace(0, 1)
        pct = (counts.div(totals, axis=0) * 100).round(1)

        import plotly.graph_objects as go
        color_map = {
            'positive': 'seagreen',
            'neutral': 'orange',
            'negative': 'crimson',
        }

        fig = go.Figure()
        for s in order:
            fig.add_bar(
                x=counts.index,
                y=counts[s].values,
                name=s,
                marker_color=color_map[s],
                text=[f"{p:.1f}%" if v > 0 else "" for p, v in zip(pct[s].values, counts[s].values)],
                textposition='inside',
                hovertemplate=f"Category: %{{x}}<br>{s.title()} count: %{{y}}<br>Share: %{{text}}<extra></extra>",
            )

        fig.update_layout(
            title="Sentiment Distribution by Category (stacked)",
            xaxis_title="Categories",
            yaxis_title="Number of comments",
            barmode='stack',
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for current filters.")

# Second row charts
col3, col4 = st.columns(2)

with col3:
    # Overall sentiment distribution (simple bar)
    sent_counts = filtered_df['sent_label'].value_counts()
    fig = px.bar(x=sent_counts.index, y=sent_counts.values, title="Overall Sentiment Distribution",
                 labels={'x': 'Sentiment', 'y': 'Number of comments'},
                 color=sent_counts.index,
                 color_discrete_map={'positive': 'seagreen', 'neutral': 'orange', 'negative': 'crimson'})
    st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Sample Comments")
# Show exactly 5 specific comments by index from the full dataset
target_indices = [7, 11, 18, 20, 3011]
available_indices = [i for i in target_indices if i in df.index]
sample_columns = ['textOriginal', 'category_final', 'sent_label', 'relevance_label']
sample_df = df.loc[available_indices, sample_columns]
st.dataframe(sample_df.reset_index(drop=True))

# Run with: streamlit run dashboard.py
