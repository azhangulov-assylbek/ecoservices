/* ecoservices.kz — демо-панель мониторинга, фильтр каталога, заявки
   Переводимые строки берутся из JS-каталога Django (jsi18n), подключённого перед этим файлом:
   gettext()/interpolate() определены глобально скриптом django.views.i18n.JavaScriptCatalog. */
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const uiLocale = document.documentElement.lang || "ru";
/* console */
const sensors = [
  {id:"so2", label:gettext("SO₂, дымовая труба № 1"), unit:"мг/нм³", base:172, noise:9, lim:200, dec:0, spike:true, c:"var(--c-climate)"},
  {id:"pm",  label:gettext("PM10, граница СЗЗ"), unit:"мкг/м³", base:38, noise:4, lim:60, dec:0, c:"var(--c-health)"},
  {id:"ph",  label:gettext("pH, водоём-охладитель"), unit:"", base:7.4, noise:.06, lim:8.5, dec:2, c:"var(--c-water)"},
  {id:"db",  label:gettext("Шум, жилая зона"), unit:"дБА", base:46, noise:1.5, lim:55, dec:0, c:"var(--c-health)"}
];
const N = 40, tilesEl = document.getElementById("tiles");
sensors.forEach(s=>{
  s.hist = Array.from({length:N},()=>s.base + (Math.random()-.5)*2*s.noise); s.alarm=false;
  const d = document.createElement("div"); d.className="tile"; d.id="t-"+s.id; d.style.setProperty("--tc", s.c);
  d.innerHTML = `<span class="t-label">${s.label}</span><span><span class="t-val num">0</span><span class="t-unit">${s.unit}</span></span>
    <span class="t-state">${gettext("в норме")}</span><svg viewBox="0 0 100 34" preserveAspectRatio="none" aria-hidden="true"><line class="lim" x1="0" x2="100"/><polyline class="spark"/></svg>`;
  tilesEl.appendChild(d);
});
let tick=0, spikeLeft=0;
const logEl=document.getElementById("log"), aiEl=document.getElementById("ai");
const hm=()=>new Date().toLocaleTimeString(uiLocale,{hour:"2-digit",minute:"2-digit"});
function addLog(t,al){const li=document.createElement("li");if(al)li.className="al";li.innerHTML=`<span class="num">${hm()}</span><b>${t}</b>`;logEl.prepend(li);while(logEl.children.length>6)logEl.lastChild.remove();}
function draw(s){
  const t=document.getElementById("t-"+s.id), v=s.hist[N-1];
  t.querySelector(".t-val").textContent=v.toFixed(s.dec).replace(".",",");
  const lo=Math.min(...s.hist,s.lim)*0.92, hi=Math.max(...s.hist,s.lim)*1.04, y=val=>32-(val-lo)/(hi-lo)*30;
  t.querySelector(".spark").setAttribute("points",s.hist.map((h,i)=>`${(i/(N-1)*100).toFixed(1)},${y(h).toFixed(1)}`).join(" "));
  const l=t.querySelector(".lim"); l.setAttribute("y1",y(s.lim)); l.setAttribute("y2",y(s.lim));
  const al=v>s.lim; t.classList.toggle("alarm",al);
  t.querySelector(".t-state").textContent = al?interpolate(gettext("выше ориентира %s"),[s.lim]):gettext("в норме");
  if(al&&!s.alarm){const pct=Math.round((v/s.lim-1)*100);addLog(interpolate(gettext("%(label)s: превышение на %(pct)s%%"),{label:s.label.split(",")[0],pct:pct},true),true);if(s.id==="so2")explain(Math.round(v),pct);}
  if(!al&&s.alarm)addLog(interpolate(gettext("%(label)s: вернулся в норму"),{label:s.label.split(",")[0]},true),false);
  s.alarm=al;
}
function step(){
  tick++; if(tick===4||(tick>4&&tick%26===0))spikeLeft=7;
  sensors.forEach(s=>{const target=(s.spike&&spikeLeft>0)?s.base*1.42:s.base, prev=s.hist[N-1];
    s.hist.push(prev+(target-prev)*0.45+(Math.random()-.5)*2*s.noise); s.hist.shift(); draw(s);});
  if(spikeLeft>0)spikeLeft--;
  document.getElementById("clock").textContent=new Date().toLocaleTimeString(uiLocale);
}
let typing=null;
function explain(val,pct){
  const parts=[
    interpolate(gettext("Концентрация SO₂ %(val)s мг/нм³, на %(pct)s%% выше ориентира НДТ для угольного котла этой мощности."),{val:val,pct:pct},true),
    gettext("Вероятная причина: рост содержания серы в поставке угля. Рекомендуемые техники: полусухая или мокрая известняковая сероочистка, контроль качества топлива.")
  ];
  const src=gettext("Справочник НДТ «Сжигание топлива на крупных установках в целях производства энергии», ПП РК от 23.01.2024 № 23");
  clearInterval(typing);
  aiEl.innerHTML=`<p id="a1"></p><p id="a2"></p><span class="src" id="a3" hidden>${src}</span>`;
  const el=[document.getElementById("a1"),document.getElementById("a2")], a3=document.getElementById("a3");
  if(reduce){el[0].textContent=parts[0];el[1].textContent=parts[1];a3.hidden=false;return;}
  let pi=0,ci=0;
  typing=setInterval(()=>{ci+=3;el[pi].innerHTML=parts[pi].slice(0,ci)+'<span class="caret"></span>';
    if(ci>=parts[pi].length){el[pi].textContent=parts[pi];pi++;ci=0;if(pi>=parts.length){clearInterval(typing);a3.hidden=false;}}},28);
}
sensors.forEach(draw); addLog(gettext("Подключено 4 поста мониторинга"),false); step(); setInterval(step,1500);

/* ---------- каталог: фильтр по задачам (данные в data-tasks строк) ---------- */
const chips=document.getElementById("chips");
if(chips){
  chips.addEventListener("click",e=>{
    const b=e.target.closest(".chip"); if(!b)return;
    chips.querySelectorAll(".chip").forEach(c=>c.setAttribute("aria-pressed",c===b));
    const task=b.dataset.task;
    document.querySelectorAll(".row[data-tasks]").forEach(r=>{
      const tasks=r.dataset.tasks.split(",");
      r.classList.toggle("dim",!(task==="all"||tasks.includes(task)));
    });
  });
}
/* «Сообщить о запуске»: пока только визуально. TODO: форма email -> модель NotifyRequest */
document.addEventListener("click",e=>{
  const b=e.target.closest("[data-notify]"); if(!b)return;
  const on=b.getAttribute("aria-pressed")!=="true";
  b.setAttribute("aria-pressed",on); b.textContent=on?gettext("Сообщим о запуске"):gettext("Сообщить о запуске");
});

/* ---------- заявка на оборудование: отправка на сервер ---------- */
const quote=document.getElementById("quote");
if(quote){
  const sent=document.getElementById("quote-sent"), err=document.getElementById("quote-error");
  document.querySelectorAll("[data-quote]").forEach(b=>b.addEventListener("click",()=>{
    document.getElementById("quote-title").textContent=interpolate(gettext("Запрос предложения: %s"),[b.dataset.quoteName]);
    quote.elements.equipment.value=b.dataset.quote;
    sent.hidden=true; err.hidden=true; quote.hidden=false; quote.elements.company.focus();
  }));
  document.getElementById("quote-close").addEventListener("click",()=>{quote.hidden=true;});
  quote.addEventListener("submit",async e=>{
    e.preventDefault(); err.hidden=true;
    try{
      const r=await fetch(quote.action,{method:"POST",body:new FormData(quote),headers:{"X-Requested-With":"fetch"}});
      if(!r.ok) throw new Error();
      sent.hidden=false; quote.reset();
    }catch(_){ err.hidden=false; }
  });
}
