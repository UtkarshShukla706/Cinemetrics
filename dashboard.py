import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(
    page_title='CineMetrics',
    page_icon='🎬',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Complete dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0d0d1a; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e !important;
        border-right: 2px solid #e94560;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* FIX 1: Target specifically the tags (chips) to prevent overriding layout elements */
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background-color: #e94560 !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #e94560 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }[data-testid="stSidebar"] .stSlider label {
        color: #e94560 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Multiselect dropdown */
    .stMultiSelect div[data-baseweb="select"] {
        background-color: #16213e !important;
        border: 1px solid #e94560 !important;
        border-radius: 8px !important;
    }
    
    /* FIX 2: Set nested elements to transparent so they don't block the first letters */
    .stMultiSelect div[data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    /* Slider */
    .stSlider div[data-baseweb="slider"] {
        background-color: #16213e !important;
    }

    /* Metric cards */[data-testid="stMetric"] {
        background-color: #1a1a2e !important;
        border: 1px solid #e94560 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }[data-testid="stMetric"] label {
        color: #a0a8b8 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }

    /* Headings */
    h1 {
        color: #e94560 !important;
        font-size: 52px !important;
        font-weight: 800 !important;
    }
    h2 {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    h3 {
        color: #ffffff !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }
    h4 {
        color: #e94560 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* Text */
    p { color: #a0a8b8 !important; }

    /* Text input */
    .stTextInput input {
        background-color: #16213e !important;
        color: #ffffff !important;
        border: 1px solid #e94560 !important;
        border-radius: 8px !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: #1a1a2e !important;
        border: 1px solid #e94560 !important;
        border-radius: 8px !important;
    }

    /* Divider */
    hr {
        border-color: #e94560 !important;
        opacity: 0.3;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d0d1a; }
    ::-webkit-scrollbar-thumb {
        background: #e94560;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Dark matplotlib theme
plt.style.use('dark_background')

# Load data
df = pd.read_csv('data/imdb-cleaned.csv')

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <div style='font-size: 64px;'>🎬</div>
    <h1 style='color: #e94560; font-size: 52px; 
    font-weight: 800; margin: 0;'>CineMetrics</h1>
    <p style='color: #a0a8b8; font-size: 18px; margin-top: 8px;'>
    Uncovering Patterns in Cinema's Top 1000 Films
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('---')

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align: center; padding: 10px 0 20px 0;'>
    <span style='font-size: 40px;'>🎬</span>
    <h2 style='color: #e94560; font-size: 24px; 
    font-weight: 800; margin: 5px 0;'>CineMetrics</h2>
    <p style='color: #a0a8b8; font-size: 12px;'>
    Filters & Controls
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<p style='color: #e94560; font-size: 16px; 
font-weight: 700;'>🎭  Genre</p>
""", unsafe_allow_html=True)
all_genres = sorted(df['Genres'].unique().tolist())
selected_genres = st.sidebar.multiselect(
    'Select Genres',
    options=all_genres,
    default=all_genres,
    label_visibility='collapsed'
)

st.sidebar.markdown("""
<p style='color: #e94560; font-size: 16px; 
font-weight: 700; margin-top: 16px;'>📅  Decade</p>
""", unsafe_allow_html=True)
all_decades = sorted(df['Decade'].unique().tolist())
selected_decades = st.sidebar.multiselect(
    'Select Decades',
    options=all_decades,
    default=all_decades,
    label_visibility='collapsed'
)

st.sidebar.markdown("""
<p style='color: #e94560; font-size: 16px; 
font-weight: 700; margin-top: 16px;'>⭐  IMDB Rating Range</p>
""", unsafe_allow_html=True)
rating_range = st.sidebar.slider(
    'IMDB Rating Range',
    min_value=float(df['IMDB'].min()),
    max_value=float(df['IMDB'].max()),
    value=(float(df['IMDB'].min()), float(df['IMDB'].max())),
    step=0.1,
    label_visibility='collapsed'
)

st.sidebar.markdown("""
<p style='color: #e94560; font-size: 16px; 
font-weight: 700; margin-top: 16px;'>💰  Gross Range (Millions)</p>
""", unsafe_allow_html=True)
gross_range = st.sidebar.slider(
    'Gross Range',
    min_value=float(df['Gross_per_M'].min()),
    max_value=float(df['Gross_per_M'].max()),
    value=(float(df['Gross_per_M'].min()),
           float(df['Gross_per_M'].max())),
    label_visibility='collapsed'
)

st.sidebar.markdown("""
<p style='color: #e94560; font-size: 16px; 
font-weight: 700; margin-top: 16px;'>🎬  Top N Directors</p>
""", unsafe_allow_html=True)
top_n = st.sidebar.slider(
    'Top N Directors',
    min_value=5,
    max_value=20,
    value=10,
    label_visibility='collapsed'
)

st.sidebar.markdown('---')
st.sidebar.markdown("""
<p style='color: #a0a8b8; font-size: 11px; text-align: center;'>
CineMetrics v1.0 | Built with Streamlit
</p>
""", unsafe_allow_html=True)

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
filtered_df = df[
    (df['Genres'].isin(selected_genres)) &
    (df['Decade'].isin(selected_decades)) &
    (df['IMDB'] >= rating_range[0]) &
    (df['IMDB'] <= rating_range[1]) &
    (df['Gross_per_M'] >= gross_range[0]) &
    (df['Gross_per_M'] <= gross_range[1])
]

# ── TOP METRICS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<p style='color: #a0a8b8; font-size: 14px;'>
Showing <b style='color:#e94560; 
font-size: 18px;'>{len(filtered_df)}</b> films
</p>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('🎬  Total Films', f"{len(filtered_df)}")
col2.metric('⭐  Avg Rating', f"{filtered_df['IMDB'].mean():.2f}")
col3.metric('💰  Avg Gross', 
            f"${filtered_df['Gross_per_M'].mean():.1f}M")
col4.metric('📝  Avg Metascore', 
            f"{filtered_df['Metascore'].mean():.1f}")
col5.metric('⏱️  Avg Runtime', 
            f"{filtered_df['Duration'].mean():.0f} min")

st.markdown('---')

# ── ROW 1 ─────────────────────────────────────────────────────────────────────
st.markdown("### 📊  Genre & Rating Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎭  Genre Frequency")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    genre_counts = filtered_df['Genres'].value_counts()
    colors = sns.color_palette('RdPu', len(genre_counts))
    sns.barplot(x=genre_counts.values, y=genre_counts.index,
                palette=colors, ax=ax)
    ax.set_xlabel('Number of Films', color='#a0a8b8')
    ax.set_ylabel('Genre', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("#### ⭐  IMDB Rating Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    sns.histplot(data=filtered_df, x='IMDB', bins=20,
                 color='#e94560', alpha=0.8, ax=ax)
    ax.set_xlabel('IMDB Rating', color='#a0a8b8')
    ax.set_ylabel('Count', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

st.markdown('---')

# ── ROW 2 ─────────────────────────────────────────────────────────────────────
st.markdown("### 🔍  Correlation Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💰  IMDB Rating vs Box Office Gross")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    sns.regplot(data=filtered_df, x='IMDB', y='Gross_per_M',
                scatter_kws={'alpha': 0.5, 'color': '#4fc3f7'},
                line_kws={'color': '#e94560', 'linewidth': 2},
                ax=ax)
    ax.set_xlabel('IMDB Rating', color='#a0a8b8')
    ax.set_ylabel('Gross Per Million ($)', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("#### 📝  IMDB Rating vs Metascore")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    sns.regplot(data=filtered_df, x='IMDB', y='Metascore',
                scatter_kws={'alpha': 0.5, 'color': '#ce93d8'},
                line_kws={'color': '#e94560', 'linewidth': 2},
                ax=ax)
    ax.set_xlabel('IMDB Rating', color='#a0a8b8')
    ax.set_ylabel('Metascore', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

st.markdown('---')

# ── ROW 3 ─────────────────────────────────────────────────────────────────────
st.markdown("### 📅  Decade Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ⭐  Average IMDB Rating by Decade")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    survive = filtered_df.groupby(
        'Decade')['IMDB'].mean().sort_index()
    sns.barplot(x=survive.index, y=survive.values,
                color='#4fc3f7', alpha=0.8, ax=ax)
    ax.plot(range(len(survive)), survive.values,
            color='#e94560', linewidth=2,
            marker='o', markersize=6, label='Trend')
    ax.set_ylim(7, 9)
    ax.set_xlabel('Decade', color='#a0a8b8')
    ax.set_ylabel('Average IMDB Rating', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    ax.legend(facecolor='#1a1a2e', labelcolor='#a0a8b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("#### 🎬  Number of Films by Decade")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    decade_counts = filtered_df[
        'Decade'].value_counts().sort_index()
    sns.barplot(x=decade_counts.index, y=decade_counts.values,
                color='#81c784', alpha=0.8, ax=ax)
    ax.plot(range(len(decade_counts)), decade_counts.values,
            color='#e94560', linewidth=2,
            marker='o', markersize=6, label='Trend')
    ax.set_xlabel('Decade', color='#a0a8b8')
    ax.set_ylabel('Number of Films', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    ax.legend(facecolor='#1a1a2e', labelcolor='#a0a8b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

st.markdown('---')

# ── ROW 4 ─────────────────────────────────────────────────────────────────────
st.markdown("### 🎬  Director & Star Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### 🏆  Top {top_n} Directors by Film Count")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    top_directors = filtered_df[
        'Director'].value_counts().head(top_n)
    colors = sns.color_palette('RdPu', len(top_directors))
    sns.barplot(x=top_directors.values, y=top_directors.index,
                palette=colors, ax=ax)
    ax.set_xlabel('Number of Films', color='#a0a8b8')
    ax.set_ylabel('Director', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown(f"#### ⭐  Top {top_n} Directors by Avg Rating")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    dir_rating = filtered_df.groupby('Director')['IMDB'].mean()
    dir_count = filtered_df['Director'].value_counts()
    dir_qualified = dir_count[dir_count >= 2].index
    top_dir_rating = dir_rating[
        dir_rating.index.isin(dir_qualified)].nlargest(top_n)
    colors = sns.color_palette('PuBu', len(top_dir_rating))
    sns.barplot(x=top_dir_rating.values, y=top_dir_rating.index,
                palette=colors, ax=ax)
    ax.set_xlabel('Average IMDB Rating', color='#a0a8b8')
    ax.set_ylabel('Director', color='#a0a8b8')
    ax.tick_params(colors='#a0a8b8')
    ax.set_xlim(7,9)
    for spine in ax.spines.values():
        spine.set_edgecolor('#16213e')
    st.pyplot(fig)
    plt.close()

st.markdown('---')

# ── HEATMAP ───────────────────────────────────────────────────────────────────
st.markdown("### 🔥  Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')
numeric_cols = filtered_df[['IMDB', 'Gross_per_M',
                             'Votes_per_K', 'Duration',
                             'Metascore']]
sns.heatmap(numeric_cols.corr(), annot=True, fmt='.2f',
            cmap='RdPu', ax=ax,
            linewidths=0.5, linecolor='#16213e')
ax.tick_params(colors='#a0a8b8')
st.pyplot(fig)
plt.close()

st.markdown('---')

# ── DATA TABLE ────────────────────────────────────────────────────────────────
st.markdown("### 📋  Raw Data Explorer")
st.markdown(f"*{len(filtered_df)} films match your filters*")

search = st.text_input('🔍  Search by film name', '')
if search:
    display_df = filtered_df[
        filtered_df['Name'].str.contains(
            search, case=False, na=False)]
else:
    display_df = filtered_df

st.dataframe(
    display_df[['Name', 'Year', 'Genres', 'IMDB',
                'Director', 'Lead', 'Gross_per_M',
                'Metascore', 'Decade']].reset_index(drop=True),
    use_container_width=True,
    height=400
)

st.markdown('---')
st.markdown("""
<p style='text-align: center; color: #a0a8b8; font-size: 12px;'>
🎬 CineMetrics | Built with Streamlit & Seaborn | 
IMDB Top 1000 Dataset
</p>
""", unsafe_allow_html=True)