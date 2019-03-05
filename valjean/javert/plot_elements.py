'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from .. import LOGGER
from .items import PlotItem, CurveElements, concatenate


def dimension_from_array(array_shape):
    '''Check if array is consistent with 1D plot.

    Checks are done on presence of non-trivial and trivial dimensions, trivial
    being a dimension with size equal to one, non-trivial being for a dimension
    with at least two values.

    :param tuple(int) array_shape: shape of the **values** array
    :returns: index of the chosen dimension in the tuple of array shape
    :rtype: int
    :raises: TypeError if more than one non-trivial dimensions or only trivial
        dimensions and more than one.
    '''
    non_trivial_dims = tuple(d for d, s in enumerate(array_shape) if s > 1)
    LOGGER.debug("Non-trivial dimensions: %s", str(non_trivial_dims))
    if len(non_trivial_dims) > 1:
        raise TypeError("More than one non-trivial dimensions, N-dimensions "
                        "should be required or a dataset slice.")
    if not non_trivial_dims:
        LOGGER.info("Only trivial dimension, you may prefer a different kind "
                    "of plot (PlotPoint).")
        if len(array_shape) > 1:
            raise TypeError("Only trivial dimensions and more than one trivial"
                            " dimensions, no dimension choice possible.")
        return 0
    return non_trivial_dims[0]


def dimension(bins, array_shape):
    '''Determine the x-dimension of the result from the :class:`OrderedDict` of
    bins. It is expected to be the "only non-trivial" dimension.

    :param bins: bins coming from the results dataset
    :type bins: :obj:`collections.OrderedDict` (str, :obj:`numpy.ndarray`)
    :param tuple(int) array_shape: shape of the **values** array from the
        results dataset
    :returns: dimension to be used
    :rtype: str
    '''
    idim = dimension_from_array(array_shape)
    dim_name = list(bins.keys())[idim]
    LOGGER.debug("Used dimension: %s among %s", dim_name,
                 str(list(bins.keys())))
    return dim_name


def repr_testresultstudent(result):
    '''Represent the Student test result as a plot.

    Per default two :class:`PlotItem` are returned in order to get a top plot
    representing the two series of values and the bottom plot representing the
    Δ from the Student test.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: list( :class:`PlotItem`)
    '''
    return concatenate(repr_student_values(result)
                       + repr_student_delta(result))


def repr_student_delta(result):
    '''Represent the Δ distribution from a Student test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: list( :class:`PlotItem`)

    .. note::
        if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.
    '''
    dim = dimension(result.test.ds1.bins, result.test.ds1.value.shape)
    bins = result.test.ds1.bins[dim]
    curve = CurveElements(values=result.delta, label=result.test.name,
                          yname=r'$\Delta_{Student}$', errors=None)
    return [PlotItem(bins=bins, xname=dim, curves=[curve])]


def repr_student_values(result):
    '''Represent the values distributions from a Student test result as a plot
    (both distributions expected to be on the same plot).

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: list( :class:`PlotItem`)

    .. note::
        if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.
    '''
    dim = dimension(result.test.ds1.bins, result.test.ds1.value.shape)
    bins = result.test.ds1.bins[dim]
    cds1 = CurveElements(values=result.test.ds1.value,
                         label=result.test.name+': dataset 1', yname='',
                         errors=result.test.ds1.error)
    cds2 = CurveElements(values=result.test.ds2.value,
                         label=result.test.name+': dataset 2', yname='',
                         errors=result.test.ds2.error)
    return [PlotItem(bins=bins, xname=dim, curves=[cds1, cds2])]


def repr_student_pvalues(result):
    '''Representation of p-values from Student test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: list( :class:`PlotItem`)
    :raises: ValueError if p-value is None
    '''
    if result.pvalue is None:
        raise ValueError("p-value is None, won't be possible to plot it.")
    dim = dimension(result.test.ds1.bins, result.test.ds1.value.shape)
    bins = result.test.ds1.bins[dim]
    curve = CurveElements(values=result.pvalue,
                          label=result.test.name, yname='p-value', errors=None)
    return [PlotItem(bins=bins, xname=dim, curves=[curve])]


def repr_datasets_values(result):
    '''Representation of the datasets values from test results like
    :class:`TestResultEqual` or :class:`TestResultApproxEqual`, i.e. all tests
    containing a ``dataset1`` and a ``dataset2`` members.

    :param result: test result
    :type result: :class:`TestResultEqual`, :class:`TestResultApproxEqual`
    :returns: list( :class:`PlotItem`)
    '''
    dim = dimension(result.test.dataset1.bins,
                    result.test.dataset1.value.shape)
    bins = result.test.dataset1.bins[dim]
    cds1 = CurveElements(values=result.test.dataset1.value,
                         label=result.test.name+': dataset 1', yname='',
                         errors=result.test.dataset1.error)
    cds2 = CurveElements(values=result.test.dataset2.value,
                         label=result.test.name+': dataset 2', yname='',
                         errors=result.test.dataset2.error)
    return [PlotItem(bins=bins, xname=dim, curves=[cds1, cds2])]


def repr_testresultequal(result):
    '''Represent the equal test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultEqual`
    :returns: list( :class:`PlotItem`)
    '''
    return repr_datasets_values(result)


def repr_testresultapproxequal(result):
    '''Represent the approx equal test result as a plot.

    :param result:  a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :returns: list( :class:`PlotItem`)
    '''
    return repr_datasets_values(result)
