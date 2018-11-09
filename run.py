import initialisation
import eroscode
import plotting_analytical
import plots
import statistical_ensemble as se


def run_asteroid(planet="Earth", asteroid='Tunguska', show=True, anal_assumption=False, tol=1e-8):
    """
    Run the simulation for a specified asteroid and planet
    Returns:
            array_like
    """

    initialisation.set_parameters(planet, analytical_assumption=anal_assumption)
    if asteroid == "Analytical Assumptions":
        initialisation.set_parameters(planet, analytical_assumption=anal_assumption)
    initialisation.settolerance(tol)
    state = initialisation.set_variables(asteroid)
    eroscode.initial_state = state
    eroscode.ensemble = False
    eroscode.main()
    final_state = eroscode.main()

    if show is True:
        plots.plot_5_graphs(final_state)

    return final_state


def run_custom(variables, planet="Earth", show=True, anal_assumption=False, tol=1e-8):
    """
    input:
    variables = array li
                v_init, m_init, theta_init, z_init, x_init, r_init
                
    output:
        
    """

    initialisation.set_parameters(planet, analytical_assumption=anal_assumption)

    initialisation.settolerance(tol)
    state = variables
    eroscode.initial_state = state
    eroscode.ensemble = False
    eroscode.main()
    final_state = eroscode.main()

    if show is True:
        plots.plot_5_graphs(final_state)

    return final_state


def run_ensemble(planet="Earth", num=10, show=True, tol=1e-8):
    final_states = []
    ke = []
    height = []
    initialisation.set_parameters(planet, analytical_assumption=False)
    initialisation.settolerance(tol)
    eroscode.ensemble = True

    states = se.confidence_prediction(num)
    for n, i in enumerate(range(states.shape[1])):
        if n % 50 == 0:
            print(n)
        state = states[:, i]
        eroscode.initial_state = state
        eroscode.main()
        final_state = eroscode.main()
        ke_max_value, ke_max_height = eroscode.find_ke_max(final_state)

        ke.append(ke_max_value)
        height.append(ke_max_height)
        final_states.append(final_state)

    if show is True:
        plots.ensemble_scatter(ke, height)

    return final_states


def analytical_compare(asteroid="Chelyabinsk"):
    v_init, m_init, theta_init, z_init, x_init, diam_init, rho_m, y = initialisation.set_variables(asteroid)
    print(v_init, m_init, theta_init, z_init, x_init, diam_init)

    plotting_analytical.initialise_parameters(C_D=1, H=8000, rho_0=1.2)
    plotting_analytical.initialise_variables(v_init, m_init, theta_init, z_init, diam_init)

    initialisation.set_parameters(planet="Earth", analytical_assumption=True)
    initialisation.set_variables(asteroid)

    analytical = plotting_analytical.analytical()
    numerical = run_asteroid(asteroid, show=False, anal_assumption=True)

    plots.analytical_comparison(analytical, numerical)


#run_asteroid(planet="Earth", anal_assumption=False)
#run_ensemble(num=200)
analytical_compare()