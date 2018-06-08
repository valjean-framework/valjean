'''Plot detector response for Livermore spheres'''

# pylint: disable=invalid-name

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.rcParams['font.size'] = 15

def read_file(tfile):
    '''Read the file and return energy bin and associated response.'''
    ebins, response = [], []
    with open(tfile) as fil:
        for line in fil:
            ebins.append(eval(line.split()[0]))
            response.append(eval(line.split()[1]))
    return np.array(ebins), np.array(response)

fdir = "/data/tmplepp/el220326/RunTripoli/spheresLivermore/input"
old_ne213_file = os.path.join(fdir, "old_NE213_response.txt")
new_ne213_file = os.path.join(fdir, "new_NE213_response.txt")

old_ne213_eb, old_ne213_resp = read_file(old_ne213_file)
new_ne213_eb, new_ne213_resp = read_file(new_ne213_file)

# print(np.amax(old_ne213_resp), np.amax(new_ne213_resp))
# ne213_factor = np.amax(old_ne213_resp) / np.amax(new_ne213_resp)
# print(np.argmax(old_ne213_resp), np.argmax(new_ne213_resp))
# print(old_ne213_eb[np.argmax(old_ne213_resp)],
#       new_ne213_eb[np.argmax(new_ne213_resp)])

# bin 134 corresponding to energy = 15.0 MeV in UCID-16-372
ne213_factor = 3.061
print(new_ne213_eb[134], "new factor=", ne213_factor,
      "old one =", np.amax(old_ne213_resp) / np.amax(new_ne213_resp))

plt.figure(1)
plt.plot(old_ne213_eb, old_ne213_resp,
         's-', ms=5, color='m', label="Old response")
plt.plot(new_ne213_eb, new_ne213_resp,
         'o-', ms=2, color='b', label="New response")
plt.plot(new_ne213_eb, new_ne213_resp*ne213_factor,
         'o-', ms=2, mfc="none", color='c',
         label=r"New response $\times$ max ratio")
plt.legend()
plt.xlabel("Energy [MeV]")
plt.ylabel(r"Response (A$\epsilon$) [%]")
plt.title("Response of NE213 detector")
plt.savefig("NE213_response.png")


old_pilotb_file = os.path.join(fdir, "old_PILOT-B_response.txt")
new_pilotb_file = os.path.join(fdir, "new_PILOT-B_response.txt")


old_pilotb_eb, old_pilotb_resp = read_file(old_pilotb_file)
new_pilotb_eb, new_pilotb_resp = read_file(new_pilotb_file)

# pilotb_factor = np.amax(old_pilotb_resp) / np.amax(new_pilotb_resp)
# bin 134 corresponding to energy = 15.0 MeV
print(new_pilotb_eb[134])
pilotb_factor = 3.741

plt.figure(2)
plt.plot(old_pilotb_eb, old_pilotb_resp,
         's-', ms=5, color='m', label="Old response")
plt.plot(new_pilotb_eb, new_pilotb_resp,
         'o-', ms=2, color='b', label="New response")
plt.plot(new_pilotb_eb, new_pilotb_resp*pilotb_factor,
         'o-', ms=2, mfc="none", color='c',
         label=r"New response $\times$ max ratio")
plt.legend()
plt.xlabel("Energy [MeV]")
plt.ylabel(r"Response (A$\epsilon$) [%]")
plt.title("Response of PILOT-B detector")
plt.savefig("PILOT-B_response.png")
# plt.show()

# print in file values to use them in T4

ofile = open("detectors_responses.txt", 'w')
ofile.write("NE213\n")
for ind, ebin in enumerate(new_ne213_eb):
    ofile.write("{0:>15}{1:.1f}   {2:.4f}\n"
                .format(" ", ebin, new_ne213_resp[ind]*ne213_factor))

ofile.write("\nPILOT-B\n")
for ind, ebin in enumerate(new_pilotb_eb):
    ofile.write("{0:>15}{1:.1f}   {2:.4f}\n"
                .format(" ", ebin, new_pilotb_resp[ind]*pilotb_factor))

ofile.close()


# Test response versus time
# MCNP:
#    E= rme*((1.0/dsqrt(1.0-(fp*fp/(t*t*c*c))))-1.0)
# where
#    c= velocity of light = 29.97925 cm/nanosecond
#    t= the time (in nanoseconds), at the midpoint of the time bin
#    fp= the length of the flightpath (in cm)
#    rme= the rest mass energy of a neutron (939.550 MeV)
#    E= the energy of the neutron

light_vel = 29.97925
m_neutron = 939.550
def time_to_energy(time, length):
    gamma = np.sqrt(1 - (length**2 / (time**2 * light_vel**2)))
    energy = m_neutron * (1/gamma - 1)
    return energy

def energy_to_time(energy, length):
    num = 1 + energy / m_neutron
    denom = np.sqrt(num**2 -1)
    time = length / light_vel * num / denom
    return time

time_from_old_ne213_30deg = energy_to_time(old_ne213_eb, 766.0)
print(time_from_old_ne213_30deg)
check_calcul = time_to_energy(time_from_old_ne213_30deg, 766.0)
print(check_calcul)
time_from_old_ne213_120deg = energy_to_time(old_ne213_eb, 975.2)
time_from_new_ne213_30deg = energy_to_time(new_ne213_eb, 766.0)
time_from_new_ne213_120deg = energy_to_time(new_ne213_eb, 975.2)

time_from_old_pilotb_30deg = energy_to_time(old_pilotb_eb, 766.0)
time_from_old_pilotb_120deg = energy_to_time(old_pilotb_eb, 975.2)
time_from_new_pilotb_30deg = energy_to_time(new_pilotb_eb, 766.0)
time_from_new_pilotb_120deg = energy_to_time(new_pilotb_eb, 975.2)

print("Energy at 300 ns at 766.0 cm =", time_to_energy(300, 766.0))
print("Energy at 300 ns at 966.0 cm =", time_to_energy(300, 966.0))

plt.figure(3)
plt.plot(time_from_old_ne213_30deg, old_ne213_resp,
         's-', ms=5, color='m', label="Old response, 30°")
plt.plot(time_from_new_ne213_30deg, new_ne213_resp,
         'o-', ms=5, color='b', label="New response, 30°")
plt.plot(time_from_new_ne213_30deg, new_ne213_resp*ne213_factor,
         'o-', ms=2, mfc="none", color='c',
         label=r"New response $\times$ max ratio, 30°")
plt.legend()
plt.xlabel("Time [ns]")
plt.ylabel(r"Response (A$\epsilon$) [%]")
plt.title("Response of NE213 detector at L = 766.0 cm (30°)")
plt.savefig("NE213_response_vs_time.png")

plt.figure(4)
plt.plot(time_from_old_pilotb_30deg, old_pilotb_resp,
         's-', ms=5, color='m', label="Old response, 30°")
plt.plot(time_from_new_pilotb_30deg, new_pilotb_resp,
         'o-', ms=5, color='b', label="New response, 30°")
plt.plot(time_from_new_pilotb_30deg, new_pilotb_resp*pilotb_factor,
         'o-', ms=2, mfc="none", color='c',
         label=r"New response $\times$ max ratio, 30°")
plt.legend()
plt.xlabel("Time [ns]")
plt.ylabel(r"Response (A$\epsilon$) [%]")
plt.title("Response of PILOT-B detector at L = 766.0 cm (30°)")
plt.savefig("PILOT-B_response_vs_time.png")
# plt.show()

# Test interpolation in order to compare...
# inutile : utiliser les bins de new suffit !
# et on est sur que ce sont les memes !
def get_smaller_interval(array):
    interval = 100
    for ielt in range(len(array[:-1])):
        # print("i =", ielt, "j=", ielt+1)
        # print("interval =", array[ielt+1] - array[ielt])
        if array[ielt+1] - array[ielt] < interval:
            interval = array[ielt+1] - array[ielt]
    return interval

print(len(old_ne213_eb))
old_ne213_interval = get_smaller_interval(old_ne213_eb)
new_ne213_interval = get_smaller_interval(new_ne213_eb)
nb_evals = (new_ne213_eb[-1] - new_ne213_eb[0])/new_ne213_interval + 1
# All advices to use linspace instead of arange, but ugly with rounding
evals = np.linspace(new_ne213_eb[0], new_ne213_eb[-1], int(nb_evals))
new_ne213_interp = np.interp(evals, new_ne213_eb, new_ne213_resp)
# evals1 = np.arange(new_ne213_eb[0], new_ne213_eb[-1], new_ne213_interval)
# print(new_ne213_eb[0], new_ne213_eb[-1])
# print(len(evals))
# print(evals)
# print(evals1)
# print(np.linspace(1.6, 16, 144))
# print(new_ne213_resp)
# print(new_ne213_interp)
# print("len(eb) =", len(new_ne213_eb))
# print("len(resp) =", len(new_ne213_resp), "interp =", len(new_ne213_interp))

old_ne213_interp = np.interp(new_ne213_eb, old_ne213_eb, old_ne213_resp)
# print(old_ne213_interp)

fig, splt = plt.subplots(2, sharex=True,
                         gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
splt[0].plot(old_ne213_eb, old_ne213_resp,
             's-', ms=5, color='m', label="Old response")
splt[0].plot(new_ne213_eb, new_ne213_resp*ne213_factor,
             'o-', ms=2, mfc="none", color='c',
             label=r"New response $\times$ max ratio")
splt[0].plot(new_ne213_eb, old_ne213_interp,
             'o-', ms=2, color='y',
             label=r"Interpolation old")
splt[0].set_ylabel(r"Response (A$\epsilon$) [%]")
splt[0].set_title("Response of NE213 detector")
splt[0].legend()
splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
ratio = new_ne213_resp[1:]*ne213_factor / old_ne213_interp[1:]
splt[1].plot(new_ne213_eb[1:], ratio,
             'ro-', ms=3, label="New / old interpolated")
splt[1].set_ylim(ymax=1 + (1-np.min(ratio)))
splt[1].set_ylabel("Ratio")
splt[1].set_xlabel("Energy [MeV]")
splt[1].legend()

old_pilotb_interp = np.interp(new_pilotb_eb, old_pilotb_eb, old_pilotb_resp)
fig, splt = plt.subplots(2, sharex=True,
                         gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
splt[0].plot(old_pilotb_eb, old_pilotb_resp,
             's-', ms=5, color='m', label="Old response")
splt[0].plot(new_pilotb_eb, new_pilotb_resp*pilotb_factor,
             'o-', ms=2, mfc="none", color='c',
             label=r"New response $\times$ max ratio")
splt[0].plot(new_pilotb_eb, old_pilotb_interp,
             'o-', ms=2, color='y',
             label=r"Interpolation old")
splt[0].set_ylabel(r"Response (A$\epsilon$) [%]")
splt[0].set_title("Response of PILOT-B detector")
splt[0].legend()
splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
ratio = new_pilotb_resp[1:]*pilotb_factor / old_pilotb_interp[1:]
splt[1].plot(new_pilotb_eb[1:], ratio,
             'ro-', ms=3, label="New / old interpolated")
splt[1].set_ylabel("Ratio")
splt[1].set_xlabel("Energy [MeV]")
splt[1].legend()


# Et en fonction du temps
fig, splt = plt.subplots(2, sharex=True,
                         gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
splt[0].plot(time_from_old_ne213_30deg, old_ne213_resp,
             's-', ms=5, color='m', label="Old response")
splt[0].plot(time_from_new_ne213_30deg, new_ne213_resp*ne213_factor,
             'o-', ms=2, mfc="none", color='c',
             label=r"New response $\times$ max ratio")
splt[0].plot(time_from_new_ne213_30deg, old_ne213_interp,
             'o-', ms=2, color='y',
             label=r"Interpolation old")
splt[0].set_ylabel(r"Response (A$\epsilon$) [%]")
splt[0].set_title("Response of NE213 detector")
splt[0].legend()
splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
ratio = new_ne213_resp[1:]*ne213_factor / old_ne213_interp[1:]
splt[1].plot(time_from_new_ne213_30deg[1:], ratio,
             'ro-', ms=3, label="New / old interpolated")
splt[1].set_ylim(ymax=1 + (1-np.min(ratio)))
splt[1].set_ylabel("Ratio")
splt[1].set_xlabel("Time [ns]")
splt[1].legend()


fig, splt = plt.subplots(2, sharex=True,
                         gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
splt[0].plot(time_from_old_pilotb_30deg, old_pilotb_resp,
             's-', ms=5, color='m', label="Old response")
splt[0].plot(time_from_new_pilotb_30deg, new_pilotb_resp*pilotb_factor,
             'o-', ms=2, mfc="none", color='c',
             label=r"New response $\times$ max ratio")
splt[0].plot(time_from_new_pilotb_30deg, old_pilotb_interp,
             'o-', ms=2, color='y',
             label=r"Interpolation old")
splt[0].set_ylabel(r"Response (A$\epsilon$) [%]")
splt[0].set_title("Response of PILOT-B detector")
splt[0].legend()
splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
ratio = new_pilotb_resp[1:]*pilotb_factor / old_pilotb_interp[1:]
splt[1].plot(time_from_new_pilotb_30deg[1:], ratio,
             'ro-', ms=3, label="New / old interpolated")
splt[1].set_ylabel("Ratio")
splt[1].set_xlabel("Time [ns]")
splt[1].legend()

# plt.show()

def read_numerated_values(tfile):
    '''Read the file and return energy bin and associated response for
    numerated response from Wong 72.
    '''
    ebins, response = [], []
    with open(tfile) as fil:
        for line in fil:
            if line.startswith('"') or line == "\n":
                continue
            elif len(line.split(',')) != 3:
                continue
            else:
                ebins.append(eval(line.split(',')[0]))
                response.append(eval(line.split(',')[1]))
    # print("Energy bins:", np.array(ebins))
    # print("Response:", np.array(response))
    return np.array(ebins), np.array(response)

ne213_numerated_file = "NE213_numerise_v0.csv"
num_ne213_eb, num_ne213_resp = read_numerated_values(ne213_numerated_file)
ne213_numerated_file1 = "NE213_numerise_v1.csv"
num_ne213_eb1, num_ne213_resp1 = read_numerated_values(ne213_numerated_file1)


def read_from_UCID_16372(tfile):
    '''Read the file and return energy bin and associated response for
    numerated response from Wong 72.
    '''
    ebins, response = [], []
    with open(tfile) as fil:
        for line in fil:
            ebins.append(eval(line.split()[0]))
            response.append(eval(line.split()[1]))
    print("Energy bins:", np.array(ebins))
    print("Response:", np.array(response))
    return np.array(ebins), np.array(response)

ne213_ucid16372_eb, ne213_ucid16372_resp = read_from_UCID_16372("ne213_UCID-16372.txt")

# fig, splt = plt.subplots(2, sharex=True,
#                          gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
fig, splt = plt.subplots(1)
# , sharex=True,
# gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
splt.plot(old_ne213_eb, old_ne213_resp,
          's-', ms=5, color='m', label="Old response")
splt.plot(new_ne213_eb, old_ne213_interp,
          '--', color='plum', label="Old response interpolated")
# splt.plot(new_ne213_eb, new_ne213_resp*ne213_factor,
#           'o-', ms=2, mfc="none", color='c',
#           label=r"New response $\times$ max ratio")
splt.plot(new_ne213_eb, new_ne213_resp*ne213_factor,
          'o-', ms=2, mfc="none", color='c',
          label=r"Response in MCNP renormalised")
# splt.plot(num_ne213_eb, num_ne213_resp,
#              'o-', ms=2, color='b', label="Digitized curve")
# splt.plot(num_ne213_eb1, num_ne213_resp1,
#           'o-', ms=2, color='b', label="Digitized curve")
splt.plot(ne213_ucid16372_eb, ne213_ucid16372_resp,
          'o-', ms=2, color='orange', label="Response from UCID-16372")
# splt.plot(new_ne213_eb, old_ne213_interp,
#              'o-', ms=2, color='y',
#              label=r"Interpolation old")
splt.set_ylabel(r"Response (A$\epsilon$) [%]")
splt.set_title("Response of NE213 detector")
splt.set_xlabel("Energy [MeV]")
splt.legend()
plt.savefig("NE213_responses_vs_energy.png")


# Et en fonction du temps
fig, splt = plt.subplots(2, sharex=True,
                         gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
splt[0].plot(time_from_old_ne213_30deg, old_ne213_resp,
             's-', ms=5, color='m', label="Old response")
splt[0].plot(time_from_new_ne213_30deg, old_ne213_interp,
             '--', color='plum', label="Old response interpolated")
splt[0].plot(time_from_new_ne213_30deg, new_ne213_resp*ne213_factor,
             'o-', ms=2, mfc="none", color='c',
             label=r"Response in MCNP renormalised")
splt[0].plot(time_from_new_ne213_30deg, ne213_ucid16372_resp,
             'o-', ms=2, color='orange', label="Response from UCID-16372")
splt[0].set_ylabel(r"Response (A$\epsilon$) [%]")
splt[0].set_title("Response of NE213 detector")
splt[0].legend()
splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
ratio =  ne213_ucid16372_resp[1:]/ old_ne213_interp[1:]
splt[1].plot(time_from_new_ne213_30deg[1:], ratio,
             'ro-', ms=3, label="New / old interpolated")
splt[1].set_ylim(ymax=1 + (1-np.min(ratio)))
splt[1].set_ylabel("Ratio")
splt[1].set_xlabel("Time [ns]")
splt[1].legend()
plt.savefig("NE213_responses_vs_time.png")


pilotb_ucid16372_eb, pilotb_ucid16372_resp = read_from_UCID_16372("pilotb_UCID-16372.txt")

fig, splt = plt.subplots(1)
splt.plot(old_pilotb_eb, old_pilotb_resp,
          's-', ms=5, color='m', label="Old response")
splt.plot(new_pilotb_eb, old_pilotb_interp,
          '--', color='plum', label="Old response interpolated")
splt.plot(new_pilotb_eb, new_pilotb_resp*pilotb_factor,
          'o-', ms=2, mfc="none", color='c',
          label=r"Response in MCNP renormalised")
splt.plot(pilotb_ucid16372_eb, pilotb_ucid16372_resp,
          'o-', ms=2, color='orange', label="Response from UCID-16372")
splt.set_ylabel(r"Response (A$\epsilon$) [%]")
splt.set_title("Response of PILOT-B detector")
splt.set_xlabel("Energy [MeV]")
splt.legend()
plt.savefig("PILOT-B_responses_vs_energy.png")


# Et en fonction du temps
fig, splt = plt.subplots(2, sharex=True,
                         gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
splt[0].plot(time_from_old_pilotb_30deg, old_pilotb_resp,
             's-', ms=5, color='m', label="Old response")
splt[0].plot(time_from_new_pilotb_30deg, old_pilotb_interp,
             '--', color='plum', label="Old response interpolated")
splt[0].plot(time_from_new_pilotb_30deg, new_pilotb_resp*pilotb_factor,
             'o-', ms=2, mfc="none", color='c',
             label=r"Response in MCNP renormalised")
splt[0].plot(time_from_new_pilotb_30deg, pilotb_ucid16372_resp,
             'o-', ms=2, color='orange', label="Response from UCID-16372")
splt[0].set_ylabel(r"Response (A$\epsilon$) [%]")
splt[0].set_title("Response of PILOT-B detector")
splt[0].legend()
splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
ratio = pilotb_ucid16372_resp[1:] / old_pilotb_interp[1:]
splt[1].plot(time_from_new_pilotb_30deg[1:], ratio,
             'ro-', ms=3, label="New / old interpolated")
splt[1].set_ylabel("Ratio")
splt[1].set_xlabel("Time [ns]")
splt[1].legend()
plt.savefig("PILOT-B_responses_vs_time.png")



fig, splt = plt.subplots(1)
splt.plot(time_from_new_pilotb_30deg, pilotb_ucid16372_resp,
          'o-', ms=2, color='C0', label="PILOT-B")
splt.plot(time_from_new_ne213_30deg, ne213_ucid16372_resp,
          'o-', ms=2, color='C1', label="NE213")
splt.set_ylabel(r"Response (A$\epsilon$) [%]")
splt.set_title("Detector responses")  # from UCID-16372
splt.set_xlabel("Time [ns]")
splt.legend()
plt.savefig("detector_responses_vs_time.png")

fig, splt = plt.subplots(1)
splt.plot(pilotb_ucid16372_eb, pilotb_ucid16372_resp,
          'o-', ms=2, color='C0', label="PILOT-B")
splt.plot(ne213_ucid16372_eb, ne213_ucid16372_resp,
          'o-', ms=2, color='C1', label="NE213")
splt.set_ylabel(r"Response (A$\epsilon$) [%]")
splt.set_title("Detector responses")  # from UCID-16372
splt.set_xlabel("Energy [MeV]")
splt.legend()
plt.savefig("detector_responses_vs_energy.png")

# num_ne213_interp = np.interp(new_ne213_eb, num_ne213_eb1, num_ne213_resp1)
# ofile2 = open("ne213_digitized_response.txt", 'w')
# ofile2.write("NE213\n")
# for ind, ebin in enumerate(new_ne213_eb):
#     ofile2.write("{0:>15}{1:.1f}   {2:.4f}\n"
#                  .format(" ", ebin, num_ne213_interp[ind]))
# ofile2.close()
ofile2 = open("ucid_response.txt", 'w')
ofile2.write("NE213\n")
for ind, ebin in enumerate(new_ne213_eb):
    ofile2.write("{0:>15}{1:.1f}   {2:.4f}\n"
                 .format(" ", ebin, ne213_ucid16372_resp[ind]))
ofile2.write("\n")
ofile2.write("PILOT-B\n")
for ind, ebin in enumerate(new_pilotb_eb):
    ofile2.write("{0:>15}{1:.1f}   {2:.4f}\n"
                 .format(" ", ebin, pilotb_ucid16372_resp[ind]))
ofile2.close()

# splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
# ratio = new_ne213_resp[1:]*ne213_factor / old_ne213_interp[1:]
# splt[1].plot(new_ne213_eb[1:], ratio,
#              'ro-', ms=3, label="New / old interpolated")
# splt[1].set_ylim(ymax=1 + (1-np.min(ratio)))
# splt[1].set_ylabel("Ratio")
# splt[1].set_xlabel("Energy [MeV]")
# splt[1].legend()
# plt.show()
