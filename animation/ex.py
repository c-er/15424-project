from manimlib.imports import *

class Plot2(Scene):
    def construct(self):
        c1 = FunctionGraph(lambda x: 2*np.exp(-2*(x-1)**2))
        c2 = FunctionGraph(lambda x: x**2)
        axes1=Axes(y_min=-3,y_max=3)
        axes2=Axes(y_min=0,y_max=10)
        self.play(ShowCreation(axes1),ShowCreation(c1))
        self.wait()
        self.play(
            ReplacementTransform(axes1,axes2),
            ReplacementTransform(c1,c2)
        )
        self.wait()