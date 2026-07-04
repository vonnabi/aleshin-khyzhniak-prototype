document.documentElement.classList.add('js');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const header=document.querySelector('.site-header');
const burger=document.querySelector('.burger');

const innerMenu=document.querySelector('.links');
if(innerMenu&&!innerMenu.querySelector('[data-home-link]')){
  innerMenu.insertAdjacentHTML('afterbegin','<a href="aleshin-corporate.html" data-home-link>Головна</a>');
}
if(innerMenu){
  [...innerMenu.querySelectorAll(':scope > a:not(.menu-consult)')].forEach((link,index)=>link.dataset.index=String(index+1).padStart(2,'0'));
  innerMenu.insertAdjacentHTML('afterbegin','<svg class="menu-art" viewBox="0 0 360 360" aria-hidden="true"><circle cx="180" cy="180" r="150"/><circle class="dash" cx="180" cy="180" r="122"/><circle cx="180" cy="180" r="68"/><path d="M180 30C236 98 262 124 330 180C262 236 236 262 180 330C124 262 98 236 30 180C98 124 124 98 180 30Z"/><path d="M180 68C218 116 244 142 292 180C244 218 218 244 180 292C142 244 116 218 68 180C116 142 142 116 180 68Z"/></svg><span class="menu-caption">МЕНЮ</span>');
  innerMenu.insertAdjacentHTML('beforeend','<a class="menu-consult" href="contact.html"><span>Отримати консультацію</span><span class="menu-consult-arrow" aria-hidden="true"><svg viewBox="0 0 18 18"><path d="M3.5 14.5 14.5 3.5M7 3.5h7.5V11"/></svg></span></a><div class="menu-meta"><div><small>Звʼязатися</small><a href="tel:+380994000303">+38 (099) 400 03 03</a></div><div class="online">Захист<br>і представництво</div></div>');
}

document.body.insertAdjacentHTML('afterbegin',`
  <canvas class="ambient-canvas" aria-hidden="true"></canvas>
  <div class="security-field" aria-hidden="true">
    <svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">
      <defs><g id="inner-petal"><path d="M0 0C42-104 126-104 168 0C126 104 42 104 0 0Z" class="fine"/><path d="M18 0C50-72 112-72 150 0C112 72 50 72 18 0Z" class="fine"/></g></defs>
      <g class="scroll-layer scroll-seal-a"><g class="seal-a medium"><g transform="translate(1180 205)"><circle r="210" class="fine"/><circle r="180" class="fine trace"/><circle r="112" class="fine"/><use href="#inner-petal" transform="rotate(0) scale(.72)"/><use href="#inner-petal" transform="rotate(45) scale(.72)"/><use href="#inner-petal" transform="rotate(90) scale(.72)"/><use href="#inner-petal" transform="rotate(135) scale(.72)"/></g></g></g>
      <g class="scroll-layer scroll-seal-b"><g class="seal-b faint"><g transform="translate(70 650)"><circle r="250" class="fine"/><circle r="205" class="fine trace"/><use href="#inner-petal" transform="rotate(15) scale(.9)"/><use href="#inner-petal" transform="rotate(75) scale(.9)"/><use href="#inner-petal" transform="rotate(135) scale(.9)"/></g></g></g>
      <g class="scroll-layer scroll-orbit"><g class="orbit bright"><path d="M460 120C690 10 910 35 1070 170S1280 480 1095 610S650 730 420 590" class="fine"/><path d="M430 155C680 70 890 85 1020 210S1160 470 1000 565S650 650 455 555" class="fine trace"/><circle cx="1068" cy="170" r="6" fill="#e8ca8d"/><circle cx="421" cy="590" r="4" fill="#e8ca8d"/></g></g>
      <g class="scroll-layer weave"><path d="M-80 190C180 20 380 370 650 190S1120 20 1510 210" class="fine trace"/><path d="M-100 330C170 510 410 120 720 330S1180 510 1540 300" class="fine"/><path d="M-80 470C210 280 430 650 760 455S1210 300 1510 480" class="fine trace"/><path d="M-40 610C250 790 500 410 810 620S1240 770 1500 590" class="fine"/></g>
      <g class="scroll-layer medallion"><g transform="translate(720 450)"><circle r="290" class="fine"/><circle r="245" class="fine trace"/><circle r="155" class="fine"/><use href="#inner-petal" transform="rotate(0) scale(1.05) translate(-84 0)"/><use href="#inner-petal" transform="rotate(60) scale(1.05) translate(-84 0)"/><use href="#inner-petal" transform="rotate(120) scale(1.05) translate(-84 0)"/></g></g>
    </svg>
  </div>
  <div class="scroll-progress" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div><div class="cursor-dot" aria-hidden="true"></div>
`);

const brandArrow='<svg class="brand-arrow" viewBox="0 0 18 18" aria-hidden="true"><path d="M3.5 14.5 14.5 3.5M7 3.5h7.5V11"/></svg>';
function replaceArrowText(elements,markup){
elements.forEach(element=>{
  [...element.childNodes].filter(node=>node.nodeType===Node.TEXT_NODE&&node.textContent.includes('↗')).forEach(node=>{
    const parts=node.textContent.split('↗');
    const fragment=document.createDocumentFragment();
    parts.forEach((part,index)=>{
      if(part)fragment.append(document.createTextNode(part.trimEnd()));
      if(index<parts.length-1){
        const template=document.createElement('template');
        template.innerHTML=markup;
        fragment.append(template.content.cloneNode(true));
      }
    });
    node.replaceWith(fragment);
  });
});
}
replaceArrowText(document.querySelectorAll('.go,.ar'),brandArrow);
replaceArrowText(document.querySelectorAll('.button,.btn'),'<span class="text-arrow" aria-hidden="true">↗︎</span>');

const progress=document.querySelector('.scroll-progress');
function updateChrome(){
  header?.classList.toggle('scrolled',scrollY>20);
  const max=document.documentElement.scrollHeight-innerHeight;
  if(progress)progress.style.width=`${max>0?scrollY/max*100:0}%`;
}
addEventListener('scroll',updateChrome,{passive:true});
addEventListener('resize',updateChrome,{passive:true});
updateChrome();

burger?.addEventListener('click',()=>{
  const open=document.body.classList.toggle('menu-open');
  burger.setAttribute('aria-expanded',String(open));
});
document.querySelectorAll('.links a').forEach(link=>link.addEventListener('click',()=>{
  document.body.classList.remove('menu-open');
  burger?.setAttribute('aria-expanded','false');
}));

const revealTargets=document.querySelectorAll('.metric,.card,.practice,.person,.case,.article,.split,.head,.contact-row,.form,.cta,.authority-title,.authority-portrait,.authority-copy,.home-heading,.practice-tile,.result-item,.media-intro,.media-row,.recognition-item');
revealTargets.forEach((element,index)=>{
  element.classList.add('reveal-item');
  element.style.transitionDelay=`${Math.min(index%4,3)*70}ms`;
});
if('IntersectionObserver' in window&&!reduce){
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target);}
  }),{threshold:.11,rootMargin:'0px 0px -30px'});
  revealTargets.forEach(element=>observer.observe(element));
}else revealTargets.forEach(element=>element.classList.add('is-visible'));

if(matchMedia('(hover:hover) and (pointer:fine)').matches&&!reduce){
  const ring=document.querySelector('.cursor-ring');
  const dot=document.querySelector('.cursor-dot');
  if(ring&&dot){
    document.body.classList.add('has-custom-cursor');
    let mouseX=innerWidth/2,mouseY=innerHeight/2,ringX=mouseX,ringY=mouseY;
    addEventListener('mousemove',event=>{
      mouseX=event.clientX;mouseY=event.clientY;
      dot.style.transform=`translate(${mouseX}px,${mouseY}px) translate(-50%,-50%)`;
    },{passive:true});
    (function followCursor(){
      ringX+=(mouseX-ringX)*.18;ringY+=(mouseY-ringY)*.18;
      ring.style.transform=`translate(${ringX}px,${ringY}px) translate(-50%,-50%)`;
      requestAnimationFrame(followCursor);
    })();
    document.querySelectorAll('a,button,.card,.practice,.person').forEach(element=>{
      element.addEventListener('mouseenter',()=>ring.classList.add('is-active'));
      element.addEventListener('mouseleave',()=>ring.classList.remove('is-active'));
    });
  }
}

const canvas=document.querySelector('.ambient-canvas');
if(canvas){
  const ctx=canvas.getContext('2d');
  let width=0,height=0,dpr=1,frame=0,particles=[],mx=.5,my=.5,targetX=.5,targetY=.5;
  const orbs=[
    {x:.12,y:.2,r:.36,s:.00016,p:0,a:.13,c:'215,180,111'},
    {x:.86,y:.14,r:.3,s:-.00013,p:2.1,a:.12,c:'173,137,83'},
    {x:.72,y:.82,r:.42,s:.0001,p:4.3,a:.085,c:'195,166,122'},
    {x:.34,y:.68,r:.28,s:-.00008,p:1.2,a:.055,c:'139,125,120'}
  ];
  function sizeCanvas(){
    dpr=Math.min(devicePixelRatio||1,2);width=innerWidth;height=innerHeight;
    canvas.width=width*dpr;canvas.height=height*dpr;canvas.style.width=`${width}px`;canvas.style.height=`${height}px`;
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  sizeCanvas();addEventListener('resize',sizeCanvas);
  if(!reduce)addEventListener('pointermove',event=>{targetX=event.clientX/width;targetY=event.clientY/height;},{passive:true});
  const count=reduce?18:Math.min(innerWidth<600?34:64,Math.floor(innerWidth/20));
  for(let i=0;i<count;i++)particles.push({x:Math.random(),y:Math.random(),r:Math.random()*1.35+.25,vx:(Math.random()-.5)*.000018,vy:-(Math.random()*.000025+.000006),a:Math.random()*.24+.035,z:Math.random()*.7+.3,p:Math.random()*6.283});
  function draw(time=0){
    ctx.clearRect(0,0,width,height);mx+=(targetX-mx)*.018;my+=(targetY-my)*.018;
    for(const orb of orbs){
      const x=(orb.x+Math.sin(time*orb.s+orb.p)*.07+(mx-.5)*.04)*width;
      const y=(orb.y+Math.cos(time*orb.s*.83+orb.p)*.075+(my-.5)*.035)*height;
      const radius=Math.max(width,height)*orb.r;
      const gradient=ctx.createRadialGradient(x,y,0,x,y,radius);
      gradient.addColorStop(0,`rgba(${orb.c},${orb.a})`);gradient.addColorStop(.38,`rgba(${orb.c},${orb.a*.38})`);gradient.addColorStop(1,'rgba(23,22,25,0)');
      ctx.fillStyle=gradient;ctx.fillRect(0,0,width,height);
    }
    for(const particle of particles){
      if(!reduce){particle.x+=particle.vx;particle.y+=particle.vy;if(particle.x<0)particle.x=1;if(particle.x>1)particle.x=0;if(particle.y<-.02){particle.y=1.02;particle.x=Math.random();}}
      const pulse=.7+Math.sin(time*.0007+particle.p)*.3;
      ctx.beginPath();ctx.arc(particle.x*width+(mx-.5)*12*particle.z,particle.y*height+(my-.5)*8*particle.z,particle.r*particle.z,0,6.283);
      ctx.fillStyle=`rgba(235,211,164,${particle.a*pulse})`;ctx.fill();
    }
    if(!reduce)frame=requestAnimationFrame(draw);
  }
  draw(reduce?1800:0);
  document.addEventListener('visibilitychange',()=>{if(reduce)return;if(document.hidden)cancelAnimationFrame(frame);else{cancelAnimationFrame(frame);frame=requestAnimationFrame(draw);}});
}

const securityField=document.querySelector('.security-field');
if(securityField){
  const layers={sealA:securityField.querySelector('.scroll-seal-a'),sealB:securityField.querySelector('.scroll-seal-b'),orbit:securityField.querySelector('.scroll-orbit'),weave:securityField.querySelector('.weave'),medallion:securityField.querySelector('.medallion')};
  let target=0,current=0,morphFrame=0;
  const clamp=value=>Math.max(0,Math.min(1,value));
  const mix=(a,b,t)=>a+(b-a)*t;
  const band=(p,start,peak,end)=>p<=start||p>=end?0:p<peak?(p-start)/(peak-start):(end-p)/(end-peak);
  function setLayer(element,x,y,scale,rotate,opacity){element.style.transform=`translate3d(${x}px,${y}px,0) scale(${scale}) rotate(${rotate}deg)`;element.style.opacity=opacity;}
  function drawMorph(p){
    const first=clamp(p/.34),middle=clamp((p-.24)/.42),final=clamp((p-.68)/.32),weave=band(p,.22,.58,.9);
    setLayer(layers.orbit,mix(0,-90,first),mix(0,75,middle),mix(1,.7,middle),mix(0,-16,middle),mix(1,.12,final));
    setLayer(layers.sealA,mix(0,-420,middle),mix(0,245,middle),mix(1,1.3,middle),mix(0,18,middle),mix(1,.28,final));
    setLayer(layers.sealB,mix(0,390,middle),mix(0,-225,middle),mix(1,1.22,middle),mix(0,-14,middle),mix(.7,.2,final));
    setLayer(layers.weave,mix(90,-70,middle),mix(80,-35,middle),mix(.86,1.08,middle),mix(-7,5,middle),weave*.28);
    setLayer(layers.medallion,0,mix(170,0,final),mix(.52,1.05,final),mix(-28,0,final),final*.23);
  }
  function morph(){current+=(target-current)*.065;if(Math.abs(target-current)<.0001)current=target;drawMorph(current);morphFrame=current===target?0:requestAnimationFrame(morph);}
  function updateMorph(){target=clamp(scrollY/Math.max(1,document.documentElement.scrollHeight-innerHeight));if(!morphFrame)morphFrame=requestAnimationFrame(morph);}
  addEventListener('scroll',updateMorph,{passive:true});addEventListener('resize',updateMorph,{passive:true});updateMorph();
}

const heroCoinVisual=document.querySelector('[data-hero-coin]');
if(heroCoinVisual&&!reduce&&matchMedia('(hover:hover) and (pointer:fine)').matches){
  let targetX=0,targetY=0,currentX=0,currentY=0,coinFrame=0;
  const moveCoin=()=>{
    currentX+=(targetX-currentX)*.075;
    currentY+=(targetY-currentY)*.075;
    heroCoinVisual.style.setProperty('--hero-parallax-x',`${currentX.toFixed(2)}px`);
    heroCoinVisual.style.setProperty('--hero-parallax-y',`${currentY.toFixed(2)}px`);
    coinFrame=requestAnimationFrame(moveCoin);
  };
  addEventListener('pointermove',event=>{
    targetX=(event.clientX/innerWidth-.5)*22;
    targetY=(event.clientY/innerHeight-.5)*16;
    if(!coinFrame)coinFrame=requestAnimationFrame(moveCoin);
  },{passive:true});
  document.addEventListener('mouseleave',()=>{targetX=0;targetY=0;},{passive:true});
}

const form=document.querySelector('[data-contact-form]');
form?.addEventListener('submit',event=>{
  event.preventDefault();
  const data=new FormData(form);
  const subject=encodeURIComponent(`Запит на консультацію — ${data.get('name')}`);
  const body=encodeURIComponent(`Імʼя: ${data.get('name')}\nКонтакт: ${data.get('contact')}\n\nЗавдання:\n${data.get('message')}`);
  location.href=`mailto:aleshin.partners@ukr.net?subject=${subject}&body=${body}`;
});

/* FAQ accordion (service pages) */
document.querySelectorAll('.faq-q').forEach(q=>{
  q.setAttribute('aria-expanded','false');
  q.addEventListener('click',()=>{
    const item=q.closest('.faq-item');
    const ans=item.querySelector('.faq-a');
    const open=item.classList.toggle('open');
    q.setAttribute('aria-expanded',String(open));
    ans.style.maxHeight=open?ans.scrollHeight+'px':'';
  });
});

/* Category filter bars (cases / team / media) */
document.querySelectorAll('.filter-bar').forEach(bar=>{
  const scope=bar.closest('section')||document;
  const chips=bar.querySelectorAll('.filter-chip');
  chips.forEach(chip=>chip.addEventListener('click',()=>{
    chips.forEach(c=>c.classList.remove('is-on'));
    chip.classList.add('is-on');
    const cat=chip.dataset.filter;
    scope.querySelectorAll('[data-cat]').forEach(el=>{
      const show=(cat==='all'||el.dataset.cat===cat);
      el.style.display=show?'':'none';
      if(show)el.classList.add('is-visible');
    });
  }));
});

/* Practices mega-menu (desktop dropdown) */
if(matchMedia('(hover:hover) and (pointer:fine)').matches){
  const trigger=[...document.querySelectorAll('.links > a')].find(a=>(a.getAttribute('href')||'').indexOf('practices.html')===0);
  if(trigger){
    const items=[
      ['practice-kryminalne.html','Захист','Кримінальне право'],
      ['practice-tsyvilne.html','Спори','Цивільне право'],
      ['practice-simejne.html','Приватні клієнти','Сімейне право'],
      ['practice-korporatyvne.html','Бізнес','Корпоративне право'],
      ['practice-migraczijne.html','Мобільність','Міграційне право'],
      ['practice-viiskove.html','ТЦК','Військове право']
    ];
    const panel=document.createElement('div');
    panel.className='practices-mega';
    panel.innerHTML=items.map(([href,tag,name])=>`<a href="${href}"><small>${tag}</small><b>${name}</b></a>`).join('');
    document.body.appendChild(panel);
    let hideTimer;
    const place=()=>{
      const r=trigger.getBoundingClientRect();
      panel.style.top=`${r.bottom+14}px`;
      const width=panel.offsetWidth||540;
      panel.style.left=`${Math.min(r.left,innerWidth-width-20)}px`;
    };
    const show=()=>{clearTimeout(hideTimer);place();panel.classList.add('open');};
    const hide=()=>{hideTimer=setTimeout(()=>panel.classList.remove('open'),150);};
    trigger.addEventListener('mouseenter',show);
    trigger.addEventListener('mouseleave',hide);
    panel.addEventListener('mouseenter',show);
    panel.addEventListener('mouseleave',hide);
    addEventListener('scroll',()=>panel.classList.remove('open'),{passive:true});
  }
}
