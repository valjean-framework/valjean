Vaches sphériques
=================

Cet exemple présente une implémentation simplifiée d'un job ``valjean`` pour la
comparaison systématique de TRIPOLI-4® et MCNP sur des systèmes très simples :
des sphères contenant un seul isotope et une source de neutrons
monoénergétiques placée au centre. Nous calculons le flux neutron intégré sur
la sphère et découpé à 616 groupes.

Note : cet exemple est censé être exécuté par l'exécutable ``valjean``.

Fichier ``job.py``
------------------

Imports
~~~~~~~

.. code:: python

    import os
    from pathlib import Path
    
    from valjean.cosette.run import RunTaskFactory
    from valjean.cosette.task import TaskStatus
    from valjean.cosette.pythontask import PythonTask
    from valjean.eponine.tripoli4.parse import Parser
    from valjean.eponine.tripoli4.data_convertor import convert_data
    from valjean.gavroche.stat_tests.student import TestStudent
    from valjean.gavroche.stat_tests.bonferroni import TestHolmBonferroni
    from valjean.javert.test_report import TestReport
    from valjean.javert.representation import Representation, FullRepresenter
    from valjean.javert.rst import RstTestReportTask
    import mcnp  # module auxiliaire de lecture de fichiers MCTAL, pas inclus dans valjean

Définitions des chemins et des paramètres
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    JOB_PATH = Path(__file__)
    
    # paramètres pour TRIPOLI-4
    T4_EXE = '/path/to/bin/tripoli4'
    T4_PATH = '/path/to/t4path'
    
    # paramètres pour MCNP
    MCNP_EXE = '/path/to/bin/mcnp6'
    MCNP_DATAPATH = '/path/to/MCNP_DATA'
    MCNP_XSDIR = '/path/to/MCNP/xsdir'
    os.environ['DATAPATH'] = MCNP_DATAPATH
    
    TABPROB = True        # utiliser les tables de probabilités ?
    N_HISTORIES = 100000  # nombre d'histoires à simuler

Systèmes à tester
~~~~~~~~~~~~~~~~~

On définit ici une liste de nucléides à étudier.

.. code:: python

    #             ┌────────────────────────────────────── noyau
    #             │          ┌─────────────────────────── nom noyau TRIPOLI-4
    #             │          │       ┌─────────────────── code noyau MCNP (ZZZAAA)
    #             │          │       │     ┌───────────── énergie (MeV)
    #             │          │       │     │    ┌──────── température (K)
    #             │          │       │     │    │      ┌─ concentration en 1/(b cm²)
    #             v          v       v     v    v      v
    SYSTEMS = [('O16',     'O16',  8016, 14.0, 294, 1.527e-1),
               ('U235',   'U235', 92235, 14.0, 294, 4.549e-3),
               ('Pu239', 'PU239', 94239, 14.0, 294, 4.590e-3)]

Définition de la fonction ``job()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cette fonction définit le travail à exécuter par ``valjean``. On va
déclarer les tâches et les dépendances entre elles, et ``valjean`` va
s'occuper du lancement. Il existe des types de tâches différentes.

.. code:: python

    def job():
        # On crée une classe utilitaire pour générer des tâches qui
        # exécutent TRIPOLI-4. Les options de la ligne de commande T4
        # sont paramétrées par des mot-clés.
        t4_args = ['-s', '{fmt}', '-d', '{input_file}', '-c', '{t4path}',
                   '-l', '{language}', '-a', '-u']
        t4_fac = RunTaskFactory.from_executable(T4_EXE, name='t4',
                                                default_args=t4_args,
                                                t4path=T4_PATH,
                                                language='english')
    
        # On fait la même chose pour MCNP.
        mcnp_args = ['i={input_file}', 'xs={xsdir}', 'o={output_file}']
        mcnp_fac = RunTaskFactory.from_executable(MCNP_EXE,
                                                  name='mcnp',
                                                  default_args=mcnp_args,
                                                  xsdir=MCNP_XSDIR)
    
        # Voici la liste des tâches de comparaison TRIPOLI-4 vs. MCNP
        # à exécuter. La fonction make_comparison_task() apparaît
        # ci-dessous.
        tasks = [make_comparison_task(system, t4_fac, mcnp_fac)
                 for system in SYSTEMS]
    
        # Les tâches de comparaison vont générer des résultat de tests statistiques.
        # On va les transformer en rapport HTML, via un format intermédiaire
        # (reStructuredText, une sorte de Markdown).
        my_repr = Representation(FullRepresenter())
        # La construction du rapport de test est aussi une tâche valjean ! La seule
        # ligne mystérieuse est...
        report_task = RstTestReportTask.from_tasks(name='report',
                                                   make_report=make_report, # celle-ci
                                                   eval_tasks=tasks,
                                                   representation=my_repr,
                                                   author='Davide Mancusi',
                                                   version='0.0.1',
                                                   kwargs={'title': 'Spherical cows'})
        # Ici make_report est une fonction qui décrit comment organiser les résultats
        # de test en sections. Dans notre cas, elle va être très simple.
    
        # On renvoie uniquement la tâche de construction du rapport. Elle dépend
        # implicitement des tâches de comparaison, qui dependent des tâches d'exécution
        # de TRIPOLI-4 et MCNP...
        return [report_task]

Comparaison TRIPOLI-4/MCNP pour un système donné
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cette fonction prépare les jeux de données TRIPOLI-4 et MCNP en remplissant les
cases vides de fichiers templates (:download:`TRIPOLI-4 <templates/t4>`,
:download:`MCNP <templates/mcnp>`).

.. code:: python

    def make_comparison_task(system, t4_fac, mcnp_fac):
        
        # On déballe le tuple qui décrit le système
        nucleus, t4_nucleus, zaid, energy, temperature, conc = system
        nuc_id = str(zaid)
    
        input_path = JOB_PATH.with_name('input') / f'{nucleus}_{energy}'
        input_path.mkdir(parents=True, exist_ok=True)
    
        # On crée le jeu de données pour TRIPOLI-4 à partir des paramètres du
        # système et d'un jeu de données "template".
        t4_input_path = input_path / 't4'
        format_t4_input(t4_input_path, nucleus=t4_nucleus, concentration=conc,
                        n_histories=N_HISTORIES, temperature=temperature,
                        energy=energy)
    
        # On fait la même chose pour MCNP
        mcnp_input_path = input_path / 'mcnp'
        mcnp_output_path = 'mcnp.out'
        format_mcnp_input(mcnp_input_path, nucleus=nucleus, concentration=conc,
                          nuc_id=nuc_id, tabprob=TABPROB,
                          n_histories=N_HISTORIES, temperature=temperature,
                          energy=energy)
        
        # Les fonctions format_t4_input() et format_mcnp_input() apparaîssent
        # plus bas.
    
        # Voici les tâches qui vont exécuter TRIPOLI-4 et MCNP
        t4_fmt = 'TABPROB' if TABPROB else 'NJOY'
        t4_task = t4_fac.make(input_file=str(t4_input_path), fmt=t4_fmt,
                              name=f'{nucleus}@{energy}')
        mcnp_task = mcnp_fac.make(input_file=str(mcnp_input_path),
                                  output_file=str(mcnp_output_path),
                                  name=f'{nucleus}@{energy}')
    
        # Et voici la tâche de comparaison entre le résultat de TRIPOLI-4 et
        # celui de MCNP. La tâche consiste à appeler une fonction appelée
        # compare(), qui apparaitra dans la suite
        task_name = f'comparison {nucleus}_{energy}'
        compare_task = PythonTask(task_name,
                                  compare,  # voici la fonction à appeler
                                  env_kwarg='env',
                                  # voici les arguments à passer à compare()
                                  kwargs={'nucleus': nucleus,
                                          'energy': float(energy),
                                          't4_name': t4_task.name,
                                          'task_name': task_name,
                                          'mcnp_name': mcnp_task.name},
                                  # on déclare que cette tâche dépend de t4_task et mcnp_task
                                  deps=[t4_task, mcnp_task])
        return compare_task

Que fait la fonction de comparaison? Elle lit le listing de sortie
TRIPOLI-4 et celui de MCNP, extrait les flux neutron multigroupe et fait
un test statistique de compatibilité entre les deux.

.. code:: python

    def compare(*, t4_name, mcnp_name, task_name, nucleus, energy, env):
        mcnp_mctal = Path(env[mcnp_name]['result']).with_name('mctal')
        mcnp_ds = mcnp.MCTALResult(str(mcnp_mctal)).result(4, 1)
        mcnp_ds.name = mcnp_name
    
        t4_out = Path(env[t4_name]['result'])
        t4_br = Parser(t4_out).parse_from_index().to_browser()
        t4_res = t4_br.select_by(score_name='flux_score')['results']
        t4_ds = (convert_data(t4_res, 'spectrum', name=t4_name, what='flux')
                 .squeeze())
    
        test = TestHolmBonferroni(test=TestStudent(t4_ds, mcnp_ds, name=nucleus),
                                  name=f'Holm-Bonferroni test, {nucleus} '
                                       f'@ {energy} MeV',
                                  labels={'nucleus': nucleus,
                                          'energy': energy})
        test_result = test.evaluate()
        return {task_name: {'result': [test_result]}}, TaskStatus.DONE

Fonctions auxiliaires
~~~~~~~~~~~~~~~~~~~~~

Le reste, c'est de la bureaucratie. La fonction qui génère le jeu de
données TRIPOLI-4 ne fait que lire le template et remplir les cases
vides.

.. code:: python

    def format_t4_input(output_path, *, n_batch=200, temperature, n_histories,
                        **kwargs):
        template_path = JOB_PATH.with_name('templates') / 't4'
        template = template_path.read_text()
        batch_size = max(1, n_histories // n_batch)
        edition = max(1, n_batch // 10)
        content = template.format(batch_size=batch_size, n_batch=n_batch,
                                  temperature=int(temperature), edition=edition,
                                  **kwargs)
        Path(output_path).write_text(content)

La fonction MCNP est très similaire.

.. code:: python

    def format_mcnp_input(output_path, *, tabprob, temperature, **kwargs):
        boltzmann = 8.617341e-11  # MeV/K
        temperature_MeV = temperature*boltzmann
        template_path = JOB_PATH.with_name('templates') / 'mcnp'
        template = template_path.read_text()
        tabprob_int = 0 if tabprob else 1
        content = template.format(tabprob=tabprob_int, temperature=temperature_MeV,
                                  **kwargs)
        Path(output_path).write_text(content)

Voici enfin la fonction ``make_report()``, qui organise les résultats de
test en sections.

.. code:: python

    def make_report(all_test_results, *, title):
        # Ici all_test_results est un dictionnaire qui associe les nom des tâches
        # à des listes de résultats de tests.
        sections = []
        for task_name, test_results in sorted(all_test_results.items()):
            # On récupère le nom du noyau et l'énergie du test pour construire
            # le titre de la page.
            test = test_results[0].test
            nucleus = test.labels['nucleus']
            energy = test.labels['energy']
            section = TestReport(title=f'{nucleus}, {energy} MeV',
                                 content=test_results)
            sections.append(section)
    
        report = TestReport(title=title,
                            content=[TestReport(title='Test results',
                                                text='Here is the good stuff.',
                                                content=sections)])
        return report

Exécution
---------

Voici ce qui se passe quand on exécute le job avec ``valjean`` dans un
terminal :

.. code:: console

    $ valjean run job.py
    * graphs built in 0.6359915770590305 seconds
    * hard_graph contains 11 tasks
    * soft_graph contains 11 tasks
    * will schedule up to 4 tasks in parallel
    * deserializing pickle environment from 'valjean.env' files in /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/output
    * 0 environment files found and deserialized
    * graph completed in 1.5154480934143066e-05 seconds
    * graph completed in 1.0513700544834137e-05 seconds
    * hard graph copied in 0.00017551984637975693 seconds
    * hard graph flattened in 1.2297183275222778e-05 seconds
    * graph completed in 9.783543646335602e-06 seconds
    * full graph computed in 0.00023496989160776138 seconds
    * full graph flattened in 9.047798812389374e-06 seconds
    * scheduling tasks
    * full graph sorted in 6.301887333393097e-05 seconds
    * master: 11 tasks left
    * master: 5 tasks left
    * task 'U235@14.0.t4' starts
    * task 'U235@14.0.mcnp' starts
    * task 'O16@14.0.mcnp' starts
    * task 'O16@14.0.t4' starts
    * task 'U235@14.0.mcnp' completed with status TaskStatus.DONE
    * task 'Pu239@14.0.t4' starts
    * master: 5 tasks left
    * task 'O16@14.0.mcnp' completed with status TaskStatus.DONE
    * task 'Pu239@14.0.mcnp' starts
    * master: 5 tasks left
    * task 'U235@14.0.t4' completed with status TaskStatus.DONE
    * master: 5 tasks left
    * master: 4 tasks left
    * task 'comparison U235_14.0' starts
    * Parsing /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/output/U235@14.0.t4/stdout
    * Successful scan in 0.017888 s
    * Successful parsing in 0.130465 s
    * task 'Pu239@14.0.mcnp' completed with status TaskStatus.DONE
    * master: 4 tasks left
    * task 'comparison U235_14.0' completed with status TaskStatus.DONE
    * master: 4 tasks left
    * task 'Pu239@14.0.t4' completed with status TaskStatus.DONE
    * master: 4 tasks left
    * master: 3 tasks left
    * task 'comparison Pu239_14.0' starts
    * Parsing /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/output/Pu239@14.0.t4/stdout
    * Successful scan in 0.029409 s
    * Successful parsing in 0.129308 s
    * task 'comparison Pu239_14.0' completed with status TaskStatus.DONE
    * master: 3 tasks left
    * task 'O16@14.0.t4' completed with status TaskStatus.DONE
    * master: 3 tasks left
    * master: 2 tasks left
    * task 'comparison O16_14.0' starts
    * Parsing /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/output/O16@14.0.t4/stdout
    * Successful scan in 0.027760 s
    * Successful parsing in 0.093801 s
    * task 'comparison O16_14.0' completed with status TaskStatus.DONE
    * master: 2 tasks left
    * master: 1 tasks left
    * task 'report-report' starts
    * task 'report-report' completed with status TaskStatus.DONE
    * master: 1 tasks left
    * task 'report' starts
    * writing tree_path: /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/index
    * writing tree_path: /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/Test results
    * writing tree_path: /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/Test results/O16, 14.0 MeV
    * writing tree_path: /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/Test results/Pu239, 14.0 MeV
    * writing tree_path: /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/Test results/U235, 14.0 MeV
    * writing 3 plots using 4 subprocesses
    /data/tmpdm2s/dm232107/src/valjean/valjean/gavroche/stat_tests/student.py:478: RuntimeWarning: invalid value encountered in true_divide
      studentt = diff.value / diff.error
    * drawing figure /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/figures/plot_cc240cbb3a9ae844616da16989931f4a21578e75aa8b9b3d895d36b2247ac7fd.png
    * drawing figure /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/figures/plot_9589d583b0b1af6b1ff2ec2aefcc88deda3ee5cec98d1a25c487e247c5aeaf52.png
    * drawing figure /data/tmpdm2s/dm232107/src/valjean-demo/spherical_cows/report/report/figures/plot_1f8ae35814f479a1b25ba26f0e810126875b2a1cfb5ce3d2bb23bcd4f2de6f9a.png
    * task 'report' completed with status TaskStatus.DONE
    * final environment statistics:
         DONE: 11/11 (100.0%)
    * serializing pickle environment to 'valjean.env' files
    * 7 environment files written

Un rapport au format RST a été généré dans ``report/report``. Je le
convertis en HTML avec ``sphinx`` :

.. code:: console

    $ sphinx-build -j30 -a -bhtml report/report report/html
