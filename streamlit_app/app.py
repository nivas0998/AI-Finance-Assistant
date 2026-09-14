import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import html

API = "https://ai-finance-assistant-xuf9.onrender.com"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Education", "Other"]

st.set_page_config(page_title="AI Finance Assistant", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")

# -----------------------------------------------------------------------------
# POLISHED FINTECH THEME — rebuilt from the original React dashboard structure.
# Includes hover/highlight states and a cursor-follow glow approximation.
# -----------------------------------------------------------------------------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--bg:#070b14;--panel:#0d1422;--panel2:#101827;--line:#1b2738;--muted:#8290a5;--text:#f4f7fb;--blue:#4f7cff;--purple:#8b5cf6;--green:#22c55e;--red:#ef4444;--cyan:#06b6d4;}
html,body,[class*="css"]{font-family:Inter,system-ui,sans-serif!important}
.stApp{background:#070b14;color:var(--text)}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;background:radial-gradient(500px circle at 50% 35%,rgba(79,124,255,.075),transparent 70%);z-index:0}
.block-container{max-width:1180px;padding:0 1.4rem 4rem;position:relative;z-index:1}
header[data-testid="stHeader"]{background:rgba(7,11,20,.82)!important;backdrop-filter:blur(18px);height:0}
#MainMenu,footer{visibility:hidden}
section[data-testid="stSidebar"]{display:none}
.stButton>button,.stDownloadButton>button{border-radius:10px!important;border:1px solid #24324a!important;background:#101827!important;color:#eaf0f8!important;font-weight:600!important;transition:all .22s ease!important;box-shadow:none!important}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:#4f7cff!important;background:#162238!important;transform:translateY(-1px);box-shadow:0 0 25px rgba(79,124,255,.14)!important}
button[kind="primary"]{background:linear-gradient(135deg,#4f7cff,#6c55ff)!important;border:none!important;box-shadow:0 8px 25px rgba(79,124,255,.18)!important}
button[kind="primary"]:hover{box-shadow:0 10px 32px rgba(79,124,255,.3)!important}
input,textarea,[data-baseweb="select"]>div{background:#0b1220!important;color:#f4f7fb!important;border:1px solid #202d41!important;border-radius:10px!important}
input:focus,textarea:focus{border-color:#4f7cff!important;box-shadow:0 0 0 1px #4f7cff,0 0 22px rgba(79,124,255,.12)!important}
label{color:#9aa8bb!important;font-size:.82rem!important}
[data-testid="stMetric"]{background:transparent}
hr{border-color:#1b2738!important}

.navbar{height:70px;margin:0 -1.4rem 42px;padding:0 1.4rem;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(37,50,70,.8);background:rgba(7,11,20,.72);backdrop-filter:blur(18px);position:sticky;top:0;z-index:20}
.brand{display:flex;align-items:center;gap:11px}.brand-mark{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;background:linear-gradient(135deg,#4f7cff,#8b5cf6);box-shadow:0 0 28px rgba(79,124,255,.24);font-size:20px}.brand-name strong{display:block;font-size:15px;letter-spacing:-.2px}.brand-name span{display:block;font-size:11px;color:#7f8da2;margin-top:1px}.welcome{display:flex;align-items:center;gap:18px}.welcome-text{text-align:right}.welcome-text span{display:block;color:#748197;font-size:10px}.welcome-text strong{display:block;font-size:13px;margin-top:2px}.logout-chip{display:inline-flex;align-items:center;gap:7px;padding:9px 13px;border:1px solid #26344a;border-radius:10px;color:#d8dfeb;font-size:12px}
.eyebrow{color:#6d8cff;font-size:10px;font-weight:800;letter-spacing:2px;margin:0 0 8px}.hero{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:25px}.hero h1{font-size:31px;line-height:1.15;margin:0;font-weight:800;letter-spacing:-1.1px}.hero p{color:#7d8ba0;margin:9px 0 0;font-size:13px}.hero-action{min-width:115px}
.summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:18px}.summary-card{background:linear-gradient(145deg,#0d1523,#0b111c);border:1px solid #1b283a;border-radius:15px;padding:20px;display:flex;align-items:center;gap:14px;position:relative;overflow:hidden;transition:.25s}.summary-card:after{content:"";position:absolute;inset:-60%;background:radial-gradient(circle,rgba(79,124,255,.08),transparent 55%);opacity:0;transition:.25s}.summary-card:hover{transform:translateY(-3px);border-color:#2d4260;box-shadow:0 14px 40px rgba(0,0,0,.22),0 0 25px rgba(79,124,255,.07)}.summary-card:hover:after{opacity:1}.summary-icon{width:43px;height:43px;border-radius:12px;display:grid;place-items:center;font-size:20px;position:relative;z-index:1}.income{background:rgba(34,197,94,.12);color:#4ade80}.expense{background:rgba(239,68,68,.12);color:#f87171}.balance{background:rgba(79,124,255,.13);color:#7596ff}.summary-copy{position:relative;z-index:1}.summary-copy span{font-size:11px;color:#7d8ba0}.summary-copy h2{font-size:24px;margin:5px 0 0;letter-spacing:-.7px}.money{font-variant-numeric:tabular-nums}
.panel{background:linear-gradient(145deg,#0d1523,#0a111c);border:1px solid #1b283a;border-radius:16px;padding:21px;margin-top:16px;transition:.25s}.panel:hover{border-color:#253750;box-shadow:0 12px 35px rgba(0,0,0,.16)}.panel-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}.panel-label{font-size:9px;letter-spacing:1.8px;font-weight:800;color:#7183a0;margin:0 0 5px}.panel-title{font-size:17px;font-weight:700;margin:0;display:flex;align-items:center;gap:8px}.panel-sub{font-size:11px;color:#6f7d91;margin:5px 0 0}.ai-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.insight{display:flex;gap:11px;padding:14px;border:1px solid #1b283a;background:#0b1220;border-radius:12px;transition:.22s}.insight:hover{transform:translateY(-2px);border-color:#314764;background:#0d1626}.insight-icon{width:32px;height:32px;border-radius:9px;display:grid;place-items:center;flex:none}.insight strong{font-size:12px}.insight p{font-size:11px;line-height:1.55;color:#7e8ca0;margin:4px 0 0}.positive .insight-icon{color:#4ade80;background:rgba(34,197,94,.1)}.warning .insight-icon,.budget .insight-icon{color:#fbbf24;background:rgba(245,158,11,.1)}.category .insight-icon{color:#fb7185;background:rgba(239,68,68,.1)}.tip .insight-icon{color:#a78bfa;background:rgba(139,92,246,.1)}.info .insight-icon{color:#60a5fa;background:rgba(6,182,212,.1)}.disclaimer{display:flex;align-items:center;gap:7px;color:#64748b;font-size:10px;margin-top:15px;padding-top:13px;border-top:1px solid #182436}
.two-col{display:grid;grid-template-columns:1.12fr .88fr;gap:16px}.chart-wrap{height:285px}.budget-item{padding:14px 0;border-bottom:1px solid #172235}.budget-item:last-child{border-bottom:0}.budget-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.budget-top strong{font-size:12px}.budget-top span{font-size:10px;color:#77859a}.progress{height:7px;background:#162133;border-radius:20px;overflow:hidden}.progress>div{height:100%;border-radius:20px;background:linear-gradient(90deg,#4f7cff,#8b5cf6)}.progress.over>div{background:linear-gradient(90deg,#ef4444,#f59e0b)}
.section-title{font-size:18px;font-weight:700;margin:0 0 13px}.mini-note{font-size:10px;color:#68778c}.tx-card{background:#0b1220;border:1px solid #1b283a;border-radius:12px;padding:12px 14px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;transition:.2s}.tx-card:hover{border-color:#2b405d;transform:translateX(2px)}.tx-left{display:flex;align-items:center;gap:11px}.tx-dot{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:#111d30;color:#7392ff;font-size:15px}.tx-desc{font-size:12px;font-weight:600}.tx-meta{font-size:10px;color:#69778b;margin-top:3px}.tx-amount{font-size:12px;font-weight:700}.tx-expense{color:#f87171}.tx-income{color:#4ade80}
.chat-launch{position:fixed;right:28px;bottom:26px;z-index:50;width:55px;height:55px;border-radius:17px;background:linear-gradient(135deg,#4f7cff,#8b5cf6);box-shadow:0 12px 35px rgba(79,124,255,.35);display:grid;place-items:center;color:white;font-size:22px}
.login-shell{min-height:100vh;display:grid;place-items:center;padding:30px}.login-box{width:min(460px,100%);background:linear-gradient(145deg,rgba(15,24,39,.98),rgba(9,15,25,.98));border:1px solid #1e2d43;border-radius:20px;padding:34px;box-shadow:0 30px 90px rgba(0,0,0,.4),0 0 50px rgba(79,124,255,.08);position:relative;overflow:hidden}.login-box:before{content:"";position:absolute;width:240px;height:240px;right:-120px;top:-120px;background:radial-gradient(circle,rgba(79,124,255,.18),transparent 68%);pointer-events:none}.login-brand{display:flex;justify-content:center;margin-bottom:16px}.login-title{text-align:center;font-size:25px;font-weight:800}.login-sub{text-align:center;color:#738198;font-size:12px;margin:7px 0 25px}.tabs{display:flex;gap:7px;background:#09101c;padding:5px;border-radius:11px;margin-bottom:20px}.tabs .stButton{flex:1}.tabs .stButton>button{border:0!important;background:transparent!important}.tabs .stButton>button:hover{background:#131e30!important}.small-link{text-align:center;color:#627189;font-size:10px;margin-top:15px}
[data-testid="stForm"]{border:0!important;padding:0!important}
@media(max-width:850px){.summary-grid,.two-col,.ai-grid{grid-template-columns:1fr}.hero{align-items:flex-start;gap:15px;flex-direction:column}.navbar{margin-bottom:25px}.welcome-text{display:none}}

/* ===== LOGIN SCREEN — VISIBLE STREAMLIT CARD ===== */
.login-bg-glow{position:fixed;pointer-events:none;border-radius:50%;filter:blur(12px);z-index:0}
.glow-a{width:420px;height:420px;left:-170px;top:15%;background:radial-gradient(circle,rgba(79,124,255,.13),transparent 68%);animation:loginFloatA 8s ease-in-out infinite alternate}
.glow-b{width:520px;height:520px;right:-220px;bottom:-120px;background:radial-gradient(circle,rgba(139,92,246,.11),transparent 68%);animation:loginFloatB 10s ease-in-out infinite alternate}
@keyframes loginFloatA{from{transform:translate(0,0) scale(.9)}to{transform:translate(90px,55px) scale(1.12)}}
@keyframes loginFloatB{from{transform:translate(0,0) scale(1)}to{transform:translate(-70px,-45px) scale(.88)}}
.login-heading{text-align:center;position:relative;z-index:2;padding-top:105px;margin-bottom:22px}
.login-orbit{width:68px;height:68px;margin:0 auto 17px;border-radius:20px;padding:1px;background:linear-gradient(135deg,#4f7cff,#8b5cf6);box-shadow:0 0 45px rgba(79,124,255,.22);animation:loginPulse 3s ease-in-out infinite}
.login-brain{width:100%;height:100%;border-radius:19px;display:grid;place-items:center;background:#0d1523;font-size:29px}
@keyframes loginPulse{0%,100%{transform:translateY(0);box-shadow:0 0 30px rgba(79,124,255,.2)}50%{transform:translateY(-3px);box-shadow:0 0 48px rgba(139,92,246,.3)}}
.login-title{font-family:'Space Grotesk',sans-serif!important;font-size:29px;font-weight:700;letter-spacing:-.8px;color:#f5f7fb}
.login-sub{color:#77869c;font-size:12px;margin-top:7px}
.login-card-top{height:1px}
.login-divider{height:1px;background:linear-gradient(90deg,transparent,#1f2d42,transparent);margin:17px 0 20px}
.login-footer{text-align:center;color:#5f6e84;font-size:10px;padding:17px 0 4px}
/* Style the actual centered widget column as the glass card. */
.login-heading + div [data-testid="stVerticalBlock"]{background:linear-gradient(145deg,rgba(15,24,39,.94),rgba(8,14,24,.96));border:1px solid rgba(42,58,82,.85);border-radius:22px;padding:27px 29px 20px;box-shadow:0 30px 90px rgba(0,0,0,.42),0 0 60px rgba(79,124,255,.06);position:relative;overflow:hidden}
.login-heading + div [data-testid="stVerticalBlock"]:before{content:"";position:absolute;width:260px;height:260px;right:-160px;top:-160px;border-radius:50%;background:radial-gradient(circle,rgba(79,124,255,.16),transparent 68%);pointer-events:none}
.login-heading + div [data-testid="stVerticalBlock"] > div{position:relative;z-index:1}
</style>
<style>
/* ===== FINAL VISUAL POLISH ===== */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--glow:#5b7cff;--violet:#8b5cf6;--cyan:#22d3ee;--surface:rgba(13,21,35,.78)}
html,body,[class*="css"]{font-family:'DM Sans',Inter,system-ui,sans-serif!important}
h1,h2,h3,.hero h1,.panel-title,.section-title,.brand-name strong,.login-title{font-family:'Space Grotesk','DM Sans',sans-serif!important}
body,.stApp{cursor:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'%3E%3Cdefs%3E%3CradialGradient id='g'%3E%3Cstop offset='0' stop-color='%23ffffff'/%3E%3Cstop offset='.18' stop-color='%235b7cff'/%3E%3Cstop offset='.55' stop-color='%238b5cf6' stop-opacity='.65'/%3E%3Cstop offset='1' stop-color='%235b7cff' stop-opacity='0'/%3E%3C/radialGradient%3E%3Cfilter id='b'%3E%3CfeGaussianBlur stdDeviation='1.5'/%3E%3C/filter%3E%3C/defs%3E%3Ccircle cx='14' cy='14' r='12' fill='url(%23g)' filter='url(%23b)'/%3E%3Ccircle cx='14' cy='14' r='3' fill='white'/%3E%3C/svg%3E") 14 14,auto!important}
.stApp{overflow-x:hidden;background:
 radial-gradient(900px 500px at 8% 8%,rgba(79,124,255,.11),transparent 60%),
 radial-gradient(800px 500px at 92% 35%,rgba(139,92,246,.09),transparent 62%),
 radial-gradient(700px 400px at 50% 100%,rgba(6,182,212,.055),transparent 65%),#070b14!important}
.stApp:after{content:"";position:fixed;width:420px;height:420px;left:-210px;top:35%;border-radius:50%;background:radial-gradient(circle,rgba(79,124,255,.09),transparent 68%);filter:blur(10px);animation:floatGlow 9s ease-in-out infinite alternate;pointer-events:none;z-index:0}
@keyframes floatGlow{from{transform:translate(0,-25px) scale(.9);opacity:.45}to{transform:translate(55px,35px) scale(1.18);opacity:.9}}
.block-container{padding-top:0!important}
.navbar{box-shadow:0 12px 45px rgba(0,0,0,.25),0 1px 0 rgba(91,124,255,.06);}
.brand-mark{animation:brandPulse 3s ease-in-out infinite;position:relative}
.brand-mark:after{content:"";position:absolute;inset:-5px;border-radius:15px;border:1px solid rgba(91,124,255,.25);animation:ring 2.5s ease-out infinite}
@keyframes brandPulse{0%,100%{box-shadow:0 0 24px rgba(79,124,255,.22)}50%{box-shadow:0 0 38px rgba(139,92,246,.42)}}
@keyframes ring{0%{transform:scale(.9);opacity:.7}100%{transform:scale(1.35);opacity:0}}
.hero h1{background:linear-gradient(90deg,#fff 0%,#dce5ff 45%,#9eb3ff 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 0 28px rgba(91,124,255,.08)}
.eyebrow{animation:eyebrowGlow 3s ease-in-out infinite}
@keyframes eyebrowGlow{50%{text-shadow:0 0 16px rgba(109,140,255,.55)}}
.summary-card,.panel,.insight,.tx-card{backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)}
.summary-card{isolation:isolate}
.summary-card:before,.panel:before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;background:linear-gradient(120deg,rgba(91,124,255,.28),transparent 35%,rgba(139,92,246,.18),transparent 75%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;opacity:.55}
.summary-card:hover{border-color:rgba(91,124,255,.55)!important;box-shadow:0 18px 50px rgba(0,0,0,.32),0 0 35px rgba(91,124,255,.14)!important}
.summary-card:hover .summary-icon{transform:scale(1.08) rotate(-3deg);box-shadow:0 0 25px rgba(91,124,255,.16)}
.summary-icon{transition:.28s ease}
.panel{position:relative;overflow:hidden}
.panel:hover{transform:translateY(-1px);border-color:rgba(91,124,255,.35)!important;box-shadow:0 18px 55px rgba(0,0,0,.23),0 0 30px rgba(79,124,255,.055)!important}
.insight{position:relative;overflow:hidden}
.insight:after{content:"";position:absolute;left:-80%;top:0;width:55%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.055),transparent);transform:skewX(-18deg);transition:.55s}
.insight:hover:after{left:130%}
.insight:hover .insight-icon{box-shadow:0 0 20px currentColor}
.progress{box-shadow:inset 0 0 8px rgba(0,0,0,.28)}
.progress>div{box-shadow:0 0 13px rgba(91,124,255,.45);animation:progressGlow 2.5s ease-in-out infinite alternate}
@keyframes progressGlow{to{box-shadow:0 0 21px rgba(139,92,246,.7)}}
.stButton>button{font-family:'DM Sans',sans-serif!important;position:relative;overflow:hidden}
.stButton>button:after{content:"";position:absolute;top:-80%;left:-25%;width:20%;height:260%;background:rgba(255,255,255,.08);transform:rotate(20deg);transition:.55s}
.stButton>button:hover:after{left:125%}
button[kind="primary"]{background:linear-gradient(110deg,#4f7cff,#7658ff,#8b5cf6)!important;background-size:180% 180%!important;animation:buttonShift 5s ease infinite}
@keyframes buttonShift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
input,textarea,[data-baseweb="select"]>div{box-shadow:inset 0 1px 0 rgba(255,255,255,.025),0 5px 18px rgba(0,0,0,.08)!important}
input:hover,textarea:hover,[data-baseweb="select"]>div:hover{border-color:#334a6b!important;box-shadow:0 0 20px rgba(79,124,255,.07)!important}
.login-box{animation:loginIn .65s cubic-bezier(.2,.8,.2,1);}
@keyframes loginIn{from{opacity:0;transform:translateY(18px) scale(.98)}to{opacity:1;transform:none}}
.login-box:after{content:"";position:absolute;inset:-2px;border-radius:22px;background:linear-gradient(120deg,rgba(79,124,255,.28),transparent 30%,rgba(139,92,246,.2),transparent 70%);z-index:-1;filter:blur(18px);opacity:.55}
.chat-launch{animation:chatPulse 2.2s ease-in-out infinite;}
@keyframes chatPulse{0%,100%{box-shadow:0 12px 35px rgba(79,124,255,.3)}50%{box-shadow:0 12px 45px rgba(139,92,246,.52),0 0 22px rgba(79,124,255,.25)}}
/* Streamlit widget chrome cleanup */
[data-testid="stVerticalBlock"]{position:relative}
[data-testid="stPlotlyChart"]{border-radius:12px;overflow:hidden}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}

/* REQUESTED LANDING PAGE THEME */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,.stApp,[class*="css"]{font-family:'Manrope',Inter,system-ui,sans-serif!important}
body,.stApp{cursor:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'%3E%3Cdefs%3E%3CradialGradient id='g'%3E%3Cstop stop-color='%236f91ff' stop-opacity='.95'/%3E%3Cstop offset='.38' stop-color='%235b7dff' stop-opacity='.5'/%3E%3Cstop offset='1' stop-color='%235b7dff' stop-opacity='0'/%3E%3C/radialGradient%3E%3C/defs%3E%3Ccircle cx='14' cy='14' r='13' fill='url(%23g)'/%3E%3Ccircle cx='14' cy='14' r='2.7' fill='%23fff'/%3E%3C/svg%3E") 14 14,auto!important}
.block-container{max-width:1500px!important;padding:0 74px 0!important}
.landing-divider{height:1px;background:rgba(38,48,70,.48);margin:0 -74px}.site-brand{height:74px;display:flex;align-items:center;gap:12px}.site-logo{width:42px;height:42px;border:1px solid #29427a;border-radius:12px;display:grid;place-items:center;color:#73a0ff;font-size:26px;background:rgba(24,38,68,.42);box-shadow:0 0 22px rgba(79,124,255,.12);animation:logoPulse 3s infinite}.site-brand-name{font-weight:800;font-size:17px;color:#f6f8fd;letter-spacing:-.4px}.site-nav-links{height:74px;display:flex;align-items:center;justify-content:center;gap:42px;color:#8c97aa;font-size:13px}.site-nav-links span{transition:.25s}.site-nav-links span:hover{color:#dbe5ff;text-shadow:0 0 14px rgba(100,130,255,.4)}@keyframes logoPulse{50%{box-shadow:0 0 34px rgba(79,124,255,.28)}}
.stButton>button{font-family:'Manrope',sans-serif!important;border-radius:11px!important;border:1px solid #24324d!important;background:rgba(13,21,36,.75)!important;color:#dfe7f6!important;font-size:13px!important;font-weight:700!important;height:44px!important;transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease,background .25s ease!important;position:relative;overflow:hidden}.stButton>button:hover{transform:translateY(-2px)!important;border-color:#3d5e9a!important;background:#121e34!important;box-shadow:0 10px 30px rgba(0,0,0,.24),0 0 24px rgba(79,124,255,.13)!important}.stButton>button:after{content:"";position:absolute;top:-120%;left:-35%;width:18%;height:340%;background:rgba(255,255,255,.12);transform:rotate(20deg);transition:left .65s ease;pointer-events:none}.stButton>button:hover:after{left:125%}button[kind="primary"]{background:linear-gradient(110deg,#4f7cff,#5c6fff,#775cff)!important;border:0!important;color:#fff!important;box-shadow:0 10px 28px rgba(66,101,230,.27)!important;background-size:180% 180%!important;animation:buttonGradient 5s ease infinite}button[kind="primary"]:hover{box-shadow:0 14px 38px rgba(79,124,255,.4)!important}@keyframes buttonGradient{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.hero-copy{padding-top:120px;position:relative;z-index:3}.hero-pill{display:inline-flex;align-items:center;gap:9px;border:1px solid #233b70;border-radius:22px;padding:9px 15px;color:#83a2ff;background:rgba(13,25,52,.42);font-size:12px;font-weight:600;box-shadow:inset 0 0 18px rgba(79,124,255,.04),0 0 20px rgba(79,124,255,.04)}.spark{font-size:17px}.hero-copy h1{font-size:72px;line-height:.98;letter-spacing:-4px;margin:42px 0 34px;font-weight:800;color:#f9fbff;text-shadow:0 5px 35px rgba(0,0,0,.2)}.hero-copy h1 span{background:linear-gradient(100deg,#eef3ff 3%,#b7c7ff 34%,#557cff 85%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 0 40px rgba(86,124,255,.15)}.hero-description{font-size:16px;line-height:2.05;color:#8f9aae;margin:0 0 38px;letter-spacing:.05px}.trust-line{font-size:11px;color:#65738a;margin-top:26px;display:flex;align-items:center;gap:8px}.shield{color:#6e94ff;font-size:17px}
.preview-window{margin-top:108px;border:1px solid #29354b;border-radius:22px;background:linear-gradient(145deg,rgba(14,20,33,.94),rgba(6,11,19,.96));box-shadow:0 30px 100px rgba(0,0,0,.48),0 0 80px rgba(68,88,180,.08);overflow:hidden;position:relative;z-index:3;animation:previewFloat 7s ease-in-out infinite}.preview-window:before{content:"";position:absolute;inset:-1px;border-radius:22px;background:linear-gradient(120deg,rgba(96,129,255,.28),transparent 28%,rgba(119,88,255,.12),transparent 72%);pointer-events:none}.window-bar{height:50px;border-bottom:1px solid #1b2537;display:grid;grid-template-columns:1fr 2fr 1fr;align-items:center;padding:0 19px;color:#68758a;font-size:10px;text-align:center}.window-dots{display:flex;gap:6px}.window-dots i{width:7px;height:7px;border-radius:50%;background:#384152}.preview-body{padding:29px}.preview-topline{display:flex;justify-content:space-between;align-items:flex-start}.preview-topline small,.trend-head small{display:block;font-size:9px;letter-spacing:1.6px;color:#63708a;font-weight:800}.preview-topline h3{font-size:23px;margin:8px 0 22px;letter-spacing:-.8px}.ai-active{font-size:10px;color:#54d79b;border:1px solid rgba(42,175,119,.23);background:rgba(24,103,73,.12);border-radius:9px;padding:8px 11px}.ai-active b{display:inline-block;width:6px;height:6px;border-radius:50%;background:#31d98b;box-shadow:0 0 9px #31d98b;margin-right:7px}.preview-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:11px}.preview-card{border:1px solid #1d2738;background:linear-gradient(145deg,#0e1522,#0a101a);border-radius:13px;padding:17px 15px;transition:.25s}.preview-card:hover{transform:translateY(-3px);border-color:#324a73;box-shadow:0 12px 35px rgba(0,0,0,.28),0 0 22px rgba(79,124,255,.07)}.preview-card small{display:block;color:#68758a;font-size:9px;margin-bottom:10px}.preview-card strong{display:block;font-size:17px;color:#f4f7fb;letter-spacing:-.3px}.preview-card em{display:block;font-size:8px;font-style:normal;margin-top:14px}.up,.healthy{color:#3ed98f}.down{color:#e89568}.trend-card{margin-top:13px;border:1px solid #1d2738;background:linear-gradient(145deg,#0d1420,#0a1019);border-radius:13px;padding:16px}.trend-head{display:flex;justify-content:space-between;align-items:flex-start}.trend-head strong{display:block;font-size:12px;margin-top:8px}.trend-head span{color:#6b93ff;font-size:22px}.trend-svg{width:100%;height:155px;margin-top:9px;filter:drop-shadow(0 0 9px rgba(79,124,255,.13))}.landing-bottom-space{height:120px}.landing-glow{position:fixed;pointer-events:none;border-radius:50%;filter:blur(18px);z-index:0}.glow-left{width:540px;height:540px;left:-250px;top:180px;background:radial-gradient(circle,rgba(52,82,214,.20),rgba(35,55,145,.07) 45%,transparent 70%);animation:glowMove 9s ease-in-out infinite alternate}.glow-right{width:420px;height:420px;right:-180px;bottom:-80px;background:radial-gradient(circle,rgba(89,52,195,.13),transparent 68%);animation:glowMove2 11s ease-in-out infinite alternate}.landing-particles{position:fixed;inset:0;pointer-events:none;z-index:1}.particle{position:absolute;width:6px;height:6px;border-radius:50%;background:#6e91ff;box-shadow:0 0 16px 5px rgba(79,124,255,.42);animation:particleFloat 6s ease-in-out infinite}.p1{left:33%;top:20%}.p2{left:71%;top:25%;animation-delay:-3s}.p3{left:13%;top:68%;width:4px;height:4px}.p4{left:86%;top:54%;width:4px;height:4px;animation-delay:-2s}.p5{left:47%;top:79%;width:3px;height:3px;animation-delay:-4s}.p6{left:61%;top:12%;width:3px;height:3px}@keyframes previewFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}@keyframes glowMove{from{transform:translate(0,0) scale(.9)}to{transform:translate(100px,55px) scale(1.15)}}@keyframes glowMove2{from{transform:translate(0,0)}to{transform:translate(-70px,-45px) scale(1.15)}}@keyframes particleFloat{0%,100%{transform:translateY(0);opacity:.5}50%{transform:translateY(-20px);opacity:1}}
@media(max-width:1000px){.block-container{padding:0 25px 40px!important}.landing-divider{margin:0 -25px}.hero-copy{padding-top:55px}.hero-copy h1{font-size:54px;letter-spacing:-3px}.hero-description{font-size:14px}.preview-window{margin-top:45px}.site-nav-links{display:none}}
</style>
""", unsafe_allow_html=True)


def api_error(resp):
    try:
        data = resp.json()
        return data.get("detail") or data.get("message") or "Request failed."
    except Exception:
        return f"Request failed ({resp.status_code})."


def money(v):
    try:
        return f"₹{float(v):,.0f}"
    except Exception:
        return "₹0"


def icon_for_category(cat):
    return {"Food":"🍴","Transport":"🚗","Shopping":"🛍️","Bills":"🧾","Entertainment":"🎬","Health":"❤","Education":"📚","Other":"•"}.get(cat,"•")


def login_screen():
    # Streamlit widgets cannot safely live inside an HTML div opened by a
    # different st.markdown call. The previous version therefore rendered an
    # empty glass rectangle. This version uses native Streamlit widgets and
    # styles their actual containers, so the login UI is visible and usable.
    st.markdown("""
    <div class="login-bg-glow glow-a"></div>
    <div class="login-bg-glow glow-b"></div>
    <div class="login-heading">
        <div class="login-orbit"><div class="login-brain">🧠</div></div>
        <div class="login-title">AI Finance Assistant</div>
        <div class="login-sub">Smart personal finance, powered by AI &amp; machine learning.</div>
    </div>
    """, unsafe_allow_html=True)

    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "Sign In"

    # Centered card using Streamlit's real widget tree.
    left, center, right = st.columns([1.25, 1.8, 1.25])
    with center:
        st.markdown('<div class="login-card-top"></div>', unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            if st.button("Sign In", use_container_width=True,
                         type="primary" if st.session_state.auth_tab == "Sign In" else "secondary",
                         key="tab_signin"):
                st.session_state.auth_tab = "Sign In"
                st.rerun()
        with t2:
            if st.button("Create Account", use_container_width=True,
                         type="primary" if st.session_state.auth_tab == "Create Account" else "secondary",
                         key="tab_register"):
                st.session_state.auth_tab = "Create Account"
                st.rerun()

        st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)

        if st.session_state.auth_tab == "Sign In":
            email = st.text_input("Email", placeholder="you@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            if st.button("Sign In  →", type="primary", use_container_width=True, key="login_btn"):
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    try:
                        payload = {"email": email.strip().lower(), "password": password}
                        r = None
                        last_error = None

                        # Render may sleep when idle. Give it time to wake and retry once.
                        for attempt in range(2):
                            try:
                                r = requests.post(f"{API}/login", json=payload, timeout=90)
                                if r.ok or r.status_code not in (502, 503, 504):
                                    break
                            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                                last_error = e
                                if attempt == 0:
                                    continue
                                break
                            except requests.RequestException as e:
                                last_error = e
                                break

                        if r is not None and r.ok:
                            d = r.json()
                            if not d.get("user_id"):
                                st.error("Login succeeded but the server did not return a user ID.")
                            else:
                                st.session_state["user_id"] = int(d["user_id"])
                                st.session_state["user_name"] = d.get("name", "User")
                                st.session_state["authenticated"] = True
                                st.session_state["show_landing"] = False
                                st.session_state["auth_tab"] = "Sign In"
                                st.session_state.pop("data", None)
                                st.rerun()
                        elif r is not None:
                            st.error(api_error(r))
                        else:
                            st.error("Backend is taking too long to respond. Render may be waking up. Wait a few seconds and click Sign In again.")
                    except Exception as e:
                        st.error(f"Login failed: {e}")
        else:
            name = st.text_input("Full Name", placeholder="Your name", key="reg_name")
            email = st.text_input("Email", placeholder="you@example.com", key="reg_email")
            password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
            if st.button("Create Account  →", type="primary", use_container_width=True, key="register_btn"):
                if not name or not email or not password:
                    st.error("Please fill all fields.")
                elif len(password) < 6:
                    st.error("Password should be at least 6 characters.")
                else:
                    try:
                        r = requests.post(f"{API}/register", json={"name": name, "email": email, "password": password}, timeout=30)
                        if r.ok:
                            d = r.json()
                            st.session_state["user_id"] = int(d["user_id"])
                            st.session_state["user_name"] = d.get("name", name)
                            st.session_state["authenticated"] = True
                            st.session_state["show_landing"] = False
                            st.session_state.pop("data", None)
                            st.success("Account created! Opening your dashboard...")
                            st.rerun()
                        else:
                            st.error(api_error(r))
                    except requests.RequestException as e:
                        st.error(f"Backend connection failed: {e}")

        st.markdown('<div class="login-footer">Educational personal finance assistant&nbsp; • &nbsp;Not professional financial advice</div>', unsafe_allow_html=True)


def load_data():
    uid=st.session_state.user_id
    results={}
    endpoints={"dashboard":f"/dashboard/{uid}","transactions":f"/transactions/{uid}","budgets":f"/budgets/{uid}","insights":f"/insights/{uid}","forecast":f"/forecast/{uid}"}
    for k,p in endpoints.items():
        try:
            r=requests.get(API+p,timeout=45); results[k]=r.json() if r.ok else None
        except Exception: results[k]=None
    st.session_state.data=results


def ensure_data():
    if "data" not in st.session_state: load_data()
    d=st.session_state.get("data",{})
    if not d.get("dashboard"): load_data()
    return st.session_state.data


def add_transaction():
    uid=st.session_state.user_id
    try:
        payload={"user_id":uid,"date":str(st.session_state.tx_date),"description":st.session_state.tx_desc,"amount":float(st.session_state.tx_amount),"type":st.session_state.tx_type,"category":st.session_state.tx_category}
        r=requests.post(f"{API}/transactions",json=payload,timeout=30)
        if r.ok: st.session_state.notice="Transaction added successfully."; load_data()
        else: st.session_state.error=api_error(r)
    except Exception as e: st.session_state.error=str(e)


def create_budget():
    try:
        p={"user_id":st.session_state.user_id,"month":st.session_state.b_month,"category":st.session_state.b_category,"limit_amount":float(st.session_state.b_amount)}
        r=requests.post(f"{API}/budgets",json=p,timeout=30)
        if r.ok: st.session_state.notice="Budget created successfully."; load_data()
        else: st.session_state.error=api_error(r)
    except Exception as e: st.session_state.error=str(e)


def delete_tx(tid):
    try:
        r=requests.delete(f"{API}/transactions/{tid}?user_id={st.session_state.user_id}",timeout=30)
        if r.ok: st.session_state.notice="Transaction deleted successfully."; load_data()
        else: st.session_state.error=api_error(r)
    except Exception as e: st.session_state.error=str(e)


def dashboard():
    data=ensure_data(); dash=data.get("dashboard") or {}; summary=dash.get("summary",{})
    name=st.session_state.get("user_name","User")
    # Navbar
    st.markdown(f'''<div class="navbar"><div class="brand"><div class="brand-mark">🧠</div><div class="brand-name"><strong>AI Finance</strong><span>Assistant</span></div></div><div class="welcome"><div class="welcome-text"><span>Welcome back</span><strong>{html.escape(name)}</strong></div></div></div>''',unsafe_allow_html=True)
    if "logout" not in st.session_state: st.session_state.logout=False
    nav1,nav2=st.columns([8,1])
    with nav2:
        if st.button("↪ Logout",key="logout_btn"):
            st.session_state.clear(); st.rerun()
    st.markdown("<div style='height:4px'></div>",unsafe_allow_html=True)

    c1,c2=st.columns([7,1])
    with c1:
        st.markdown('<p class="eyebrow">PERSONAL FINANCE</p><div class="hero"><div><h1>Your financial overview</h1><p>Track your income, expenses and budgets from one place.</p></div></div>',unsafe_allow_html=True)
    with c2:
        if st.button("↻ Refresh",key="refresh",use_container_width=True): load_data(); st.rerun()

    if st.session_state.get("notice"): st.success(st.session_state.pop("notice"))
    if st.session_state.get("error"): st.error(st.session_state.pop("error"))

    st.markdown(f'''<div class="summary-grid"><div class="summary-card"><div class="summary-icon income">↗</div><div class="summary-copy"><span>Total Income</span><h2 class="money">{money(summary.get('total_income',0))}</h2></div></div><div class="summary-card"><div class="summary-icon expense">↘</div><div class="summary-copy"><span>Total Expenses</span><h2 class="money">{money(summary.get('total_expenses',0))}</h2></div></div><div class="summary-card"><div class="summary-icon balance">◉</div><div class="summary-copy"><span>Current Balance</span><h2 class="money">{money(summary.get('balance',0))}</h2></div></div></div>''',unsafe_allow_html=True)

    # AI Insights
    insights=(data.get("insights") or {}).get("insights",[])
    st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">ARTIFICIAL INTELLIGENCE</p><p class="panel-title">✨ AI Financial Insights</p></div></div>',unsafe_allow_html=True)
    if insights:
        cols=st.columns(2)
        for i,x in enumerate(insights):
            typ=x.get("type","info"); icon={"positive":"✓","warning":"!","budget":"!","category":"↘","tip":"✦"}.get(typ,"i")
            with cols[i%2]: st.markdown(f'<div class="insight {typ}"><div class="insight-icon">{icon}</div><div><strong>{html.escape(str(x.get("title","Insight")))}</strong><p>{html.escape(str(x.get("message","")))}</p></div></div>',unsafe_allow_html=True)
    else: st.info("Add some transactions to generate AI insights.")
    st.markdown('<div class="disclaimer">🧠 Insights are generated from your recorded financial activity and are for educational purposes only.</div></div>',unsafe_allow_html=True)

    # Forecast
    forecast=data.get("forecast") or {}
    st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">MACHINE LEARNING</p><p class="panel-title">▥ AI Spending Forecast</p><p class="panel-sub">Estimated spending based on your historical transaction data.</p></div></div>',unsafe_allow_html=True)
    if forecast.get("status")=="success":
        fc=forecast.get("historical_data",[]).copy()
        if fc:
            fdf=pd.DataFrame(fc); fdf["expense"]=pd.to_numeric(fdf["expense"],errors="coerce")
            fig=go.Figure(); fig.add_trace(go.Scatter(x=fdf["month"],y=fdf["expense"],mode="lines+markers",name="Historical spending",line=dict(width=3)))
            if forecast.get("next_month") is not None: fig.add_trace(go.Scatter(x=[forecast.get("next_month")],y=[float(forecast.get("predicted_spending",0))],mode="markers",name="Predicted",marker=dict(size=12,symbol="diamond")))
            fig.update_layout(template="plotly_dark",height=250,margin=dict(l=5,r=5,t=10,b=5),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#94a3b8",size=10),legend=dict(orientation="h",y=1.12,x=0),xaxis=dict(gridcolor="#182436"),yaxis=dict(gridcolor="#182436",tickprefix="₹"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            st.markdown(f'<div class="disclaimer">Predicted next-month spending: <strong style="color:#e7ecf4">{money(forecast.get("predicted_spending",0))}</strong> • Forecasts are estimates, not guarantees.</div>',unsafe_allow_html=True)
    else: st.info(forecast.get("message","Add at least a few months of data for a forecast."))
    st.markdown('</div>',unsafe_allow_html=True)

    # Charts + budgets
    cat=dash.get("category_spending",[]) or []
    monthly=dash.get("monthly_trends",[]) or dash.get("monthly_spending",[]) or []
    left,right=st.columns([1,1])
    with left:
        st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">SPENDING ANALYTICS</p><p class="panel-title">Category spending</p></div></div>',unsafe_allow_html=True)
        if cat:
            cdf=pd.DataFrame(cat); cdf["total"]=pd.to_numeric(cdf["total"],errors="coerce"); cdf=cdf[cdf["category"].notna()]
            fig=px.pie(cdf,names="category",values="total",hole=.66)
            fig.update_layout(template="plotly_dark",height=285,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#a7b2c3",size=10),legend=dict(font=dict(size=9)))
            fig.update_traces(textinfo="percent",textfont_size=10,marker=dict(line=dict(color="#0b1220",width=2)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        else: st.info("No expense data yet.")
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">MONTHLY TREND</p><p class="panel-title">Income vs expenses</p></div></div>',unsafe_allow_html=True)
        if monthly:
            mdf=pd.DataFrame(monthly)
            # tolerate common backend field names
            if "month" not in mdf.columns: mdf["month"]=range(1,len(mdf)+1)
            inc_col=next((c for c in ["income","total_income"] if c in mdf.columns),None); exp_col=next((c for c in ["expense","expenses","total_expenses"] if c in mdf.columns),None)
            fig=go.Figure()
            if inc_col: fig.add_trace(go.Bar(x=mdf["month"],y=mdf[inc_col],name="Income"))
            if exp_col: fig.add_trace(go.Bar(x=mdf["month"],y=mdf[exp_col],name="Expenses"))
            fig.update_layout(template="plotly_dark",barmode="group",height=285,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#94a3b8",size=9),xaxis=dict(gridcolor="#182436"),yaxis=dict(gridcolor="#182436",tickprefix="₹"),legend=dict(orientation="h",y=1.1,x=0))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        else: st.info("Monthly trend data will appear here.")
        st.markdown('</div>',unsafe_allow_html=True)

    budgets=data.get("budgets") or []
    st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">BUDGET MANAGEMENT</p><p class="panel-title">Budget overview</p></div></div>',unsafe_allow_html=True)
    if budgets:
        # backend budget rows can have spent/used/status or just limits
        for b in budgets[:8]:
            limit=float(b.get("limit_amount",0) or 0); spent=float(b.get("spent",b.get("used",b.get("spent_amount",0))) or 0); pct=(spent/limit*100) if limit else 0; cls="over" if pct>100 else ""
            st.markdown(f'<div class="budget-item"><div class="budget-top"><strong>{icon_for_category(b.get("category","Other"))} {html.escape(str(b.get("category","Other")))}</strong><span>{money(spent)} / {money(limit)} • {pct:.0f}%</span></div><div class="progress {cls}"><div style="width:{min(pct,100)}%"></div></div></div>',unsafe_allow_html=True)
    else: st.info("No budgets created yet.")
    st.markdown('</div>',unsafe_allow_html=True)

    # Transactions and forms
    st.markdown('<div style="height:18px"></div><p class="section-title">Transactions</p>',unsafe_allow_html=True)
    f1,f2=st.columns([1.05,.95])
    with f1:
        st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">ADD TRANSACTION</p><p class="panel-title">Record income or expense</p></div></div>',unsafe_allow_html=True)
        st.date_input("Date",value=date.today(),key="tx_date")
        st.text_input("Description",placeholder="e.g. Grocery shopping",key="tx_desc")
        st.number_input("Amount",min_value=0.0,step=100.0,key="tx_amount")
        a,b=st.columns(2)
        with a: st.selectbox("Type",["expense","income"],key="tx_type")
        with b: st.selectbox("Category",CATEGORIES,key="tx_category")
        p1,p2=st.columns([1,1])
        with p1:
            if st.button("✨ AI Predict Category",use_container_width=True,key="predict_btn"):
                if not st.session_state.get("tx_desc","").strip(): st.warning("Enter a description first.")
                else:
                    try:
                        r=requests.post(f"{API}/predict-category",json={"description":st.session_state.tx_desc},timeout=30)
                        if r.ok:
                            q=r.json(); st.session_state.tx_category=q.get("category",st.session_state.tx_category); st.success(f"AI predicted {q.get('category')} • {q.get('confidence')}% confidence")
                        else: st.error(api_error(r))
                    except Exception as e: st.error(str(e))
        with p2:
            if st.button("＋ Add Transaction",type="primary",use_container_width=True,key="add_tx_btn"):
                if not st.session_state.get("tx_desc","").strip(): st.error("Please enter a description.")
                elif not st.session_state.get("tx_amount",0): st.error("Please enter an amount.")
                else: add_transaction(); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">MONTHLY BUDGET</p><p class="panel-title">Create a budget limit</p></div></div>',unsafe_allow_html=True)
        st.text_input("Month",value=date.today().strftime("%Y-%m"),key="b_month")
        st.selectbox("Category",CATEGORIES,key="b_category")
        st.number_input("Limit amount",min_value=0.0,step=500.0,key="b_amount")
        if st.button("＋ Create Budget",type="primary",use_container_width=True,key="budget_btn"):
            if not st.session_state.get("b_amount",0): st.error("Please enter a budget amount.")
            else: create_budget(); st.rerun()
        st.markdown('<div class="disclaimer">Budget alerts compare recorded spending against your limits.</div></div>',unsafe_allow_html=True)

    st.markdown('<div style="height:18px"></div><p class="section-title">Recent activity</p>',unsafe_allow_html=True)
    tx=data.get("transactions") or []
    if tx:
        for t in tx[:12]:
            typ=t.get("type","expense"); amount=money(t.get("amount",0)); sign="+" if typ=="income" else "−"; cls="tx-income" if typ=="income" else "tx-expense"
            d=html.escape(str(t.get("date", ""))); desc=html.escape(str(t.get("description","Transaction"))); cat=html.escape(str(t.get("category","Other")))
            c1,c2=st.columns([9,1])
            with c1: st.markdown(f'<div class="tx-card"><div class="tx-left"><div class="tx-dot">{icon_for_category(t.get("category","Other"))}</div><div><div class="tx-desc">{desc}</div><div class="tx-meta">{d} • {cat}</div></div></div><div class="tx-amount {cls}">{sign}{amount}</div></div>',unsafe_allow_html=True)
            with c2:
                if st.button("🗑",key=f"del_{t.get('transaction_id',t.get('id',0))}",help="Delete transaction"):
                    delete_tx(t.get("transaction_id",t.get("id"))); st.rerun()
    else: st.info("No transactions yet. Add your first transaction above.")

    # Chatbot controls at bottom (Streamlit-safe equivalent of floating React chat)
    if "chat_open" not in st.session_state: st.session_state.chat_open=False
    st.markdown('<div style="height:15px"></div>',unsafe_allow_html=True)
    if st.button("💬  Finance Assistant",key="chat_toggle",type="primary"):
        st.session_state.chat_open=not st.session_state.chat_open; st.rerun()
    if st.session_state.chat_open:
        st.markdown('<div class="panel"><div class="panel-head"><div><p class="panel-label">AI FINANCIAL CHATBOT</p><p class="panel-title">🧠 Finance Assistant</p><p class="panel-sub">AI financial chatbot</p></div></div>',unsafe_allow_html=True)
        if "chat_messages" not in st.session_state: st.session_state.chat_messages=[{"role":"bot","text":f"Hello {name}! 👋 Ask me about your income, expenses, balance or spending categories."}]
        for m in st.session_state.chat_messages:
            if m["role"]=="user": st.markdown(f'<div style="display:flex;justify-content:flex-end;margin:8px 0"><div style="background:#253a73;border-radius:12px 12px 3px 12px;padding:10px 13px;max-width:78%;font-size:12px">{html.escape(m["text"])}</div></div>',unsafe_allow_html=True)
            else: st.markdown(f'<div style="display:flex;justify-content:flex-start;margin:8px 0"><div style="background:#111b2b;border:1px solid #1e2c40;border-radius:12px 12px 12px 3px;padding:10px 13px;max-width:78%;font-size:12px;color:#cbd5e1">🧠 {html.escape(m["text"])}</div></div>',unsafe_allow_html=True)
        q1,q2,q3=st.columns(3)
        suggestions=["How much did I spend?","What is my balance?","What is my highest spending category?"]
        for i,(col,q) in enumerate(zip([q1,q2,q3],suggestions)):
            with col:
                if st.button(q,key=f"suggestion_btn_{i}"): st.session_state.chat_input=q; st.rerun()
        cc1,cc2=st.columns([8,1])
        with cc1: st.text_input("",placeholder="Ask about your finances...",key="chat_input",label_visibility="collapsed")
        with cc2:
            if st.button("➤",key="chat_send",type="primary"):
                msg=st.session_state.get("chat_input","").strip()
                if msg:
                    st.session_state.chat_messages.append({"role":"user","text":msg})
                    try:
                        r=requests.post(f"{API}/chat",json={"user_id":st.session_state.user_id,"message":msg},timeout=45)
                        reply=r.json().get("response","Sorry, I couldn't process that request.") if r.ok else api_error(r)
                    except Exception: reply="Sorry, I couldn't connect to the finance assistant right now."
                    st.session_state.chat_messages.append({"role":"bot","text":reply}); st.session_state.chat_input=""; st.rerun()
        st.markdown('<div class="disclaimer">🧠 Educational financial assistant</div></div>',unsafe_allow_html=True)




# -----------------------------------------------------------------------------
# LANDING PAGE — requested AI Finance website design.
# -----------------------------------------------------------------------------
def landing_page():
    st.markdown("""
    <div class="landing-particles"><span class="particle p1"></span><span class="particle p2"></span><span class="particle p3"></span><span class="particle p4"></span><span class="particle p5"></span><span class="particle p6"></span></div>
    <div class="landing-arc arc1"></div><div class="landing-arc arc2"></div>
    <div class="landing-glow glow-left"></div><div class="landing-glow glow-right"></div>
    """, unsafe_allow_html=True)

    n1,n2,n3=st.columns([2.2,4.8,3.0])
    with n1:
        st.markdown('<div class="site-brand"><div class="site-logo">♧</div><div class="site-brand-name">AI Finance</div></div>', unsafe_allow_html=True)
    with n2:
        st.markdown('<div class="site-nav-links"><span>Features</span><span>About</span></div>', unsafe_allow_html=True)
    with n3:
        a,b=st.columns([1,1.35])
        with a:
            if st.button("Login",key="landing_login",use_container_width=True):
                st.session_state.show_landing=False; st.session_state.auth_tab="Sign In"; st.rerun()
        with b:
            if st.button("Get Started",key="landing_started",use_container_width=True,type="primary"):
                st.session_state.show_landing=False; st.session_state.auth_tab="Create Account"; st.rerun()

    st.markdown('<div class="landing-divider"></div>',unsafe_allow_html=True)
    left,right=st.columns([1.02,1],gap="large")
    with left:
        st.markdown("""
        <div class="hero-copy">
          <div class="hero-pill"><span class="spark">✧</span> AI-powered personal finance</div>
          <h1>Your money.<br><span>Understood.</span></h1>
          <p class="hero-description">AI Finance Assistant helps you understand your spending, manage budgets,<br>track transactions and discover meaningful financial patterns — all in one<br>simple dashboard.</p>
        </div>""",unsafe_allow_html=True)
        c1,c2=st.columns([1.25,.75])
        with c1:
            if st.button("Start Managing   →",key="hero_start",type="primary",use_container_width=True):
                st.session_state.show_landing=False; st.session_state.auth_tab="Create Account"; st.rerun()
        with c2:
            if st.button("Sign In",key="hero_signin",use_container_width=True):
                st.session_state.show_landing=False; st.session_state.auth_tab="Sign In"; st.rerun()
        st.markdown('<div class="trust-line"><span class="shield">♢</span> Educational finance assistant · Your data stays yours</div>',unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="preview-window">
          <div class="window-bar"><div class="window-dots"><i></i><i></i><i></i></div><span>AI Finance Assistant</span><div></div></div>
          <div class="preview-body">
            <div class="preview-topline"><div><small>FINANCIAL OVERVIEW</small><h3>Dashboard</h3></div><div class="ai-active"><b></b> AI Active</div></div>
            <div class="preview-metrics">
              <div class="preview-card"><small>Total Income</small><strong>₹25,000</strong><em class="up">↑ Money received</em></div>
              <div class="preview-card"><small>Total Expenses</small><strong>₹8,450</strong><em class="down">↓ Money spent</em></div>
              <div class="preview-card"><small>Balance</small><strong>₹16,550</strong><em class="healthy">Healthy balance</em></div>
            </div>
            <div class="trend-card"><div class="trend-head"><div><small>MONTHLY ANALYSIS</small><strong>Spending Trend</strong></div><span>▥</span></div>
              <svg class="trend-svg" viewBox="0 0 680 180" preserveAspectRatio="none"><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#527dff" stop-opacity=".22"/><stop offset="1" stop-color="#527dff" stop-opacity=".02"/></linearGradient></defs><g opacity=".45" stroke="#1c2940" stroke-width="1"><line x1="0" y1="35" x2="680" y2="35"/><line x1="0" y1="78" x2="680" y2="78"/><line x1="0" y1="121" x2="680" y2="121"/><line x1="0" y1="164" x2="680" y2="164"/></g><path d="M0 140 L55 124 L110 132 L165 105 L220 118 L275 82 L330 96 L385 70 L440 84 L495 51 L550 70 L610 43 L680 55 L680 180 L0 180 Z" fill="url(#area)"/><polyline points="0,140 55,124 110,132 165,105 220,118 275,82 330,96 385,70 440,84 495,51 550,70 610,43 680,55" fill="none" stroke="#4f7cff" stroke-width="3"/></svg>
            </div>
          </div>
        </div>""",unsafe_allow_html=True)
    st.markdown('<div class="landing-bottom-space"></div>',unsafe_allow_html=True)

if "user_id" not in st.session_state: st.session_state.user_id = None
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "show_landing" not in st.session_state: st.session_state.show_landing = True
if "auth_tab" not in st.session_state: st.session_state.auth_tab = "Sign In"

# user_id is the single source of truth for authentication.
# This prevents the landing/auth state from accidentally blocking the dashboard.
if st.session_state.get("user_id") is not None:
    dashboard()
elif st.session_state.get("show_landing", True):
    landing_page()
else:
    login_screen()
