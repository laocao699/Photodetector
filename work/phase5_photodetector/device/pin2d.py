# 2D axisymmetric silicon PIN photodiode after Roger et al., MDPI Proceedings
# 2018, 2, 909 (doi:10.3390/proceedings2130909).
#
# Vertical NIP stack (light enters from the top n+ well):
#   n+ shallow well (top contact, cathode)
#   p- intrinsic EPI, resistivity 400 ohm.cm  (20 or 30 um)   <- absorber
#   p+ low-resistive substrate, 20 mohm.cm    (bottom contact, anode)
#
# The device is a 365 um circle, modelled in DEVSIM 2D cylindrical coordinates
# with x = radius (raxis), y = depth.

from devsim import (
    add_2d_contact,
    add_2d_mesh_line,
    add_2d_region,
    create_2d_mesh,
    create_device,
    finalize_mesh,
    set_parameter,
    cylindrical_edge_couple,
    cylindrical_node_volume,
    cylindrical_surface_area,
)
from devsim.python_packages.model_create import CreateNodeModel

# ---- baseline parameters (cm, cm^-3) ----
RADIUS = 182.5e-4        # 365 um diameter
T_SUB = 5.0e-4           # substrate thickness (assumed)
NA_EPI = 3.3e13          # 400 ohm.cm p-type  -> NA = 1/(q mu_p rho)
NA_SUB = 1.0e19          # 20 mohm.cm p+
ND_WELL = 1.0e19         # n+ well peak
XJ_WELL = 0.5e-4         # n+ well junction depth
WD_WELL = 0.15e-4        # erfc transition width

# derived device area (for current-density normalisation)
AREA_CM2 = 3.141592653589793 * RADIUS ** 2


def create_mesh(device, region, t_epi=20e-4, t_sub=T_SUB,
                dy_epi=0.5e-4, dy_sub=2.5e-4, nx=2, h_air=1.0e-4):
    """Build the 2D cylindrical mesh: x = radius [0, R], y = depth.

    Two thin dummy regions above and below the silicon are required so that
    add_2d_contact() has a region on both sides of each contact (DEVSIM
    requirement for the built-in 2D mesher).
    """
    t_end = t_epi + t_sub

    create_2d_mesh(mesh="pin2d")

    # depth (y): fine near the illuminated n+ well, uniform across the epi
    add_2d_mesh_line(mesh="pin2d", dir="y", pos=-h_air, ps=h_air)
    add_2d_mesh_line(mesh="pin2d", dir="y", pos=0.0, ps=1e-6)
    add_2d_mesh_line(mesh="pin2d", dir="y", pos=XJ_WELL * 0.5, ps=1e-6)
    add_2d_mesh_line(mesh="pin2d", dir="y", pos=XJ_WELL, ps=1e-6)
    y = XJ_WELL + dy_epi
    while y < t_epi - 1e-12:
        add_2d_mesh_line(mesh="pin2d", dir="y", pos=y, ps=dy_epi)
        y += dy_epi
    add_2d_mesh_line(mesh="pin2d", dir="y", pos=t_epi, ps=1e-6)
    y = t_epi + dy_sub
    while y < t_end - 1e-12:
        add_2d_mesh_line(mesh="pin2d", dir="y", pos=y, ps=dy_sub)
        y += dy_sub
    add_2d_mesh_line(mesh="pin2d", dir="y", pos=t_end, ps=1e-6)
    add_2d_mesh_line(mesh="pin2d", dir="y", pos=t_end + h_air, ps=h_air)

    # radius (x): structure is uniform in r, a few columns are enough
    for i in range(nx + 1):
        add_2d_mesh_line(mesh="pin2d", dir="x", pos=RADIUS * i / nx,
                         ps=RADIUS / nx)

    add_2d_region(mesh="pin2d", material="Si", region=region,
                  xl=0.0, xh=RADIUS, yl=0.0, yh=t_end)
    add_2d_region(mesh="pin2d", material="dummy", region="air_top",
                  xl=0.0, xh=RADIUS, yl=-h_air, yh=0.0)
    add_2d_region(mesh="pin2d", material="dummy", region="air_bot",
                  xl=0.0, xh=RADIUS, yl=t_end, yh=t_end + h_air)

    add_2d_contact(mesh="pin2d", name="cathode", material="metal",
                   region=region, xl=0.0, xh=RADIUS, yl=0.0, yh=0.0,
                   bloat=1e-10)
    add_2d_contact(mesh="pin2d", name="anode", material="metal",
                   region=region, xl=0.0, xh=RADIUS, yl=t_end, yh=t_end,
                   bloat=1e-10)

    finalize_mesh(mesh="pin2d")
    create_device(mesh="pin2d", device=device)
    return dict(t_epi=t_epi, t_sub=t_sub, t_end=t_end)


def set_doping(device, region, t_epi=20e-4):
    """n+ well / p- epi / p+ substrate net doping profile."""
    t_sub = T_SUB
    # donors: shallow n+ well (erfc decay from the top surface)
    CreateNodeModel(
        device, region, "Donors",
        "%.6e*erfc((y-%.6e)/%.6e)" % (ND_WELL, XJ_WELL, WD_WELL),
    )
    # acceptors: uniform p- epi plus p+ substrate (turns on below t_epi)
    CreateNodeModel(
        device, region, "Acceptors",
        "%.6e + %.6e*0.5*(1+erf((y-%.6e)/(%.6e)))"
        % (NA_EPI, NA_SUB, t_epi, 0.25e-4),
    )
    CreateNodeModel(device, region, "NetDoping", "Donors-Acceptors")


def setup_cylindrical(device, region):
    """Enable 2D cylindrical (axisymmetric) integration with x = radius."""
    set_parameter(device=device, name="raxis_variable", value="x")
    set_parameter(device=device, name="raxis_zero", value=0.0)
    cylindrical_node_volume(device=device, region=region)
    cylindrical_edge_couple(device=device, region=region)
    cylindrical_surface_area(device=device, region=region)
    set_parameter(name="node_volume_model", value="CylindricalNodeVolume")
    set_parameter(name="edge_couple_model", value="CylindricalEdgeCouple")
    set_parameter(name="surface_area_model", value="CylindricalSurfaceArea")
    set_parameter(name="element_edge_couple_model",
                  value="ElementCylindricalEdgeCouple")
    set_parameter(name="element_node0_volume_model",
                  value="ElementCylindricalNodeVolume@en0")
    set_parameter(name="element_node1_volume_model",
                  value="ElementCylindricalNodeVolume@en1")
