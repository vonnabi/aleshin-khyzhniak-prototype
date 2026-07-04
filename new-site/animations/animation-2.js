/* Анімація №2 — збережений альтернативний canvas-концепт */
export function startAnimationTwo(canvas,{reducedMotion=false}={}){
  const ctx=canvas.getContext('2d');
  let width=0,height=0,dpr=1,frame=0;
  const particles=Array.from({length:reducedMotion?14:48},()=>({
    x:Math.random(),y:Math.random(),r:.5+Math.random()*1.4,
    speed:.00002+Math.random()*.00005,phase:Math.random()*Math.PI*2
  }));
  function size(){
    dpr=Math.min(devicePixelRatio||1,2);width=innerWidth;height=innerHeight;
    canvas.width=width*dpr;canvas.height=height*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  function draw(time=0){
    ctx.clearRect(0,0,width,height);
    [{x:.82,y:.08,r:.44,a:.10},{x:.08,y:.72,r:.36,a:.06},{x:.68,y:.9,r:.3,a:.045}].forEach((light,index)=>{
      const x=(light.x+Math.sin(time*.00012+index)*.035)*width;
      const y=(light.y+Math.cos(time*.0001+index)*.03)*height;
      const gradient=ctx.createRadialGradient(x,y,0,x,y,Math.max(width,height)*light.r);
      gradient.addColorStop(0,`rgba(210,172,109,${light.a})`);
      gradient.addColorStop(1,'rgba(210,172,109,0)');
      ctx.fillStyle=gradient;ctx.fillRect(0,0,width,height);
    });
    particles.forEach(particle=>{
      particle.y-=particle.speed*(reducedMotion?0:16);
      if(particle.y<-.02)particle.y=1.02;
      ctx.beginPath();ctx.arc(particle.x*width,particle.y*height,particle.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(240,220,174,${.12+Math.sin(time*.001+particle.phase)*.08})`;ctx.fill();
    });
    if(!reducedMotion)frame=requestAnimationFrame(draw);
  }
  size();addEventListener('resize',size);draw();
  return()=>cancelAnimationFrame(frame);
}
