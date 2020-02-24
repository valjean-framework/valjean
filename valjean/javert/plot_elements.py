'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from .. import LOGGER
from .templates import PlotTemplate, CurveElements, join, PlotNDTemplate
from .verbosity import Verbosity


# turn off pylint warnings about invalid names in this file; there are just too
# many long function names and they cannot be renamed because
# javert.representation looks for them by programmatically constructing their
# name based on the name of the test result class, the verbosity, etc.
# pylint: disable=invalid-name


def dimension_from_array(array_shape):
    '''Check if array is consistent with 1D plot.

    Checks are done on presence of non-trivial and trivial dimensions, trivial
    being a dimension with size equal to one, non-trivial being for a dimension
    with at least two values.

    :param tuple(int) array_shape: shape of the **values** array
    :returns: index of the chosen dimension in the tuple of array shape
    :rtype: int
    '''
    non_trivial_dims = tuple(d for d, s in enumerate(array_shape) if s > 1)
    LOGGER.warning("Non-trivial dimensions: %s", non_trivial_dims)
    if len(non_trivial_dims) > 1:
        LOGGER.warning("More than one non-trivial dimensions, N-dimensions "
                       "should be required or a dataset slice.")
        if len(non_trivial_dims) == 2:
            return non_trivial_dims
        return None
    if not non_trivial_dims:
        LOGGER.debug("Only trivial dimensions, you may prefer a different "
                     "kind of plot (PlotPoint).")
        return None
    return non_trivial_dims[0]


def dimension(bins, array_shape):
    '''Determine the x-dimension of the result from the
    :obj:`collections.OrderedDict` of bins. It is expected to be the "only
    non-trivial" dimension.

    :param bins: bins coming from the results dataset
    :type bins: :obj:`collections.OrderedDict` (:class:`str`,
        :obj:`numpy.ndarray`)
    :param tuple(int) array_shape: shape of the **values** array from the
        results dataset
    :returns: dimension to be used
    :rtype: str
    '''
    idim = dimension_from_array(array_shape)
    lbins = list(bins.keys())
    if not isinstance(idim, tuple):
        dim_name = lbins[idim] if idim is not None else None
        LOGGER.debug("Used dimension: %s among %s", dim_name, lbins)
    else:
        dim_name = [lbins[i] for i in idim]
        print(dim_name)
    return dim_name


def repr_testresultstudent(result, verbosity=None):
    '''Plot the Student results according to verbosity.

    :param  result: a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: Representation of a :class:`~.TestResultStudent` as a plot.
    :rtype: :class:`list` (:class:`~.PlotTemplate`)
    '''
    LOGGER.debug("PLOT student repr, %s, res = %s", verbosity, bool(result))
    # faire une condition sur le bool dans le cas de SUMMARY ?
    if verbosity in (Verbosity.SILENT, Verbosity.SUMMARY):
        return []
    if verbosity is None or verbosity == Verbosity.INTERMEDIATE:
        return repr_student_intermediate(result)
    if verbosity.value >= Verbosity.FULL_DETAILS.value:
        return repr_student_full_details(result)
    return repr_student_intermediate(result)


def repr_student_intermediate(result):
    '''Represent the Student test result as a plot.

    By default two :class:`~.templates.PlotTemplate` are returned in order to
    get a top plot representing the two series of values and the bottom plot
    representing the Δ from the Student test.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.PlotTemplate`)
    '''
    rval = repr_student_values(result)
    rdelta = repr_student_delta(result)
    rstudent = [join(rvals, rdelta)
                for rvals, rdelta in zip(rval, rdelta)]
    if not rstudent and rval:
        rstudent = rval
    return rstudent


def repr_student_full_details(result):
    '''Represent the Student test result as a plot.

    By default two :class:`~.templates.PlotTemplate` are returned in order to
    get a top plot representing the two series of values and the bottom plot
    representing the Δ from the Student test.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.PlotTemplate`)
    '''
    LOGGER.debug('in repr_student_full_details')
    rval = repr_student_values(result)
    rdelta = repr_student_delta(result)
    rpval = repr_student_pvalues(result)
    rstudent = [join(rvals, rdelta, rpvals)
                for rvals, rdelta, rpvals in zip(rval, rdelta, rpval)]
    if not rstudent and rval:
        rstudent = rval
    return rstudent


def repr_student_delta(result):
    '''Represent the Δ distribution from a Student test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.PlotTemplate`)

    .. note::
        if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.

    If the dimension cannot be determined an empty list is returned.
    '''
    dim = dimension(result.test.dsref.bins, result.test.dsref.value.shape)
    if dim is None:
        return []
    if not isinstance(dim, str):
        return []
    bins = result.test.dsref.bins[dim]
    curves = []
    for ind, delta in enumerate(result.delta):
        curves.append(CurveElements(
            values=delta,
            label=' '.join([(result.test.datasets[ind].name
                             if result.test.datasets[ind].name
                             else 'dataset '+str(ind)), 'vs', 'reference']),
            index=ind+1, yname=r'$t_{Student}$', errors=None))
    return [PlotTemplate(bins=bins, xname=dim, curves=curves)]


def repr_student_values(result):
    '''Represent the values distributions from a Student test result as a plot
    (both distributions expected to be on the same plot).

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.PlotTemplate`)

    .. note::
        if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.

    If the dimension cannot be determined an empty list is returned.
    '''
    dim = dimension(result.test.dsref.bins, result.test.dsref.value.shape)
    if dim is None:
        LOGGER.debug('value: dim is None')
        return []
    cds = [CurveElements(values=result.test.dsref.value,
                         label=(result.test.dsref.name
                                if result.test.dsref.name else 'reference'),
                         index=0, yname='', errors=result.test.dsref.error)]
    for ids, tds in enumerate(result.test.datasets):
        cds.append(CurveElements(
            values=tds.value,
            label=(tds.name if tds.name else 'dataset '+str(ids)),
            index=ids+1, yname='', errors=tds.error))
    if not isinstance(dim, str):
        bins = (result.test.dsref.bins
                if len(result.test.dsref.bins) == len(dim)
                else [result.test.dsref.bins[d] for d in dim])
        if result.test.dsref.value.ndim != len(bins):
            LOGGER.warning('Bins and values have different dimensions, '
                           'consider squeezing dataset before plotting.')
            return []
        return [PlotNDTemplate(bins=bins, curves=cds)]
    bins = result.test.dsref.bins[dim]
    return [PlotTemplate(bins=bins, xname=dim, curves=cds)]


def repr_student_pvalues(result):
    '''Representation of p-values from Student test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.templates.PlotTemplate`)

    If p-values were not calculated, no :class:`~.PlotTemplate` is built, so
    an empty list is returned.
    '''
    if result.pvalue is None:
        LOGGER.debug("p-value is None, won't be possible to plot it.")
        return []
    dim = dimension(result.test.dsref.bins, result.test.dsref.value.shape)
    if dim is None:
        return []
    if not isinstance(dim, str):
        return []
    bins = result.test.dsref.bins[dim]
    curves = []
    for ind, pval in enumerate(result.pvalue):
        curves.append(CurveElements(
            values=pval,
            label=' '.join([(result.test.datasets[ind].name
                             if result.test.datasets[ind].name
                             else 'dataset '+str(ind)), 'vs', 'reference']),
            index=ind+1, yname='p-value', errors=None))
    return [PlotTemplate(bins=bins, xname=dim, curves=curves)]


def repr_datasets_values(result):
    '''Representation of the datasets values from test results like
    :class:`~valjean.gavroche.test.TestResultEqual` or
    :class:`~valjean.gavroche.test.TestResultApproxEqual`, i.e. all tests
    containing a ``dataset1`` and a ``dataset2`` members.

    :param result: test result
    :type result: :class:`~valjean.gavroche.test.TestResultEqual`,
        :class:`~valjean.gavroche.test.TestResultApproxEqual`
    :returns: :class:`list` (:class:`~.PlotTemplate`)

    If the dimension cannot be determined an empty list is returned.
    '''
    dim = dimension(result.test.dsref.bins,
                    result.test.dsref.value.shape)
    if dim is None:
        return []
    if not isinstance(dim, str):
        return []
    bins = result.test.dsref.bins[dim]
    cds = [CurveElements(values=result.test.dsref.value,
                         label=(result.test.dsref.name
                                if result.test.dsref.name else 'reference'),
                         index=0, yname='', errors=result.test.dsref.error)]
    cds.extend([CurveElements(values=ds.value,
                              label=(ds.name if ds.name
                                     else 'dataset '+str(ids)),
                              index=ids+1, yname='', errors=ds.error)
                for ids, ds in enumerate(result.test.datasets)])
    LOGGER.info("bins %s", bins)
    return [PlotTemplate(bins=bins, xname=dim, curves=cds)]


def repr_testresultequal(result, _verbosity=None):
    '''Represent the equal test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultEqual`
    :returns: :class:`list` (:class:`~.templates.PlotTemplate`)
    '''
    return repr_datasets_values(result)


def repr_testresultapproxequal(result, _verbosity=None):
    '''Represent the approx equal test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :returns: :class:`list` (:class:`~.templates.PlotTemplate`)
    '''
    return repr_datasets_values(result)


def repr_testresultmetadata(_result, _verbosity=None):
    '''Plot metadata test -> no plot done.'''
    return []


def repr_testresultfailed(_result, _verbosity=None):
    '''Plot failed test -> no plot done.'''
    return []


def repr_testresultstatstestsperflags(_result, _verbosity=None):
    '''Plot statistics on the tests classified per flags -> no plot done.'''
    return []
