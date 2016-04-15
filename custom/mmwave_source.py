import warnings
class MMWaveSource(object):
    name = 'mmwave_source'
    def __init__(self):
        self._state = dict(multiplier_input = None, ttl_modulation_source=None, multiplier_factor=12.0,
                           before_multiplier = None, after_multiplier = 'bpf_140_160_GHz', waveguide_twist_angle = None)
        self._required_keys = ['multiplier_input', 'ttl_modulation_source', 'waveguide_twist_angle', 'mickey_ticks',
                               'minnie_ticks']
        self.ticks_per_turn = 25.

    @property
    def state(self):
        for key in self._required_keys:
            if self._state[key] is None:
                raise RuntimeError("You must set the state of these properties before requesting state: "
                                   + ' '.join(self._required_keys))
        return self._state

    def set_attentuator_ticks(self,mickey,minnie):
        self._state['mickey_ticks'] = mickey
        self._state['minnie_ticks'] = minnie

    def set_attenuator_turns(self,mickey,minnie):
        self.set_attentuator_ticks(mickey*self.ticks_per_turn,minnie*self.ticks_per_turn)

    @property
    def multiplier_input(self):
        return self._state['multiplier_input']

    @multiplier_input.setter
    def multiplier_input(self,value):
        if value in ['hittite','thermal']:
            self._state['multiplier_input'] = value
        else:
            raise ValueError("Invalid multiplier input, must be 'hittite' or 'thermal'")

    @property
    def ttl_modulation_source(self):
        return self._state['ttl_modulation_source']

    @ttl_modulation_source.setter
    def ttl_modulation_source(self,value):
        if value in ['roach','roach_1','roach_2','function_generator']:
            self._state['ttl_modulation_source'] = value
        else:
            raise ValueError("Invalid ttl modulation source, must be roach, roach_1, roach_2, or function_generator")

    @property
    def before_multiplier(self):
        """
        Catch-all for items before the multiplier (i.e. pin_attenuator, 11 GHz narrow filter, etc.)
        Returns
        -------

        """
        return self._state['before_multiplier']

    @before_multiplier.setter
    def before_multiplier(self,value):
        self._state['before_multiplier'] = value

    @property
    def after_multiplier(self):
        """
        Catch-all for items after the multiplier. Default is the Pacific mm-wave 140-160 GHz bandpass filter
        Returns
        -------

        """
        return self._state['before_multiplier']

    @after_multiplier.setter
    def after_multiplier(self,value):
        self._state['before_multiplier'] = value

    @property
    def waveguide_twist_angle(self):
        return self._state['waveguide_twist_angle']

    @waveguide_twist_angle.setter
    def waveguide_twist_angle(self,value):
        if value not in [0,45,90]:
            warnings.warn("waveguide_twist_angle should probably be 0, 45, or 90 degrees. you have set it to %f" %
                          value)
        self._state['waveguide_twist_angle'] = value