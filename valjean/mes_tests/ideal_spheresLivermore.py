jdd1 = sphere
jdd2 = air
jdd3 = mcnp
jdd4 = experience

t4res = jdd1/jdd2
graph(t4res, experience, jdd3)


# en ce moment:
from spheresLivermore import Comparison
# initialisation de la comparaison, ici = lecture des données expérimentales
comp = Comparison()
# ajout des fichiers T4
comp.set_t4_files(
    [("Old",
      "/data/tmplepp/el220326/RunTripoli/spheresLivermore/"
      "PARA/ceav5/prob102_carbone2.9_fine.SPHAIR.d.res"),
     ("New ceav5",
      "/data/tmplepp/el220326/RunTripoli/spheresLivermore/"
      "PARA/ceav5/mon_test/prob102_carboneNat2.9_fine.SPHAIR.d.res"),
     ("New endf7r1",
      "/data/tmplepp/el220326/RunTripoli/spheresLivermore/"
      "PARA/endbf71/prob102_carboneNat2.9_fine.SPHAIR.d.res")])
# possibilité d'ajouter autant de fichiers que l'on veut
# ajout des fichiers MCNP, mais que les données expérimentales pour le moment
# A prévoir : changement dans les outputs si résultats...
comp.set_mcnp_files("/data/tmplepp/el220326/RunTripoli/spheresLivermore/"
                    "MCNP/lps_carbon.expt", "Carbon_30deg")
comp.compare_plots(
    ('CARBON', '2.9', '30'),
    # identification par index de reponse
    {"Old": "[0, 1]",
     # identification par score name
     "ceav5": "['neutron_response_30deg', 'neutron_response_integral_30deg']",
     "endf7r1": "['neutron_response_30deg', 'neutron_response_integral_30deg']"
    },
    # non obligatoire : MCNP
    "Carbon_30deg")
