from manimlib.imports import *
import os
import pyclbr

class PlotFunctions(Scene):
  def construct(self):
    div = TexMobject(r"p_1(x_k)", r"=", r"p_i", r"(x_k)", r"q_i(x_k)", r"+", r"r_i(x_k)")
    div.move_to(0.5*DOWN)
    div[2].set_color(YELLOW)
    txt = TextMobject(r"If $x_k$ is a root of ", r"$p_i$")
    txt[1].set_color(YELLOW)
    txt.move_to(0.5*UP)

    vg = VGroup(div[2], div[3])
    zero = TexMobject(r"0")
    zero.set_color(RED)
    zero.move_to(vg)

    div3 = TexMobject(r"\mathrm{sign}(p_1(x_k)) = \mathrm{sign}(r_i(x_k))")
    div3.move_to(div)

    self.play(Write(div))
    self.play(Write(txt))
    self.wait(2)
    self.play(ReplacementTransform(vg, zero))
    self.wait(2)
    self.play(FadeOut(vg), FadeOut(div[4]), FadeOut(div[5]), FadeOut(zero))
    self.wait(2)
    vg.set_opacity(0)
    div[4].set_opacity(0)
    div[5].set_opacity(0)
    zero.set_opacity(0)
    self.play(Transform(div, div3))

    self.wait(3)