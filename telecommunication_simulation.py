import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import hilbert
import warnings
warnings.filterwarnings('ignore')

# ============================================
# Initial Settings and Parameters
# ============================================
fs = 10000
T = 1
t = np.arange(0, T, 1/fs)
N = len(t)

print("="*60)
print("TELECOMMUNICATION SYSTEMS PROJECT - COMPLETE SIMULATION")
print("="*60)

# ============================================
# Signal Analysis Function (FIXED)
# ============================================
def analyze_signal(signal, time_vector, title, freq_limit=400, fc=None, bandwidth=120):

    n = len(signal)

    # Energy & Power
    energy = np.trapz(signal**2, time_vector)
    power = np.mean(signal**2)

    # FFT
    X = fft(signal)
    f = np.fft.fftfreq(n, d=1/fs)

    idx = np.where(f >= 0)
    f_pos = f[idx]
    X_pos = X[idx]
    X_mag = 2*np.abs(X_pos)/n

    plt.figure(figsize=(14,5))

    # Time Domain
    plt.subplot(1,2,1)
    plt.plot(time_vector, signal, 'b', linewidth=1)
    plt.title(f'{title} - Time Domain')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.xlim(0,0.5)

    # Frequency Domain
    plt.subplot(1,2,2)
    markerline, stemlines, baseline = plt.stem(
        f_pos, X_mag,
        linefmt='r-',
        markerfmt='ro',
        basefmt='k-'
    )
    plt.setp(markerline, markersize=4)

    plt.title(f'{title} - Frequency Domain')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("|X(f)|")
    plt.grid(True, alpha=0.3)

    # اصلاح اصلی اینجاست 👇
    if fc is not None:
        plt.xlim(fc - bandwidth/2, fc + bandwidth/2)
    else:
        plt.xlim(0, freq_limit)

    plt.tight_layout()
    plt.show()

    return energy, power

# ============================================
# PART 1: MESSAGE SIGNAL
# ============================================
print("\n" + "="*60)
print("PART 1: MESSAGE SIGNAL")
print("="*60)

fm1 = 5
fm2 = 12

m_t = np.sin(2*np.pi*fm1*t) + 0.5*np.cos(2*np.pi*fm2*t)

e1, p1 = analyze_signal(m_t, t, 'Message Signal', freq_limit=30)

# ============================================
# PART 2: ADDING NOISE
# ============================================
print("\n" + "="*60)
print("PART 2: ADDING AWGN")
print("="*60)

SNR_dB = 20

P_signal = np.mean(m_t**2)
P_noise = P_signal / (10**(SNR_dB/10))
noise_std = np.sqrt(P_noise)

noise = noise_std * np.random.randn(len(m_t))
m_t_noisy = m_t + noise

SNR_actual = 10 * np.log10(np.mean(m_t**2) / np.mean(noise**2))
print(f"Target SNR: {SNR_dB} dB")
print(f"Actual SNR: {SNR_actual:.2f} dB")

e2, p2 = analyze_signal(m_t_noisy, t, 'Noisy Signal', freq_limit=30)

# ============================================
# PART 3: CARRIER
# ============================================
print("\n" + "="*60)
print("PART 3: CARRIER")
print("="*60)

Ac = 100
fc = 250

carrier = Ac * np.cos(2*np.pi*fc*t)

# ============================================
# PART 4: MODULATIONS
# ============================================
print("\n" + "="*60)
print("PART 4: MODULATIONS (AM, FM, PM)")
print("="*60)

# AM
mu = 0.5
x_AM_t = Ac * (1 + mu*m_t) * np.cos(2*np.pi*fc*t)
analyze_signal(x_AM_t, t, 'AM Modulation', fc=fc, bandwidth=300)

# FM
f_delta = 50
m_int = np.cumsum(m_t)/fs
x_FM_t = Ac * np.cos(2*np.pi*fc*t + 2*np.pi*f_delta*m_int)
analyze_signal(x_FM_t, t, 'FM Modulation', fc=fc, bandwidth=300)

# PM
phi_delta = np.pi/2
x_PM_t = Ac * np.cos(2*np.pi*fc*t + phi_delta*m_t)
analyze_signal(x_PM_t, t, 'PM Modulation', fc=fc, bandwidth=300)

# ============================================
# PART 5: DEMODULATION
# ============================================
print("\n" + "="*60)
print("PART 5: DEMODULATION")
print("="*60)

# AM
analytic_am = hilbert(x_AM_t)
envelope = np.abs(analytic_am)
demod_am = (envelope - Ac)/(Ac*mu)
demod_am -= np.mean(demod_am)
demod_am_norm = demod_am/np.max(np.abs(demod_am))

# FM
analytic_fm = hilbert(x_FM_t)
inst_phase_fm = np.unwrap(np.angle(analytic_fm))
inst_freq = np.diff(inst_phase_fm)*fs/(2*np.pi)
inst_freq = np.append(inst_freq, inst_freq[-1])
demod_fm = (inst_freq - fc)/f_delta
demod_fm -= np.mean(demod_fm)
demod_fm_norm = demod_fm/np.max(np.abs(demod_fm))

# PM
analytic_pm = hilbert(x_PM_t)
inst_phase_pm = np.unwrap(np.angle(analytic_pm))
demod_pm = inst_phase_pm - (2*np.pi*fc*t)
demod_pm -= np.mean(demod_pm)
demod_pm_norm = demod_pm/np.max(np.abs(demod_pm))

m_t_norm = m_t/np.max(np.abs(m_t))

# ============================================
# PART 6: COMPARISON
# ============================================
print("\n" + "="*60)
print("PART 6: COMPARISON")
print("="*60)

plt.figure(figsize=(14,12))

plt.subplot(3,1,1)
plt.plot(t, m_t_norm, label='Original')
plt.plot(t, demod_am_norm, '--', label='AM')
plt.legend()
plt.xlim(0,0.5)
plt.grid()

plt.subplot(3,1,2)
plt.plot(t, m_t_norm, label='Original')
plt.plot(t, demod_fm_norm, '--', label='FM')
plt.legend()
plt.xlim(0,0.5)
plt.grid()

plt.subplot(3,1,3)
plt.plot(t, m_t_norm, label='Original')
plt.plot(t, demod_pm_norm, '--', label='PM')
plt.legend()
plt.xlim(0,0.5)
plt.grid()

plt.tight_layout()
plt.show()

# ============================================
# PART 7: ERROR METRICS
# ============================================
print("\n" + "="*60)
print("PART 7: ERROR METRICS")
print("="*60)

mse_am = np.mean((m_t_norm - demod_am_norm)**2)
mse_fm = np.mean((m_t_norm - demod_fm_norm)**2)
mse_pm = np.mean((m_t_norm - demod_pm_norm)**2)

corr_am = np.corrcoef(m_t_norm, demod_am_norm)[0,1]
corr_fm = np.corrcoef(m_t_norm, demod_fm_norm)[0,1]
corr_pm = np.corrcoef(m_t_norm, demod_pm_norm)[0,1]

print(f"AM - MSE: {mse_am:.6f}, Correlation: {corr_am:.4f}")
print(f"FM - MSE: {mse_fm:.6f}, Correlation: {corr_fm:.4f}")
print(f"PM - MSE: {mse_pm:.6f}, Correlation: {corr_pm:.4f}")