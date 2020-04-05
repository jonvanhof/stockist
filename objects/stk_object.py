class stk_object():
    def __init__(self, data_store, ext_sources, models, filter_crit=None):
	    self.ds = data_store
        self.src = ext_sources
        self.mdl = models
        self.crit = filter_crit

    def 