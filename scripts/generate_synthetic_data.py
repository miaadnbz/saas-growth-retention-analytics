"""Generate all synthetic source tables used in the SaaS growth analytics case study.

The fixed seed makes the project reproducible. All entities are fictional.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'data' / 'raw').mkdir(parents=True, exist_ok=True)
(ROOT / 'data' / 'sample').mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)
N = 12000
start = pd.Timestamp('2024-01-01')
end = pd.Timestamp('2025-09-30')
obs_end = pd.Timestamp('2026-03-31')
all_days = pd.date_range(start, end, freq='D')
# slight seasonality: higher signups in Jan, Sep, Nov
weights = np.array([1.0 + (d.month in [1,9,11])*0.35 + (d.dayofweek < 5)*0.10 for d in all_days], dtype=float)
weights /= weights.sum()
signup_dates = rng.choice(all_days.to_numpy(), size=N, p=weights)
signup_dates = pd.to_datetime(signup_dates)
channels = np.array(['Organic Search','Paid Search','Paid Social','Referral','Partner','Direct','Email'])
channel_probs = np.array([0.22,0.20,0.18,0.12,0.08,0.12,0.08])
channel = rng.choice(channels, size=N, p=channel_probs)
company_sizes = np.array(['1-5','6-20','21-50','51-200','201+'])
company_probs = np.array([0.34,0.31,0.17,0.12,0.06])
company_size = rng.choice(company_sizes, size=N, p=company_probs)
industries = np.array(['Professional Services','Healthcare','Retail','Technology','Education','Home Services'])
industry = rng.choice(industries, size=N, p=[0.22,0.18,0.17,0.17,0.12,0.14])
countries = np.array(['Canada','United States','United Kingdom','Australia'])
country = rng.choice(countries, size=N, p=[0.38,0.37,0.15,0.10])

# Campaign mapping
campaign_map = {
    'Paid Search':['PS_Brand','PS_NonBrand','PS_Competitor'],
    'Paid Social':['SOC_Prospecting','SOC_Retargeting','SOC_Video'],
    'Email':['EML_Nurture','EML_Reactivation'],
    'Partner':['PART_Consultants','PART_Community'],
    'Organic Search':['ORG_SEO'], 'Referral':['REF_Customer'], 'Direct':['DIR_None']
}
campaign_id=[]
for ch in channel:
    campaign_id.append(rng.choice(campaign_map[ch]))
campaign_id=np.array(campaign_id)

# Latent engagement and action probabilities
channel_eng = {'Referral':0.85,'Partner':0.70,'Organic Search':0.45,'Direct':0.35,'Email':0.25,'Paid Search':0.10,'Paid Social':-0.30}
size_eng = {'1-5':-0.15,'6-20':0.10,'21-50':0.25,'51-200':0.35,'201+':0.20}
base = rng.normal(0,1,N) + np.array([channel_eng[x] for x in channel]) + np.array([size_eng[x] for x in company_size])
# support burden correlated with lower engagement and larger org complexity
support_prop = 1/(1+np.exp(-( -0.5*base + np.array([[0.0,0.1,0.2,0.35,0.5][company_sizes.tolist().index(s)] for s in company_size]))))

# critical onboarding actions within 14 days
sigmoid=lambda x:1/(1+np.exp(-x))
p_project = sigmoid(-0.05 + 0.95*base)
p_invite = sigmoid(-0.35 + 0.90*base + np.where(np.isin(company_size,['21-50','51-200','201+']),0.4,0))
p_integration = sigmoid(-0.55 + 0.80*base + np.where(np.isin(industry,['Technology','Professional Services']),0.25,0))
project = rng.random(N) < p_project
invite = rng.random(N) < p_invite
integration = rng.random(N) < p_integration
critical_count = project.astype(int)+invite.astype(int)+integration.astype(int)
activated = critical_count >= 2
activation_date=[]
for i, sd in enumerate(signup_dates):
    if activated[i]:
        activation_date.append(sd + pd.Timedelta(days=int(rng.integers(1,14))))
    else:
        activation_date.append(pd.NaT)
activation_date=pd.to_datetime(activation_date)

# Conversion, plan, cancellation
channel_conv = {'Referral':0.45,'Partner':0.34,'Organic Search':0.22,'Direct':0.18,'Email':0.14,'Paid Search':0.12,'Paid Social':-0.18}
conv_logit = -1.25 + 1.45*activated.astype(int) + 0.45*base + np.array([channel_conv[x] for x in channel])
converted = rng.random(N) < sigmoid(conv_logit)
plans=[]; mrr=[]
for s, conv in zip(company_size, converted):
    if not conv:
        plans.append('Trial Only'); mrr.append(0)
    else:
        if s in ['1-5','6-20']:
            plan = rng.choice(['Starter','Pro'], p=[0.72,0.28])
        elif s in ['21-50']:
            plan = rng.choice(['Starter','Pro','Business'], p=[0.18,0.62,0.20])
        else:
            plan = rng.choice(['Pro','Business'], p=[0.42,0.58])
        plans.append(plan); mrr.append({'Starter':49,'Pro':99,'Business':249}[plan])
plans=np.array(plans); mrr=np.array(mrr)
conversion_date=[]
for i, sd in enumerate(signup_dates):
    if converted[i]:
        # activated accounts convert sooner
        low, high = (3,18) if activated[i] else (8,29)
        conversion_date.append(sd + pd.Timedelta(days=int(rng.integers(low,high))))
    else:
        conversion_date.append(pd.NaT)
conversion_date=pd.to_datetime(conversion_date)

# cancellation hazard by activation/channel/support propensity
cancel_date=[]
for i in range(N):
    if not converted[i]:
        cancel_date.append(pd.NaT); continue
    # annualized-ish hazard translated into discrete lifetime draw
    base_monthly = 0.045
    if not activated[i]: base_monthly += 0.095
    if channel[i]=='Paid Social': base_monthly += 0.035
    if channel[i]=='Referral': base_monthly -= 0.018
    if channel[i]=='Partner': base_monthly -= 0.010
    base_monthly += 0.025*support_prop[i]
    base_monthly = float(np.clip(base_monthly,0.015,0.22))
    # simulate monthly cancellation through obs end
    cd = conversion_date[i]
    d = cd + pd.offsets.MonthBegin(1)
    cancelled = pd.NaT
    while d <= obs_end:
        if rng.random() < base_monthly:
            cancelled = d + pd.Timedelta(days=int(rng.integers(0,25)))
            break
        d += pd.offsets.MonthBegin(1)
    cancel_date.append(cancelled)
cancel_date=pd.to_datetime(cancel_date)

account_ids=[f'A{i:05d}' for i in range(1,N+1)]
accounts=pd.DataFrame({
    'account_id':account_ids,'signup_date':signup_dates,'country':country,'industry':industry,
    'company_size':company_size,'first_touch_channel':channel,'first_touch_campaign_id':campaign_id,
    'trial_days':14
}).sort_values('signup_date')
accounts.to_csv(ROOT/'data/raw/accounts.csv',index=False)

# marketing touches: 1-4 touches before signup; last touch often first channel but not always
mt=[]
for i, aid in enumerate(account_ids):
    n=int(rng.choice([1,2,3,4],p=[0.38,0.34,0.20,0.08]))
    selected=[channel[i]]
    if n>1:
        other=rng.choice(channels,size=n-1,p=channel_probs)
        selected=list(other)+[channel[i]]
    for j,ch in enumerate(selected):
        days_before=int(rng.integers(0,30)) if j < n-1 else int(rng.integers(0,4))
        touch_dt=signup_dates[i]-pd.Timedelta(days=days_before)
        camp=rng.choice(campaign_map[ch])
        mt.append((f'T{len(mt)+1:07d}',aid,touch_dt,ch,camp,j+1,n))
marketing=pd.DataFrame(mt,columns=['touch_id','account_id','touch_date','channel','campaign_id','touch_position','touch_count'])
marketing.to_csv(ROOT/'data/raw/marketing_touches.csv',index=False)

# events
rows=[]
event_id=1
for i,aid in enumerate(account_ids):
    sd=signup_dates[i]
    # baseline events
    rows.append((f'E{event_id:08d}',aid,sd,'created_workspace')); event_id+=1
    if rng.random() < sigmoid(0.1+0.6*base[i]):
        rows.append((f'E{event_id:08d}',aid,sd+pd.Timedelta(days=int(rng.integers(0,4))),'completed_profile')); event_id+=1
    if project[i]:
        rows.append((f'E{event_id:08d}',aid,sd+pd.Timedelta(days=int(rng.integers(0,10))),'created_project')); event_id+=1
    if invite[i]:
        rows.append((f'E{event_id:08d}',aid,sd+pd.Timedelta(days=int(rng.integers(1,13))),'invited_teammate')); event_id+=1
    if integration[i]:
        rows.append((f'E{event_id:08d}',aid,sd+pd.Timedelta(days=int(rng.integers(1,14))),'connected_integration')); event_id+=1
    if rng.random() < sigmoid(-0.3+0.75*base[i]):
        rows.append((f'E{event_id:08d}',aid,sd+pd.Timedelta(days=int(rng.integers(2,21))),'viewed_dashboard')); event_id+=1
    if rng.random() < sigmoid(-0.8+0.7*base[i]):
        rows.append((f'E{event_id:08d}',aid,sd+pd.Timedelta(days=int(rng.integers(5,30))),'used_automation')); event_id+=1
    # recurring activity for converters; more if retained/activated
    if converted[i]:
        active_end = min(cancel_date[i] if not pd.isna(cancel_date[i]) else obs_end, obs_end)
        weeks=max(0,int((active_end-conversion_date[i]).days/7))
        rate = 1.4 + 1.2*activated[i] + 0.35*max(base[i],-1)
        count=int(rng.poisson(max(1,weeks*rate)))
        for _ in range(min(count,140)):
            day=int(rng.integers(0,max(1,(active_end-conversion_date[i]).days+1)))
            evdt=conversion_date[i]+pd.Timedelta(days=day)
            ev=rng.choice(['login','created_project','viewed_dashboard','exported_report','used_automation'],p=[0.52,0.12,0.18,0.10,0.08])
            rows.append((f'E{event_id:08d}',aid,evdt,ev)); event_id+=1
product_events=pd.DataFrame(rows,columns=['event_id','account_id','event_timestamp','event_name']).sort_values('event_timestamp')
product_events.to_csv(ROOT/'data/raw/product_events.csv',index=False)

subscriptions=pd.DataFrame({
    'subscription_id':[f'S{i:05d}' for i in range(1,N+1)],'account_id':account_ids,'trial_start_date':signup_dates,
    'conversion_date':conversion_date,'plan_name':plans,'monthly_recurring_revenue':mrr,'cancel_date':cancel_date,
    'status':np.where(~converted,'trial_expired',np.where(pd.isna(cancel_date),'active','cancelled'))
})
subscriptions.to_csv(ROOT/'data/raw/subscriptions.csv',index=False)

# invoices
inv=[]
for i,aid in enumerate(account_ids):
    if not converted[i]: continue
    d=pd.Timestamp(conversion_date[i]).normalize()
    stop=min(cancel_date[i] if not pd.isna(cancel_date[i]) else obs_end,obs_end)
    k=0
    while d <= stop:
        inv.append((f'I{len(inv)+1:07d}',aid,d,float(mrr[i]),'paid'))
        k+=1; d=conversion_date[i]+pd.DateOffset(months=k)
invoices=pd.DataFrame(inv,columns=['invoice_id','account_id','invoice_date','amount','payment_status'])
invoices.to_csv(ROOT/'data/raw/invoices.csv',index=False)

# support tickets
st=[]
for i,aid in enumerate(account_ids):
    lam=0.25+1.25*support_prop[i]+(0.45 if converted[i] else 0)
    n=int(rng.poisson(lam))
    max_day=max(14,int(((cancel_date[i] if not pd.isna(cancel_date[i]) else obs_end)-signup_dates[i]).days))
    for _ in range(min(n,8)):
        created=signup_dates[i]+pd.Timedelta(days=int(rng.integers(0,max_day+1)))
        if created>obs_end: created=obs_end
        priority=rng.choice(['low','medium','high'],p=[0.50,0.36,0.14])
        resolution=max(0.5,float(rng.gamma(2.0,6.0)*(1.7 if priority=='high' else 1.0)))
        csat=float(np.clip(rng.normal(4.25-0.025*resolution,0.55),1,5))
        st.append((f'K{len(st)+1:06d}',aid,created,priority,round(resolution,1),round(csat,1)))
support=pd.DataFrame(st,columns=['ticket_id','account_id','created_at','priority','resolution_hours','csat_score'])
support.to_csv(ROOT/'data/raw/support_tickets.csv',index=False)

# monthly campaign spend
months=pd.date_range(start.replace(day=1),end.replace(day=1),freq='MS')
sp=[]
spend_base={'PS_Brand':18000,'PS_NonBrand':28000,'PS_Competitor':9000,'SOC_Prospecting':32000,'SOC_Retargeting':14000,'SOC_Video':10000,
            'EML_Nurture':5000,'EML_Reactivation':3000,'PART_Consultants':9000,'PART_Community':6000,'ORG_SEO':8500,'REF_Customer':6000,'DIR_None':0}
channel_lookup={camp:ch for ch,camps in campaign_map.items() for camp in camps}
for m in months:
    for camp,b in spend_base.items():
        season=1+0.15*(m.month in [1,9,11])
        amount=max(0,round(b*season*rng.normal(1,0.08),2))
        sp.append((m,channel_lookup[camp],camp,amount))
spend=pd.DataFrame(sp,columns=['spend_month','channel','campaign_id','spend'])
spend.to_csv(ROOT/'data/raw/campaign_spend.csv',index=False)

