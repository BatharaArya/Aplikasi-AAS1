import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Virtual Lab AAS 7000", page_icon="🔬", layout="wide")

THREE_LIBS = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
"""

# =====================================================================
# 1) MODEL 3D AAS (skala seragam 1 unit = 1 cm, proporsi 1:1 ke ukuran nyata)
# =====================================================================
AAS_HTML = THREE_LIBS + """
<style>
 body{margin:0;font-family:Segoe UI,Arial,sans-serif;background:#0f172a;color:#e2e8f0}
 #wrap{display:flex;flex-wrap:wrap;height:660px}
 #c{flex:1 1 480px;position:relative;min-height:420px}
 #panel{flex:0 0 330px;padding:14px;overflow:auto;background:#1e293b;font-size:14px;line-height:1.55;max-height:660px;box-sizing:border-box}
 #panel h3{margin:0 0 6px;color:#38bdf8}
 .chip{display:inline-block;margin:2px;padding:4px 9px;border-radius:14px;background:#334155;color:#e2e8f0;cursor:pointer;font-size:12px;border:1px solid #475569}
 .chip:hover,.chip.on{background:#0ea5e9;border-color:#0ea5e9}
 #hint{position:absolute;left:10px;top:8px;font-size:12px;color:#94a3b8;pointer-events:none}
 #tools{position:absolute;right:10px;top:8px;font-size:12px}
 #tools label{color:#cbd5e1;margin-left:8px;cursor:pointer}
</style>
<div id="wrap">
 <div id="c"><div id="hint">Putar: seret • Zoom: scroll • Klik komponen untuk penjelasan • 1 unit = 1 cm</div>
  <div id="tools"><label><input type="checkbox" id="rot"> Putar otomatis</label>
  <label><input type="checkbox" id="trans" checked> Bodi transparan</label></div></div>
 <div id="panel"><div id="chips"></div><hr style="border-color:#334155"><div id="info">
 <h3>Klik komponen AAS</h3>Klik bagian 3D atau tombol di atas untuk menampilkan fungsi dan prinsip kerjanya.</div></div>
</div>
<script>
const el=document.getElementById('c');
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x0f172a);
const camera=new THREE.PerspectiveCamera(45,el.clientWidth/el.clientHeight,0.1,2000);
camera.position.set(75,55,100);
const renderer=new THREE.WebGLRenderer({antialias:true}); renderer.setPixelRatio(devicePixelRatio);
renderer.setSize(el.clientWidth,el.clientHeight); el.appendChild(renderer.domElement);
const controls=new THREE.OrbitControls(camera,renderer.domElement); controls.target.set(0,15,0); controls.update();
scene.add(new THREE.AmbientLight(0xffffff,0.7));
const dl=new THREE.DirectionalLight(0xffffff,0.8); dl.position.set(60,100,80); scene.add(dl);
scene.add(new THREE.GridHelper(160,16,0x475569,0x334155));

const parts={}, pick=[];
function M(c,o){return new THREE.MeshStandardMaterial({color:c,transparent:o<1,opacity:o,metalness:.25,roughness:.55,emissive:0x000000});}
function reg(key,m,pickable=true){m.userData.key=key;(parts[key]=parts[key]||[]).push(m);scene.add(m);if(pickable)pick.push(m);return m;}
function box(k,w,h,d,x,y,z,c,o=1,p=true){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),M(c,o));m.position.set(x,y,z);return reg(k,m,p);}
function cyl(k,rt,rb,h,ax,x,y,z,c,o=1){const m=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,32),M(c,o));
 if(ax=='x')m.rotation.z=Math.PI/2; if(ax=='z')m.rotation.x=Math.PI/2; m.position.set(x,y,z);return reg(k,m);}

// ---- Bodi (ukuran perkiraan, ganti sesuai manual jika perlu): 46 x 34 x 57 cm
const body=box('body',46,34,57,0,17,0,0xe2e8f0,0.12,false);
const edges=new THREE.LineSegments(new THREE.EdgesGeometry(body.geometry),new THREE.LineBasicMaterial({color:0x94a3b8}));
edges.position.copy(body.position);scene.add(edges);
box('body',48,2,59,0,-1,0,0x94a3b8,1,false);

// ---- Jalur optik (sumbu x, tinggi y=14)
cyl('beam',0.3,0.3,28,'x',-1,14,0,0xfde047,0.7);
// Lampu katoda berongga + turret
cyl('hcl',2.3,2.3,9,'x',-15,14,0,0xf59e0b);
cyl('turret',6,6,2,'x',-21,14,0,0x64748b);
// Lampu D2 (koreksi latar)
cyl('d2',1.6,1.6,7,'z',-8,14,-9,0x818cf8);
// Atomizer nyala
cyl('chamber',3.2,3.2,9,'y',0,4.5,0,0x64748b);
cyl('nebulizer',0.9,0.9,6,'x',-6,5,0,0xf97316);
box('burner',11,1.2,0.7,0,10,0,0xcbd5e1);
const fl=new THREE.Mesh(new THREE.ConeGeometry(1.8,6,24),M(0xfb923c,0.6)); fl.position.set(0,13.6,0);reg('flame',fl);
box('drain',0.8,5,0.8,3.5,-0.5,0,0x0ea5e9);
// Monokromator + detektor
box('mono',10,10,12,10.5,14,0,0x22c55e,0.85);
cyl('pmt',2.5,2.5,5,'x',18,14,0,0xef4444);
// Kontrol gas (belakang)
box('gas',12,6,2,10,22,-27.5,0x334155);
cyl('gasport',0.7,0.7,3,'z',7,22,-29.5,0xfacc15);
cyl('gasport',0.7,0.7,3,'z',13,22,-29.5,0x60a5fa);
// Tungku grafit GFA-7000 (opsional, di sisi kiri)
box('gfa',22,20,25,-38,10,0,0xa78bfa,0.9);
// Autosampler ASC-7000 (sisi kanan)
box('asc',20,14,25,38,7,0,0x14b8a6,0.9);
cyl('asc',8,8,2,'y',38,15,0,0x2dd4bf);
// Komputer + monitor
box('pc',30,20,2,0,26,44,0x0f172a);
box('pc',26,16,0.4,0,26,45.1,0x38bdf8);
cyl('pc',1.5,1.5,10,'y',0,8,44,0x64748b);

const INFO={
 body:['Rangka / Bodi Utama','Rumah instrumen yang melindungi sistem optik dan atomizer, menjaga stabilitas suhu dan keselamatan operator (interlock, ventilasi). Ukuran model ±46 × 57 × 34 cm (perkiraan).'],
 beam:['Jalur Berkas Cahaya','Radiasi dari lampu melewati uap atom di nyala/tungku lalu menuju monokromator. Absorbansi mengikuti Hukum Lambert–Beer: A = ε·b·c.'],
 hcl:['Hollow Cathode Lamp (HCL)','Sumber radiasi garis spesifik unsur (mis. lampu Ca, λ 422,7 nm). Katoda dari logam analit; gas isian Ne/Ar tereksitasi sehingga atom katoda memancarkan garis yang sama dengan garis serapan analit. Setiap unsur butuh lampu sendiri.'],
 turret:['Turret Lampu Otomatis','AA-7000 memiliki turret multi-lampu (hingga 6). Lampu berikutnya dapat dipanaskan lebih dulu sehingga ganti unsur cepat dan stabil.'],
 d2:['Lampu Deuterium (D₂) – Koreksi Latar','Memancarkan spektrum kontinu (UV) untuk mengoreksi serapan latar (absorpsi molekul, hamburan) pada koreksi D₂. Latar diukur dengan D₂, lalu dikurangi dari serapan total. Shimadzu juga menyediakan koreksi SR (self-reversal).'],
 chamber:['Ruang Pengabut (Spray Chamber)','Mengubah aerosol menjadi tetesan halus dan seragam; tetesan besar dibuang ke drain. Terdapat impact bead untuk memecah tetesan.'],
 nebulizer:['Nebulizer','Menyedot larutan sampel (efek Venturi akibat aliran oksidan) dan mengubahnya menjadi aerosol. Laju hisap tipikal 4–6 mL/menit.'],
 burner:['Kepala Pembakar (Burner Head)','Slot panjang memberi lintasan optik panjang (b besar) sehingga sensitivitas tinggi. Udara–asetilena (±2300 °C) untuk Ca; N₂O–asetilena (±2700 °C) bila gangguan fosfat/Al sangat kuat dan dipakai burner khusus.'],
 flame:['Nyala (Atomizer)','Zona tempat desolvasi → penguapan → disosiasi sehingga terbentuk atom bebas Ca⁰ yang menyerap 422,7 nm. Senyawa tahan panas (Ca₃(PO₄)₂) menurunkan jumlah atom bebas.'],
 drain:['Saluran Drain','Membuang kelebihan cairan dari spray chamber melalui water-seal/liquid trap agar tidak ada gas balik (flashback). Wajib selalu terisi cairan.'],
 mono:['Monokromator','Memilih satu garis panjang gelombang (celah + kisi difraksi tipe Czerny–Turner) dan menyingkirkan emisi nyala serta garis lain. Lebar celah mempengaruhi resolusi dan intensitas.'],
 pmt:['Detektor – Photomultiplier Tube (PMT)','Mengubah foton menjadi arus listrik dan memperkuatnya. Sinyal intensitas (I dan I₀) dikonversi menjadi absorbansi oleh prosesor.'],
 gas:['Unit Kontrol Gas','Mengatur dan memantau aliran asetilena, udara, dan N₂O secara otomatis, dilengkapi sensor tekanan dan sistem keamanan (pemadaman otomatis jika kebocoran/tekanan abnormal).'],
 gasport:['Inlet Gas','Kuning: asetilena (C₂H₂, bahan bakar). Biru: udara/oksidan. Selang harus bebas kebocoran; periksa dengan larutan sabun, jangan memakai api.'],
 gfa:['Tungku Grafit GFA-7000 (opsional)','Atomisasi elektrotermal: tahap pengeringan → pengabuan → atomisasi → pembersihan. Sensitivitas ppb (µg/L) karena atom tertahan lama di jalur optik, volume sampel hanya 5–50 µL.'],
 asc:['Autosampler ASC-7000','Menyampaikan sampel, standar, dan blanko ke atomizer secara otomatis; mendukung pengenceran otomatis sehingga analisis banyak sampel lebih cepat dan presisi.'],
 pc:['Komputer & Perangkat Lunak WizAArd','Mengontrol instrumen, membuat kurva kalibrasi, menampilkan sinyal real-time, mengolah data, dan membuat laporan.']
};
const ORDER=['body','hcl','turret','d2','beam','nebulizer','chamber','burner','flame','drain','mono','pmt','gas','gasport','gfa','asc','pc'];
const chips=document.getElementById('chips'), info=document.getElementById('info');
ORDER.forEach(k=>{const s=document.createElement('span');s.className='chip';s.textContent=INFO[k][0].split(' (')[0].split(' –')[0];s.dataset.k=k;s.onclick=()=>sel(k);chips.appendChild(s);});
function sel(k){
 Object.values(parts).flat().forEach(m=>m.material.emissive.setHex(0));
 (parts[k]||[]).forEach(m=>m.material.emissive.setHex(0x2563eb));
 document.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',c.dataset.k==k));
 info.innerHTML='<h3>'+INFO[k][0]+'</h3>'+INFO[k][1];
}
const ray=new THREE.Raycaster(), mouse=new THREE.Vector2(); let down=null;
renderer.domElement.addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);
renderer.domElement.addEventListener('pointerup',e=>{
 if(!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;
 const r=renderer.domElement.getBoundingClientRect();
 mouse.set(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);
 ray.setFromCamera(mouse,camera); const h=ray.intersectObjects(pick);
 if(h.length)sel(h[0].object.userData.key);
});
document.getElementById('rot').onchange=e=>controls.autoRotate=e.target.checked;
document.getElementById('trans').onchange=e=>{body.visible=e.target.checked;};
addEventListener('resize',()=>{camera.aspect=el.clientWidth/el.clientHeight;camera.updateProjectionMatrix();renderer.setSize(el.clientWidth,el.clientHeight);});
let t=0;(function loop(){requestAnimationFrame(loop);t+=0.05;
 fl.scale.set(1,1+0.12*Math.sin(t*4),1);controls.update();renderer.render(scene,camera);})();
</script>
"""

# =====================================================================
# 2) SIMULASI 3D GANGGUAN FOSFAT PADA ANALISIS Ca
# =====================================================================
INTERF_HTML = THREE_LIBS + """
<style>
 body{margin:0;font-family:Segoe UI,Arial,sans-serif;background:#0f172a;color:#e2e8f0}
 #bar{padding:8px;background:#1e293b}
 .b{padding:7px 12px;margin:2px;border:1px solid #475569;background:#334155;color:#e2e8f0;border-radius:8px;cursor:pointer;font-size:13px}
 .b.on{background:#0ea5e9;border-color:#0ea5e9}
 #c{height:470px;position:relative}
 #cap{padding:10px 14px;background:#1e293b;font-size:14px;line-height:1.55;min-height:70px}
 #cap b{color:#38bdf8}
 #leg{position:absolute;left:8px;bottom:8px;font-size:12px;background:#0f172acc;padding:6px 8px;border-radius:6px}
 .d{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}
</style>
<div id="bar"></div>
<div id="c"><div id="leg">
 <span class="d" style="background:#3b82f6"></span>Ca²⁺ &nbsp;<span class="d" style="background:#ef4444"></span>PO₄³⁻ (O merah, P kuning)
 &nbsp;<span class="d" style="background:#22c55e"></span>Sr²⁺ &nbsp;<span class="d" style="background:#a855f7"></span>La³⁺
 &nbsp;<span class="d" style="background:#14b8a6"></span>EDTA &nbsp;(ukuran bola ∝ jari-jari ion, skala 1:1 relatif)</div></div>
<div id="cap"></div>
<script>
const el=document.getElementById('c');
const scene=new THREE.Scene();scene.background=new THREE.Color(0x0f172a);
const camera=new THREE.PerspectiveCamera(45,el.clientWidth/el.clientHeight,0.1,500);camera.position.set(0,12,34);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setSize(el.clientWidth,el.clientHeight);el.appendChild(renderer.domElement);
const controls=new THREE.OrbitControls(camera,renderer.domElement);controls.autoRotate=true;controls.autoRotateSpeed=1.2;
scene.add(new THREE.AmbientLight(0xffffff,0.75));const dl=new THREE.DirectionalLight(0xffffff,0.8);dl.position.set(20,30,20);scene.add(dl);

function label(txt,color,s){const c=document.createElement('canvas');c.width=512;c.height=64;const g=c.getContext('2d');
 g.font='bold 34px sans-serif';g.fillStyle=color;g.textAlign='center';g.fillText(txt,256,44);
 const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthTest:false}));
 sp.scale.set(16*s,2*s,1);return sp;}
function sph(r,c){return new THREE.Mesh(new THREE.SphereGeometry(r,24,24),new THREE.MeshStandardMaterial({color:c,roughness:.4,metalness:.1}));}
function ion(t){
 if(t=='Ca')return sph(1.0,0x3b82f6);
 if(t=='Sr')return sph(1.18,0x22c55e);
 if(t=='La')return sph(1.03,0xa855f7);
 if(t=='PO4'){const g=new THREE.Group();g.add(sph(0.55,0xfacc15));
  [[1,1,1],[-1,-1,1],[-1,1,-1],[1,-1,-1]].forEach(v=>{const o=sph(0.62,0xef4444);o.position.set(v[0]*0.75,v[1]*0.75,v[2]*0.75);g.add(o);});return g;}
 if(t=='EDTA'){const g=new THREE.Group();
  [0,1].forEach(i=>{const m=new THREE.Mesh(new THREE.TorusGeometry(2.0,0.28,12,40),new THREE.MeshStandardMaterial({color:0x14b8a6,transparent:true,opacity:.85}));
   m.rotation.x=i?Math.PI/2:0;g.add(m);});return g;}
}
function ring(types,r){return types.map((t,i)=>{const a=i/types.length*Math.PI*2;return{t:t,p:[Math.cos(a)*r,0,Math.sin(a)*r]};});}
const FLAME=()=>{const g=new THREE.Group();const m=new THREE.Mesh(new THREE.ConeGeometry(15,7,32,1,true),new THREE.MeshBasicMaterial({color:0xfb923c,transparent:true,opacity:.28,side:THREE.DoubleSide}));
 m.position.y=-12;g.add(m);const l=label('Nyala udara–C₂H₂ (±2300 °C)','#fdba74',0.8);l.position.set(0,-17,0);g.add(l);return g;};

const S=[
 {n:'1. Ca saja',cap:'<b>Tanpa pengganggu.</b> Ca²⁺ dalam nyala mudah terdisosiasi menjadi atom bebas Ca⁰ yang menyerap 422,7 nm. Jumlah atom bebas maksimum sehingga absorbansi sesuai konsentrasi (kurva kalibrasi benar).',
  cl:[[-8,3,0],[0,6,-4],[8,2,3],[-4,-4,5],[5,-3,-6],[0,0,6]].map(p=>({c:p,items:[{t:'Ca',p:[0,0,0]}],tag:'Ca²⁺'}))},
 {n:'2. Ca + fosfat (gangguan)',cap:'<b>Gangguan kimia.</b> PO₄³⁻ berikatan dengan Ca²⁺ membentuk <b>Ca₃(PO₄)₂</b> yang sangat stabil secara termal; pada suhu nyala udara–asetilena tidak terdisosiasi sempurna. Atom Ca⁰ yang terbentuk sedikit → absorbansi turun → hasil analisis terlalu rendah (galat negatif).',
  cl:[{c:[-8,1,0],items:ring(['Ca','PO4','Ca','PO4','Ca'],3.4),tag:'Ca₃(PO₄)₂ (sulit atomisasi)',b:1},
      {c:[8,3,-3],items:ring(['Ca','PO4','Ca','PO4','Ca'],3.4),tag:'Ca₃(PO₄)₂ (sulit atomisasi)',b:1}]},
 {n:'3. + Sr²⁺ / La³⁺ (releasing agent)',cap:'<b>Releasing agent.</b> Sr²⁺ dan La³⁺ (dibuat berlebih, mis. 0,1–1 % La atau Sr) berikatan dengan fosfat <b>lebih kuat</b> daripada Ca (membentuk Sr₃(PO₄)₂ dan LaPO₄ yang lebih stabil). PO₄³⁻ “ditangkap”, sehingga Ca²⁺ <b>terbebas</b> dan dapat teratomisasi → absorbansi pulih.',
  cl:[{c:[-10,2,-2],items:ring(['Sr','PO4','Sr','PO4','Sr'],3.4),tag:'Sr₃(PO₄)₂',b:1},
      {c:[10,1,-2],items:ring(['La','PO4'],1.9),tag:'LaPO₄',b:1},
      {c:[-3,7,5],items:[{t:'Ca',p:[0,0,0]}],tag:'Ca²⁺ bebas'},{c:[3,5,6],items:[{t:'Ca',p:[0,0,0]}],tag:'Ca²⁺ bebas'},
      {c:[0,-4,6],items:[{t:'Ca',p:[0,0,0]}],tag:'Ca²⁺ bebas'},{c:[-6,-5,3],items:[{t:'Ca',p:[0,0,0]}],tag:'Ca²⁺ bebas'}]},
 {n:'4. + EDTA (protecting agent)',cap:'<b>Protecting agent.</b> EDTA membentuk kompleks khelat stabil <b>Ca–EDTA</b> sehingga Ca terlindungi dari fosfat. Kompleks ini mudah terurai di nyala (ligan organik terbakar) sehingga Ca⁰ dibebaskan dan teratomisasi. Berbeda dengan Sr/La yang “merebut” fosfat, EDTA “membungkus” Ca.',
  cl:[[-8,3,0],[0,6,-4],[8,2,3],[-3,-4,5]].map(p=>({c:p,items:[{t:'Ca',p:[0,0,0]},{t:'EDTA',p:[0,0,0]}],tag:'Ca–EDTA'})).concat(
      [[9,-5,-4],[-10,-3,-5],[4,8,-8]].map(p=>({c:p,items:[{t:'PO4',p:[0,0,0]}],tag:'PO₄³⁻ (tidak bereaksi)'})))}
];

let world=null,groups=[];
function build(i){
 if(world)scene.remove(world);world=new THREE.Group();groups=[];world.add(FLAME());
 S[i].cl.forEach((c,k)=>{const g=new THREE.Group();g.position.set(...c.c);g.userData.ph=k*1.3;g.userData.base=g.position.clone();
  const pts=[];c.items.forEach(it=>{const o=ion(it.t);o.position.set(...it.p);g.add(o);pts.push(new THREE.Vector3(...it.p));});
  if(c.b&&pts.length>1){pts.push(pts[0]);g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineBasicMaterial({color:0xffffff})));}
  const l=label(c.tag,'#e2e8f0',0.7);l.position.set(0,5,0);g.add(l);world.add(g);groups.push(g);});
 scene.add(world);document.getElementById('cap').innerHTML=S[i].cap;
 document.querySelectorAll('.b').forEach((b,j)=>b.classList.toggle('on',j==i));
}
S.forEach((s,i)=>{const b=document.createElement('button');b.className='b';b.textContent=s.n;b.onclick=()=>build(i);document.getElementById('bar').appendChild(b);});
build(0);
addEventListener('resize',()=>{camera.aspect=el.clientWidth/el.clientHeight;camera.updateProjectionMatrix();renderer.setSize(el.clientWidth,el.clientHeight);});
let t=0;(function loop(){requestAnimationFrame(loop);t+=0.03;
 groups.forEach(g=>{const b=g.userData.base,p=g.userData.ph;g.position.set(b.x+0.5*Math.sin(t+p),b.y+0.6*Math.sin(t*1.3+p),b.z+0.5*Math.cos(t+p));g.rotation.y=t*0.3;});
 controls.update();renderer.render(scene,camera);})();
</script>
"""

# =====================================================================
# UI STREAMLIT
# =====================================================================
st.title("🔬 Virtual Lab Spektrofotometer Serapan Atom (AAS) – Shimadzu AA-7000")
st.caption("Model 3D interaktif • Kurva kalibrasi otomatis • Simulasi gangguan fosfat pada analisis Ca")

tab1, tab2, tab3 = st.tabs(["🧩 Model 3D AAS 7000", "📈 Kurva Kalibrasi & Hitung Sampel", "⚗️ Gangguan Ca: Sr²⁺, La³⁺, EDTA"])

# ---------------------- TAB 1 ----------------------
with tab1:
    st.markdown("Klik komponen pada model 3D (atau tombol di panel kanan) untuk melihat penjelasannya. "
                "Model dibuat dengan *skala seragam 1:1 (1 unit = 1 cm)* tanpa distorsi sumbu. "
                "Dimensi adalah perkiraan; sesuaikan dengan manual resmi bila diperlukan.")
    components.html(AAS_HTML, height=680, scrolling=False)

# ---------------------- TAB 2 ----------------------
with tab2:
    st.subheader("Data Deret Standar")
    c1, c2 = st.columns([1, 1.4])
    with c1:
        satuan = st.selectbox("Satuan konsentrasi", ["mg/L (ppm)", "µg/L (ppb)", "mol/L"], index=0)
        unit = satuan.split(" ")[0]
        origin = st.checkbox("Paksa garis melalui titik nol (intercept = 0)", value=False)
        default = pd.DataFrame({"Konsentrasi": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
                                "Absorbansi": [0.002, 0.052, 0.101, 0.153, 0.198, 0.251]})
        df = st.data_editor(default, num_rows="dynamic", use_container_width=True, key="std",
                            column_config={"Konsentrasi": st.column_config.NumberColumn(f"Konsentrasi ({unit})", format="%.4f"),
                                           "Absorbansi": st.column_config.NumberColumn("Absorbansi", format="%.4f")})
    d = df.dropna()
    ok = len(d) >= 2 and d["Konsentrasi"].nunique() >= 2
    with c2:
        if not ok:
            st.info("Masukkan minimal 2 titik data dengan konsentrasi berbeda.")
        else:
            x = d["Konsentrasi"].to_numpy(float); y = d["Absorbansi"].to_numpy(float)
            if origin:
                m = float((x * y).sum() / (x * x).sum()); b = 0.0
            else:
                m, b = np.polyfit(x, y, 1)
            yhat = m * x + b
            ss_res = float(((y - yhat) * 2).sum()); ss_tot = float(((y - y.mean()) * 2).sum())
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
            r = np.corrcoef(x, y)[0, 1] if len(x) > 2 or not origin else float(np.sqrt(max(r2, 0)))
            sign = "+" if b >= 0 else "−"
            st.success(f"*Persamaan regresi:* y = {m:.5f}x {sign} {abs(b):.5f}")
            k1, k2, k3 = st.columns(3)
            k1.metric("Slope (m)", f"{m:.5f}"); k2.metric("Koefisien korelasi (r)", f"{r:.5f}"); k3.metric("R²", f"{r2:.5f}")
            if r2 < 0.995:
                st.warning("R² < 0,995 – periksa deret standar (pengenceran, kontaminasi, atau titik pencilan).")
            xs = np.linspace(min(x.min(), 0), x.max() * 1.05, 50)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="Standar", marker=dict(size=10)))
            fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", name="Regresi"))
            fig.update_layout(xaxis_title=f"Konsentrasi ({unit})", yaxis_title="Absorbansi", height=360,
                              margin=dict(l=10, r=10, t=30, b=10), title=f"y = {m:.5f}x {sign} {abs(b):.5f} | R² = {r2:.5f}")
            st.plotly_chart(fig, use_container_width=True)

    if ok:
        st.subheader("Hitung Konsentrasi Sampel")
        s_def = pd.DataFrame({"Nama sampel": ["Sampel 1", "Sampel 2"], "Absorbansi": [0.120, 0.180], "Faktor pengenceran": [1.0, 1.0]})
        smp = st.data_editor(s_def, num_rows="dynamic", use_container_width=True, key="smp")
        res = smp.dropna(subset=["Absorbansi"]).copy()
        if m == 0:
            st.error("Slope = 0, konsentrasi tidak dapat dihitung.")
        else:
            fp = res["Faktor pengenceran"].fillna(1.0)
            res[f"Konsentrasi terukur ({unit})"] = (res["Absorbansi"] - b) / m
            res[f"Konsentrasi sampel asli ({unit})"] = res[f"Konsentrasi terukur ({unit})"] * fp
            amin, amax = y.min(), y.max()
            res["Status"] = np.where((res["Absorbansi"] >= amin) & (res["Absorbansi"] <= amax), "Dalam rentang",
                                     "⚠️ Di luar rentang kalibrasi")
            st.dataframe(res.style.format({"Absorbansi": "{:.4f}", f"Konsentrasi terukur ({unit})": "{:.4f}",
                                           f"Konsentrasi sampel asli ({unit})": "{:.4f}"}), use_container_width=True)
            st.caption("Rumus: x = (y − b) / m, lalu dikalikan faktor pengenceran. "
                       "Hasil di luar rentang standar sebaiknya diencerkan/diukur ulang.")
            st.download_button("⬇️ Unduh hasil (CSV)", res.to_csv(index=False).encode("utf-8"), "hasil_aas.csv", "text/csv")

# ---------------------- TAB 3 ----------------------
with tab3:
    st.markdown("Pilih tahap 1–4 pada tombol di dalam visual 3D. Ion digambar dengan *skala relatif 1:1* "
                "(Ca²⁺ ≈ 100 pm, Sr²⁺ ≈ 118 pm, La³⁺ ≈ 103 pm). Seret untuk memutar, scroll untuk zoom.")
    components.html(INTERF_HTML, height=640, scrolling=False)
    st.markdown("""
*Ringkasan kimia*

| Agen | Jenis | Mekanisme | Reaksi |
|---|---|---|---|
| Fosfat (PO₄³⁻) | Pengganggu | Membentuk senyawa Ca tahan panas, atom bebas Ca⁰ berkurang | 3Ca²⁺ + 2PO₄³⁻ → Ca₃(PO₄)₂ |
| Sr²⁺ / La³⁺ | Releasing agent | Mengikat fosfat lebih kuat daripada Ca sehingga Ca terbebas | La³⁺ + PO₄³⁻ → LaPO₄; 3Sr²⁺ + 2PO₄³⁻ → Sr₃(PO₄)₂ |
| EDTA | Protecting agent | Membentuk kompleks khelat Ca–EDTA yang terurai di nyala | Ca²⁺ + EDTA⁴⁻ → [Ca(EDTA)]²⁻ |

Alternatif lain: memakai nyala *N₂O–asetilena* yang lebih panas (±2700 °C) sehingga Ca₃(PO₄)₂ ikut terdisosiasi,
atau metode adisi standar / matrix matching.
""")
