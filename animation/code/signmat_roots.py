from manimlib.imports import *
import os
import pyclbr

class PlotFunctions(Scene):
  def construct(self):
    mat = TexMobject(r"\begin{array}{cccccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, x_3) & x_3 & (x_3, \infty) \\ p_1' & - & - & - & - & - & 0 & + \\ p_2 & + & 0 & - & - & - & 0 & + \\ r_1 & - & - & - & - & - & - & - \\ r_2 & + & + & + & 0 & - & - & - \\ \\ p_1 & ? & ? & ? & \varnothing & ? & ? & ? \end{array}")

    VGroup(mat[0][33], mat[0][34], mat[0][35]).set_color(YELLOW)
    VGroup(mat[0][43], mat[0][44]).set_color(BLUE)
    VGroup(mat[0][52], mat[0][53]).set_color(YELLOW)
    VGroup(mat[0][61], mat[0][62]).set_color(BLUE)
    
    VGroup(mat[0][70], mat[0][71]).set_color(GREEN)

    VGroup(*[mat[0][i] for i in range(72, 79)]).set_color(BLACK)

    self.play(Write(mat))
    self.wait()

    l = [37, 46, 70, 71]
    anims = []
    for i in range(len(mat[0])):
      if i in l:
        anims.append(ApplyMethod(mat[0][i].set_opacity, 1))
      else:
        anims.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
    
    self.play(*anims)
    self.wait()

    self.play(ApplyMethod(mat[0][46].set_color, BLUE))
    self.wait()
    self.play(ApplyMethod(VGroup(mat[0][43], mat[0][44]).set_opacity, 1), ApplyMethod(VGroup(mat[0][61], mat[0][62]).set_opacity, 1), ApplyMethod(mat[0][64].set_opacity, 1))
    self.wait()
    self.play(ApplyMethod(mat[0][64].set_color, BLUE))
    self.wait()

    self.play(ApplyMethod(mat[0][64].deepcopy().move_to, mat[0][73]))
    self.wait()

    l = [ 39, 48, 70, 71]
    anims = []
    for i in range(len(mat[0])):
      if i in l:
        anims.append(ApplyMethod(mat[0][i].set_opacity, 1))
      else:
        anims.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
    
    self.play(*anims)
    self.wait()
    mat[0][75].set_opacity(1)
    self.play(ApplyMethod(mat[0][75].set_color, RED))
    self.wait()

    l = [41, 50, 70, 71]
    anims = []
    for i in range(len(mat[0])):
      if i in l:
        anims.append(ApplyMethod(mat[0][i].set_opacity, 1))
      else:
        anims.append(ApplyMethod(mat[0][i].set_opacity, 0.3))
    
    self.play(*anims)
    self.wait()

    self.play(ApplyMethod(mat[0][41].set_color, YELLOW))
    self.wait()
    self.play(ApplyMethod(VGroup(mat[0][33], mat[0][34], mat[0][35]).set_opacity, 1), ApplyMethod(VGroup(mat[0][52], mat[0][53]).set_opacity, 1), ApplyMethod(mat[0][59].set_opacity, 1))
    self.wait()
    self.play(ApplyMethod(mat[0][59].set_color, YELLOW))
    self.wait()

    self.play(ApplyMethod(mat[0][59].deepcopy().move_to, mat[0][77]))
    self.wait()

    anims = []
    for i in range(len(mat[0])):
      anims.append(ApplyMethod(mat[0][i].set_opacity, 1))
    
    self.play(*anims)
    self.wait(3)
