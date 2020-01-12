import random
import numpy as np

def wave_sample(nb_points=240,
                x_range=(0,60),
                wave_profile=None,
                random_seed=None):
    """
    nb_points:
    x_range:
    wave_profile:
        a set of { wave_name : { PROFILE } }
            PROFILE:
                "max":
                "min":
                "cycle":
                "phase":
                "trend":
                "noise":
        default is:
    return:
        a list of { "x": [...], "y": [...], "label": "name" }
    """
    #
    if random_seed is not None:
        random.seed(random_seed)
    #
    if wave_profile is None:
        wave_profile = {}
        for n in [ "A", "B", "C", "D", "E", "F", "G", "H", "I", ]:
            wave_profile.update({
                    n : {
                            "max": 30., "min": -30., "cycle": 12., "phase": 0,
                            "trend": random.uniform(-1., 1),
                            "noise": random.uniform(0,.5) } } )
    #
    sample = []
    for n, p in wave_profile.items():
        ret_x = []
        ret_y = []
        diff = (p["max"] + p["min"]) / 2
        amp = p["max"] - diff
        trend = 0
        for x in np.linspace(x_range[0],x_range[1],nb_points):
            noise = random.uniform(-amp,amp)*p["noise"]
            ret_x.append(x)
            ret_y.append(
                amp*np.sin(np.pi*(x+p["phase"])*2/p["cycle"])+
                diff+
                noise+
                trend
            )
            trend += amp*p["trend"]/100
        sample.append({"x":ret_x, "y":ret_y, "label":n})
    #
    return sample

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    def test(wave_profile=None):
        ret = wave_sample(nb_points=240,
                          x_range=(0,60),
                          wave_profile=wave_profile,
                          random_seed=0
                        )
        print(ret)
        fig = plt.figure()
        for d in ret:
            plt.plot(d["x"], d["y"], label=d["label"])
        fig.legend()
        plt.tight_layout()
        plt.show()
    #
    test()
    #
    test({
            "A": { "max": 50., "min": 30.,
                  "cycle": 12., "phase": 0,
                  "trend": 0, "noise": 0 },
            "B": { "max": 50., "min": 30.,
                  "cycle": 6., "phase": 0,
                  "trend": 0, "noise": 0 },
            "C": { "max": 50., "min": 30.,
                  "cycle": 12., "phase": 6,
                  "trend": 0, "noise": 0 },
            "D": { "max": 20., "min": 0.,
                  "cycle": 12., "phase": 0,
                  "trend": 0, "noise": 0 },
            "E": { "max": 20., "min": 0.,
                  "cycle": 12., "phase": 0,
                  "trend": 0, "noise": 0.2 },
            })
    #
    test({
        "A": { "max": 50., "min": 30.,
                "cycle": 12., "phase": 0,
                "trend": 0, "noise": 0.2 },
        "B": { "max": 45., "min": 35.,
                "cycle": 12., "phase": 0,
                "trend": 0, "noise": 0.1 },
        "C": { "max": 40., "min": 30.,
                "cycle": 12., "phase": 0,
                "trend": 0, "noise": 0.1 },
        "D": { "max": 30., "min": 10.,
                "cycle": 12., "phase": 0,
                "trend": 0.5, "noise": 0.1 },
        "E": { "max": 30., "min": 15.,
                "cycle": 12., "phase": 0,
                "trend": 0, "noise": 0.1 },
        "F": { "max": 25., "min": 10.,
                "cycle": 12., "phase": 0,
                "trend": 0, "noise": 0.1 },
        "G": { "max": 15., "min": -20.,
                "cycle": 12., "phase": 0,
                "trend": -0.5, "noise": 0.1 },
        "H": { "max": 10., "min": -10.,
                "cycle": 12., "phase": 0,
                "trend": 0, "noise": 0.1 },
        "I": { "max":  0., "min": -30.,
                "cycle": 12., "phase": 0,
                "trend": 0, "noise": 0.1 },
        })
