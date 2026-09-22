![](images/b6f87b85f4b7951eb3fc363a5f3ccd0846474a5eff7d0b8a763ee05fefb73cd0.jpg)


# Electrical and optical performances investigation of planar solar blind photodetector based on ${ \sf I Z T O } / { \sf G a } _ { 2 } 0 _ { 3 }$ Schottky diode via TCAD simulation

Naila Boulahia<sup>1</sup> · Walid Filali<sup>2</sup> · Dalila Hocine<sup>1</sup> · Slimane Oussalah<sup>3</sup> · Nouredine Sengouga<sup>4</sup> 

Received: 19 November 2023 / Accepted: 28 December 2023 / Published online: 30 January 2024 © The Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature 2024 

## Abstract

The development of sophisticated solar-blind photodetector devices is being motivated by the increasing need for solar-blind sensors with remarkable photosensitive qualities. This work is a modeling and simulation of electrical and optical properties of a Schottky photodetector based on gallium oxide $( \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } )$ , one of the most promising wide-band-gap material. It focuses on the optimization of the device structure design, assumed fully transparent to visible light. In addition, analysis of electrical and optical properties of ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 } .$ -based photodetector was carried out to accurately describe physical phenomenon through the semiconductor bulk. The impact of several parameters of the device on its performances is such as layer thickness, doping concentration, and electron afinity, anode work function and diferent cathode contact materials. Besides that, and for more understanding the real behaviors within diferent layers of the photodetector, diverse optical parameters were varied, for instance the light power intensity and the spectral response by changing the optical wavelength. The obtained results show a promising performance enhancement compared to previous works, for instance the photo to dark current ratio of $3 \times 1 0 ^ { 4 }$ , the good spec tral responsivity in UV light illumination [250–350 nm], in addition to the relatively high detectivity of $2 . 5 \times 1 0 ^ { 9 }$ (Jones). 

Keywords Gallium oxide · Photodetector · Silvaco · UV light · Wide bandgap 

## 1 Introduction

There are numerous wavebands within the electromagnetic spectrum of ultraviolet (UV) radiation, such as UVA, UVB, UVC, and vacuum UV (VUV) (Hou et al. 2020). The ozone layer mostly absorbs UVC and VUV light from solar UV radiation before it reaches the earth’s surface, where UV wavelengths range of 200–280 nm is known as the "solar-blind" waveband (Lee et al. 2017). 

The rapid development in power electronic, automotive and optoelectronic components are mainly driven by advances in specific wide-band-gap semiconductor-based devices with high performance (Shur 2019; Tang et al. 2021). In the recent years, intensive work was devoted to ultra-wide bandgap (UWBG) semiconductors materials including aluminum gallium nitride alloys $( \mathrm { { A l } _ { x } \mathrm { { G a } _ { 1 - x } \mathrm { { N } ) } } }$ , GaN, diamond, SiC, and a number of other UWBG binary and ternary oxides owing to their outstanding radiation hardness, chemical and thermal stability in addition to an eficient absorption of a specific wavelength light (Qin et  al. 2021; Raj et  al. 2021), due to the strong inherent critical breakdown electric field, their thin drift region and low on-state resistance (Zhang et al. 2022). Among them, Gallium oxide $( \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } )$ is one of the aforementioned semiconductors with an indirect bandgap of 4.5–5.2  eV. Although; it has six polymorphs (α, β, γ, δ, ε, and k) (Galazka et  al. 2021; Higashiwaki et  al. 2020; Mandal et  al. 2022), the beta-phase ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ is the most stable, due to its physical properties such as thermal stability for the operational temperature range up to the melting point, a high breakdown electrical field of~ 8 MV/cm and its high saturation velocity of $1 \times 1 0 ^ { 7 }$ cm/s. Furthermore, its important optical properties has demonstrated that is colorless and high transparent to the UV-C range of the light spectrum (Galazka et al. 2021; Labed et al. 2021a). One-dimensional (1D) high surface-to-volume ratio of nanostructured UV detectors has drawn interest due to their high light sensitivity. However, due to the dominance of surface photocurrent and the high temperature of UV detectors based on nanostructured semiconductors, they encounter dificult conditions, and hence, bulk-dominated photocurrents are preferred (Sang et al. 2013). 

Light emitting diodes, phototransistors, photo-detectors (PDs) and other optoelectronic devices based on $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ attracted a great interest from the researcher’s community in recent years in order to enhance and achieve the desired performance responding to real world issues (Guo et al. 2019; Kumar et al. 2023; Ping et al. 2021). To deal with this concern, and especially to $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } – \mathrm { b a s e d P D s }$ , various structures (designs) such as metal–semiconductor–metal (MSM), Schottky barrier diode (SBD) and metal–oxide –semiconductor (MOS) photo-detectors have been proposed. Diferent elaboration techniques and deposition methods; halide vapor phase epitaxy (HVPE), metal–organic chemical vapor deposition (MOCVD) and molecular beam epitaxial (MBE) are used for the growth of $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ semiconductor layer (Labed et al. 2021b; Patil-Chaudhari et al. 2017; Pearton et al. 2018; Singh Pratiyush et al. 2017; Yadav et al. 2020; Zhang et al. 2022). 

Several researchers focused on this field by fabrication of fully transparent solar-blind photodectors based on ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ semiconductor as an active layer. Those works show a high transmittance up to 80% from visible to near infrared (NIR) optical wavelengths, in addition to a low dark current value $( { \sim } 1 0 ^ { - 9 } \mathrm { A } )$ (Wei et  al. 2014). One of the used structures based on ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ Schottky diode was investigated in a recent work (Kim et  al. 2022), where both InZnSnO (IZTO) and InSnO (ITO) were used as Schottky and ohmic contacts, respectively. With high rectifying ratio and workfunction of the studied photodetector, it ofers several advantages in terms of fast photodetection, responsivity, and precisely it react as self-powered photodetectors (Zou et al. 2018). 

The aim of this work is the analysis and investigation of electrical and optical simulated characteristics of Schottky ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ -based photodetector (PD). This PD, which consists of a top-contact made of Indium-Zinc-Tin oxide (IZTO) and diferent transparent conductive oxides (TCOs) (Choi et al. 2010; Heo et al. 2013) as Schottky and ohmic contacts, respectively on ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 } ,$ was analyzed using Silvaco TCAD simulator (Filali et al. 2017). The efect of doping concentration, thickness, workfunction and electron afinity of ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ semiconductor were performed. Moreover, the impact of optical parameters of the beam power and wavelength variation on the device performance was carried out to evaluate the figures of merit (FOM) of the PD namely sensitivity, responsivity, and detectivity. A deep analysis of the obtained results could be advantageous for the enhancement of UV selfpowered photodetectors. 

## 2 Device design and structure

The simulation study of the Schottky PD based on $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ semiconductor was carried out using Silvaco ATLAS software (Filali et  al. 2017), which is a vast environment tool for the design, modelling and simulation of semiconductor-based devices under diferent conditions by solving the main equations describing conduction in semiconductors such as continuity and Poisson (Labed et al. 2021b; Sze et al. 2021). Such simulation can give an overview of the device functioning and performance. Figure 1 shows a 3D schematic illustration of the structure suggested in this study. In Silvaco ATLAS, each material (layer) in the specified structure is considered as a region with diferent geometrical and physical parameters. The mesh definition is a crucial parameter in such simulation, which lead to solve the diferential equations related to various mechanisms through the material bulk. Mesh refinement is important at junction’s location or for metal–semiconductor interfaces. 

In this structure; firstly, starting by a quartz substrate with a thickness of 800  µm which will be taken into account in the simulation stage by enlarging the mesh spacing. Quartz is considered as extremely versatile material used in diferent optoelectronic domains with outstanding thermal stability properties related to both elaboration or functionality temperature change, excellent optical transmission, efective electrical insulation and anti-corrosion performances. Secondly, diferent doping concentration and thicknesses of ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ film ranging from $3 \times 1 0 ^ { \overline { { 1 6 } } }$ to $1 \times 1 0 ^ { 1 8 } ~ \mathrm { c m } ^ { - 3 }$ and from 100 to 900 nm, respectively, have been implemented in ATLAS tool. As mentioned before, our structure is top-contacts configuration, where both electrodes IZTO as Schottky contact (150 nm thickness and 1 µm width) and Al as an ohmic contact (150 nm thickness and 1 µm width) were deposited on the top of the efective semiconductor layer $( \beta \mathrm { - } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } )$ . In order to elaborate a fully transparent photodetector and to analyze the efect of ohmic contact material on the optical characteristics of the device in question, several transparent conductive oxides (TCOs) such as AZO, ITO, FTO and IZO have been chosen according to their work function values. Other test has been simulated to demonstrate the impact of Schottky contact workfunction on the device performance. Knowing that ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ material did not exist in the used software library (Filali et al. 2018; Sze et  al. 2021), this issue lead to another important contribution in this study which is expressed by the implementation of diferent material properties such as the electronic gap, electron afinity, electrons and holes mass and mobility, traps capture cross section and density…etc. After introducing these parameters within the code, it is necessary to input refractive index (n) and extinction coeficient (k) variation with wavelength which are extracted from previous experimental works (Choi et al. 2010; Heo et al. 2013; Labed et al. 2022; Rebien et al. 2002) for the used materials (quartz, contacts and $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 } )$ 


Fig. 1 A general 3D schematic view of photodetector based on $\mathrm { T C O } / \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$


![](images/fb14bbbee75459b21ebe3380d60c334400fdbb001dfda37fb445640a22b1f7ed.jpg)


Once the structure has been designed and all the related material’s parameters have been implemented, the simulation phase to obtain electrical and optical characteristics of the device in question is initiated under diferent condition such as beam power intensity, semiconductor afinity and optical wavelength variation. The whole operation was carried out using diferent models: Shockley Read Hall (SRH), Auger and Band Gap Narrowing (BGN), Arora and impact Selb models to evaluate photodetector performance under dark, illumination and light spectrum variation conditions. Equation 1 describes the recombination SRH rate $( \mathrm { R } _ { \mathrm { S R H } } )$ which is the net recombination of photo-generated carriers inside the semiconductor bulk (Labed et al. 2022; Sze et al. 2021). 

$$
R _ {S R H} = \frac {p n - n _ {i} ^ {2}}{\tau_ {p} \left[ n + n _ {i} \exp \left(\frac {E _ {T}}{K T}\right) \right] + \tau_ {n} [ p + n _ {i} \exp (\frac {- E _ {T}}{K T}) ]}\tag{1}
$$

where p, n and $\mathfrak { n } _ { \mathrm { i } }$ denotes hole, electron and intrinsic carrier concentration, respectively. $\tau _ { \mathrm { p } }$ and $\tau _ { \mathrm { n } }$ are lifetimes for holes and electrons, respectively, T is absolute temperature and K is the Boltzmann constant. In the simulation, we take account the traps in the bandgap of the semiconductor and the values are from (Labed et al. 2022) The diference between trap and intrinsic level energies is denoted by $\mathrm { E _ { T } }$ . Table 1 (Pearton et al. 2018; Rebien et al. 2002) lists a set of incorporated ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ material properties into the software library. 

## 3 Results and discussion

The obtained simulation results of the pre-designed Schottky ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ based photodetector are described below. 


Table 1 $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 }$ material parameters implemented to software library


<table><tr><td>Symbol</td><td>Parameter</td><td>Values</td></tr><tr><td><eq>\text{Eg (eV)}</eq></td><td>Bandgap</td><td>4.8</td></tr><tr><td><eq>N_{D} (cm^{-3})</eq></td><td>Donor concentration</td><td><eq>3 \times 10^{16}</eq></td></tr><tr><td><eq>N_{C} (cm^{-3})</eq></td><td>Effective density of states in the conduction band</td><td><eq>3.7 \times 10^{18}</eq></td></tr><tr><td><eq>N_{V} (cm^{-3})</eq></td><td>Effective density of states in the valance band</td><td><eq>5 \times 10^{18}</eq></td></tr><tr><td><eq>\mu_{n} (cm^{2}V^{-1} s^{-1})</eq></td><td>Electron mobility</td><td>172</td></tr><tr><td><eq>\mu_{p} (cm^{2}V^{-1} s^{-1})</eq></td><td>Hole mobility</td><td>10</td></tr><tr><td><eq>m_{n}</eq></td><td>Effective mass of electrons</td><td>0.28</td></tr><tr><td><eq>m_{p}</eq></td><td>Effective mass of holes</td><td>0.35</td></tr><tr><td><eq>\chi (eV)</eq></td><td>Affinity</td><td>4</td></tr><tr><td><eq>\varepsilon_{r}</eq></td><td>Relative permittivity</td><td>12.6</td></tr><tr><td><eq>v_{\text{sat}} (cm s^{-1})</eq></td><td>Saturation velocity (<eq>cm s^{-1}</eq>)</td><td><eq>10^{7}</eq></td></tr></table>

## 3.1 Dark and illumination I–V characteristics

Dark and illumination currents densities as a function of bias voltage were compared and depicted in Fig. 2a. $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ layer thickness was fixed at 300 nm. Firstly, one can observe a typical rectifying behavior of Schottky structure $\left( \mathrm { I Z T O } / \mathrm { \beta } { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } \right)$ due to the diference between the work function value of IZTO and the electron afinity of $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ (Lee et  al. 2007). Secondly, it can be seen from the graph at reverse bias that under illumination condition (255 nm wavelength and optical power of $1 0 0 \mathrm { m W } / \mathrm { c m } ^ { 2 } )$ , an apparent enhancement in the current density compared to that at darkness. Indeed, the reverse current increases from $1 0 ^ { - 3 }$ to $1 0 ^ { - 1 }$ A when the device is illuminated. In this case, within the depletion region at the $\beta – \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } / \mathrm { I Z T O }$ interface, the electric field is suficient to split the photogenerated electron–hole pairs towards their corresponding electrodes, thus creating the photocurrent. Thirdly, at direct bias, a slight shift of the threshold voltage $( \mathrm { V _ { t h } } )$ could be remarked. 

As an important figure of merit for such device, the photo to dark current ratio (PDCR) (Young et al. 2008) is defined as the ratio of the current under illumination to the dark current (Eq. 2). Figure 2b shows the dependence of the contrast ratio on the reverse applied voltage under illumination. It is evaluated from $1 0 ^ { 2 }$ to $3 \times 1 0 ^ { 4 }$ at − 2 and 0 V, respectively. 

![](images/0ff8b4492295fb9fc9816b42f0a01b0b854034f17cb925e8677478c22504a8cd.jpg)


![](images/bea294d553d8b8c4345f24011638488bb0b875cd8efb84c0a4d6f13152e09d7d.jpg)



Fig. 2 a Simulated I–V characteristics of $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 }$ photodiode under darkness and illumination of 100 mW/ $\mathrm { c m } ^ { 2 }$ , and b calculated contrast ratio as a function bias


Otherwise, it reflect the sensitivity of the device to a specific wavelength (255 nm), this is attributed to the presence of hole-trap states associated with oxygen atoms, which afect the photoresponse mechanism (Labed et al. 2022). 

$$
\mathrm{PDCR} = \frac {\mathrm {I_ {illum}}}{\mathrm {I_ {dark}}}\tag{2}
$$

where $\mathrm { { I } _ { i l l u m } }$ and $\mathrm { I } _ { \mathrm { d a r k } }$ are the current under illumination and dark, respectively. Higher sensitivity reflects high and well rectifying behavior of Schottky-based photodetector. 

## 3.2 Effect of light intensity

As presented in Fig. 3, the increase in beam power intensity has a seeming impact on the photocurrent at reverse and 0 V bias, where at reverse voltage [− 2 to near 0 V] it rise from $\mathrm { \dot { 8 } } \times 1 0 ^ { - 4 } \mathrm { t o } 2 \times 1 0 ^ { - 3 } \mathrm { A / c m } ^ { 2 }$ for 1 and $1 0 ^ { 3 }$ m $\mathrm { { _ { 1 W / c m } } } ^ { 2 }$ beam intensities, respectively. At 0 V, the photocurrent density reaches $1 0 ^ { - 3 } \mathrm { \ A / c m } ^ { 2 }$ for the high beam intensity. This augmentation is related to the correlation between photo absorption and photo generation phenomenon at the bulk of $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 }$ layer across the IZTO contact and the resulted photocurrent. This outcome concurs with the ones that was attained in previous works (Labed et  al. 2022; Periyanagounder et al. 2018; Wu et al. 2021). 

## 3.3 Effect of $\pmb { \beta } \mathbf { - G a } _ { 2 } \pmb { 0 } _ { 3 }$ layer thickness

Both beam power and optical wavelength are fixed at $1 0 ^ { 2 } \ \mathrm { m W } / \mathrm { c m } ^ { 2 }$ and 255 nm, respectively. The efect of $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ layer thickness on the I–V characteristics is shown in Fig. 4a. It can be been noted that the current density increases with increasing ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ layer thickness. The thicker semiconductor layer, leads to an increase of electron–hole pairs generation, which is manifested by an increase in photocurrent (Sharma et al. 2017). Figure 4b shows the linearity of the photocurrent as function of thickness rise. 

![](images/b2f927f12aeb885ac2c4948a0f4f8287570e54dbb72b327f526db07efca034f4.jpg)



Fig. 3 Simulated I–V characteristics of $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 }$ photodiode under diferent light intensitie


![](images/b91d257f87d15108fcb7b61f2a1a7b433fa7cfb390d14135666fedd5aef64a77.jpg)


![](images/1e92bb7bb52e363d31d067a227f2224253b8ade64e5ad3db4509ec602a9ea17e.jpg)



Fig. 4 a Simulated I–V characteristics from 100 to 900 nm thickness under an illumination of 100 $\mathrm { m W } / \mathrm { c m } ^ { 2 }$ and b Current density as function of layer thickness at − 1 and 1 V


## 3.4 Efect of Schottky contact work function

Another parameter that can afect the I–V characteristic of the device in question is the work function $( \mathrm { W _ { f } } )$ variation for the IZTO Schottky electrode (Anode). As can be seen from Fig. 5, for fixed 300 nm thick structure, by varying the $\mathrm { W _ { f } }$ from 3.78 to 4.58 eV, an increase in current density was observed with decreasing work function until it saturates at $6 . 2 \times 1 0 ^ { 3 } \mathrm { A / c m } ^ { 2 }$ for a 3,98 eV work function. This outcome is related to the diminution in the barrier height $( \varphi _ { \flat } )$ at the heterojunction interface, which leads for carriers charge being able to surmount the lowest barrier height (Filali et al. 2017). 

## 3.5 Efect of $\mathbf { G a } _ { 2 } \mathbf { 0 } _ { 3 }$ afinity

Additional, as shown in Fig. 6 below. At direct bias polarization, an apparent influence of the afinity of β-Ga2O3 current–voltage characteristics was remarked. Seeing first the shift 


Fig. 5 Simulated I–V characteristics for different metal’s work function


![](images/f29d987ad3e11158f4a31a5abf101977621b441d3d74d500e658b4fb1dccc425.jpg)



Fig. 6 Simulated I–V characteristics for diferent semiconducto afinities


![](images/c38642881d8a5b65dc029e0d13803445d82dcf9b9330006da07d4313a2fd1b8a.jpg)



of the threshold voltage $( \mathrm { V _ { t h } } )$ from 0.22 V to 0.8 V as well as the insignificant decrease of the saturation current in function of increasing afinity of semiconductors. These results are in good agreement with those obtained in the literature where the afinity is highly dependent to the structural and morphological composition of the semiconductor layer (Labed et al. 2022; Mao 2007).


## 3.6 Efect of $\pmb { \beta } \mathbf { - G a } _ { 2 } \pmb { 0 } _ { 3 }$ doping concentration

Figure 7a shows the efect of doping concentration variation on the electrical I–V characteristics of the photodetector, for both reverse and forward current density. As the doping concentration increases from $3 \times 1 0 ^ { 1 6 } ~ \mathrm { t o } ~ 1 0 ^ { 1 8 } ~ \mathrm { c m } ^ { - 3 }$ , a significant rise in current density from $1 0 ^ { - 3 }$ to $1 0 ^ { - 2 } \mathrm { \ A } / \mathrm { c m } ^ { 2 }$ is noticed. These phenomena mainly due to the enhancement in the carriers (electron–hole) within the bulk of ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ , when they react according to the bias voltage under illumination to participate on the photo-generation mechanism, in addition to the important impact of doping concentration on the diference between conduction band and Fermi level energy which will afect the conductivity of the device (Mao 2007; Sze et  al. 2021). As depicted in Fig.  7b, an apparent increase in photocurrent with increasing in semiconductor doping concentration, this is with correlation with result shows in Fig. 7a. 

![](images/0faef29e56b61a9b481ce2c704b1d2fc60a42792985f24e31ccc9168acc11917.jpg)


![](images/d8dbb3027e4e4857c9e29092aae5e9b2e870522aecb6b7669fe73a17f6957f57.jpg)



Fig. 7 a Simulated I–V characteristics of β-Ga2O3 photodiode for diferent doping concentration and b plot of current density as function of ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ doping concentration


As presented in Fig.  8, an apparent efect of doping concentration of ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ semiconductor layer on the band bending of the conduction and valence energy bands. One can see that heavily doped semiconductor has narrow space-charge region width that allows electrons to tunnel from the metal to semiconductor and from semiconductor to the metal. This phenomenon is called tunneling efect. 

## 3.7 Efect of ohmic contact material

In order to evaluate the performance for diferent cathode contact materials, four transparent conductive oxides: Aluminium-Zinc Oxide (AZO), Fluorine-Tin oxide (FTO), Indium-Tin oxide (ITO) and Indium-Zinc oxide (IZO) were tested. The choice of those $\mathrm { T C O ^ { \circ } s }$ was based on their both electrical and optical properties discussed in several previous works (Choi et  al. 2010; Heo et  al. 2013). Figure  9 shows the current density–voltage (J–V) at the forward bias. Knowing that both ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ layer thickness and beam power intensity are fixed to 300 nm and $1 0 ^ { \overline { { 2 } } }$ m ${ \mathrm { W } } / { \mathrm { c m } } ^ { 2 } .$ , respectively. It can be seen that there is large gap between the current values of ITO and AZO contacts compared to that of IZO and FTO. This diference is around 4 decades till reaches $5 \times 1 0 ^ { 3 } ~ \mathrm { A } / \mathrm { c m } ^ { 2 }$ This diference is commonly attributed to the good but not perfect transmission properties of the used $\mathrm { T C O ^ { \circ } s }$ that leads to some absorption losses in photodetection. On the other hand, materials stoichiometry and defects in bulk could afect the resistivity, which lead to an increase or decrease on electrical contact conductivity (Chesson 2021; Choi et al. 2010; Fang et al. 2006). 

Fig. 8 Equilibrium bands diagram variation with $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 }$ doping concentration change at $0 . 2 5 5$ µm optical wavelength and $1 0 ^ { 2 }$ mW/cm<sup>2</sup>) 

![](images/686f3966f49e7ac9bcca9b2339903f8235a92df127be5b18884478024825fdd5.jpg)



Fig. 9 Simulated I–V characteristics for transparent conductive oxides (TCOs) according to their work function values


![](images/45b38ebaddc924d7262f9c53fa046750c32272d97dcb3b5e347fba16cb02d161.jpg)


## 3.8 Efect of optical wavelength

In order to investigate the behavior of the Schottky ${ \beta } { \mathrm { - G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ based photodetector with different optical wavelengths (UV and visible), the semiconductor absorption layer $( \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } )$ thickness is fixed at 300  nm while the beam power is set to 100 mW/cm<sup>2</sup>. The reverse current density as a function of wavelength and responsivity are presented in Fig. 10a, b, respectively. Figure 10c presents the photocurrent versus wavelength variation at -2 V. The current steadily increases with increasing wavelength starting from just above 100 nm and peaks at 250, 254 and 256 nm for 100, 500 and 1000 $\mathrm { m W } / \mathrm { c m } ^ { - 2 }$ , respectively, the response peak at 255  nm wavelength demonstrates the excellent selectivity of $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ absorption layer, which responds solely to the solar-blind UV with wavelengths below 261 nm. These finding agree with those reported in a previous work (Li et al. 2023; Sharma et al. 2017). Responsivity is another important figure of merit that confirms the well-functioning mechanism of the UV photodetector with specific wavelength. The responsivity (R) (Liao 2022; Sze et al. 2021) is considered as a measure of the efectiveness of the conversion of the light power into electrical current. Hence, R is defined as the ratio of the photocurrent $( \mathrm { I _ { p h } } )$ to the incident light power $( \mathrm { P _ { o p t } } )$ at a given wavelength: 

$$
\mathrm{R} = \frac {\mathrm {I_ {ph}}}{\mathrm {P_ {opt}}}\tag{3}
$$

As can be seen from Fig. 11b, the device has shown a maximum responsivity around 0.23 A/W for UV light wavelengths 250, 254 and 256 nm. This outcome is in good agreement with literature bibliography about $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ optical properties, where the wavelengths around 250 nm corresponds to the optical absorption edge of this material (Pearton et al. 2018; Rebien et al. 2002). In addition, these results indicate that the photo-generated carriers in the device are mostly excited by solar-blind radiation (UV light) with a higher energy than $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ band gap, possibly, the deep defect levels, which are associated with oxygen vacancies, are the source of this occurrence. Photocurrent is produced when electrons in oxygen vacancies are stimulated to the conduction band (Labed et  al. 2022; Mao 2007; Rebien et al. 2002). 

![](images/c5e4c49e6b85d3468066cc1cd4288f009ab1e236666bfca05d7fd5f32ce4cd8f.jpg)


![](images/7a3055dbc3a9bc210d571b0430184a7dc394cd7ce37e41583185f15d50da1b04.jpg)


![](images/2445af8e71595989151daaaf260e67fa4ac3e37505fd55c2e641d33f5cd26807.jpg)



Fig. 10 Simulated a I–V characteristics, b responsivity as a function of the incident light wavelength and c current density as function of optical wavelength variation from 155 to 855 nm at − 2 V


Figure 11a–c presents the plot of the photoabsorption rate across $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ layer with different wavelengths irradiance. It can be seen that the high photoabsorption rate value was obtained where we irradiate the photodetector with 0.255  µm wavelength compared to 0.355 and 0.455 µm, which is in good correlation with result obtained in Fig. 10b (responsivity). Other simulations were done to confirm previous results as depicted in Fig.  11d, the photogeneration rate has the highest value $1 \dot { 0 } ^ { 2 2 } \mathrm { c m } ^ { - 3 } \mathrm { s } ^ { - 1 }$ for irradiance of 0.255 µm. A decrease in the photogeneration rate gowing deeply in the bulk of $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Layer can be explained by the photons absorption (at 0.255 µm) which have energy higher than $\mathrm { E _ { g } }$ of ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ , consequently an important carriers charge generation which lead to high measured photocurrent value. 

Depending to the used device type, structure and configuration, the detectivity (D) expressed by $\mathrm { ( c m H z ^ { 1 / 2 } / W ) }$ or (Jones) is a pivotal metric used to assess the performance of photodetectors (Chakrabarti et al. 2003; Hazra et al. 2014). It exhibits the capability of the device to describe the slightest detectable optical signals. 

$$
\mathrm{D} = \frac {q \lambda \eta}{h c} \times \left(\frac {R _ {A}}{4 k T}\right) ^ {1 / 2}\tag{4}
$$

![](images/f9ba724dbc498e87f0531fc69c503910db37cd3b591e72505d59375dea27368c.jpg)


![](images/7c0ad433238414290d05e2cc03a2e443182d7bf70767085f8b5142e9f4b88674.jpg)


![](images/1df375d7fb7a685ac01b7820f2868c3904e4159ee26d1e02b5c78a70dc7c4b72.jpg)


![](images/15ac89d003ccd47caed9b0a7e2a7141a7ceb30b9051e46869f1c8036d874c5e0.jpg)



Fig. 11 A Tonyplot of photoabsorption rate at a 0.255 µm, b 0.355 µm, c 0.455 µm and d photogeneration rate of the three wavelengths 0.255, 0.355 and 0.455 µm through $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ bulk


where k, T, ${ \mathfrak { q } } , { \mathfrak { h } } , { \mathfrak { c } } , \lambda ,$ and $\boldsymbol { \mathsf { \Pi } } ^ { \boldsymbol { \mathsf { \Pi } } }$ represent Boltzmann constant, lattice temperature, electronic charge, Plank’s constant, velocity of light, illumination wavelength, and quantum eficiency $[ \boldsymbol \eta = \mathbf { R } \times ( \mathbf { h c } / \mathbf { q } \lambda ) ]$ , respectively. $\mathrm { R _ { A } }$ is the resistance-area product of the device and can be obtained from J–V characteristics as follows (Lee et al. 2004): 

$$
R _ {A} = \left(\frac {\partial J}{\partial V}\right) ^ {- 1}\tag{5}
$$

As can be seen from Fig. 12, detectivity value was calculated according to (Ali et al. 2010; Chakrabarti et al. 2003) and found to be $2 . 5 \times 1 0 ^ { 9 }$ (Jones) which is in good accordance with that obtained in a previous work (Wang et al. 2020). Table 2 presents a comparison of some parameters of the present Schottky β-Ga2O3 based photodetector with previous works. 

## 4 Conclusion

In this work, a conception and simulation of planar top contacts heterojunction Schottky photodetector based on β-phase gallium oxide semiconductor were investigated. The design and simulation phases were carried out using Silvaco™ TCAD simulation software. 

![](images/4e106559020cc21da9bea6956a76cfccaa08cefdd764a4a7ccb133278bebc41b.jpg)



Fig. 12 Photodetector detectivity as a function of optical wavelength for − 2 V bias voltage and 100 mW/ cm<sup>2</sup> power light intensity



Table 2 presents a comparison of some parameters of the present Schottky $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 }$ based photodetector with previous work


<table><tr><td>substrate</td><td>Contacts / semiconductor</td><td>Bias (V)</td><td><eq>I_{Photo}</eq>/<eq>I_{Dark}</eq></td><td>R (mA/W)</td><td>D (Jones)</td><td>Ref</td></tr><tr><td>Diamond</td><td>Ti/Au/ β-Ga2O3</td><td>0</td><td>37</td><td>0.2</td><td>6.9×109</td><td>Chen et al. (2018)</td></tr><tr><td>Sapphire</td><td>Ag/Ga2O3</td><td>-</td><td>122</td><td>5.7×10-2</td><td>5.4×109</td><td>Wang et al. (2020)</td></tr><tr><td>Quartz</td><td>IZTO/ β-Ga2O3</td><td>-2 V</td><td>3×104</td><td>225</td><td>2.5×109</td><td>Our work</td></tr><tr><td>NSTO</td><td>Au/Ti/Ga2O3</td><td>0</td><td>20</td><td>2.6</td><td>-</td><td>Daoyou et al. (2017)</td></tr><tr><td>6H-SiC</td><td>Au/ β-Ga2O3</td><td>-2</td><td>103</td><td>68</td><td>-</td><td>Nakagomi et al. (2013)</td></tr></table>

The establishment of new materials library for $\mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ , IZTO and diferent TCOs with their diferent properties was incorporated. The simulation results showed that diferent parameters of $\beta \mathrm { - G a } _ { 2 } \mathrm { O } _ { 3 }$ such as doping concentration, layer thickness, workfunction and electron afinity as well as light power intensity and wavelength afect its opto-electrical performances. These results present a good accordance with several recent published works in terms of rectifying behavior of the Schottky-based photodetector, under dark and UV light irradiance. A contrast ratio found $3 \times 1 0 ^ { 4 }$ which signifies the well functioning of the proposed device under dark and illumination conditions. In addition, both responsivity and detectivity were found to be $\mathrm { R } { = } 0 . 2 3 \ \mathrm { A } / \mathrm { W }$ and ${ \mathrm { D } } { = } 2 . 5 { \times } 1 0 ^ { 9 }$ Jones, respectively, which are similar to those obtained in quasi-similar studies. A great dependence on the afinity and workfunction was remarked by the shift in $\mathrm { V _ { t h } }$ values, this prove the correlation between physical phenomenon within the device and the electrical conductivity. At zero bias voltage, a current value of $1 0 ^ { - 3 } \mathrm { A } / \mathrm { c m } ^ { 2 }$ for $1 0 0 \mathrm { m W } / \mathrm { c m } ^ { 2 }$ was observed, which reflect the property of self-powered for the studied photodetector. The entire obtained results can broaden the elaboration of such device and enhance its performances to become an alternative of other Schottky diodes for photodetection. 

Acknowledgements The authors are grateful for Dr. Madani Labed and Dr Mohammed Labed for their support and recommendations. 

Author contributions All authors have contributed to the study simulation and investigation. Material preparation, data collection and analysis were performed by Boulahia Naila, and Filali Walid. The first draft of the manuscript was written by Boulahia Naila and Hocine Dalila. Results analysis and validation have been done by Boulahia Naila, Oussalah Slimane and Noureddine Sengouga All authors read and approved the final manuscript. 

Funding The authors declare that no funds, grants, or other support were received during the preparation of this manuscript 

## Declarations

Conflict of interest The authors declare no competing interests. 

## References



Ali, G.M., Chakrabarti, P.: Performance of ZnO-based ultraviolet photodetectors under varying thermal treatment. IEEE Photonics J. (5), 784–793 (2010) 





Chakrabarti, P., Krier, A., Morgan, A.: Analysis and simulation of a mid-infrared P/sup+/-InAs/sub 0.55/ Sb/sub 0.15/P/sub 0.30//n/sup 0/-InAs/sub 0.89/Sb/sub 0.11//N/sup+/-InAs/sub 0.55/Sb/sub 0.15/P/ sub 0.30/double heterojunction photodetector grown by LPE. IEEE Trans. Electron Devices 50(10), 2049–2058 (2003) 





Chen, Y.-C., Lu, Y.-J., Lin, C.-N., Tian, Y.-Z., Gao, C.-J., Dong, L., Shan, C.-X.: Self-powered diamond/ β-Ga 2 O 3 photodetectors for solar-blind imaging. J. Mater. Chem. C 6(21), 5727–5732 (2018) 





Chesson, D.A.: Efect of of-stoichiometry on electrical conductivity in Ni-Fe and Mn-Co spinel systems. J. Electrochem. Soc. (12), 124515 (2020). https://doi.org/10.1149/1945-7111/abae3a 





Choi, K.-H., Jeong, J.-A., Kim, H.-K.: Dependence of electrical, optical, and structural properties on the thickness of IZTO thin films grown by linear facing target sputtering for organic solar cells. Sol. Energy Mater. Sol. Cells 94(10), 1822–1830 (2010) 





Daoyou, G., Han, L., Peigang, L., Zhenping, W., Shunli, W., Can, C., Chaorong, L., Weihua, T.: Zeropower-consumption solar-blind photodetector based on β-Ga2O3/NSTO heterojunction (2017). 





Fang, T.-T., Mei, L.-T., Ho, H.-F.: Efects of Cu stoichiometry on the microstructures, barrier-layer structures, electrical conduction, dielectric responses, and stability of CaCu3Ti4O12. Acta Mater. 54(10), 2867–2875 (2006) 





Filali, W., Sengouga, N., Oussalah, S., Mari, R.H., Jameel, D., Al Saqri, N.A., Aziz, M., Taylor, D., Henini, M.: Characterisation of temperature dependent parameters of multi-quantum well (MQW) Ti/Au/n-AlGaAs/n-GaAs/n-AlGaAs Schottky diodes. Superlattices Microstruct. 111, 1010–1021 (2017) 





Filali, W., Oussalah, S., Sengouga, N., Henini, M., Taylor, D.: Simulation of p-type Schottky diode based on Al 0.29 Ga 0.71 As with titanium/gold Schottky contact. In: 2018 30th International Conference on Microelectronics (ICM). IEEE 272–275 (2018) 





Galazka, Z., Ganschow, S., Irmscher, K., Klimm, D., Albrecht, M., Schewski, R., Pietsch, M., Schulz, T., Dittmar, A., Kwasniewski, A.: Bulk single crystals of β-Ga2O3 and Ga-based spinels as ultra-wide bandgap transparent semiconducting oxides. Prog. Cryst. Growth Charact. Mater. 67(1), 100511 (2021). https://doi.org/10.1016/j.pcrysgrow.2020.100511 





Guo, D., Guo, Q., Chen, Z., Wu, Z., Li, P., Tang, W.: Review of Ga2O3-based optoelectronic devices. Mater. Today Phys. 11, 100157 (2019). https://doi.org/10.1016/j.mtphys.2019.100157 





Hazra, P., Singh, S., Jit, S.: Ultraviolet photodetection properties of ZnO/Si heterojunction diodes fabricated by ALD technique without using a bufer layer. J. Semicond. Technol. Sci. 14(1), 117–123 (2014) 





Heo, S.W., Ko, Y.D., Kim, Y.S., Moon, D.K.: Enhanced performance in polymer light emitting diodes using an indium–zinc–tin oxide transparent anode by the controlling of oxygen partial pressure at room temperature. J. Mater. Chem. C (42), 7009–7019 (2013) 





Higashiwaki, M., Fujita, S.: Materials Properties, Crystal Growth, and Devices. Springer, Switzerland (2020) 





Hou, X., Zou, Y., Ding, M., Qin, Y., Zhang, Z., Ma, X., Tan, P., Yu, S., Zhou, X., Zhao, X.: Review of polymorphous Ga2O3 materials and their solar-blind photodetector applications. J. Phys. D Appl. Phys. 54(4), 043001 (2020). https://doi.org/10.1088/1361-6463/abbb45 





Kim, H., Seok, H.-J., Park, J.H., Chung, K.-B., Kyoung, S., Kim, H.-K., Rim, Y.S.: Fully transparent InZnSnO/β-Ga2O3/InSnO solar-blind photodetectors with high schottky barrier height and lowdefect interfaces. J. Alloys Compd. 890, 161931 (2022). https://doi.org/10.1016/j.jallcom.2021. 161931 





Kumar, A., Singh, L., Bag, A.: Tailoring of structural and optical properties of electrosprayed β-Ga2O3 nanostructures via self-assembly. Opt. Quant. Electron. 55(5), 437 (2023).https://doi.org/10.1007/ s11082-023-04707-x 





Labed, M., Park, J.H., Meftah, A., Sengouga, N., Hong, J.Y., Jung, Y.-K., Rim, Y.S.: Low temperature modeling of Ni/β-Ga2O3 Schottky barrier diode interface. ACS Appl. Electron. Mater. 3(8), 3667–3673 (2021a) 





Labed, M., Sengouga, N., Labed, M., Meftah, A., Kyoung, S., Kim, H., Rim, Y.S.: Modeling a Ni/β Ga2O3 Schottky barrier diode deposited by confined magnetic-field-based sputtering. J. Phys. D Appl. Phys. 54(11), 115102 (2021b). https://doi.org/10.1088/1361-6463/abce2c 





Labed, M., Kim, H., Park, J.H., Labed, M., Meftah, A., Sengouga, N., Rim, Y.S.: Physical operations of a self-powered IZTO/β-Ga2O3 Schottky barrier diode photodetector. Nanomaterials 12(7), 1061 (2022). https://doi.org/10.3390/nano12071061 





Lee, J.-H., Yeo, B.-W., Park, B.-O.: Efects of the annealing treatment on electrical and optical properties of ZnO transparent conduction films by ultrasonic spraying pyrolysis. Thin Solid Films 457(2), 333–337 (2004) 





Lee, H.Y., Lichtenwalner, D.J., Jur, J.S., Kingon, A.I.: Investigation of conducting oxide and metal electrode work functions on lanthanum silicate high-k dielectric. ECS Trans. 11(4), 607–612 (2007) 





Lee, S.H., Kim, S.B., Moon, Y.-J., Kim, S.M., Jung, H.J., Seo, M.S., Lee, K.M., Kim, S.-K., Lee, S.W.: High-responsivity deep-ultraviolet-selective photodetectors using ultrathin gallium oxide films. ACS Photonics 4(11), 2937–2943 (2017) 





Li, Y., Zhou, Z., Pan, H., Chen, J., Wang, Y., Qu, Q., Zhang, D., Li, M., Lu, Y., He, Y.: High-performance Ga2O3/FTO-based self-driven solar-blind UV photodetector with thickness-optimized graphene top electrode. J. Mater. Res. Technol. 22, 2174–2185 (2023) 





Liao, M.: Progress in semiconductor diamond photodetectors and MEMS sensors. Funct. Diam. 1(1), 29–46 (2022) 





Mandal, P., Roy, S., Singh, U.: Investigation on the optical and electrical performance of aluminium doped gallium oxide thin films. Opt. Quant. Electron. 54(8), 476 (2022). https://doi.org/10.1007/ s11082-022-03851-0 





Mao, L.-F.: Temperature dependence of the tunneling current in metal-oxide-semiconductor devices due to the coupling between the longitudinal and transverse components of the electron thermal energy. Appl. Phys. Lett. (2007). https://doi.org/10.1063/1.2735929 





Nakagomi, S., Momo, T., Takahashi, S., Kokubun, Y.: Deep ultraviolet photodiodes based on β-Ga2O3/ SiC heterojunction. Appl. Phys. Lett. (2013). https://doi.org/10.1063/1.4818620 





Patil-Chaudhari, D., Ombaba, M., Oh, J.Y., Mao, H., Montgomery, K.H., Lange, A., Mahajan, S., Woodall, J.M., Islam, M.S.: Solar blind photodetectors enabled by nanotextured β-Ga2O3 films grown via oxidation of GaAs substrates. IEEE Photonics J. 9(2), 1–7 (2017) 





Pearton, S., Ren, F., Tadjer, M., Kim, J.: Perspective: Ga2O3 for ultra-high power rectifiers and MOS-FETS. J. Appl. Phys. (2018). https://doi.org/10.1063/1.5062841 





Periyanagounder, D., Gnanasekar, P., Varadhan, P., He, J.-H., Kulandaivel, J.: High performance, selfpowered photodetectors based on a graphene/silicon Schottky junction diode. J. Mater. Chem. C 6(35), 9545–9551 (2018) 





Ping, L.K., Berhanuddin, D.D., Mondal, A.K., Menon, P.S., Mohamed, M.A.: Properties and perspectives of ultrawide bandgap Ga2O3 in optoelectronic applications. Chin. J. Phys. 73, 195–212 (2021) 





Qin, Y., Li, L.H., Yu, Z., Wu, F., Dong, D., Guo, W., Zhang, Z., Yuan, J.H., Xue, K.H., Miao, X.: Ultrahigh performance amorphous Ga2O3 photodetector arrays for solar-blind imaging. Adv. Sci. 8(20), 2101106 (2021). https://doi.org/10.1002/advs.202101106 





Raj, J.S.S., Sivaraman, P., Prem, P., Matheswaran, A.: Wide Band Gap semiconductor material for electric vehicle charger. Mater. Today: Proc. 45, 852–856 (2021) 





Rebien, M., Henrion, W., Hong, M., Mannaerts, J., Fleischer, M.: Optical properties of gallium oxide thin films. Appl. Phys. Lett. 81(2), 250–252 (2002) 





Sang, L., Liao, M., Sumiya, M.: A comprehensive review of semiconductor ultraviolet photodetectors: from thin film to one-dimensional nanostructures. Sensors 13(8). 10482–10518 (2013 





Sharma, S., Sumathi, A., Periasamy, C.: Photodetection properties of ZnO/Si heterojunction diode: A simulation study. IETE Tech. Rev. 34(1), 83–90 (2017) 





Shur, M.: Wide band gap semiconductor technology: State-of-the-art. Solid-State Electron. 155, 65–75 (2019) 





Singh Pratiyush, A., Krishnamoorthy, S., Vishnu Solanke, S., Xia, Z., Muralidharan, R., Rajan, S., Nath, D.N.: High responsivity in molecular beam epitaxy grown β-Ga2O3 metal semiconductor metal solar blind deep-UV photodetector. Appl. Phys. Lett. (2017). https://doi.org/10.1063/1.4984904 





Sze, S.M., Li, Y., Ng, K.K.: Physics of Semiconductor Devices. John Wiley & Sons, Hoboken, New Jersey (2021) 





Tang, X., Li, K.-H., Zhao, Y., Sui, Y., Liang, H., Liu, Z., Liao, C.-H., Babatain, W., Lin, R., Wang, C.: Quasi-epitaxial growth of β-Ga2O3-coated wide band gap semiconductor tape for flexible UV photodetectors. ACS Appl. Mater. Interfaces. 14(1), 1304–1314 (2021) 





Wang, Y., Wu, C., Guo, D., Li, P., Wang, S., Liu, A., Li, C., Wu, F., Tang, W.: All-oxide NiO/Ga2O3 p–n junction for self-powered UV photodetector. ACS Appl. Electron. Mater. 2(7), 2032–2038 (2020) 





Wei, T.-C., Tsai, D.-S., Ravadgar, P., Ke, J.-J., Tsai, M.-L., Lien, D.-H., Huang, C.-Y., Horng, R.-H., He, J.-H.: See-through Ga2O3 solar-blind photodetectors for use in harsh environments. IEEE J. Sel. Top. Quantum Electron. 20(6), 112–117 (2014) 





Wu, D., Zhao, Z., Lu, W., Rogée, L., Zeng, L., Lin, P., Shi, Z., Tian, Y., Li, X., Tsang, Y.H.: Highly sensitive solar-blind deep ultraviolet photodetector based on graphene/PtSe 2/β-Ga 2 O 3 2D/3D Schottky junction with ultrafast speed. Nano Res. 14, 1973–1979 (2021) 





Yadav, M.K., Mondal, A., Das, S., Sharma, S.K., Bag, A.: Impact of annealing temperature on band-align ment of PLD grown Ga2O3/Si (100) heterointerface. J. Alloys Compd. 819, 153052 (2020). https:// doi.org/10.1016/j.jallcom.2019.153052 





Young, S.-J., Ji, L.-W., Chang, S.-J., Liang, S., Lam, K.-T., Fang, T.-H., Chen, K.-J., Du, X., Xue, Q.-K.: ZnO-based MIS photodetectors. Sens. Actuators, A 141(1), 225–229 (2008) 





Zhang, M., Liu, Z., Yang, L., Yao, J., Chen, J., Zhang, J., Wei, W., Guo, Y., Tang, W.: β-Ga2O3-based power devices: a concise review. Crystals 12(3), 406 (2022). https://doi.org/10.3390/cryst12030406 





Zou, Y., Zhang, Y., Hu, Y., Gu, H.: Ultraviolet detectors based on wide bandgap semiconductor nanowire: a review. Sensors 18(7), 2072 (2018). https://doi.org/10.3390/s18072072 



Publisher’s Note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations. 

Springer Nature or its licensor (e.g. a society or other partner) holds exclusive rights to this article under a publishing agreement with the author(s) or other rightsholder(s); author self-archiving of the accepted manuscript version of this article is solely governed by the terms of such publishing agreement and applicable law. 