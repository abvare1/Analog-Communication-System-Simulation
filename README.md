# Analog Communication System Simulation (AM, FM, PM)

This project provides a complete end-to-end simulation of an analog communication chain, including signal generation, noise modeling, multiple modulation schemes, and digital recovery using Hilbert Transform.

##  Simulation Workflow

The project is structured into 7 core parts, following a professional communication engineering pipeline:

### PART 1: Message Signal Generation
A multi-tone signal $x(t) = \sin(2\pi \cdot 5t) + 0.5 \cos(2\pi \cdot 12t)$ is defined as the information source. The system calculates the initial energy and power in both time and frequency domains.

### PART 2: AWGN Noise Modeling
To simulate a real-world channel, **Additive White Gaussian Noise (AWGN)** is added to the message.
* **Target SNR:** 20 dB.
* The script calculates the actual SNR after adding noise to verify channel conditions.

### PART 3: Carrier Configuration
A high-frequency carrier signal is generated with:
* **Amplitude ($A_c$):** 100
* **Frequency ($f_c$):** 250 Hz

### PART 4: Modulation Schemes
Implementation of three major analog modulations:
1. **AM (DSB-FC):** Using a modulation index ($\mu$) of 0.5.
2. **FM:** Frequency deviation set to $f_{\Delta} = 50$ Hz/V.
3. **PM:** Phase deviation set to $\phi_{\Delta} = \pi/2$ rad/V.

### PART 5: Advanced Digital Demodulation
Signal recovery is performed using the **Analytic Signal (Hilbert Transform)**:
* **AM Recovery:** Envelope detection via `abs(hilbert(x))`.
* **FM Recovery:** Instantaneous frequency estimation by taking the derivative of the unwrapped phase.
* **PM Recovery:** Instantaneous phase extraction and carrier phase subtraction.

### PART 6: Comparison & Visualization
The original signal is plotted against the recovered signals for AM, FM, and PM to visually assess the fidelity of each modulation scheme.

### PART 7: Performance Metrics (Error Analysis)
The system evaluates the quality of reconstruction using:
* **Mean Squared Error (MSE):** Quantifies the difference between original and recovered signals.
* **Correlation Coefficient:** Measures the linear relationship and similarity between waveforms.

---

## 📊 Visual Results
The repository includes visual representations of:
* Time-domain waveforms for all modulated signals.
* Frequency spectra (FFT) showing the distribution of power and sidebands.
* Comparison plots of Original vs. Recovered signals.

##  Tech Stack
* **Language:** Python 3.12
* **Libraries:** NumPy, SciPy (Signal Processing), Matplotlib (Visualization)

---
*This project was developed for the Analog Communication Systems course.*
