'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from .. import LOGGER
from .templates import PlotTemplate, CurveElements, join


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
    LOGGER.debug("Non-trivial dimensions: %s", non_trivial_dims)
    if len(non_trivial_dims) > 1:
        LOGGER.error("More than one non-trivial dimensions, N-dimensions "
                     "should be required or a dataset slice.")
        return None
    if not non_trivial_dims:
        LOGGER.info("Only trivial dimension, you may prefer a different kind "
                    "of plot (PlotPoint).")
        if len(array_shape) > 1:
            LOGGER.error("Only trivial dimensions and more than one trivial"
                         " dimensions, no dimension choice possible.")
            return None
        return 0
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
    dim_name = list(bins.keys())[idim] if idim is not None else None
    LOGGER.debug("Used dimension: %s among %s", dim_name, list(bins.keys()))
    return dim_name


def repr_testresultstudent(result):
    '''Represent the Student test result as a plot.

    By default two :class:`~.templates.PlotTemplate` are returned in order to
    get a top plot representing the two series of values and the bottom plot
    representing the Δ from the Student test.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.PlotTemplate`)
    '''
    rstudent = [join(rvals, rdelta)
                for rvals, rdelta in zip(repr_student_values(result),
                                         repr_student_delta(result))]
    return rstudent


def repr_student_delta(result):
    '''Represent the Δ distribution from a Student test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.PlotTemplate`)

    .. note::
        if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.

    If the dimension cannot be determined a empty list is returned.
    '''
    dim = dimension(result.test.dsref.bins, result.test.dsref.value.shape)
    if dim is None:
        return []
    bins = result.test.dsref.bins[dim]
    curves = []
    for ind, delta in enumerate(result.delta):
        curves.append(CurveElements(
            values=delta,
            label=' '.join([(result.test.datasets[ind].name
                             if result.test.datasets[ind].name
                             else 'dataset '+str(ind)), 'vs', 'reference']),
            index=ind+1, yname=r'$\Delta_{Student}$', errors=None))
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

    If the dimension cannot be determined a empty list is returned.
    '''
    dim = dimension(result.test.dsref.bins, result.test.dsref.value.shape)
    if dim is None:
        return []
    bins = result.test.dsref.bins[dim]
    cds = [CurveElements(values=result.test.dsref.value,
                         label=(result.test.dsref.name
                                if result.test.dsref.name else 'reference'),
                         index=0, yname='', errors=result.test.dsref.error)]
    for ids, tds in enumerate(result.test.datasets):
        cds.append(CurveElements(
            values=tds.value,
            label=(tds.name if tds.name else 'dataset '+str(ids)),
            index=ids+1, yname='', errors=tds.error))
    return [PlotTemplate(bins=bins, xname=dim, curves=cds)]


def repr_student_pvalues(result):
    '''Representation of p-values from Student test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: :class:`list` (:class:`~.templates.PlotTemplate`)

    If p-values were not calculated, no :class:`~.PlotTemplate` is build, so
    an empty list is returned.
    '''
    if result.pvalue is None:
        LOGGER.error("p-value is None, won't be possible to plot it.")
        return []
    dim = dimension(result.test.dsref.bins, result.test.dsref.value.shape)
    if dim is None:
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

    If the dimension cannot be determined a empty list is returned.
    '''
    dim = dimension(result.test.dsref.bins,
                    result.test.dsref.value.shape)
    if dim is None:
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
    return [PlotTemplate(bins=bins, xname=dim, curves=cds)]


def repr_testresultequal(result):
    '''Represent the equal test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultEqual`
    :returns: :class:`list` (:class:`~.templates.PlotTemplate`)
    '''
    return repr_datasets_values(result)


def repr_testresultapproxequal(result):
    '''Represent the approx equal test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :returns: :class:`list` (:class:`~.templates.PlotTemplate`)
    '''
    return repr_datasets_values(result)
