from pysad.core.base_model import BaseModel
from pysad.stats.median_meter import MedianMeter


class MedianAbsoluteDeviation(BaseModel):

    def __init__(self, absolute=True, b=1.4826):
        """Median Absolute Deviation method :cite:`hochenbaum2017automatic`.

        Args:
            absolute: bool (Default=True)
                Whether to output score's absolute value.
            b: float (Default=1.4826)
                The default value `1.4826` is used for normally distributed data. See :cite:`hochenbaum2017automatic` for details.
        """
        self.b = b
        self.absolute = absolute
        self.median_meter = MedianMeter()
        self.mad_meter = MedianMeter()

    def fit_partial(self, X, y=None):
        """Fits the model to next instance.

        Args:
            X: float
                The instance to fit. Note that this model is univariate.
            y: int (Default=None)
                Ignored since the model is unsupervised.

        Returns:
            self: object
                Returns the self.
        """
        assert len(X) == 1 # Only for time series

        self.median_meter.update(X)
        self.mad_meter.update(X)

    def score_partial(self, X):
        """Scores the anomalousness of the next instance.

        Args:
            X: float
                The instance to score. Higher scores represent more anomalous instances whereas lower scores correspond to more normal instances. Note that this model is univariate.

        Returns:
            score: float
                The anomalousness score of the input instance.
        """
        median = self.median_meter.get()
        mad = self.b*self.mad_meter.get()
        score = (X - median)/mad

        return abs(score) if self.absolute else score