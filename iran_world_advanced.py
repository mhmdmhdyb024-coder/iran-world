
from flask import Flask, render_template_string, jsonify
import json

app = Flask(__name__)

# اطلاعات رتبه‌ها از فهرست قبلی پروژه
DATA = [
    {"id":1,"title":"تولید جهانی استرانسیم","rank":1,"category":"معدن و صنایع","value":"حدود ۵۰٪ تولید جهان","year":"۲۰۲۴","icon":"🥇","description":"استرانسیم ماده‌ای معدنی با کاربرد در صنایع شیمیایی، سرامیک و شیشه است.","meaning":"رتبه اول یعنی ایران در این برآورد، بزرگ‌ترین تولیدکننده این ماده در جهان معرفی شده است.","source":"USGS","url":"https://www.usgs.gov/centers/national-minerals-information-center"},
    {"id":2,"title":"تولید آهن اسفنجی","rank":2,"category":"معدن و صنایع","value":"حدود ۲۴٪ تولید جهان","year":"۲۰۲۴","icon":"🏭","description":"آهن اسفنجی ماده اولیه مهم تولید فولاد است.","meaning":"رتبه دوم نشان‌دهنده جایگاه مهم ایران در صنعت آهن اسفنجی است.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":3,"title":"تولید گچ معدنی","rank":2,"category":"معدن و صنایع","value":"حدود ۱۰٪ تولید جهان","year":"۲۰۲۴","icon":"🧱","description":"گچ در ساختمان‌سازی، سیمان و صنایع مختلف کاربرد دارد.","meaning":"ایران در این برآورد یکی از تولیدکنندگان بزرگ گچ معرفی شده است.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":4,"title":"تولید فلدسپار","rank":3,"category":"معدن و صنایع","value":"حدود ۱۲٪ تولید جهان","year":"۲۰۲۴","icon":"💎","description":"فلدسپار در تولید شیشه، کاشی و سرامیک کاربرد دارد.","meaning":"رتبه سوم نشان‌دهنده سهم قابل توجه ایران در تولید این ماده است.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":5,"title":"تولید ید","rank":4,"category":"معدن و صنایع","value":"حدود ۲٫۱٪ تولید جهان","year":"۲۰۲۴","icon":"⚗️","description":"ید در صنایع دارویی، پزشکی و شیمیایی استفاده می‌شود.","meaning":"رتبه چهارم ایران را در میان تولیدکنندگان مهم این ماده قرار می‌دهد.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":6,"title":"تولید باریت","rank":5,"category":"معدن و صنایع","value":"حدود ۳٫۸٪ تولید جهان","year":"۲۰۲۴","icon":"🪨","description":"باریت از مواد مهم مورد استفاده در حفاری چاه‌های نفت و گاز است.","meaning":"رتبه پنجم نشان‌دهنده حضور ایران در میان تولیدکنندگان برتر است.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":7,"title":"تولید سنگ‌آهن","rank":5,"category":"معدن و صنایع","value":"حدود ۳٫۷٪ تولید جهان","year":"۲۰۲۴","icon":"⛏️","description":"سنگ‌آهن ماده اولیه اصلی تولید آهن و فولاد است.","meaning":"ایران در این برآورد یکی از تولیدکنندگان مهم سنگ‌آهن است.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":8,"title":"تولید سیمان","rank":6,"category":"معدن و صنایع","value":"حدود ۱٫۸٪ تولید جهان","year":"۲۰۲۴","icon":"🏗️","description":"سیمان در ساخت بتن، ساختمان‌ها و زیرساخت‌ها استفاده می‌شود.","meaning":"رتبه ششم بیانگر حضور ایران در میان تولیدکنندگان بزرگ سیمان است.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":9,"title":"تولید منیزیم فلزی","rank":7,"category":"معدن و صنایع","value":"حدود ۰٫۴۶٪ تولید جهان","year":"۲۰۲۴","icon":"🔩","description":"منیزیم فلزی در آلیاژسازی و ساخت قطعات سبک کاربرد دارد.","meaning":"رتبه هفتم یعنی ایران در این برآورد در میان ده تولیدکننده برتر قرار دارد.","source":"USGS","url":"https://www.usgs.gov/"},
    {"id":10,"title":"تولید گاز طبیعی","rank":4,"category":"انرژی","value":"حدود ۲۹۱٫۵ میلیارد مترمکعب","year":"۲۰۲۵","icon":"🔥","description":"گاز طبیعی یکی از منابع مهم انرژی و خوراک صنایع پتروشیمی است.","meaning":"این مقدار، حجم تولید را نشان می‌دهد؛ رتبه آن باید با جدول جهانی هم‌سال تطبیق داده شود.","source":"Energy Institute","url":"https://www.energyinst.org/statistical-review"}
]

DATA = [x for x in DATA if 1 <= x["rank"] <= 10]

PAGE = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#061710">
<title>ایران در جهان | دستاوردهای برتر</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{
 --bg:#061710;--panel:#0d261c;--panel2:#123526;
 --green:#16a36a;--lime:#b8ef70;--gold:#f6c75c;
 --white:#f4fff8;--muted:#a6c3b3;--red:#e94c52;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
 margin:0;background:var(--bg);color:var(--white);
 font-family:Vazirmatn,sans-serif;overflow-x:hidden;
}
body:before{
 content:"";position:fixed;inset:0;z-index:-3;
 background:
 radial-gradient(ellipse at 15% 10%,#0e764a44,transparent 40%),
 radial-gradient(ellipse at 90% 80%,#b8ef7019,transparent 35%),
 linear-gradient(140deg,#061710,#0a2118 55%,#061710);
}
#particles{position:fixed;inset:0;z-index:-1;pointer-events:none}
a{color:inherit;text-decoration:none}
button,input,select{font-family:inherit}
.nav{
 position:fixed;top:0;left:0;right:0;z-index:30;
 display:flex;align-items:center;justify-content:space-between;
 padding:14px 5%;background:#061710b8;
 border-bottom:1px solid #ffffff13;backdrop-filter:blur(18px);
}
.brand{font-size:19px;font-weight:900;color:var(--lime)}
.brand span{color:white}
.navlinks{display:flex;gap:25px;color:var(--muted);font-size:13px}
.navlinks a:hover{color:var(--lime)}
.navbtn{
 background:#b8ef7018;color:var(--lime);border:1px solid #b8ef7055;
 padding:9px 17px;border-radius:30px;cursor:pointer;
}
.hero{
 min-height:710px;padding:140px 20px 100px;
 display:flex;align-items:center;justify-content:center;text-align:center;
 position:relative;overflow:hidden;
}
.hero:before,.hero:after{
 content:"";position:absolute;border:1px solid #b8ef7025;
 width:390px;height:390px;border-radius:50%;
 animation:spin 28s linear infinite;
}
.hero:after{width:560px;height:560px;animation-direction:reverse}
@keyframes spin{to{transform:rotate(360deg)}}
.hero-content{position:relative;z-index:2;max-width:850px}
.flag{font-size:65px;filter:drop-shadow(0 0 30px #16a36a66)}
.tag{
 display:inline-block;padding:8px 17px;border-radius:40px;
 color:var(--lime);border:1px solid #b8ef7045;
 background:#b8ef7010;font-size:12px;letter-spacing:1px;
}
h1{font-size:clamp(43px,7vw,78px);line-height:1.35;margin:20px 0}
h1 span{color:var(--lime);text-shadow:0 0 35px #b8ef7055}
.hero p{color:var(--muted);font-size:17px;line-height:2.2}
.actions{display:flex;gap:13px;justify-content:center;flex-wrap:wrap;margin-top:32px}
.btn{
 display:inline-flex;align-items:center;justify-content:center;
 padding:14px 25px;border-radius:40px;
 border:1px solid #b8ef7060;background:#b8ef7017;
 color:var(--lime);transition:.3s;cursor:pointer;
}
.btn.primary{background:var(--lime);color:#071b16;font-weight:900}
.btn:hover{transform:translateY(-5px);box-shadow:0 10px 30px #b8ef7025}
.stats{
 max-width:1120px;margin:-65px auto 70px;padding:0 20px;
 display:grid;grid-template-columns:repeat(3,1fr);gap:17px;
 position:relative;z-index:3;
}
.stat{
 text-align:center;padding:28px 15px;border-radius:22px;
 background:#102c20dd;border:1px solid #ffffff17;
 backdrop-filter:blur(20px);box-shadow:0 20px 50px #0003;
}
.stat strong{display:block;font-size:37px;color:var(--lime)}
.stat span{font-size:13px;color:var(--muted)}
main{max-width:1250px;margin:auto;padding:20px}
.heading{text-align:center;margin:50px 0 30px}
.heading .mini{color:var(--lime);font-size:12px;font-weight:800}
.heading h2{font-size:34px;margin:10px 0}
.heading p{color:var(--muted);line-height:2}
.controls{display:flex;gap:12px;margin:30px 0;flex-wrap:wrap}
.controls input,.controls select{
 background:#102a20;border:1px solid #ffffff20;color:white;
 border-radius:14px;padding:14px 16px;font-size:14px;outline:none;
}
.controls input{flex:1;min-width:220px}
.controls select{min-width:160px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{
 background:linear-gradient(145deg,#143729,#0b2118);
 border:1px solid #ffffff15;border-radius:25px;padding:24px;
 position:relative;overflow:hidden;transition:.4s;
 animation:appear .7s both;box-shadow:0 15px 40px #0002;
}
.card:before{
 content:"";position:absolute;width:150px;height:150px;top:-80px;left:-70px;
 background:var(--glow);filter:blur(55px);opacity:.2;
}
.card:hover{
 transform:translateY(-10px) rotateX(2deg);
 border-color:#b8ef7070;box-shadow:0 25px 55px #0005;
}
@keyframes appear{from{opacity:0;transform:translateY(25px)}to{opacity:1;transform:translateY(0)}}
.card-top{display:flex;align-items:center;justify-content:space-between}
.icon{font-size:35px}
.rank{
 background:#b8ef7018;color:var(--lime);
 border:1px solid #b8ef7055;border-radius:13px;padding:8px 13px;
 font-weight:900;font-size:13px;
}
.category{color:var(--lime);font-size:12px;margin-top:18px}
.card h3{font-size:19px;line-height:1.8;margin:8px 0}
.value{font-size:21px;font-weight:900;margin:15px 0;color:white}
.explain,.meaning{
 font-size:13px;line-height:2.1;color:#d0e4d8;
 padding:13px;margin-top:12px;border-radius:12px;
 background:#ffffff07;
}
.meaning{border-right:3px solid var(--lime);background:#b8ef700d}
.meta{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;color:var(--muted);font-size:11px;margin-top:17px}
.source{display:inline-block;margin-top:15px;color:var(--lime);font-size:12px}
.source:hover{text-decoration:underline}
.empty{display:none;text-align:center;padding:45px;color:var(--muted)}
.about{
 margin:65px 0 30px;padding:25px;border-radius:22px;
 background:#f6c75c0b;border:1px solid #f6c75c44;
 color:#f5e6c0;line-height:2.2;font-size:13px;
}
footer{
 margin-top:90px;text-align:center;padding:55px 20px;
 background:#04110c;border-top:1px solid #ffffff15;color:var(--muted);
}
footer strong{color:var(--lime)}
/* آدمک دنبال‌کننده موس */
#mascot{
 position:fixed;right:30px;bottom:25px;width:105px;height:145px;
 z-index:50;pointer-events:none;
 filter:drop-shadow(0 12px 20px #0008);
 animation:float 3s ease-in-out infinite;
 transform-origin:50% 85%;
}
@keyframes float{0%,100%{translate:0 0}50%{translate:0 -9px}}
.mascot-head{
 position:absolute;top:5px;left:14px;width:78px;height:77px;
 border-radius:48% 48% 44% 44%;
 background:linear-gradient(145deg,#b8ef70,#68b849);
 border:3px solid #e5ffc2;
 box-shadow:inset -8px -8px 0 #4e9a3b55,0 0 22px #b8ef7040;
}
.mascot-ear{position:absolute;top:28px;width:19px;height:26px;background:#79c653;border:2px solid #d7ffad;border-radius:50%}
.mascot-ear.left{left:0}.mascot-ear.right{right:0}
.eyes{position:absolute;top:27px;left:13px;right:13px;display:flex;justify-content:space-between}
.eye{
 width:21px;height:25px;border-radius:50%;background:#fff;
 position:relative;overflow:hidden;box-shadow:inset 0 -2px 3px #9ab98a;
}
.pupil{
 width:10px;height:13px;background:#10251b;border-radius:50%;
 position:absolute;top:6px;left:6px;transition:transform .08s;
}
.pupil:after{
 content:"";position:absolute;top:2px;left:2px;width:3px;height:3px;
 border-radius:50%;background:white;
}
.brow{position:absolute;top:18px;width:23px;height:4px;border-radius:5px;background:#397c32}
.brow.left{left:12px;transform:rotate(-7deg)}
.brow.right{right:12px;transform:rotate(7deg)}
.mouth{
 position:absolute;top:57px;left:31px;width:16px;height:8px;
 border-bottom:3px solid #27672b;border-radius:0 0 50% 50%;
}
.body{
 position:absolute;top:78px;left:24px;width:60px;height:53px;
 background:linear-gradient(145deg,#eaf8dc,#7ecb55);
 border-radius:23px 23px 15px 15px;
 border:2px solid #d7ffad;
}
.badge-mini{
 position:absolute;top:92px;left:44px;font-size:16px;
}
.arm{
 position:absolute;top:87px;width:14px;height:34px;
 background:#8bd35d;border:2px solid #d7ffad;border-radius:15px;
 transform-origin:top center;
}
.arm.left{left:14px;transform:rotate(25deg)}
.arm.right{right:12px;transform:rotate(-25deg)}
.leg{
 position:absolute;top:123px;width:17px;height:17px;
 border-radius:8px;background:#6bb94d;
}
.leg.left{left:30px}.leg.right{right:25px}
#mascot.blink .eye{transform:scaleY(.12)}
#mascot.clicked .mascot-head{transform:rotate(-9deg) scale(1.05)}
.mascot-label{
 position:absolute;bottom:-18px;right:-15px;
 white-space:nowrap;font-size:10px;color:var(--lime);
 background:#061710dd;padding:4px 9px;border-radius:20px;
 border:1px solid #b8ef7044;
}
#top{
 position:fixed;bottom:25px;left:25px;width:45px;height:45px;
 border:0;border-radius:50%;background:var(--lime);
 color:#071b16;font-size:22px;cursor:pointer;display:none;z-index:20;
}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){
 .navlinks{display:none}.hero{min-height:620px}
 .stats{grid-template-columns:1fr;margin-top:-35px}
 .grid{grid-template-columns:1fr}
 .heading h2{font-size:27px}
 #mascot{width:75px;height:105px;transform:scale(.75);transform-origin:bottom right;right:8px;bottom:8px}
}
@media(prefers-reduced-motion:reduce){
 *,*:before,*:after{animation-duration:.01ms!important;transition-duration:.01ms!important}
}
</style>
</head>
<body>
<canvas id="particles"></canvas>

<nav class="nav">
 <div class="brand">🇮🇷 ایران <span>در جهان</span></div>
 <div class="navlinks">
  <a href="#">خانه</a><a href="#rankings">دستاوردها</a><a href="#about">درباره پروژه</a>
 </div>
 <a class="navbtn" href="#rankings">مشاهده رتبه‌ها</a>
</nav>

<header class="hero">
 <div class="hero-content">
  <div class="flag">🇮🇷</div>
  <div class="tag">IRAN GLOBAL ACHIEVEMENTS</div>
  <h1>ایران در <span>جهان</span></h1>
  <p>
   نگاهی به جایگاه‌های برتر ایران در عرصه جهانی؛
   دستاوردها، آمارها و توضیح هر رتبه در یک تجربه تعاملی.
  </p>
  <div class="actions">
   <a class="btn primary" href="#rankings">کشف دستاوردها ↓</a>
   <a class="btn" href="#about">درباره آمارها</a>
  </div>
 </div>
</header>

<section class="stats">
 <div class="stat"><strong id="count">{{data|length}}</strong><span>رتبه ثبت‌شده</span></div>
 <div class="stat"><strong>۱ تا ۱۰</strong><span>بازه رتبه‌های جهانی</span></div>
 <div class="stat"><strong>۲۰۲۶</strong><span>سال نسخه وب‌سایت</span></div>
</section>

<main id="rankings">
 <div class="heading">
  <div class="mini">ACHIEVEMENT COLLECTION</div>
  <h2>دستاوردهای برتر ایران</h2>
  <p>هر رتبه را باز کن، مفهوم آن را بخوان و منبع اطلاعات را بررسی کن.</p>
 </div>

 <div class="controls">
  <input id="search" placeholder="🔎 جست‌وجوی دستاورد، شاخص یا توضیح...">
  <select id="category">
   <option value="all">همه حوزه‌ها</option>
   <option value="معدن و صنایع">معدن و صنایع</option>
   <option value="انرژی">انرژی</option>
  </select>
  <select id="sort">
   <option value="rank">بهترین رتبه</option>
   <option value="name">نام دستاورد</option>
  </select>
 </div>

 <div class="grid" id="grid">
 {% for item in data %}
 <article class="card" style="--glow:{{loop.index}}">
  <div class="card-top">
   <span class="icon">{{item.icon}}</span>
   <span class="rank">رتبه {{item.rank}} جهان</span>
  </div>
  <div class="category">{{item.category}}</div>
  <h3>{{item.title}}</h3>
  <div class="value">{{item.value}}</div>
  <div class="explain"><b>این دستاورد چیست؟</b><br>{{item.description}}</div>
  <div class="meaning"><b>این رتبه چه معنایی دارد؟</b><br>{{item.meaning}}</div>
  <div class="meta"><span>سال داده: {{item.year}}</span><span>رتبه: {{item.rank}} از ۱ تا ۱۰</span></div>
  <a class="source" href="{{item.url}}" target="_blank" rel="noopener">منبع: {{item.source}} ↗</a>
 </article>
 {% endfor %}
 </div>
 <div class="empty" id="empty">نتیجه‌ای پیدا نشد.</div>

 <div class="about" id="about">
  <b>درباره اطلاعات سایت</b><br>
  سال داده‌ها و سال انتشار گزارش باید از یکدیگر تفکیک شوند.
  اعداد این نسخه از فهرست قبلی پروژه منتقل شده‌اند و پیش از انتشار عمومی
  باید با جدول اصلی هر منبع و تعریف دقیق شاخص تطبیق داده شوند.
  رتبه‌های نمایش‌داده‌شده لزوماً همگی مربوط به سال ۲۰۲۶ نیستند.
 </div>
</main>

<footer>
 <div style="font-size:24px">🇮🇷 ایران در جهان</div>
 <p>دستاوردها را بشناسیم، دقیق و مستند معرفی کنیم.</p>
 <p>طراح و توسعه‌دهنده: <strong>محمد مهدی عباسی</strong></p>
 <small>© 2026 • تمام حقوق طراحی محفوظ است.</small>
</footer>

<div id="mascot" aria-hidden="true">
 <div class="mascot-ear left"></div><div class="mascot-ear right"></div>
 <div class="mascot-head">
  <div class="brow left"></div><div class="brow right"></div>
  <div class="eyes">
   <div class="eye"><div class="pupil"></div></div>
   <div class="eye"><div class="pupil"></div></div>
  </div>
  <div class="mouth"></div>
 </div>
 <div class="body"></div><div class="badge-mini">🇮🇷</div>
 <div class="arm left"></div><div class="arm right"></div>
 <div class="leg left"></div><div class="leg right"></div>
 <div class="mascot-label">سلام! من همراه توام 👋</div>
</div>

<button id="top" onclick="scrollTo({top:0,behavior:'smooth'})">↑</button>

<script>
/* جست‌وجو و فیلتر */
const search=document.getElementById('search');
const category=document.getElementById('category');
const sort=document.getElementById('sort');
const grid=document.getElementById('grid');
const empty=document.getElementById('empty');

function filterCards(){
 const cards=[...document.querySelectorAll('.card')];
 let count=0;
 cards.forEach(card=>{
  const text=card.innerText.toLowerCase();
  const q=search.value.trim().toLowerCase();
  const cat=category.value;
  const ok=text.includes(q)&&(cat==='all'||text.includes(cat));
  card.style.display=ok?'':'none';
  if(ok)count++;
 });
 empty.style.display=count?'none':'block';
}
search.addEventListener('input',filterCards);
category.addEventListener('change',filterCards);

sort.addEventListener('change',()=>{
 const cards=[...document.querySelectorAll('.card')];
 cards.sort((a,b)=>{
  if(sort.value==='name')
   return a.querySelector('h3').innerText.localeCompare(b.querySelector('h3').innerText,'fa');
  const ra=Number(a.querySelector('.rank').innerText.match(/\d+/)[0]);
  const rb=Number(b.querySelector('.rank').innerText.match(/\d+/)[0]);
  return ra-rb;
 });
 cards.forEach(c=>grid.appendChild(c));
});

/* چشم‌های آدمک دقیقاً موس را دنبال می‌کنند */
const mascot=document.getElementById('mascot');
const pupils=document.querySelectorAll('.pupil');
let mouseX=window.innerWidth/2;
let mouseY=window.innerHeight/2;

function moveEyes(x,y){
 pupils.forEach(p=>{
  const rect=p.parentElement.getBoundingClientRect();
  const cx=rect.left+rect.width/2;
  const cy=rect.top+rect.height/2;
  const angle=Math.atan2(y-cy,x-cx);
  const distance=Math.min(5,Math.hypot(x-cx,y-cy)/30);
  p.style.transform=`translate(${Math.cos(angle)*distance}px,${Math.sin(angle)*distance}px)`;
 });
 const dx=(x/window.innerWidth-.5)*13;
 mascot.style.rotate=`${dx}deg`;
}
window.addEventListener('mousemove',e=>{
 mouseX=e.clientX;mouseY=e.clientY;
 moveEyes(mouseX,mouseY);
});
window.addEventListener('touchmove',e=>{
 if(e.touches.length){
  mouseX=e.touches[0].clientX;
  mouseY=e.touches[0].clientY;
  moveEyes(mouseX,mouseY);
 }
},{passive:true});
document.addEventListener('click',()=>{
 mascot.classList.add('clicked');
 setTimeout(()=>mascot.classList.remove('clicked'),350);
});
/* پلک زدن تصادفی */
function blink(){
 mascot.classList.add('blink');
 setTimeout(()=>mascot.classList.remove('blink'),160);
 setTimeout(blink,2500+Math.random()*3500);
}
setTimeout(blink,2000);

/* ذرات نورانی پس‌زمینه */
const canvas=document.getElementById('particles');
const ctx=canvas.getContext('2d');
let particles=[];
function resize(){
 canvas.width=window.innerWidth*devicePixelRatio;
 canvas.height=window.innerHeight*devicePixelRatio;
 ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
}
window.addEventListener('resize',resize);
resize();

for(let i=0;i<75;i++){
 particles.push({
  x:Math.random()*innerWidth,
  y:Math.random()*innerHeight,
  r:Math.random()*2+0.5,
  vx:(Math.random()-.5)*.35,
  vy:(Math.random()-.5)*.35,
  a:Math.random()*.5+.15
 });
}
let frame=0;
function animate(){
 ctx.clearRect(0,0,innerWidth,innerHeight);
 particles.forEach((p,i)=>{
  p.x+=p.vx;p.y+=p.vy;
  if(p.x<0||p.x>innerWidth)p.vx*=-1;
  if(p.y<0||p.y>innerHeight)p.vy*=-1;
  ctx.beginPath();
  ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
  ctx.fillStyle=`rgba(184,239,112,${p.a})`;
  ctx.fill();
  for(let j=i+1;j<particles.length;j++){
   const q=particles[j];
   const d=Math.hypot(p.x-q.x,p.y-q.y);
   if(d<100){
    ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);
    ctx.strokeStyle=`rgba(184,239,112,${.08*(1-d/100)})`;
    ctx.stroke();
   }
  }
 });
 frame++;
 requestAnimationFrame(animate);
}
animate();

/* شمارنده و دکمه بازگشت */
const counter=document.getElementById('count');
const target=Number(counter.innerText);
let n=0;
const timer=setInterval(()=>{
 n++;
 counter.innerText=n;
 if(n>=target)clearInterval(timer);
},90);
window.addEventListener('scroll',()=>{
 document.getElementById('top').style.display=scrollY>450?'block':'none';
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE, data=DATA)

@app.route("/api/rankings")
def rankings():
    return jsonify(DATA)

@app.route("/api/stats")
def stats():
    return jsonify({
        "total": len(DATA),
        "year": 2026,
        "minimum_rank": 1,
        "maximum_rank": 10
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

