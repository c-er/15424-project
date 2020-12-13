from manimlib.imports import *
import os
import pyclbr

class PlotFunctions(Scene):
  def construct(self):
    mat = TexMobject(r"\begin{array}{cccccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, x_3) & x_3 & (x_3, \infty) \\ p_1' & - & - & - & - & - & 0 & + \\ p_2 & + & 0 & - & - & - & 0 & + \\ r_1 & - & - & - & - & - & - & - \\ r_2 & + & + & + & 0 & - & - & - \\ \\ p_1 & ? & + & ? & \varnothing & ? & - & ? \end{array}")

    VGroup(mat[0][33], mat[0][34], mat[0][35]).set_color(YELLOW)
    VGroup(mat[0][43], mat[0][44]).set_color(BLUE)
    VGroup(mat[0][52], mat[0][53]).set_color(YELLOW)
    VGroup(mat[0][61], mat[0][62]).set_color(BLUE)
    
    VGroup(mat[0][70], mat[0][71]).set_color(GREEN)

    VGroup(*[mat[0][i] for i in range(72, 79)]).set_color(BLACK)
    mat[0][73].set_color(BLUE)
    mat[0][75].set_color(RED)
    mat[0][77].set_color(YELLOW)

    self.play(Write(mat))
    self.wait(1.5)

    self.play(FadeOut(VGroup(*list(mat[0][i] for i in range(52,70)))))
    self.wait(1.5)

    l = list(range(9, 25)) + [38, 39, 40, 47, 48, 49, 75]
    anims = []
    for i in range(len(mat[0])):
      if i in l:
        anims.append(ApplyMethod(mat[0][i].set_opacity, 1))
      elif i not in range(52,70):
        anims.append(ApplyMethod(mat[0][i].set_opacity, 0.3))

    self.play(*anims)
    self.wait(1.5)

    l = list(range(16, 25)) + [39, 40, 48, 49, 75]
    anims = []
    for i in l:
      anims.append(FadeOut(mat[0][i]))
    
    vg = VGroup(*(mat[0][i] for i in range(9, 16)))
    newlab = TexMobject("(x_1, x_3)")
    newlab.move_to(vg)
    self.play(*anims)
    self.play(ReplacementTransform(vg, newlab))
    self.wait(1.5)

    l = list(range(0, 16)) + list(range(25, 39)) + list(range(41, 48)) + [50, 51] + [70, 71, 73, 77]
    anims = []
    for i in l:
      anims.append(ApplyMethod(mat[0][i].set_opacity, 1))
    
    self.play(*anims)
    self.wait(0.5)

    anims = []
    vgs = VGroup(*(mat[0][i] for i in range(25, 27)))
    vgd = VGroup(*(mat[0][i] for i in range(16, 18)))
    anims.append(ApplyMethod(vgs.move_to, vgd))

    vgs = VGroup(*(mat[0][i] for i in range(27, 33)))
    vgd = VGroup(*(mat[0][i] for i in range(18, 26)))
    anims.append(ApplyMethod(vgs.move_to, vgd))

    anims.append(ApplyMethod(mat[0][41].move_to, mat[0][39]))
    anims.append(ApplyMethod(mat[0][42].move_to, mat[0][40]))

    anims.append(ApplyMethod(mat[0][50].move_to, mat[0][48]))
    anims.append(ApplyMethod(mat[0][51].move_to, mat[0][49]))

    anims.append(ApplyMethod(mat[0][77].move_to, mat[0][75]))

    self.play(*anims)
    


    self.wait(3)

    