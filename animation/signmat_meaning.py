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

    gp1_1 = self.get_graph(self.p1,color=BLUE,x_min=-2,x_max=-1)
    gp2_1 = self.get_graph(self.p2,color=YELLOW,x_min=-2,x_max=-1)
    gp3_1 = self.get_graph(self.p3,color=PURPLE,x_min=-2,x_max=-1)
    gp1_1.set_stroke(width=8)
    gp2_1.set_stroke(width=8)
    gp3_1.set_stroke(width=8)

    sym1_1 = TexMobject("+")
    sym1_1.move_to(mat[0][26])
    sym1_1.set_color(BLUE)
    sym2_1 = TexMobject("-")
    sym2_1.move_to(mat[0][33])
    sym2_1.set_color(YELLOW)
    sym3_1 = TexMobject("+")
    sym3_1.set_color(PURPLE)
    sym3_1.move_to(mat[0][40])


    self.play(ApplyMethod(mat[0][26].set_color, WHITE), ApplyMethod(mat[0][33].set_color, WHITE), ApplyMethod(mat[0][40].set_color, WHITE))
    self.wait(1)
    self.play(ReplacementTransform(mat[0][26], gp1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp1_1, sym1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][33], gp2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp2_1, sym2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][40], gp3_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp3_1, sym3_1), run_time=1)
    self.wait(1)

    gp1_1 = Dot(color=BLUE).move_to(self.coords_to_point(-1, self.p1(-1)))
    gp2_1 = Dot(color=YELLOW).move_to(self.coords_to_point(-1, self.p2(-1)))
    gp3_1 = Dot(color=PURPLE).move_to(self.coords_to_point(-1, self.p3(-1)))
    gp1_1.set_stroke(width=8)
    gp2_1.set_stroke(width=8)
    gp3_1.set_stroke(width=8)

    sym1_2 = TexMobject("0")
    sym1_2.move_to(mat[0][27])
    sym1_2.set_color(BLUE)
    sym2_2 = TexMobject("0")
    sym2_2.move_to(mat[0][34])
    sym2_2.set_color(YELLOW)
    sym3_2 = TexMobject("+")
    sym3_2.move_to(mat[0][41])
    sym3_2.set_color(PURPLE)

    self.play(ApplyMethod(mat[0][27].set_color, WHITE), ApplyMethod(mat[0][34].set_color, WHITE), ApplyMethod(mat[0][41].set_color, WHITE))
    self.wait(1)
    self.play(ReplacementTransform(mat[0][27], gp1_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp1_1, sym1_2), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][34], gp2_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp2_1, sym2_2), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(mat[0][41], gp3_1), run_time=1)
    self.wait(1)
    self.play(ReplacementTransform(gp3_1, sym3_2), run_time=1)
    self.wait(1)

    gp1_3 = self.get_graph(self.p1,color=BLUE,x_min=-1,x_max=1)
    gp2_3 = self.get_graph(self.p2,color=YELLOW,x_min=-1,x_max=1)
    gp3_3 = self.get_graph(self.p3,color=PURPLE,x_min=-1,x_max=1)
    gp1_3.set_stroke(width=8)
    gp2_3.set_stroke(width=8)
    gp3_3.set_stroke(width=8)

    gp1_4 = Dot(color=BLUE).move_to(self.coords_to_point(1, self.p1(1)))
    gp2_4 = Dot(color=YELLOW).move_to(self.coords_to_point(1, self.p2(1)))
    gp3_4 = Dot(color=PURPLE).move_to(self.coords_to_point(1, self.p3(1)))
    gp1_4.set_stroke(width=8)
    gp2_4.set_stroke(width=8)
    gp3_4.set_stroke(width=8)

    gp1_5 = self.get_graph(self.p1,color=BLUE,x_min=1,x_max=2)
    gp2_5 = self.get_graph(self.p2,color=YELLOW,x_min=1,x_max=2)
    gp3_5 = self.get_graph(self.p3,color=PURPLE,x_min=1,x_max=2)
    gp1_5.set_stroke(width=8)
    gp2_5.set_stroke(width=8)
    gp3_5.set_stroke(width=8)

    sym1_3 = TexMobject("-")
    sym1_3.move_to(mat[0][28])
    sym1_3.set_color(BLUE)
    sym2_3 = TexMobject("+")
    sym2_3.move_to(mat[0][35])
    sym2_3.set_color(YELLOW)
    sym3_3 = TexMobject("+")
    sym3_3.set_color(PURPLE)
    sym3_3.move_to(mat[0][42])

    sym1_4 = TexMobject("0")
    sym1_4.move_to(mat[0][29])
    sym1_4.set_color(BLUE)
    sym2_4 = TexMobject("+")
    sym2_4.move_to(mat[0][36])
    sym2_4.set_color(YELLOW)
    sym3_4 = TexMobject("0")
    sym3_4.move_to(mat[0][43])
    sym3_4.set_color(PURPLE)

    sym1_5 = TexMobject("+")
    sym1_5.move_to(mat[0][30])
    sym1_5.set_color(BLUE)
    sym2_5 = TexMobject("+")
    sym2_5.move_to(mat[0][37])
    sym2_5.set_color(YELLOW)
    sym3_5 = TexMobject("-")
    sym3_5.set_color(PURPLE)
    sym3_5.move_to(mat[0][44])

    self.play(AnimationGroup(ApplyMethod(mat[0][28].set_color, WHITE), ApplyMethod(mat[0][35].set_color, WHITE), ApplyMethod(mat[0][42].set_color, WHITE),
      ApplyMethod(mat[0][29].set_color, WHITE), ApplyMethod(mat[0][36].set_color, WHITE), ApplyMethod(mat[0][43].set_color, WHITE),
      ApplyMethod(mat[0][30].set_color, WHITE), ApplyMethod(mat[0][37].set_color, WHITE), ApplyMethod(mat[0][44].set_color, WHITE), lag_ratio=0.2))
    self.play(AnimationGroup(ReplacementTransform(mat[0][28], gp1_3), ReplacementTransform(mat[0][35], gp2_3), ReplacementTransform(mat[0][42], gp3_3),
      ReplacementTransform(mat[0][29], gp1_4), ReplacementTransform(mat[0][36], gp2_4), ReplacementTransform(mat[0][43], gp3_4),
      ReplacementTransform(mat[0][30], gp1_5), ReplacementTransform(mat[0][37], gp2_5), ReplacementTransform(mat[0][44], gp3_5), lag_ratio=0.5), run_time=3)
    self.wait()
    self.play(AnimationGroup(ReplacementTransform(gp1_3, sym1_3), ReplacementTransform(gp2_3, sym2_3), ReplacementTransform(gp3_3, sym3_3),
      ReplacementTransform(gp1_4, sym1_4), ReplacementTransform(gp2_4, sym2_4), ReplacementTransform(gp3_4, sym3_4),
      ReplacementTransform(gp1_5, sym1_5), ReplacementTransform(gp2_5, sym2_5), ReplacementTransform(gp3_5, sym3_5), lag_ratio=0.5), run_time=3)
    
    self.wait(5)



  def p1(self,x):
    return 0.2 * x**2 - 0.2

  def p2(self,x):
    return 0.05 * (x + 1)**3
  
  def p3(self,x):
    return -0.25*x + 0.25
    
    
