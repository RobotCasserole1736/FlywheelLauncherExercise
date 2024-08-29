class ExpFilter:
    def __init__(self, alpha):
        """
        Initialize the Exponential Smoothing filter.

        :param alpha: Smoothing factor between 0 and 1.
        """
        if not (0 < alpha < 1):
            raise ValueError("Alpha must be between 0 and 1.")
        
        self.alpha = alpha
        self.prev_y = 0  # Previous output sample

    def smooth(self, x):
        """
        Apply exponential smoothing to the input sample.

        :param x: Current input sample.
        :return: Smoothed output sample.
        """
        y = self.alpha * x + (1 - self.alpha) * self.prev_y
        
        # Update previous value
        self.prev_y = y
        
        return y