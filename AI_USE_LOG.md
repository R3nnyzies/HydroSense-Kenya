# AI Use Log: HydroSense-Kenya Capstone Project

**Project Title:** HydroSense-Kenya: A Scientific Computing System for Smart Irrigation

**Course:** ICS 2207 Scientific Computing

**Semester:** February-May 2026

## Statement of Responsible AI Use
In accordance with the project requirements, AI-assisted coding tools (e.g., ChatGPT, GitHub Copilot) were used strictly as support tools for syntax generation, conceptual explanations, and boilerplate test generation. **No AI output was treated as authoritative.** Every AI-generated function, loop, and visualization was thoroughly inspected, modified to fit the specific agro-climatic context of this project, and validated using numerical experiments or trusted reference methods.

---

## AI Prompt and Validation Log

| Prompt Used | AI Output Summary | Accepted? | Modified? | Validation Method |
| :--- | :--- | :--- | :--- | :--- |
| *Example: Generate pytest cases for bisection method* | *AI proposed tests for x^2 - 4* | *Partly* | *Tolerance adjusted to 1e-5* | *Compared with known root x = 2* |
| *Example: Explain central difference accuracy* | *AI gave a conceptual explanation* | *Yes* | *Edited for clarity* | *Checked against lecture notes and numerical experiment* |
| "How to interpolate missing values in a Pandas dataframe but grouped by a specific column like `zone_id`?" | Suggested using `df.groupby('zone_id').apply(lambda x: x.interpolate())`. | Partly | Modified to use `.transform()` instead of `.apply()` to prevent MultiIndex creation, and added `.bfill().ffill()` to handle edge cases (NaNs at the start/end). | Checked `df.isna().sum()` before and after. Plotted the output using Matplotlib to visually confirm that the interpolation didn't create artificial spikes. |
| "Write a Python implementation of Simpson's 1/3 rule that can handle an even number of data points." | Provided a function that uses Simpson's 1/3 for the first $n-1$ points and adds the Trapezoidal rule for the last segment. | Yes | Adjusted the array slicing (e.g., `y[1:-2:2]`) to perfectly match NumPy vectorization and avoid loop overhead. | Tested in `test_integration.py` against the known integral of $f(x) = x^2$ from 0 to 2. Checked results against `scipy.integrate.simpson` for verification only. |
| "Python code for Runge-Kutta 4th order method for a differential equation." | Generated a generic RK4 solver `rk4(f, y0, t, dt)`. | Partly | Completely refactored the function parameters to take our specific environmental variables (`R`, `I`, `ET`, `field_capacity`) and call our `soil_water_derivative` function. | Ran a numerical experiment in `test_simulation.py` comparing RK4 output to the Euler method for a linear case (where no drainage is triggered); confirmed identical results. |
| "Write a function to solve $Ax = b$ using manual Gaussian elimination." | Provided a basic Gaussian elimination algorithm with forward elimination and back substitution. | Partly | Added partial pivoting logic (`np.argmax(abs(M[i:n, i]))`) to prevent division by zero, and raised a `ValueError` for singular matrices. | Checked against `np.linalg.solve` for verification. Added a specific test in `test_linear_systems.py` to ensure it successfully fails on singular matrices. |
| "Generate 1000 Monte Carlo scenarios for rainfall data by adding random noise." | Proposed using a `for` loop with `random.uniform(-0.5, 0.5)` added to the rainfall values. | No | Discarded the uniform addition. Re-wrote it to use `np.random.normal` as a multiplicative multiplier (`scale=0.3`), and added `np.maximum(0, rain)` to prevent negative rainfall. | Printed `.shape` to confirm `(1000, n_days)`. Visualized the 5th and 95th percentiles using `matplotlib` fill_between to ensure the uncertainty envelope was physically realistic. |
| "Generate pytest cases for manual Gaussian elimination function." | Provided basic tests for 2x2 and 3x3 matrices. | Partly | Kept the 3x3 test case but manually added a test for linear dependence (identical rows) to check error handling. | Ran `pytest tests/test_linear_systems.py` and manually solved the 3x3 matrix on paper to confirm the expected output `x=[2, 3, -1]`. |
| "Create a matplotlib plot with dual Y-axes for soil moisture and irrigation." | Provided boilerplate code using `fig, ax1 = plt.subplots()` and `ax2 = ax1.twinx()`. | Yes | Adjusted colors to scientific standards (`tab:blue`, `tab:cyan`), added horizontal threshold lines for `min_moisture`, and fixed legend positioning. | Executed the plot function (`plot_optimized_schedule`) in the Jupyter Notebook to ensure legends didn't overlap and axes scales were legible. |

***

### Summary of AI Impact on the Project
The use of AI significantly sped up the generation of boilerplate code (like the structural setup of Matplotlib graphs and basic Pytest assertions). However, **AI frequently failed at context-specific scientific logic**. For example:
1. It did not inherently know that rainfall cannot be negative in Monte Carlo simulations.
2. It failed to implement partial pivoting in Gaussian elimination, which would have resulted in floating-point errors.
3. It struggled with Pandas `MultiIndex` behaviors when grouping and interpolating simultaneously.

By treating the AI as an assistant rather than an authoritative source, the group was able to use numerical reasoning to correct these flaws, fulfilling the reproducibility, stability, and verification goals of the ICS 2207 syllabus.