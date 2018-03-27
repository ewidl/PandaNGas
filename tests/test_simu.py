import numpy as np
import pandangas.simulation as sim
import pandangas.topology as top

import fluids
from thermo.chemical import Chemical

from tests.test_core import fix_create


def test_scaled_loads(fix_create):
    net = fix_create
    assert sim._scaled_loads_as_dict(net) == {'BUS2': 0.000262, 'BUS3': 0.000394}


def test_p_min_loads(fix_create):
    net = fix_create
    assert sim._p_min_loads_as_dict(net) == {'BUS2': 0.022E5, 'BUS3': 0.022E5}


def test_p_nom_feed(fix_create):
    net = fix_create
    assert sim._p_nom_feed_as_dict(net) == {'BUS1': 0.025E5, 'BUSF': 0.9E5}


def test_i_mat(fix_create):
    net = fix_create
    g = top.graphs_by_level_as_dict(net)["BP"]
    i_mat = sim._i_mat(g)
    assert type(i_mat) is np.matrixlib.defmatrix.matrix
    waited = np.array([[1., 0., 1.], [-1., -1., 0.], [0., 1., -1.]])
    for l in waited:
        assert l in np.asarray(i_mat)


def test_dp_from_m_dot():
    gas = Chemical('natural gas', T=10+273.15, P=4.5E5)
    material = fluids.nearest_material_roughness('steel', clean=True)
    eps = fluids.material_roughness(material)
    assert round(sim._dp_from_m_dot_vec(0.005, 100, 0.05, eps, gas).tolist(), 1) == 61.8


def test_run_sim(fix_create):
    net = fix_create
    p_nodes, m_dot_pipes, m_dot_nodes = sim._run_sim(net)
    assert p_nodes == {'BUS1': 2500.0, 'BUS2': 1962.7, 'BUS3': 1827.8}
    assert m_dot_pipes == {'PIPE3': 6.6e-05, 'PIPE1': 0.000328, 'PIPE2': 0.000328}
    assert m_dot_nodes == {'BUS1': -0.000656, 'BUS2': 0.000262, 'BUS3': 0.000394}
