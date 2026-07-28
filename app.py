import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Global Economy Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background-color: #0B1120; color: #E0E6F0; }
[data-testid="stSidebar"] { background-color: #0D1526; border-right: 1px solid #1E2D4A; }
.kpi-card {
    background: linear-gradient(135deg, #0D1F3C 0%, #112240 100%);
    border: 1px solid #1E3A5F; border-radius: 14px;
    padding: 18px 20px; text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,114,178,0.18); }
.kpi-value { font-size: 2.1rem; font-weight: 800; margin: 6px 0 2px 0; }
.kpi-label { font-size: 0.72rem; color: #7B93B4; text-transform: uppercase; letter-spacing: 1.2px; }
.kpi-sub   { font-size: 0.78rem; color: #4A6080; margin-top: 2px; }
.section-hdr {
    font-size: 0.85rem; font-weight: 700; color: #4FC3F7;
    text-transform: uppercase; letter-spacing: 1.8px;
    border-left: 3px solid #0072B2; padding-left: 9px;
    margin: 16px 0 8px 0;
}
.insight {
    background: linear-gradient(90deg,#0D1F3C,#0B1120);
    border-left: 3px solid #E69F00; border-radius: 5px;
    padding: 9px 13px; font-size: 0.82rem; color: #B0C4DE; margin-top: 5px;
}
button[data-baseweb="tab"] { color: #7B93B4 !important; font-size: 0.86rem !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    color: #4FC3F7 !important; border-bottom-color: #0072B2 !important;
}
.stMultiSelect label, .stSlider label, .stSelectbox label {
    color: #7B93B4 !important; font-size: 0.79rem !important;
}
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Palette ───────────────────────────────────────────────────────────────────
INCOME_COLORS = {
    'High income':         '#0072B2',
    'Upper middle income': '#E69F00',
    'Lower middle income': '#009E73',
    'Low income':          '#CC79A7'
}
REGION_COLORS = {
    'Americas': '#0072B2', 'Europe': '#E69F00',
    'Asia':     '#009E73', 'Africa': '#CC79A7', 'Oceania': '#56B4E9'
}
BG    = '#0B1120'
CARD  = '#0D1F3C'
GRID  = '#1E2D4A'
FONT  = '#C5D5EA'
LINE  = '#2A3F5F'

def cl(fig, h=400):
    fig.update_layout(
        plot_bgcolor=BG, paper_bgcolor=BG,
        font=dict(family='Inter,Arial', size=11, color=FONT),
        height=h, margin=dict(l=50,r=30,t=45,b=45),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickfont=dict(color=FONT), linecolor=LINE, showline=True),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickfont=dict(color=FONT), linecolor=LINE, showline=True),
    )
    return fig

ISO_MAP = {
    'USA':'USA','China':'CHN','Germany':'DEU','India':'IND','Brazil':'BRA',
    'UK':'GBR','France':'FRA','Japan':'JPN','South Korea':'KOR','Canada':'CAN',
    'Australia':'AUS','Mexico':'MEX','Indonesia':'IDN','Nigeria':'NGA',
    'South Africa':'ZAF','Egypt':'EGY','Turkey':'TUR','Argentina':'ARG',
    'Saudi Arabia':'SAU','UAE':'ARE','Thailand':'THA','Vietnam':'VNM',
    'Bangladesh':'BGD','Pakistan':'PAK','Ethiopia':'ETH','Kenya':'KEN',
    'Ghana':'GHA','Tanzania':'TZA','Sweden':'SWE','Norway':'NOR',
    'Denmark':'DNK','Finland':'FIN','Netherlands':'NLD','Switzerland':'CHE',
    'Spain':'ESP','Italy':'ITA','Poland':'POL','Russia':'RUS','Ukraine':'UKR',
    'Romania':'ROU','Chile':'CHL','Colombia':'COL','Peru':'PER','Venezuela':'VEN',
    'Morocco':'MAR','Algeria':'DZA','Malaysia':'MYS','Philippines':'PHL',
    'Singapore':'SGP','New Zealand':'NZL'
}

@st.cache_data
def load():
    df = pd.read_csv("global_economy.csv")
    df['Year'] = df['Year'].astype(int)
    return df
df = load()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-size:1.4rem;font-weight:800;color:#4FC3F7;margin-bottom:2px;'>🌍 Global Economy</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#4A6080;margin-bottom:18px;'>Data Visualization · Summer 2026</div>", unsafe_allow_html=True)
    st.divider()
    regions  = st.multiselect("🌐 Region",       sorted(df.Region.unique()),       default=sorted(df.Region.unique()))
    incomes  = st.multiselect("💰 Income Group", sorted(df.Income_Group.unique()), default=sorted(df.Income_Group.unique()))
    y1, y2   = st.slider("📅 Year Range", 2000, 2023, (2000, 2023))
    sel_ctry = st.multiselect("🏳️ Countries (optional)", sorted(df.Country.unique()))
    st.divider()
    st.markdown("<div style='font-size:0.7rem;color:#3A5070;'>50 countries · 2000–2023 · 15 indicators<br>World Development Indicators</div>", unsafe_allow_html=True)

dff = df[df.Region.isin(regions) & df.Income_Group.isin(incomes) & df.Year.between(y1,y2)]
if sel_ctry:
    dff = dff[dff.Country.isin(sel_ctry)]
latest = dff[dff.Year==dff.Year.max()]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:22px 0 6px 0;'>
  <span style='font-size:1.9rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.5px;'>
    🌍 Global Economy Intelligence
  </span><br>
  <span style='font-size:0.88rem;color:#7B93B4;'>
    50 countries · 24 years of economic crises, growth, inequality & sustainability
  </span>
</div>""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
cols = st.columns(5)
kpi_data = [
    ("Countries",         f"{dff.Country.nunique()}",                          "in current filter",   "#4FC3F7"),
    ("Avg GDP/Capita",    f"${latest.GDP_Per_Capita.mean():,.0f}",             "latest year",         "#E69F00"),
    ("Life Expectancy",   f"{latest.Life_Expectancy.mean():.1f} yrs",          "latest year",         "#009E73"),
    ("Unemployment",      f"{latest.Unemployment_Rate.mean():.1f}%",           "latest year",         "#CC79A7"),
    ("Avg CO₂/Capita",    f"{latest.CO2_Emissions_Per_Capita.mean():.1f} t",   "latest year",         "#56B4E9"),
]
for col, (label, val, sub, color) in zip(cols, kpi_data):
    col.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-label'>{label}</div>
      <div class='kpi-value' style='color:{color};'>{val}</div>
      <div class='kpi-sub'>{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "📈 Growth & Inequality",
    "🏭 Trade & CO₂",
    "🏥 Health & Education",
    "🗺️ World Map",
    "⚡ Crisis Analysis"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Growth & Inequality
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1,c2 = st.columns(2)

    # ── Q1: GDP line chart ────────────────────────────────────────────────────
    with c1:
        st.markdown("<div class='section-hdr'>GDP per Capita by Income Group</div>", unsafe_allow_html=True)
        q1 = dff.groupby(['Year','Income_Group'])['GDP_Per_Capita'].mean().reset_index()
        fig = go.Figure()
        ls = {'High income':dict(width=2.8,dash='solid'),
              'Upper middle income':dict(width=2.2,dash='solid'),
              'Lower middle income':dict(width=1.8,dash='dot'),
              'Low income':dict(width=1.8,dash='dot')}
        for ig in ['High income','Upper middle income','Lower middle income','Low income']:
            sub = q1[q1.Income_Group==ig]
            fig.add_trace(go.Scatter(
                x=sub['Year'], y=sub['GDP_Per_Capita'], name=ig,
                mode='lines', line=dict(color=INCOME_COLORS[ig],**ls[ig]),
                fill='tozeroy' if ig=='High income' else None,
                fillcolor='rgba(0,114,178,0.06)' if ig=='High income' else None,
                hovertemplate=f'<b>{ig}</b><br>Year: %{{x}}<br>GDP: $%{{y:,.0f}}<extra></extra>'
            ))
        fig.add_vrect(x0=2008,x1=2010,fillcolor='#D55E00',opacity=0.07,line_width=0,layer='below',
                      annotation_text='2008–09',annotation_font=dict(size=9,color='#D55E00'),
                      annotation_position='top left')
        fig.add_vrect(x0=2020,x1=2021,fillcolor='#CC79A7',opacity=0.10,line_width=0,layer='below',
                      annotation_text='COVID',annotation_font=dict(size=9,color='#CC79A7'),
                      annotation_position='top left')
        fig.update_layout(
            xaxis=dict(tickvals=list(range(2000,2024,4)),ticktext=[str(y) for y in range(2000,2024,4)],range=[2000,2025]),
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation='h',y=-0.22,x=0.5,xanchor='center',font=dict(size=9)),
            hovermode='x unified'
        )
        fig = cl(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 High-income gap widened after every crisis. Low-income remained below $2K throughout — a structural wealth trap.</div>", unsafe_allow_html=True)

    # ── Q2: Wealth vs Longevity ───────────────────────────────────────────────
    with c2:
        st.markdown("<div class='section-hdr'>Wealth vs Longevity — The Big Divide</div>", unsafe_allow_html=True)
        lat2 = dff[dff.Year==dff.Year.max()].copy()
        lat2['BubbleSize'] = np.sqrt(lat2['Population']/1e6).clip(upper=20)
        fig = go.Figure()
        for region in sorted(lat2.Region.unique()):
            sub = lat2[lat2.Region==region]
            fig.add_trace(go.Scatter(
                x=sub['GDP_Per_Capita'], y=sub['Life_Expectancy'],
                mode='markers', name=region,
                marker=dict(size=sub['BubbleSize']*2.2, color=REGION_COLORS[region],
                            opacity=0.80, line=dict(width=1,color='white')),
                customdata=sub[['Country','Income_Group']].values,
                hovertemplate='<b>%{customdata[0]}</b><br>GDP: $%{x:,.0f}<br>Life Exp: %{y:.1f} yrs<br>%{customdata[1]}<extra></extra>'
            ))
        fig.add_hline(y=75,line_dash='dot',line_color='#4A6080',line_width=1,
                      annotation_text='75 yr mark',annotation_font=dict(size=9,color='#4A6080'))
        fig.update_layout(
            xaxis=dict(tickformat='$,.0f', title='GDP per Capita (USD)'),
            yaxis=dict(title='Life Expectancy (yrs)', range=[58,88]),
            legend=dict(orientation='h',y=-0.22,x=0.5,xanchor='center',font=dict(size=9))
        )
        fig = cl(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 Africa lags 8–10 years in life expectancy at similar GDP levels to Asia — inequality beyond just income.</div>", unsafe_allow_html=True)

    # ── Q6: Unemployment area chart ───────────────────────────────────────────
    st.markdown("<div class='section-hdr'>Unemployment Recovery — Crisis Comparison by Region</div>", unsafe_allow_html=True)
    q6 = dff.groupby(['Year','Region'])['Unemployment_Rate'].mean().reset_index()
    fig = go.Figure()
    for region in sorted(q6.Region.unique()):
        sub = q6[q6.Region==region]
        fig.add_trace(go.Scatter(
            x=sub['Year'], y=sub['Unemployment_Rate'], name=region,
            mode='lines', fill='tozeroy',
            line=dict(color=REGION_COLORS[region], width=2),
            fillcolor={
                'Americas':'rgba(0,114,178,0.08)',
                'Europe':'rgba(230,159,0,0.08)',
                'Asia':'rgba(0,158,115,0.08)',
                'Africa':'rgba(204,121,167,0.08)',
                'Oceania':'rgba(86,180,233,0.08)'
            }.get(region,'rgba(0,114,178,0.06)'),
            hovertemplate=f'<b>{region}</b><br>Year: %{{x}}<br>Unemployment: %{{y:.1f}}%<extra></extra>'
        ))
    fig.add_vrect(x0=2008,x1=2010,fillcolor='#D55E00',opacity=0.07,line_width=0)
    fig.add_vrect(x0=2020,x1=2021,fillcolor='#CC79A7',opacity=0.08,line_width=0)
    fig.update_layout(
        xaxis=dict(tickvals=list(range(2000,2024,2))),
        yaxis=dict(ticksuffix='%', title='Avg Unemployment Rate'),
        legend=dict(orientation='h',y=-0.18,x=0.5,xanchor='center',font=dict(size=10)),
        hovermode='x unified'
    )
    fig = cl(fig, 300)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div class='insight'>💡 Asia recovered fastest after both crises. Africa consistently above 10%. Europe took 5+ years after 2008.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Trade & CO2
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    c1,c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-hdr'>Top Export-Dependent Economies</div>", unsafe_allow_html=True)
        yr = st.selectbox("Year", sorted(dff.Year.unique(),reverse=True), key='exp')
        q4 = dff[dff.Year==yr].nlargest(15,'Exports_PCT_GDP').copy()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=q4['Exports_PCT_GDP'], y=q4['Country'],
            orientation='h',
            marker=dict(
                color=q4['Region'].map(REGION_COLORS),
                opacity=0.88,
                line=dict(width=0)
            ),
            customdata=q4[['Region','Income_Group']].values,
            hovertemplate='<b>%{y}</b><br>Exports: %{x:.1f}% GDP<br>%{customdata[0]} · %{customdata[1]}<extra></extra>'
        ))
        fig.update_layout(
            yaxis=dict(categoryorder='total ascending'),
            xaxis=dict(title='Exports as % of GDP', ticksuffix='%'),
        )
        fig = cl(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 Singapore leads consistently. Most economies increased export reliance post-2008 as a recovery strategy.</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section-hdr'>GDP Growth vs CO₂ Change (2000–2022)</div>", unsafe_allow_html=True)
        try:
            yr_start = max(2000, dff.Year.min())
            yr_end   = min(2022, dff.Year.max())
            def pct_chg(col):
                return dff.groupby('Country').apply(
                    lambda x: (x[x.Year==yr_end][col].values[0]-x[x.Year==yr_start][col].values[0])
                              /x[x.Year==yr_start][col].values[0]*100
                    if len(x[x.Year==yr_end])>0 and len(x[x.Year==yr_start])>0 else np.nan
                ).reset_index(name=col+'_chg')
            gdp_c = pct_chg('GDP_Per_Capita')
            co2_c = pct_chg('CO2_Emissions_Per_Capita')
            q7 = gdp_c.merge(co2_c).merge(dff[dff.Year==yr_end][['Country','Region']].drop_duplicates()).dropna()
            q7 = q7[(q7.GDP_Per_Capita_chg<900)&(q7.CO2_Emissions_Per_Capita_chg.between(-90,400))]
            fig = go.Figure()
            fig.add_shape(type='rect',x0=0,x1=900,y0=-90,y1=0,
                          fillcolor='#009E73',opacity=0.05,line_width=0,layer='below')
            fig.add_shape(type='rect',x0=0,x1=900,y0=0,y1=400,
                          fillcolor='#D55E00',opacity=0.05,line_width=0,layer='below')
            for region in sorted(q7.Region.unique()):
                sub = q7[q7.Region==region]
                fig.add_trace(go.Scatter(
                    x=sub['GDP_Per_Capita_chg'], y=sub['CO2_Emissions_Per_Capita_chg'],
                    mode='markers', name=region,
                    marker=dict(size=11,color=REGION_COLORS[region],opacity=0.82,
                                line=dict(width=1,color='white')),
                    customdata=sub['Country'].values,
                    hovertemplate='<b>%{customdata}</b><br>GDP Growth: %{x:.0f}%<br>CO₂ Change: %{y:.0f}%<extra></extra>'
                ))
            fig.add_hline(y=0,line_dash='dot',line_color='#4A6080',line_width=1)
            fig.add_vline(x=0,line_dash='dot',line_color='#4A6080',line_width=1)
            fig.add_annotation(x=600,y=-50,text='✅ Decoupled',showarrow=False,
                               font=dict(color='#009E73',size=10),bgcolor=CARD,borderpad=3)
            fig.add_annotation(x=600,y=300,text='⚠️ Both Rising',showarrow=False,
                               font=dict(color='#D55E00',size=10),bgcolor=CARD,borderpad=3)
            fig.update_layout(
                xaxis=dict(title='GDP Growth (%)',ticksuffix='%'),
                yaxis=dict(title='CO₂ Change (%)',ticksuffix='%'),
                legend=dict(orientation='h',y=-0.22,x=0.5,xanchor='center',font=dict(size=9))
            )
            fig = cl(fig, 420)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<div class='insight'>💡 Europe decoupled — GDP grew while CO₂ fell. Asia grew both. Africa minimal change in either.</div>", unsafe_allow_html=True)
        except Exception as e:
            st.info(f"Adjust filters for this chart. ({e})")

    st.markdown("<div class='section-hdr'>CO₂ Emissions per Capita Trend by Income Group</div>", unsafe_allow_html=True)
    q_co2 = dff.groupby(['Year','Income_Group'])['CO2_Emissions_Per_Capita'].mean().reset_index()
    fig = go.Figure()
    for ig in ['High income','Upper middle income','Lower middle income','Low income']:
        sub = q_co2[q_co2.Income_Group==ig]
        fig.add_trace(go.Scatter(
            x=sub['Year'], y=sub['CO2_Emissions_Per_Capita'], name=ig,
            mode='lines+markers', marker=dict(size=4),
            line=dict(color=INCOME_COLORS[ig], width=2),
            hovertemplate=f'<b>{ig}</b><br>Year: %{{x}}<br>CO₂: %{{y:.1f}} t<extra></extra>'
        ))
    fig.update_layout(
        xaxis=dict(tickvals=list(range(2000,2024,2))),
        yaxis=dict(title='CO₂ per Capita (tonnes)', ticksuffix=' t'),
        legend=dict(orientation='h',y=-0.18,x=0.5,xanchor='center',font=dict(size=10)),
        hovermode='x unified'
    )
    fig = cl(fig, 280)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div class='insight'>💡 High-income CO₂ declining since 2010 — policy and green energy working. Low-income rising slightly as they develop.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Health & Education
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    sel_yr = st.selectbox("Select Year", sorted(dff.Year.unique(),reverse=True), key='hlth')

    c1,c2 = st.columns(2)

    # ── Q8: Health faceted ────────────────────────────────────────────────────
    with c1:
        st.markdown("<div class='section-hdr'>Health Spending vs Life Expectancy</div>", unsafe_allow_html=True)
        q8 = dff[dff.Year==sel_yr].copy()
        q8['BubbleSize'] = np.sqrt(q8['Population']/1e6).clip(upper=18)
        fig = make_subplots(rows=2,cols=2,
            subplot_titles=['High Income','Upper Middle','Lower Middle','Low Income'],
            horizontal_spacing=0.12, vertical_spacing=0.20)
        income_order = ['High income','Upper middle income','Lower middle income','Low income']
        for idx,ig in enumerate(income_order):
            row,col = idx//2+1, idx%2+1
            sub = q8[q8.Income_Group==ig]
            color = INCOME_COLORS[ig]
            fig.add_trace(go.Scatter(
                x=sub['Health_Spend_PCT_GDP'], y=sub['Life_Expectancy'],
                mode='markers', name=ig, showlegend=False,
                marker=dict(size=10,color=color,opacity=0.80,line=dict(width=1,color='white')),
                customdata=sub['Country'].values,
                hovertemplate='<b>%{customdata}</b><br>Health: %{x:.1f}%<br>Life: %{y:.1f} yrs<extra></extra>'
            ),row=row,col=col)
            if len(sub)>=3:
                m,b = np.polyfit(sub['Health_Spend_PCT_GDP'],sub['Life_Expectancy'],1)
                xl = np.linspace(sub['Health_Spend_PCT_GDP'].min(),sub['Health_Spend_PCT_GDP'].max(),50)
                fig.add_trace(go.Scatter(
                    x=xl,y=np.clip(m*xl+b,58,88),mode='lines',showlegend=False,
                    line=dict(color=color,width=2,dash='dash'),opacity=0.5,hoverinfo='skip'
                ),row=row,col=col)
        for ann in fig.layout.annotations:
            ann.font = dict(size=10,color=FONT,family='Arial')
        fig.update_xaxes(showgrid=True,gridcolor=GRID,tickfont=dict(size=9,color=FONT),
                         ticksuffix='%',linecolor=LINE,showline=True)
        fig.update_yaxes(showgrid=True,gridcolor=GRID,tickfont=dict(size=9,color=FONT),
                         range=[58,88],linecolor=LINE,showline=True)
        fig.update_layout(plot_bgcolor=BG,paper_bgcolor=BG,
                          font=dict(family='Arial',size=10,color=FONT),
                          height=420,margin=dict(l=40,r=20,t=50,b=30))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 Low-income gains most per health dollar. High-income shows diminishing returns above 8% GDP spend.</div>", unsafe_allow_html=True)

    # ── Q5: Education vs GDP ──────────────────────────────────────────────────
    with c2:
        st.markdown("<div class='section-hdr'>Education Spend → GDP Outcome (10-yr lag)</div>", unsafe_allow_html=True)
        edu_yr  = max(2010, dff.Year.min())
        gdp_yr  = min(edu_yr+10, dff.Year.max())
        edu_df  = df[df.Year==edu_yr].groupby('Country').agg(
            Education_Spend_PCT_GDP=('Education_Spend_PCT_GDP','mean'),
            Income_Group=('Income_Group','first'),Region=('Region','first')).reset_index()
        gdp_df  = df[df.Year==gdp_yr].groupby('Country')['GDP_Per_Capita'].mean().reset_index()
        q5      = edu_df.merge(gdp_df,on='Country',how='inner')
        fig = go.Figure()
        fig.add_shape(type='rect',x0=0.5,x1=4,y0=0,y1=15000,
                      fillcolor='#D55E00',opacity=0.05,line_width=0,layer='below')
        fig.add_shape(type='rect',x0=4,x1=9.5,y0=20000,y1=145000,
                      fillcolor='#009E73',opacity=0.05,line_width=0,layer='below')
        for ig in income_order:
            sub = q5[q5.Income_Group==ig]
            if len(sub)==0: continue
            color = INCOME_COLORS[ig]
            fig.add_trace(go.Scatter(
                x=sub['Education_Spend_PCT_GDP'],y=sub['GDP_Per_Capita'],
                mode='markers',name=ig,
                marker=dict(size=10,color=color,opacity=0.82,line=dict(width=1,color='white')),
                customdata=sub['Country'].values,
                hovertemplate='<b>%{customdata}</b><br>Edu Spend: %{x:.1f}%<br>GDP: $%{y:,.0f}<extra></extra>'
            ))
            if len(sub)>=3:
                m,b = np.polyfit(sub['Education_Spend_PCT_GDP'],sub['GDP_Per_Capita'],1)
                xl = np.linspace(sub['Education_Spend_PCT_GDP'].min(),sub['Education_Spend_PCT_GDP'].max(),60)
                fig.add_trace(go.Scatter(
                    x=xl,y=np.clip(m*xl+b,0,145000),mode='lines',showlegend=False,
                    line=dict(color=color,width=1.8,dash='dash'),opacity=0.5,hoverinfo='skip'
                ))
        fig.add_hline(y=20000,line_dash='dot',line_color='#4A6080',line_width=1)
        fig.add_vline(x=4.0,line_dash='dot',line_color='#4A6080',line_width=1)
        fig.update_layout(
            xaxis=dict(title=f'Education Spend % GDP ({edu_yr})',ticksuffix='%',range=[0.5,9.5]),
            yaxis=dict(title=f'GDP per Capita USD ({gdp_yr})',tickformat='$,.0f',range=[0,145000]),
            legend=dict(orientation='h',y=-0.22,x=0.5,xanchor='center',font=dict(size=9))
        )
        fig = cl(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 Clear positive trend — education investment pays off 10 years later. Low-income stuck in bottom-left trap.</div>", unsafe_allow_html=True)

    # ── Internet animation ────────────────────────────────────────────────────
    st.markdown("<div class='section-hdr'>Internet Penetration vs GDP — Developing Nations (Animated)</div>", unsafe_allow_html=True)
    # Use every 3rd year to reduce congestion
    years_anim = sorted(dff[dff.Income_Group.isin(['Lower middle income','Low income'])].Year.unique())[::3]
    q9 = dff[dff.Income_Group.isin(['Lower middle income','Low income']) & dff.Year.isin(years_anim)].copy()
    q9['BubbleSize'] = np.sqrt(q9['Population']/1e6).clip(upper=25)
    fig = px.scatter(q9, x='Internet_Users_PCT', y='GDP_Per_Capita',
                     color='Region', animation_frame='Year', hover_name='Country',
                     size='BubbleSize', color_discrete_map=REGION_COLORS, size_max=35,
                     range_x=[0,100], range_y=[0,8000],
                     labels={'Internet_Users_PCT':'Internet Users (%)','GDP_Per_Capita':'GDP per Capita (USD)'})
    fig = cl(fig, 360)
    fig.update_layout(
        xaxis=dict(ticksuffix='%'),
        yaxis=dict(tickformat='$,.0f'),
        legend=dict(orientation='h',y=-0.2,x=0.5,xanchor='center',font=dict(size=10))
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div class='insight'>💡 Press ▶ to animate. Every 10% internet gain = ~$300 GDP per capita in developing nations. Asia moves fastest.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — World Map
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    c1,c2 = st.columns([2,1])
    with c1:
        indicator = st.selectbox("Indicator", [
            'GDP_Per_Capita','Life_Expectancy','Unemployment_Rate','Inflation_Rate',
            'CO2_Emissions_Per_Capita','Internet_Users_PCT',
            'Education_Spend_PCT_GDP','Health_Spend_PCT_GDP','Exports_PCT_GDP'
        ], format_func=lambda x: x.replace('_',' '))
    with c2:
        map_yr = st.slider("Year", 2000, 2023, 2022, key='map')

    map_df = dff[dff.Year==map_yr].copy()
    map_df['ISO3'] = map_df['Country'].map(ISO_MAP)
    map_df = map_df.dropna(subset=['ISO3'])
    map_df['GDP_Formatted'] = map_df['GDP_Per_Capita'].apply(lambda x: f"${x:,.0f}")

    fig = px.choropleth(
        map_df, locations='ISO3', color=indicator, hover_name='Country',
        hover_data={indicator:False,'GDP_Formatted':True,'Income_Group':True,'Life_Expectancy':True},
        color_continuous_scale=[[0,'#1a0a00'],[0.1,'#7B3F00'],[0.3,'#F4A460'],
                                  [0.55,'#87CEEB'],[0.75,'#4169E1'],[1.0,'#00008B']],
        labels={indicator:indicator.replace('_',' '),'GDP_Formatted':'GDP per Capita','Income_Group':'Income Group'}
    )
    fig.update_traces(marker_line_color='white', marker_line_width=0.4)
    fig.update_layout(
        geo=dict(showframe=False,showcoastlines=True,coastlinecolor='#3A5070',
                 showland=True,landcolor='#1E2D4A',showocean=True,oceancolor='#0B1120',
                 showcountries=True,countrycolor='#2A3F5F',countrywidth=0.3,
                 projection_type='natural earth',bgcolor=BG),
        coloraxis_colorbar=dict(
            tickformat='$,.0f' if 'GDP' in indicator else None,
            len=0.72, thickness=13, x=1.01,
            bgcolor='rgba(13,31,60,0.85)', bordercolor=LINE,
            tickfont=dict(color=FONT,size=9),
            title=dict(text=indicator.replace('_',' '),font=dict(color=FONT,size=10))
        ),
        title=dict(text=f"{indicator.replace('_',' ')} · {map_yr}",
                   font=dict(size=13,color='#4FC3F7'),x=0.5,xanchor='center'),
        paper_bgcolor=BG, font=dict(color=FONT,family='Arial'),
        height=520, margin=dict(l=0,r=10,t=45,b=5)
    )
    fig.add_trace(go.Scattergeo(
        locations=map_df['ISO3'], mode='markers',
        marker=dict(size=6,color='#4FC3F7',opacity=0.6,
                    line=dict(width=0.5,color='white'),showscale=False),
        text=map_df['Country'],
        customdata=map_df[['GDP_Formatted','Income_Group','Life_Expectancy']].values,
        hovertemplate='<b>%{text}</b><br>GDP: %{customdata[0]}<br>%{customdata[1]}<br>Life Exp: %{customdata[2]} yrs<extra></extra>',
        showlegend=False
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div class='insight'>💡 North-South wealth divide persists. Change the indicator above to explore health, education, CO₂ and more across any year.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Crisis Analysis
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-hdr'>COVID-19 Economic Impact vs Recovery</div>", unsafe_allow_html=True)
    try:
        pre   = dff[dff.Year==2019].set_index('Country')['GDP_Per_Capita']
        hit   = dff[dff.Year==2020].set_index('Country')['GDP_Per_Capita']
        rec   = dff[dff.Year==2022].set_index('Country')['GDP_Per_Capita']
        q10   = pd.DataFrame({
            'COVID Impact (%)':   ((hit-pre)/pre*100),
            'Recovery (%)':       ((rec-pre)/pre*100)
        }).reset_index()
        q10   = q10.merge(dff[dff.Year==2020][['Country','Region','Income_Group']].drop_duplicates()).dropna()
        q10s  = q10.sort_values('COVID Impact (%)').head(30)
        fig   = go.Figure()
        fig.add_trace(go.Bar(name='GDP Drop 2020 vs 2019',
            x=q10s['Country'], y=q10s['COVID Impact (%)'],
            marker=dict(color='#D55E00',opacity=0.85,line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>COVID Impact: %{y:.1f}%<extra></extra>'))
        fig.add_trace(go.Bar(name='Recovery 2022 vs 2019',
            x=q10s['Country'], y=q10s['Recovery (%)'],
            marker=dict(color='#009E73',opacity=0.85,line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>Recovery: %{y:.1f}%<extra></extra>'))
        fig.add_hline(y=0,line_color='#4A6080',line_width=1)
        fig.update_layout(barmode='group',
            xaxis=dict(tickangle=40,tickfont=dict(size=9)),
            yaxis=dict(title='GDP per Capita Change (%)',ticksuffix='%'),
            legend=dict(orientation='h',y=-0.28,x=0.5,xanchor='center',font=dict(size=10))
        )
        fig = cl(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 Venezuela and Argentina hardest hit. Asian economies recovered above pre-COVID levels by 2022. European recovery slower.</div>", unsafe_allow_html=True)
    except:
        st.info("Select year range 2019–2023 to see COVID analysis.")

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-hdr'>Inflation Surge 2018–2023</div>", unsafe_allow_html=True)
        inf_df = dff[dff.Year>=2018].groupby(['Year','Region'])['Inflation_Rate'].mean().reset_index()
        fig = go.Figure()
        for region in sorted(inf_df.Region.unique()):
            sub = inf_df[inf_df.Region==region]
            fig.add_trace(go.Scatter(
                x=sub['Year'],y=sub['Inflation_Rate'],name=region,mode='lines+markers',
                line=dict(color=REGION_COLORS[region],width=2.2),
                marker=dict(size=6,color=REGION_COLORS[region],line=dict(width=1,color='white')),
                hovertemplate=f'<b>{region}</b><br>Year: %{{x}}<br>Inflation: %{{y:.1f}}%<extra></extra>'
            ))
        fig.update_layout(
            yaxis=dict(ticksuffix='%',title='Avg Inflation Rate'),
            legend=dict(orientation='h',y=-0.22,x=0.5,xanchor='center',font=dict(size=10)),
            hovermode='x unified'
        )
        fig = cl(fig, 320)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 2022 energy crisis drove inflation to multi-decade highs. Africa and Americas hit hardest.</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section-hdr'>GDP Growth — 2008 Crisis vs COVID 2020</div>", unsafe_allow_html=True)
        crisis_df = dff[dff.Year.isin([2009,2020])].copy()
        crisis_df['Crisis'] = crisis_df['Year'].map({2009:'2008–09 Crisis',2020:'COVID-19 2020'})
        qc = crisis_df.groupby(['Crisis','Region'])['GDP_Growth_Rate'].mean().reset_index()
        fig = go.Figure()
        for crisis,color in [('2008–09 Crisis','#D55E00'),('COVID-19 2020','#CC79A7')]:
            sub = qc[qc.Crisis==crisis]
            fig.add_trace(go.Bar(
                x=sub['Region'],y=sub['GDP_Growth_Rate'],name=crisis,
                marker=dict(color=color,opacity=0.85,line=dict(width=0)),
                hovertemplate=f'<b>%{{x}}</b><br>{crisis}: %{{y:.1f}}%<extra></extra>'
            ))
        fig.add_hline(y=0,line_color='#4A6080',line_width=1)
        fig.update_layout(
            barmode='group',
            yaxis=dict(ticksuffix='%',title='Avg GDP Growth Rate'),
            legend=dict(orientation='h',y=-0.22,x=0.5,xanchor='center',font=dict(size=10))
        )
        fig = cl(fig, 320)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='insight'>💡 COVID hit harder and faster than 2008 in every region — but recovery was also faster due to unprecedented fiscal stimulus.</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;color:#2A3F5F;font-size:0.72rem;padding:10px 0;border-top:1px solid #1E2D4A;margin-top:16px;'>
  🌍 Global Economy Intelligence · Data Visualization · Summer 2026 · 50 Countries · 2000–2023 · 15 Indicators
</div>""", unsafe_allow_html=True)
