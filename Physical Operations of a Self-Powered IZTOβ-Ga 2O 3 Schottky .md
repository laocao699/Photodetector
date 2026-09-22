Article 

# Physical Operations of a Self-Powered IZTO/β-Ga<sub>2</sub>O<sub>3</sub> Schottky Barrier Diode Photodetector

Madani Labed <sup>1</sup> , Hojoong Kim <sup>2,3</sup>, Joon Hui Park <sup>2</sup>, Mohamed Labed <sup>4</sup>, Afak Meftah <sup>1</sup>, Nouredine Sengouga <sup>1</sup> and You Seung Rim <sup>2,</sup>* 

Laboratory of Semiconducting and Metallic Materials (LMSM), University of Biskra, Biskra 07000, Algeria; madani.labed@univ-biskra.dz (M.L.); af.meftah@univ-biskra.dz (A.M.); n.sengouga@univ-biskra.dz (N.S.) 

2 Department of Intelligent Mechatronics Engineering, and Convergence Engineering for Intelligent Drone Sejong University, Seoul 05006, Korea; hkim3023@gatech.edu (H.K.); julia980406@gmail.com (J.H.P.) 

3 George W. Woodruff School of Mechanical Engineering, Institute for Electronics and Nanotechnology, Georgia Institute of Technology, Atlanta, GA 30332, USA 

4 High Collage of Food Sciences and Food Industries, Algiers 16200, Algeria; labed@essaia.dz 

米 Correspondence: youseung@sejong.ac.kr 

![](images/37cfee8f207ac20934eaa428ed96dd042d29e006a6bc4746b07ea511e33f0b07.jpg)


Citation: Labed, M.; Kim, H.; Park, J.H.; Labed, M.; Meftah, A.; Sengouga, N.; Rim, Y.S. Physical Operations of a Self-Powered $\mathrm { I Z T O } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky Barrier Diode Photodetector. Nanomaterials 2022, 12, 1061. https://doi.org/ 10.3390/nano12071061 

Academic Editors: Qiongfeng Shi, Jianxiong Zhu and Uroš Cvelbar 

Received: 29 December 2021 Accepted: 21 March 2022 Published: 24 March 2022 

Publisher’s Note: MDPI stays neutral with regard to jurisdictional claims in published maps and institutional affiliations. 

![](images/bc0827b60800c73f19037c37425506934aba29214a0f899573b9c046e4a7855b.jpg)


Copyright: © 2022 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/). 

Abstract: In this work, a self-powered, solar-blind photodetector, based on InZnSnO (IZTO) as a Schottky contact, was deposited on the top of Si-doped $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ by the sputtering of two-faced targets with InSnO (ITO) as an ohmic contact. A detailed numerical simulation was performed by using the measured J–V characteristics of $\mathrm { I Z T O } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky barrier diodes (SBDs) in the dark. Good agreement between the simulation and the measurement was achieved by studying the effect of the IZTO workfunction, $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ interfacial layer (IL) electron affinity, and the concentrations of interfacial traps. The $\mathrm { I Z T O } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ (SBDs) was tested at a wavelength of 255 nm with the photo power density of 1 $. \mathrm { m } \mathrm { W } / \mathrm { c m } ^ { 2 }$ . A high photo-to-dark current ratio of $3 . 7 0 \times 1 0 ^ { 5 }$ and a photoresponsivity of 0.64 mA/W were obtained at 0 V as self-powered operation. Finally, with increasing power density the photocurrent increased, and a 17.80 mA/W responsivity under 10 mW $\mathrm { \ddot { / c m } } ^ { 2 }$ was obtained. 

Keywords: $\mathrm { I Z T O } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky diode; solar-blind; self-powered; photodetector; modeling 

## 1. Introduction

Gallium oxide $\left( \operatorname { G a } _ { 2 } \operatorname { O } _ { 3 } \right)$ is an oxide semiconductor material with a long, rich history [1–3]. It has an ultra-wide bandgap (UWBG) of ${ \sim } 4 . 8 \ \mathrm { e V } , \ i$ a high breakdown electric field of ~8 MV/cm, and a high saturation velocity of $1 \times 1 0 ^ { 7 } \mathrm { c m / s } ,$ and these properties have brought ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ to the fore once again $[ 1 , 2 , 4 ] . \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } $ has six polymorphs, ${ \mathrm { i . e . , } } \alpha , \ \beta , \ \gamma , \ \delta , \ \varepsilon ,$ and k, with $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ being the most stable [1]. Unipolar devices based on $\mathrm { \mathsf { beta - G a } } _ { 2 } \mathrm { O } _ { 3 } ,$ such as the metal–oxide–semiconductor field-effect transistor (MOSFET) [5], thin film transistor (TFT) [6], field emission (FE) [7], and Schottky barrier diode (SBD) $[ 1 - 4 , 8 , 9 ]$ , have been studied extensively. It is also used for deep ultraviolet (DUV) photodetectors (PDs) for solar blind applications [10,11]. DUV PDs work in the solar-blind spectrum with wavelengths shorter than 280 nm, which means that they can be applied to optical communication, chem ical analysis, missile tracking, and harsh environmental monitoring [12]. Different types of solar-blind PD structures based on $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } \mathrm { O } _ { 3 }$ , such as metal–semiconductor–metal [13], heterojunction [14], and Schottky [15], have been reported. The Schottky barrier diode solar-blind has some advantages, including low dark current and low cost in comparison with heterojunctions [11,16]. Self-powered solar-blind PDs are of special interest, because they can work in the absence of an external power supply. A strong built-in electric field ensures that this high-performance, self-powered, solar-blind Schottky barrier diode pho todetector can operate at zero bias voltage [14]. Different metals have been used as the Schottky contacts of $\mathrm { \beta _ { - G a _ { 2 } O _ { 3 } , \ e . g . , A u , \bar { \ T i } , N i , P t , C u , } }$ and Pb [17]. For example, Chen et al. [18] reported a self-powered photodetector based on a $\mathsf { A u } / \beta \mathsf { - G a } _ { 2 } \mathrm { O } _ { 3 }$ nanowire array film Schottky, in which the responsivity reached 0.01 (mA/W) during 254 nm light illumination with $2 { \mathrm { m } } W / { \mathrm { c m } } ^ { 2 }$ at a bias of 0 V. Zhi et al. [19] studied the $\mathsf { A u } / \beta \mathsf { - G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky solar-blind photodetector, and they achieved a responsivity of 0.4 (mA/W) for 0 V bias and 254 nm illumination. Peng et al. [10] reported a $\mathrm { P t } / \beta \mathrm { - } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky barrier diode solar-blind photodetector with nearly a $1 0 ^ { 4 }$ of light to dark current ratio at 0 V bias and a wavelength of 254 nm. Liu et al. [20] studied a $\mathrm { N i } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky barrier diode solar-blind photodetector tested under 254 nm light, and they obtained responsivities of about 806.02 (A/W) and 1372.92 (A/W) under −5 V and 5 V, respectively. In the publications mentioned above, various metals were used, such as Pt, Ni, and $\mathrm { \ A u }$ , for Schottky contact formation with $\mathsf { { \beta { - } } } \mathsf { { G a } } _ { 2 } \mathrm { { O } } _ { 3 }$ . In addition, transparent materials and oxides are used for the formation of the Schottky contact with $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } \mathrm { O } _ { 3 }$ . However, these types of materials formed a low Schottky barrier height with $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } \mathrm { O } _ { 3 }$ . For example, Zhuo et al. [14] reported a $\mathrm { M o S } _ { 2 } / \beta \mathrm { - } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ heterojunction self-powered photodetector with a 670 ratio of light current to dark current at $0 \mathrm { V } ,$ and this result was achieved because of the very low value of the Schottky barrier. Chen et al. [17] studied a self-powered MXenes/β ${ \bf - G a } _ { 2 } { \bf O } _ { 3 }$ photodetector under 254 nm wavelength with a light illumination of 115.1 $\mu \mathrm { W } . \mathrm { c m } ^ { - 2 }$ and $\bar { \mathsf { a } } 1 . 6 \times 1 0 ^ { 4 }$ ratio of light current to dark current at 0 V and an extracted Schottky barrier height of about $0 . 9 \mathrm { e V } .$ Then, Cui et al. [21] published a flexible solar-blind amorphous $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ photodetector with an indium tin oxide (ITO) transparent conducting electrode, with a photocurrent that is less effected at 0 V and under 254 nm when it is exposed to an oxygen flux of 0.14 SCCM; this result was related to the low Schottky barrier height of about $0 . 9 7 \mathrm { e V . }$ In addition, Kim et al. [11] used InZnSnO (IZTO) for Schottky contact formation with $\mathsf { \beta - G a } _ { 2 } \mathrm { O } _ { 3 } ,$ , and a Schottky barrier height greater than 1.06 eV was obtained; these results indicate that this photodetector can work in the absence of an external power supply. 

Here, we constructed simulation–experiment combination of ITZO/ ${ \bf \beta } { \bf \mathrm { - } } { \bf G a } _ { 2 } { \bf O } _ { 3 }$ SBDbased UV photodiodes under the illumination to reveal the physics behind the behavior of the J–V characteristics in terms of workfunction, IL electron affinity and interfacial traps. The different conduction mechanisms we performed were taken into consideration either collectively or individually. Their parameters were scanned over a physically acceptable range so that an acceptable comparison of measurement to simulation was achieved. Good agreement between simulation and experiment was observed clearly with the consideration of the effect of different IZTO workfunctions, $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ interfacial layer electron affinity, and the effect of interfacial traps. Additionally, the $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ self-powered solar-blind PDs were tested and compared with measurements at the photo power density of 1 $\mathrm { m } \mathrm { W } / \mathrm { c m } ^ { 2 }$ and the wavelength of 255 nm. 

## 2. Experiment

The Solar-blind Schottky photodetector was fabricated on a 650 µm, Sn-doped, bulk $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } \mathrm { O } _ { 3 }$ single-crystal wafer $\mathrm { \hat { ( ( N _ { d } { - } N _ { a } ) } } = 1 \times 1 0 ^ { 1 8 } \mathrm { c m } ^ { - 3 }$ , Novel Crystal Technology, Inc., Saitama, Japan) with (001) surface orientation. The epitaxial layer of Si-doped $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ (10 µm thick, $1 \times 1 0 ^ { 1 8 } \mathrm { c m } ^ { - 3 } )$ ) was grown by halide vapor phase epitaxy (HVPE). Si-doped β- ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ was used as the active layer in this solar-blind Schottky photodetector, as it provides a high purity and a low resistance [2]. The ITO electrode was deposited by sputtering on the bottom of Sn-doped $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ as an ohmic contact. IZTO was deposited on the top of the Si-doped $\mathsf { { \beta { - } } } \mathsf { { G a } } _ { 2 } \mathrm { { O } } _ { 3 }$ as a Schottky contact by two-faced target co-sputtering with ITO $( \mathrm { I n } _ { 2 } \mathrm { O } _ { 3 } { : } \mathrm { S n O } = 9 { : } 1 )$ and IZO $( \mathrm { I n } _ { 2 } \mathrm { O } _ { 3 } { : } Z \mathrm { n O } = 9 { : } 1 )$ ) at room temperature. Figure 1 shows a schematic representation of this SBD structure. After the deposition of the layers, the device was annealed at $6 0 0 ^ { \circ } \mathrm { C }$ in Ar for 1 min using rapid thermal annealing. The electrical J–V in dark and light was measured using a semiconductor analyzer and a source meter (SCS-4200A and 2410 Source meter, Keithley, Beaverton, OR, USA). Further details can be found in our previous publication [11]. 

![](images/74211da7ba77273981059caaa50ca9915b76b9dbc8d29d1f10625822a23e1ddd.jpg)



Figure 1. A schematic representation of the $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ Schottky barrier diode (SBD) structure.


## 3. Simulation Methodology

For the simulation, we considered thermionic emission, Shockley–Read–Hall, Auger recombination, and image force lowering models. The physical parameters of different layers and related traps are presented in Tables 1 and 2, respectively. 

SILVACO TCAD (Version 5.24.1.R, Silvaco Inc.: Santa Clara, CA, USA) was used to model the above structure. It solves the basic drift–diffusion semiconductor Poisson and continuity equations, which are [2,3,22]: 


Table 1. Properties of each layer of the studied SBD [2,3,23].


<table><tr><td>Parameters</td><td>Sn: <eq>\beta-Ga_{2}O_{3}</eq></td><td>Si: <eq>\beta-Ga_{2}O_{3}</eq></td></tr><tr><td>Bandgap (eV)</td><td>4.8</td><td>4.8</td></tr><tr><td>Affinity (eV)</td><td>4</td><td>4</td></tr><tr><td>Hole mobility (<eq>cm^{2}V^{-1}s^{-1}</eq>)</td><td>10</td><td>10</td></tr><tr><td>Electron mobility (<eq>cm^{2}V^{-1}s^{-1}</eq>)</td><td>172</td><td>300</td></tr><tr><td><eq>m_{e}^{*}/m_{0}</eq></td><td>0.28</td><td>0.28</td></tr><tr><td><eq>m_{h}^{*}/m_{0}</eq></td><td>0.35</td><td>0.35</td></tr><tr><td>Relative permittivity</td><td>12.6</td><td>11</td></tr><tr><td><eq>N_{c}</eq> (<eq>cm^{-3}</eq>)</td><td><eq>3.7 \times 10^{18}</eq></td><td><eq>3.7 \times 10^{18}</eq></td></tr><tr><td><eq>N_{v}</eq> (<eq>cm^{-3}</eq>)</td><td><eq>5 \times 10^{18}</eq></td><td><eq>5 \times 10^{18}</eq></td></tr><tr><td><eq>N_{d}</eq> (<eq>cm^{-3}</eq>)</td><td><eq>1 \times 10^{18}</eq></td><td><eq>3 \times 10^{16}</eq></td></tr><tr><td>Minority carrier diffusion length (nm)</td><td>450</td><td>450</td></tr><tr><td>Saturation velocity (<eq>cm s^{-1}</eq>)</td><td><eq>10^{7}</eq></td><td><eq>10^{7}</eq></td></tr></table>


Table 2. Characteristics of the Sn-doped and Si-doped $\mathsf { { \beta { - } } } G \mathsf { a } _ { 2 } \mathrm { { O } } _ { 3 }$ traps considered in this work [1–3,24].


<table><tr><td>Traps</td><td>Trap Level (Ec-E) (eV)</td><td>Concentration (cm-3)</td><td>Capture Cross Section σn (cm2)</td><td>σn/σp</td></tr><tr><td rowspan="3">Sn-doped β-Ga2O3Bulk layer</td><td>0.55</td><td>3 × 1013</td><td>2 × 10-14</td><td>100</td></tr><tr><td>0.74</td><td>2 × 1016</td><td>2 × 10-14</td><td>100</td></tr><tr><td>1.04</td><td>4 × 1016</td><td>2 × 10-14</td><td>10</td></tr><tr><td rowspan="4">Si-doped β-Ga2O3thin layer</td><td>0.60</td><td>3.6 × 1013</td><td>2 × 10-14</td><td>100</td></tr><tr><td>0.75</td><td>4.6 × 1013</td><td>2 × 10-14</td><td>100</td></tr><tr><td>0.72</td><td>4.6 × 1013</td><td>2 × 10-14</td><td>100</td></tr><tr><td>1.05</td><td>1.1 × 1014</td><td>2 × 10-14</td><td>10</td></tr></table>

Poisson equation is given by [2,3,22]: 

$$
d i v (\varepsilon \nabla \psi) = - q (p - n + N _ {d} \pm N _ {t} ^ {\pm})\tag{1}
$$

where $\psi$ is the electrostatic potential, ε is the permittivity, p and n are the concentrations of the free holes and electrons, respectively, and $N _ { t } ^ { \pm }$ is the density of the ionized traps $( \mathrm { c m } ^ { - 3 } )$ 

The continuity equations for electrons and holes as defined in steady states are given by $[ 2 , 3 , 2 2 ]$ : 

$$
0 = \frac {1}{q} d i v \vec {J _ {n}} + G _ {n} - R _ {n}\tag{2}
$$

$$
0 = - \frac {1}{q} d i v \vec {J _ {p}} + G _ {p} - R _ {p}\tag{3}
$$

where $G _ { n }$ and $G _ { p }$ are the generation rates for electrons and holes, respectively, and $R _ { n }$ and $R _ { p }$ are the recombination rates for electrons and holes, respectively. ${ \vec { J } } _ { n }$ and $\vec { J } _ { p }$ are the electron density and the hole current density, respectively, which are given in terms of the free electron and hole density (n and $p )$ , electric field (E) and mobility $( \mu _ { n }$ and $\mu _ { p } )$ [25]: 

$$
\vec {J} _ {n} = q \mu_ {n} n E + \mu_ {n} K _ {B} T \nabla n\tag{4}
$$

$$
\vec {J} _ {p} = q \mu_ {p} p E - \mu_ {p} K _ {B} T \nabla p\tag{5}
$$

Traps are represented by their ionized density, $N _ { t } ^ { \pm }$ . The sign ± depends on whether the trap is an acceptor or a donor, so that $N _ { t } ^ { + } ~ = ~ f \dot { N } _ { t }$ and $N _ { t } ^ { - } ~ = ~ ( 1 - f ) N _ { t } , f$ is the occupancy function given by $\begin{array} { r } { f = \frac { \sigma _ { n } n + \sigma _ { p } p } { \sigma _ { n } ( n + n _ { t } ) + \sigma _ { p } ( p + p _ { t } ) } , } \end{array}$ and $\sigma _ { n ( p ) }$ is the trap capture crosssection for electrons (holes). The recombination rate is related to traps through the well known SRH formula, i.e., $\begin{array} { r } { R _ { n , p } = \frac { p n - n _ { i } ^ { 2 } } { \tau _ { 0 n } ( p + p _ { t } ) + \tau _ { 0 p } ( n + n _ { t } ) } , } \end{array}$ where $n _ { t } = n _ { i } e x p { \big ( } { - } ( E _ { i } - E _ { t } { \big ) } / k T { \big ) }$ and $p _ { t } = n _ { i } e x p \bigl ( - \bigl ( E _ { t } - E _ { i } \bigr ) / k T \bigr ) .$ , and $\tau _ { 0 n }$ and $\tau _ { 0 p }$ are the minority carrier lifetimes which are also related to the traps through $\begin{array} { r } { \tau _ { 0 n ( p ) } = \frac { 1 } { v _ { t h n ( p ) } \sigma _ { n ( p ) } N _ { t } } } \end{array}$ , where $v _ { t h n ( p ) }$ is the thermal velocity of electrons (holes). 

According to several publications [11,26,27], ITO forms an Ohmic contact with $\beta -$ ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ . In this simulation, an ideal ohmic contact was considered for $\mathrm { I T O } / \beta – \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ interface. A low $\mathrm { I T O } / \beta – \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ barrier was achieved when highly doped $\mathsf { { \beta { - } } } \mathsf { { G a } } _ { 2 } \mathrm { { O } } _ { 3 }$ substrate was used. 

## 4. Results and Discussion

## 4.1. Optical and Electrical Properties of IZTO Thin Film

The obtained resistivity, carrier concentration, workfunction, and mobility of IZTO were $4 . 8 6 \times 1 0 ^ { - 4 }$ Ω cm, $2 . 8 0 \dot { \times } 1 0 ^ { 2 0 } \mathrm { c m } ^ { - 3 }$ , 4.79 eV, and 10.83 cm<sup>2</sup>/V s, respectively. Figure 2a shows the optical transmission $( T ( \lambda ) )$ ) of IZTO thin film as a function of the wavelength in the 250–1200 nm range. The average transmittance of the IZTO films in the visible wavelength range was over $8 7 \%$ 

![](images/e410cf86e456cf4e0e3e5653649f7996228ae7d51df472d88e95684cce25b987.jpg)


![](images/e999f8784c9e5285126d313eee1b6a35ffbb296fb614ac3b4bdba3bd23cc5eef.jpg)



Figure 2. (a) The transmittance of IZTO thin film; (b) $( \alpha \left( \lambda \right) . h v ) ^ { 2 }$ of the IZTO thin film.


For direct bandgap semiconductors, the absorption can be obtained from the following Equation [15]: 

$$
(\alpha h \nu) ^ {2} = C \cdot (h \nu - E _ {g})\tag{6}
$$

where α is the absorption coefficient, C is a constant, h is Planck’s constant, and ν is the frequency of the incident light. By plotting $( \alpha ( \lambda ) { \cdot } h v ) ^ { 2 }$ versus hυ, the optical bandgap of the IZTO thin film was determined to be 3.5 eV, as shown in Figure 2b. This value agrees with the published value [28]. The refractive index has a significant importance in the design of optical devices. It reflects the crystallinity and optical quality of thin films. The extinction coefficient (k) and the refractive index (n) of IZTO thin film are calculated by [29]: 

$$
k (\lambda) = \frac {\alpha . \lambda}{4 \pi}\tag{7}
$$

$$
n (\lambda) = \frac {(1 - R (\lambda))}{(1 + R (\lambda))} + \sqrt {\frac {4 R (\lambda)}{1 - R (\lambda) ^ {2}} - k (\lambda) ^ {2}}\tag{8}
$$

where $R ( \lambda )$ is the reflectance of the thin film, which can be calculated by the following Equation [30]: 

$$
R (\lambda) = 1 - \sqrt {T (\lambda)} e ^ {\frac {\alpha . t}{2}}\tag{9}
$$

where t is the IZTO thin film thickness, which is evaluated by ellipsometry at ≈300 nm. The extracted refractive index (n) and the extinction coefficient (k) are presented in Figure 3. 

As mentioned above, the photodetector consisted of 300 nm IZTO deposited on the top of Si-doped $\mathsf { { \beta { - } } } \mathsf { { G a } } _ { 2 } \mathsf { { O } } _ { 3 } ,$ and the ITO layer was considered as an ohmic contact on the bottom of the Sn-doped $\beta { \mathrm { - } } G { \mathsf { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ (Figure 1). Before simulating the proposed photodetector, the measurement of the dark output current density of SBD was reproduced, and details are provided in the next section. 

![](images/309bc25907d21a86e863714bb3db41b8be13d035ba26ba8de89b896118d594b7.jpg)



Figure 3. The extracted refractive index (n) and the extinction coefficient (k) of IZTO thin film.


## 4.2. Modeling the Dark Current of IZTO/β- ${ \cdot } G a _ { 2 } O _ { 3 }$ SBD

As presented in Figure 4, when the tunneling transport mechanism was not considered, the shape of the $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ SBD current is parallel to the measurement current; this indicates that the thermionic transport mechanism dominates in the forward bias. However, when the properties presented in Table 1 and the traps presented in Table 2 were considered, a huge disagreement was obtained between the simulation and the measurement. This disagreement is related to the IZTO workfunction, i.e., the $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ IL electron affinity (conduction band minimum), in addition to the effect of the surface traps between IZTO and the $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } \mathrm { O } _ { 3 }$ drift layer. 

![](images/771d04e664600113fb23501fd64ed9714f6d08ed2735bc219accabe640006513.jpg)



Figure 4. $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ SBD forward current density with and without the tunneling model compared to measurement.


## 4.3. Effect of IL Electron Affinity

Next, an IL (10 nm thickness) between Si-doped $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ and IZTO was considered for modeling the effect $\scriptstyle { \mathrm { I Z T O } } / \beta \ – \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ conduction band offset on the SBD performance. The effects of the IL electron affinity on the SBD J–V characteristics were studied, and these effects are shown in Figure 5. Experimentally, the IL electron affinity is related to the chemical composition of the surface [2] and surface polarization [31] as well as external effects, such as argon (Ar) bombardment, plasma, etc. The current density decreases with decreasing IL electron affinity of Si-doped $\beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } , \mathrm { i } . \mathrm { e } . .$ , from 4 to 3.5 e V [32], but the IL electron affinity has a more pronounced effect in the high voltage domain. This is due to the increase in the height of the Schottky barrier (φ ) with decreasing IL electron affinity according to the Schottky–Mott rule and the increase in the series resistance [2]. As presented in Figure 6, with decreasing IL electron affinity, the barrier between IZTO and $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } \mathrm { O } _ { 3 }$ increases. An agreement between measurement and simulation occurs for voltages higher than 1 V for a 3.556 eV IL electron affinity. However, a disagreement between simulation and measurement was noticed in the low-voltage domain, and this is related to the effect of the IZTO workfunction and the concentrations of the interfacial traps, which are addressed in the next two subsections. 

![](images/78f949d263fe815c35328c89c2e6b68a6e6e6501725037f55aaaea69521ddb94.jpg)



Figure 5. Effect of the IL electron affinity on the simulated J–V characteristics compared to measurement.


![](images/86838ffb3ca41d0aae93a19179dd7c3677b4c8ab5af02e0d398bef51b9545c2c.jpg)



Figure 6. Equilibrium band diagram variation with the IL electron affinity.


## 4.4. Effect of the IZTO Workfunction

In addition to the IL electron affinity, the IZTO workfunction will have an effect. As shown in Figure $^ { 7 , }$ when the IZTO workfunction decreases from 5 to 4.5 eV [33,34] the current density increases. This increase in the current density is related to the decrease in $\phi _ { B }$ as presented in Figure 8; the formed barrier between IZTO and Si-doped $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ increased. The best agreement between simulation and measurement was achieved for $\phi _ { I Z T O } = 4 . 6 \ : \mathrm { e V }$ . The small deviation from measurement, i.e., in the range of 0.4–0.8 V, was due to the parameters of the traps that are considered (Table 2), which may not be accurate. It also may be related to the effect of the different compositions of the materials (In, Zn, and Sn) [35]. 

![](images/2ffe19fa2e91c9bc7d706eef6b0af80aae7f479def24fbcf38807e418370b4f6.jpg)



Figure 7. Simulated J–V characteristics for different IZTO workfunctions compared to measurements.


![](images/458ee06c1eed0b62dbeba6f31ffeb3cc023a2f1d62ed8253678c7ea121f6cd22.jpg)



Figure 8. Equilibrium band diagram variation with the IZTO workfunction.


## 4.5. Effect of the Concentration of Traps at the IL

We studied the effect of the concentration of the $( \mathrm { E } _ { \mathrm { c } } - 1 . 0 5 )$ traps at IL on the characteristics of the SBD J–V. The traps that we considered were the most affected, especially given that the surface of the ${ \beta } { - } \bar { \mathrm { { G a } } _ { 2 } \mathrm { { O } } _ { 3 } }$ is exposed to plasma and $\mathrm { A r }$ bombardment [2]. For the four traps, these effects are shown in Figure 9a–d, respectively. First, all of the defects that were considered have a significant effect on the current density of the SBD. Among the defect concentrations that were considered, those that gave the best comparison with the measurements were $3 . 6 \times 1 0 ^ { 1 6 } , 4 . 6 \times 1 0 ^ { 1 6 } , 4 . 6 \times 1 0 ^ { 1 6 }$ and $1 . 1 \times 1 0 ^ { 1 5 } \mathrm { c m } ^ { - 3 } .$ , respectively. The dark current was affected at high trap densities, and this result was related to electrons being captured by the traps. Figure 10 shows the effect of traps on the equilibrium band diagram. When traps were considered with the concentration mentioned above, the dif ference of conduction band and Fermi level $( \mathrm { E _ { c } - E _ { f } } )$ increased, and this meant a decrease in the free electron density. A good comparison between simulation and measurement is obtained as presented in Figure 11 and the extracted SBD parameters are presented in Table 3. The Schottky barrier height $\left( \phi _ { B } \right)$ and the $\mathrm { R } _ { \mathrm { s } }$ were extracted using the Sato and Yasumura method [3,36]. A high $\phi _ { B }$ was obtained with a low ideality factor close to unity in addition to the low densities of the interfacial traps, as expected in our previous publication [11]. In addition, a very low saturation current was obtained. 

![](images/4676c832d7efc1d6442af7e72f44afd77c6440269bb789b89532469f4524cf14.jpg)


![](images/3d23ebad1d59fed50f52c8d0077a4bf27a5e20a08bb29bde8e8ba8c8d5a2657e.jpg)


![](images/d258c767a8099bec710fd5cc50e357d33de2ed30cf1286bad4a9dcf42ae72357.jpg)


![](images/b5a89d43b6c61244a25d16ab4c07c1521d8bd0327e9849b6145e4fdd8b64d799.jpg)



Figure 9. Effects of the density of the traps on ${ \mathrm { S B D } } , { \mathrm { i } } . { \mathrm { e } } .$ , the (a) $E _ { c } - 0 . 6 \ \mathrm { e V } ,$ (b) $E _ { c } - 0 . 7 5 \mathrm { e V } ,$ (c) $E _ { c } - 0 . 7 2 \mathrm { e V } ,$ and (d) $E _ { c } - 1 . 0 5 \mathrm { e V }$ traps.


![](images/ba1f6ec48c72834fee641230a14721da0d28425ecfd73fed4e93775c62ef4ffb.jpg)



Figure 10. Equilibrium band diagram variation with and without traps.


![](images/16e7e48fa44319d8284c1cb7380238bfcac4b37529d9415af9a38be3d4c3ab4e.jpg)



Figure 11. The best comparison between the simulation and the experimental results.



Table 3. Output parameters from simulation and measurement.


<table><tr><td>Parameter</td><td>n</td><td><eq>\phi_B</eq> (eV)</td><td><eq>R_s</eq> (<eq>\Omega</eq> cm<eq>^2</eq>)</td><td><eq>R_{on}</eq> (<eq>\Omega</eq> cm<eq>^2</eq>)</td><td><eq>J_s</eq> (A/cm<eq>^2</eq>)</td></tr><tr><td>Simulation</td><td>1.02</td><td>1.25</td><td>1.78</td><td>1.01</td><td><eq>1.72 \times 10^{-12}</eq></td></tr><tr><td>Measurement</td><td>1.03</td><td>1.29</td><td>1.91</td><td>1.04</td><td><eq>1.11 \times 10^{-11}</eq></td></tr></table>

## 4.6. The Effect of 255 nm Wavelength Illumination on Forward Current

The simulated SBD J–V characteristics were successfully compared to measurements made at room temperature. This good agreement was achieved by modeling the effect of IL electron affinity, IZTO workfunction, and the concentrations of the IL traps. As shown in Table $^ { 3 , }$ a low dark saturation current was obtained, so this SBD is proposed as a high-performance solar-blind PD. The $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ SBD was illuminated at 255 nm with a light intensity of $1 \mathrm { m } \mathrm { W } / \mathrm { c m } ^ { 2 }$ . To evaluate the performance of the $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ solar-blind SBD under 255 nm, the forward photocurrent was extracted with the consideration of the previous IZTO work function, the IL electron affinity, and the concentrations of the interfacial traps. As presented in Figure 12, good agreement was demonstrated between the simulation results and the actual measurements. The solar-blind SBD exhibited a high rectifying characteristic after illumination at 255 nm in forward voltage $\left( J _ { P h o t o n } / \stackrel { \smile } { J _ { d a r k } } = 3 . 7 \stackrel { \cdot } { 0 } \times \stackrel { \triangledown } { 1 } 0 ^ { 5 } \right)$ under 0 V. The responsivity reached 0.64 (mA/W). The responsivity was estimated as follows [37]: 

$$
R _ {\lambda} = \frac {J _ {P h o t o n} - J _ {d a r k}}{P}\tag{10}
$$

where $J _ { P h o t o n } , J _ { d a r k } ,$ and P are the photocurrent at a given voltage, the dark current, and the power density, respectively. With zero bias voltage, the photodetector had good responsivity under 255 nm light illumination with intensity of 1 $\bar { ( } \mathrm { m } \mathrm { W } / \mathrm { c m } ^ { 2 } )$ . In addition, a decrease in $\phi _ { B }$ from 1.25 eV in dark to 1.18 after illumination was observed. 

![](images/a87f078f96aabe7f2ca8f7a5fcdd655580db29a5c0af9754da51226f820e2356.jpg)



Figure 12. Comparison between simulation and measurement (under incident light power density of $1 \mathrm { m } \mathrm { W } / \mathrm { c m } ^ { 2 } )$ of J–V characteristics of $\mathrm { I Z T O } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ at 255 nm wavelength.


In this solar-blind PD, the built-in electric field in the depletion region of the $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } \mathrm { O } _ { 3 }$ and IZTO interface was enough to separate the photogenerated electron–hole pairs toward corresponding electrodes. In this structure, a high built-in potential is related to the high $\phi _ { B }$ . In addition, the effect of light power density on simulated J–V characteristics was studied. As presented in Figure 13, with increasing power density, the photocurrent increased, and a responsivity of 17.80 mA/W under 10 $\mathrm { m } \mathrm { W } / \mathrm { c m } ^ { 2 }$ was achieved. This increase in photocurrent is related to the increase in photo-excited, separated, and collected carriers [38]. This result agrees with the result obtained by Wu et al. [39]. 

![](images/578f3a38bdbab0a072cae543b03793340066363c147529a746d83c295eaa0a1a.jpg)



Figure 13. Effect of light power density on the simulated J–V characteristics. The inset is the variation of photocurrent with light power density at 0 V.


## 5. Conclusions

The J–V characteristics of an $\mathrm { I Z T O } / \beta { \mathrm { - } } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky barrier diode was simulated by SILVACO-Atlas and compared with measurements. The effects of the IZTO workfunction and the interfacial layer electron affinity and trap concentrations were studied for further agreement with measurements made in the dark. Then, we demonstrated the $\mathrm { I Z T O } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ self-powered Schottky photodetector with a high photo-to-dark ratio and responsivity of $3 . 7 0 \times 1 0 ^ { 5 }$ and 0.64 (mA/W) under 255 nm illumination with 1 mW $/ \mathrm { c m } ^ { 2 }$ for 0 V, respectively. Finally, with increasing power density, the photocurrent increased, and a 17.80 mA/W responsivity under 10 $\mathrm { m } \mathrm { \breve { W } / c m } ^ { 2 }$ was obtained. 

Author Contributions: Software, writing—original draft preparation, M.L. (Madani Labed); concep tualization, visualization, H.K.; visualization, J.H.P.; visualization, M.L. (Mohamed Labed); method ology A.M.; writing—review and editing N.S.; writing—review and editing Y.S.R. All authors have read and agreed to the published version of the manuscript. 

Funding: This paper was supported by the Korea Institute for Advancement of Technology (KIAT) grant funded by the Ministry of Trade, Industry & Energy (MOTIE, Korea). (P0012451, The Competency Development Program for Industry Specialist) and was also supported by the Technology Innovation Program—(20016102, Development of 1.2 kV Gallium oxide power semiconductor devices technology) funded by MOTIE, Korea. 

Institutional Review Board Statement: Not applicable. 

Informed Consent Statement: Not applicable. 

Data Availability Statement: Data presented in this article is available on request from the corre sponding author. 

Acknowledgments: Madani Labed and Hojoong Kim contributed equally to this work. 

Conflicts of Interest: The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

## References



1. Galazka, $Z . \ \beta \mathrm { - } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ for wide-bandgap electronics and optoelectronics. Semicond. Sci. Technol. 2018, 33, 113001. [CrossRef] 





2. Labed, M.; Sengouga, N.; Labed, M.; Meftah, A.; Kyoung, S.; Kim, H.; Rim, Y.S. Modeling a $\mathrm { N i } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky barrier diode deposited by confined magnetic-field-based sputtering. J. Phys. D Appl. Phys. 2021, 54, 115102. [CrossRef] 





3. Labed, M.; Sengouga, N.; Labed, M.; Meftah, A.; Kyoung, S.; Kim, H.; Rim, Y.S. Modeling and analyzing temperature-dependent parameters of $\mathrm { N i } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky barrier diode deposited by confined magnetic field-based sputtering. Semicond. Sci. Technol. 2021, 36, 35020. [CrossRef] 





4. Labed, M.; Sengouga, N.; Meftah, A.; Labed, M.; Kyoung, S.; Kim, H.; Rim, Y.S. Leakage Current Modelling and Optimization of $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ Schottky Barrier Diode with Ni Contact under High Reverse Voltage. ECS J. Solid State Sci. Technol. 2020, 9, 125001. [CrossRef] 





5. Pearton, S.J.; Ren, F.; Tadjer, M.; Kim, J. Perspective: ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ for ultra-high power rectifiers and MOSFETS. J. Appl. Phys. 2018, 124, 220901. [CrossRef] 





6. Thomas, S.R.; Adamopoulos, G.; Lin, Y.-H.; Faber, H.; Sygellou, L.; Stratakis, E.; Pliatsikas, N.; Patsalas, P.A.; Anthopoulos, T.D. High electron mobility thin-film transistors based on ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ grown by atmospheric ultrasonic spray pyrolysis at low temperatures. Appl. Phys. Lett. 2014, 105, 092105. [CrossRef] 





7. Grillo, A.; Barrat, J.; Galazka, Z.; Passacantando, M.; Giubileo, F.; Iemmo, L.; Luongo, G.; Urban, F.; Dubourdieu, C.; Di Bartolomeo, A. High field-emission current density from $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ nanopillars. Appl. Phys. Lett. 2019, 114, 193101. [CrossRef] 





8. Jian, ${ \mathrm { G . ; H e , Q . ; } }$ Mu, W.; Fu, B.; Dong, H.; Qin, Y.; Zhang, Y.; Xue, H.; Long, S.; Jia, Z.; et al. Characterization of the inhomogeneous barrier distribution in a $\mathrm { P t } / ( 1 0 0 ) \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky diode via its temperature-dependent electrical properties. AIP Adv. 2018, 8, 015316. [CrossRef] 





9. Labed, M.; Park, J.H.; Meftah, A.; Sengouga, N.; Hong, J.Y.; Jung, Y.-K.; Rim, Y.S. Low Temperature Modeling of $\mathrm { N i } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky Barrier Diode Interface. ACS Appl. Electron. Mater. 2021, 3, 3667–3673. [CrossRef] 





10. Peng, B.; Yuan, L.; Zhang, H.; Cheng, H.; Zhang, S.; Zhang, Y.; Zhang, Y.; Jia, R. Fast-response self-powered solar-blind photodetector based on $\mathrm { P t } / \beta \mathrm { - } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky barrier diodes. Optik 2021, 245, 167715. [CrossRef] 





11. Kim, H.; Seok, H.-J.; Park, J.H.; Chung, K.-B.; Kyoung, S.; Kim, H.-K.; Rim, Y.S. Fully Transparent InZnSnO/β-Ga O /InSnO Solar-Blind Photodetectors with High Schottky Barrier Height and Low-Defect Interfaces. J. Alloys Compd. 2021, 890, 161931. [CrossRef] 





12. Guo, D.; Liu, H.; Li, P.; Wu, Z.; Wang, S.; Cui, C.; Li, C.; Tang, W. Zero-Power-Consumption Solar-Blind Photodetector Based on $\beta – \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 } / \mathrm { N S T O }$ Heterojunction. ACS Appl. Mater. Interfaces 2017, 9, 1619–1628. [CrossRef] [PubMed] 





13. Qin, Y.; Li, L.; Zhao, X.; Tompa, G.S.; Dong, H.; Jian, G.; He, Q.; Tan, P.; Hou, X.; Zhang, Z.; et al. Metal–Semiconductor–Metal $\varepsilon { - } G a _ { 2 } \mathrm { O } _ { 3 }$ Solar-Blind Photodetectors with a Record-High Responsivity Rejection Ratio and Their Gain Mechanism. ACS Photonics 2020, 7, 812–820. [CrossRef] 





14. Zhuo, R.; Wu, D.; Wang, Y.; Wu, E.; Jia, C.; Shi, Z.; Xu, T.; Tian, Y.; Li, X. A self-powered solar-blind photodetector based on a MoS /β-Ga O heterojunction. J. Mater. Chem. C 2018, 6, 10982–10986. [CrossRef] 





15. Liu, Z.; Wang, X.; Liu, Y.; Guo, D.; Li, S.; Yan, Z.; Tan, C.-K.; Li, W.; Li, P.; Tang, W. A high-performance ultraviolet solar-blind photodetector based on a $\mathsf { { \beta { - } } } \mathsf { { G a } } _ { 2 } \mathrm { { O } } _ { 3 }$ Schottky photodiode. J. Mater. Chem. C 2019, 7, 13920–13929. [CrossRef] 





16. Zou, Y.; Zhang, Y.; Hu, Y.; Gu, H. Ultraviolet Detectors Based on Wide Bandgap Semiconductor Nanowire: A Review. Sensors 2018, 18, 2072. [CrossRef] 





17. Chen, Y.; Zhang, K.; Yang, X.; Chen, X.; Sun, J.; Zhao, Q.; Li, K.; Shan, C. Solar-blind photodetectors based on MXenes– ${ \bf \cdot } \beta { \bf - } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Schottky junctions. J. Phys. D Appl. Phys. 2020, 53, 484001. [CrossRef] 





18. Chen, X.; Liu, K.; Zhang, Z.; Wang, C.; Li, B.; Zhao, H.; Zhao, D.; Shen, D. Self-Powered Solar-Blind Photodetector with Fast Response Based on $\mathsf { A u } / \beta \mathsf { - G a } _ { 2 } \mathrm { O } _ { 3 }$ Nanowires Array Film Schottky Junction. ACS Appl. Mater. Interfaces 2016, 8, 4185–4191. [CrossRef] 





19. Zhi, Y.; Liu, Z.; Chu, X.; Li, S.; Yan, Z.; Wang, X.; Huang, Y.; Wang, J.; Wu, Z.; Guo, D.; et al. Self-Powered β-Ga2O3 Solar-Blind Photodetector Based on the Planar $\boldsymbol { \mathrm { A u } } / \boldsymbol { \mathrm { G a } } _ { 2 } \boldsymbol { \mathrm { O } } _ { 3 }$ Schottky Junction. ECS J. Solid State Sci. Technol. 2020, 9, 65011. [CrossRef] 





20. Liu, Z.; Zhi, Y.; Zhang, S.; Li, S.; Yan, Z.; Gao, A.; Zhang, S.; Guo, D.; Wang, J.; Wu, Z.; et al. Ultrahigh-performance planar $\mathsf { { \beta { - } } } G \mathsf { a } _ { 2 } \mathrm { { O } } _ { 3 }$ solar-blind Schottky photodiode detectors. Sci. China Technol. Sci. 2021, 64, 59–64. [CrossRef] 





21. Cui, S.; Mei, Z.; Zhang, Y.; Liang, H.; Du, X. Room-Temperature Fabricated Amorphous ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ High-Response-Speed Solar-Blind Photodetector on Rigid and Flexible Substrates. Adv. Opt. Mater. 2017, 5, 1700454. [CrossRef] 





22. Labed, M.; Sengouga, N.; Meftah, A.; Meftah, A.; Rim, Y.S. Study on the improvement of the open-circuit voltage of NiOx/Si heterojunction solar cell. Opt. Mater. 2021, 120, 111453. [CrossRef] 





23. Polyakov, A.Y.; Lee, I.-H.; Smirnov, N.B.; Yakimov, E.B.; Shchemerov, I.V.; Chernykh, A.V.; Kochkova, A.I.; Vasilev, A.A.; Carey, P.H.; Ren, F.; et al. Defects at the surface of $\beta { \mathrm { - } } G { \mathrm { a } } _ { 2 } { \mathrm { O } } _ { 3 }$ produced by Ar plasma exposure. APL Mater. 2019, 7, 061102. [CrossRef] 





24. Labed, M.; Sengouga, N.; Rim, Y.S. Control of $\mathrm { N i } / \beta { \cdot } \mathrm { G a } _ { 2 } \mathrm { O } _ { 3 }$ Vertical Schottky Diode Output Parameters at Forward Bias by Insertion of a Graphene Layer. Nanomaterials 2022, 12, 827. [CrossRef] 





25. Sze, S.M.; Ng, K.K. Physics and Properties of Semiconductors—A Review. Phys. Semicond. Devices 2006, 3, 5–75. 





26. Carey, P.H.; Yang, J.; Ren, F.; Hays, D.C.; Pearton, S.J.; Kuramata, A.; Kravchenko, I.I. Improvement of Ohmic contacts on ${ \mathrm { G a } } _ { 2 } { \mathrm { O } } _ { 3 }$ through use of ITO-interlayers. J. Vac. Sci. Technol. B 2017, 35, 61201. [CrossRef] 





27. Oshima, T.; Wakabayashi, R.; Hattori, M.; Hashiguchi, A.; Kawano, N.; Sasaki, K.; Masui, T.; Kuramata, A.; Yamakoshi, S.; Yoshimatsu, K.; et al. Formation of indium–tin oxide ohmic contacts for β-Ga O . Jpn. J. Appl. Phys. 2016, 55, 1202B7. [CrossRef] 





28. Li, K.-D.; Chen, P.-W.; Chang, K.-S.; Hsu, S.-C.; Jan, D.-J. Indium-Zinc-Tin-Oxide Film Prepared by Reactive Magnetron Sputtering for Electrochromic Applications. Materials 2018, 11, 2221. [CrossRef] 





29. Hakkoum, H.; Tibermacine, T.; Sengouga, N.; Belahssen, O.; Ghougali, M.; Benhaya, A.; Moumen, A.; Comini, E. Effect of the source solution quantity on optical characteristics of ZnO and NiO thin films grown by spray pyrolysis for the design NiO/ZnO photodetectors. Opt. Mater. 2020, 108, 110434. [CrossRef] 





30. Hassanien, A.S.; Akl, A.A. Influence of composition on optical and dispersion parameters of thermally evaporated non-crystalline Cd S Se thin films. J. Alloys Compd. 2015, 648, 280–290. [CrossRef] 





31. Yang, W.-C.; Rodriguez, B.J.; Gruverman, A.; Nemanich, R.J. Polarization-dependent electron affinity of LiNbO<sub>3</sub> surfaces. Appl. Phys. Lett. 2004, 85, 2316–2318. [CrossRef] 





32. Mohamed, M.; Irmscher, K.; Janowitz, C.; Galazka, Z.; Manzke, R.; Fornari, R. Schottky barrier height of Au on the transparent semiconducting oxide β-Ga O . Appl. Phys. Lett. 2012, 101, 132106. [CrossRef] 





33. Lee, H.Y.; Lichtenwalner, D.J.; Jur, J.S.; Kingon, A.I. Investigation of Conducting Oxide and Metal Electrode Work Functions on Lanthanum Silicate High-k Dielectric. ECS Trans. 2019, 11, 607–612. [CrossRef] 





34. Choi, K.-H.; Nam, H.-J.; Jeong, J.-A.; Cho, S.-W.; Kim, H.-K.; Kang, J.-W.; Kim, D.-G.; Cho, W.-J. Highly flexible and transparent InZnSnO /Ag/InZnSnO multilayer electrode for flexible organic light emitting diodes. Appl. Phys. Lett. 2008, 92, 223302. [CrossRef] 





35. Buchholz, D.B.; Proffit, D.E.; Wisser, M.D.; Mason, T.O.; Chang, R.P.H. Electrical and band-gap properties of amorphous zinc–indium–tin oxide thin films. Prog. Nat. Sci. Mater. Int. 2012, 22, 1–6. [CrossRef] 





36. Sato, K.; Yasumura, Y. Study of forward I-V plot for Schottky diodes with high series resistance. J. Appl. Phys. 1985, 58, 3655–3657. [CrossRef] 





37. Hu, Q.; Wang, P.; Yin, J.; Liu, Y.; Lv, B.; Zhu, J.-L.; Dong, Z.; Zhang, W.; Ma, W.; Sun, J. High-Responsivity Photodetector Based on a Suspended Monolayer Graphene/RbAg I Composite Nanostructure. ACS Appl. Mater. Interfaces 2020, 12, 50763–50771. [CrossRef] 





38. Periyanagounder, D.; Gnanasekar, P.; Varadhan, P.; He, J.-H.; Kulandaivel, J. High performance, self-powered photodetectors based on a graphene/silicon Schottky junction diode. J. Mater. Chem. C 2018, 6, 9545–9551. [CrossRef] 





39. Wu, D.; Zhao, Z.; Lu, W.; Rogée, L.; Zeng, L.; Lin, P.; Shi, Z.; Tian, Y.; Li, X.; Tsang, Y.H. Highly sensitive solar-blind deep ultraviolet photodetector based on graphene/PtSe2/β-Ga O 2D/3D Schottky junction with ultrafast speed. Nano Res. 2021, 14, 1973–1979. [CrossRef] 

