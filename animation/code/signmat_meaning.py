from manimlib.imports import *
import os
import pyclbr
class PlotFunctions(GraphScene):
  CONFIG = {
    "x_min" : -2,
    "x_max" : 2,
    "y_min" : -0.5,
    "y_max" : 2,
    "graph_origin" : 2 * UP ,
    "function_color" : PURPLE ,
    "axes_color" : GREEN,
    "x_axis_label": "",
    "y_axis_label": "",
    "x_tick_frequency": 1,
    "y_tick_frequency": 1
  }

  CUSTOM_CONFIG = {
      "color": LIGHT_GREY,
      "x_min": -FRAME_X_RADIUS,
      "x_max": FRAME_X_RADIUS,
      "unit_size": 1,
      "include_ticks": False,  # this boolean controls tick generation
      "tick_size": 0.1,
      "tick_frequency": 1,
      # Defaults to value near x_min s.t. 0 is a tick
      # TODO, rename this
      "leftmost_tick": None,
      # Change name
      "numbers_with_elongated_ticks": [0],
      "include_numbers": False,
      "numbers_to_show": None,
      "longer_tick_multiple": 2,
      "number_at_center": 0,
      "number_scale_val": 0.75,
      "label_direction": DOWN,
      "line_to_number_buff": MED_SMALL_BUFF,
      "include_tip": False,
      "tip_width": 0.25,
      "tip_height": 0.25,
      "decimal_number_config": {"num_decimal_places": 0},
      "exclude_zero_from_default_numbers": False,
  }

  NumberLine.CONFIG = CUSTOM_CONFIG

  def construct(self):
    # axes = Axes(x_min=-2, x_max=2, y_min=-1.2, y_max=2, color=GREEN)
    self.setup_axes(animate=True)

    gp1 = self.get_graph(self.p1,color=BLUE)
    gp1_lab = self.get_graph_label(gp1, label=r"p_1")

    gp2 = self.get_graph(self.p2,color=YELLOW)
    gp2_lab = self.get_graph_label(gp2, label=r"p_2", direction=UP/2)

    gp3 = self.get_graph(self.p3,color=PURPLE)
    gp3_lab = self.get_graph_label(gp3, label=r"p_3")

    root1 = Dot(color=WHITE).move_to(self.coords_to_point(-1,0))
    root1_lab = TexMobject(r"x_1")
    root1_lab.next_to(root1,DOWN)

    root2 = Dot(color=WHITE).move_to(self.coords_to_point(1,0))
    root2_lab = TexMobject(r"x_2")
    root2_lab.next_to(root2,DOWN)

    self.play(ShowCreation(gp1), ShowCreation(gp2),ShowCreation(gp3))
    self.play(ShowCreation(gp1_lab), ShowCreation(gp2_lab), ShowCreation(gp3_lab))
    self.play(ShowCreation(root1),ShowCreation(root2))
    self.play(ShowCreation(root1_lab),ShowCreation(root2_lab))

    self.wait()

    mat = TexMobject(r"\begin{array}{cccccc} & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\ p_1 & ? & ? & ? & ? & ? \\ p_2 & ? & ? & ? & ? & ? \\ p_3 & ? & ? & ? & ? & ? \end{array}")
    mat.move_to(2*DOWN)
    mat[0][24].set_color(BLUE)
    mat[0][25].set_color(BLUE)
    mat[0][26].set_color(BLACK)
    mat[0][27].set_color(BLACK)
    mat[0][28].set_color(BLACK)
    mat[0][29].set_color(BLACK)
    mat[0][30].set_color(BLACK)

    mat[0][31].set_color(YELLOW)
    mat[0][32].set_color(YELLOW)
    mat[0][33].set_color(BLACK)
    mat[0][34].set_color(BLACK)
    mat[0][35].set_color(BLACK)
    mat[0][36].set_color(BLACK)
    mat[0][37].set_color(BLACK)

    mat[0][38].set_color(PURPLE)
    mat[0][39].set_color(PURPLE)
    mat[0][40].set_color(BLACK)
    mat[0][41].set_color(BLACK)
    mat[0][42].set_color(BLACK)
    mat[0][43].set_color(BLACK)
    mat[0][44].set_color(BLACK)
    
    self.play(Write(mat))

    self.play(ApplyMethod(gp1.set_color, GREY), ApplyMethod(gp2.set_color, GREY), ApplyMethod(gp3.set_color, GREY))
    self.wait()

    xmn = -2
    xmx = -1
    gp1_1 = self.get_graph(self.p1,color=BLUE,x_min=xmn,x_max=xmx)
    gp2_1 = self.get_graph(self.p2,color=YELLOW,x_min=xmn,x_max=xmx)
    gp3_1 = self.get_graph(self.p3,color=PURPLE,x_min=xmn,x_max=xmx)
    gp1_1.set_stroke(width=8)
    gp2_1.set_stroke(width=8)
    gp3_1.set_stroke(width=8)

    v1 = 26
    v2 = 33
    v3 = 40
    sym1_1 = TexMobject("+")
    sym1_1.move_to(mat[0][v1])
    sym1_1.set_color(BLUE)
    sym2_1 = TexMobject("-")
    sym2_1.move_to(mat[0][v2])
    sym2_1.set_color(YELLOW)
    sym3_1 = TexMobject("+")
    sym3_1.set_color(PURPLE)
    sym3_1.move_to(mat[0][v3])
    l = [sym1_1, sym2_1, sym3_1]


    self.play(ApplyMethod(mat[0][v1].set_color, WHITE), ApplyMethod(mat[0][v2].set_color, WHITE), ApplyMethod(mat[0][v3].set_color, WHITE))
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v1], gp1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp1_1, l[0]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v2], gp2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp2_1, l[1]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v3], gp3_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp3_1, l[2]), run_time=1)
    self.wait(2)

    x = -1
    gp1_1 = Dot(color=BLUE).move_to(self.coords_to_point(x, self.p1(x)))
    gp2_1 = Dot(color=YELLOW).move_to(self.coords_to_point(x, self.p2(x)))
    gp3_1 = Dot(color=PURPLE).move_to(self.coords_to_point(x, self.p3(x)))
    gp1_1.set_stroke(width=8)
    gp2_1.set_stroke(width=8)
    gp3_1.set_stroke(width=8)

    v1 = 27
    v2 = 34
    v3 = 41
    sym1_2 = TexMobject("0")
    sym1_2.move_to(mat[0][v1])
    sym1_2.set_color(BLUE)
    sym2_2 = TexMobject("0")
    sym2_2.move_to(mat[0][v2])
    sym2_2.set_color(YELLOW)
    sym3_2 = TexMobject("+")
    sym3_2.move_to(mat[0][v3])
    sym3_2.set_color(PURPLE)
    l = [sym1_2, sym2_2, sym3_2]

    self.play(ApplyMethod(mat[0][v1].set_color, WHITE), ApplyMethod(mat[0][v2].set_color, WHITE), ApplyMethod(mat[0][v3].set_color, WHITE))
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v1], gp1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp1_1, l[0]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v2], gp2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp2_1, l[1]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v3], gp3_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp3_1, l[2]), run_time=1)
    self.wait(2)


    xmn = -1
    xmx = 1
    gp1_1 = self.get_graph(self.p1,color=BLUE,x_min=xmn,x_max=xmx)
    gp2_1 = self.get_graph(self.p2,color=YELLOW,x_min=xmn,x_max=xmx)
    gp3_1 = self.get_graph(self.p3,color=PURPLE,x_min=xmn,x_max=xmx)
    gp1_1.set_stroke(width=8)
    gp2_1.set_stroke(width=8)
    gp3_1.set_stroke(width=8)

    v1 = 28
    v2 = 35
    v3 = 42
    sym1_1 = TexMobject("-")
    sym1_1.move_to(mat[0][v1])
    sym1_1.set_color(BLUE)
    sym2_1 = TexMobject("+")
    sym2_1.move_to(mat[0][v2])
    sym2_1.set_color(YELLOW)
    sym3_1 = TexMobject("+")
    sym3_1.set_color(PURPLE)
    sym3_1.move_to(mat[0][v3])
    l = [sym1_1, sym2_1, sym3_1]


    self.play(ApplyMethod(mat[0][v1].set_color, WHITE), ApplyMethod(mat[0][v2].set_color, WHITE), ApplyMethod(mat[0][v3].set_color, WHITE))
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v1], gp1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp1_1, l[0]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v2], gp2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp2_1, l[1]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v3], gp3_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp3_1, l[2]), run_time=1)
    self.wait(2)

    x = 1
    gp1_1 = Dot(color=BLUE).move_to(self.coords_to_point(x, self.p1(x)))
    gp2_1 = Dot(color=YELLOW).move_to(self.coords_to_point(x, self.p2(x)))
    gp3_1 = Dot(color=PURPLE).move_to(self.coords_to_point(x, self.p3(x)))
    gp1_1.set_stroke(width=8)
    gp2_1.set_stroke(width=8)
    gp3_1.set_stroke(width=8)

    v1 = 29
    v2 = 36
    v3 = 43
    sym1_2 = TexMobject("0")
    sym1_2.move_to(mat[0][v1])
    sym1_2.set_color(BLUE)
    sym2_2 = TexMobject("+")
    sym2_2.move_to(mat[0][v2])
    sym2_2.set_color(YELLOW)
    sym3_2 = TexMobject("0")
    sym3_2.move_to(mat[0][v3])
    sym3_2.set_color(PURPLE)
    l = [sym1_2, sym2_2, sym3_2]

    self.play(ApplyMethod(mat[0][v1].set_color, WHITE), ApplyMethod(mat[0][v2].set_color, WHITE), ApplyMethod(mat[0][v3].set_color, WHITE))
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v1], gp1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp1_1, l[0]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v2], gp2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp2_1, l[1]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v3], gp3_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp3_1, l[2]), run_time=1)
    self.wait(2)

    xmn = 1
    xmx = 2
    gp1_1 = self.get_graph(self.p1,color=BLUE,x_min=xmn,x_max=xmx)
    gp2_1 = self.get_graph(self.p2,color=YELLOW,x_min=xmn,x_max=xmx)
    gp3_1 = self.get_graph(self.p3,color=PURPLE,x_min=xmn,x_max=xmx)
    gp1_1.set_stroke(width=8)
    gp2_1.set_stroke(width=8)
    gp3_1.set_stroke(width=8)

    v1 = 30
    v2 = 37
    v3 = 44
    sym1_1 = TexMobject("+")
    sym1_1.move_to(mat[0][v1])
    sym1_1.set_color(BLUE)
    sym2_1 = TexMobject("+")
    sym2_1.move_to(mat[0][v2])
    sym2_1.set_color(YELLOW)
    sym3_1 = TexMobject("-")
    sym3_1.set_color(PURPLE)
    sym3_1.move_to(mat[0][v3])
    l = [sym1_1, sym2_1, sym3_1]


    self.play(ApplyMethod(mat[0][v1].set_color, WHITE), ApplyMethod(mat[0][v2].set_color, WHITE), ApplyMethod(mat[0][v3].set_color, WHITE))
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v1], gp1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp1_1, l[0]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v2], gp2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp2_1, l[1]), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][v3], gp3_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp3_1, l[2]), run_time=1)
    self.wait(5)



  def p1(self,x):
    return 0.2 * x**2 - 0.2

  def p2(self,x):
    return 0.05 * (x + 1)**3
  
  def p3(self,x):
    return -0.25*x + 0.25
    
    
